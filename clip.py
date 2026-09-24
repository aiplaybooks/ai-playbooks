"""Frame a video clip as a hook Reel (1080x1920): black background, brand line + big hook text on top, the clip below.

Usage:
    python clip.py <video file or post URL> --hook "Someone recreated the iPhone Duo's folding animation on a MacBook"
                   [--title "Higgsfield Seedance 2.5 Prompt:"] [--credit "@creator on X"] [--name my-clip]

A URL (X / Reddit / ...) is fetched with yt-dlp: only for a single post the owner picked (see CLAUDE.md, viral Reels).
`--title` is an optional bold first line above the hook. `--credit` adds a small "Source: @creator on X" line under the clip.
    python clip.py content/clips/<name>.json      (Studio: hook/title/credit/source from the JSON; the clip is
                                                  output/clips/<name>/source.mp4 if already fetched)
Output: output/clips/<name>/reel.mp4 (+ header.png, cover.jpg = first frame, meta.json)
Keeps the clip's own audio (loudness-normalised); max 90 s. Needs ffmpeg + ffprobe on PATH.
"""
import sys, json, re, html, shutil, pathlib, argparse, subprocess
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
FONTS = ROOT / "fonts"
W, H = 1080, 1920
TOP = 250            # below the IG top safe zone (~190 px)
BOTTOM_SAFE = 330    # IG caption/buttons area
MAX_SECS = 90
VIDEO = (".mp4", ".webm", ".mkv", ".mov")
e = html.escape

