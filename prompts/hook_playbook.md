# Hook playbook (AI Playbooks)

What makes people stop scrolling, right now. Read by: the hook writer (clip Reels, prompts/hook.md), the writer (the
carousel's `cover.headline`, prompts/write.md) and the caption agent (the caption's first line). Updated every day by
the hook-learning job (prompts/hook_learn.md) from real numbers: big AI accounts' posts (hooks.py), trending Shorts,
web research, and our own results. Keep it short: the best ~12 live patterns, each with proof.

## Rules that don't change
- A hook is one idea, 6-22 words, readable in 2 seconds. Concrete nouns, numbers, names. No filler ("In this post").
- It must match what the media shows (a hook that lies about the clip/carousel kills retention and trust).
- News facts (what launched, versions, dates) must be true. Bold result/money promises are allowed (owner's rule).
- Don't reuse the exact wording of another account's hook: take the pattern, write our own line.
- Vary the pattern: don't use the same pattern as our last 3 posts (check `content/` hooks).

## Live patterns (updated 2026-09-29)
Each: template · example (ours) · proof (data line: account, engagement vs. the account's median).

1. **Comment-keyword DM** · "Comment "[WORD]" and I'll send you [the full thing]." · "Comment AGENT and I'll send you
   the 7 prompts." · proof: @theaifield 364.46x its median (2,875 comments, 2026-09-29 scan; was 255.6x/274x — still
   climbing), @godofprompt 13.05x / 11.48x (2,000+ comments). Use when we really deliver (the post has a
   `dm.keyword`: our bot DMs the page). Best for packs. Vary it: "Comment X, I'll send you the link" / "Comment X to
   learn how, we'll DM you" / "Want it? Comment X".
2. **Big number + insider move** · "[Person/company] just [did something surprising] [$ figure]" · "Claude Opus 5.5
   designed a LEGO duck from real parts, then wrote a 141-page instruction booklet for it" · proof: @theaifield
   90.14x (Higgsfield CEO $5.4B open-source, 2026-09-29 scan; was 61.63x) — the same line reappeared 3x in this
   scan's top results, the most repeat-surfacing hook we've tracked; still our best IG-clip performer (220 views/1
   like, hooks.py OURS). Use for news with a figure or a person's surprising move.
3. **Time-lapse shock** · "[Short time]. That's all it took for [thing] to [change completely]." · proof:
   @theaifield 56.0x, @airesearches 53.51x (same line, both accounts, 2026-09-29 scan; was 47.59x/38.72x) — also
   now proven in our OWN data: "30 minutes. That's all it took to build this whole product launch animation with
   Claude Opus 5.5 and After Effects" pulled 1,416 YT Short views / 176 IG views (hooks.py OURS, 2026-09-29), our
   #2 all-time performer. Use for "then vs. now" AI clips and speed-of-build stories.
4. **Short punchy statement** (under 8 words, period) · "OpenAI waited just 90 minutes." / "Peak internet." / "meta
   just made VR look wearable." · proof: @chatgptricks 10.18x-14.78x across four separate posts this scan. Use for
   news with one striking fact.
5. **"AI is starting to [pay/save you] real money"** · "AI agents are starting to save people real money." · proof:
   @chatgptricks 21x (2026-09-26), 11.97x on a repeat post (2026-09-27) — still clearing the bar two scans running.
   Use for money packs / agent stories.
6. **What-if question** · "What if you could [impossible thing]?" · proof: @chatgptricks 27.6x/14.4x (2026-09-26),
   15.64x "What if AI takes humanity beyond Earth?" (2026-09-27). Use for imaginative AI video clips.
7. **Breaking-update alert** · "🚨 [Company] is rolling out [update] today, [biggest in years]." · proof: @theaifield
   56.95x on the iOS 27 rollout line (2026-09-29 scan; was 39.78x/20.28x). Use for a big consumer update (phone,
   app) on launch day.
8. **Division / debate** · "[Topic] has divided [group], and both sides have a point." · proof: @chatgptricks 26x
   (2026-09-26), 14.66x on a repeat post (2026-09-27). Use to drive comments on controversial AI topics.
9. **Secret reveal** · "[Someone] is secretly [doing a surprising thing], and [the twist]." — shows a normal scene,
   then flips it in the same sentence · "This guy is secretly puppeteering the AI woman on screen, and she mirrors
   his every move in real time." · proof: our own current best performer across both platforms (hooks.py OURS,
   2026-09-27): 162 YouTube Short views and 169 IG views/1 save — the top line of all our posts to date. Use for
   AI-avatar/deepfake-style clips where the twist is visual.
