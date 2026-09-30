"""AI Playbooks Studio: local workflow engine + web UI (n8n-style canvas) for the daily pipeline.

Usage:
    python studio.py [--port 8787] [--no-browser]
    then open http://localhost:8787

Three workflows:
    scan  (scheduled, default 08:00 + 18:00; missed slots run at startup)
          trigger -> collect (news.py) -> scout (Claude: web search, verify, rank) -> choose (owner picks in the UI)
    post  (one per picked candidate, one at a time)
          write (Claude: verify + content JSON) -> cover (Commons photo of the person, else a licensed topic photo) -> carousel -> reel (the
          carousel as a voiced video, only for YouTube) -> qa (Claude looks at the output, fixes) -> approve (owner:
          publish / revise / reject; can be switched off) -> upload -> ig_carousel -> fb_photos -> yt_short
          -> log (publish_log.jsonl + git commit/push)
    repo  (GitHub repo post, owner 2026-09-28: one photo of the repo page + captions + the link in the FB first comment /
          by Instagram DM; candidates come from the daily `repos` job: repos.py -> Claude picks, GitHub tab)
          write (Claude verifies the README, writes hook/captions draft/fb_comment) -> caption -> card (repocard.py)
          -> approve -> upload -> ig_photo -> fb_photos -> comments (FB first comment) -> dm (direct link) -> log
    clip  (viral Reel: the owner pastes an X/post link)
          fetch (yt-dlp) -> hook (Claude watches frames, writes hook + caption) -> frame (clip.py) -> qa (Claude
          compares the framed Reel with the source: crop, fit, hook; fixes + re-frames) -> approve
          -> upload -> ig_reel -> fb_reel -> yt_short -> comments -> log
State lives in runs/<run-id>/state.json, logs in runs/<run-id>/<node>.log; a failed node can be retried from the UI.
Claude steps run `claude -p` (Claude Code headless) with the prompts in prompts/.
"""
import sys, os, re, json, time, queue, shutil, pathlib, argparse, threading, subprocess, webbrowser, urllib.parse
from datetime import datetime, timedelta
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import telegram_bot as TG
import remote
import strategy as STRAT
import starseed_studio as SS

ROOT = pathlib.Path(__file__).parent.resolve()
RUNS = ROOT / "runs"
SETTINGS = RUNS / "settings.json"
PY = str(pathlib.Path(sys.executable).with_name("python.exe")) if sys.executable.lower().endswith("pythonw.exe") else sys.executable
CLAUDE = shutil.which("claude") or "claude"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
CLAUDE_TOOLS = ["WebSearch", "WebFetch", "Read", "Write", "Edit", "Glob", "Grep",
                "Bash(python carousel.py:*)", "Bash(python reel.py:*)", "Bash(python news.py:*)",
                "Bash(python cover.py:*)", "Bash(python clip.py:*)",
                "Bash(python tags.py:*)", "Bash(python captions.py:*)", "Bash(python hooks.py:*)",
                "Bash(python repos.py:*)", "Bash(python repocard.py:*)", "Bash(python strategy.py:*)", "Bash(python xscout.py:*)"]

SCAN = [("trigger", "Zamanlayıcı", "trigger"), ("collect", "Haber topla", "code"),
        ("scout", "Ara, doğrula, havuza ekle", "ai"), ("pool", "Havuzdan listele", "code"), ("choose", "Senin seçimin", "human")]
# background jobs (no canvas, no Telegram): gathers fill the candidate pool 5x a day, learn keeps the hook playbook fresh
GATHER = [("collect", "Haber topla", "code"), ("scout", "Ara, doğrula, havuza ekle", "ai")]
LEARN = [("hooks", "Hook trendlerini öğren", "ai")]
REPOS = [("rcollect", "Repoları topla", "code"), ("rscout", "Repo seç & doğrula", "ai")]
STRATEGY = [("review", "Strateji & trend analizi", "ai")]
BACKGROUND = ("gather", "learn", "repos", "strategy")
POST = [("write", "Doğrula & yaz", "ai"), ("caption", "Caption & tag", "ai"), ("cover", "Kapak görseli", "code"), ("carousel", "Carousel", "code"),
        ("reel", "Video · ses + müzik (YouTube)", "code"), ("qa", "Kalite kontrol", "ai"),
        ("approve", "Yayından önce onay", "human"), ("upload", "Medya yükle", "code"),
        ("ig_carousel", "Instagram carousel", "publish"), ("fb_photos", "Facebook gönderi", "publish"),
        ("ig_reel", "Instagram Reel (video)", "publish"), ("fb_reel", "Facebook Reel (video)", "publish"),
        ("yt_short", "YouTube Short", "publish"), ("comments", "Yorumlar", "publish"), ("dm", "DM botu kaydı", "publish"), ("tiktok", "TikTok", "publish"), ("x_post", "X gönderi", "publish"), ("log", "Kayıt & GitHub", "code")]
CLIP = [("fetch", "Videoyu indir", "code"), ("hook", "Hook", "ai"), ("caption", "Caption & tag", "ai"), ("frame", "Reel çerçevesi", "code"),
        ("qa", "Kalite kontrol", "ai"), ("approve", "Yayından önce onay", "human"), ("upload", "Medya yükle", "code"), ("ig_reel", "Instagram Reel", "publish"),
        ("fb_reel", "Facebook Reel", "publish"), ("yt_short", "YouTube Short", "publish"), ("comments", "Yorumlar", "publish"),
        ("dm", "DM botu kaydı", "publish"), ("tiktok", "TikTok", "publish"), ("x_post", "X gönderi", "publish"), ("log", "Kayıt & GitHub", "code")]
REPO = [("write", "Repo'yu doğrula & yaz", "ai"), ("caption", "Caption & tag", "ai"), ("card", "Repo görseli", "code"),
        ("rreel", "Repo Reel (kayan sayfa)", "code"),
        ("approve", "Yayından önce onay", "human"), ("upload", "Medya yükle", "code"), ("ig_photo", "Instagram gönderi", "publish"),
        ("fb_photos", "Facebook gönderi", "publish"), ("ig_reel", "Instagram Reel", "publish"), ("fb_reel", "Facebook Reel", "publish"),
        ("comments", "FB ilk yorum (link)", "publish"),
        ("dm", "DM botu kaydı", "publish"), ("tiktok", "TikTok", "publish"), ("x_post", "X gönderi", "publish"), ("log", "Kayıt & GitHub", "code")]
FLOWS = {"scan": SCAN, "post": POST, "clip": CLIP, "repo": REPO, "gather": GATHER, "learn": LEARN, "repos": REPOS, "strategy": STRATEGY}

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
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    for i in range(20):  # Windows: the target can be open for a moment (UI read, antivirus) -> PermissionError
        try: os.replace(tmp, p); return
        except PermissionError:
            if i == 19: raise
            time.sleep(0.1)


# the learning job (hooks + captions, used by every flow) runs 10x a day (owner, 2026-09-28), each run on one focus
LEARN_TIMES = ["07:00", "08:30", "10:00", "11:30", "13:00", "14:30", "16:00", "17:30", "19:00", "21:00"]
LEARN_FOCUS = [
    "news carousels: cover headlines + caption hooks for AI news",
    "prompt packs: money / daily-life pack headlines and caption openers",
    "viral clip Reels: hook lines over AI videos",
    "GitHub repo posts: caption openers (the 'GitHub repo hooks' section)",
    "captions: first lines, comment CTAs and follow lines that drive comments/saves (caption_playbook.md Lessons)",
]


def settings():
    s = {"scan_times": ["08:00", "18:00"], "approval": True, "last_slot": None, "dm_bot": False,
         "gather_times": ["06:30", "10:30", "13:30", "16:30", "21:30"], "last_gather_slot": None,
         "learn_times": LEARN_TIMES, "last_learn_slot": None, "repo_time": "07:15", "last_repo_slot": None,
         "autopilot": True, "post_slots": ["14:00", "17:00", "20:00", "23:00"], "strategy_time": "09:30", "last_strategy_slot": None}
    s.update(read_json(SETTINGS, {}) or {})
    s.pop("learn_time", None)  # before 2026-09-28: one learning run a day
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
        if s and "created" in s and "kind" in s: out.append(s)  # runs/agent_studio etc. are not runs
    return sorted(out, key=lambda s: s["created"], reverse=True)


# ---------------------------------------------------------------- already posted (never offered again)

GENERIC_URL = re.compile(r"(?i)changelog|release-?notes|/releases/?$|/updates/?$|/news/?$|/blog/?$|/\d{4}/?$")


def _url(u):
    return re.sub(r"^https?://(www\.)?|[?#].*$|/+$", "", str(u).strip().lower())


def posted():
    """Every post made so far (content/*.json; rejected ones are moved out of content/)."""
    runs = {pathlib.Path(r["content"]).stem: r for r in all_runs() if r["kind"] == "post" and r.get("content")}
    out = []
    for p in sorted((ROOT / "content").glob("*.json")):
        d = read_json(p, {}) or {}; r = runs.get(p.stem, {}); s0 = (d.get("slides") or [{}])[0]
        out.append({"name": p.stem, "slug": re.sub(r"-\d+$", "", p.stem[11:]), "topic": d.get("topic"),
                    "title": (d.get("cover") or {}).get("title") or s0.get("title"), "sources": d.get("sources", []),
                    "candidate": (r.get("candidate") or {}).get("id"), "scan": r.get("scan")})
    return out


