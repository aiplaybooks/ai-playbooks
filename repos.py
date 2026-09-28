"""GitHub repo collector for the repo pillar (single image + caption + first comment posts).

Usage:
    python repos.py                    collect -> research/repos/<date>.json (+ README excerpts of the top repos)
    python repos.py --info owner/repo  fresh numbers + README start of one repo (the writer verifies with this)

Sources (all free, the `gh` login's token; never printed):
    GitHub Search API   rising repos (created in the last 45 days, many stars) + per-category searches
                        (agents / Claude Code, local media generation, creator tools, learning, SaaS alternatives)
    GitHub Trending     github.com/trending (daily + weekly): what is viral right now, with "stars this week"
    star history        research/repos/stars.json: our own daily star snapshots -> gain over ~7 days
Filters: not archived / not a fork, pushed in the last 90 days, a description, >= 1000 stars or a real weekly gain;
repos we already posted (content/repos/*.json) are left out. README excerpts of the top 40 go to
research/repos/readme/<owner>__<repo>.md, with `flags` (deprecated, no license ...) so the scout can skip them.
"""
import sys, re, json, time, pathlib, argparse, subprocess, urllib.request, urllib.parse, urllib.error, base64
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).parent.resolve()
OUT = ROOT / "research" / "repos"
API = "https://api.github.com"
NOW = datetime.now(timezone.utc)
D = lambda days: f"{NOW - timedelta(days=days):%Y-%m-%d}"

# (category, query) - category is only a hint for the scout; one repo can be found by several queries
SEARCHES = [
    ("rising", f"created:>{D(45)} stars:>800"),
    ("rising", f"created:>{D(14)} stars:>300"),
    ("agents", f"topic:claude-code stars:>300 pushed:>{D(60)}"),
    ("agents", f"topic:mcp stars:>1500 pushed:>{D(60)}"),
    ("agents", f"topic:ai-agents stars:>3000 pushed:>{D(60)}"),
    ("agents", f"topic:agent-skills stars:>300 pushed:>{D(60)}"),
    ("agents", f"\"claude code\" in:name,description stars:>1000 pushed:>{D(60)}"),
    ("agents", f"codex in:name,description topic:ai stars:>1000 pushed:>{D(60)}"),
    ("local_media", f"topic:text-to-speech stars:>2000 pushed:>{D(90)}"),
    ("local_media", f"topic:voice-cloning stars:>1000 pushed:>{D(90)}"),
    ("local_media", f"topic:comfyui stars:>2000 pushed:>{D(60)}"),
    ("local_media", f"topic:video-generation stars:>1500 pushed:>{D(90)}"),
    ("local_media", f"topic:image-generation stars:>2000 pushed:>{D(90)}"),
    ("local_media", f"topic:music-generation stars:>1000 pushed:>{D(90)}"),
    ("creator", f"topic:video-editing stars:>1500 pushed:>{D(90)}"),
    ("creator", f"topic:subtitles stars:>1500 pushed:>{D(90)}"),
    ("creator", f"topic:social-media ai stars:>1000 pushed:>{D(90)}"),
    ("creator", f"topic:automation ai stars:>3000 pushed:>{D(60)}"),
    ("creator", f"topic:self-hosted ai stars:>3000 pushed:>{D(60)}"),
    ("learning", f"topic:prompt-engineering stars:>3000 pushed:>{D(90)}"),
    ("learning", f"course llm in:name,description stars:>3000 pushed:>{D(90)}"),
    ("learning", f"tutorial agents in:name,description stars:>2000 pushed:>{D(90)}"),
    ("alternative", f"\"open-source alternative\" in:description stars:>2000 pushed:>{D(60)}"),
    ("alternative", f"\"alternative to\" in:description ai stars:>2000 pushed:>{D(60)}"),
]
BAD_README = re.compile(r"(?i)\b(this (repo|repository|project) (is|has been) (deprecated|archived|discontinued)|"
                        r"no longer (maintained|supported|under active development)|deprecated[.:])")


