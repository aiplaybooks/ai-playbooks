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

## Live patterns (updated 2026-09-26)
Each: template · example (ours) · proof (data line: account, engagement vs. the account's median).

1. **Comment-keyword DM** · "Comment "[WORD]" and I'll send you [the full thing]." · "Comment AGENT and I'll send you
   the 7 prompts." · proof: @theaifield 274x its median (2,852 comments), @godofprompt 12.9x / 11.4x (2,000+ comments).
   Use when we really deliver (the post has a `dm.keyword`: our bot DMs the page). Best for packs. Vary it:
   "Comment X, I'll send you the link" / "Comment X to learn how, we'll DM you" / "Want it? Comment X".
2. **Big number + insider move** · "[Person/company] just [did something surprising] [$ figure]" · "Higgsfield's CEO
   just open-sourced his entire $5.4B platform" style · proof: @theaifield 65x. Use for news with a figure.
3. **Time-lapse shock** · "[Short time]. That's all it took for [thing] to [change completely]." · proof:
   @airesearches 46x, @theaifield 40x (same line, both accounts). Use for "then vs. now" AI clips.
4. **Short punchy statement** (under 8 words, period) · "OpenAI waited just 90 minutes." / "Meta's Muse just hit
   No. 1." · proof: @chatgptricks 18x, 15.7x. Use for news with one striking fact.
5. **"AI is starting to [pay/save you] real money"** · "AI agents are starting to save people real money." · proof:
   @chatgptricks 21x. Use for money packs / agent stories.
6. **What-if question** · "What if you could [impossible thing]?" · proof: @chatgptricks 27.6x, 14.4x (video).
   Use for imaginative AI video clips.
7. **Breaking-update alert** · "🚨 [Company] is rolling out [update] today, [biggest in years]." · proof: @chatgptips
   21x, @theaifield 42.8x. Use for a big consumer update (phone, app) on launch day.
8. **Division / debate** · "[Topic] has divided [group], and both sides have a point." · proof: @chatgptricks 26x
   (264 comments). Use to drive comments on controversial AI topics.
9. **Real or AI?** · "Real or AI? [what we see]" · (our pattern for AI-vs-real clips; ask the viewer to guess).
10. **"Most people use X wrong"** · "[Tool] has [huge number] users, but most people still use it like [simple thing]."
    · reference style: @chatgptips cover "ChatGPT has more than 1 billion monthly users, but most people still don't
    know how to use it properly". Use for prompt packs.
11. **Identity call** · "If you [use/do a specific thing], this is for you." — names the exact audience in one line,
    keep it under ~12 words · "If you're still copy-pasting into ChatGPT one tab at a time, this is for you." ·
    proof: 2026 short-form hook testing scored Identity Call highest of 30 tested patterns (~85/100 vs. next-best
    Contrarian Strike/Open Loop, both >70; generic openers like "Hey guys" scored <30) — HookMafia/Socialync, Sep 2026.
    Use for prompt packs and tool-specific tips.
12. **Contrarian strike** · "Stop [doing the common thing]." — a flat command, no explanation yet · "Stop typing your
    prompts from scratch every time." · proof: same 2026 testing, one of only 4 patterns to clear the 70-score bar;
    negative framings ("stop X" / "you're doing X wrong") beat positive framings of the same idea by 1.3-1.8x hook
    rate (HookMafia/Socialync, Sep 2026). Use for tips/prompt packs, don't overlap with #10 in the same week.

## Weak patterns (data says avoid)
- Long explanatory first sentences (> 25 words) that describe a product like a press release ("X is an AI-powered
  platform that enables anyone to ..."): bottom of the ranking.
- Spec lists in the hook ("weighs 100 grams, less than a fifth of ..."): the numbers belong in the carousel.

## Our results (from runs/metrics.json; the learning job fills this in)
- Numbers are still tiny (best post so far: 219 IG views, 2 IG comments) — not enough to rank patterns yet.
  Directional only: the "big number + insider move" clip ("Claude Opus 5.5 designed a LEGO duck... wrote a 141-page
  instruction booklet", pattern #2) leads our clips at 219 IG views/1 like; the transformation-style cover "Google
  just gave Gemini a face" (pattern #3-adjacent) leads our carousels at 102 YT Short views. Re-check once 30-day
  history has real spread.

## Log
- 2026-09-26: first version from hooks.py (12 AI accounts, last 21 days).
- 2026-09-26: added #11 Identity call and #12 Contrarian strike from 2026 short-form hook testing (HookMafia/
  Socialync) — both cleared the 70-score bar and negative framing beat positive by 1.3-1.8x; filled in "Our results"
  with early directional numbers (sample still too small to retire anything).