def posted_text():
    """Posted list for the scout prompt."""
    return "\n".join(f"- {p['name'][:10]} · {p['topic']} · \"{p['title']}\" · id {p['candidate'] or p['slug']} · "
                     + " ".join(p["sources"][:3]) for p in posted()) or "- (nothing yet)"


def load_candidates(path, scan_id=None):
    """A scan's candidate list without anything that was already posted (same candidate id, same slug, or a news
    item sharing a specific source URL with a post). Posts picked from this same scan stay (shown as chosen)."""
    data = read_json(ROOT / path, {}) or {}
    done = [p for p in posted() if not scan_id or p["scan"] != scan_id]
    urls = {_url(u): p["name"] for p in done for u in p["sources"] if not GENERIC_URL.search(u)}
    keep, hidden = [], []
    for c in data.get("candidates", []):
        hit = next((p["name"] for p in done if c.get("id") in (p["candidate"], p["slug"])), None)
        if not hit and c.get("kind") == "news":
            hit = next((urls[_url(u)] for u in c.get("sources", []) if _url(u) in urls), None)
        (hidden if hit else keep).append({**c, "posted": hit} if hit else c)
    data["candidates"] = keep
    if hidden: data["hidden"] = hidden
    return data


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


def claude(run, nid, template, prompt_name=None, **fields):
    """Run Claude Code headless with a prompt from prompts/, stream a readable log."""
    prompt = (ROOT / "prompts" / f"{template}.md").read_text(encoding="utf-8").format(**fields)
    (run.dir / f"{prompt_name or nid}.prompt.md").write_text(prompt, encoding="utf-8")
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


POOL_DAYS = 7          # a candidate stays in the pool this long after it was first found (unless posted)
FRESH_HOURS = 3        # a scan uses the pool as is when the last gather is younger than this


def last_gather():
    return next((r for r in all_runs() if r["kind"] in ("gather", "scan") and r["nodes"].get("scout", {}).get("status") == "done"), None)


def n_collect(run):
    if run.s["kind"] == "scan":
        busy = next((r for r in all_runs() if r["kind"] == "gather" and r["status"] in ("running", "queued")), None)
        if busy:  # a background gather is running: wait for it instead of doing the same work twice
            run.log("collect", f"arka plan toplaması sürüyor ({busy['id']}), bekleniyor")
            for _ in range(160):
                if Run(busy["id"]).s["status"] not in ("running", "queued"): break
                if run.id in CANCELED: raise Canceled()
                time.sleep(15)
        g = last_gather()
        if g and now() - datetime.fromisoformat(g["nodes"]["scout"]["ended"]) < timedelta(hours=FRESH_HOURS):
            run.s["skip_scout"] = True; run.save()
            return f"Atlandı: havuz güncel (son toplama {datetime.fromisoformat(g['nodes']['scout']['ended']):%H:%M})"
        run.s["skip_scout"] = False; run.save()
    tail = sh(run, "collect", [PY, "news.py", "--hours", "36"])
    msg = next((t for t in reversed(tail) if "items" in t), "tamam").split("->")[0].strip()
    try: sh(run, "collect", [PY, "viral.py"])  # trending AI videos for the Viral tab; never fails the scan
    except StepError as ex: run.log("collect", f"viral.py: {ex}")
    return msg


def pool_items(exclude=None):
    """Every candidate gathered in the last POOL_DAYS days, newest version per id, with first_seen / times_seen."""
    items = {}
    cut = f"{now() - timedelta(days=POOL_DAYS):%Y-%m-%d}"
    files = sorted((ROOT / "research").glob("*_gather.json"))
    files += sorted(f for f in (ROOT / "research").glob("*_candidates.json") if not (read_json(f, {}) or {}).get("pool"))  # pre-pool scans
    for f in sorted(files, key=lambda f: f.name):
        if f.name[:10] < cut or f == exclude: continue
        d = read_json(f, {}) or {}
        hm = f.name[11:15]; when = f"{f.name[:10]}T{hm[:2]}:{hm[2:]}" if hm.isdigit() else f.name[:10]  # local time, from the name
        for c in d.get("candidates", []):
            old = items.get(c["id"])
            items[c["id"]] = {**c, "first_seen": (old or {}).get("first_seen") or when, "times_seen": (old or {}).get("times_seen", 0) + 1,
                              "gather_file": f.name}
    return items


def pool_text():
    rows = sorted(pool_items().values(), key=lambda c: c["first_seen"], reverse=True)
    return "\n".join(f"- {c['id']} · {c.get('tool')} · {c.get('title')}" for c in rows[:120]) or "- (empty)"


def source_task(run):
    """The day's first gather also looks after the sources (health, new sources)."""
    day = run.s["day"]
    done_today = any(r["kind"] in ("gather", "scan") and r.get("day") == day and r.get("source_task") and r["id"] != run.id
                     and r["nodes"].get("scout", {}).get("status") == "done" for r in all_runs())
    if done_today: return ""
    run.s["source_task"] = True; run.save()
    return (ROOT / "prompts" / "scout_sources.md").read_text(encoding="utf-8").format(date=day)


def n_scout(run):
    if run.s.get("skip_scout"): return "Atlandı: havuz güncel"
    day = run.s["day"]
    out = ROOT / "research" / f"{day}_{run.s['hhmm']}_gather.json"
    rel = str(out.relative_to(ROOT)).replace("\\", "/")
    claude(run, "scout", "scout", date=day, time=run.s["hhmm"], research=f"research/{day}.json", out=rel,
           pool=pool_text(), posted=posted_text(), source_task=source_task(run))
    data = read_json(out)
    if data is None: raise StepError(f"{out.name} yazılmadı ya da geçersiz JSON")
    run.status(run.s["status"], gather_file=rel)
    n = len(data.get("candidates", [])); ch = data.get("sources_changed") or []
    return f"{n} yeni aday" + (f" · kaynak: {len(ch)} değişiklik" if ch else "")


def n_pool(run):
    """The owner's list = the whole pool (not posted, not older than POOL_DAYS); new since the last delivery marked."""
    t = now(); out = ROOT / "research" / f"{run.s['day']}_{t:%H%M}_candidates.json"
    prev = next((r for r in all_runs() if r["kind"] == "scan" and r["id"] != run.id and r["nodes"].get("pool", {}).get("status") == "done"), None)
    since = prev["nodes"]["pool"]["ended"] if prev else ""
    items = list(pool_items().values())
    for c in items: c["new"] = bool(since) and c["first_seen"] > since[:16]
    items.sort(key=lambda c: (-(c.get("score") or 0), c["first_seen"]), reverse=False)
    items.sort(key=lambda c: not c["new"])  # new ones first, each group by score
    news = [c for c in items if c.get("kind") == "news"]
    cov = {}
    for c in news: cov[c.get("tool") or "Other"] = cov.get(c.get("tool") or "Other", 0) + 1
    gathers = [r for r in all_runs() if r["kind"] in ("gather", "scan") and r["nodes"].get("scout", {}).get("status") == "done"]
    last = gathers[0] if gathers else None
    notes = [f"Havuz: son {POOL_DAYS} günün adayları, {sum(c['new'] for c in items)} tanesi son teslimden beri yeni."]
    if last: notes.append(f"Son toplama {datetime.fromisoformat(last['nodes']['scout']['ended']):%d.%m %H:%M}.")
    lg = read_json(ROOT / (last.get("gather_file") or ""), {}) if last and last.get("gather_file") else {}
    if lg and lg.get("notes_tr"): notes.append(lg["notes_tr"])
    ch = [x for g in gathers[:6] if g.get("gather_file") for x in ((read_json(ROOT / g["gather_file"], {}) or {}).get("sources_changed") or [])]
    if ch: notes.append("Kaynaklar: " + " · ".join(ch[:4]))
    failed = [r for r in all_runs()[:30] if r["kind"] == "gather" and r["status"] == "error"]
    if failed: notes.append(f"⚠ {len(failed)} arka plan toplaması hata verdi (son: {failed[0]['created'][11:16]}).")
    write_json(out, {"generated": iso(t), "pool": True, "candidates": items, "coverage": cov, "notes_tr": " ".join(notes)})
    rel = str(out.relative_to(ROOT)).replace("\\", "/")
    data = load_candidates(rel)
    run.status(run.s["status"], candidates_file=rel)
    n = len(data.get("candidates", [])); new = sum(1 for c in data.get("candidates", []) if c.get("new"))
    if not n: raise StepError("havuz boş: arka plan toplaması henüz aday bulmadı")
    if not settings().get("autopilot"):  # autopilot: the list only feeds the planner, nobody is asked to pick
        notify("AI Playbooks", f"{n} aday hazır ({new} yeni). Studio'dan birini seç.")
        TG.event("candidates", run)
    return f"{n} aday · {new} yeni" + (f" ({len(data['hidden'])} paylaşılmış gizlendi)" if data.get("hidden") else "")


def n_review(run):
    """Daily strategy director (prompts/strategy.md): numbers + trends -> strategy.json, strategy_playbook.md,
    research/clips/, strategy/backlog.md."""
    claude(run, "review", "strategy", date=run.s["day"], run_id=run.id)
    r = read_json(run.dir / "strategy_result.json", {}) or {}
    AUTO["checked"] = 0.0  # re-plan with the new mix / slots
    if r.get("summary_tr"): TG.event("strategy", run, summary=r["summary_tr"])
    return (r.get("summary_tr") or "tamam").split("\n")[0][:160]


