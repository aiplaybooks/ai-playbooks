"""Telegram remote control for the Studio: the owner writes or sends voice messages from the phone, the bot pushes
candidates, approval previews (cover, slides, video), publish links and errors.

Runs inside studio.py (start(studio) spawns a long-polling thread; no webhook, no open port). Setup: create a bot with
@BotFather, put TELEGRAM_BOT_TOKEN in .env. The first chat that sends /start becomes the only allowed chat
(TELEGRAM_CHAT_ID is written to .env); every other chat is ignored.

Commands (typed or spoken, Turkish; voice goes through stt.py = faster-whisper in the Pinokio TTS env):
    tara / şimdi tara            start a scan
    adaylar                      the latest scan's candidates, with "Seç" buttons
    3 / 3'ü seç / gemini'yi seç  pick a candidate (always asks "Evet/Hayır" first)
    durum                        what is running / waiting
    önizle                       send the waiting approval preview again
    yayınla / reddet             need a confirmation tap
    revize: <note> / revize et <note>
    a link (x.com/...)           start a viral Reel from it
    yardım
Buttons use short ids kept in memory (Telegram limits callback data to 64 bytes).
"""
import os, re, json, time, uuid, random, pathlib, threading, subprocess, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).parent.resolve()
STT_PY = os.environ.get("KOKORO_PYTHON", r"E:\pinokio-new\api\Ultimate-TTS-Studio.git\app\tts_env\python.exe")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
S = None            # the studio module
TOKEN = None
CHAT = None
ACTIONS = {}        # short id -> (kind, payload)
LOCK = threading.Lock()


def env():
    out = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def log(*a):
    try: S.slog("telegram:", *a)
    except Exception: pass  # noqa: BLE001


# ---------------------------------------------------------------- Bot API

