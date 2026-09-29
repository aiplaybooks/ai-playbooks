# Strategy backlog (production changes that need code)

Written by the daily strategy director (prompts/strategy.md), built by Claude Code in its next session (the
session-start hook prints the open items). Mark done items `- [x] ... (commit <hash>)`.

- [x] 2026-09-29 GitHub repo Reels: a 10-15 s screen recording scrolling the repo page (Playwright video) with the hook (commit 5c20bb8)
  on top + music, published as IG/FB Reel next to the photo post — why: Reels are our only format that reaches
  non-followers (clips 220 IG avg vs photo 16) — expected: repo posts reach 100+ views
- [ ] 2026-09-29 X metrics: views/likes/reposts of our X posts (GET /2/tweets?ids=..&tweet.fields=public_metrics, ~$0.005 per read: batch up to 100 ids in ONE call, max 1x/day) into metrics.py + strategy.py — why: X went live 2026-09-29, the director needs its numbers — effect: X can be judged/skipped like the other platforms