def n_hooks(run):
    today = sum(1 for r in all_runs() if r["kind"] == "learn" and r.get("day") == run.s["day"] and r["created"] < run.s["created"])
    focus = LEARN_FOCUS[today % len(LEARN_FOCUS)]
    run.s["focus"] = focus; run.save()
    claude(run, "hooks", "hook_learn", date=run.s["day"], run_id=run.id, focus=focus, round=today + 1)
    r = read_json(run.dir / "learn.json", {}) or {}
    return (r.get("summary_tr") or "tamam")[:160]


def n_choose(run):
    if settings().get("autopilot"):
        return "Otopilot seçip planlıyor (istersen yine elle seçebilirsin)"
    run.node("choose", status="waiting", msg="Soldaki listeden bir haber seç")
    return None  # stays waiting; select() finishes it


# ---------------------------------------------------------------- post nodes

def content_path(run):
    return ROOT / run.s["content"]


def out_dir(run):
    return ROOT / "output" / {"clip": "clips", "repo": "repos"}.get(run.s["kind"], "") / content_path(run).stem


DM_ON = """## Instagram DM bot (ON)
Our comment-to-DM bot is live on Instagram. When the post gives people something to take away (prompts, a setup, a
guide, the prompt behind a clip), add `"dm": {"keyword": "WORD"}`: one short, easy-to-type English word in capitals
tied to the topic (AGENT, BUDGET, PROMPTS, GUIDE, SETUP, SKETCH ...), not the keyword of our last 5 posts. Whoever
comments it gets a DM (follow gate) with the post's page, which lists everything copy-ready. The caption agent writes
the "Comment WORD" call to action; you only choose the word. Clips: with a `dm` keyword the prompts stay OFF the public
comments (they are the reward): still put them in `comments`, the page and YouTube use them."""
DM_OFF = "## Instagram DM bot (OFF)\nThe comment-to-DM bot is off: no `dm` block, no \"Comment WORD\" promises."


def dm_rule():
    return DM_ON if settings().get("dm_bot") else DM_OFF


def n_write(run):
    if run.s["kind"] == "repo": return n_repo_write(run)
    c = run.s["candidate"]
    note = ""
    if run.s.get("note"):
        note = (f"## Revision request from the owner\n{run.s['note']}\n\nThe file {run.s['content']} already exists: "
                "update it according to the request instead of starting over (keep its `voice`).")
    claude(run, "write", "write", date=run.s["day"], candidate=json.dumps(c, indent=1, ensure_ascii=False), note=note,
           content=run.s["content"], result=f"runs/{run.id}/write.json", dm_rule=dm_rule())
    data = read_json(content_path(run))
    if not data: raise StepError(f"{run.s['content']} yazılmadı ya da geçersiz JSON")
    n = len(data.get("slides", []))
    if not 2 <= n <= 10: raise StepError(f"{n} slayt var (2-10 olmalı)")
    if not (ROOT / "themes" / f"{data.get('theme')}.py").exists(): raise StepError(f"tema yok: {data.get('theme')}")
    return f"{data['theme']} · {n} slayt"


# ---------------------------------------------------------------- GitHub repo pillar (owner, 2026-09-28)

REPO_DIR = ROOT / "research" / "repos"
REPO_POOL_DAYS = 14


def posted_repos():
    """Repos already posted or in production (content/repos/*.json)."""
    out = {}
    for f in (ROOT / "content" / "repos").glob("*.json"):
        d = read_json(f, {}) or {}
        if (d.get("repo") or {}).get("full_name"): out[d["repo"]["full_name"].lower()] = f.stem
    return out


def repo_pool():
    """Every picked repo of the last REPO_POOL_DAYS days (newest version per id), not posted yet."""
    items = {}; cut = f"{now() - timedelta(days=REPO_POOL_DAYS):%Y-%m-%d}"
    for f in sorted(REPO_DIR.glob("*_picks.json")):
        if f.name[:10] < cut: continue
        hm = f.name[11:15]
        for c in (read_json(f, {}) or {}).get("candidates", []):
            old = items.get(c["id"])
            items[c["id"]] = {**c, "first_seen": (old or {}).get("first_seen") or f"{f.name[:10]}T{hm[:2]}:{hm[2:]}"}
    done = posted_repos()
    busy = {r["candidate"].get("id"): r["id"] for r in all_runs()
            if r["kind"] == "repo" and r["status"] not in ("rejected", "canceled") and r.get("candidate")}
    out = []
    for c in items.values():
        if (c.get("full_name") or "").lower() in done and c["id"] not in busy: continue
        out.append({**c, "run": busy.get(c["id"])})
    out.sort(key=lambda c: (c.get("run") is not None, -(c.get("score") or 0), c["first_seen"]))
    return out


def n_rcollect(run):
    tail = sh(run, "rcollect", [PY, "repos.py"])
    return next((t for t in reversed(tail) if "repos seen" in t), "tamam").split("->")[0].strip()


def n_rscout(run):
    day = run.s["day"]; out = REPO_DIR / f"{day}_{run.s['hhmm']}_picks.json"
    rel = out.relative_to(ROOT).as_posix()
    pool = "\n".join(f"- {c['id']} · {c.get('full_name')} · {c.get('stars')} stars" for c in repo_pool()[:80]) or "- (empty)"
    posted = "\n".join(f"- {k} ({v})" for k, v in posted_repos().items()) or "- (nothing yet)"
    claude(run, "rscout", "repo_scout", date=day, time=run.s["hhmm"], research=f"research/repos/{day}.json", pool=pool,
           posted=posted, out=rel)
    data = read_json(out)
    if data is None: raise StepError(f"{out.name} yazılmadı ya da geçersiz JSON")
    return f"{len(data.get('candidates', []))} repo adayı"


def n_repo_write(run):
    c = run.s["candidate"]
    note = ""
    if run.s.get("note"):
        note = (f"## Revision request from the owner\n{run.s['note']}\n\nThe file {run.s['content']} already exists: "
                "update it according to the request instead of starting over.")
    claude(run, "write", "repo_write", date=run.s["day"], candidate=json.dumps(c, indent=1, ensure_ascii=False), note=note,
           content=run.s["content"], run_id=run.id, full_name=c["full_name"], out=out_dir(run).relative_to(ROOT).as_posix())
    data = read_json(content_path(run))
    if not data: raise StepError(f"{run.s['content']} yazılmadı ya da geçersiz JSON")
    if data.get("reject"): raise StepError("Claude bu repoyu uygun bulmadı: " + str(data["reject"])[:200])
    miss = [k for k in ("repo", "hook", "fb_comment", "dm") if not data.get(k)]
    if miss: raise StepError("eksik alan: " + ", ".join(miss))
    return (data["hook"][0] if isinstance(data["hook"], list) else str(data["hook"]))[:120]


def n_card(run):
    tail = sh(run, "card", [PY, "repocard.py", run.s["content"]])
    return next((t for t in reversed(tail) if t.startswith("card:")), "tamam")[5:].split("->")[0].strip()


def n_rreel(run):
    tail = sh(run, "rreel", [PY, "repocard.py", run.s["content"], "--reel"])
    return next((t for t in reversed(tail) if t.startswith("reel:")), "tamam")[5:].split("->")[0].strip()


def start_repo(c, **extra):
    t = now(); day = f"{t:%Y-%m-%d}"
    slug = re.sub(r"[^a-z0-9-]+", "-", c["id"].lower()).strip("-")[:50] or "repo"
    (ROOT / "content" / "repos").mkdir(parents=True, exist_ok=True)
    content = f"content/repos/{day}_repo-{slug}.json"; k = 2
    while (ROOT / content).exists(): content = f"content/repos/{day}_repo-{slug}-{k}.json"; k += 1
    run = Run.create("repo", f"repo-{t:%Y%m%d-%H%M%S}-{slug}"[:80], day=day, candidate=c, content=content,
                     title=c.get("title") or c.get("full_name"), **extra)
    enqueue(run)
    return run


def repo_candidate(rid):
    c = next((x for x in repo_pool() if x["id"] == rid), None)
    if not c: raise ValueError("repo adayı bulunamadı (ya da paylaşıldı)")
    if c.get("run"): raise ValueError("bu repo zaten üretimde")
    return {k: v for k, v in c.items() if k != "run"}


def repos_state():
    s = settings(); last = next((r for r in all_runs() if r["kind"] == "repos"), None)
    return {"candidates": repo_pool(), "next": iso(next_slot([s["repo_time"]], now())), "last": last and {
        "id": last["id"], "status": last["status"], "created": last["created"],
        "msg": next((n.get("msg") for n in reversed(list(last["nodes"].values())) if n.get("msg")), "")},
        "notes_tr": next(((read_json(f, {}) or {}).get("notes_tr") for f in sorted(REPO_DIR.glob("*_picks.json"), reverse=True)), "")}