10. **Curiosity gap / open loop** · "[Someone/something] is [doing a specific thing] to [solve/answer] [a named
    mystery]." — states a concrete situation but hides the result, so the viewer must watch to close the loop ·
    "A developer ran Claude Code nonstop for 30 days to see how much of his job it could actually replace." ·
    proof: @rowancheung 77.03x its median ("A startup is using artificial intelligence to investigate one of
    science's oldest problems: why the same experiment can work in one lab and fail in another" — 80,002 likes,
    2026-09-29 scan; was 82.73x/76.36x on earlier scans) — a fresh example line clearing the same bar, so the
    pattern (not just one post) is what's working; also top-tier in the 2026 HookMafia/Socialync testing. 2026-09-29
    web research adds a refinement worth applying: specific curiosity beats broad ("this posting habit quietly
    killed my reach" > "you won't believe this trick") — no dedicated AI-niche proof yet, treat as a phrasing note,
    not a new pattern. Use for news/investigation-style stories, don't reveal the punchline in the hook.
11. **Identity call** · "If you [use/do a specific thing], this is for you." — names the exact audience in one line,
    keep it under ~12 words · "If you're still copy-pasting into ChatGPT one tab at a time, this is for you." ·
    proof: 2026 short-form hook testing scored Identity Call highest of 30 tested patterns (~85/100 vs. next-best
    Contrarian Strike/Open Loop, both >70; generic openers like "Hey guys" scored <30) — HookMafia/Socialync, Sep 2026.
    Use for prompt packs and tool-specific tips.
12. **Contrarian strike** · "Stop [doing the common thing]." — a flat command, no explanation yet · "Stop typing your
    prompts from scratch every time." · proof: same 2026 testing (one of only 4 patterns to clear the 70-score bar;
    negative framings beat positive by 1.3-1.8x) plus a fresh match this scan, @chatgptips 10.88x "Stop asking
    ChatGPT vague things like..." Use for tips/prompt packs.

## GitHub repo hooks (caption openers for repo posts; the learning job keeps these current)
Seeded 2026-09-28 from the owner's 4 reference posts (big AI pages, 100+ reactions each). Proof gets refreshed with
engagement numbers by the learning job.
1. **CAPS discovery** · "I JUST FOUND A GITHUB REPO THAT [turns X into Y]." + staccato benefits ("No tabs. No context
   switching.") + "It's 100% FR££ and open source." + "It's called [Name]." · for tools that give a new ability
   (agents, workflows). Proof: owner reference (Collaborator post, 141 reactions, 53 shares).
2. **Solo-dev vs. paid giant** · "🚨A solo dev just open sourced a FR££ [paid tool] replacement that [runs on your
   machine]." + a verified versus-number ("646 languages versus [tool]'s 32") + "No [cost]." lines + star proof ·
   for `alternative` repos. Proof: owner reference (VoiceStudio post).
3. **Numbered FR££ course** · "The FR££ course includes [N lectures] and [N projects] teaching how to [outcome]." ·
   for `learning` repos. Proof: owner reference (learn-harness-engineering post).
4. **Must-save + big name** · "🚨 This is an absolute must save resource" / "[Big company] open sourced [thing]" +
   "Extremely useful" · for official releases by a big company. Proof: owner reference (openai/skills post).

## Trial patterns (unproven: from pattern libraries, being tested; max 4, 14 days each)
Writers may use a trial pattern when it fits the topic better than a live one; set `hook_pattern` to "trial: <name>"
so the learning job can compare its results. (None yet: the learning job adds them from research/hooks/.)