HEADER = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Inter;src:url(%(inter)s);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent;width:1080px}
.h{padding:0 64px;color:#fff;font-family:Inter,sans-serif}
.brand{display:flex;align-items:center;gap:14px;font-size:38px;font-weight:800;letter-spacing:-.5px}
.logo{width:48px;height:48px;border-radius:13px;background:linear-gradient(135deg,#C06BFF,#4F9BFF);display:grid;place-items:center;font-size:26px;font-weight:900}
.handle{font-size:27px;font-weight:500;color:#8E8E96;margin-left:4px}
.title{margin-top:34px;font-size:%(ts)spx;font-weight:800;line-height:1.18;letter-spacing:-.6px}
.hook{margin-top:%(hm)spx;font-size:%(hs)spx;font-weight:%(hw)s;line-height:1.2;letter-spacing:-.8px;text-wrap:pretty}
</style></head><body><div class="h" id="h">
<div class="brand"><div class="logo">A</div>AI Playbooks<span class="handle">@aiplaybooks.daily</span></div>
%(title)s<div class="hook">%(hook)s</div></div></body></html>"""


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe(f):
    d = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(f)]).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    rot = int((v.get("tags") or {}).get("rotate", 0) or 0)
    for sd in v.get("side_data_list") or []:
        if "rotation" in sd: rot = int(sd["rotation"])
    w, h = int(v["width"]), int(v["height"])
    if abs(rot) in (90, 270): w, h = h, w
    return w, h, float(d["format"]["duration"]), any(s["codec_type"] == "audio" for s in d["streams"])


def fetch(url, out):
    run([sys.executable, "-m", "yt_dlp", "-q", "--no-playlist", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
         "-o", str(out / "source.%(ext)s"), url])
    return next(f for f in out.glob("source.*") if f.suffix in VIDEO)


def header(out, hook, title):
    n = len(hook)
    hs = 66 if n <= 60 else 58 if n <= 100 else 50
    ctx = {"inter": (FONTS / "InterVariable.ttf").as_uri(), "hook": e(hook), "hs": hs, "hw": 500 if title else 500,
           "hm": 22 if title else 34, "ts": 56, "title": f'<div class="title">{e(title)}</div>' if title else ""}
    f = out / "header.html"; f.write_text(HEADER % ctx, encoding="utf-8")
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": 900})
        pg.goto(f.as_uri()); pg.wait_for_timeout(200)
        box = pg.locator("#h").bounding_box()
        pg.locator("#h").screenshot(path=str(out / "header.png"), omit_background=True)
        br.close()
    return int(box["height"])


def badge(out, text):
    f = out / "credit.html"
    f.write_text(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Inter;src:url({(FONTS / "InterVariable.ttf").as_uri()});font-weight:100 900}}
*{{margin:0}}html,body{{background:transparent}}#c{{display:inline-block;font:500 28px Inter,sans-serif;color:#9A9AA4}}</style></head>
<body><span id="c">Source: {e(text)}</span></body></html>''', encoding="utf-8")
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": 200})
        pg.goto(f.as_uri()); pg.wait_for_timeout(150)
        pg.locator("#c").screenshot(path=str(out / "credit.png"), omit_background=True); br.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--hook"); ap.add_argument("--title")
    ap.add_argument("--credit"); ap.add_argument("--name")
    a = ap.parse_args()
    if a.src.endswith(".json"):
        d = json.loads(pathlib.Path(a.src).read_text(encoding="utf-8"))
        a.name = pathlib.Path(a.src).stem; a.hook = d["hook"]; a.title = d.get("title"); a.credit = d.get("credit")
        got = [f for f in sorted((ROOT / "output" / "clips" / a.name).glob("source.*")) if f.suffix in VIDEO]
        a.src = str(got[0]) if got else d["source"]
    if not a.hook: ap.error("--hook is required")
    name = a.name or re.sub(r"[^a-z0-9]+", "-", a.hook.lower()).strip("-")[:50]
    out = ROOT / "output" / "clips" / name; out.mkdir(parents=True, exist_ok=True)
    src = fetch(a.src, out) if re.match(r"https?://", a.src) else pathlib.Path(a.src)
    vw, vh, dur, audio = probe(src)
    dur = min(dur, MAX_SECS)

    hh = header(out, a.hook, a.title)
    y = TOP + hh + 40                                   # clip starts under the header
    room = H - BOTTOM_SAFE - y - (60 if a.credit else 0)
    sw = W; sh = round(vh * W / vw / 2) * 2              # full width ...
    crop = ""
    if sh > room:                                        # ... tall clip: grow it so a center crop of <= 25% fills the room
        sw = min(W, round(room / 0.75 * vw / vh / 2) * 2); sh = round(vh * sw / vw / 2) * 2
        if sh > room: crop = f",crop={sw}:{room // 2 * 2}"; sh = room // 2 * 2
    sx = (W - sw) // 2
    if sh < room: y += (room - sh) // 3                  # short (landscape) clips sit a bit lower, not glued to the text

    inputs = ["-loop", "1", "-i", str(out / "header.png")]
    credit = ""
    if a.credit:
        badge(out, a.credit); inputs += ["-loop", "1", "-i", str(out / "credit.png")]
        credit = f"[c];[c][2:v]overlay=64:{y + sh + 22}:format=auto"
    fc = (f"color=c=black:s={W}x{H}:d={dur:.3f}:r=30[bg];[0:v]scale={sw}:-2:flags=lanczos{crop},setsar=1,fps=30[v];"
          f"[bg][v]overlay={sx}:{y}[b];[b][1:v]overlay=0:{TOP}:format=auto{credit},format=yuv420p[out]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), *inputs,
           "-filter_complex", fc, "-map", "[out]"]
    if audio: cmd += ["-map", "0:a:0", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high",
            "-movflags", "+faststart", str(out / "reel.mp4")]
    run(cmd)
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.5", "-i", str(out / "reel.mp4"), "-frames:v", "1", "-q:v", "2", str(out / "cover.jpg")])
    (out / "meta.json").write_text(json.dumps({"src": a.src, "hook": a.hook, "title": a.title, "credit": a.credit,
                                               "secs": round(dur, 2), "clip": [vw, vh]}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", out / "reel.mp4")


if __name__ == "__main__":
    main()