def n_cover(run):
    tail = sh(run, "cover", [PY, "cover.py", run.s["content"]])
    t = next((x for x in tail if x.startswith(("photo:", "flux:"))), "tamam")
    return t.replace("photo: File:", "Foto: ").replace("photo: ", "Foto: ")[:120]


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
    if run.s["kind"] == "clip": return n_clip_qa(run)
    frames = reel_frames(run)
    claude(run, "qa", "qa", content=run.s["content"], name=content_path(run).stem,
           frames=", ".join(frames) or "none", result=f"runs/{run.id}/qa.json")
    r = read_json(run.dir / "qa.json")
    if r is None: raise StepError("qa.json yazılmadı")
    return "sorun yok" if r.get("ok") else "dikkat: " + "; ".join(r.get("problems", []))[:120]


def publish_at(run):
    """The planned publish time of a run from the share pool (None = as soon as it's ready)."""
    t = run.s.get("publish_at")
    return datetime.fromisoformat(t).astimezone() if t else None


def hold(run, msg):
    """Keep a ready (approved or approval-free) run until its planned time; the scheduler releases it."""
    t = publish_at(run)
    if not t or t <= now(): return False
    run.node("approve", status="scheduled", msg=f"{msg} · {t:%d.%m %H:%M}'de paylaşılacak")
    return True


def n_approve(run):
    qa = read_json(run.dir / "qa.json", {})
    need = run.s["approval"] if "approval" in run.s else settings()["approval"]  # pool items carry their own checkbox
    if need or not qa.get("ok", True):
        t = publish_at(run)
        run.node("approve", status="waiting", msg="Önizleme hazır: Yayınla / Revize et / Reddet"
                 + (f" · planlı {t:%d.%m %H:%M}" if t else ""))
        notify("AI Playbooks", f"Onay bekliyor: {(run.s.get('title') or '')[:80]}")
        TG.event("approval", run)
        return None
    if hold(run, "Onaysız"): return None
    return "otomatik (onay kapalı)"


def publish_step(step):
    def f(run):
        if STRAT.skipped(run.s["kind"], step):  # the strategy director turned this platform off for this flow
            run.log(step, f"strategy.json skip: {run.s['kind']} / {step}"); return "atlandı (strateji: bu platform şu an kapalı)"
        tail = sh(run, step, [PY, "publish.py", run.s["content"], "--steps", step])
        st = read_json(out_dir(run) / "publish.json", {}).get(step, {})
        return st.get("link") or (tail[-1] if tail else "tamam")
    return f


def n_log(run):
    publish_step("log")(run)
    rel = run.s["content"]
    record_timings(run, "published")
    for args in (["add", rel, "publish_log.jsonl", "research", "stats"],
                 ["commit", "-q", "-m", f"{run.s['kind'] if run.s['kind'] in ('clip', 'repo') else 'post'}: {content_path(run).stem}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"],
                 ["push", "-q"]):
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           creationflags=NO_WINDOW)
        run.log("log", f"$ git {args[0]}\n{r.stdout}{r.stderr}")
        if r.returncode and not (args[0] == "commit" and "nothing to commit" in r.stdout + r.stderr):
            raise StepError(f"git {args[0]}: {(r.stderr or r.stdout).strip()[:200]}")
    links = {k: v.get("link") for k, v in read_json(out_dir(run) / "publish.json", {}).items()
             if isinstance(v, dict) and v.get("link")}
    notify("AI Playbooks", "Paylaşıldı: " + (links.get("ig_carousel") or links.get("ig_photo") or links.get("ig_reel") or run.s["content"]))
    TG.event("published", run, links=links)
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


FETCH_ERRORS = [  # yt-dlp message -> what it means for the owner
    ("private video", "Video gizli: sahibi herkese açık yapmadan indirilemez"),
    ("video unavailable", "Video kaldırılmış ya da erişilemiyor"),
    ("sign in to confirm your age", "Yaş doğrulaması isteyen video: giriş yapmadan indirilemez"),
    ("sign in to confirm you", "YouTube bot kontrolü istedi: biraz bekleyip tekrar dene"),
    ("not available in your country", "Video bu ülkede engelli"),
    ("members-only", "Sadece kanal üyelerine açık video"),
    ("no video could be found", "Bu gönderide video yok"),
    ("unsupported url", "Bu link desteklenmiyor"),
]


def n_fetch(run):
    out = out_dir(run); out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("source.*"): f.unlink()
    try:  # Node as the JS runtime: YouTube extraction without one misses formats
        sh(run, "fetch", [PY, "-m", "yt_dlp", "-q", "--no-playlist", "--js-runtimes", "node", "-f", "bv*+ba/b",
                          "--merge-output-format", "mp4", "--write-info-json", "-o", str(out / "source.%(ext)s"), run.s["url"]])
    except StepError as ex:
        s = str(ex).lower()
        why = next((tr for key, tr in FETCH_ERRORS if key in s), None)
        raise StepError(f"{why} ({ex})" if why else str(ex)) from None
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
           frames=", ".join(c["frames"]), note=note, content=run.s["content"], dm_rule=dm_rule())
    data = read_json(content_path(run))
    if not data: raise StepError(f"{run.s['content']} yazılmadı ya da geçersiz JSON")
    if data.get("reject"): raise StepError("Claude bu videoyu uygun bulmadı: " + str(data["reject"])[:200])
    if not data.get("hook") or not data.get("caption"): raise StepError("hook ya da caption eksik")
    run.status(run.s["status"], title=data["hook"])
    return data["hook"][:120]


def n_caption(run):
    """Caption agent: per-platform captions + researched hashtags (prompts/caption.md, trained by caption_playbook.md)."""
    import captions as CAP
    clip = run.s["kind"] == "clip"
    note = f"\n## Owner's note for this post (revision request)\n{run.s['note']}\n" if run.s.get("note") else ""
    repo = run.s["kind"] == "repo"
    claude(run, "caption", "caption", date=run.s["day"], content=run.s["content"], run_id=run.id, note=note,
           kind="clip" if clip else "repo" if repo else "carousel",
           kind_hint="a viral video Reel framed with our hook; IG Reel + FB Reel + YouTube Short" if clip
           else "a GitHub repo post: ONE photo (the plain repo page) on IG + FB, NO YouTube (leave captions.youtube out); "
                "follow section 6b of the playbook" if repo
           else "a carousel post; IG carousel + FB photo post, and its voiced video goes out as IG Reel + FB Reel + "
                "YouTube Short with the SAME IG/FB captions: write them so they fit both (no 'swipe', no 'slide 3')")
    data = read_json(content_path(run))
    probs = CAP.check(data or {})
    if probs: raise StepError("Caption kurallara uymuyor: " + "; ".join(probs)[:280])
    r = read_json(run.dir / "caption.json", {}) or {}
    tags = " ".join(t[0] if isinstance(t, list) else str(t) for t in (r.get("hashtags") or {}).get("instagram", []))
    return (tags or data["caption"].split("\n", 1)[0])[:120]


def n_clip_qa(run):
    out = out_dir(run); qa = run.dir / "qa"
    claude(run, "qa", "clipqa", content=run.s["content"], out=out.relative_to(ROOT).as_posix(),
           source_frames=", ".join(run.s["clip"]["frames"]), result=f"runs/{run.id}/qa.json")
    r = read_json(run.dir / "qa.json")
    if r is None: raise StepError("qa.json yazılmadı")
    frames_of(out / "reel.mp4", qa, n=5)  # the preview shows the final version (QA may have re-framed)
    return "sorun yok" if r.get("ok") else "dikkat: " + "; ".join(r.get("problems", []))[:120]


def n_frame(run):
    sh(run, "frame", [PY, "clip.py", run.s["content"]])
    secs = (read_json(out_dir(run) / "meta.json", {}) or {}).get("secs")
    return f"{secs} sn" if secs else "tamam"


PHASES = {"trigger": "scan", "collect": "scan", "scout": "scan", "pool": "scan", "hooks": "scan", "choose": "wait", "write": "production", "cover": "production",
          "fetch": "production", "hook": "production", "caption": "production", "frame": "production",
          "carousel": "production", "reel": "production", "qa": "production", "approve": "wait", "upload": "publish", "card": "production", "rreel": "production", "ig_photo": "publish",
          "rcollect": "scan", "rscout": "scan", "review": "scan",
          "ig_carousel": "publish", "ig_reel": "publish", "fb_photos": "publish", "fb_reel": "publish", "yt_short": "publish", "x_post": "publish", "tiktok": "publish", "comments": "publish", "dm": "publish", "log": "publish"}


def secs_between(a, b):
    if not a: return 0
    return max(0, round(((datetime.fromisoformat(b) if b else now()) - datetime.fromisoformat(a)).total_seconds()))


def timings(run):
    """Per-node time the system worked on a post run (+ its scan), earlier attempts included; totals per phase.
    The owner's own time (picking a candidate, approving) is left out on purpose: it says nothing about the pipeline."""
    flows = []
    scan = Run(run.s["scan"]) if run.s.get("scan") and (RUNS / run.s["scan"] / "state.json").exists() else None
    if scan and scan.s: flows.append(scan.s)
    flows.append(run.s)
    rows = []
    for s in flows:
        for nid, label, _ in FLOWS[s["kind"]]:
            if PHASES[nid] == "wait": continue
            n = s["nodes"][nid]
            tries = n.get("attempts", []) + ([n] if n.get("started") else [])
            secs = sum(secs_between(t.get("started"), t.get("ended")) for t in tries)
            rows.append({"node": nid, "label": label, "phase": PHASES[nid], "secs": secs, "attempts": len(tries),
                         "status": n["status"]})
    tot = {ph: sum(r["secs"] for r in rows if r["phase"] == ph) for ph in ("scan", "production", "publish")}
    return {"run": run.id, "post": pathlib.Path(run.s["content"]).stem, "title": run.s.get("title"),
            "nodes": rows, "phases": tot, "total": sum(tot.values())}


