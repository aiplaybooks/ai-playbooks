"""Hashtag research for the caption agent: which tags are really used, and with how much engagement, for a post's topic.

Usage:
    python tags.py "chatgpt prompts" "side hustle" [--days 30] [--json out.json]

Data (all free, official APIs, cached per day in research/tags/):
- Instagram (+ Facebook, same Meta audience): the last ~40 posts of big AI accounts (sources.json -> "tags" ->
  "ig_accounts") via the Graph API's Business Discovery. Instagram's hashtag search needs a Meta feature review we
  don't have, so this is the signal: for every hashtag, how many of their posts used it, by how many accounts, and
  the average likes + comments of those posts, overall and on the posts whose caption matches the keywords.
- YouTube: for each keyword, the most-viewed Shorts of the last N days (YouTube Data API search, 100 quota units per
  keyword): their tags and #hashtags weighted by views.
Prints a readable ranking; --json writes the full data. Never fails hard: a source that errors is listed under errors.
"""
import sys, json, re, math, time, argparse, pathlib, urllib.request, urllib.parse, urllib.error
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

ROOT = pathlib.Path(__file__).parent.resolve()
CACHE = ROOT / "research" / "tags"
GRAPH = "https://graph.facebook.com/v25.0"
DEFAULT_IG = ["chatgptips", "chatgptricks", "openai", "googlegemini", "nvidia", "airesearches", "theaifield",
              "therundownai", "rowancheung", "godofprompt", "techcrunch", "notionhq"]
STOP = {"the", "and", "for", "with", "you", "your", "that", "this", "how", "what", "are", "can", "from", "into", "ai"}


def env():
    out = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1); out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def cfg():
    try: return json.loads((ROOT / "sources.json").read_text(encoding="utf-8")).get("tags", {})
    except (OSError, ValueError): return {}


def words(t):
    return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if len(w) > 2 and w not in STOP}


PAID = re.compile(r"partner|sponsor|^ad$|^ads$|paidpartnership|collab")  # paid-partnership tags are not topic tags


def hashtags(t):
    return [h.lower() for h in re.findall(r"#(\w+)", t or "") if not PAID.search(h.lower())]


# ---------------------------------------------------------------- Instagram (Business Discovery)

def ig_posts(e, errors):
    day = f"{datetime.now():%Y-%m-%d}"; f = CACHE / f"ig_accounts_{day}.json"
    if f.exists(): return json.loads(f.read_text(encoding="utf-8"))
    posts = []
    for u in cfg().get("ig_accounts") or DEFAULT_IG:
        fields = f"business_discovery.username({u}){{followers_count,media.limit(40){{caption,like_count,comments_count,media_type,timestamp,permalink}}}}"
        url = f"{GRAPH}/{e['IG_USER_ID']}?" + urllib.parse.urlencode({"fields": fields, "access_token": e["META_PAGE_TOKEN"]})
        try:
            with urllib.request.urlopen(url, timeout=60) as r: b = json.load(r)["business_discovery"]
        except urllib.error.HTTPError as ex:
            errors.append(f"instagram @{u}: {json.load(ex).get('error', {}).get('message', ex)}"[:200]); continue
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as ex:
            errors.append(f"instagram @{u}: {ex}"[:200]); continue
        for m in b.get("media", {}).get("data", []):
            posts.append({"account": u, "followers": b.get("followers_count", 0), "caption": m.get("caption") or "",
                          "likes": m.get("like_count") or 0, "comments": m.get("comments_count") or 0,
                          "type": m.get("media_type"), "date": m.get("timestamp"), "link": m.get("permalink")})
        time.sleep(0.5)
    CACHE.mkdir(parents=True, exist_ok=True)
    if posts: f.write_text(json.dumps(posts, ensure_ascii=False), encoding="utf-8")
    return posts


def rank_ig(posts, kw):
    def table(ps):
        t = defaultdict(lambda: {"posts": 0, "accounts": set(), "eng": 0.0})
        for p in ps:
            # engagement relative to the account's size, so a giant account doesn't drown the rest
            rel = (p["likes"] + 3 * p["comments"]) / max(1000, p["followers"]) * 1000
            for h in set(hashtags(p["caption"])):
                t[h]["posts"] += 1; t[h]["accounts"].add(p["account"]); t[h]["eng"] += rel
        rows = [{"tag": h, "posts": v["posts"], "accounts": len(v["accounts"]), "eng_per_post": round(v["eng"] / v["posts"], 2),
                 "score": round(v["posts"] * (1 + len(v["accounts"])) * (1 + v["eng"] / v["posts"]) ** 0.5, 1)} for h, v in t.items()]
        return sorted(rows, key=lambda r: -r["score"])[:25]
    rel = [p for p in posts if kw & words(p["caption"])]
    return {"all": table(posts), "matching": table(rel), "matching_posts": len(rel), "posts": len(posts),
            "top_matching": [{k: p[k] for k in ("account", "likes", "comments", "link")} | {"caption": p["caption"][:400]}
                             for p in sorted(rel, key=lambda p: -(p["likes"] + 3 * p["comments"]))[:5]]}


