"""Collect performance numbers of our published posts (YouTube, Instagram, Facebook) into runs/metrics.json.

Usage:
    python metrics.py            (the Studio also runs it every 6 hours and from its "Yenile" button)

Reads publish_log.jsonl for the post ids. Stores data only locally (runs/ is gitignored), because our privacy policy
promises YouTube API data stays on our own computer and is refreshed or deleted at least every 30 days: every run
rewrites the numbers and history older than 30 days is dropped.
Metrics that need a permission we don't have yet are listed under "needs" (the UI shows what to enable).
"""
import sys, json, pathlib, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta
from types import SimpleNamespace
import publish as P

ROOT = pathlib.Path(__file__).parent.resolve()
OUT = ROOT / "runs" / "metrics.json"
KEEP_DAYS = 30
IG_INSIGHTS = "reach,saved,shares,views,total_interactions"


def graph(path, **params):
    env = P.read_env()
    return P.api("GET", f"{P.GRAPH}/{path}", {**params, "access_token": env["META_PAGE_TOKEN"]})


def yt_get(url, tok):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
    except urllib.error.HTTPError as ex:
        raise P.PublishError(f"YouTube {urllib.parse.urlparse(url).path}: {(ex.read() or b'')[:300].decode('utf-8', 'replace')}") from None


def perm_error(ex):
    s = str(ex).lower()
    return "permission" in s or "(#10)" in s or "(#200)" in s or "code 10," in s or "code 200," in s


