"""Performance numbers for the daily strategy review (prompts/strategy.md) + the strategy the Studio follows.

Usage:
    python strategy.py [--days 14] [--json out.json]     per-format / per-platform results of our posts

Formats: news (carousel about news), evergreen (carousel, not news), pack (prompt pack carousel), clip (viral Reel),
repo (GitHub photo post). Numbers from runs/metrics.json (metrics.py, refreshed every 6 h).

strategy.json (repo root, written by the strategy agent, read by studio.py):
    {"updated": "...", "mix": {"news": 3, "repo": 2, "pack": 2, "clip": 1},     autopilot rotation weights
     "post_slots": ["14:00", ...] | null,                                          optional new publish times
     "skip": {"post": ["fb_photos"], "repo": [], "clip": []},                      publish steps to skip per flow
     "experiments": [{"id", "started", "change", "metric", "success", "status"}]}
The directives for the writers live in prompts/strategy_playbook.md (read by every writing agent).
"""
import sys, json, pathlib, argparse
from datetime import datetime, timedelta

ROOT = pathlib.Path(__file__).parent.resolve()
STRATEGY = ROOT / "strategy.json"
DEFAULT = {"mix": {"news": 3, "repo": 2, "pack": 2}, "post_slots": None, "skip": {}, "experiments": []}
PLATFORM_VIEW = {"ig_carousel": "views", "ig_photo": "views", "ig_reel": "views", "fb_photos": "reach",
                 "fb_reel": "plays", "yt_short": "views"}


def load():
    try: s = json.loads(STRATEGY.read_text(encoding="utf-8"))
    except (OSError, ValueError): s = {}
    return {**DEFAULT, **s}


def rotation(s=None):
    """Autopilot format order from the mix weights, interleaved: {"news": 3, "repo": 2, "pack": 2} ->
    news repo pack news repo pack news."""
    mix = {k: int(v) for k, v in ((s or load()).get("mix") or DEFAULT["mix"]).items() if k in ("news", "repo", "pack", "clip") and int(v) > 0}
    out, left = [], dict(mix)
    while any(left.values()):
        for k in mix:
            if left[k] > 0: out.append(k); left[k] -= 1
    return out or ["news", "repo", "pack"]


def skipped(kind, step):
    return step in ((load().get("skip") or {}).get(kind) or [])


def content_of(name):
    for d in ("", "clips", "repos"):
        f = ROOT / "content" / d / f"{name}.json"
        if f.exists():
            try: return json.loads(f.read_text(encoding="utf-8")), d
            except ValueError: return {}, d
    return {}, None


def fmt(name, c, d):
    if d == "clips": return "clip"
    if d == "repos": return "repo"
    if c.get("theme") == "prompts" or "pack" in name or "prompts" in name: return "pack"
    return "evergreen" if c.get("kind") == "evergreen" else "news"


def report(days):
    m = json.loads((ROOT / "runs" / "metrics.json").read_text(encoding="utf-8"))
    cut = (datetime.now().astimezone() - timedelta(days=days)).isoformat()
    posts, agg = [], {}
    for p in m.get("posts", []):
        if p["date"] < cut[:16]: continue
        c, d = content_of(p["post"]); f = fmt(p["post"], c, d)
        row = {"post": p["post"], "format": f, "date": p["date"], "hour": p["date"][11:13],
               "hook": ((c.get("cover") or {}).get("headline") or c.get("hook") or c.get("topic") or "")
               if not isinstance(c.get("hook"), list) else c["hook"][0],
               "hook_pattern": c.get("hook_pattern"), "theme": c.get("theme"), "m": p.get("m", {})}
        posts.append(row)
        for pf, v in row["m"].items():
            a = agg.setdefault(f, {}).setdefault(pf, {"posts": 0, "views": 0, "likes": 0, "comments": 0, "saved": 0, "shares": 0})
            a["posts"] += 1
            a["views"] += v.get(PLATFORM_VIEW.get(pf, "views")) or 0
            a["likes"] += v.get("likes") or v.get("reactions") or 0
            for k in ("comments", "saved", "shares"): a[k] += v.get(k) or 0
    for f in agg.values():
        for a in f.values(): a["avg_views"] = round(a["views"] / a["posts"], 1)
    top = sorted(posts, key=lambda r: -sum((v.get(PLATFORM_VIEW.get(pf, "views")) or 0) for pf, v in r["m"].items()))
    return {"days": days, "channel": m.get("channel"), "updated": m.get("updated"), "by_format": agg,
            "top": [{k: r[k] for k in ("post", "format", "hook", "hook_pattern", "hour")} for r in top[:5]],
            "bottom": [{k: r[k] for k in ("post", "format", "hook", "hook_pattern", "hour")} for r in top[-5:]],
            "posts": posts, "strategy": load()}


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=14); ap.add_argument("--json")
    a = ap.parse_args()
    r = report(a.days)
    if a.json: pathlib.Path(a.json).write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"channel: {json.dumps(r['channel'])}")
    for f, pfs in r["by_format"].items():
        print(f"{f}: " + " | ".join(f"{pf} {a['posts']} posts avg {a['avg_views']} views, {a['likes']} likes, {a['comments']} comments, "
                                    f"{a['saved']} saves, {a['shares']} shares" for pf, a in pfs.items()))
    print("top:", "; ".join(f"{t['format']} {t['post']}" for t in r["top"]))


if __name__ == "__main__":
    main()