def token():
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or None
    except (OSError, subprocess.TimeoutExpired):
        return None


TOKEN = None


def get(url, accept="application/vnd.github+json", tries=3):
    h = {"Accept": accept, "User-Agent": "aiplaybooks-repos", "X-GitHub-Api-Version": "2022-11-28"}
    if TOKEN and url.startswith(API): h["Authorization"] = f"Bearer {TOKEN}"
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=40) as r:
                body = r.read()
                return json.loads(body) if "json" in accept else body.decode("utf-8", "replace")
        except urllib.error.HTTPError as ex:
            if ex.code in (403, 429) and i < tries - 1:  # search API: 30 requests/min
                wait = int(ex.headers.get("Retry-After") or 0) or max(5, int(ex.headers.get("X-RateLimit-Reset", time.time() + 30)) - int(time.time()))
                time.sleep(min(wait, 70)); continue
            if ex.code == 404: return None
            raise
        except (urllib.error.URLError, TimeoutError):
            if i == tries - 1: raise
            time.sleep(3)


def slim(r):
    lic = (r.get("license") or {}).get("spdx_id")
    return {"full_name": r["full_name"], "url": r["html_url"], "description": (r.get("description") or "").strip()[:300],
            "stars": r["stargazers_count"], "forks": r["forks_count"], "language": r.get("language"),
            "license": None if lic in (None, "NOASSERTION") else lic, "topics": r.get("topics", [])[:12],
            "created": r["created_at"][:10], "pushed": r["pushed_at"][:10], "homepage": r.get("homepage") or "",
            "archived": r.get("archived", False), "fork": r.get("fork", False), "owner_type": r["owner"]["type"]}


def search(q, n=40):
    d = get(f"{API}/search/repositories?" + urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": n}))
    return [slim(r) for r in (d or {}).get("items", [])]


def trending(since):
    """github.com/trending: [(full_name, stars gained in the period)]."""
    try: html = get(f"https://github.com/trending?since={since}", accept="text/html")
    except Exception as ex:  # noqa: BLE001 - a page change must never stop the collection
        print(f"trending {since}: {ex}"); return []
    out = []
    for art in html.split("<article")[1:]:
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"/]+/[^"/]+)"', art)
        g = re.search(r"([\d,]+)\s+stars?\s+(today|this week|this month)", art)
        if m: out.append((m.group(1), int(g.group(1).replace(",", "")) if g else 0))
    return out


def readme(full):
    d = get(f"{API}/repos/{full}/readme")
    if not d or not d.get("content"): return ""
    return base64.b64decode(d["content"]).decode("utf-8", "replace")


def clean_md(t, n=3500):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<img[^>]*>|!\[[^\]]*\]\([^)]*\)", "", t)          # images / badges
    t = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()[:n]


def posted_repos():
    out = set()
    for f in (ROOT / "content" / "repos").glob("*.json"):
        try: out.add((json.loads(f.read_text(encoding="utf-8")).get("repo") or {}).get("full_name", "").lower())
        except (OSError, ValueError): pass
    return out - {""}


