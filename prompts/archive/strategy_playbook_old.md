

<!-- archived 2026-10-04 -->
## Older directives (2026-10-01)
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


## Log (older)
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
- 2026-10-02 (strategy director, 14-day report): clip dominance reconfirmed again (yt_short 626.5 / ig_reel 201.3 /
  fb_reel 179.4 avg views vs news/pack/repo all under 135 everywhere) — mix stays 4 clip : 1 news : 1 repo, packs
  stay out per the owner's 2026-10-06 hold. New data point: repo fb_photos now has its own 4-post sample at exactly
  0.0 avg views, joining news (16 posts) and pack (9 posts) at the same dead number — 29 posts combined all at zero
  — so repo fb_photos is off now too (`skip-repo-fb-photos`, repo ig_photo keeps running, it's the comment funnel,
  not a views play). Repo ig_reel (132.3) and fb_reel (448.7) still look very strong but n=3, watching not acting
  further yet. `sub-30s-reel-length` and `packs-out-of-rotation` both too early to judge; `hook-skip-rate-discipline`
  still blocked on the same unbuilt cold-open backlog item (now 3 days open, flagged again). `python xscout.py`
  worked (42 video posts scanned) — picked 5 fresh clips into `research/clips/2026-10-02_clips.json`: Tavus' Griffin
  "video Turing test" clip (27K likes/10M views, the single biggest number seen in any scout so far), a Metal Gear
  Solid skateboarding mashup (same AI-hackers-in-classic-game format as yesterday's Call of Duty clip which got our
  best share count of the week, different game so not a repeat), an "is this AI or real" reveal, a full AI-made TV
  episode scene, and an AI-illustrated physics-lecture clip; skipped official-brand launch clips (OpenAI dots/Codex/
  GPT-6.1 — redundant with our own news posts) and every political/state-media post (DeSantis, Trump, PressTV, the
  Congress-bot story, the US/Israel LEGO video). 3 web searches (Instagram Reels ranking changes, YouTube Shorts
  retention update, viral AI video trends) reconfirmed skip-rate and watch-time as 2026's top IG ranking factors
  (nothing new to act on beyond the existing directive) but surfaced one fresh, sourced finding: Instagram's Dec
  2025 memo explicitly de-prioritizes "polished, perfect aesthetic" content in favor of raw/real-sounding posts for
  2026 — added as a wording directive (first-person/direct-address hooks over announcement-style phrasing) rather
  than a formal experiment, since it can't be isolated from other changes. `post_slots` left unchanged, no per-hour
  data yet.
- 2026-10-03 (strategy director, 14-day report): clips still lead everywhere (yt_short 586.0 / ig_reel 191.4 /
  fb_reel 166.5, n=25) vs news (204.0 / 55.0 / 93.6) — mix stays 4 clip : 1 news : 1 repo, packs out until
  2026-10-06. Clip YouTube views are hit-driven and the last 7 clips averaged ~150 (Oct 1-2: 386, 31, 52, 3, 375,
  146) vs the 9-27/29 hits; the AI-film-story clips are the floor (avg 28). 3 changes: (1) `ig_carousel` skipped in
  the post flow (34 carousels at ~1 view; the Reel carries IG); (2) no slow AI short-film clips; (3) clip hooks + YT
