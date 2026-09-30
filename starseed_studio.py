"""Starseed Transmission workspace of the Studio (owner, 2026-09-30: a second portfolio next to AI Playbooks, shown
on its own page /starseed, never mixed with AI Playbooks).

The Starseed engine and its data live outside this repo, in E:\\masaüstü AI\\STARSEED (pipeline/ = engine + .env,
ORTAK/ = folder shared with the owner). This module only reads that state for the UI and saves UI settings
(voice per race) into pipeline/config.json.
"""
import json, time, pathlib, threading

BASE = pathlib.Path(r"E:\masaüstü AI\STARSEED")
PIPE = BASE / "pipeline"
ORTAK = BASE / "ORTAK"
VOICES_DIR = BASE / "Kokoro Ses Ornekleri"
CONFIG = PIPE / "config.json"
FILE_PREFIXES = ("ORTAK/", "Kokoro Ses Ornekleri/")  # what /starseed/file/ may serve
VIDEO = {".mp4", ".mov", ".m4v"}

RACES = [  # the Six Rays (look/tone locked in fb-comment-automation/src/personas/characters.json)
    {"key": "arcturian", "name": "Arcturian", "theme": "DNA, kadim kod, plan", "archetype": "Your DNA remembers", "color": "#7b8cff"},
    {"key": "lyran", "name": "Lyran", "theme": "Savaşçı cesaret", "archetype": "The warrior within you woke up", "color": "#f2a93b"},
    {"key": "pleiadian", "name": "Pleiadian", "theme": "Kalp, bütünlük", "archetype": "You are already enough", "color": "#3fd0c9"},
    {"key": "sirian", "name": "Sirian", "theme": "Su, frekans", "archetype": "Return to your frequency", "color": "#3a8dde"},
    {"key": "andromedan", "name": "Andromedan", "theme": "Özgürlük", "archetype": "Take back your freedom", "color": "#b69cff"},
    {"key": "lemurian", "name": "Lemurian", "theme": "Toprak, atalar", "archetype": "The earth remembers you", "color": "#8fb35e"},
]
DEFAULT_POOLS = {"arcturian": r"D:\masaustuAI2\ARCTURIAN\videos", "lemurian": r"D:\masaustuAI2\Lemurian\video"}
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
    for k, v in DEFAULT_POOLS.items(): c["pools"].setdefault(k, v)
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
    for d in sorted((ORTAK / "1_PROJELER").glob("*/"), reverse=True):
        s = read_json(d / "status.json", {}) or {}
        out.append({"id": d.name, "title": s.get("title") or d.name, "race": s.get("race"), "stage": s.get("stage", "topic"),
                    "created": s.get("created"), "book": s.get("book"), "minutes": s.get("minutes"), "note": s.get("note")})
    return out


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
        "races": [{**r, "clips": counts.get(r["key"], 0), "pool": c["pools"].get(r["key"]), "voice": c["voices"].get(r["key"])} for r in RACES],
        "stages": [{"id": i, "label": l} for i, l in STAGES],
        "projects": projects(), "finished": files_in("2_BITEN_VIDEOLAR"), "published": files_in("3_YAYINLANDI"),
        "books": books, "samples": samples,
        "checks": {"gumroad": "GUMROAD_ACCESS_TOKEN" in env, "kokoro": bool(samples),
                   "capcut": pathlib.Path(r"E:\masaüstü AI\tools\capcut-cli\dist\index.js").exists(),
                   "facebook": "FB_PAGE_TOKEN" in env, "shared": ORTAK.is_dir()},
    }


def summary():
    """Small numbers for the portfolio home page."""
    s = state()
    return {"projects": len(s["projects"]), "finished": len(s["finished"]), "published": len(s["published"]),
            "books": len([b for b in s["books"] if b.get("published")]), "sales": sum(b.get("sales") or 0 for b in s["books"]),
            "races_ready": sum(1 for r in s["races"] if r["clips"])}


def set_voice(race, voice):
    if race not in {r["key"] for r in RACES}: raise ValueError("bilinmeyen ırk")
    c = config()
    if voice: c["voices"][race] = voice
    else: c["voices"].pop(race, None)
    save_config(c)


def file_path(rel):
    """A file under the STARSEED folder the UI may show (videos, voice samples); None when not allowed."""
    if not rel.startswith(FILE_PREFIXES): return None
    f = (BASE / rel).resolve()
    return f if BASE.resolve() in f.parents and f.is_file() else None
