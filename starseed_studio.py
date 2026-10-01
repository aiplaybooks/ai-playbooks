"""Starseed Transmission workspace of the Studio (owner, 2026-09-30: a second portfolio next to AI Playbooks, shown
on its own page /starseed, never mixed with AI Playbooks).

The Starseed engine and its data live outside this repo, in E:\\masaüstü AI\\STARSEED (pipeline/ = engine + .env,
ORTAK/ = folder shared with the owner). This module only reads that state for the UI and saves UI settings
(voice per race) into pipeline/config.json.
"""
import json, time, socket, pathlib, threading, datetime as dt

BASE = pathlib.Path(r"E:\masaüstü AI\STARSEED")
PIPE = BASE / "pipeline"
ORTAK = BASE / "ORTAK"
VOICES_DIR = BASE / "Kokoro Ses Ornekleri"
CONFIG = PIPE / "config.json"
FILE_PREFIXES = ("ORTAK/", "Kokoro Ses Ornekleri/")  # what /starseed/file/ may serve
VIDEO = {".mp4", ".mov", ".m4v"}
IMAGE = {".jpg", ".jpeg", ".png", ".webp"}
OUR_FILES = {"voice", "voice_tts", "preview"}  # stems of files we write into a project folder (never "the final render")


def final_files(d):
    """The owner's final render + thumbnail in a project folder (owner, 2026-09-30: both go into the project's folder)."""
    vids = [f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in VIDEO and f.stem.lower() not in OUR_FILES]  # CapCut exports into its own sub-folder
    thumbs = [f for f in d.iterdir() if f.is_file() and f.suffix.lower() in IMAGE and "clip" not in f.stem.lower()]
    newest = lambda fs: max(fs, key=lambda f: f.stat().st_mtime) if fs else None
    return newest(vids), newest(thumbs)

RACES = [  # the Six Rays (look/tone locked in fb-comment-automation/src/personas/characters.json)
    {"key": "arcturian", "name": "Arcturian", "theme": "DNA, kadim kod, plan", "archetype": "Your DNA remembers", "color": "#7b8cff"},
    {"key": "lyran", "name": "Lyran", "theme": "Savaşçı cesaret", "archetype": "The warrior within you woke up", "color": "#f2a93b"},
    {"key": "pleiadian", "name": "Pleiadian", "theme": "Kalp, bütünlük", "archetype": "You are already enough", "color": "#3fd0c9"},
    {"key": "sirian", "name": "Sirian", "theme": "Su, frekans", "archetype": "Return to your frequency", "color": "#3a8dde"},
    {"key": "andromedan", "name": "Andromedan", "theme": "Özgürlük", "archetype": "Take back your freedom", "color": "#b69cff"},
    {"key": "lemurian", "name": "Lemurian", "theme": "Toprak, atalar", "archetype": "The earth remembers you", "color": "#8fb35e"},
]
POOL_BASE = pathlib.Path(r"D:\masaustuAI2\STARSEED VIDEO HAVUZ")  # owner, 2026-09-30: one folder per race
DEFAULT_POOLS = {k: str(POOL_BASE / d) for k, d in {"arcturian": "Arcturian", "lyran": "Lyran", "pleiadian": "Pleiadian",
                                                     "sirian": "Sirian", "andromedan": "andromedan", "lemurian": "Lemurian"}.items()}
STAGES = [("topic", "Konu"), ("script", "Senaryo"), ("voice", "Ses"), ("capcut", "CapCut · sende"),
          ("approve", "Onay"), ("published", "Yayında")]
_cache = {"t": 0, "pools": {}}
_lock = threading.Lock()


def read_json(p, default=None):
    try: return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError): return default


def config():
    c = read_json(CONFIG, {}) or {}
    c.setdefault("pools", {}); c.setdefault("voices", {})
    c["pools"] = {**DEFAULT_POOLS, **c.get("pools_override", {})}
    return c


def save_config(c):
    PIPE.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(c, indent=1, ensure_ascii=False), encoding="utf-8")


def pool_counts(c):
    with _lock:
        if time.time() - _cache["t"] > 120:
            out = {}
            for k, d in c["pools"].items():
                p = pathlib.Path(d)
                out[k] = sum(1 for f in p.iterdir() if f.suffix.lower() in VIDEO) if p.is_dir() else 0
            _cache.update(t=time.time(), pools=out)
        return dict(_cache["pools"])


def book_race(name):
    n = name.lower()
    return next((r["key"] for r in RACES if r["key"] in n), "starseed")


def projects():
    """ORTAK/1_PROJELER/<date_topic>/status.json -> {title, race, stage, created, book, words, minutes}."""
    out = []
    for d in sorted((ORTAK / "1_PROJELER").glob("*/")):  # folder names start with the slot: next video first
        s = read_json(d / "status.json", {}) or {}
        vid, thumb = final_files(d)
        stage = s.get("stage", "topic"); pub = read_json(d / "publish.json")
        if vid and stage == "capcut": stage = "approve"  # the owner's render arrived: approval next
        out.append({"video": vid.name if vid else None, "thumb": thumb.name if thumb else None, "slot": s.get("slot"),
                    "emissary": s.get("emissary"), "voice": s.get("voice"), "id": d.name, "title": s.get("title") or d.name, "race": s.get("race"), "stage": stage,
                    "created": s.get("created"), "book": s.get("book"), "minutes": s.get("minutes"), "note": s.get("note"),
                    "words": s.get("words"), "capcut": s.get("capcut"), "error": s.get("error"), "music": s.get("music"),
                    "publish": {k: pub.get(k) for k in ("asked", "approved", "uploaded", "fb_link", "yt_link", "fb_scheduled", "yt_scheduled", "errors")} if pub else None})
    return out


