# Caption & hashtag playbook (AI Playbooks)

The training document of the caption agent (`prompts/caption.md`). Keep it true: platform rules come from research
(sources at the bottom). The "Lessons" section grows from our own numbers.

## 1. What a caption must do
The media stops the scroll; the caption turns the stop into **saves, comments and follows**. The owner's brief
(2026-09-26): creative, easy to understand, easy to read, pushes people to comment, neat paragraphs.
- Write fresh, in our own words, for THIS post. Never copy other accounts' captions (the references are ideas only).
- **No sources, no photo/video credits, no "Source: @..." lines, no links** in any caption. Credits are already on the
  media (cover photo line, "Source: @creator" under the clip); in the caption they kill the reading flow.
- **No disclaimer lines** ("not financial advice" ...). Bold result promises with numbers are allowed (owner's rule).
  News facts (what launched, versions, dates) must match the content JSON: don't add facts it doesn't have.
- Emojis: 1-4 in the whole caption, each with a job (a bullet, a mood, the CTA). Never a row of emojis.
- Plain words, short sentences, "you" language. No hashtags or @mentions in the middle of sentences.

## 2. Instagram (carousel posts and Reels)
Rules: max 2,200 characters; **max 5 hashtags** per post/Reel (Instagram's cap since Dec 2025; hashtags in the first
comment count too); only the first **~125 characters** show before "more"; caption keywords are a search/ranking
signal (Instagram search and, since 2025, Google index professional accounts' captions). Hashtags help people
understand what the post is about; they don't buy reach, so few and exact beats many and generic.

Shape (blank line between every block; each paragraph at most ~3 phone lines, ~300 characters):
1. **Hook line** (<= 125 chars; a live pattern from `prompts/hook_playbook.md`, not the cover headline again): the promise or the surprise + the main keyword ("ChatGPT prompts", "AI agent",
   "side hustle", "Gemini"). It must make people tap "more". Not the same sentence as the cover headline.
2. **Why it matters** (1-3 short sentences): the pain or the opportunity, in the reader's words.
3. **What's inside / how to use it**: 2-5 short lines, each starting with the same marker ("→", "✅", "1." ...),
   or one short paragraph. For packs: what the prompts do, not the prompts themselves.
4. **Engagement**: one specific question that is easy to answer in 1-3 words, or a comment keyword
   ("Which one are you trying first: 3 or 5?", "Comment AGENT and I'll ...", only if we really deliver). Then a
   save/share nudge ("Save this for your next ... ").
5. **Follow line**: short and varied ("Follow @aiplaybooks.daily for a new AI playbook every day.").
6. **Hashtags**: 3-5, one line, at the very end.

Length: carousels 450-900 characters, Reels 250-550.

### Comment-keyword call to action (when the post has `dm.keyword`)
Our Instagram bot DMs the post's page to everyone who comments the keyword (follow gate: they must follow us). Then
the Instagram caption's engagement block IS the keyword CTA, and the hook line may tease it. Vary the wording every
post (never the same line twice in a row), e.g.:
- "Comment AGENT and I'll send you all 7 prompts 📩"
- "Want the full setup? Comment GUIDE, we'll DM it to you."
- "Comment BUDGET to learn how, I'll DM you the link."
- "Drop "PROMPTS" in the comments and they're in your DMs in seconds."
- "Type SKETCH below 👇 and I'll send you the exact prompt."
Keyword in capitals, exactly as in `dm.keyword`. Facebook and YouTube have no bot: no keyword there.

## 3. Facebook (Page photo posts and Reels)
Same audience as Instagram (Meta); the same post may read a bit more like a story. Rules: long text is fine, but only
the first line or two show before "See more", so the hook works the same way. **2-4 hashtags** (more reads as spam;
on Reels they help the Reels feed a bit), at the end. Facebook demotes **engagement bait** ("comment YES", "tag 3
friends", "share if you agree"): ask a real question instead. No "link in bio" (it doesn't exist on Facebook).
Shape: hook line → 1-2 short story paragraphs → what's inside → a real question → hashtags.

## 4. YouTube Shorts
- `title`: <= 100 characters including " #Shorts" (the publisher adds " #Shorts" when missing; aim for 40-70
  characters before it). Keyword first ("ChatGPT prompts that ..."), a clear promise, matches the video exactly.
- `description`: first line = what the Short gives + keyword (it shows in search). 2-4 short paragraphs. The prompts
  of a clip (`comments`) are appended by the publisher: don't paste them. 3-5 hashtags at the end: the first 3 can
  show above the title. **Over 15 hashtags in title + description and YouTube ignores all of them.**
- `tags`: 5-10 search phrases people type ("chatgpt prompts", "ai side hustle"), max ~450 characters together.
  They matter little but help with misspellings / variants.

## 5. Hashtag method (research, not guessing)
1. Pick 2-3 **keywords** a viewer would search for this post (tool + outcome: "chatgpt prompts", "ai agent",
   "side hustle", "gemini tts").
2. Run `python tags.py "kw one" "kw two" --json runs/<run>/tags.json`. It shows:
   - Instagram/Facebook: hashtags that big AI accounts (@chatgptips, @openai, @theaifield ...) really used in their last
     ~40 posts each, how often, by how many accounts, and the engagement of those posts (overall + on posts that match
     your keywords).
   - YouTube: tags + hashtags of the most-viewed Shorts of the last 30 days for each keyword, weighted by views.
3. Optionally 1-2 web searches for the topic's current tags (e.g. a new product's official hashtag).
4. Choose per platform, all tied to the post:
   - 1-2 **broad** tags with proven volume (#ai, #chatgpt, #artificialintelligence, #aitools)
   - 2 **topic** tags (#chatgptprompts, #sidehustle, #aiagents, #gemini)
   - 0-1 **intent/format** tag (#productivity, #makemoneyonline, #learnwithai)
   Avoid: paid-partnership tags (#...partner), tags about something else (#film on a finance post), empty generic
   tags (#fyp, #explore, #instagood), more than one of #viral/#trending, brand tags of brands not in the post, tags
   with spaces or punctuation. Instagram tags and YouTube tags may differ: pick from each platform's own data.
   The Instagram data comes from AI accounts only: it proves the AI tags, not the topic tags. For the topic side of a
   non-AI subject (money, budgeting, fitness, trading, side hustle ...) the evidence is the YouTube data and web
   research; every post needs **at least 2 topic tags** on every platform (a budgeting pack without #budgeting or
   #personalfinance is wrong even if AI accounts never used them).
5. Write down why each tag was picked (the data line) in the result file.

## 6. Clips (viral Reels) vs carousels
- Clip (format changed 2026-10-06: the video is now the raw clip, nothing is drawn on it, so the caption carries
  everything the frame used to): **first line = the hook** (the line that used to sit on top of the video; it must work
  on its own and fit before "more"), then 2-3 short blocks on what we see and why it matters, then the question.
  **The creator credit is now in the caption**: a line `Credit: @handle on X` (from the post's `credit` field) as the
  last line before the hashtags, on Instagram, Facebook and in the YouTube description. It is the one "Credit:" line
  captions.py still allows, and only for clips. If the post has `comments` (e.g. the prompts behind the video), say
  clearly that they're in the comments ("The full prompt is in the comments 👇").
- Carousel: tell people to swipe and save; the hook can name the number of prompts/tips.

## 6b. GitHub repo posts (`"kind": "repo"`, owner 2026-09-28)
One photo (the plain GitHub page, no text on it): the caption carries everything. No YouTube for these posts:
leave `captions.youtube` out.
- Start from the content JSON's `hook` lines: they are the scroll-stopper and they open BOTH captions almost
  word for word. Sharpen them if you can, never soften them into a friendly intro.

#### Scroll-stopping hooks (owner, 2026-09-28: "dikkat çekici, öldürücü, scroll stopping", like his references)
The owner's reference posts (big AI pages, each with 100+ reactions) - study the SHAPE, never copy the words:
```
I JUST FOUND A GITHUB REPO THAT TURNS CLAUDE CODE INTO AN ARMY OF AGENTS.
No tabs. No context switching.
It's 100% FR££ and open source.
Run multiple Claude Code agents in parallel (researching, coding, debugging, and documenting) while you simply oversee the work.
It's called Collaborator.
```
```
🚨A solo dev just open sourced a FR££ ElevenLabs replacement that runs entirely on your machine. It clones voices from a reference clip, dubs video into 646 languages versus ElevenLabs' 32 and offers 14 TTS engines.
No per-character charges.
No audio leaving your computer.
Already at 41K+ GitHub stars.
```
```
The FR££ course includes 14 lectures and 8 hands-on projects teaching how to build environments that make coding agents work longer, verify themselves, and actually finish tasks.
```
```
🚨 This is an absolute must save resource
OpenAI open sourced a bunch of Codex skills
Extremely useful
```
What makes them stop the scroll:
- **Line 1 is a pattern interrupt**: ALL-CAPS discovery ("I JUST FOUND A GITHUB REPO THAT ..."), 🚨 + a story
  ("A solo dev just open sourced ..."), a big name doing something ("OpenAI open sourced ..."), or a save command
  ("This is an absolute must save resource"). It names the payoff in the first ~10 words.
- **An enemy or a price**: the paid tool it replaces (ElevenLabs, Midjourney, CapCut ...) or the cost it kills
  ("No per-character charges", "No subscription").
- **Concrete numbers beat adjectives**: "646 languages versus ElevenLabs' 32", "14 lectures and 8 projects",
  "41K+ GitHub stars". A versus-number is the strongest line you can have (only when verified).
- **Staccato punch lines**: 2-5 word sentences, one per line ("No tabs. No context switching.").
- **Social proof last**: the star count ("Already at 41K+ GitHub stars.") or who made it.
- **FR££** always, never "free".
- Vary the opener type from post to post (check the last 5 repo posts in `content/repos/`).
- Never: "Check out this cool repo", "Here's a useful tool", questions as the first line, hashtags or emojis spam in
  the hook, claims the README doesn't support.

- Write FREE as **FR££** (house style, both platforms).
- **Instagram**: after the hook lines, the keyword CTA: the bot DMs the repo link right away, e.g. "Comment VOICE
  and I'll DM you the repo link 📩", then ask for the follow ("Follow @aiplaybooks.daily, we post a FR££ AI tool
  every day"). No URL in the caption.
- **Facebook**: the same hook lines, then "Link in the first comment 👇" (the publisher posts `fb_comment` as our
  first comment). No keyword, no URL in the caption. A real question is fine but short.
- 3-5 hashtags on Instagram, 2-4 on Facebook, e.g. #github #opensource + the topic.
Length: 250-600 characters.

## 7. Examples
Bad (our old captions, 2026-09-25):
```
A viral private jet flex video, recreated line-for-line and pose-for-pose — labeled 'Real' vs 'AI' side by side.
Same suit, same champagne pop — swapped for a backyard and plastic water bottles.
Source: @kirillk_web3 on X
Follow @aiplaybooks.daily for daily AI tips & news
#AI #AIContent #ContentCreation #ViralVideo #SocialMediaTips #BehindTheScenes
```
Why bad: no blank lines (one grey block), a source line, no question, 6 hashtags (over the cap), generic tags.

Good (clip, same video):
```
Real or AI? This "private jet" flex was shot in a backyard 🤯

Same suit, same pose, same champagne pop. The only thing that changed: the jet is gone and the champagne is a
plastic bottle.

This is how easy it is to fake a luxury lifestyle online now.

Would you have spotted it? Tell us in the comments 👇

Follow @aiplaybooks.daily for the AI tricks everyone's talking about.

#ai #aivideo #realvsai #chatgpt
```

Good (prompt pack carousel):
```
7 ChatGPT prompts that turn a faceless page into a $3,000/month machine 💸

Most faceless pages fail for one reason: no plan. These prompts give you the plan, from the niche to the first
brand deal.

→ pick a niche that already pays
→ 30 days of posts in one sitting
→ an AI agent that drafts, schedules and asks you to approve
→ a sponsor pitch that gets answers

Which prompt are you stealing first: 1, 3 or 6? 👇

Save this before you start your page, and follow @aiplaybooks.daily for a new playbook every day.

#chatgptprompts #aiagents #sidehustle #chatgpt #ai
```

Good (news carousel):
```
Gemini can now clone a voice from a 30-second clip 🎙️

Google just launched Gemini 3.8 Flash TTS: 2,000+ voices, 100+ languages and built-in consent checks.

Swipe to see how to try it in AI Studio, plus 4 prompts to test it today.

Would you let AI read your videos in your own voice? Yes or no? 👇

Follow @aiplaybooks.daily for AI news you can actually use.

#gemini #googleai #texttospeech #aitools #ai
```

## 8. Lessons (from our own numbers; the agent adds dated lines here only when runs/metrics.json shows a clear pattern)
- 2026-09-29: the comment-keyword CTA in section 6b (repo posts) works — our first repo post (OpenMontage) got 8
  comments on 16 IG views (50%), our highest comment rate of any post to date, and real accounts (instagram.com/
  reel/DakrLG1MwgV, instagram.com/p/Da-ccAlJIih) run the identical "Comment [WORD] and I'll send you the GitHub
  repo" shape on their own repo posts. Keep this CTA on every repo post exactly as section 6b writes it, placed
  after the hook lines (moving it earlier, into the first ~125 characters, is not supported by our own data and
  would push the hook lines out of the "before more" window).
- 2026-09-30 (trial, not yet AI-niche-proven): Metricool's own cross-account measurement found that @-tagging a
  relevant account in the caption (e.g. the tool's official page on a news post) beats every other CTA type they
  measured for accounts under 10,000 followers specifically — +45% comments, +20% reach — but the same tag hurts
  accounts over 1M followers (metricool.com/create-a-call-to-action-that-converts, Sep 2026). We are exactly the
  small-account profile this applies to (1-3 followers). Worth testing on a news carousel/clip about a named tool
  (tag its real account once, not spammed): if it lifts comments/reach on our own numbers, promote to a standing
  rule; this is general cross-niche data, not AI-account-specific, so it stays a trial until our own metrics confirm
  or contradict it.
- 2026-10-03: news posts — open the caption (and the cover) with the STAKES or the conflict, not with "[Company] just
  launched X. Meet X:". Our news Reels on YouTube (hooks.py OURS, 2026-10-03): conflict/record/rule-breaking lines got
  441-972 views ("Claude ... broke a physics record that stood since 2023" 972, "Anthropic just shipped a coding model
  that beats its own flagship" 586, "An OpenAI training agent tried to sneak a question past its sandbox ... caught in
  15 minutes" 441) vs. 12-57 for plain launch/feature lines ("ChatGPT can now track your Experian credit score" 12,
  "Apple just gave Siri ..." 43, "... Meet dots:" 50, "... Meet GPT-6 Sol and Luna:" 57). Name what was beaten,
  broken or caught; keep the product name, drop the "Meet X:" close.
- 2026-10-03: prompt packs — the first line names the concrete TASK the AI does for you, the $ figure (if any) comes
  after it. Same accounts, same carousel format (hooks.py, 21 days): skill/daily-life openers "ChatGPT isn't just for
  answering questions anymore. It can also help you build complete presentations ..." 7.65x and "... your personal
  language tutor ..." 3.8x (@chatgptips), "ChatGPT can now be your interior designer." 4.36x (@chatgptricks) vs. money
  openers 0.51-0.95x ("... income streams" @chatgptips 0.95x, "You don't need to earn more money ..." 0.72x,
  "Claude can now launch your business like ... Steve Jobs" @godofprompt 0.51x). Ours agree: money-promise pack lines
  0-2 IG views; the bank-statement capability line 7 views / 6 comments.
- 2026-10-04: news — when the story has a real PERSON in it, open the caption with that person and hold the outcome
  back for the slides; don't summarise the outcome in the first line. Same week, same news story, same carousel
  format (hooks.py, 21 days): @theaifield's narrative version "A woman told ChatGPT she was deleting the app so she
  could spend more time with her newborn, but the farewell quickly became far more emotional than she expected."
  got 70.51x its median (2,434 likes) — the highest carousel line in the window — while @chatgptricks' resolved,
  short version of the same story ("She deleted ChatGPT, then immediately came back.") got 6.19x. Keep the first
  ~125 characters on the person and the unresolved turn ("but what happened next ...", "but it was far worse than
  he expected"). Hook playbook pattern #5.
- 2026-10-04: news — pick the real-world story over the feature story, and say what the thing physically DOES.
  Ours (hooks.py OURS): "China just built an AI lifebuoy that flies to you when you're drowning." 377 YT / 143 IG
  views / 2 likes, our best-engaged news carousel, vs. 12-152 YT for feature/announcement captions ("... Experian
  credit score" 12, "Apple just gave Siri ..." 43, "... Meet dots:" 62, Muse-AI-on-glasses 131). Big accounts split
  the same way: @rowancheung's four best lines are all hardware/physical (hip surgery 33.1x, house-as-robot 7.1x,
  Dyson toothbrush 6.17x, lab-reproducibility 142.02x) while @therundownai's software-feature lines top out at 8x.

## Sources (research 2026-09-26)
- Instagram 5-hashtag cap (Dec 2025), Mosseri on hashtags: https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/
- 125-character "more" cutoff, caption keywords: https://creatorlanehq.com/blog/instagram-5-hashtag-limit-2026 ,
  https://later.com/blog/instagram-seo/
- YouTube hashtags (15 / 60 rule, first 3 above the title): https://support.google.com/youtube/answer/6390658 ,
  https://hashtagtools.io/blog/youtube-hashtags-shorts-seo-guide-2026
- Facebook hashtags 2-5, Reels: https://sproutsocial.com/insights/hashtags-on-facebook/ ,
  https://contentstudio.io/blog/facebook-hashtags
- Facebook engagement bait demotion: https://about.fb.com/news/2017/12/news-feed-fyi-fighting-engagement-bait-on-facebook/