def collect():
    OUT.mkdir(parents=True, exist_ok=True); (OUT / "readme").mkdir(exist_ok=True)
    found, errors = {}, []
    for cat, q in SEARCHES:
        try:
            for r in search(q):
                x = found.setdefault(r["full_name"], {**r, "found_by": []})
                if cat not in x["found_by"]: x["found_by"].append(cat)
        except Exception as ex:  # noqa: BLE001
            errors.append(f"search {q!r}: {ex}")
        time.sleep(2.2)  # stay under 30 search requests / minute
    trend = {}
    for since in ("daily", "weekly"):
        for full, gain in trending(since):
            trend.setdefault(full, {})[since] = gain
    for full in trend:
        if full not in found:
            try:
                r = get(f"{API}/repos/{full}")
                if r: found[full] = {**slim(r), "found_by": []}
            except Exception as ex:  # noqa: BLE001
                errors.append(f"repo {full}: {ex}")
        if full in found:
            found[full]["trending"] = trend[full]
            if "trending" not in found[full]["found_by"]: found[full]["found_by"].append("trending")
    # own star history -> gain over ~7 days
    hist_f = OUT / "stars.json"
    try: hist = json.loads(hist_f.read_text(encoding="utf-8"))
    except (OSError, ValueError): hist = {}
    today = f"{NOW:%Y-%m-%d}"
    for full, r in found.items():
        h = hist.setdefault(full, {}); h[today] = r["stars"]
        old = sorted(d for d in h if d <= D(6))
        if old: r["gain_7d"] = r["stars"] - h[old[-1]]
    cut = D(60)
    for full in list(hist):  # keep the file small
        hist[full] = {d: v for d, v in hist[full].items() if d >= cut}
        if not hist[full]: del hist[full]
    hist_f.write_text(json.dumps(hist, separators=(",", ":")), encoding="utf-8")

    done = posted_repos(); keep = []
    for r in found.values():
        week = (r.get("trending") or {}).get("weekly") or r.get("gain_7d") or 0
        r["week_gain"] = week
        if r["archived"] or r["fork"] or not r["description"] or r["full_name"].lower() in done: continue
        if r["pushed"] < D(90): continue
        if r["stars"] < 1000 and week < 300: continue
        age = max(1, (NOW - datetime.fromisoformat(r["created"]).replace(tzinfo=timezone.utc)).days)
        # rough ranking for the scout: momentum first, size second
        r["rank"] = round(min(week, 20000) / 100 + min(r["stars"], 100000) / 5000 + (30 if age <= 45 and r["stars"] / age > 50 else 0), 1)
        keep.append(r)
    keep.sort(key=lambda r: -r["rank"])
    for r in keep[:40]:  # README excerpts for the scout (verification starts here)
        f = OUT / "readme" / (r["full_name"].replace("/", "__") + ".md")
        try:
            if not f.exists() or f.stat().st_mtime < time.time() - 3 * 86400:
                f.write_text(clean_md(readme(r["full_name"]), 6000), encoding="utf-8")
            text = f.read_text(encoding="utf-8")
            r["readme"] = f.relative_to(ROOT).as_posix()
            r["flags"] = [x for x, bad in (("deprecated", BAD_README.search(text[:2500])), ("no license", not r["license"]),
                                          ("readme mostly non-English", len(re.findall(r"[一-鿿]", text[:1500])) > 150))
                          if bad]
        except Exception as ex:  # noqa: BLE001
            errors.append(f"readme {r['full_name']}: {ex}")
    out = OUT / f"{today}.json"
    out.write_text(json.dumps({"generated": NOW.isoformat(timespec="seconds"), "count": len(keep), "errors": errors,
                               "repos": keep[:150]}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(found)} repos seen, {len(keep)} kept ({len(errors)} errors) -> {out.relative_to(ROOT).as_posix()}")


def info(full):
    r = get(f"{API}/repos/{full}")
    if not r: sys.exit(f"not found: {full}")
    s = slim(r); rel = get(f"{API}/repos/{full}/releases/latest")
    s["latest_release"] = rel and {"tag": rel.get("tag_name"), "date": (rel.get("published_at") or "")[:10]}
    s["stars_rounded"] = rounded(s["stars"])
    print(json.dumps(s, indent=1, ensure_ascii=False))
    print("\n----- README (start) -----\n" + clean_md(readme(full), 8000))


def rounded(n):
    """Star count for hooks, always rounded DOWN (41,380 -> 41K+)."""
    if n >= 1000: return f"{n // 1000}K+"
    return f"{n // 100 * 100}+" if n >= 100 else str(n)


def main():
    global TOKEN
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("--info")
    a = ap.parse_args()
    TOKEN = token()
    if not TOKEN: print("warning: no `gh` token, GitHub allows only 10 searches/min without it")
    info(a.info) if a.info else collect()


if __name__ == "__main__":
    main()