def published():
    """ORTAK/3_YAYINLANDI/<project>/ (moved there by the bot after the slot): title, slot, links."""
    out = []
    for d in sorted((ORTAK / "3_YAYINLANDI").glob("*/"), reverse=True):
        s = read_json(d / "status.json", {}) or {}; l = read_json(d / "links.json", {}) or {}
        out.append({"id": d.name, "title": s.get("title") or d.name, "race": s.get("race"), "slot": s.get("slot"), "minutes": s.get("minutes"),
                    "fb": l.get("fb_link"), "yt": l.get("yt_link")})
    return out


def topics_today():
    """Today's topic file of the engine (pipeline/topics/<date>.json): status, the 2 picks, the other candidates."""
    d = read_json(PIPE / "topics" / f"{dt.date.today()}.json")
    if not d: return None
    keys = ("id", "race", "family", "title", "summary_tr", "book", "comment_word", "thumbnail_text", "why_now", "score", "slot")
    picks = [{k: c.get(k) for k in keys} for c in d.get("picks", [])]; ids = {c["id"] for c in picks}
    others = sorted((c for c in d.get("candidates", []) if c.get("id") not in ids), key=lambda c: -(c.get("score_final", c.get("score", 0)) or 0))
    return {"date": d.get("date"), "status": d.get("status"), "production": d.get("production"), "picks": picks,
            "others": [{k: c.get(k) for k in keys} for c in others]}


def archive():
    """The YouTube archive queues of pipeline/shorts.py: the owner's finished reels and older long videos."""
    out = {}; now = dt.datetime.now().astimezone().isoformat()
    for name, label in (("shorts", "Shorts · Transmission Starseed"), ("backlog", "Uzun arşiv · Starseed Transmission")):
        q = read_json(PIPE / "runs" / f"{name}_queue.json", []) or []
        out[name] = {"label": label, "total": len(q), "uploaded": sum(1 for i in q if i.get("video")),
                     "out": sum(1 for i in q if i.get("video") and i["slot"] <= now), "last": q[-1]["slot"][:10] if q else None,
                     "items": [{k: i.get(k) for k in ("slot", "race", "title", "link", "error")} for i in q]}
    return out


def bot_running():
    s = socket.socket()
    try: s.bind(("127.0.0.1", 8797)); return False  # pipeline/bot.py holds this port while it runs
    except OSError: return True
    finally: s.close()


def files_in(sub):
    d = ORTAK / sub
    return [{"name": f.name, "size": f.stat().st_size, "time": f.stat().st_mtime}
            for f in sorted(d.iterdir(), key=lambda f: -f.stat().st_mtime) if f.is_file() and f.suffix.lower() in VIDEO] if d.is_dir() else []


def state():
    c = config(); counts = pool_counts(c)
    books = read_json(PIPE / "gumroad_products.json", []) or []
    for b in books: b["race"] = book_race(b["name"]); b.pop("desc", None)
    samples = sorted(f.name for f in VOICES_DIR.glob("*.wav")) if VOICES_DIR.is_dir() else []
    env = (PIPE / ".env").read_text(encoding="utf-8") if (PIPE / ".env").exists() else ""
    return {
        "races": [{**r, "clips": counts.get(r["key"], 0), "pool": c["pools"].get(r["key"]), "voices": voices_of(c, r["key"])} for r in RACES],
        "stages": [{"id": i, "label": l} for i, l in STAGES],
        "projects": projects(), "published": published(), "topics": topics_today(), "archive": archive(),
        "schedule": c.get("schedule", {}),
        "books": books, "samples": samples,
        "checks": {"gumroad": "GUMROAD_ACCESS_TOKEN" in env, "kokoro": bool(samples),
                   "capcut": pathlib.Path(r"E:\masaüstü AI\tools\capcut-cli\dist\index.js").exists(),
                   "facebook": "FB_PAGE_TOKEN" in env, "shared": ORTAK.is_dir(), "youtube": "YT_REFRESH_TOKEN" in env,
                   "shorts": (PIPE / ".env.shorts").exists(), "bot": bot_running()},
    }


def summary():
    """Small numbers for the portfolio home page."""
    s = state()
    return {"projects": len([p for p in s["projects"] if p["stage"] not in ("approve", "published")]),
            "finished": len([p for p in s["projects"] if p["stage"] == "approve"]), "published": len(s["published"]),
            "books": len([b for b in s["books"] if b.get("published")]), "sales": sum(b.get("sales") or 0 for b in s["books"]),
            "races_ready": sum(1 for r in s["races"] if r["clips"])}


def voices_of(c, race):
    v = c["voices"].get(race) or []
    return [v] if isinstance(v, str) else list(v)


def set_voice(race, voice, on=True):
    """Add (on) or remove a Kokoro voice from the race's list; each video picks one of them at random (owner, 2026-09-30)."""
    if race not in {r["key"] for r in RACES}: raise ValueError("bilinmeyen ırk")
    c = config(); vs = voices_of(c, race)
    if on and voice not in vs: vs.append(voice)
    if not on and voice in vs: vs.remove(voice)
    c["voices"][race] = vs; c.pop("pools", None)
    save_config(c)


def file_path(rel):
    """A file under the STARSEED folder the UI may show (videos, voice samples); None when not allowed."""
    if not rel.startswith(FILE_PREFIXES): return None
    f = (BASE / rel).resolve()
    return f if BASE.resolve() in f.parents and f.is_file() else None