def record_timings(run, outcome):
    (ROOT / "stats").mkdir(exist_ok=True)
    with (ROOT / "stats" / "timings.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"date": iso(), "outcome": outcome, **timings(run)}, ensure_ascii=False) + "\n")


NODES = {"trigger": n_trigger, "collect": n_collect, "scout": n_scout, "pool": n_pool, "choose": n_choose, "hooks": n_hooks,
         "write": n_write, "caption": n_caption, "card": n_card, "rreel": n_rreel, "rcollect": n_rcollect, "rscout": n_rscout, "review": n_review,
         "ig_photo": publish_step("ig_photo"), "cover": n_cover, "carousel": n_carousel, "fetch": n_fetch, "hook": n_hook, "frame": n_frame, "reel": n_reel, "qa": n_qa, "approve": n_approve,
         "upload": publish_step("upload"), "ig_carousel": publish_step("ig_carousel"), "ig_reel": publish_step("ig_reel"),
         "fb_photos": publish_step("fb_photos"), "fb_reel": publish_step("fb_reel"),
         "yt_short": publish_step("yt_short"), "x_post": publish_step("x_post"), "tiktok": publish_step("tiktok"), "comments": publish_step("comments"), "dm": publish_step("dm"), "log": n_log}


# ---------------------------------------------------------------- self-repair (owner, 2026-09-27: "no more errors for me")
# A failing step first retries on its own when it talks to a platform (hiccups), then the doctor (prompts/doctor.md,
# Claude) finds the root cause, fixes the content or makes our code robust, verifies it, and the step reruns. Only
# what can't be fixed from here (expired token, private video, no Claude usage left ...) reaches the owner, with
# what to do. Every repair is kept in the run (`repairs`) and code fixes are committed.

NO_REPAIR = {"trigger", "choose", "approve"}  # the owner's steps
PUBLISH_NODES = {"upload", "ig_carousel", "ig_photo", "ig_reel", "fb_photos", "fb_reel", "yt_short", "x_post", "tiktok", "comments", "dm", "log"}
RETRY_WAITS = [60, 300]  # seconds before plain retries of a publish step (publish.py never posts twice)
MAX_REPAIRS = 2


def log_tail(run, nid, n=80):
    f = run.dir / f"{nid}.log"
    return "\n".join(f.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]) if f.exists() else "(empty)"


def commit_repair(run, r):
    """Commit the code the doctor fixed (content files are committed by the log step when the post goes out)."""
    files = [f for f in r.get("files") or [] if f and not f.startswith(("content/", "runs/", "output/")) and ".env" not in f
             and (ROOT / f).resolve().is_relative_to(ROOT) and (ROOT / f).exists()]
    if not files: return
    msg = f"doctor: {r.get('cause_tr') or 'otomatik onarım'} ({run.id} / {r['node']})\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
    for args in (["add", *files], ["commit", "-q", "-m", msg, "--", *files], ["push", "-q"]):
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           creationflags=NO_WINDOW)
        run.log(r["node"], f"$ git {args[0]}: {(p.stdout + p.stderr).strip()[:300]}")
        if p.returncode: break


def repair(run, nid, label, ex, attempt):
    run.node(nid, msg=f"Otomatik onarım {attempt}/{MAX_REPAIRS}: {str(ex)[:100]}")
    run.log(nid, f"\n----- otomatik onarım {attempt} {iso()} -----")
    res = run.dir / f"doctor_{nid}.json"; res.unlink(missing_ok=True)
    hist = [{k: r.get(k) for k in ("cause_tr", "changes", "kind")} for r in run.s.get("repairs", []) if r.get("node") == nid]
    try: out = out_dir(run).relative_to(ROOT).as_posix() if run.s.get("content") else "(none)"
    except Exception: out = "(none)"
    try:
        claude(run, nid, "doctor", prompt_name=f"doctor_{nid}", run_id=run.id, kind=run.s["kind"], node=nid, label=label,
               attempt=attempt, content=run.s.get("content") or "(none: this flow has no content file)", out=out,
               error=f"{type(ex).__name__}: {str(ex)[:800]}", history=json.dumps(hist, ensure_ascii=False) if hist else "none",
               log=log_tail(run, nid).replace("```", "'''"))
        r = read_json(res, {}) or {"fixed": False, "retry": False, "kind": "unknown", "cause_tr": "onarım sonucu yazılmadı"}
    except Canceled: raise
    except Exception as e2:
        r = {"fixed": False, "retry": False, "kind": "external", "cause_tr": f"onarım çalışamadı: {str(e2)[:160]}"}
    r.update(node=nid, at=iso(), error=str(ex)[:300])
    with LOCK: run.s.setdefault("repairs", []).append(r); run.save()
    slog(run.id, nid, "repair", attempt, r.get("kind"), r.get("fixed"), r.get("cause_tr"))
    if r.get("kind") == "code" and r.get("fixed"):
        try: commit_repair(run, r)
        except Exception as e3: run.log(nid, f"commit: {e3}")
    return r


def wait_or_cancel(run, secs):
    for _ in range(int(secs)):
        if run.id in CANCELED: raise Canceled()
        time.sleep(1)


def execute(run):
    """Run the flow's nodes from the first one that isn't done. Stops at a waiting node or an error that the
    self-repair couldn't fix."""
    run.status("running"); CANCELED.discard(run.id)
    for nid, label, _ in FLOWS[run.s["kind"]]:
        if run.s["nodes"][nid]["status"] == "done": continue
        run.node(nid, status="running", started=iso(), ended=None, msg="")
        t0 = time.time(); waits = list(RETRY_WAITS) if nid in PUBLISH_NODES else []; repairs = []
        max_rep = 0 if nid in NO_REPAIR else 1 if run.s["kind"] in BACKGROUND else MAX_REPAIRS
        while True:
            try:
                msg = NODES[nid](run); break
            except Canceled:
                run.node(nid, status="error", ended=iso(), msg="Durduruldu"); run.status("canceled"); return
            except Exception as ex:
                run.log(nid, f"HATA: {type(ex).__name__}: {ex}")
                slog(run.id, nid, "error:", ex)
                try:
                    if run.id in CANCELED: raise Canceled()
                    if waits:  # platform hiccup? same step again after a pause
                        w = waits.pop(0)
                        run.node(nid, msg=f"Geçici sorun, {w // 60} dk sonra tekrar deneniyor")
                        run.log(nid, f"----- {w} sn sonra tekrar deneniyor -----")
                        wait_or_cancel(run, w); continue
                    if len(repairs) < max_rep:
                        r = repair(run, nid, label, ex, len(repairs) + 1); repairs.append(r)
                        if r.get("retry"):
                            run.node(nid, msg=f"Onarıldı, tekrar çalışıyor: {r.get('cause_tr', '')[:100]}"); continue
                except Canceled:
                    run.node(nid, status="error", ended=iso(), msg="Durduruldu"); run.status("canceled"); return
                last = repairs[-1] if repairs else {}
                why = last.get("cause_tr") or str(ex)
                todo = last.get("owner_action_tr") or ""
                text = f"{why}" + (f" · Yapman gereken: {todo}" if todo else "") + (f" ({len(repairs)} otomatik onarım denendi)" if repairs else "")
                run.node(nid, status="error", ended=iso(), msg=text[:400]); run.status("error")
                if run.s["kind"] not in BACKGROUND:  # background errors show up in the next delivery's notes instead
                    notify("AI Playbooks: yardım gerekiyor", f"{label}: {text[:160]}")
                    TG.event("error", run, label=label, node=nid, msg=text)
                return
        if run.s["nodes"][nid]["status"] in ("waiting", "scheduled"):
            run.status(run.s["nodes"][nid]["status"]); return
        fixed = [r for r in repairs if r.get("retry")]
        run.node(nid, status="done", ended=iso(), secs=round(time.time() - t0),
                 msg=(msg or "") + (f" · 🔧 kendi onardı: {fixed[-1].get('cause_tr', '')[:80]}" if fixed else ""))
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


def start_bg(kind, trigger_msg):
    """A background gather / learn job in its own thread (never two of the same kind at once)."""
    with LOCK:
        if any(s["kind"] == kind and s["status"] in ("running", "queued") for s in all_runs()): return None
        t = now(); rid = f"{kind}-{t:%Y%m%d-%H%M%S}"
        run = Run.create(kind, rid, day=f"{t:%Y-%m-%d}", hhmm=f"{t:%H%M}", trigger_msg=trigger_msg)
    threading.Thread(target=execute, args=(run,), daemon=True).start()
    slog(kind, "started:", rid, trigger_msg)
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
            for kind, times, key in (("gather", s["gather_times"], "last_gather_slot"), ("learn", s["learn_times"], "last_learn_slot"),
                                     ("repos", [s["repo_time"]], "last_repo_slot"), ("strategy", [s["strategy_time"]], "last_strategy_slot")):
                slot = last_slot(times, t)
                if slot and (not s.get(key) or s[key] < slot.isoformat()):
                    if start_bg(kind, f"Planlı {slot:%H:%M}" + (" (telafi)" if t - slot > timedelta(minutes=10) else "")):
                        s = settings(); s[key] = slot.isoformat(); save_settings(s)
        except Exception as ex:
            slog("scheduler error:", ex)
        try: autopilot_tick()
        except Exception as ex: slog("autopilot error:", ex)
        try: share_tick()
        except Exception as ex: slog("share pool error:", ex)
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
            if s["kind"] in ("scan",) + BACKGROUND: threading.Thread(target=execute, args=(run,), daemon=True).start()
            else: enqueue(run)
        elif s["status"] == "queued" and s["kind"] in ("post", "clip", "repo"):
            POST_Q.put(s["id"])


