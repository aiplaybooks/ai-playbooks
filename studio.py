"""AI Playbooks Studio: local workflow engine + web UI (n8n-style canvas) for the daily pipeline.

Usage:
    python studio.py [--port 8787] [--no-browser]
    then open http://localhost:8787

Three workflows:
    scan  (scheduled, default 08:00 + 18:00; missed slots run at startup)
          trigger -> collect (news.py) -> scout (Claude: web search, verify, rank) -> choose (owner picks in the UI)
    post  (one per picked candidate, one at a time)
          write (Claude: verify + content JSON) -> cover (Wikimedia photo or Flux) -> carousel -> qa (Claude looks
          at the output, fixes) -> approve (owner: publish / revise / reject; can be switched off) -> upload
          -> ig_carousel -> fb_photos -> log (publish_log.jsonl + git commit/push)
    clip  (viral Reel: the owner pastes an X/post link)
          fetch (yt-dlp) -> hook (Claude watches frames, writes hook + caption) -> frame (clip.py) -> approve
          -> upload -> ig_reel -> fb_reel -> log
State lives in runs/<run-id>/state.json, logs in runs/<run-id>/<node>.log; a failed node can be retried from the UI.
Claude steps run `claude -p` (Claude Code headless) with the prompts in prompts/.
"""
import sys, os, re, json, time, queue, shutil, pathlib, argparse, threading, subprocess, webbrowser, urllib.parse
from datetime import datetime, timedelta
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

ROOT = pathlib.Path(__file__).parent.resolve()
RUNS = ROOT / "runs"
SETTINGS = RUNS / "settings.json"
PY = str(pathlib.Path(sys.executable).with_name("python.exe")) if sys.executable.lower().endswith("pythonw.exe") else sys.executable
CLAUDE = shutil.which("claude") or "claude"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
CLAUDE_TOOLS = ["WebSearch", "WebFetch", "Read", "Write", "Edit", "Glob", "Grep",
                "Bash(python carousel.py:*)", "Bash(python reel.py:*)", "Bash(python news.py:*)",
                "Bash(python cover.py:*)", "Bash(python clip.py:*)"]

SCAN = [("trigger", "Zamanlayıcı", "trigger"), ("collect", "Haber topla", "code"),
        ("scout", "Ara, doğrula, sırala", "ai"), ("choose", "Senin seçimin", "human")]
POST = [("write", "Doğrula & yaz", "ai"), ("cover", "Kapak görseli", "code"), ("carousel", "Carousel", "code"),
        ("qa", "Kalite kontrol", "ai"), ("approve", "Yayından önce onay", "human"), ("upload", "Medya yükle", "code"),
        ("ig_carousel", "Instagram carousel", "publish"), ("fb_photos", "Facebook gönderi", "publish"),
        ("log", "Kayıt & GitHub", "code")]
CLIP = [("fetch", "Videoyu indir", "code"), ("hook", "Hook & caption", "ai"), ("frame", "Reel çerçevesi", "code"),
        ("approve", "Yayından önce onay", "human"), ("upload", "Medya yükle", "code"), ("ig_reel", "Instagram Reel", "publish"),
        ("fb_reel", "Facebook Reel", "publish"), ("log", "Kayıt & GitHub", "code")]
FLOWS = {"scan": SCAN, "post": POST, "clip": CLIP}

LOCK = threading.RLock()
POST_Q = queue.Queue()
PROCS = {}  # run id -> running Popen (for cancel)
CANCELED = set()  # run ids the owner stopped


class StepError(Exception):
    pass


class Canceled(Exception):
    pass


def now():
    return datetime.now().astimezone()


def iso(d=None):
    return (d or now()).isoformat(timespec="seconds")


def slog(*a):
    line = f"{now():%Y-%m-%d %H:%M:%S} " + " ".join(str(x) for x in a)
    with (RUNS / "studio.log").open("a", encoding="utf-8") as f: f.write(line + "\n")
    if sys.stdout: print(line, flush=True)


def read_json(p, default=None):
    try: return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError): return default


def write_json(p, data):
    p = pathlib.Path(p); tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8"); os.replace(tmp, p)


def settings():
    s = {"scan_times": ["08:00", "18:00"], "approval": True, "last_slot": None}
    s.update(read_json(SETTINGS, {}) or {})
    return s


def save_settings(s):
    with LOCK: write_json(SETTINGS, s)


def notify(title, text):
    """Windows toast (best effort)."""
    q = lambda s: s.replace("'", "''")
    ps = ("[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;"
          "$x=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
          f"$t=$x.GetElementsByTagName('text'); $t.Item(0).AppendChild($x.CreateTextNode('{q(title)}')) > $null;"
          f"$t.Item(1).AppendChild($x.CreateTextNode('{q(text)}')) > $null;"
          "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("
          "'{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe')"
          ".Show([Windows.UI.Notifications.ToastNotification]::new($x))")
    try: subprocess.Popen(["powershell", "-NoProfile", "-Command", ps], creationflags=NO_WINDOW)
    except OSError: pass


