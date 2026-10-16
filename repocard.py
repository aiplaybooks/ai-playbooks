"""The single image of a GitHub repo post: the repo's real GitHub page (dark mode), nothing written on it.

Usage:
    python repocard.py content/repos/<post>.json      -> output/repos/<post>/slide_01.png (1080x1350)

Owner, 2026-09-28: the post is ONE photo, the plain GitHub screenshot (repo header, a few files, About box with the
star count, start of the README). All text (hook, benefits, CTA) lives in the captions and the platform's comment.
Before rendering, the star count is re-read from the GitHub API: text that claims more stars than the repo has
(captions, first comment) fails the render (counts are always rounded down).
"""
import sys, re, json, pathlib, subprocess, urllib.request
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
W, H = 1080, 1350
VW = 1120  # page width in CSS px: still GitHub's layout with the About sidebar, text close to 1:1 in the post
HIDE = """.js-cookie-consent-banner, #cookie-consent-banner, cookie-consent-link, [data-testid="cookie-consent"],
.signup-prompt, .signup-prompt-bg, .flash-full, .js-notice, .Popover, .AppHeader, header.header-logged-out,
[data-target="react-app.reactRoot"] .Banner { display: none !important; }
table[aria-labelledby="folders-and-files"] tbody tr:nth-child(n+8):not(:last-child) { display: none !important; }"""
# ^ long file lists are cut to ~6 rows so the README start (usually the demo image) makes it into the frame
# GitHub's repo page header: the old layout had #repository-container-header; the 2026-10 redesign moved the owner/repo
# line + tabs into a <header> inside #js-repo-pjax-container (#repo-title-component = the repo name row, proof it's a repo)
REPO_READY = "#repository-container-header, #repo-title-component"
HEADER_TOP = """(() => { const h = document.querySelector('#repository-container-header')
  || document.querySelector('#js-repo-pjax-container header') || document.querySelector('#js-repo-pjax-container');
  return h.getBoundingClientRect().top + scrollY; })()"""


def api_repo(full):
    req = urllib.request.Request(f"https://api.github.com/repos/{full}", headers={"User-Agent": "aiplaybooks-repocard"})
    try:
        tok = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=20).stdout.strip()
        if tok: req.add_header("Authorization", f"Bearer {tok}")
    except (OSError, subprocess.TimeoutExpired):
        pass
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())


def post_text(data):
    caps = data.get("captions") or {}
    return " ".join(str(x) for x in (data.get("caption"), caps.get("instagram"), caps.get("facebook"), data.get("fb_comment")) if x)


def check_stars(text, stars):
    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*([kK])?\+?\s*(?:GitHub\s+)?stars", text):
        n = float(m.group(1).replace(",", ".") if m.group(2) else m.group(1).replace(",", "")) * (1000 if m.group(2) else 1)
        if n > stars: sys.exit(f"ERROR: the post says {m.group(0)!r} but the repo has {stars:,} stars (round DOWN)")


def screenshot(url, out):
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": VW, "height": 1500}, device_scale_factor=2, color_scheme="dark",
                         locale="en-US", timezone_id="UTC")
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        try: pg.wait_for_selector(REPO_READY, timeout=20000)
        except Exception: sys.exit("ERROR: the GitHub page did not show a repository (login wall, 404 or GitHub throttling?)")
        pg.wait_for_timeout(2500)
        pg.add_style_tag(content=HIDE)
        top = pg.evaluate(HEADER_TOP)
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(out), clip={"x": 0, "y": max(0, top - 4), "width": VW, "height": VW * H / W}, full_page=True)
        br.close()


def render(content):
    content = pathlib.Path(content)
    data = json.loads(content.read_text(encoding="utf-8"))
    if data.get("reject"): sys.exit(f"ERROR: the writer rejected this repo: {data['reject']}")
    repo = data.get("repo") or {}
    if not repo.get("full_name"): sys.exit("ERROR: `repo.full_name` is required")
    info = api_repo(repo["full_name"])
    if info.get("archived"): sys.exit("ERROR: the repo is archived")
    check_stars(post_text(data), info["stargazers_count"])
    if repo.get("stars") != info["stargazers_count"]:
        repo["stars"] = info["stargazers_count"]; data["repo"] = repo
        content.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out = ROOT / "output" / "repos" / content.stem; out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"): f.unlink()
    shot = out / "shot.png"
    screenshot(info["html_url"], shot)
    Image.open(shot).convert("RGB").resize((W, H), Image.LANCZOS).save(out / "slide_01.png")
    shot.unlink()
    print(f"card: {info['full_name']} · {info['stargazers_count']:,} stars -> {(out / 'slide_01.png').relative_to(ROOT).as_posix()}")