# ---------------------------------------------------------------- actions (called from the UI)

def scan_candidate(scan_id, cand_id):
    scan = Run(scan_id)
    cands = load_candidates(scan.s["candidates_file"], scan_id).get("candidates", [])
    c = next((x for x in cands if x["id"] == cand_id), None)
    if not c: raise ValueError("aday bulunamadı (ya da daha önce paylaşıldı)")
    return scan, c


def mark_chosen(scan, cand_id, rid, how="Seçildi"):
    chosen = [x for x in scan.s.get("chosen", []) if x["id"] != cand_id] + [{"id": cand_id, "run": rid}]
    scan.status(scan.s["status"] if scan.s["status"] != "waiting" else "done", chosen=chosen)
    title = next((c.get("title", "") for c in load_candidates(scan.s["candidates_file"], scan.id).get("candidates", [])
                  if c["id"] == cand_id), "")
    scan.node("choose", status="done", msg=f"{how}: {title[:60]}", ended=iso())


def start_post(c, scan_id=None, **extra):
    t = now(); day = f"{t:%Y-%m-%d}"
    slug = re.sub(r"[^a-z0-9-]+", "-", c["id"].lower()).strip("-")[:50] or "post"
    content = f"content/{day}_{slug}.json"; k = 2
    while (ROOT / content).exists(): content = f"content/{day}_{slug}-{k}.json"; k += 1
    run = Run.create("post", f"post-{t:%Y%m%d-%H%M%S}-{slug}"[:80], day=day, candidate=c, content=content,
                     title=c.get("title"), **({"scan": scan_id} if scan_id else {}), **extra)
    enqueue(run)
    return run


def select(scan_id, cand_id):
    scan, c = scan_candidate(scan_id, cand_id)
    run = start_post(c, scan_id)
    mark_chosen(scan, cand_id, run.id)
    return run.id


def packs():
    """The prompt pack library (prompt_packs.json) with each pack's state: used = a post was made from it."""
    lib = read_json(ROOT / "prompt_packs.json", {}) or {}
    done = {p["candidate"] or p["slug"]: p["name"] for p in posted()}
    busy = {r["candidate"].get("id"): r["id"] for r in all_runs()
            if r["kind"] == "post" and r["status"] not in ("rejected", "canceled", "done") and r.get("candidate")}
    cats = lib.get("categories", {})
    return {"categories": cats, "packs": [{**p, "category_tr": cats.get(p["category"], p["category"]),
                                           "used": done.get(p["id"]), "run": busy.get(p["id"])} for p in lib.get("packs", [])]}


def pack_candidate(pack_id):
    p = next((x for x in packs()["packs"] if x["id"] == pack_id), None)
    if not p: raise ValueError("paket bulunamadı")
    if p["used"]: raise ValueError(f"bu paket zaten paylaşıldı ({p['used']})")
    if p["run"]: raise ValueError("bu paket zaten üretimde")
    return {"id": p["id"], "tool": "Prompt pack", "kind": "prompts", "title": p["headline"], "summary_tr": p["title_tr"],
            "angle": " · ".join(x["name"] for x in p["prompts"]), "tools": p["tools"], "sources": [],
            "pack": {k2: p[k2] for k2 in ("title", "em", "headline", "headline_em", "person", "photo_query", "prompts", "category")}}


def select_pack(pack_id):
    """Start a post from a library pack (no scan needed)."""
    return start_post(pack_candidate(pack_id)).id


def check_clip_url(url):
    url = url.strip()
    if not re.match(r"https?://\S+$", url): raise ValueError("geçerli bir video bağlantısı değil")
    log = ROOT / "publish_log.jsonl"
    done = {str(json.loads(l).get("source_url") or "").split("?")[0] for l in log.read_text(encoding="utf-8").splitlines()
            if l.strip()} if log.exists() else set()
    if url.split("?")[0] in done: raise ValueError("bu video zaten paylaşıldı")
    return url


def start_clip(url, note="", **extra):
    url = check_clip_url(url)
    t = now(); day = f"{t:%Y-%m-%d}"
    m = re.search(r"/status/(\d+)", url)
    slug = (m.group(1)[-8:] if m else re.sub(r"[^a-z0-9]+", "-", url.lower().split("//")[-1])[-30:].strip("-")) or "clip"
    content = f"content/clips/{day}_clip-{slug}.json"; k = 2
    while (ROOT / content).exists(): content = f"content/clips/{day}_clip-{slug}-{k}.json"; k += 1
    (ROOT / "content" / "clips").mkdir(parents=True, exist_ok=True)
    run = Run.create("clip", f"clip-{t:%Y%m%d-%H%M%S}-{slug}"[:80], day=day, url=url, content=content,
                     title=url, candidate={"title": url}, **({"note": note.strip()} if note.strip() else {}), **extra)
    enqueue(run)
    return run.id


# ---------------------------------------------------------------- share pool (owner, 2026-09-27)
# The owner drops clip links (Viral tab) and news / packs ("Havuza at") into a pool, ticks "onay" per item and either
# shares now or plans a time. Production starts LEAD minutes before the planned time; a finished run waits at the
# approve node ("scheduled") until then. Approval ticked -> it comes to the owner first; unticked -> posted as is
# (a QA problem still asks, like the global switch).

SHARE = RUNS / "share_pool.json"
LEAD = {"clip": 45, "post": 90, "repo": 30}  # minutes of production (+ time to approve) before the planned time


def share_items():
    return read_json(SHARE, []) or []


def save_share(items):
    with LOCK: write_json(SHARE, items)


def share_add(kind, approval=True, url="", note="", scan=None, candidate=None, pack=None, repo=None):
    items = share_items(); live = [i for i in items if i["status"] in ("pool", "producing")]
    t = now(); item = {"id": f"s{t:%Y%m%d%H%M%S%f}"[:21], "kind": kind, "added": iso(t), "approval": bool(approval),
                       "at": None, "status": "pool"}
    if kind == "clip":
        url = check_clip_url(url)
        if any(i.get("url", "").split("?")[0] == url.split("?")[0] for i in live): raise ValueError("bu link zaten havuzda")
        item.update(url=url, note=note.strip(), title=url)
    elif kind == "repo":
        c = repo_candidate(repo)
        if any((i.get("candidate") or {}).get("id") == c["id"] for i in live): raise ValueError("bu repo zaten havuzda")
        item.update(candidate=c, title=c.get("title") or c.get("full_name"))
    else:
        if pack: c = pack_candidate(pack)
        else: sc, c = scan_candidate(scan, candidate); item["scan"] = scan
        if any((i.get("candidate") or {}).get("id") == c["id"] for i in live): raise ValueError("bu içerik zaten havuzda")
        item.update(candidate=c, title=c.get("title"))
        if not pack: mark_chosen(sc, c["id"], "", how="Havuza atıldı")
    save_share(items + [item])
    return item["id"]


def share_start(item):
    """Start production for a pool item (called with LOCK held via share_tick or share_now)."""
    extra = {"approval": item["approval"], "share": item["id"], **({"publish_at": item["at"]} if item.get("at") else {})}
    if item["kind"] == "clip": rid = start_clip(item["url"], item.get("note", ""), **extra)
    elif item["kind"] == "repo": rid = start_repo(item["candidate"], **extra).id
    else:
        rid = start_post(item["candidate"], item.get("scan"), **extra).id
        if item.get("scan") and (RUNS / item["scan"] / "state.json").exists():
            mark_chosen(Run(item["scan"]), item["candidate"]["id"], rid, how="Havuzdan üretiliyor")
    item.update(status="producing", run=rid, started=iso())


def share_edit(sid, approval=None, at=False, remove=False, now_=False):
    with LOCK:
        items = share_items(); item = next((i for i in items if i["id"] == sid), None)
        if not item: raise ValueError("havuzda böyle bir öğe yok")
        run = Run(item["run"]) if item.get("run") and (RUNS / item["run"] / "state.json").exists() else None
        busy = run and run.s["status"] not in ("done", "rejected", "canceled", "error")
        if remove:
            if busy: raise ValueError("üretimde: önce kanvastan durdur ya da reddet")
            items.remove(item)
        if approval is not None:
            item["approval"] = bool(approval)
            if run and run.s["nodes"]["approve"]["status"] in ("idle", "running"): run.s["approval"] = bool(approval); run.save()
        if at is not False:  # "" or None clears the plan
            item["at"] = datetime.fromisoformat(at).astimezone().isoformat(timespec="seconds") if at else None
            if run and run.s["status"] not in ("done",):
                run.s["publish_at"] = item["at"]; run.save()
                if not item["at"] and run.s["status"] == "scheduled": release(run)
        if now_:
            item["at"] = None
            if item["status"] in ("pool", "error", "canceled") and not busy: share_start(item)
            elif run and run.s["status"] == "scheduled": run.s.pop("publish_at", None); run.save(); release(run)
            elif run: run.s.pop("publish_at", None); run.save()
        save_share(items)


