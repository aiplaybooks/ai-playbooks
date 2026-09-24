"""Viral AI video finder for the Reels: collects candidate clips into research/<date>_viral.json.

Usage:
    python viral.py [--date 2026-09-25]          collect candidates
    python viral.py --download <id>              fetch one Reddit clip -> output/viral/<id>/source.mp4 (+ meta.json)

Sources (settings in sources.json -> "viral"):
- Reddit (downloadable): top video posts of the day/week in AI subreddits, via the official API (read-only,
  application-only OAuth: REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET in .env; create a "script" app at
  https://www.reddit.com/prefs/apps). NSFW, too short/long and low-score posts are dropped.
- YouTube (signal only, never downloaded: that breaks YouTube's terms and would put our API project at risk):
  the most-viewed recent AI shorts, so the picker sees what is trending and can look for the same clip on Reddit.
Every Reddit candidate keeps its author + subreddit + permalink: the Reel must credit the creator.
"""
import sys, os, json, re, time, base64, pathlib, argparse, subprocess, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

ROOT = pathlib.Path(__file__).parent.resolve()
UA = "windows:aiplaybooks-viral:0.1 (by /u/aiplaybooks)"


def read_env():
    env = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"):
        if os.environ.get(k): env[k] = os.environ[k]
    return env


def http(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())


def reddit_token(env):
    auth = base64.b64encode(f"{env['REDDIT_CLIENT_ID']}:{env['REDDIT_CLIENT_SECRET']}".encode()).decode()
    r = http("https://www.reddit.com/api/v1/access_token", data=b"grant_type=client_credentials",
             headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"})
    if "access_token" not in r: raise RuntimeError(f"Reddit token: {r}")
    return r["access_token"]


def reddit(cfg, env, errors):
    if not (env.get("REDDIT_CLIENT_ID") and env.get("REDDIT_CLIENT_SECRET")):
        errors.append("Reddit: REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET missing in .env"); return []
    tok = reddit_token(env); items = {}
    for sub in cfg["subreddits"]:
        for period in cfg.get("periods", ["day"]):
            try:
                d = http(f"https://oauth.reddit.com/r/{sub}/top?t={period}&limit=50&raw_json=1",
                         headers={"Authorization": f"Bearer {tok}"})
            except urllib.error.HTTPError as ex:
                errors.append(f"r/{sub} {period}: HTTP {ex.code}"); continue
            for c in d["data"]["children"]:
                p = c["data"]
                if p.get("crosspost_parent_list"): p = {**p["crosspost_parent_list"][0], "score": max(p["score"], p["crosspost_parent_list"][0]["score"])}
                v = ((p.get("secure_media") or p.get("media") or {}) or {}).get("reddit_video")
                if not v or p.get("over_18") or p.get("spoiler"): continue
                secs = v.get("duration") or 0
                if p["score"] < cfg["min_score"] or not cfg["min_secs"] <= secs <= cfg["max_secs"]: continue
                key = p["id"]
                if key in items and items[key]["score"] >= p["score"]: continue
                items[key] = {
                    "id": f"rd-{p['id']}", "source": "reddit", "downloadable": True,
                    "title": p["title"], "subreddit": p["subreddit"], "author": p.get("author"),
                    "url": "https://www.reddit.com" + p["permalink"], "score": p["score"],
                    "comments": p.get("num_comments", 0), "upvote_ratio": p.get("upvote_ratio"),
                    "date": datetime.fromtimestamp(p["created_utc"], timezone.utc).isoformat(timespec="seconds"),
                    "secs": secs, "width": v.get("width"), "height": v.get("height"),
                    "flair": p.get("link_flair_text"), "thumb": p.get("thumbnail") if str(p.get("thumbnail", "")).startswith("http") else None,
                }
            time.sleep(0.7)  # stay far below the free API rate limit
    return sorted(items.values(), key=lambda x: -x["score"])


def youtube(cfg, errors):
    try:
        import publish as P, metrics as M
        env = P.read_env()
        if not env.get("YT_REFRESH_TOKEN"): errors.append("YouTube: no YT_REFRESH_TOKEN"); return []
        tok = P.yt_access(SimpleNamespace(env=env))
    except Exception as ex:  # noqa: BLE001 - YouTube is only a signal; never fail the run for it
        errors.append(f"YouTube: {ex}"); return []
    after = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen = {}
    for q in cfg.get("youtube_queries", []):
        try:
            s = M.yt_get("https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(
                {"part": "snippet", "q": q, "type": "video", "videoDuration": "short", "order": "viewCount",
                 "publishedAfter": after, "maxResults": 25, "relevanceLanguage": "en"}), tok)
            ids = [i["id"]["videoId"] for i in s.get("items", [])]
            if not ids: continue
            v = M.yt_get("https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id=" + ",".join(ids), tok)
        except Exception as ex:  # noqa: BLE001
            errors.append(f"YouTube '{q}': {ex}"); continue
        for it in v.get("items", []):
            views = int(it["statistics"].get("viewCount", 0))
            if views < cfg.get("youtube_min_views", 0) or it["id"] in seen: continue
            seen[it["id"]] = {"id": f"yt-{it['id']}", "source": "youtube", "downloadable": False,
                              "title": it["snippet"]["title"], "channel": it["snippet"]["channelTitle"],
                              "url": f"https://www.youtube.com/shorts/{it['id']}", "views": views,
                              "date": it["snippet"]["publishedAt"], "query": q}
    return sorted(seen.values(), key=lambda x: -x["views"])


def posted_ids():
    log = ROOT / "publish_log.jsonl"
    if not log.exists(): return set()
    return {json.loads(l).get("viral_id") for l in log.read_text(encoding="utf-8").splitlines() if l.strip()} - {None}


def collect(day):
    cfg = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))["viral"]
    env = read_env(); errors = []
    try: rd = reddit(cfg, env, errors)
    except Exception as ex:  # noqa: BLE001
        rd = []; errors.append(f"Reddit: {ex}")
    done = posted_ids()
    rd = [x for x in rd if x["id"] not in done]
    out = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "reddit": rd,
           "youtube_signal": youtube(cfg, errors), "errors": errors}
    f = ROOT / "research" / f"{day}_viral.json"
    f.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(rd)} reddit clips, {len(out['youtube_signal'])} youtube signals, {len(errors)} errors -> {f.relative_to(ROOT)}")
    for e in errors: print("  !", e)


def download(cid, day):
    if not cid.startswith("rd-"): sys.exit("only Reddit clips (rd-...) can be downloaded; YouTube is a signal only")
    item = None
    for f in sorted((ROOT / "research").glob("*_viral.json"), reverse=True):
        item = next((x for x in json.loads(f.read_text(encoding="utf-8"))["reddit"] if x["id"] == cid), None)
        if item: break
    if not item: sys.exit(f"{cid} not found in research/*_viral.json")
    out = ROOT / "output" / "viral" / cid; out.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-playlist", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
                    "-o", str(out / "source.%(ext)s"), item["url"]], check=True)
    (out / "meta.json").write_text(json.dumps(item, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", out / "source.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d")); ap.add_argument("--download")
    a = ap.parse_args()
    download(a.download, a.date) if a.download else collect(a.date)


if __name__ == "__main__":
    main()