# ---------------------------------------------------------------- runs

class Run:
    def __init__(self, rid):
        self.id = rid; self.dir = RUNS / rid
        self.s = read_json(self.dir / "state.json")
        if self.s:  # runs created before a node was added to the flow get it as idle
            for n, _, _ in FLOWS[self.s["kind"]]: self.s["nodes"].setdefault(n, {"status": "idle"})

    @classmethod
    def create(cls, kind, rid, **extra):
        d = RUNS / rid; d.mkdir(parents=True, exist_ok=True)
        s = {"id": rid, "kind": kind, "created": iso(), "status": "queued",
             "nodes": {n: {"status": "idle"} for n, _, _ in FLOWS[kind]}, **extra}
        write_json(d / "state.json", s)
        return cls(rid)

    def save(self):
        with LOCK: write_json(self.dir / "state.json", self.s)

    def node(self, nid, **kw):
        with LOCK:
            self.s["nodes"][nid].update(kw); self.save()

    def status(self, st, **kw):
        with LOCK:
            self.s["status"] = st; self.s.update(kw); self.save()

    def log(self, nid, text):
        with (self.dir / f"{nid}.log").open("a", encoding="utf-8") as f: f.write(text.rstrip("\n") + "\n")

    def reset_from(self, nid):
        ids = [n for n, _, _ in FLOWS[self.s["kind"]]]
        with LOCK:
            for n in ids[ids.index(nid):]:
                old = self.s["nodes"][n]; tries = old.get("attempts", [])
                if old.get("started"):  # keep earlier attempts: they count in the time breakdown
                    tries = tries + [{k: old.get(k) for k in ("started", "ended", "status", "msg")}]
                    self.log(n, f"\n----- yeni deneme {iso()} -----")
                self.s["nodes"][n] = {"status": "idle", **({"attempts": tries} if tries else {})}
            self.save()


def all_runs():
    out = []
    for d in RUNS.iterdir() if RUNS.exists() else []:
        s = read_json(d / "state.json")
        if s: out.append(s)
    return sorted(out, key=lambda s: s["created"], reverse=True)


def sh(run, nid, cmd, env=None):
    """Run a command, stream its output into the node log."""
    env = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8", **(env or {}))
    env.pop("CLAUDECODE", None)
    run.log(nid, "$ " + " ".join(str(c) for c in cmd))
    p = subprocess.Popen([str(c) for c in cmd], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace", env=env,
                         creationflags=NO_WINDOW)
    PROCS[run.id] = p
    tail = []
    try:
        for line in p.stdout:
            run.log(nid, line); tail = (tail + [line.strip()])[-5:]
        rc = p.wait()
    finally:
        PROCS.pop(run.id, None)
    if run.id in CANCELED: raise Canceled()
    if rc: raise StepError(next((t for t in reversed(tail) if t), f"çıkış kodu {rc}")[:300])
    return tail


