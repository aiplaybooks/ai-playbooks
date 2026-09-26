"""Daily news collector: pulls the last N hours from the sources in sources.json (no AI, no API keys).

Usage:
    python news.py [--hours 36] [--date 2026-09-24]

Output: research/YYYY-MM-DD.json  {"generated", "hours", "items": [...], "errors": [...], "manual": [...]}
Each item: source, tier (official | signal | community), title, url, date (UTC ISO), summary.
This is the candidate list for the daily run. Only `official` items can back a factual claim; `signal` and
`community` (Hacker News) items are hints that must be verified against an official source. `manual` lists
sources that block scripts and have to be checked with web search.
"""
import sys, json, re, html, gzip, time, pathlib, argparse, email.utils, urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).parent.resolve()
UA = {"User-Agent": "Mozilla/5.0 (AI Playbooks news collector)"}
MONTHS = "Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?"
ATOM = "{http://www.w3.org/2005/Atom}"


def get(url):
    for attempt in (1, 2):  # one retry: some sites answer 400/5xx now and then
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
                b = r.read()
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt == 2: raise
            time.sleep(3)
    if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)  # some servers gzip even when not asked
    return b.decode("utf-8", "replace")


def text(s, n=400):
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or "")); s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def parse_date(s):
    s = (s or "").strip()
    if not s: return None
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try: d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError: return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def feed(src):
    root = ET.fromstring(get(src["url"]).encode("utf-8"))
    out = []
    for it in root.iter("item"):  # RSS
        out.append((it.findtext("title"), it.findtext("link"), it.findtext("pubDate"), it.findtext("description")))
    for it in root.iter(ATOM + "entry"):  # Atom
        link = it.find(ATOM + "link[@rel='alternate']")  # (Elements without children are falsy: no `or` here)
        if link is None: link = it.find(ATOM + "link")
        out.append((it.findtext(ATOM + "title"), link.get("href") if link is not None else "",
                    it.findtext(ATOM + "published") or it.findtext(ATOM + "updated"),
                    it.findtext(ATOM + "content") or it.findtext(ATOM + "summary")))
    return [{"title": text(t, 200), "url": (u or "").strip(), "date": parse_date(d), "summary": text(s)} for t, u, d, s in out]


def anthropic_news(src):
    h = get(src["url"]); out, seen = [], set()
    for m in re.finditer(r'href="(/news/[a-z0-9-]+)"[^>]*>(.{0,1500})', h, re.S):
        if m.group(1) in seen: continue
        seen.add(m.group(1))
        parts = [p for p in (text(x, 300) for x in re.split(r"<[^>]+>", m.group(2))) if p]
        date = next((parse_date(p) or _mdy(p) for p in parts[:3] if _mdy(p)), None)
        title = next((p for p in parts[1:5] if len(p) > 25), parts[0] if parts else m.group(1))
        out.append({"title": title, "url": "https://www.anthropic.com" + m.group(1), "date": date, "summary": ""})
    return out


def _mdy(s):
    s = re.sub(r"(\d)(st|nd|rd|th)", r"\1", s.strip()).replace("Sept ", "Sep ").replace(".", "")
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%b %d %Y", "%B %d %Y", "%Y-%m-%d"):
        try: return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError: pass
    return None


def dated_sections(src):
    """Changelog pages: split the page text at dates ('Sep 22, 2026', 'September 22 2026', '2026-09-22').
    Sections with the same date are merged; future dates (deprecation/shutdown notices) are dropped in main()."""
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", get(src["url"]), flags=re.S)
    h = re.sub(r"Last updated \d{4}-\d\d-\d\d UTC", " ", h)  # page footer, not a changelog entry
    pat = re.compile(rf"(\b(?:{MONTHS})\.? \d{{1,2}}(?:st|nd|rd|th)?,? 20\d\d\b|\b20\d\d-\d\d-\d\d\b)")
    bits = pat.split(text(h, 10 ** 7)); days = {}
    for i in range(1, len(bits) - 1, 2):
        d = _mdy(bits[i])
        if d: days.setdefault(d, []).append(bits[i + 1].strip())
    return [{"title": f"{src['name']}: {d:%b %d, %Y}", "url": src["url"], "date": d, "summary": text(" … ".join(b), 900)}
            for d, b in days.items()]