def call(method, params=None, files=None, timeout=70):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if files:
        b = uuid.uuid4().hex; body = b""
        for k, v in (params or {}).items():
            body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        for k, path in files.items():
            body += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{pathlib.Path(path).name}\"\r\n"
                     f"Content-Type: application/octet-stream\r\n\r\n").encode() + pathlib.Path(path).read_bytes() + b"\r\n"
        body += f"--{b}--\r\n".encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    else:
        req = urllib.request.Request(url, data=json.dumps(params or {}).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r: return json.load(r).get("result")
    except urllib.error.HTTPError as ex:
        raise RuntimeError(f"{method}: {ex.read()[:300].decode('utf-8', 'replace')}") from None


def send(text, buttons=None):
    if not CHAT: return
    p = {"chat_id": CHAT, "text": text[:4000], "parse_mode": "HTML", "disable_web_page_preview": True}
    if buttons: p["reply_markup"] = {"inline_keyboard": buttons}
    try: return call("sendMessage", p)
    except Exception as ex: log("send failed", ex)  # noqa: BLE001


def btn(label, kind, payload=None):
    k = uuid.uuid4().hex[:10]
    with LOCK:
        ACTIONS[k] = (kind, payload)
        if len(ACTIONS) > 500:
            for old in list(ACTIONS)[:200]: ACTIONS.pop(old, None)
    return {"text": label, "callback_data": k}


def esc(s):
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def send_media(paths, caption=""):
    """Slides as one album (max 10 photos)."""
    paths = [p for p in paths if pathlib.Path(p).exists()][:10]
    if not paths: return
    media = [{"type": "photo", "media": f"attach://f{i}", **({"caption": caption[:1000]} if i == 0 and caption else {})}
             for i in range(len(paths))]
    try: call("sendMediaGroup", {"chat_id": CHAT, "media": json.dumps(media)}, {f"f{i}": p for i, p in enumerate(paths)}, timeout=180)
    except Exception as ex: log("album failed", ex)  # noqa: BLE001


def send_video(path, caption=""):
    if not pathlib.Path(path).exists(): return
    if pathlib.Path(path).stat().st_size > 48 * 2**20: return send(f"(Video 50 MB'tan büyük, Telegram'a gönderilemedi: {esc(caption)})")
    try: call("sendVideo", {"chat_id": CHAT, "caption": caption[:1000], "supports_streaming": "true"}, {"video": path}, timeout=300)
    except Exception as ex: log("video failed", ex)  # noqa: BLE001


# ---------------------------------------------------------------- views

def latest_scan():
    return next((r for r in S.all_runs() if r["kind"] == "scan"), None)


def candidates(scan):
    if not scan or not scan.get("candidates_file"): return []
    return S.load_candidates(scan["candidates_file"], scan.get("id")).get("candidates", [])


def show_candidates(scan=None):
    scan = scan or latest_scan()
    cs = candidates(scan)
    if not cs: return send("Bu taramada henüz aday yok." if scan else "Henüz tarama yapılmadı. <b>tara</b> yaz.")
    chosen = {x["id"] for x in scan.get("chosen", [])}
    kinds = {"news": "📰", "prompts": "📋", "evergreen": "🌱"}
    lines, rows = [f"<b>{len(cs)} aday</b> · tarama {esc(scan['created'][11:16])}"], []
    for i, c in enumerate(cs, 1):
        lines.append(f"\n<b>{i}.</b> {kinds.get(c.get('kind'), '•')} {esc(c.get('title'))}{' ✓' if c['id'] in chosen else ''}"
                     f"\n<i>{esc(c.get('tool') or '')} · puan {esc(c.get('score'))}</i> — {esc(c.get('summary_tr'))}")
    for i in range(0, len(cs), 5):
        rows.append([btn(str(j + 1), "ask_select", (scan["id"], cs[j]["id"])) for j in range(i, min(i + 5, len(cs)))])
    send("\n".join(lines)[:4000], rows)
    send("Numara yaz ya da söyle (örn. <b>3</b>), ya da yukarıdaki düğmeye bas.")


def status():
    runs = S.all_runs(); out = []
    sc = latest_scan()
    if sc: out.append(f"🔎 Son tarama {esc(sc['created'][5:16].replace('T', ' '))}: {S_tr(sc['status'])}")
    for r in runs:
        if r["kind"] in ("post", "clip") and r["status"] in ("running", "queued", "waiting", "error"):
            node = next((n for n, v in r["nodes"].items() if v["status"] in ("running", "waiting", "error")), "")
            out.append(f"{'🎞' if r['kind'] == 'clip' else '🖼'} {esc((r.get('title') or r['id'])[:70])}\n   → {S_tr(r['status'])} · {esc(node)}")
    done = [r for r in runs if r["kind"] in ("post", "clip") and r["status"] == "done"][:2]
    for r in done: out.append(f"✅ {esc((r.get('title') or '')[:70])}")
    s = S.settings()
    out.append(f"⏰ Sonraki tarama: {S.next_slot(s['scan_times'], S.now()):%d.%m %H:%M} · onay {'açık' if s['approval'] else 'kapalı'}")
    send("\n".join(out) or "Her şey sakin.")


def S_tr(st):
    return {"queued": "sırada", "running": "çalışıyor", "waiting": "seni bekliyor", "done": "tamam", "error": "hata",
            "rejected": "reddedildi", "canceled": "durduruldu"}.get(st, st)


def preview(rid):
    d = S.run_detail(rid); c = d.get("content_data") or {}; q = d.get("qa_result") or {}
    head = f"⏸ <b>Onay bekliyor</b>\n{esc(d.get('title'))}"
    if q: head += f"\n\n{'✅' if q.get('ok') else '⚠️'} Kalite kontrol: {esc(q.get('summary_tr'))}"
    if d["kind"] == "clip":
        send(head + f"\n\n<b>Hook:</b> {esc((c.get('title') or '') + ' ' + (c.get('hook') or ''))}\n<b>Kaynak:</b> {esc(d.get('url'))}"
             "\n⚠️ Video başkasına ait; kaynak gösterilir ama bu izin sayılmaz.")
        if d.get("reel"): send_video(str(ROOT / d["reel"]), "Viral Reel önizleme")
    else:
        send(head)
        send_media([str(ROOT / s) for s in d.get("slides", [])], "Carousel")
        if d.get("reel"): send_video(str(ROOT / d["reel"]), "YouTube Short videosu")
    send(f"<b>Caption:</b>\n{esc(c.get('caption'))}",
         [[btn("✅ Yayınla", "ask_publish", rid), btn("✎ Revize", "ask_revise", rid), btn("✕ Reddet", "ask_reject", rid)]])


def waiting_run():
    return next((r for r in S.all_runs() if r["kind"] in ("post", "clip") and r["nodes"].get("approve", {}).get("status") == "waiting"), None)


# ---------------------------------------------------------------- events pushed by the Studio

def event(kind, run, **kw):
    """Called by studio.py; never raises."""
    if not (TOKEN and CHAT): return
    def work():
        try:
            if kind == "candidates": show_candidates(S.Run(run.id).s)
            elif kind == "approval": preview(run.id)
            elif kind == "published":
                links = "\n".join(f"• {esc(k)}: {esc(v)}" for k, v in kw.get("links", {}).items())
                send(f"🎉 <b>Paylaşıldı</b>\n{esc(run.s.get('title'))}\n{links}")
            elif kind == "error":
                send(f"❌ <b>Hata</b> · {esc(kw.get('label'))}\n{esc(run.s.get('title') or run.id)}\n<code>{esc(kw.get('msg'))[:600]}</code>",
                     [[btn("↻ Tekrar dene", "retry", (run.id, kw.get("node")))]])
            elif kind == "started": send(f"▶️ Başladı: {esc(run.s.get('title') or run.id)}")
        except Exception as ex: log("event failed", kind, ex)  # noqa: BLE001
    threading.Thread(target=work, daemon=True).start()


# ---------------------------------------------------------------- input

NUM_WORDS = {"bir": 1, "birinci": 1, "iki": 2, "ikinci": 2, "üç": 3, "üçüncü": 3, "dört": 4, "dördüncü": 4, "beş": 5,
             "beşinci": 5, "altı": 6, "altıncı": 6, "yedi": 7, "yedinci": 7, "sekiz": 8, "sekizinci": 8, "dokuz": 9,
             "dokuzuncu": 9, "on": 10, "onuncu": 10, "on bir": 11, "on birinci": 11, "on iki": 12, "on ikinci": 12,
             "on üç": 13, "on dört": 14}


def norm(t):
    return re.sub(r"\s+", " ", t.lower().replace("İ", "i").replace("I", "ı")).strip(" .!?,")


def number_in(t):
    m = re.search(r"\b(\d{1,2})\b", t)
    if m: return int(m.group(1))
    for w in sorted(NUM_WORDS, key=len, reverse=True):  # Turkish suffixes: "üçüncüyü", "ikiyi", "beşinciyi"
        if re.search(rf"\b{w}\b" if w == "on" else rf"\b{w}", t): return NUM_WORDS[w]
    return None


def handle_text(text, spoken=False):
    t = norm(text)
    url = re.search(r"https?://\S+", text)
    if url:
        try:
            rid = S.start_clip(url.group(0))
            return send(f"🎞 Viral Reel başladı. Video indiriliyor, hook yazılıyor; onaya gelince haber veririm.\n<code>{esc(rid)}</code>")
        except ValueError as ex: return send(f"⚠️ {esc(ex)}")
    if re.match(r"^/?(start|yardım|yardim|help|komutlar)\b", t): return help_msg()
    if re.match(r"^/?(şimdi )?tara\b|^tarama (yap|başlat)", t):
        rid = S.start_scan("Telegram'dan başlatıldı")
        return send("🔎 Tarama başladı (~5-8 dk). Adaylar hazır olunca listeyi gönderirim." if rid else "Zaten bir tarama çalışıyor.")
    if re.match(r"^/?(durum|ne durumda|status)", t): return status()
    if re.match(r"^/?(adaylar|aday listesi|liste)", t): return show_candidates()
    if re.match(r"^/?(önizle|önizleme|onizle|onay)\b", t):
        w = waiting_run(); return preview(w["id"]) if w else send("Onay bekleyen gönderi yok.")
    m = re.match(r"^/?revize( et)?[:,]?\s*(.*)$", t, re.S)
    if m:
        w = waiting_run()
        if not w: return send("Onay bekleyen gönderi yok.")
        note = text.split(":", 1)[1].strip() if ":" in text else re.sub(r"(?i)^\s*/?revize( et)?\s*", "", text).strip()
        if not note:
            with LOCK: PENDING_NOTE[CHAT] = w["id"]
            return send("Ne değişsin? Bir sonraki mesajın (yazı ya da ses) revizyon notu olacak.")
        return ask("revise", (w["id"], note), f"Revize edilsin mi?\n<i>{esc(note)}</i>")
    if re.match(r"^/?(yayınla|paylaş|onayla)\b", t):
        w = waiting_run()
        return ask("publish", w["id"], f"<b>Yayınlansın mı?</b>\n{esc(w.get('title'))}") if w else send("Onay bekleyen gönderi yok.")
    if re.match(r"^/?(reddet|iptal et)\b", t):
        w = waiting_run()
        return ask("reject", w["id"], f"Reddedilsin mi?\n{esc(w.get('title'))}") if w else send("Onay bekleyen gönderi yok.")
    # pick a candidate: "3", "3'ü seç", "üçüncüyü seç", "gemini'yi seç"
    sc = latest_scan(); cs = candidates(sc)
    short = len(t.split()) <= 4  # longer sentences ("bir sorum var, neden ...") are questions for Claude, not picks
    if cs and short and (re.search(r"\bseç", t) or re.fullmatch(r"\d{1,2}", t) or (spoken and number_in(t))):
        n = number_in(t)
        if n and 1 <= n <= len(cs): c = cs[n - 1]
        else:
            words = [w for w in re.findall(r"\w+", t) if len(w) > 3 and w not in ("seç", "seçelim", "haberi", "şunu")]
            scored = sorted(((sum(w[:5] in norm(x.get("title", "") + " " + (x.get("tool") or "")) for w in words), x) for x in cs),
                            key=lambda y: -y[0])
            c = scored[0][1] if scored and scored[0][0] else None
        if not c: return send("Hangi adayı seçeyim? Numarasını yaz (örn. <b>3</b>).")
        return ask("select", (sc["id"], c["id"]), f"Bu aday seçilsin mi?\n<b>{cs.index(c) + 1}.</b> {esc(c.get('title'))}")
    with LOCK: rid = PENDING_NOTE.pop(CHAT, None)
    if rid: return ask("revise", (rid, text.strip()), f"Revize edilsin mi?\n<i>{esc(text.strip())}</i>")
    ask_claude(text, spoken)


# ---------------------------------------------------------------- free-form: Claude

HISTORY = ROOT / "runs" / "telegram" / "history.json"
CLAUDE_BUSY = threading.Lock()


def state_summary():
    runs = S.all_runs(); s = S.settings(); sc = latest_scan()
    out = {"settings": {"scan_times": s["scan_times"], "approval": s["approval"]},
           "next_scan": f"{S.next_slot(s['scan_times'], S.now()):%Y-%m-%d %H:%M}"}
    if sc:
        out["latest_scan"] = {"id": sc["id"], "status": sc["status"], "created": sc["created"],
                              "chosen": [c["id"] for c in sc.get("chosen", [])],
                              "candidates": [{"n": i, "id": c["id"], "title": c.get("title"), "tool": c.get("tool"),
                                              "kind": c.get("kind"), "score": c.get("score")} for i, c in enumerate(candidates(sc), 1)]}
    out["runs"] = []
    for r in runs[:12]:
        if r["kind"] == "scan": continue
        cur = next(((n, v) for n, v in r["nodes"].items() if v["status"] in ("running", "waiting", "error")), (None, {}))
        out["runs"].append({"id": r["id"], "kind": r["kind"], "status": r["status"], "title": r.get("title"),
                            "created": r["created"], "content": r.get("content"), "step": cur[0], "step_msg": cur[1].get("msg")})
    return out


def history(add=None):
    h = S.read_json(HISTORY, []) or []
    if add:
        h = (h + add)[-16:]; HISTORY.parent.mkdir(parents=True, exist_ok=True)
        HISTORY.write_text(json.dumps(h, ensure_ascii=False), encoding="utf-8")
    return h


def ask_claude(text, spoken=False):
    if not CLAUDE_BUSY.acquire(blocking=False):
        return send("Bir önceki soruyu düşünüyorum, biter bitmez buna geçebilmen için birazdan tekrar yaz.")
    def work():
        try:
            send("🤔 Bakıyorum… (15-60 sn)")
            h = history()
            prompt = (ROOT / "prompts" / "chat.md").read_text(encoding="utf-8").format(
                now=f"{S.now():%Y-%m-%d %H:%M}", message=text, spoken="(voice message, transcribed: may contain small errors)" if spoken else "",
                history="\n".join(f"{m['who']}: {m['text']}" for m in h) or "(none)",
                state=json.dumps(state_summary(), ensure_ascii=False, indent=1))
            envv = dict(os.environ, PYTHONIOENCODING="utf-8"); envv.pop("CLAUDECODE", None)
            r = subprocess.run([S.CLAUDE, "-p", "--output-format", "json", "--allowedTools", "Read", "Glob", "Grep", "WebSearch", "WebFetch"],
                               input=prompt, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               env=envv, creationflags=NO_WINDOW, timeout=420)
            res = json.loads(r.stdout or "{}").get("result", "")
            m = re.search(r"\{.*\}", res, re.S)
            data = json.loads(m.group(0)) if m else {"reply": res or "Cevap alınamadı.", "actions": []}
            reply = data.get("reply") or ""
            send(reply or "Tamam.")
            for a in (data.get("actions") or [])[:5]: propose(a)
            history([{"who": "owner", "text": text}, {"who": "assistant", "text": reply}])
        except Exception as ex:  # noqa: BLE001
            log("claude chat failed", ex); send(f"⚠️ Claude'a soramadım: {esc(ex)}")
        finally:
            CLAUDE_BUSY.release()
    threading.Thread(target=work, daemon=True).start()


def propose(a):
    t = a.get("type"); label = a.get("label") or t
    if t == "scan": return ask("scan", None, f"👉 {esc(label)}")
    if t == "select" and a.get("scan") and a.get("candidate"): return ask("select", (a["scan"], a["candidate"]), f"👉 {esc(label)}")
    if t == "publish" and a.get("run"): return ask("publish", a["run"], f"👉 <b>{esc(label)}</b> (paylaşılır)")
    if t == "reject" and a.get("run"): return ask("reject", a["run"], f"👉 {esc(label)}")
    if t == "revise" and a.get("run") and a.get("note"): return ask("revise", (a["run"], a["note"]), f"👉 {esc(label)}\n<i>{esc(a['note'])}</i>")
    if t == "retry" and a.get("run") and a.get("node"): return ask("retry", (a["run"], a["node"]), f"👉 {esc(label)}")
    if t == "settings": return ask("settings", {k: a[k] for k in ("scan_times", "approval") if k in a}, f"👉 {esc(label)}")
    if t == "clip" and a.get("url"): return ask("clip", a["url"], f"👉 {esc(label)}")
    log("unknown action", a)


def apply_settings(p):
    s = S.settings()
    if "approval" in p: s["approval"] = bool(p["approval"])
    if "scan_times" in p:
        times = sorted({t for t in p["scan_times"] if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", str(t))})
        if not times: raise ValueError("geçerli saat yok (SS:DD)")
        s["scan_times"] = times; s["last_slot"] = (S.last_slot(times, S.now()) or S.now()).isoformat()
    S.save_settings(s)
    return f"Tarama saatleri {', '.join(s['scan_times'])} · onay {'açık' if s['approval'] else 'kapalı'}"


PENDING_NOTE = {}


def ask(kind, payload, text):
    send(text, [[btn("✅ Evet", kind, payload), btn("Hayır", "cancel")]])


def help_msg():
    send("<b>AI Playbooks Studio</b> · yazabilir ya da sesli mesaj atabilirsin\n\n"
         "• <b>tara</b> — şimdi tarama başlat\n• <b>adaylar</b> — son taramanın adayları\n"
         "• <b>3</b> / <b>3'ü seç</b> / <b>gemini'yi seç</b> — aday seç (onay sorulur)\n"
         "• <b>durum</b> — ne çalışıyor, ne bekliyor\n• <b>önizle</b> — onay bekleyen gönderiyi tekrar gönder\n"
         "• <b>yayınla</b> / <b>reddet</b> — onay sorulur\n• <b>revize: kapağı kısalt…</b> — revizyon notu\n"
         "• <b>bir X linki</b> (ya da X'ten bota paylaş) — viral Reel yap")


def on_callback(cq):
    call("answerCallbackQuery", {"callback_query_id": cq["id"]})
    with LOCK: act = ACTIONS.pop(cq.get("data"), None)
    if not act: return send("Bu düğmenin süresi doldu. Tekrar dene (örn. <b>durum</b>).")
    kind, p = act
    try:
        if kind == "cancel": return send("Tamam, vazgeçildi.")
        if kind == "ask_select":
            c = next((x for x in candidates(S.Run(p[0]).s) if x["id"] == p[1]), {})
            return ask("select", p, f"Bu aday seçilsin mi?\n<b>{esc(c.get('title'))}</b>")
        if kind == "select":
            rid = S.select(*p); return send(f"✍️ Üretim başladı: yazı → kapak → carousel → video → kalite kontrol. Onaya gelince önizlemeyi gönderirim.\n<code>{esc(rid)}</code>")
        if kind == "ask_publish": return ask("publish", p, "<b>Yayınlansın mı?</b> (Instagram + Facebook" + ("" if p.startswith("clip") else " + YouTube") + ")")
        if kind == "publish": S.approve(p); return send("🚀 Onaylandı, paylaşılıyor. Linkleri bitince gönderirim.")
        if kind == "ask_reject": return ask("reject", p, "Reddedilsin mi? Paylaşılmayacak.")
        if kind == "reject": S.reject(p); return send("✕ Reddedildi.")
        if kind == "ask_revise":
            with LOCK: PENDING_NOTE[CHAT] = p
            return send("Ne değişsin? Bir sonraki mesajın (yazı ya da ses) revizyon notu olacak.")
        if kind == "revise": S.revise(*p); return send("✎ Revizyon gönderildi, yeniden üretiliyor.")
        if kind == "retry": S.retry(*p); return send("↻ Tekrar deneniyor.")
        if kind == "scan":
            return send("🔎 Tarama başladı." if S.start_scan("Telegram'dan başlatıldı") else "Zaten bir tarama çalışıyor.")
        if kind == "settings": return send("⚙️ " + esc(apply_settings(p)))
        if kind == "clip": rid = S.start_clip(p); return send(f"🎞 Viral Reel başladı.\n<code>{esc(rid)}</code>")
    except ValueError as ex:
        send(f"⚠️ {esc(ex)}")


def transcribe(file_id):
    info = call("getFile", {"file_id": file_id})
    d = ROOT / "runs" / "telegram"; d.mkdir(parents=True, exist_ok=True)
    f = d / f"{int(time.time())}_{pathlib.Path(info['file_path']).name}"
    urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{TOKEN}/{info['file_path']}", f)
    envv = dict(os.environ, PYTHONIOENCODING="utf-8", HF_HOME=str(ROOT / ".cache" / "hf"))
    r = subprocess.run([STT_PY, str(ROOT / "stt.py"), str(f)], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=envv, creationflags=NO_WINDOW, timeout=300)
    f.unlink(missing_ok=True)
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    return lines[-1].strip() if lines else ""


def on_message(m):
    global CHAT
    chat = m["chat"]["id"]
    if not CHAT:
        if (m.get("text") or "").startswith("/start"):
            CHAT = chat; save_chat(chat)
            send("🔒 Bu sohbet artık Studio'nun tek yetkili sohbeti.")
            help_msg()
        return
    if chat != CHAT: return log("ignored chat", chat)
    if m.get("voice") or m.get("audio"):
        send("🎙 Dinliyorum…")
        t = transcribe((m.get("voice") or m.get("audio"))["file_id"])
        if not t: return send("Sesi anlayamadım, tekrar dener misin?")
        send(f"🗣 <i>{esc(t)}</i>")
        return handle_text(t, spoken=True)
    text = m.get("text") or m.get("caption") or ""
    for e in m.get("entities") or m.get("caption_entities") or []:  # shared links
        if e.get("type") == "text_link": text += " " + e["url"]
    if text: handle_text(text)


def save_chat(chat):
    f = ROOT / ".env"; lines = f.read_text(encoding="utf-8").splitlines()
    lines = [l for l in lines if not l.startswith("TELEGRAM_CHAT_ID=")] + [f"TELEGRAM_CHAT_ID={chat}"]
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log("chat locked", chat)


def loop():
    offset = None
    try:
        call("setMyCommands", {"commands": [{"command": c, "description": d} for c, d in (
            ("durum", "Ne çalışıyor, ne bekliyor"), ("adaylar", "Son taramanın adayları"), ("tara", "Şimdi tara"),
            ("onizle", "Onay bekleyen gönderi"), ("yardim", "Komutlar"))]})
    except Exception as ex: log("setMyCommands", ex)  # noqa: BLE001
    while True:
        try:
            ups = call("getUpdates", {"timeout": 50, **({"offset": offset} if offset else {}),
                                      "allowed_updates": ["message", "callback_query"]}, timeout=70) or []
            for u in ups:
                offset = u["update_id"] + 1
                try:
                    if "callback_query" in u:
                        if u["callback_query"]["message"]["chat"]["id"] == CHAT: on_callback(u["callback_query"])
                    elif "message" in u: on_message(u["message"])
                except Exception as ex: log("update failed", ex); send(f"⚠️ Hata: {esc(ex)}")  # noqa: BLE001
        except Exception as ex:  # noqa: BLE001 - network hiccup: wait and poll again
            log("poll", ex); time.sleep(random.uniform(5, 15))


def start(studio):
    global S, TOKEN, CHAT
    S = studio; e = env()
    TOKEN = e.get("TELEGRAM_BOT_TOKEN")
    CHAT = int(e["TELEGRAM_CHAT_ID"]) if e.get("TELEGRAM_CHAT_ID", "").lstrip("-").isdigit() else None
    if not TOKEN: return log("no TELEGRAM_BOT_TOKEN: bot off")
    threading.Thread(target=loop, daemon=True).start()
    log("bot running", "locked" if CHAT else "waiting for /start")
