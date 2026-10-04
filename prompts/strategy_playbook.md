# Strategy playbook (AI Playbooks)

Read by every writing agent (news/pack writer, hook writer, caption agent, repo writer, scouts) BEFORE writing.
Written every day by the strategy director (prompts/strategy.md) from our numbers (strategy.py) and trend research.
Directives here override older habits, never the fixed rules (verified facts, no fake quotes, credits on clips).

## Current directives (2026-10-03)
- **Clips: say OUR take, don't describe the screen (2026-10-03, YouTube's Shorts originality update of 2026-10-01,
  https://ppc.land/re-uploaded-shorts-lose-reach-as-youtube-favours-original-clips/):** YouTube now shows less of
  "channels primarily aggregating or re-uploading other creators' videos" in the Shorts feed; template edits and
  narrating what's on screen don't count, "your own voice, storytelling or point of view" does. Meta has the same rule
  since March 2026. So every clip hook states a take: what it means, what the viewer can do with it, or a stance
  ("Kids dreamed of these games for 20 years. AI hackers built them in a weekend.") — never a caption of the visible
  action ("A robot flies through a forest"). The YouTube description starts with 2-3 lines of our own analysis
  (why it matters / which tool / what to try), then the credit. Experiment `clip-own-take`.
- **Clips: no slow narrative AI short films (2026-10-03, data):** AI story films (dragon love story, forest heartbeat,
  pottery village) got 31 / 3 / 49 YouTube views — avg 28 vs 586 for all clips (20x gap), IG 113-134 vs 191. Pick
  transformations, before/after reveals, AI models competing on one task, "built X in N minutes" demos, action/fight
  scenes and robots doing something physical (our winners: teddy bear → soldier 4,979; product launch animation
  2,326; 5 models design a bridge 1,422; kung-fu fight 1,276). Experiment `no-ai-film-story-clips`.
- **News/pack posts: Instagram gets the Reel only (2026-10-03, data):** IG carousels averaged 0.8 (news, n=20) and 1.2
  (pack, n=14) views; the Reel of the same post gets 55 (news). `ig_carousel` is skipped in the post flow. Write the
  slides for the VIDEO first (they still render the Reel, YouTube Short and TikTok). Experiment `skip-ig-carousel`.

## Directives (2026-10-02)
- **Repo posts drop fb_photos (2026-10-02, data):** repo ig_photo keeps running (it's the comment-to-DM funnel, not a
  views play) but repo fb_photos is off, matching the already-closed post-flow skip: fb_photos now sits at exactly
  0.0 avg views across news (16 posts), pack (9 posts) and repo (4 posts) — 29 posts combined, the same dead format
  everywhere. fb_reel already carries repo's FB views (448.7 avg, n=3). Experiment `skip-repo-fb-photos` running.
- **Keep hooks raw, not polished (2026-10-02, Instagram's year-end memo):** Instagram's Dec 2025 policy memo
  explicitly said the "polished, perfect aesthetic" is dead for 2026 and committed to favoring raw, real, human-
  sounding content over AI-generated/template content. Our carousels/reels are code-rendered templates by design
  (that doesn't change), but the WORDS on them should read like a person talking, not a brand announcement: hooks
  and voice-over lines use first-person/direct-address phrasing ("I just found...", "you can now...", "watch what
  happens") over neutral announcement phrasing ("X company launches Y feature"). This is a wording note for every
  writer, not a visual-design change — no experiment to track (can't isolate it from other changes), just apply it.

## Still-standing directives
- Repo posts: the "Comment WORD → DM" CTA got 8 comments on the first repo post: keep it on every repo post.
- Carousels: their voiced video also goes out as IG Reel + FB Reel. Write the carousel so the VIDEO works:
  a result-first cover (what the viewer gets), one idea per slide, voice-over lines that hook in the first 2s,
  captions that fit the Reel too (no "swipe", no "slide 3") — now sharpened by the skip-rate directive above:
  that cover/hook must BE the first frame, no intro pause first.

## Running experiments
See strategy.json `experiments`. `carousel-video-reels`, `skip-fb-photos`, `clip-heavy-mix` (started 2026-09-29)
all closed **won** today with numbers (see Learned below) and are kept as permanent settings.
Running: `hook-skip-rate-discipline` (2026-09-30, still blocked on the unbuilt cold-open backlog item), `sub-30s-
reel-length` (2026-10-01, needs 8 posts), `packs-out-of-rotation` (2026-10-01, don't revisit before 2026-10-06),
`skip-repo-fb-photos` (2026-10-02, no repo post since), `skip-ig-carousel`, `no-ai-film-story-clips`,
`clip-own-take` (all 2026-10-03).

## Learned (won / lost, with numbers)
- **2026-09-30 — clip-heavy mix: WON.** 14-day report, clips now n=18/platform: clip avg views beat news/pack by
  5-25x on every platform (yt_short 579.6 vs 153.3/24.8; ig_reel 214.9 vs 35.0/5.7; fb_reel 148.1 vs 41.6/132.7).
  Kept the 3 clip : 1 news : 1 repo : 1 pack autopilot mix.
- **2026-09-30 — carousel Reels + skip-fb-photos: WON.** News/pack carousels posted as IG/FB Reels now average
  35-133 views vs 0-2 for the old carousel-only posts, and FB Reels alone beat FB photo posts' flat 0. Both
  changes kept permanently.

## Log
  descriptions carry our own take after YouTube's 2026-10-01 Shorts originality update (re-upload channels lose
  Shorts-feed reach; Meta has the same rule since 2026-03). Backlog: voiced "our take" card on clip Shorts. xscout
  worked (35 video posts): 6 clips into `research/clips/2026-10-03_clips.json` (AI game mashup montage 19K likes/4M,
  flying humanoid robots, Seedance 2.5 effect, AI superhero fight, Eleven v4 "what AI voices can't do" ad, a 497K-view
  realism clip); skipped official-brand launches (OpenAI dots, Ideogram, Grok, Boston Dynamics hands → news
  territory), politics (Harris, PressTV, Hannity, Fadnavis), drama/celebrity posts. Other searches: Instagram 2026
  (completion > shares/saves > likes, smaller accounts boosted, harder on watermarked reposts), small-account Reels
  reach 134 vs carousel 56 median (contentdrips/collabkit 2026 studies), Kling 4.0 (30 s) launching in October.
