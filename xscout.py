"""Viral AI clip finder on X for the strategy director (X blocks anonymous search, the Nitter/xcancel mirrors are dead,
Reddit returns 403 since 2025): a headless Chromium with a saved login of a SECONDARY X account.

Usage:
    python xscout.py --login          opens a visible browser: log in to X ONCE with a secondary account (never the
                                      owner's main account: automated browsing is against X's rules, the account can
                                      get limited). The session is kept in .cache/x-profile (gitignored).
    python xscout.py [--json out.json] [--days 3] [--min-likes 1500]
                                      headless search of recent video posts about AI, ranked by likes -> printed / JSON:
                                      [{url, creator, text, likes, reposts, views, posted}]
The strategy director (prompts/strategy.md) picks from this list; clip.py / yt-dlp fetch the chosen post.
"""
import sys, re, json, time, pathlib, argparse, urllib.parse
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
PROFILE = ROOT / ".cache" / "x-chrome"  # a profile of the installed Google Chrome (x-profile was Playwright's Chromium)
CHROME = next((p for p in (pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
                           pathlib.Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
                           pathlib.Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe") if p.exists()), None)
QUERIES = ["(AI OR Sora OR Veo OR Kling OR Seedance OR Higgsfield OR Runway) video",
           "(ChatGPT OR Claude OR Gemini OR Grok) demo", "AI robot", "AI agent demo",
           "made with AI", "AI generated"]


def num(s):
    s = (s or "").strip().replace(",", "")
    m = re.match(r"([\d.]+)\s*([KMB]?)", s, re.I)
    if not m: return 0
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2).upper()])


def login():
    """X freezes its login page in an automated browser (2026-09-29: a `debugger` trap under Playwright), so the login
    runs in a plain Google Chrome window on our own profile folder; the headless search reuses its cookies."""
    import subprocess
    if not CHROME: sys.exit("ERROR: Google Chrome is not installed")
    PROFILE.mkdir(parents=True, exist_ok=True)
    print("Log in with the SECONDARY X account in the Chrome window, then CLOSE that window.")
    subprocess.run([str(CHROME), f"--user-data-dir={PROFILE}", "--no-first-run", "--no-default-browser-check",
                    "--new-window", "https://x.com/login"])
    print("window closed: checking the session ...")
    try: search(1, 10**9, check_only=True); print("logged in: the session works")
    except SystemExit as ex: print(ex)


def search(days, min_likes, limit_per_query=25, check_only=False):
    if not PROFILE.exists(): sys.exit("ERROR: no X login yet: run `python xscout.py --login` once (owner, secondary account)")
    since = f"{datetime.now(timezone.utc) - timedelta(days=days):%Y-%m-%d}"
    found = {}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(PROFILE), channel="chrome", headless=True,
                                                   viewport={"width": 1200, "height": 2400}, locale="en-US",
                                                   args=["--disable-blink-features=AutomationControlled"])
        pg = ctx.new_page()
        if check_only:
            pg.goto("https://x.com/home", wait_until="domcontentloaded"); pg.wait_for_timeout(4000)
            ok = "/home" in pg.url and "login" not in pg.url; ctx.close()
            if not ok: sys.exit("ERROR: not logged in (the X session is missing): run X_giris.bat again")
            return []
        for q in QUERIES:
            full = f"{q} filter:native_video min_faves:{min_likes} since:{since} lang:en -filter:replies"
            pg.goto("https://x.com/search?" + urllib.parse.urlencode({"q": full, "f": "top"}), wait_until="domcontentloaded")
            if "login" in pg.url or "onboarding" in pg.url:
                ctx.close(); sys.exit("ERROR: the X session expired: run `python xscout.py --login` again")
            try: pg.wait_for_selector("article", timeout=20000)
            except Exception: continue
            for _ in range(4):
                for a in pg.query_selector_all("article"):
                    link = a.query_selector("a[href*='/status/'] time")
                    href = link and link.evaluate("t => t.closest('a').getAttribute('href')")
                    if not href or not a.query_selector("video, [data-testid='videoPlayer']"): continue
                    url = "https://x.com" + href.split("/analytics")[0]
                    if url in found: continue
                    def stat(tid):
                        el = a.query_selector(f"[data-testid='{tid}'], [data-testid='un{tid}']")
                        return num(el.inner_text()) if el else 0
                    views_el = a.query_selector("a[href$='/analytics']")
                    text_el = a.query_selector("[data-testid='tweetText']")
                    found[url] = {"url": url, "creator": "@" + href.strip("/").split("/")[0],
                                  "text": (text_el.inner_text() if text_el else "")[:280],
                                  "likes": stat("like"), "reposts": stat("retweet"),
                                  "views": num(views_el.inner_text()) if views_el else 0,
                                  "posted": link.get_attribute("datetime"), "query": q}
                pg.mouse.wheel(0, 2200); time.sleep(1.5)
                if len(found) > limit_per_query * len(QUERIES): break
        ctx.close()
    return sorted(found.values(), key=lambda r: -r["likes"])


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("--login", action="store_true"); ap.add_argument("--json")
    ap.add_argument("--days", type=int, default=3); ap.add_argument("--min-likes", type=int, default=1500)
    a = ap.parse_args()
    if a.login: return login()
    rows = search(a.days, a.min_likes)
    if a.json: pathlib.Path(a.json).write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    for r in rows[:30]: print(f"{r['likes']:>7} likes {r['views']:>9} views  {r['url']}  {r['text'][:80]!r}")
    print(f"{len(rows)} video posts")


if __name__ == "__main__":
    main()