def collect():
    env = P.read_env(); needs = set(); errors = []
    log = ROOT / "publish_log.jsonl"
    entries = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()] if log.exists() else []
    posts = {}
    for e in entries:
        posts[e["post"]] = {"post": e["post"], "topic": e.get("topic"), "date": e.get("date"), "theme": e.get("theme"),
                            "links": {k: v.get("link") for k, v in e.items() if isinstance(v, dict) and v.get("link")},
                            "ids": {k: v.get("id") for k, v in e.items() if isinstance(v, dict) and v.get("id")}, "m": {}}

    # ---- YouTube
    yt_ids = {p["ids"]["yt_short"]: k for k, p in posts.items() if p["ids"].get("yt_short")}
    channel = {}
    if env.get("YT_REFRESH_TOKEN"):
        try:
            tok = P.yt_access(SimpleNamespace(env=env))
            ch = yt_get("https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true", tok)["items"][0]["statistics"]
            channel["youtube"] = {"subscribers": int(ch.get("subscriberCount", 0)), "views": int(ch.get("viewCount", 0)),
                                  "videos": int(ch.get("videoCount", 0))}
            if yt_ids:
                ids = ",".join(yt_ids)
                for v in yt_get(f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={ids}", tok).get("items", []):
                    st = v["statistics"]
                    posts[yt_ids[v["id"]]]["m"]["yt_short"] = {"views": int(st.get("viewCount", 0)), "likes": int(st.get("likeCount", 0)),
                                                              "comments": int(st.get("commentCount", 0))}
                start = min(p["date"][:10] for p in posts.values() if p["ids"].get("yt_short"))
                q = urllib.parse.urlencode({"ids": "channel==MINE", "startDate": start, "endDate": datetime.now().strftime("%Y-%m-%d"),
                                            "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,shares,subscribersGained",
                                            "dimensions": "video", "filters": f"video=={ids}", "maxResults": 500})
                rep = yt_get(f"https://youtubeanalytics.googleapis.com/v2/reports?{q}", tok)
                cols = [c["name"] for c in rep.get("columnHeaders", [])]
                for row in rep.get("rows", []):
                    r = dict(zip(cols, row)); m = posts[yt_ids[r["video"]]]["m"].setdefault("yt_short", {})
                    m.update(watch_minutes=round(r["estimatedMinutesWatched"], 1), avg_view_sec=round(r["averageViewDuration"]),
                             avg_view_pct=round(r["averageViewPercentage"], 1), shares=int(r["shares"]), subs_gained=int(r["subscribersGained"]))
        except Exception as ex:
            errors.append(f"YouTube: {ex}")

    # ---- Instagram
    if env.get("META_PAGE_TOKEN"):
        try:
            a = graph(env["IG_USER_ID"], fields="followers_count,media_count")
            channel["instagram"] = {"followers": a.get("followers_count"), "posts": a.get("media_count")}
        except Exception as ex:
            errors.append(f"Instagram account: {ex}")
        for k, p in posts.items():
            for step in ("ig_carousel", "ig_reel"):
                mid = p["ids"].get(step)
                if not mid: continue
                try:
                    b = graph(mid, fields="like_count,comments_count")
                    m = p["m"].setdefault(step, {}); m.update(likes=b.get("like_count", 0), comments=b.get("comments_count", 0))
                    try:
                        for it in graph(f"{mid}/insights", metric=IG_INSIGHTS).get("data", []):
                            m[it["name"]] = (it.get("values") or [{}])[0].get("value", it.get("total_value", {}).get("value"))
                    except P.PublishError as ex:
                        if perm_error(ex): needs.add("instagram_manage_insights")
                        else: errors.append(f"{k} {step} insights: {ex}")
                except Exception as ex:
                    errors.append(f"{k} {step}: {ex}")

        # ---- Facebook
        try:
            pg = graph(env["FB_PAGE_ID"], fields="followers_count,fan_count")
            channel["facebook"] = {"followers": pg.get("followers_count"), "likes": pg.get("fan_count")}
        except Exception as ex:
            errors.append(f"Facebook page: {ex}")
        for k, p in posts.items():
            pid = p["ids"].get("fb_photos")
            if pid:
                try:
                    b = graph(pid, fields="reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0),shares")
                    p["m"]["fb_photos"] = {"reactions": b.get("reactions", {}).get("summary", {}).get("total_count", 0),
                                           "comments": b.get("comments", {}).get("summary", {}).get("total_count", 0),
                                           "shares": b.get("shares", {}).get("count", 0)}
                    try:
                        # post_impressions_unique was retired by Meta; unique viewers of the post's media replace it
                        for it in graph(f"{pid}/insights", metric="post_total_media_view_unique").get("data", []):
                            p["m"]["fb_photos"]["reach"] = (it.get("values") or [{}])[0].get("value")
                    except P.PublishError as ex:
                        if perm_error(ex): needs.add("read_insights")
                        else: errors.append(f"{k} fb_photos insights: {ex}")
                except Exception as ex:
                    if perm_error(ex): needs.add("pages_read_user_content")
                    else: errors.append(f"{k} fb_photos: {ex}")
            vid = p["ids"].get("fb_reel")
            if vid:
                try:
                    b = graph(vid, fields="likes.summary(true).limit(0),comments.summary(true).limit(0)")
                    p["m"]["fb_reel"] = {"likes": b.get("likes", {}).get("summary", {}).get("total_count", 0),
                                         "comments": b.get("comments", {}).get("summary", {}).get("total_count", 0)}
                    try:
                        for it in graph(f"{vid}/video_insights", metric="blue_reels_play_count,post_video_avg_time_watched").get("data", []):
                            v = (it.get("values") or [{}])[0].get("value")
                            if it["name"] == "blue_reels_play_count": p["m"]["fb_reel"]["plays"] = v
                            else: p["m"]["fb_reel"]["avg_view_sec"] = round((v or 0) / 1000, 1)  # API gives milliseconds
                    except P.PublishError as ex:
                        if perm_error(ex): needs.add("read_insights")
                        else: errors.append(f"{k} fb_reel insights: {ex}")
                except Exception as ex:
                    errors.append(f"{k} fb_reel: {ex}")

    # ---- history (one point per post per day), pruned to KEEP_DAYS
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    today = datetime.now().strftime("%Y-%m-%d"); cutoff = (datetime.now() - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    hist = {k: [h for h in v if h["day"] >= cutoff and h["day"] != today] for k, v in (old.get("history") or {}).items() if k in posts}
    for k, p in posts.items():
        m = p["m"]
        hist.setdefault(k, []).append({"day": today, "yt_views": m.get("yt_short", {}).get("views"),
                                       "ig_likes": sum(m.get(s, {}).get("likes", 0) or 0 for s in ("ig_carousel", "ig_reel")),
                                       "fb": (m.get("fb_photos", {}).get("reactions", 0) or 0) + (m.get("fb_reel", {}).get("likes", 0) or 0)})
    data = {"updated": datetime.now().astimezone().isoformat(timespec="seconds"), "channel": channel,
            "posts": sorted(posts.values(), key=lambda p: p["date"] or "", reverse=True), "history": hist,
            "needs": sorted(needs), "errors": errors}
    OUT.parent.mkdir(exist_ok=True)
    tmp = OUT.with_suffix(".tmp"); tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8"); tmp.replace(OUT)
    return data


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    d = collect()
    print(f"{len(d['posts'])} posts, channel: {json.dumps(d['channel'])}")
    for p in d["posts"]: print(" ", p["post"], json.dumps(p["m"]))
    if d["needs"]: print("needs permissions:", ", ".join(d["needs"]))
    for e in d["errors"]: print("ERROR", e)


if __name__ == "__main__":
    main()