# ---------------------------------------------------------------- YouTube

def yt(queries, days, errors):
    try:
        import publish as P, metrics as M
        tok = P.yt_access(SimpleNamespace(env=P.read_env()))
    except Exception as ex:  # noqa: BLE001
        errors.append(f"youtube: {ex}"[:200]); return {}
    after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {}
    for q in queries:
        f = CACHE / f"yt_{datetime.now():%Y-%m-%d}_{re.sub(r'[^a-z0-9]+', '-', q.lower())[:40]}.json"
        if f.exists(): out[q] = json.loads(f.read_text(encoding="utf-8")); continue
        try:
            s = M.yt_get("https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(
                {"part": "snippet", "q": q, "type": "video", "videoDuration": "short", "order": "viewCount",
                 "publishedAfter": after, "maxResults": 30, "relevanceLanguage": "en"}), tok)
            ids = [i["id"]["videoId"] for i in s.get("items", [])]
            v = M.yt_get("https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id=" + ",".join(ids), tok) if ids else {}
        except Exception as ex:  # noqa: BLE001
            errors.append(f"youtube '{q}': {ex}"[:200]); continue
        t = defaultdict(lambda: {"videos": 0, "views": 0}); vids = []
        for it in v.get("items", []):
            sn = it["snippet"]; views = int(it["statistics"].get("viewCount", 0))
            vids.append({"title": sn["title"], "views": views, "url": f"https://www.youtube.com/shorts/{it['id']}"})
            tags = {x.lower().replace(" ", "") for x in sn.get("tags", [])} | set(hashtags(sn["title"] + " " + sn.get("description", "")))
            for x in tags:
                if x in ("shorts", "short", "youtubeshorts", "viral", "trending", "fyp"): continue
                t[x]["videos"] += 1; t[x]["views"] += views
        rows = [{"tag": k, "videos": x["videos"], "views": x["views"], "score": round(x["videos"] * math.log10(1 + x["views"]), 1)}
                for k, x in t.items() if x["videos"] >= 2]
        out[q] = {"tags": sorted(rows, key=lambda r: -r["score"])[:20], "top_videos": sorted(vids, key=lambda x: -x["views"])[:5]}
        CACHE.mkdir(parents=True, exist_ok=True); f.write_text(json.dumps(out[q], ensure_ascii=False), encoding="utf-8")
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("keywords", nargs="+"); ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--json"); ap.add_argument("--no-youtube", action="store_true")
    a = ap.parse_args()
    errors = []; e = env(); kw = set().union(*(words(k) for k in a.keywords))
    ig = rank_ig(ig_posts(e, errors), kw) if e.get("META_PAGE_TOKEN") else {}
    ys = {} if a.no_youtube else yt(a.keywords, a.days, errors)
    res = {"keywords": a.keywords, "instagram": ig, "youtube": ys, "errors": errors, "generated": datetime.now().isoformat(timespec="seconds")}
    if a.json: pathlib.Path(a.json).parent.mkdir(parents=True, exist_ok=True); pathlib.Path(a.json).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    if ig:
        print(f"INSTAGRAM (+Facebook) · {ig['posts']} posts of big AI accounts, {ig['matching_posts']} match the keywords")
        print("  on matching posts:", ", ".join(f"#{r['tag']} ({r['posts']}p/{r['accounts']}acc, eng {r['eng_per_post']})" for r in ig["matching"][:15]) or "-")
        print("  overall:          ", ", ".join(f"#{r['tag']} ({r['posts']}p/{r['accounts']}acc)" for r in ig["all"][:15]))
        for p in ig["top_matching"][:3]: print(f"  best matching post: @{p['account']} {p['likes']} likes: {p['caption'][:140]!r}")
    for q, d in ys.items():
        print(f"YOUTUBE '{q}':", ", ".join(f"#{r['tag']} ({r['videos']}v, {r['views'] // 1000}k views)" for r in d["tags"][:12]) or "-")
        for v in d["top_videos"][:2]: print(f"  top short: {v['views'] // 1000}k views · {v['title'][:90]}")
    for x in errors: print("error:", x)


if __name__ == "__main__":
    main()
