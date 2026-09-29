# Strategy backlog (production changes that need code)

Written by the daily strategy director (prompts/strategy.md), built by Claude Code in its next session (the
session-start hook prints the open items). Mark done items `- [x] ... (commit <hash>)`.

- [x] 2026-09-29 GitHub repo Reels: a 10-15 s screen recording scrolling the repo page (Playwright video) with the hook (commit 5c20bb8)
  on top + music, published as IG/FB Reel next to the photo post — why: Reels are our only format that reaches
  non-followers (clips 220 IG avg vs photo 16) — expected: repo posts reach 100+ views
- [ ] 2026-09-29 X metrics: views/likes/reposts of our X posts (GET /2/tweets?ids=..&tweet.fields=public_metrics, ~$0.005 per read: batch up to 100 ids in ONE call, max 1x/day) into metrics.py + strategy.py — why: X went live 2026-09-29, the director needs its numbers — effect: X can be judged/skipped like the other platforms
- [ ] 2026-09-29 X thread format: after x_post, 2-4 link-free self-replies (what it does / setup / why FR££ matters / "Follow @AIPlaybooks_") at $0.015 each; the link-in-first-reply variant costs $0.20 per reply (~+$4/month for 1 repo a day): turn it on only when X numbers (after 1-2 weeks) justify it — why: big AI/GitHub accounts on X put links in the first reply and use threads — effect: more replies/bookmarks, profile visits
- [ ] 2026-09-29 TikTok metrics: video.list (free, scope granted) into metrics.py + strategy.py — note: right after the first post (a PHOTO post, published from an inbox draft) /v2/video/list/ returned 0 items: recheck after a few hours; if photo posts never show up there, match our TikTok posts another way — why: the director must judge TikTok like the other platforms — effect: TikTok formats get tuned by data