## Weak patterns (data says avoid)
- Long explanatory first sentences (> 25 words) that describe a product like a press release ("X is an AI-powered
  platform that enables anyone to ..."): bottom of the ranking.
- Spec lists in the hook ("weighs 100 grams, less than a fifth of ..."): the numbers belong in the carousel.
- "Real or AI?" (ask the viewer to guess): retired 2026-09-26 — never had a proof line in three rounds of hooks.py
  data; the curiosity-gap pattern (#10 above) covers the same "make them look twice" goal with real numbers behind it.
- **"Most people use X wrong"** (retired 2026-09-27): never picked up a proof line in any hooks.py scan since it was
  added 2026-09-26 — only a single reference example (@chatgptips's "1 billion users" cover), no engagement number
  behind it. It overlaps with #11 Identity call for the same "name the audience" goal on tool-tip/pack hooks, which
  does have real testing data. Reuse #11 or #12 instead; readd only if a real proof line shows up.

## Our results (from runs/metrics.json + hooks.py OURS; the learning job fills this in)
- New leader this scan (hooks.py, 2026-09-29, ~40 posts now): "A guy hugging his teddy bear at home just became a
  soldier saving his friend in war, and the performance never changed" (pattern #9 Secret reveal) — 1,426 YT Short
  views, 1,640 IG views/1,227 reach/19 likes — our best line on both platforms by a wide margin, more than 8x the
  previous leader. Confirms #9 as our strongest pattern with a second, much bigger data point. 2) "30 minutes.
  That's all it took to build this whole product launch animation with Claude Opus 5.5 and After Effects" (pattern
  #3 Time-lapse shock) — 1,416 YT views/176 IG views/3 saves — first own-data proof for #3. 3) "Claude Opus 5.5
  designed a LEGO duck... 141-page instruction booklet" (pattern #2) — 222 IG views/1 like, still our best IG-only
  carousel-adjacent clip.
- Carousel (`kind: carousel`) posts specifically are still not getting IG traction this scan (most show 0 IG
  views/likes regardless of hook pattern) — sample too thin to rank carousel hooks against each other yet; the
  signal we do have all comes from clips. Re-check once carousels start reaching more accounts.
- Packs with a `dm.keyword` comment CTA (pattern #1) haven't shown views/comments yet in our own data (DM bot
  setting is still OFF per CLAUDE.md, so the loop isn't live) — re-check once it's turned on.

## Log
- 2026-09-26: first version from hooks.py (12 AI accounts, last 21 days).
- 2026-09-26: added #11 Identity call and #12 Contrarian strike from 2026 short-form hook testing (HookMafia/
  Socialync) — both cleared the 70-score bar and negative framing beat positive by 1.3-1.8x; filled in "Our results"
  with early directional numbers (sample still too small to retire anything).
- 2026-09-26 (2nd pass): added #9 Curiosity gap / open loop, proof @rowancheung 82.73x its own median (hooks.py,
  21-day scan) plus Later/HookMafia-Socialync research on open-loop hooks; retired the unproven "Real or AI?" pattern
  to keep the list at 12. Our numbers unchanged since this morning's pass (still too small to rank).
- 2026-09-27: added #9 Secret reveal from our own top-performing post (162 YT/169 IG views, hooks.py OURS) — the
  first pattern proven from our own results rather than another account's or a lab test's. Retired "Most people use
  X wrong" (no proof line in any scan since it was added) to keep the list at 12. Refreshed proof numbers for #1-4,
  #6-8, #10, #12 with this scan's data (mostly the same lines re-appearing, a few percent up or down). Web research
  this week (Captain Hook AI's "4 Reels Hook Formats for 2026", Later's Sep 2026 trend report) surfaced lifestyle/
  beauty-niche formats (Anti-Hook/self-aware framing, "This is your sign", age-bracket hooks) with real examples but
  no AI/tech-niche proof yet — watching, not adding until one shows up in our data or a tech account's.
- 2026-09-29 (news-carousel focus): refreshed proof for #1 (364x, up from 255x), #2 (90x, now the most repeat-
  surfacing hook we've tracked), #3 (56x, plus first own-data proof: 1,416 YT views), #7 (57x) and #10 (77x, a
  fresh example line clearing the bar). Our #9 Secret reveal jumped to a much bigger lead (1,640 IG/1,426 YT views
  on a new post) — no pattern change, just stronger proof. No new pattern added: this week's web research on news/
  breaking-alert hook formats and GitHub repo post hooks returned only generic marketing-blog advice with no
  concrete AI-niche example strong enough to clear the bar (searched viral hook formats, AI-account hook
  breakdowns, and repo-post virality; see learn.json sources) — list stays at 12, repo hooks section unchanged (no
  repo posts in this scan's data to refresh proof from).
