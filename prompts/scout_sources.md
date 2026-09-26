
## Source upkeep (REQUIRED in this gather: do it FIRST, before the news search)
`sources.json` feeds news.py. Keep it healthy and growing, so we hear about news before other pages:
1. Read `research/source_health.json` (per source: ok/fail streaks, last error, newest item). A source with
   `fail_streak` >= 3, or whose `newest` item is older than 30 days: find its current feed/page (web search), test it
   with `python news.py --check <url> --parser feed` (or `anthropic_news` / `dated_sections` for pages) and fix the url
   in sources.json. If it's gone for good, set `"disabled": true` and a `"why"`.
2. Find 1-3 NEW sources that would have brought us news earlier: official blogs / changelogs / release notes / RSS of
   the tools on the list and of big new AI tools people use, GitHub releases feeds (`https://github.com/<org>/<repo>/releases.atom`)
   of popular AI apps and CLIs, high-signal AI newsletters and news sites. Look for the feed URL (/rss, /feed,
   /atom.xml, /index.xml, /feed.xml), test it with `python news.py --check <url>`, and add only sources that pass
   (dated items, recent) to `"feeds"`:
   `{{"name": "...", "url": "...", "tier": "official" | "signal", "added": "{date}", "by": "scout", "why": "one line"}}`
   `official` only for the vendor's own domain or repo; everything else `signal`. Optional `"match"` (regex on
   title+summary) for broad feeds so only AI items come in. Sites that block scripts go to `"manual"` with a `"why"`.
3. Never add duplicates (same url or same site already there). Keep sources.json valid JSON, 2-space indent.
4. Test **at least 3 candidate sources** with `news.py --check` every day, even when all current sources are healthy
   (growth is the point). List every source you added, fixed, disabled AND the ones you tested but rejected (with the
   reason) in the output's `sources_changed` (Turkish, one short line each). An empty list is not allowed.