REEL_SECS = 14
HOLD = 2.0  # seconds on the top of the page before the scroll starts
MAX_TRAVEL = 1100  # px (at 1000 px width): header, files, the README hero; deeper parts are rarely pretty
# The Reel header (brand line + hook) used to come from clip.header(); clips dropped their frame on 2026-10-06 and
# clip.py lost it, which broke every repo Reel ("module 'clip' has no attribute 'header'"). It lives here now.
RW, RH = 1080, 1920
TOP = 250            # below the IG top safe zone (~190 px)
BOTTOM_SAFE = 330    # IG caption/buttons area
REEL_HEADER = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Inter;src:url(%(inter)s);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent;width:1080px}
.h{padding:0 64px;color:#fff;font-family:Inter,sans-serif}
.brand{display:flex;align-items:center;gap:14px;font-size:38px;font-weight:800;letter-spacing:-.5px}
.logo{width:48px;height:48px;border-radius:13px;background:linear-gradient(135deg,#C06BFF,#4F9BFF);display:grid;place-items:center;font-size:26px;font-weight:900}
.handle{font-size:27px;font-weight:500;color:#8E8E96;margin-left:4px}
.hook{margin-top:34px;font-size:%(hs)spx;font-weight:500;line-height:1.2;letter-spacing:-.8px;text-wrap:pretty}
</style></head><body><div class="h" id="h">
<div class="brand"><div class="logo">A</div>AI Playbooks<span class="handle">@aiplaybooks.daily</span></div>
<div class="hook">%(hook)s</div></div></body></html>"""


def reel_header(out, hook):
    """Brand line + hook as a transparent PNG (out/header.png); returns its height in px."""
    import html
    n = len(hook); hs = 66 if n <= 60 else 58 if n <= 100 else 50
    f = out / "header.html"
    f.write_text(REEL_HEADER % {"inter": (ROOT / "fonts" / "InterVariable.ttf").as_uri(), "hook": html.escape(hook), "hs": hs}, encoding="utf-8")
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": RW, "height": 900})
        pg.goto(f.as_uri()); pg.wait_for_timeout(200)
        box = pg.locator("#h").bounding_box()
        pg.locator("#h").screenshot(path=str(out / "header.png"), omit_background=True)
        br.close()
    return int(box["height"])


def reel(content):
    """Repo Reel (strategy backlog 2026-09-29: Reels are the only format that reaches non-followers): the clip-style
    header (brand + the post's first hook line) on black, below it the repo page scrolling top -> README inside a
    window, procedural music. -> output/repos/<post>/reel.mp4 (1080x1920, 30 fps, H.264 + AAC)."""
    content = pathlib.Path(content)
    data = json.loads(content.read_text(encoding="utf-8"))
    repo = data.get("repo") or {}; hook = data.get("hook") or [data.get("topic") or repo.get("full_name", "")]
    hook = hook[0] if isinstance(hook, list) else str(hook)
    out = ROOT / "output" / "repos" / content.stem; out.mkdir(parents=True, exist_ok=True)
    hh = reel_header(out, hook)
    top = TOP + hh + 36; win_h = RH - BOTTOM_SAFE - 30 - top; win_w = 1000
    if win_h < 700: sys.exit(f"ERROR: the hook is too long for the Reel header ({hh}px): shorten hook[0]")
    tall = out / "tall.png"
    with sync_playwright() as p:  # the page from the repo header down ~3 screens (file list cut, README start)
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": VW, "height": 1500}, device_scale_factor=2, color_scheme="dark", locale="en-US")
        pg.goto(repo.get("url") or f"https://github.com/{repo['full_name']}", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_selector(REPO_READY, timeout=20000); pg.wait_for_timeout(2500)
        pg.add_style_tag(content=HIDE); pg.wait_for_timeout(400)
        y0 = pg.evaluate(HEADER_TOP)
        full = pg.evaluate("document.documentElement.scrollHeight")
        pg.screenshot(path=str(tall), clip={"x": 0, "y": max(0, y0 - 4), "width": VW, "height": min(3200, full - y0)}, full_page=True)
        br.close()
    im = Image.open(tall).convert("RGB"); im = im.resize((win_w, round(im.height * win_w / im.width)), Image.LANCZOS)
    im.save(tall)
    bg = Image.new("RGB", (RW, RH), (0, 0, 0)); hdr = Image.open(out / "header.png")
    bg.paste(hdr, (0, TOP), hdr); bg.save(out / "reel_bg.png")
    music = out / "music.wav"
    subprocess.run([sys.executable, str(ROOT / "music.py"), str(music), str(REEL_SECS)], check=True, capture_output=True)
    travel = min(MAX_TRAVEL, max(0, im.height - win_h)); speed = travel / (REEL_SECS - HOLD - 1)
    fc = (f"[1:v]crop={win_w}:{win_h}:0:'min(max(0,t-{HOLD})*{speed:.2f},{travel})'[s];"
          f"[0:v][s]overlay={(RW - win_w) // 2}:{top}:shortest=1,format=yuv420p[v];"
          f"[2:a]afade=t=out:st={REEL_SECS - 1.5}:d=1.5,volume=0.8[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(REEL_SECS), "-i", str(out / "reel_bg.png"),
                    "-loop", "1", "-framerate", "30", "-t", str(REEL_SECS), "-i", str(tall), "-i", str(music),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(REEL_SECS), "-r", "30",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                    str(out / "reel.mp4")], check=True, capture_output=True)
    for f in (tall, music, out / "reel_bg.png"): f.unlink(missing_ok=True)
    print(f"reel: {REEL_SECS}s, scroll {travel}px -> {(out / 'reel.mp4').relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    reel(sys.argv[1]) if "--reel" in sys.argv else render(sys.argv[1])