def claude(run, nid, template, **fields):
    """Run Claude Code headless with a prompt from prompts/, stream a readable log."""
    prompt = (ROOT / "prompts" / f"{template}.md").read_text(encoding="utf-8").format(**fields)
    (run.dir / f"{nid}.prompt.md").write_text(prompt, encoding="utf-8")
    env = dict(os.environ, PYTHONIOENCODING="utf-8"); env.pop("CLAUDECODE", None)
    cmd = [CLAUDE, "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "acceptEdits",
           "--allowedTools", *CLAUDE_TOOLS]
    run.log(nid, f"$ claude -p < prompts/{template}.md")
    p = subprocess.Popen(cmd, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace", env=env, creationflags=NO_WINDOW)
    PROCS[run.id] = p
    result = None
    try:
        p.stdin.write(prompt); p.stdin.close()
        for line in p.stdout:
            try: ev = json.loads(line)
            except ValueError:
                if line.strip(): run.log(nid, line)
                continue
            if ev.get("type") == "assistant":
                for c in ev.get("message", {}).get("content", []):
                    if c.get("type") == "text" and c["text"].strip(): run.log(nid, "💬 " + c["text"].strip())
                    elif c.get("type") == "tool_use":
                        i = c.get("input", {})
                        arg = i.get("query") or i.get("url") or i.get("file_path") or i.get("command") or i.get("pattern") or ""
                        run.log(nid, f"🔧 {c['name']}: {str(arg)[:200]}")
            elif ev.get("type") == "result":
                result = ev
                run.log(nid, f"✔ bitti · {ev.get('num_turns', '?')} adım · {ev.get('duration_ms', 0) / 60000:.1f} dk")
        p.wait()
    finally:
        PROCS.pop(run.id, None)
    if run.id in CANCELED: raise Canceled()
    if not result or result.get("is_error") or result.get("subtype") != "success":
        raise StepError(f"Claude başarısız: {(result or {}).get('result') or (result or {}).get('subtype') or 'sonuç yok'}"[:300])
    return result.get("result", "")


# ---------------------------------------------------------------- scan nodes

def n_trigger(run):
    return run.s.get("trigger_msg", "Elle başlatıldı")


def n_collect(run):
    tail = sh(run, "collect", [PY, "news.py", "--hours", "36"])
    msg = next((t for t in reversed(tail) if "items" in t), "tamam").split("->")[0].strip()
    try: sh(run, "collect", [PY, "viral.py"])  # trending AI videos for the Viral tab; never fails the scan
    except StepError as ex: run.log("collect", f"viral.py: {ex}")
    return msg


def n_scout(run):
    day = run.s["day"]
    out = ROOT / "research" / f"{day}_{run.s['hhmm']}_candidates.json"
    prev = sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "research").glob(f"{day}_*_candidates.json") if p != out)
    claude(run, "scout", "scout", date=day, time=run.s["hhmm"], research=f"research/{day}.json",
           out=str(out.relative_to(ROOT)).replace("\\", "/"), previous=", ".join(prev) or "none")
    data = read_json(out)
    if not data or not data.get("candidates"): raise StepError(f"{out.name} yazılmadı ya da boş")
    run.status(run.s["status"], candidates_file=str(out.relative_to(ROOT)))
    n = len(data["candidates"])
    notify("AI Playbooks", f"{n} yeni aday hazır. Studio'dan birini seç.")
    return f"{n} aday"


def n_choose(run):
    run.node("choose", status="waiting", msg="Soldaki listeden bir haber seç")
    return None  # stays waiting; select() finishes it


# ---------------------------------------------------------------- post nodes

def content_path(run):
    return ROOT / run.s["content"]


def out_dir(run):
    return ROOT / "output" / ("clips" if run.s["kind"] == "clip" else "") / content_path(run).stem


def n_write(run):
    c = run.s["candidate"]
    note = ""
    if run.s.get("note"):
        note = (f"## Revision request from the owner\n{run.s['note']}\n\nThe file {run.s['content']} already exists: "
                "update it according to the request instead of starting over (keep its `voice`).")
    claude(run, "write", "write", date=run.s["day"], candidate=json.dumps(c, indent=1, ensure_ascii=False), note=note,
           content=run.s["content"], result=f"runs/{run.id}/write.json")
    data = read_json(content_path(run))
    if not data: raise StepError(f"{run.s['content']} yazılmadı ya da geçersiz JSON")
    n = len(data.get("slides", []))
    if not 2 <= n <= 10: raise StepError(f"{n} slayt var (2-10 olmalı)")
    if not (ROOT / "themes" / f"{data.get('theme')}.py").exists(): raise StepError(f"tema yok: {data.get('theme')}")
    return f"{data['theme']} · {n} slayt"


def n_cover(run):
    tail = sh(run, "cover", [PY, "cover.py", run.s["content"]])
    t = next((x for x in tail if x.startswith(("photo:", "flux:"))), "tamam")
    return t.replace("photo: File:", "Foto: ").replace("flux:", "Flux sahnesi ·")[:120]


def n_carousel(run):
    sh(run, "carousel", [PY, "carousel.py", run.s["content"]])
    return f"{len(list((ROOT / 'output' / content_path(run).stem).glob('slide_*.png')))} slayt"


def n_reel(run):
    sh(run, "reel", [PY, "reel.py", run.s["content"]])
    return f"{json.loads(content_path(run).read_text(encoding='utf-8')).get('voice', '')} sesi"


def reel_frames(run):
    name = content_path(run).stem; mp4 = ROOT / "output" / name / "reel.mp4"
    qa = run.dir / "qa"; shutil.rmtree(qa, ignore_errors=True); qa.mkdir()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                               capture_output=True, text=True, creationflags=NO_WINDOW).stdout.strip() or 0)
    out = []
    for i in range(8):
        t = dur * (i + 0.6) / 8.3; f = qa / f"frame_{i + 1}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", str(f)],
                       creationflags=NO_WINDOW)
        if f.exists(): out.append(str(f.relative_to(ROOT)).replace("\\", "/"))
    return out


