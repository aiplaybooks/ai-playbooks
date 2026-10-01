# Strategy playbook (AI Playbooks)

Read by every writing agent (news/pack writer, hook writer, caption agent, repo writer, scouts) BEFORE writing.
Written every day by the strategy director (prompts/strategy.md) from our numbers (strategy.py) and trend research.
Directives here override older habits, never the fixed rules (verified facts, no fake quotes, credits on clips).

## Current directives (2026-10-01)
- **Aim under 30s on every voiced Reel (news/pack/repo), not 30-40s (2026-10-01, YouTube Shorts ranking research):**
  2026 Shorts ranking moved to watch-time-per-impression with concrete retention thresholds — sub-30s Shorts need
  ~65% retention to get pushed wider, 30-60s Shorts need ~50%; average watch time across all Shorts is now only
  ~16s. Write fewer slides / tighter voice-over lines so the finished voiced Reel lands under 30s instead of
  padding to 30-40s — that's the easier retention bar to clear, and clips (already mostly sub-30s) are our best
  format by a wide margin. Experiment `sub-30s-reel-length` running, see strategy.json.
- **Add a "save this" line, not just a "send this" line (2026-10-01, Instagram ranking research):** saves-per-view
  is now confirmed as its own top-weighted 2026 ranking signal (on top of sends-per-reach and likes-per-reach,
  still true — see below). Every caption/CTA set keeps the one forward-worthy send line but also gives the viewer
  a reason to save (a reference they'll want later: "save this prompt list", "save this before you need it") —
  don't drop the send line, add the save one alongside it.

## Older directives (2026-09-30)
- **Skip-rate discipline, every video format (Instagram's 2026 ranking signal, confirmed by multiple sources
  2026-09-30):** Instagram now measures skip rate — the % who leave in the first 3s — as a direct negative ranking
  signal separate from watch time; under ~20-30% is healthy, over ~40% kills distribution to non-followers. Apply
  to every Reel (clip, news, pack, repo): first frame must read with sound OFF (big on-screen text states the one
  concrete promise, no logo/intro/slow pan), no greeting or setup line before the payoff starts, one visual
  pattern-interrupt (jump-cut, new shot, text change) every 3-4s to keep people from swiping mid-watch. This is
  why clips (already hook-framed, cold-open on the visual) beat carousel Reels: keep pushing carousel Reels toward
  the same cold-open feel — the cover slide's hook headline should be the very first video frame, no branded
  intro pause before it.
- **Sends over likes, still true (2026-09-30, reconfirmed):** watch time, sends-per-reach and likes-per-reach are
  Instagram's 3 named ranking signals; sends/shares are weighted well above likes for reach to non-followers.
  Every caption keeps its one forward-worthy line ("send this to the teammate who still does X by hand"). Also
  confirmed: reposts/near-duplicates get 40-60% less distribution and 10+ reposts/30 days can exclude an account
  from recommendations entirely — our clip hook-frame (own text, own hook, credited) already counts as original
  enough; never post a clip without the hook-frame treatment.
- **Reel length note:** Instagram is now recommending Reels up to 3 minutes to non-followers (was capped near 90s
  push before). Our clips and carousel Reels are short (well under that); no change needed yet, but don't assume
  a hard 60-90s ceiling on future longer-form ideas.
- **YouTube Shorts favors human-originality signals (2026-09-30):** YouTube's 2026 algorithm now discounts
  template-driven/AI-flooded content and rewards watch-through-on-first-loop; AI content also gets an on-video
  label when detected. Our Shorts are voiced + captioned + narratively structured (not a raw AI-tool screen
  recording), which should read as edited/original — keep the voice-over and captions on every YouTube Short,
  don't strip them to save render time.

## Still-standing directives
- Repo posts: the "Comment WORD → DM" CTA got 8 comments on the first repo post: keep it on every repo post.
- Carousels: their voiced video also goes out as IG Reel + FB Reel. Write the carousel so the VIDEO works:
  a result-first cover (what the viewer gets), one idea per slide, voice-over lines that hook in the first 2s,
  captions that fit the Reel too (no "swipe", no "slide 3") — now sharpened by the skip-rate directive above:
  that cover/hook must BE the first frame, no intro pause first.

## Running experiments
See strategy.json `experiments`. `carousel-video-reels`, `skip-fb-photos`, `clip-heavy-mix` (started 2026-09-29)
all closed **won** today with numbers (see Learned below) and are kept as permanent settings. New:
`hook-skip-rate-discipline` (started 2026-09-30) — re-evaluate after ~10 posts under the new hook rule (~1 week).

## Learned (won / lost, with numbers)
- **2026-09-30 — clip-heavy mix: WON.** 14-day report, clips now n=18/platform: clip avg views beat news/pack by
  5-25x on every platform (yt_short 579.6 vs 153.3/24.8; ig_reel 214.9 vs 35.0/5.7; fb_reel 148.1 vs 41.6/132.7).
  Kept the 3 clip : 1 news : 1 repo : 1 pack autopilot mix.
- **2026-09-30 — carousel Reels + skip-fb-photos: WON.** News/pack carousels posted as IG/FB Reels now average
  35-133 views vs 0-2 for the old carousel-only posts, and FB Reels alone beat FB photo posts' flat 0. Both
  changes kept permanently.

## Log
- 2026-09-29: seeded by Claude Code from the 7-day report: clip-heavy mix, carousel videos as Reels, FB photo posts
  off for news/packs.
- 2026-09-29 (2nd pass, strategy director): too early to evaluate the 3 running experiments same-day; added
  DM-sends-weighting and DevDay-priority directives from trend research; clip hunt came up empty (no live X
  browsing tool that session).
- 2026-10-01 (strategy director): 14-day report — clip format still dominant (ig_reel 206.8 / fb_reel 150.8 avg
  views, n=19 each), mix stays 3:1:1:1. Repo Reels look strong (134/494 avg views) but n=2, too early; repo
  fb_photos sits at 0 (n=3) but under the 5-post bar to act on, left alone. No per-hour data yet to justify moving
  post_slots. `xscout.py` worked (40 video posts scanned) — picked 4 fresh clips into
  `research/clips/2026-10-01_clips.json` (Grace_AI_ forest story, TheAIColony AI lifebuoy, bcherny's Sonnet 5.5
  Claude Code demo, OpenAIDevs Codex-keeps-working); skipped official-brand launch clips (redundant with our own
  news posts), a Megan Fox AI-LoRA deepfake (real-person likeness risk), and political/state-media posts. 7 web
  searches (faceless AI Reels formats, Instagram algorithm changes, GitHub-repo X engagement, YouTube Shorts
  algorithm, AI money-prompt Reels) surfaced two concrete, numbered findings worth acting on: YouTube Shorts 2026
  retention thresholds (65% sub-30s vs 50% 30-60s, avg watch now ~16s) → new sub-30s Reel-length directive; saves-
  per-view confirmed as its own 2026 IG ranking signal → new save-CTA directive. Checked `hook-skip-rate-discipline`
  (started 2026-09-30): the actual cold-open code change is still an unbuilt backlog item, so the experiment can't
  be fairly judged yet — left running with a note, not closed.
- 2026-09-30 (strategy director): ran `python xscout.py` successfully (headless X login worked this time, 43
  video posts scanned) — picked 6 fresh clips into `research/clips/2026-09-30_clips.json`. 14-day report closed
  all 3 running experiments as won (numbers above) and kept every change. Trend research (7 searches: Instagram
  skip-rate/algorithm 2026, faceless AI-news formats, YouTube Shorts originality rules) added the skip-rate
  discipline directive (new experiment, running) and a YouTube-originality note. Left `mix` and `post_slots`
  unchanged — no per-hour data yet to justify a slot change, and 3 experiment closes + 1 new directive is enough
  change for one day. Did not touch the open `strategy/backlog.md` items (X metrics, X thread format, TikTok
  metrics, outlier-based clip picking, fresh learn-job data) — those need code and are for the next Claude Code
  session, not this data/direction pass.

- 2026-10-01 (owner, 7-day review: 26.8K views, 65% from YouTube Shorts, 75% of those from clips): clips are the growth
  format: pick the visual transformation/comparison kind, write the hook about what the eye sees in the first second.
  Prompt packs are out of the autopilot rotation (video avg 29 YT / 10 IG); when one runs it is for followers
  ("Comment WORD"), not for views.