def hacker_news(cfg, since):
    out, seen = [], set()
    for q in cfg["queries"]:
        url = ("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
            {"query": q, "tags": "story", "numericFilters": f"created_at_i>{int(since.timestamp())},points>={cfg['min_points']}"}))
        for h in json.loads(get(url))["hits"]:
            if h["objectID"] in seen: continue
            seen.add(h["objectID"])
            out.append({"source": "Hacker News", "tier": "community", "title": h["title"],
                        "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
                        "date": datetime.fromtimestamp(h["created_at_i"], timezone.utc),
                        "summary": f"{h['points']} points, {h.get('num_comments', 0)} comments · "
                                   f"https://news.ycombinator.com/item?id={h['objectID']}"})
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace"); sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=36); ap.add_argument("--date")
    ap.add_argument("--check", metavar="URL", help="test one candidate source (the scout uses this before adding it)")
    ap.add_argument("--parser", default="feed", help="with --check: feed | anthropic_news | dated_sections")
    a = ap.parse_args()
    now = datetime.now(timezone.utc); since = now - timedelta(hours=a.hours)
    if a.check:
        try: got = globals()[a.parser]({"url": a.check, "name": "check"})
        except Exception as ex: sys.exit(f"FAIL: {type(ex).__name__}: {ex}")
        dated = sorted((i for i in got if i["date"]), key=lambda i: i["date"], reverse=True)
        print(f"{len(got)} items, {len(dated)} with a date; newest:")
        for i in dated[:5]: print(f"  {i['date']:%Y-%m-%d}  {i['title']}  {i['url']}")
        sys.exit(0 if dated else "FAIL: no dated items (wrong parser or not a feed)")
    cfg = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    items, errors = [], []
    hfile = ROOT / "research" / "source_health.json"  # per source: streaks + last result, for the scout's upkeep
    try: health = json.loads(hfile.read_text(encoding="utf-8"))
    except (OSError, ValueError): health = {}

    jobs = [(s, feed) for s in cfg["feeds"] if not s.get("disabled")] + \
           [(s, globals()[s["parser"]]) for s in cfg["pages"] if not s.get("disabled")]
    for src, fn in jobs:
        h = health.setdefault(src["name"], {"ok_streak": 0, "fail_streak": 0})
        try:
            got = fn(src)
            h.update(ok_streak=h["ok_streak"] + 1, fail_streak=0, last_ok=now.isoformat(timespec="minutes"),
                     last_items=len(got), newest=max((i["date"] for i in got if i["date"]), default=None) and
                     max(i["date"] for i in got if i["date"]).isoformat(timespec="minutes"))
            for it in got:
                if src.get("skip") and re.search(src["skip"], it["title"]): continue
                if src.get("match") and not re.search(src["match"], it["title"] + " " + it["summary"]): continue
                if it["date"] and it["date"] > now + timedelta(days=1): continue
                # pages that only give a day (no time) count as midnight UTC: keep the whole day
                if it["date"] and it["date"] >= since - (timedelta(days=1) if fn in (anthropic_news, dated_sections) else timedelta(0)):
                    items.append({"source": src["name"], "tier": src["tier"], **it})
        except Exception as ex:  # one broken source must not stop the run
            errors.append(f"{src['name']}: {type(ex).__name__}: {ex}")
            h.update(ok_streak=0, fail_streak=h["fail_streak"] + 1, last_error=f"{type(ex).__name__}: {ex}"[:200],
                     last_fail=now.isoformat(timespec="minutes"))
    hfile.parent.mkdir(exist_ok=True); hfile.write_text(json.dumps(health, indent=1, ensure_ascii=False), encoding="utf-8")
    try:
        items += hacker_news(cfg["hn"], since)
    except Exception as ex:
        errors.append(f"Hacker News: {type(ex).__name__}: {ex}")

    rank = {"official": 0, "signal": 1, "community": 2}
    items.sort(key=lambda x: (rank[x["tier"]], -x["date"].timestamp()))
    for it in items: it["date"] = it["date"].isoformat(timespec="minutes")
    day = a.date or now.astimezone().strftime("%Y-%m-%d")
    out = ROOT / "research" / f"{day}.json"; out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"generated": now.isoformat(timespec="minutes"), "hours": a.hours, "items": items,
                               "errors": errors, "manual": cfg["manual"]}, indent=1, ensure_ascii=False), encoding="utf-8")
    for it in items:
        print(f"[{it['tier'][:4]}] {it['date'][:16]}  {it['source']}: {it['title']}")
    for e in errors: print("ERROR", e, file=sys.stderr)
    print(f"{len(items)} items, {len(errors)} errors -> {out}")


if __name__ == "__main__":
    main()