def n_qa(run):
    claude(run, "qa", "qa", content=run.s["content"], name=content_path(run).stem, result=f"runs/{run.id}/qa.json")
    r = read_json(run.dir / "qa.json")
    if r is None: raise StepError("qa.json yazılmadı")
    return "sorun yok" if r.get("ok") else "dikkat: " + "; ".join(r.get("problems", []))[:120]


def n_approve(run):
    qa = read_json(run.dir / "qa.json", {})
    if settings()["approval"] or not qa.get("ok", True):
        run.node("approve", status="waiting", msg="Önizleme hazır: Yayınla / Revize et / Reddet")
        notify("AI Playbooks", f"Onay bekliyor: {(run.s.get('title') or '')[:80]}")
        return None
    return "otomatik (onay kapalı)"


def publish_step(step):
    def f(run):
        tail = sh(run, step, [PY, "publish.py", run.s["content"], "--steps", step])
        st = read_json(out_dir(run) / "publish.json", {}).get(step, {})
        return st.get("link") or (tail[-1] if tail else "tamam")
    return f


def n_log(run):
    publish_step("log")(run)
    rel = run.s["content"]
    record_timings(run, "published")
    for args in (["add", rel, "publish_log.jsonl", "research", "stats"],
                 ["commit", "-q", "-m", f"{'clip' if run.s['kind'] == 'clip' else 'post'}: {content_path(run).stem}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"],
                 ["push", "-q"]):
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           creationflags=NO_WINDOW)
        run.log("log", f"$ git {args[0]}\n{r.stdout}{r.stderr}")
        if r.returncode and not (args[0] == "commit" and "nothing to commit" in r.stdout + r.stderr):
            raise StepError(f"git {args[0]}: {(r.stderr or r.stdout).strip()[:200]}")
    links = {k: v.get("link") for k, v in read_json(out_dir(run) / "publish.json", {}).items()
             if isinstance(v, dict) and v.get("link")}
    notify("AI Playbooks", "Paylaşıldı: " + (links.get("ig_carousel") or links.get("ig_reel") or run.s["content"]))
    return "GitHub'a kaydedildi"


def frames_of(video, dest, n=8):
    dest.mkdir(parents=True, exist_ok=True)
    for f in dest.glob("*.jpg"): f.unlink()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True, creationflags=NO_WINDOW).stdout.strip() or 0)
    out = []
    for i in range(n):
        f = dest / f"frame_{i + 1}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{dur * (i + 0.5) / n:.2f}", "-i", str(video),
                        "-frames:v", "1", "-vf", "scale=720:-2", str(f)], creationflags=NO_WINDOW)
        if f.exists(): out.append(f.relative_to(ROOT).as_posix())
    return out, dur


def n_fetch(run):
    out = out_dir(run); out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("source.*"): f.unlink()
    sh(run, "fetch", [PY, "-m", "yt_dlp", "-q", "--no-playlist", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
                      "--write-info-json", "-o", str(out / "source.%(ext)s"), run.s["url"]])
    info = read_json(out / "source.info.json", {}) or {}
    video = next((f for f in out.glob("source.*") if f.suffix in (".mp4", ".webm", ".mkv", ".mov")), None)
    if not video: raise StepError("video indirilemedi")
    frames, dur = frames_of(video, run.dir / "frames")
    host = urllib.parse.urlparse(run.s["url"]).hostname or ""
    platform = "X" if host.endswith(("x.com", "twitter.com")) else info.get("extractor_key") or host
    run.s["clip"] = {"uploader": info.get("uploader") or "", "uploader_id": info.get("uploader_id") or info.get("channel_id") or "",
                     "description": (info.get("description") or info.get("title") or "")[:1500], "secs": round(dur, 1),
                     "platform": platform, "frames": frames}
    run.save()
    return f"{run.s['clip']['secs']} sn · @{run.s['clip']['uploader_id']}"


def n_hook(run):
    c = run.s["clip"]
    note = f"\n## Revision request from the owner\n{run.s['note']}\n" if run.s.get("note") else ""
    claude(run, "hook", "hook", date=run.s["day"], url=run.s["url"], uploader=c["uploader"], uploader_id=c["uploader_id"],
           platform=c["platform"], description=c["description"].replace("```", "'" * 3), secs=c["secs"],
           frames=", ".join(c["frames"]), note=note, content=run.s["content"])
    data = read_json(content_path(run))
    if not data: raise StepError(f"{run.s['content']} yazılmadı ya da geçersiz JSON")
    if data.get("reject"): raise StepError("Claude bu videoyu uygun bulmadı: " + str(data["reject"])[:200])
    if not data.get("hook") or not data.get("caption"): raise StepError("hook ya da caption eksik")
    run.status(run.s["status"], title=data["hook"])
    return data["hook"][:120]