def share_tick():
    """Scheduler: start planned items on time, release scheduled runs, mirror run results into the pool."""
    with LOCK:
        items = share_items(); t = now(); changed = False
        for i in items:
            run = Run(i["run"]) if i.get("run") and (RUNS / i["run"] / "state.json").exists() else None
            if i["status"] == "pool" and i.get("at"):
                if datetime.fromisoformat(i["at"]) - timedelta(minutes=LEAD[i["kind"]]) <= t:
                    try: share_start(i)
                    except ValueError as ex: i.update(status="error", error=str(ex))
                    changed = True
            elif i["status"] == "producing" and run:
                st = run.s["status"]
                new = {"done": "done", "rejected": "canceled", "canceled": "canceled", "error": "error"}.get(st)
                if new == "error" and run.s["nodes"].get("approve", {}).get("status") == "done": new = None  # publish retry pending
                if new: i["status"] = new; changed = True
                if st == "scheduled" and publish_at(run) and publish_at(run) <= t: release(run)
            elif i["status"] == "error" and run and run.s["status"] in ("queued", "running", "waiting", "scheduled"):
                i["status"] = "producing"; changed = True  # the owner retried the run from the canvas
        if changed: save_share(items)
    for s in all_runs():  # scheduled runs that don't come from the pool item list (e.g. item removed)
        if s["status"] == "scheduled" and not any(i.get("run") == s["id"] for i in items):
            r = Run(s["id"])
            if not publish_at(r) or publish_at(r) <= now(): release(r)


# ---------------------------------------------------------------- autopilot (owner, 2026-09-28: "never ask me, you decide
# what goes out when"). Fills every free publish slot of the next ~day from the pools: a clip the owner dropped in the
# Viral pool first, else a rotation of news / GitHub repo / prompt pack (next format when one pool is empty). Items are
# normal share-pool items (approval off, `auto`), so production, "scheduled" and publishing work as for planned ones.

AUTO = {"checked": 0.0}
CLIP_DAYS = 3  # clips found by the strategy director stay usable this long


def auto_clip(taken):
    """A viral clip found by the strategy director (research/clips/<date>_clips.json), not posted, not planned."""
    cut = f"{now() - timedelta(days=CLIP_DAYS):%Y-%m-%d}"
    live = {(i.get("url") or "").split("?")[0] for i in share_items() if i["status"] in ("pool", "producing", "done")}
    for f in sorted((ROOT / "research" / "clips").glob("*_clips.json"), reverse=True):
        if f.name[:10] < cut: break
        for c in (read_json(f, {}) or {}).get("clips", []):
            u = (c.get("url") or "").split("?")[0]
            if not u or u in live or u in taken: continue
            try: check_clip_url(u)
            except ValueError: continue
            return {"id": u, "url": u, "note": c.get("hook_idea") or "", "title": u, "why": c.get("why")}
    return None


def auto_news(taken):
    done = posted(); ids = {x for p in done for x in (p["candidate"], p["slug"]) if x}
    urls = {_url(u) for p in done for u in p["sources"] if not GENERIC_URL.search(u)}
    cands = [c for c in pool_items().values() if c.get("kind") in ("news", "evergreen") and c["id"] not in ids | taken
             and not any(_url(u) in urls for u in c.get("sources", []) if c.get("kind") == "news")]
    cut = f"{now() - timedelta(hours=48):%Y-%m-%dT%H:%M}"
    cands.sort(key=lambda c: (c.get("kind") != "news" or c["first_seen"] < cut, -(c.get("score") or 0)))
    return cands[0] if cands else None


def auto_pack(taken):
    ps = [p for p in packs()["packs"] if not p["used"] and not p["run"] and p["id"] not in taken]
    if not ps: return None
    recent = [pathlib.Path(r["content"]).stem for r in all_runs() if r["kind"] == "post" and "pack" in (r.get("content") or "")][:5]
    used_cats = {p["category"] for p in packs()["packs"] if p["used"] in recent}
    ps.sort(key=lambda p: p["category"] in used_cats)
    return pack_candidate(ps[0]["id"])


def auto_repo(taken):
    c = next((c for c in repo_pool() if not c.get("run") and c["id"] not in taken and (c.get("score") or 0) >= 6), None)
    return {k: v for k, v in c.items() if k != "run"} if c else None


def autopilot_tick():
    s = settings()
    if not s.get("autopilot") or time.time() - AUTO["checked"] < 600: return
    AUTO["checked"] = time.time(); t = now(); planned = []
    with LOCK:
        items = share_items()
        live = [i for i in items if i["status"] in ("pool", "producing")]
        taken = {(i.get("candidate") or {}).get("id") for i in live}
        slots = []; strat = STRAT.load(); rot = STRAT.rotation(strat)
        slots_today = strat.get("post_slots") or s["post_slots"]
        for d in (t.date(), t.date() + timedelta(days=1)):
            for hm in slots_today:
                h, m = map(int, hm.split(":")); at = datetime(d.year, d.month, d.day, h, m).astimezone()
                if t + timedelta(minutes=100) <= at <= t + timedelta(hours=26): slots.append(at)
        for n, at in enumerate(sorted(slots)):
            if any(i.get("at") and abs(datetime.fromisoformat(i["at"]) - at) < timedelta(minutes=45) for i in live): continue
            clip = next((i for i in live if i["kind"] == "clip" and i["status"] == "pool" and not i.get("at")), None)
            if clip:
                clip["at"] = at.isoformat(timespec="seconds"); planned.append(("clip", clip.get("title"), at)); continue
            start = (at.timetuple().tm_yday * len(slots_today) + slots_today.index(f"{at:%H:%M}")) % len(rot) \
                if f"{at:%H:%M}" in slots_today else n
            order = rot[start:] + rot[:start]
            for kind in list(dict.fromkeys(order)) + [k for k in ("news", "repo", "pack") if k not in order]:
                c = {"news": auto_news, "repo": auto_repo, "pack": auto_pack, "clip": auto_clip}[kind](taken)
                if c: break
            else:
                continue
            item = {"id": f"s{now():%Y%m%d%H%M%S%f}"[:21], "added": iso(), "approval": False, "auto": True,
                    "at": at.isoformat(timespec="seconds"), "status": "pool"}
            if kind == "clip": item.update(kind="clip", url=c["url"], note=c["note"], title=c["url"])
            else: item.update(kind="repo" if kind == "repo" else "post", candidate=c, title=c.get("title") or c.get("full_name"))
            items.append(item); live.append(item); taken.add(c["id"])
            planned.append((kind, item["title"], at))
        if planned: save_share(items)
    if planned:
        slog("autopilot planned:", "; ".join(f"{k} {a:%d.%m %H:%M}" for k, _, a in planned))
        TG.event("plan", None, planned=planned)


def share_state():
    runs = {r["id"]: r for r in all_runs()}
    out = []
    for i in share_items():
        r = runs.get(i.get("run")) or {}
        out.append({**i, "run_status": r.get("status"), "run_msg": next((n.get("msg") for n in reversed(list((r.get("nodes") or {}).values()))
                                                                        if n.get("status") in ("running", "waiting", "scheduled", "error") and n.get("msg")), "")})
    return out


def approve(rid):
    run = Run(rid)
    if run.s["nodes"]["approve"]["status"] != "waiting": raise ValueError("bu gönderi onay beklemiyor")
    if hold(run, f"Onaylandı {now():%H:%M}"): run.status("scheduled"); return
    run.node("approve", status="done", ended=iso(), msg=f"Onaylandı {now():%H:%M}")
    enqueue(run)


def release(run):
    """A scheduled run's time has come (or the owner pressed "Şimdi paylaş"): publish."""
    msg = run.s["nodes"]["approve"].get("msg", "").split(" · ")[0]
    run.node("approve", status="done", ended=iso(), msg=f"{msg} · {now():%H:%M}'de yayına çıktı")
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
    if run.s["kind"] in ("scan",) + BACKGROUND: threading.Thread(target=execute, args=(run,), daemon=True).start()
    else: enqueue(run)


def cancel(rid):
    run = Run(rid); CANCELED.add(rid)
    p = PROCS.get(rid)
    if p:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, creationflags=NO_WINDOW)
    elif run.s["status"] in ("queued", "scheduled"):
        run.status("canceled")


def state():
    s = settings(); runs = all_runs()
    for r in runs:
        if r["kind"] == "scan" and r.get("candidates_file"):
            r["candidates"] = load_candidates(r["candidates_file"], r["id"])
    fg = [r for r in runs if r["kind"] not in BACKGROUND][:40]
    bg = {}
    for kind, times in (("gather", s["gather_times"]), ("learn", s["learn_times"]), ("repos", [s["repo_time"]]), ("strategy", [s["strategy_time"]])):
        last = next((r for r in runs if r["kind"] == kind), None)
        bg[kind] = {"next": iso(next_slot(times, now())), "last": last and {
            "id": last["id"], "status": last["status"], "created": last["created"],
            "msg": next((n.get("msg") for n in reversed(list(last["nodes"].values())) if n.get("msg")), "")}}
    bg["pool"] = len(pool_items())
    return {"settings": {k: s[k] for k in ("scan_times", "approval", "gather_times", "learn_times", "dm_bot", "repo_time", "autopilot", "post_slots")},
            "next_scan": iso(next_slot(s["scan_times"], now())), "now": iso(), "background": bg,
            "flows": {k: [{"id": n, "label": l, "kind": t} for n, l, t in v] for k, v in FLOWS.items()},
            "runs": fg, "share": share_state(), "lead": LEAD}


