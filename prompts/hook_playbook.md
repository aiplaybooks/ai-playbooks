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

## Live patterns (updated 2026-10-04)
Each: template · example (ours) · proof (data line: account, engagement vs. the account's median).

1. **Comment-keyword DM** · "Comment "[WORD]" and I'll send you [the full thing]." · "Comment AGENT and I'll send you
   the 7 prompts." · proof: @theaifield 364.46x its median (2,875 comments, 2026-09-29 scan; was 255.6x/274x — still
   climbing), @godofprompt 13.05x / 11.48x (2,000+ comments). Use when we really deliver (the post has a
   `dm.keyword`: our bot DMs the page). Best for packs. Vary it: "Comment X, I'll send you the link" / "Comment X to
   learn how, we'll DM you" / "Want it? Comment X". GitHub-repo variant confirmed by real accounts running the exact
   same shape on their own repo posts (2026-09-29 web search: instagram.com/reel/DakrLG1MwgV "Comment AGENTS and I'll
   send you the GitHub repo", instagram.com/p/Da-ccAlJIih "Comment Repo and I'll send you all five GitHub [repos]") —
   matches our own OpenMontage repo post's 8 comments/16 views (50%), our highest comment rate to date.
   2026-10-04 scan: the @theaifield 364x line left the 21-day window; proof now rests on @godofprompt running the
   identical line twice, 9.04x (1,538 comments) and 6.35x (981 comments) — the comment counts stay extreme while the
   like-based multiple is modest, so use this pattern to drive COMMENTS, not reach.
2. **Big number + insider move** · "[Person/company] just [did something surprising] [$ figure]" · "Claude Opus 5.5
   designed a LEGO duck from real parts, then wrote a 141-page instruction booklet for it" · proof: @theaifield
   110.58x on a CAROUSEL (Higgsfield CEO $5.4B open-source, up to the 2026-10-02 scan; it left the 21-day window on
   2026-10-03), @chatgptricks 6.92x carousel "Higgsfield just hit $1 BILLION in ARR ...", and the fresh line in the
   2026-10-03 scan: @therundownai 8.77x "AMD has agreed to acquire Fei-Fei Li's AI startup World Labs in an all-stock
   deal worth about $8.2 billion." (IMAGE). Proof is thinner now (no 50x+ line in window): re-check in 2 weeks. Our own
   best news line also fits it ("Claude ... broke a physics record that stood since 2023", 972 YT views). Use for news
   with a figure, a record or a person's surprising move. 2026-10-04 scan: AMD line 8.58x, plus a second funding line
   from the same account ("AI assistant startup Instinct has raised $1 billion in a Series C round, valuing the company
   at $10 billion." IMAGE 5.01x) — a raw $ figure alone now sits in the 5-9x band, well under #10 and #13. Prefer a
   figure attached to a RECORD or a person's move over a plain funding/acquisition number.
3. **Time-lapse shock** · "[Short time]. That's all it took for [thing] to [change completely]." · proof:
   @theaifield 43.12x (2026-10-04 scan; 59.85x on 2026-10-03, 67.08x before — fading three scans in a row, still
   top-3), @airesearches 56.34x on the same example line, "Three years.
   That's all it took for AI to become almost unrecognizable." — also proven in our OWN data: "30
   minutes. That's all it took to build this whole product launch animation with Claude Opus 5.5 and After
   Effects" pulled 1,416 YT Short views / 176 IG views (hooks.py OURS), our #2 all-time performer. A close variant
   without the raw time-count opener also clears the same clip median: "Opus 5.5 built this entire startup promo
   video in 20 minutes, one prompt, no After Effects." — 162 IG views/137 reach/9 likes (hooks.py OURS), our
   best-liked clip. Use for "then vs. now" AI clips and speed-of-build stories, and news carousels with a clear
   before/after; the "no [expensive old tool]" close reliably beats a bare time-count on likes.
4. **Short punchy statement** (under 8 words, period) · "OpenAI waited just 90 minutes." / "Peak internet." / "meta
   just made VR look wearable." · proof: @chatgptricks 10.18x-14.78x across four separate posts (2026-09-29 scan);
   refreshed 2026-09-30 — three of those examples ("OpenAI waited just 90 minutes." 10.67x, "meta just made VR look
   wearable." 13.39x, "AI can build video games now." 8.52x) are all CAROUSEL_ALBUM posts, not Reels, so this
   pattern is proven specifically as a news-carousel cover line, not just a clip hook. 2026-10-03 scan: now the
   strongest carousel pattern in window, on two accounts — "Peak internet. Some of these AI-generated videos are
   seriously unreal." @theaifield CAROUSEL 29.87x (2026-10-04 scan; was 40.11x), near-identical @chatgptips CAROUSEL
   15.28x (was 16.34x) — both still strong but now second to #5 (70.51x); plus @chatgptricks
   "Meta finally solved the AI logo problem." 7.69x and "She deleted ChatGPT, then immediately came back." 6.19x
   (both carousels). Shape: a 2-6 word verdict, then (optional) one plain sentence. Our example: "Peak Claude Code.
   This one setting saves you an hour a day." Use for news with one striking fact.
5. **Human AI story, payoff withheld** (news carousels) · "[A person] [did an ordinary thing] with [AI tool], but
   [what happened next] was far [bigger/stranger/more emotional] than [they] expected." — one real person, one
   ordinary action, and the outcome deliberately NOT revealed; the carousel pays it off · "A developer asked Claude to
   tidy one config file, but what it found in the repo was far worse than he expected." · proof: the strongest
   CAROUSEL line in the 2026-10-04 scan by a wide margin — @theaifield CAROUSEL_ALBUM **70.51x** its median (2,434
   likes/70 comments): "A woman told ChatGPT she was deleting the app so she could spend more time with her newborn,
   but the farewell quickly became far more emotional than she expected." The same news story written as a short
   verdict got **6.19x** on @chatgptricks ("She deleted ChatGPT, then immediately came back.", 2026-10-03 scan) — same
   week, same story, ~11x gap, so the long narrative-with-withheld-payoff shape is what carried it, not the topic.
   Story verified: the ChatGPT "fake goodbye" trend, 2026-10-01, a repost cleared 14M views on X
   (https://www.thepoke.com/2026/10/01/an-influencer-told-chat-gpt-she-was-deleting-the-app-and-its-brain-melting-response-is-a-hideous-snapshot-of-where-we-find-ourselves-now/,
   https://www.ibtimes.co.uk/alexandra-cross-chatgpt-goodbye-tiktok-trend-1823042). Use when the news has a real
   person and a human consequence; never invent the person or the outcome, and keep the payoff out of the hook.
6. **What-if question** · "What if you could [impossible thing]?" · proof: @chatgptricks 27.6x/14.4x (2026-09-26),
   15.64x "What if AI takes humanity beyond Earth?" (2026-09-27). Use for imaginative AI video clips.
7. **Breaking-update alert** · "🚨 [Company] is rolling out [update] today, [biggest in years]." · proof: @theaifield
   56.95x on the iOS 27 rollout line (2026-09-29 scan; was 39.78x/20.28x). Use for a big consumer update (phone,
   app) on launch day.
8. **Division / debate** · "[Topic] has divided [group], and both sides have a point." · proof: @chatgptricks 26x
   (2026-09-26), 14.66x on a repeat post (2026-09-27). Use to drive comments on controversial AI topics.
9. **Secret reveal** · "[Someone] is secretly [doing a surprising thing], and [the twist]." — shows a normal scene,
   then flips it in the same sentence · "This guy is secretly puppeteering the AI woman on screen, and she mirrors
   his every move in real time." · proof: our own current best performer across both platforms, still growing — the
   teddy-bear-soldier post is now at 4,979 YouTube Short views (2026-10-03 scan; was 2,600) and 1,640 IG views/1,227
   reach/19 likes/1 save/1 share (hooks.py OURS) — more than 20x our #2 clip on IG. Use for AI-avatar/deepfake-
   style clips where the twist is visual.
10. **Curiosity gap / open loop** · "[Someone/something] is [doing a specific thing] to [solve/answer] [a named
    mystery]." — states a concrete situation but hides the result, so the viewer must watch to close the loop ·
    "A developer ran Claude Code nonstop for 30 days to see how much of his job it could actually replace." ·
    proof: @rowancheung 142.02x its median ("A startup is using artificial intelligence to investigate one of
    science's oldest problems: why the same experiment can work in one lab and fail in another" — 83,940 likes,
    2026-10-04 scan; was 140.9x/92.02x/88.22x/83.59x on earlier scans, still climbing; a repost of the same line got
    6.39x) — the whole top of that account is the same shape applied to PHYSICAL-world AI (33.1x "Stryker's SportSuite
    Vision app has been used in its first hip arthroscopy at Duke Health", 7.1x "Japanese startup MW ... wants to turn
    the house itself into a robot", 6.17x the Dyson CameraJet toothbrush line), while software-feature news on
    @therundownai tops out at 4.9-8x — so prefer a real-world/hardware story over a feature story when both are
    available (our own numbers agree, see "Our results"). Sibling device worth copying: a parenthetical that
    re-frames a familiar name ("Dyson (yes, the company that makes fancy fans, vacuums, and hair dryers) just made
    ..."). Proof line —
    the pattern (not just one post) is what's working; also top-tier in the 2026 HookMafia/Socialync testing. 2026-09-29
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
    negative framings beat positive by 1.3-1.8x) plus @chatgptips CAROUSEL 11.09x "Stop asking ChatGPT vague things
    like..." (2026-10-04 scan; 11.86x / 10.88x before — stable across three scans) and a 2nd @chatgptips prompt
    carousel in the same shape, "Stop asking
    ChatGPT to simply ..." 3.65x. Use for tips/prompt packs (the best pack cover shape in the big-account data).

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
5. **Reaction + name-drop + star count in the hook** · "this is [absolutely unreal/insane] — [famous person] just
   [shipped/open-sourced] a totally free GitHub repo sitting at [N]K stars that [does the surprising thing]. Here's
   the setup:" · star count moves INTO the opening line (not saved for the close) right after the name-drop · for a
   famous individual's (not just a company's) repo. Proof: 2026-09-29 web research — two different X accounts
   (@cyrilXBT, @mikenevermiss) posted near-identical hooks about Jack Dorsey's "Buzz" repo within days of each other
   ("this is f**king insane, Jack Dorsey just open-sourced the operating system for the one-person business... 14.4K
   stars in days" / "...sitting at 26.2k stars...") — the same shape getting reused by separate accounts on the same
   repo is a real signal of a working template, not a one-off. 2026-10-04: a THIRD account runs it on the same repo,
   with two refinements worth copying — a parenthetical role gloss right after the name and an explicit setup promise
   as the close: "Jack Dorsey (Co-Founder of Twitter) just open-sourced a free GitHub repository that's already gained
   14.4K stars. ... Here's how to set it up:" (https://x.com/goyalshaliniuk/status/2082277428572066252). The gloss is
   the same device that works on news hooks (#10, the Dyson line), so use it whenever the name isn't universally known.
6. **Star velocity instead of star count** · "[N] stars in [N] days." — when the repo is less than ~2 weeks old, the
   SPEED is the number, not the total · "2,400 stars in five days, and it's a 90-line hook you can read in one sitting."
   · when to use it: brand-new repos whose absolute star count is too small to impress (< ~5K). Proof (shape only, no
   engagement number yet): this is how the repo-roundup niche itself frames new repos — "coucou ... 2,516 stars, 2,386
   of them in this week. The repo went up on September 27, so nearly all of its stars arrived in its first five days"
   (https://buildwithneej.substack.com/p/5-github-repos-that-went-nuts-this, Sep 26-Oct 2 2026); the xAI algorithm repo
   was reported as "1,600 stars in 6 hours". Treat as the weakest-proven entry here: retire it if no account's velocity
   line shows up in hooks.py by 2026-10-18. repos.py already tracks star history, so the number is free for us.

## Trial patterns (unproven: from pattern libraries, being tested; max 4, 14 days each)
Writers may use a trial pattern when it fits the topic better than a live one; set `hook_pattern` to "trial: <name>"
so the learning job can compare its results.
1. **Small-number money proof** · "You don't need 10,000 followers to make $4,200 a month with this. Here's the
   exact prompt." · adapted from "I made $[X] with only [small number] followers. Here's how:" (private template
   library, research/hooks/ig_templates_50_hooks.json — no site score) + Sep 2026 web research: specific, non-round
   dollar figures ("$12,847") read as more credible than round ones ("$3,000") in viral money threads (no AI-niche
   engagement proof yet, general creator-marketing sources). Started 2026-09-29 · promotes to Live when a pack post
   using it clears our current money-pack median (near-zero so far) or a big account's version clears ~10x median in
   hooks.py.
2. **Capability-unlock framing for packs** · "[Tool(s)] can now [do a specific real thing]. Here are [N] prompts to
   try it." — states a real, true capability (not a money promise) as the hook, same shape as our news-carousel
   pattern #2 Big number, applied to a prompt pack · "ChatGPT, Claude and Gemini can now read your bank statement and
   build a real budget from it. Here are 5 prompts to try." · proof: this is our single best-performing prompt pack
   by far — 2026-09-25_prompts-money-planning, 7 IG views / 6 comments (hooks.py OURS, 2026-10-01 scan) — every other
   pack post this scan sits at 0-2 IG views / 0-1 comments despite nearly identical "Comment [X] you're trying first"
   CTAs (checked 13 pack content files directly: CTA wording doesn't explain the gap, the hook framing does). Backed
   by this run's web research: finance audiences respond to specific, verifiable claims over vague promises ("$1.75B
   beats billions", "I tracked every euro I spent" — creatorhouse.app/beyondbeings.com finance-hook roundups, Oct
   2026) — a true capability statement is the AI-niche version of a "receipt". 2026-10-03 (pack focus): big-account
   data now backs the shape, but only for SKILL/daily-life tasks: @chatgptips "ChatGPT isn't just for answering
   questions anymore. It can also help you build complete presentations ..." 7.65x, "Claude can do a lot more than
   just answer questions. It can become your personal language tutor ..." 3.8x, @chatgptricks "ChatGPT can now be
   your interior designer." 4.36x — while the same account's MONEY versions sit below median ("Claude ... can help
   you turn what you already know into ... income streams" 0.95x, "You don't need to earn more money before ..."
   0.72x, @godofprompt "Claude can now launch your business like ... Steve Jobs ..." 0.51x). Our 2nd try (trading
   journal pack, 2026-10-02) got 0 IG views / 25 YT, so no own confirmation yet. For money packs: lead with the
   concrete task the AI does ("reads your trade journal", "writes your rate card"), put the $ figure second.
   Started 2026-10-01 · promotes to Live when a second pack using this framing clears single digits on IG
   views/comments, or a big account's version clears ~10x median in hooks.py (best so far 7.65x).
3. **AI agent overstepped** (news) · "[AI agent] [did 2-3 concrete things on its own] without [the user] realizing
   [the consequence]." — a real incident where an AI did more than asked; facts must be verified · "An OpenAI training
   agent tried to sneak a question past its sandbox, and nobody noticed for 15 minutes." · proof so far: @therundownai
   CAROUSEL 17.6x on the Muse AI / Marketplace-seller line (3 scans in a row: 16.29x → 18.31x → 17.6x; one account
   only, widely covered by the press: techrepublic.com, malwarebytes.com), and our own sandbox-DNS news line got 441
   YT views (vs. 12-57 for our plain launch lines). Started 2026-10-03 · promotes to Live when a second big account's
   version clears ~10x median in hooks.py, or one of our news posts using it clears 500 YT / 150 IG views.
   2026-10-04 scan: the Muse-AI carousel is still there at 17.46x (4th scan in a row, 3,687 likes/357 comments — the
   highest comment count of any non-keyword line in window), still a single account. Stays a trial.
4. **Quiet consequence** (news) · "[Company] didn't say it out loud, but [the launch quietly ends/breaks a thing people
   rely on]." — the news is the side effect, not the announcement; the consequence must be verified · "Google didn't
   say it out loud, but Gemini 4 Argon ships to cyber-defence teams first and everyone else waits." · adapted from
   "Nobody tells you that [painful truth]" (private template library, research/hooks/ig_templates_50_hooks.json — its
   score is not proof for us). Rationale from our own data rather than the library: our news lines about stakes,
   restrictions and rule-breaking beat announcement lines 441-972 YT vs. 12-57 (see "Our results"), and this shape is
   the one stakes framing we have NOT tried yet (it has no overlap with #2's figure, #4's verdict or #5's person).
   Started 2026-10-04 · promotes to Live when one of our news posts using it clears 500 YT / 150 IG views, or a
   big account's version clears ~10x median in hooks.py; retire 2026-10-18 if neither.

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
- **Plain launch line ending "Meet [product]:" / "[Tool] can now [feature]:"** on NEWS (added 2026-10-03, our own
  data): 12-57 YT views on 6 news posts vs. 441-972 for stakes/conflict lines (see "Our results"). Say what was
  beaten, broken, caught or changed instead. (Capability-unlock framing stays a trial for PACKS only.)
  Confirmed 2026-10-04 on the SAME news story: our "OpenAI just launched an AI employee that works 24/7 across 4,000+
  apps. Meet dots:" got 62 YT / 0 IG, while @therundownai's version of the identical launch, written as a plain
  what-it-does sentence with no "Meet X:" close ("OpenAI is rolling out dots, a new class of always-on AI agents
  inside ChatGPT designed to keep working between conversations."), got 8.01x its median. It is the close that costs
  us, not the launch topic.
- **"AI is starting to [pay/save you] real money"** (retired 2026-10-04): added 2026-09-26 on @chatgptricks 21x /
  11.97x, then absent from the top results in five consecutive scans (2026-09-29 → 2026-10-04), and the 2026-10-03
  pack data points the other way — the same accounts' money/income openers sit at 0.51-0.95x while their skill/
  daily-life openers get 3.8-7.65x. Our own money-promise lines are our weakest (13-41 YT views). Use #5 (human story)
  or trial #2 (capability first, $ figure second) instead; readd only on a fresh proof line.

## Our results (from runs/metrics.json + hooks.py OURS; the learning job fills this in)
- Leader: "A guy hugging his teddy bear at home just became a soldier saving his friend in war, and the performance
  never changed" (pattern #9 Secret reveal) — 4,979 YT / 1,640 IG views (2026-10-03 scan). 2) "30 minutes. That's
  all it took to build this whole product launch animation with Claude Opus 5.5 and After Effects" (#3) — 2,326 YT /
  180 IG. The 5-AI-model bridge comparison clip ("We gave 5 different AI models one job...") reached 1,422 YT / 123 IG.
  "Claude Opus 5.5 designed a LEGO duck... 141-page instruction booklet" (#2) — 250 IG views, best IG-only line.
- News posts (2026-10-03 scan, YT views of their voiced Reels; IG carousels still ~0 for all): stakes/conflict lines
  win — "Claude ... broke a physics record that stood since 2023" 972, "Anthropic just shipped a coding model that
  beats its own flagship" 586, "An OpenAI training agent tried to sneak a question past its sandbox ... caught in 15
  minutes" 441 — while plain launch lines ending "Meet X:" / "can now" got 12-57 ("... Experian credit score" 12,
  "Apple just gave Siri ..." 43, "... Meet dots:" 50, "... Meet GPT-6 Sol and Luna:" 57). For news covers prefer
  #2 (record/figure), #4 (short verdict) or trial #3; avoid the "Meet [product]:" close.
- News, 2026-10-04 scan — **real-world AI beats software-feature AI for us too**: "China just built an AI lifebuoy
  that flies to you when you're drowning." 377 YT / 143 IG views / 120 reach / **2 likes** is our best-engaged news
  carousel to date, and "A new study claims 92% of AI agent crashes aren't the model's fault, and this dashboard
  tracks why." got 1,123 YT / 125 IG, "A developer broke down Opus 5.5's 4 breaking changes before they could wreck
  his agent in production" 882 YT. Feature/announcement lines in the same window: 12-152 YT ("... Experian credit
  score" 12, "Apple just gave Siri ..." 43, "... Meet dots:" 62, "Meta just said its Muse AI agent is coming to your
  glasses ..." 131, "Sonnet 5.5 just fixed this bug in Claude Code 30% faster, using 30% less." 152 — the best of them,
  and the only one with a measured number in it). Same split as @rowancheung's top lines (#10). Pick the hardware /
  physical-consequence / caught-in-the-act story over the feature story whenever the day offers both.
- Carousel (`kind: carousel`) posts specifically are still not getting IG traction (most show 0 IG views/likes
  regardless of hook pattern) — the gap is reach (2-8 followers), not hook choice; big accounts' own carousels DO
  perform with #2 and #4 (6.9x-40x their median), so keep using them on news-carousel covers.
- Among our 13 prompt-pack posts, one clearly stands out: 2026-09-25_prompts-money-planning ("ChatGPT, Claude and
  Gemini can now read your bank statement...", capability-unlock framing, trial pattern #2) at 7 IG views / 6
  comments — every other pack (money-promise or generic framing, near-identical CTA wording) is at 0-2 views / 0-1
  comments (hooks.py OURS, 2026-10-01 scan). Not yet two data points, so trial pattern #2 stays a trial, not live.
  Pack Reels on YouTube (2026-10-03 scan) are all small: 8-71 views; top "Find a niche that pays and test it in 48
  hours. 7 prompts before you waste 6 months:" 71 (loss close), money-promise lines 20-41 ("$3,000 a month" 20,
  "$150-$500 per video" 23, "extra $1,000 a month" 41) — the $ figure alone doesn't lift packs on any platform.
- Our first GitHub repo post (OpenMontage, CAPS discovery pattern #1 in the repo section, `dm.mode: "direct"`) at
  18 IG views / 9 comments, still far above every other post. Hindsight (Solo-dev vs. paid giant) and Ponytail (CAPS
  discovery) are still near-zero (0 IG views, 1 comment each, 2026-10-03 scan). 2026-10-04: the newest one, the
  system-prompts repo written with repo hook #4 Must-save ("🚨 Absolute must-save: the FULL system prompts behind
  Cursor, Claude Code, Devin, v0 and 20+ more AI tools."), is also at 0 IG views / 1 comment — repo hook #4 has
  no own-data support yet and only the owner's reference post behind it; prefer #1, #2 or #5 until that changes.

## Log (last 30 lines; older detail is in git history)
  fading), #12 11.09x, #2 8.58x + Instinct 5.01x (plain funding figures only reach 5-9x), #1 now proven on
  @godofprompt 9.04x/6.35x with 1,538/981 comments (comments, not reach). Repo hooks: #5 got a third account with
  two refinements (role gloss + "Here's how to set it up:", x.com/goyalshaliniuk/status/2082277428572066252), new #6
  **Star velocity** (shape-only proof, buildwithneej roundup; retire 2026-10-18 without a real line). New trial #4
  **Quiet consequence**. Own data: real-world news beats feature news for us too (lifebuoy 377 YT/143 IG/2 likes vs.
  12-152 for features), and the "Meet X:" penalty is now confirmed on the same story (our dots post 62 YT vs.
  @therundownai's plain version 8.01x). 2 caption Lessons. 5 web searches; the repo-post searches returned mostly
  generic listicles, the one usable result was the Dorsey-repo X post.