def n_frame(run):
    sh(run, "frame", [PY, "clip.py", run.s["content"]])
    secs = (read_json(out_dir(run) / "meta.json", {}) or {}).get("secs")
    return f"{secs} sn" if secs else "tamam"


PHASES = {"trigger": "scan", "collect": "scan", "scout": "scan", "choose": "wait", "write": "production", "cover": "production",
          "fetch": "production", "hook": "production", "frame": "production",
          "carousel": "production", "reel": "production", "qa": "production", "approve": "wait", "upload": "publish",
          "ig_carousel": "publish", "ig_reel": "publish", "fb_photos": "publish", "fb_reel": "publish", "yt_short": "publish", "log": "publish"}


def secs_between(a, b):
    if not a: return 0
    return max(0, round(((datetime.fromisoformat(b) if b else now()) - datetime.fromisoformat(a)).total_seconds()))


def timings(run):
    """Per-node time of a post run (+ its scan), earlier attempts included; totals per phase."""
    flows = []
    scan = Run(run.s["scan"]) if run.s.get("scan") and (RUNS / run.s["scan"] / "state.json").exists() else None
    if scan and scan.s: flows.append(scan.s)
    flows.append(run.s)
    rows, first, last = [], None, None
    for s in flows:
        for nid, label, _ in FLOWS[s["kind"]]:
            n = s["nodes"][nid]
            tries = n.get("attempts", []) + ([n] if n.get("started") else [])
            secs = sum(secs_between(t.get("started"), t.get("ended")) for t in tries)
            for t in tries:
                if t.get("started") and (not first or t["started"] < first): first = t["started"]
                end = t.get("ended") or (iso() if t.get("started") else None)
                if end and (not last or end > last): last = end
            rows.append({"node": nid, "label": label, "phase": PHASES[nid], "secs": secs, "attempts": len(tries),
                         "status": n["status"]})
    tot = {ph: sum(r["secs"] for r in rows if r["phase"] == ph) for ph in ("scan", "wait", "production", "publish")}
    return {"run": run.id, "post": pathlib.Path(run.s["content"]).stem, "title": run.s.get("title"),
            "nodes": rows, "phases": tot, "machine": tot["scan"] + tot["production"] + tot["publish"],
            "waiting": tot["wait"], "wall": secs_between(first, last), "start": first, "end": last}


