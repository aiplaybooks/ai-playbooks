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
        try: pg.wait_for_selector("#repository-container-header", timeout=20000)
        except Exception: sys.exit("ERROR: the GitHub page did not show a repository (login wall, 404 or rate limit?)")
        pg.wait_for_timeout(2500)
        pg.add_style_tag(content=HIDE)
        top = pg.evaluate("document.querySelector('#repository-container-header').getBoundingClientRect().top + scrollY")
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


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    render(sys.argv[1])