def run_detail(rid):
    run = Run(rid); s = dict(run.s)
    if s["kind"] == "clip":
        out = out_dir(run); rel = out.relative_to(ROOT).as_posix()
        s["content_data"] = read_json(content_path(run)) or read_json(run.dir / content_path(run).name)
        s["slides"] = []
        s["reel"] = f"{rel}/reel.mp4" if (out / "reel.mp4").exists() else None
        s["publish"] = read_json(out / "publish.json", {})
        s["qa_result"] = read_json(run.dir / "qa.json")
        s["qa_frames"] = [f"runs/{rid}/qa/{p.name}" for p in sorted((run.dir / "qa").glob("*.jpg"))]
    if s["kind"] == "repo":
        out = out_dir(run); rel = out.relative_to(ROOT).as_posix()
        s["content_data"] = read_json(content_path(run)) or read_json(run.dir / content_path(run).name)
        s["slides"] = [f"{rel}/{f.name}" for f in sorted(out.glob("slide_*.png"))]
        s["reel"] = f"{rel}/reel.mp4" if (out / "reel.mp4").exists() else None; s["write_result"] = read_json(run.dir / "write.json")
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
         ".woff2": "font/woff2", ".wav": "audio/wav", ".log": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8"}


def home_state():
    """Numbers for the portfolio home page (/): each portfolio's own summary, nothing shared."""
    today = f"{now():%Y-%m-%d}"
    try: posted = sum(1 for l in (ROOT / "publish_log.jsonl").read_text(encoding="utf-8").splitlines() if f'"date": "{today}' in l)
    except OSError: posted = 0
    plan = sorted((i for i in share_items() if i["status"] == "pool" and i.get("at")), key=lambda i: i["at"])
    nxt = datetime.fromisoformat(plan[0]["at"]).strftime("%H:%M") if plan else None
    s = settings()
    return {"ai": {"today": posted, "next": nxt, "queue": len(plan),
                   "chips": [("Otopilot açık" if s.get("autopilot") else "Otopilot kapalı"), "IG · FB · YT · TikTok · X"]},
            "starseed": SS.summary()}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        if not isinstance(body, bytes): body = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def gate(self, u, q):
        """Phone access through the tunnel needs the key (remote.py); True = handled (refused or redirected)."""
        ok, set_cookie = remote.authorized(self.headers, q)
        if not ok:
            self.send(401, "<h3>AI Playbooks Studio</h3><p>Bu link geçersiz ya da eski. Telegram'a <b>link</b> yaz, yenisini gönderirim.</p>".encode(),
                      TYPES[".html"])
            return True
        if set_cookie:  # drop the key from the address bar, keep it in a cookie
            rest = urllib.parse.urlencode({k: v for k, v in q.items() if k != "k"})
            self.send_response(302); self.send_header("Set-Cookie", remote.cookie_header())
            self.send_header("Location", u.path + ("?" + rest if rest else "")); self.send_header("Content-Length", "0"); self.end_headers()
            return True
        return False

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query))
        if self.gate(u, q): return
        try:
            page = {"/": "home.html", "/ai-playbooks": "index.html", "/starseed": "starseed.html"}.get(u.path.rstrip("/") or "/")
            if page: return self.send(200, (ROOT / "studio" / page).read_bytes(), TYPES[".html"])
            if u.path == "/api/home": return self.send(200, home_state())
            if u.path == "/api/starseed/state": return self.send(200, SS.state())
            if u.path.startswith("/starseed/file/"):
                f = SS.file_path(urllib.parse.unquote(u.path[len("/starseed/file/"):]))
                return self.send_file(f) if f else self.send(404, {"error": "yok"})
            if u.path == "/api/state": return self.send(200, state())
            if u.path == "/api/run": return self.send(200, run_detail(q["id"]))
            if u.path == "/api/history": return self.send(200, history())
            if u.path == "/api/packs": return self.send(200, packs())
            if u.path == "/api/repos": return self.send(200, repos_state())
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
        if not remote.authorized(self.headers, {})[0]: return self.send(401, {"error": "anahtar gerekli"})
        try:
            b = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if u.path == "/api/starseed/voice": SS.set_voice(b["race"], b.get("voice")); return self.send(200, {"ok": True})
            if u.path == "/api/gather":
                rid = start_bg("gather", "Elle başlatıldı")
                return self.send(200 if rid else 409, {"run": rid} if rid else {"error": "zaten bir toplama çalışıyor"})
            if u.path == "/api/repos/scan":
                rid = start_bg("repos", "Elle başlatıldı")
                return self.send(200 if rid else 409, {"run": rid} if rid else {"error": "repo araması zaten çalışıyor"})
            if u.path == "/api/repo": return self.send(200, {"run": start_repo(repo_candidate(b["repo"])).id})
            if u.path == "/api/strategy":
                rid = start_bg("strategy", "Elle başlatıldı")
                return self.send(200 if rid else 409, {"run": rid} if rid else {"error": "strateji analizi zaten çalışıyor"})
            if u.path == "/api/learn":
                rid = start_bg("learn", "Elle başlatıldı")
                return self.send(200 if rid else 409, {"run": rid} if rid else {"error": "zaten çalışıyor"})
            if u.path == "/api/scan":
                rid = start_scan("Elle başlatıldı (Şimdi tara)")
                return self.send(200 if rid else 409, {"run": rid} if rid else {"error": "zaten bir tarama çalışıyor"})
            if u.path == "/api/select": return self.send(200, {"run": select(b["scan"], b["candidate"])})
            if u.path == "/api/pack": return self.send(200, {"run": select_pack(b["pack"])})
            if u.path == "/api/clip": return self.send(200, {"run": start_clip(b.get("url", ""), b.get("note", ""))})
            if u.path == "/api/share/add":
                return self.send(200, {"id": share_add(b["kind"], b.get("approval", True), b.get("url", ""), b.get("note", ""),
                                                       b.get("scan"), b.get("candidate"), b.get("pack"), b.get("repo"))})
            if u.path == "/api/share/edit":
                share_edit(b["id"], b.get("approval"), b["at"] if "at" in b else False, bool(b.get("remove")), bool(b.get("now")))
                return self.send(200, {"ok": True})
            if u.path == "/api/approve": approve(b["run"]); return self.send(200, {"ok": True})
            if u.path == "/api/revise": revise(b["run"], b.get("note", "")); return self.send(200, {"ok": True})
            if u.path == "/api/reject": reject(b["run"]); return self.send(200, {"ok": True})
            if u.path == "/api/retry": retry(b["run"], b["node"]); return self.send(200, {"ok": True})
            if u.path == "/api/cancel": cancel(b["run"]); return self.send(200, {"ok": True})
            if u.path == "/api/metrics/refresh": return self.send(200, {"started": refresh_metrics()})
            if u.path == "/api/settings":
                s = settings()
                if "approval" in b: s["approval"] = bool(b["approval"])
                if "dm_bot" in b: s["dm_bot"] = bool(b["dm_bot"])
                if "autopilot" in b: s["autopilot"] = bool(b["autopilot"]); AUTO["checked"] = 0.0
                if "post_slots" in b:
                    times = sorted({t for t in b["post_slots"] if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t)})
                    if not times: raise ValueError("otopilot için geçerli yayın saati yok (SS:DD)")
                    s["post_slots"] = times; AUTO["checked"] = 0.0
                if "scan_times" in b:
                    times = sorted({t for t in b["scan_times"] if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t)})
                    if not times: raise ValueError("geçerli saat yok (SS:DD)")
                    s["scan_times"] = times
                    s["last_slot"] = (last_slot(times, now()) or now()).isoformat()  # new times start from now on
                if "gather_times" in b:
                    times = sorted({t for t in b["gather_times"] if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t)})
                    if not times: raise ValueError("toplama için geçerli saat yok (SS:DD)")
                    s["gather_times"] = times; s["last_gather_slot"] = (last_slot(times, now()) or now()).isoformat()
                if b.get("repo_time"):
                    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", b["repo_time"]): raise ValueError("repo arama saati geçersiz")
                    s["repo_time"] = b["repo_time"]; s["last_repo_slot"] = (last_slot([b["repo_time"]], now()) or now()).isoformat()
                if "learn_times" in b:
                    times = sorted({t for t in b["learn_times"] if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t)})
                    if not times: raise ValueError("öğrenme için geçerli saat yok (SS:DD)")
                    s["learn_times"] = times; s["last_learn_slot"] = (last_slot(times, now()) or now()).isoformat()
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
    TG.start(sys.modules[__name__])
    remote.start(a.port, slog, on_link=lambda: TG.event("link", None))
    slog(f"Studio running at http://localhost:{a.port}")
    if not a.no_browser: webbrowser.open(f"http://localhost:{a.port}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
