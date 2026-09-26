"""Hook research data for the daily hook-learning job (prompts/hook_learn.md): which opening lines work right now.

Usage:
    python hooks.py [--days 21] [--json out.json]

Prints three ranked lists (all free, official APIs; nothing is posted):
1. Instagram: the opening line (hook) of the recent posts of big AI accounts (sources.json -> tags.ig_accounts, via
   Business Discovery; same cache as tags.py), ranked by engagement relative to the account's size, with the
   account's median so "above its normal" is visible.
2. YouTube: the most-viewed recent AI Shorts titles from the Studio's viral scans (research/<date>_viral.json).
3. Ours: our own posts' hooks (cover headline / clip hook) with their numbers from runs/metrics.json.
"""
import sys, json, re, argparse, pathlib, statistics
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))


def first_line(caption):
    for line in (caption or "").split("\n"):
        line = line.strip()
        if line and not line.startswith("#"): return line[:220]
    return ""


def instagram(days, errors):
    import tags
    posts = tags.ig_posts(tags.env(), errors)
    since = datetime.now(timezone.utc) - timedelta(days=days)
    by_acc = {}
    for p in posts: by_acc.setdefault(p["account"], []).append(p["likes"] + 3 * p["comments"])
    med = {a: statistics.median(v) for a, v in by_acc.items() if v}
    rows = []
    for p in posts:
        try: d = datetime.fromisoformat(p["date"].replace("+0000", "+00:00"))
        except (ValueError, AttributeError, TypeError): continue
        if d < since or not p["likes"]: continue  # 0 likes = likes hidden, not a flop
        eng = p["likes"] + 3 * p["comments"]
        rows.append({"account": p["account"], "type": p["type"], "hook": first_line(p["caption"]), "likes": p["likes"],
                     "comments": p["comments"], "x_median": round(eng / max(1, med.get(p["account"], 1)), 2),
                     "date": p["date"][:10], "link": p["link"]})
    return sorted(rows, key=lambda r: -r["x_median"])


def youtube(days):
    seen, rows = set(), []
    for f in sorted((ROOT / "research").glob("*_viral.json"))[-days:]:
        try: d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError): continue
        for v in d.get("youtube_signal", []):
            if v["id"] in seen: continue
            seen.add(v["id"]); rows.append({"title": v["title"], "views": v["views"], "channel": v.get("channel"), "url": v["url"]})
    return sorted(rows, key=lambda r: -r["views"])


def ours():
    m = json.loads((ROOT / "runs" / "metrics.json").read_text(encoding="utf-8")) if (ROOT / "runs" / "metrics.json").exists() else {}
    rows = []
    for p in m.get("posts", []):
        f = ROOT / "content" / f"{p['post']}.json"
        if not f.exists(): f = ROOT / "content" / "clips" / f"{p['post']}.json"
        try: c = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError): continue
        hook = (c.get("cover") or {}).get("headline") or c.get("hook") or c.get("topic")
        mm = p.get("m", {})
        rows.append({"post": p["post"], "hook": hook, "yt_views": (mm.get("yt_short") or {}).get("views"),
                     "ig": {k: v for k, v in (mm.get("ig_carousel") or mm.get("ig_reel") or {}).items() if k in ("reach", "likes", "saved", "shares", "comments", "views")}})
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=21); ap.add_argument("--json")
    a = ap.parse_args(); errors = []
    res = {"instagram": instagram(a.days, errors), "youtube": youtube(a.days), "ours": ours(), "errors": errors}
    if a.json: pathlib.Path(a.json).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"INSTAGRAM · opening lines of big AI accounts, last {a.days} days, best vs. the account's own median:")
    for r in res["instagram"][:25]:
        print(f"  {r['x_median']:>5}x  @{r['account']} {r['type']} {r['likes']} likes/{r['comments']} com: {r['hook']}")
    print("  ... weakest:"); [print(f"  {r['x_median']:>5}x  @{r['account']}: {r['hook']}") for r in res["instagram"][-5:]]
    print("YOUTUBE · most-viewed recent AI Shorts titles (viral scans):")
    for r in res["youtube"][:20]: print(f"  {r['views'] // 1000:>6}k  {r['title']}")
    print("OURS · our hooks and results:")
    for r in res["ours"]: print(f"  yt {r['yt_views']} · ig {r['ig']} · {r['hook']}")
    for x in errors: print("error:", x)


if __name__ == "__main__":
    main()