def record_timings(run, outcome):
    (ROOT / "stats").mkdir(exist_ok=True)
    with (ROOT / "stats" / "timings.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"date": iso(), "outcome": outcome, **timings(run)}, ensure_ascii=False) + "\n")


NODES = {"trigger": n_trigger, "collect": n_collect, "scout": n_scout, "choose": n_choose,
         "write": n_write, "cover": n_cover, "carousel": n_carousel, "fetch": n_fetch, "hook": n_hook, "frame": n_frame, "reel": n_reel, "qa": n_qa, "approve": n_approve,
         "upload": publish_step("upload"), "ig_carousel": publish_step("ig_carousel"), "ig_reel": publish_step("ig_reel"),
         "fb_photos": publish_step("fb_photos"), "fb_reel": publish_step("fb_reel"),
         "yt_short": publish_step("yt_short"), "log": n_log}


def execute(run):
    """Run the flow's nodes from the first one that isn't done. Stops at a waiting node or an error."""
    run.status("running"); CANCELED.discard(run.id)
    for nid, label, _ in FLOWS[run.s["kind"]]:
        if run.s["nodes"][nid]["status"] == "done": continue
        run.node(nid, status="running", started=iso(), ended=None, msg="")
        t0 = time.time()
        try:
            msg = NODES[nid](run)
        except Canceled:
            run.node(nid, status="error", ended=iso(), msg="Durduruldu"); run.status("canceled"); return
        except Exception as ex:  # any failure: show it on the node, keep the rest for a retry
            run.log(nid, f"HATA: {type(ex).__name__}: {ex}")
            run.node(nid, status="error", ended=iso(), msg=str(ex)[:300]); run.status("error")
            slog(run.id, nid, "error:", ex)
            notify("AI Playbooks: hata", f"{label}: {str(ex)[:120]}")
            return
        if run.s["nodes"][nid]["status"] == "waiting":
            run.status("waiting"); return
        run.node(nid, status="done", ended=iso(), msg=msg or "", secs=round(time.time() - t0))
    run.status("done")


# ---------------------------------------------------------------- workers + scheduler

def start_scan(trigger_msg):
    with LOCK:
        if any(s["kind"] == "scan" and s["status"] in ("running", "queued") for s in all_runs()):
            return None
        t = now(); rid = f"scan-{t:%Y%m%d-%H%M%S}"
        run = Run.create("scan", rid, day=f"{t:%Y-%m-%d}", hhmm=f"{t:%H%M}", trigger_msg=trigger_msg)
    threading.Thread(target=execute, args=(run,), daemon=True).start()
    slog("scan started:", rid, trigger_msg)
    return rid


def post_worker():
    while True:
        rid = POST_Q.get()
        try: execute(Run(rid))
        except Exception as ex: slog("post worker crash", rid, ex)


def enqueue(run):
    run.status("queued"); POST_Q.put(run.id)


def last_slot(times, t):
    slots = []
    for d in (t.date() - timedelta(days=1), t.date()):
        for hm in times:
            h, m = map(int, hm.split(":"))
            slots.append(datetime(d.year, d.month, d.day, h, m).astimezone())
    past = [s for s in slots if s <= t]
    return max(past) if past else None


def next_slot(times, t):
    slots = []
    for d in (t.date(), t.date() + timedelta(days=1)):
        for hm in times:
            h, m = map(int, hm.split(":"))
            slots.append(datetime(d.year, d.month, d.day, h, m).astimezone())
    return min(s for s in slots if s > t)


METRICS_LOCK = threading.Lock()


def refresh_metrics():
    """metrics.py in a subprocess (keeps the server independent of API hiccups); one at a time."""
    if not METRICS_LOCK.acquire(blocking=False): return False
    def work():
        try:
            r = subprocess.run([PY, "metrics.py"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", creationflags=NO_WINDOW, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            if r.returncode: slog("metrics failed:", (r.stderr or r.stdout)[-300:])
        finally:
            METRICS_LOCK.release()
    threading.Thread(target=work, daemon=True).start()
    return True


def scheduler():
    while True:
        try:
            m = read_json(RUNS / "metrics.json", {}) or {}
            if not m.get("updated") or now() - datetime.fromisoformat(m["updated"]) > timedelta(hours=6): refresh_metrics()
        except Exception as ex:
            slog("metrics schedule error:", ex)
        try:
            s = settings(); t = now(); slot = last_slot(s["scan_times"], t)
            if slot and (not s["last_slot"] or s["last_slot"] < slot.isoformat()):
                late = t - slot > timedelta(minutes=10)
                if start_scan(f"Planlı tarama {slot:%H:%M}" + (" (kaçırılmıştı, telafi)" if late else "")):
                    s["last_slot"] = slot.isoformat(); save_settings(s)
        except Exception as ex:
            slog("scheduler error:", ex)
        time.sleep(30)


def recover():
    """After a restart: runs that were mid-node resume from that node (every step is safe to rerun, publish.py never
    posts twice); queued posts are requeued."""
    for s in all_runs():
        run = Run(s["id"])
        if s["status"] == "running":
            nid = next((n for n, v in s["nodes"].items() if v["status"] == "running"), None)
            if nid: run.reset_from(nid)
            slog("resuming after restart:", run.id, nid)
            if s["kind"] == "scan": threading.Thread(target=execute, args=(run,), daemon=True).start()
            else: enqueue(run)
        elif s["status"] == "queued" and s["kind"] == "post":
            POST_Q.put(s["id"])


# ---------------------------------------------------------------- actions (called from the UI)

def select(scan_id, cand_id):
    scan = Run(scan_id)
    cands = (read_json(ROOT / scan.s["candidates_file"], {}) or {}).get("candidates", [])
    c = next((x for x in cands if x["id"] == cand_id), None)
    if not c: raise ValueError("aday bulunamadı")
    t = now(); day = f"{t:%Y-%m-%d}"
    slug = re.sub(r"[^a-z0-9-]+", "-", c["id"].lower()).strip("-")[:50] or "post"
    content = f"content/{day}_{slug}.json"; k = 2
    while (ROOT / content).exists(): content = f"content/{day}_{slug}-{k}.json"; k += 1
    run = Run.create("post", f"post-{t:%Y%m%d-%H%M%S}-{slug}"[:80], day=day, candidate=c, content=content,
                     scan=scan_id, title=c.get("title"))
    chosen = scan.s.get("chosen", []) + [{"id": cand_id, "run": run.id}]
    scan.status(scan.s["status"] if scan.s["status"] != "waiting" else "done", chosen=chosen)
    scan.node("choose", status="done", msg=f"Seçildi: {c.get('title', '')[:60]}", ended=iso())
    enqueue(run)
    return run.id


def start_clip(url, note=""):
    url = url.strip()
    if not re.match(r"https?://\S+$", url): raise ValueError("geçerli bir video bağlantısı değil")
    log = ROOT / "publish_log.jsonl"
    done = {str(json.loads(l).get("source_url") or "").split("?")[0] for l in log.read_text(encoding="utf-8").splitlines()
            if l.strip()} if log.exists() else set()
    if url.split("?")[0] in done: raise ValueError("bu video zaten paylaşıldı")
    t = now(); day = f"{t:%Y-%m-%d}"
    m = re.search(r"/status/(\d+)", url)
    slug = (m.group(1)[-8:] if m else re.sub(r"[^a-z0-9]+", "-", url.lower().split("//")[-1])[-30:].strip("-")) or "clip"
    content = f"content/clips/{day}_clip-{slug}.json"; k = 2
    while (ROOT / content).exists(): content = f"content/clips/{day}_clip-{slug}-{k}.json"; k += 1
    (ROOT / "content" / "clips").mkdir(parents=True, exist_ok=True)
    run = Run.create("clip", f"clip-{t:%Y%m%d-%H%M%S}-{slug}"[:80], day=day, url=url, content=content,
                     title=url, candidate={"title": url}, **({"note": note.strip()} if note.strip() else {}))
    enqueue(run)
    return run.id


def approve(rid):
    run = Run(rid)
    if run.s["nodes"]["approve"]["status"] != "waiting": raise ValueError("bu gönderi onay beklemiyor")
    run.node("approve", status="done", ended=iso(), msg=f"Onaylandı {now():%H:%M}")
    enqueue(run)


def revise(rid, note):
    run = Run(rid)
    if not note.strip(): raise ValueError("revizyon notu boş")
    run.s["note"] = note.strip(); run.s.setdefault("revisions", []).append({"at": iso(), "note": note.strip()})
    run.save(); run.reset_from("hook" if run.s["kind"] == "clip" else "write"); enqueue(run)


def reject(rid):
    run = Run(rid); c = content_path(run)
    if c.exists(): shutil.move(str(c), str(run.dir / c.name))  # keep it out of content/ (dedupe, voice rotation)
    run.node("approve", status="error", ended=iso(), msg="Reddedildi")
    run.status("rejected")
    record_timings(run, "rejected")


def retry(rid, nid):
    run = Run(rid)
    if run.s["status"] in ("running", "queued"): raise ValueError("zaten çalışıyor")
    run.reset_from(nid)
    if run.s["kind"] == "scan": threading.Thread(target=execute, args=(run,), daemon=True).start()
    else: enqueue(run)


def cancel(rid):
    run = Run(rid); CANCELED.add(rid)
    p = PROCS.get(rid)
    if p:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, creationflags=NO_WINDOW)
    elif run.s["status"] == "queued":
        run.status("canceled")


def state():
    s = settings(); runs = all_runs()
    for r in runs:
        if r["kind"] == "scan" and r.get("candidates_file"):
            r["candidates"] = (read_json(ROOT / r["candidates_file"], {}) or {})
    return {"settings": {k: s[k] for k in ("scan_times", "approval")},
            "next_scan": iso(next_slot(s["scan_times"], now())), "now": iso(),
            "flows": {k: [{"id": n, "label": l, "kind": t} for n, l, t in v] for k, v in FLOWS.items()},
            "runs": runs[:40]}


def run_detail(rid):
    run = Run(rid); s = dict(run.s)
    if s["kind"] == "clip":
        out = out_dir(run); rel = out.relative_to(ROOT).as_posix()
        s["content_data"] = read_json(content_path(run)) or read_json(run.dir / content_path(run).name)
        s["slides"] = []
        s["reel"] = f"{rel}/reel.mp4" if (out / "reel.mp4").exists() else None
        s["publish"] = read_json(out / "publish.json", {})
    if s["kind"] == "post":
        name = content_path(run).stem; out = ROOT / "output" / name
        s["content_data"] = read_json(content_path(run)) or read_json(run.dir / content_path(run).name)
        s["slides"] = [f"output/{name}/{p.name}" for p in sorted(out.glob("slide_*.png"))]
        s["reel"] = f"output/{name}/reel.mp4" if (out / "reel.mp4").exists() else None
        s["write_result"] = read_json(run.dir / "write.json"); s["qa_result"] = read_json(run.dir / "qa.json")
        s["qa_frames"] = [f"runs/{rid}/qa/{p.name}" for p in sorted((run.dir / "qa").glob("*.jpg"))]
        s["publish"] = read_json(out / "publish.json", {})
    return s


def history():
    f = ROOT / "publish_log.jsonl"
    if not f.exists(): return []
    return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()][::-1]


# ---------------------------------------------------------------- http

ALLOWED = ("output/", "runs/", "content/", "fonts/", "research/")
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".png": "image/png",
         ".jpg": "image/jpeg", ".mp4": "video/mp4", ".json": "application/json; charset=utf-8", ".ttf": "font/ttf",
         ".woff2": "font/woff2", ".log": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8"}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        if not isinstance(body, bytes): body = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query))
        try:
            if u.path == "/": return self.send(200, (ROOT / "studio" / "index.html").read_bytes(), TYPES[".html"])
            if u.path == "/api/state": return self.send(200, state())
            if u.path == "/api/run": return self.send(200, run_detail(q["id"]))
            if u.path == "/api/history": return self.send(200, history())
            if u.path == "/api/metrics":
                return self.send(200, {**(read_json(RUNS / "metrics.json", {}) or {}), "refreshing": METRICS_LOCK.locked()})
            if u.path == "/api/viral":
                return self.send(200, read_json(ROOT / "research" / f"{q.get('day') or f'{now():%Y-%m-%d}'}_viral.json", {}))
            if u.path == "/api/research":
                return self.send(200, read_json(ROOT / "research" / f"{q.get('day') or f'{now():%Y-%m-%d}'}.json", {}))
            if u.path == "/api/log":
                f = RUNS / q["run"] / f"{q['node']}.log"
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()[-400:] if f.exists() else []
                return self.send(200, "\n".join(lines).encode(), TYPES[".log"])
            if u.path.startswith("/file/"):
                rel = urllib.parse.unquote(u.path[6:])
                f = (ROOT / rel).resolve()
                if not rel.startswith(ALLOWED) or ROOT not in f.parents or not f.is_file(): return self.send(404, {"error": "yok"})
                return self.send_file(f)
            self.send(404, {"error": "yok"})
        except (KeyError, OSError, ValueError) as ex:
            self.send(400, {"error": str(ex)})

    def send_file(self, f):
        size = f.stat().st_size; ctype = TYPES.get(f.suffix.lower(), "application/octet-stream")
        rng = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        start, end = 0, size - 1
        if rng and (rng.group(1) or rng.group(2)):
            if rng.group(1): start = int(rng.group(1)); end = int(rng.group(2) or end)
            else: start = size - int(rng.group(2))
            end = min(end, size - 1)
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type", ctype); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1)); self.send_header("Cache-Control", "no-store")
        if rng: self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with f.open("rb") as fh:
            fh.seek(start); left = end - start + 1
            while left > 0:
                chunk = fh.read(min(1 << 20, left))
                if not chunk: break
                try: self.wfile.write(chunk)
                except (ConnectionError, OSError): return
                left -= len(chunk)

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try:
            b = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if u.path == "/api/scan":
                rid = start_scan("Elle başlatıldı (Şimdi tara)")
                return self.send(200 if rid else 409, {"run": rid} if rid else {"error": "zaten bir tarama çalışıyor"})
            if u.path == "/api/select": return self.send(200, {"run": select(b["scan"], b["candidate"])})
            if u.path == "/api/clip": return self.send(200, {"run": start_clip(b.get("url", ""), b.get("note", ""))})
            if u.path == "/api/approve": approve(b["run"]); return self.send(200, {"ok": True})
            if u.path == "/api/revise": revise(b["run"], b.get("note", "")); return self.send(200, {"ok": True})
            if u.path == "/api/reject": reject(b["run"]); return self.send(200, {"ok": True})
            if u.path == "/api/retry": retry(b["run"], b["node"]); return self.send(200, {"ok": True})
            if u.path == "/api/cancel": cancel(b["run"]); return self.send(200, {"ok": True})
            if u.path == "/api/metrics/refresh": return self.send(200, {"started": refresh_metrics()})
            if u.path == "/api/settings":
                s = settings()
                if "approval" in b: s["approval"] = bool(b["approval"])
                if "scan_times" in b:
                    times = sorted({t for t in b["scan_times"] if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t)})
                    if not times: raise ValueError("geçerli saat yok (SS:DD)")
                    s["scan_times"] = times
                    s["last_slot"] = (last_slot(times, now()) or now()).isoformat()  # new times start from now on
                save_settings(s); return self.send(200, {"ok": True})
            self.send(404, {"error": "yok"})
        except (KeyError, ValueError, TypeError) as ex:
            self.send(400, {"error": str(ex)})


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    RUNS.mkdir(exist_ok=True)
    if sys.stdout: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", a.port), H)
    except OSError:
        slog(f"port {a.port} in use: Studio is probably already running")
        if not a.no_browser: webbrowser.open(f"http://localhost:{a.port}")
        return
    if not SETTINGS.exists():  # first start: begin with the next slot instead of scanning right away
        s = settings(); s["last_slot"] = (last_slot(s["scan_times"], now()) or now()).isoformat(); save_settings(s)
    recover()
    threading.Thread(target=post_worker, daemon=True).start()
    threading.Thread(target=scheduler, daemon=True).start()
    slog(f"Studio running at http://localhost:{a.port}")
    if not a.no_browser: webbrowser.open(f"http://localhost:{a.port}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
