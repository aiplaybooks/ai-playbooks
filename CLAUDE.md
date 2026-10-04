# AI Playbooks — automated Instagram + Facebook + YouTube + X + TikTok pages for AI tool tips & news

> Short version (token budget, 2026-10-04). **Full history, reasoning and every dated detail: `docs/PROJECT_NOTES.md`**
> (the original CLAUDE.md). Read the relevant section there only when you need the why. Keep THIS file short:
> new long notes go to docs/PROJECT_NOTES.md, only one-line rules here.

## Talk to the owner in Turkish
Owner = Cihat, writes **Turkish**. All published content is in **English**. Never ask him "shall I...?": decide, do, report.

## What this is
A zero-cost, fully automated pipeline for **AI Playbooks** — Instagram @aiplaybooks.daily, Facebook Page, YouTube
@ai-playbooks-daily, X @AIPlaybooks_, TikTok @ai.playbooks (inbox drafts) — posting AI tool news, copy-paste prompt
packs, GitHub repo finds and hook-framed viral clips. GitHub `aiplaybooks/ai-playbooks` (account aiplaybooks; never the
other gh account). Media is served from the `gh-pages` branch (https://aiplaybooks.github.io/ai-playbooks/).
The **Studio** (`studio.py`, http://localhost:8787, starts at logon via pythonw) runs everything: gather → scan → post /
clip / repo flows → publish.py → log. Claude steps run `claude -p` with prompts in `prompts/` (lean flags, see studio.py).

## Decisions already made (don't re-litigate; details in docs/PROJECT_NOTES.md)
- **Free only**; direct Graph API publishing. Images are code-rendered (HTML/CSS → Playwright), fonts OFL in `fonts/`,
  music generated (`music.py`), voice = Kokoro via the Pinokio env (`voice.py`; never pip-install it globally).
- **Design varies per topic**: default theme `adaptive` (the writer art-directs a `design` block); `prompts` theme for packs.
- **Pillars**: news (verified against official sources, URLs in `sources`), prompt packs (`prompt_packs.json`, daily life
  / money, our own wording, bold number promises OK, **no disclaimer lines**), GitHub repos (one real GitHub-page photo,
  FREE always written **FR££**, every star count rounded DOWN), viral clips (hook frame, credit @creator, **not fact-checked**,
  never to TikTok). No fake quotes/endorsements by real people, no fake verified badge.
- **Cover** = hook headline over a real freely licensed photo (Wikimedia Commons person / Openverse topic photo, credited on
  the cover); brand icons from Simple Icons (`brand_icons.py`); Flux image generation OFF.
- **Captions**: the caption agent (prompts/caption.md + caption_playbook.md): per-platform `captions` {instagram, facebook,
  youtube, x}, IG max 5 hashtags, readable paragraphs, a question, **no sources/links in captions**; `first_comment` per
  platform; `python captions.py check` enforces. No API can pin a comment.
- **DM bot** (Cloudflare Worker `bot/worker.js`, IG comment keyword → link): `dm.mode: "direct"` for every post until
  Meta grants Advanced Access; link = the post's page `p/<post>/` on gh-pages (`packpage.py`).
- **Full autonomy + autopilot**: approval OFF; `autopilot_tick` fills `post_slots` (14/17/20/23 TR); mix from
  `strategy.json` (clips-heavy). The daily **strategy director** (09:30) tunes mix/skips/experiments from metrics; items
  needing code go to `strategy/backlog.md` (build them). `learn` job 1x/day updates hook/caption playbooks.
- **Carousels also go out as Reels**; per strategy.json `skip` lists some steps (e.g. fb_photos, ig_carousel).
- **X**: never a URL in a post ($0.20 vs $0.015), no replies. **TikTok**: sandbox keys, inbox drafts only, never submit the
  app for review. **YouTube**: no paid promotion, AI-content flag on, tags include `ai`, playlist `YT_PLAYLIST_ID`.
- **Token budget (2026-10-04)**: agents run on `sonnet` (`caption`/`hook` on haiku, only `doctor` on opus), lean flags
  (no project CLAUDE.md/skills/hooks in `claude -p`), **1 gather a day (12:30)**, scans reuse the pool (FRESH_HOURS 20),
  learn 1x/day. Don't add runs, tools or long files to agent prompts without a reason. Keep interactive sessions short.
- Reels 1080x1920, 30fps, H.264+AAC, IG safe zones (top ~190px, bottom ~330px).

## Repo layout (one line each)
```
studio.py + studio/index.html   workflow engine + UI;  prompts/*.md = the `claude -p` prompts (+ *_playbook.md learned rules)
news.py, viral.py, repos.py, tags.py, hooks.py, strategy.py, xscout.py   research collectors
carousel.py, reel.py, voice.py, music.py, clip.py, cover.py, brand_icons.py, repocard.py, packpage.py   production
themes/{adaptive,prompts,neon,ledger}.py   slide themes;  fonts/ icons/ samples/
publish.py (IG/FB/YT/X/TikTok steps, idempotent via output/<name>/publish.json), xpost.py, tiktok.py, youtube.py, captions.py
metrics.py (→ runs/metrics.json), telegram_bot.py, stt.py, dm_setup.py, bot/ (Worker), meta_token.py, yt_token.py, x_token.py
content/ (one JSON per post: content/clips/, content/repos/)  output/ (gitignored)  runs/ (gitignored state, settings.json)
research/  sources.json  prompt_packs.json  strategy.json  publish_log.jsonl  docs/PROJECT_NOTES.md
```

## Content JSON schema
Top level: `theme`, `brand`, `handle`, `topic`, `caption` (= instagram), `captions`, `first_comment`, `sources` [urls],
optional `window`, `tape`, `voice` (leave out: reel.py picks the least-recently-used of `af_sarah`, `af_jessica`, `am_liam`,
`am_fenrir`, `am_puck`, `am_eric`, `am_adam`), `voice_speed` (1.1), `cover` {person, layout, photo_query, photo_pick, icons},
`design` (adaptive: see themes/adaptive.py docstring), `dm` {keyword, mode}, `comments`, `slides` [...].
Every slide may have `voiceover` (short, conversational, NOT a reading of the slide, only verified claims, ~7–15 words,
also on prompt slides). Target Reel under ~30 s.

Slide types (a theme supports a subset, see its docstring):
- `cover`: kicker, title, em (highlight substring), sub, tools[]
- `prompt`: prompt (`[PLACEHOLDERS]` in caps are highlighted) + neon: tag, name, title, sub, tip | ledger: label, name, note |
  adaptive: label, name, prompt, note | prompts theme: name, sub, prompt, tip, demo ({kind: reply, lines[]} |
  {kind: before_after, before, after, svg})
- `facts` (ledger): label, title, items [[key, value]] · `steps` (ledger): label, title, steps [[title, detail]] ·
  `limits`: label, title, items, cta · `cta`: title, title2, lines [[verb, text]]
- adaptive only: `list` (label, title, items [[title, detail]]) · `compare` (label, title, cols [{name, points[]}], 2-3) ·
  `stat` (label, value, title, sub). Text in `backticks` renders as code.
- prompts theme: `howto`: title, items [[title, detail]]; cover title without the number (`count` overrides).

## Theme contract (adding themes)
A module in `themes/` exports `render(data) -> list[str]` (one 1080x1350 HTML doc per slide, content in `.body`),
`ACCENT`, `ANIM_SEL`, `TYPE_SEL`, `DRAW_SEL`, `REEL_CSS`, `CC_ACTIVE` (+ optional `CC_CSS`, `configure(data)`).
Always visually check `contact.png` and a few Reel frames.

## Clips (Reels = hook-framed viral clips)
Black frame, brand line, hook text on top, clip below, "Source: @creator on X" (`clip.py`, yt-dlp fetch of one picked post).
Hook states OUR take (what it means / what to do with it), not a description of the screen. Clips go to IG Reel, FB Reel,
YouTube Short (+ X; never TikTok). QA checks framing and must-not-post content only, not facts.

## Running locally (Windows)
`python carousel.py content/<post>.json`, `python reel.py content/<post>.json [--voice X --no-voice]`,
`python news.py`. Deps: `pip install -r requirements.txt`, `python -m playwright install chromium`, ffmpeg.
Kokoro: `app/tts_env/python.exe voice.py` of the Pinokio app `E:\pinokio-new\api\Ultimate-TTS-Studio.git`
(env vars `KOKORO_PYTHON` / `KOKORO_HF_HOME`; read-only use, never modify Pinokio folders).

## Meta / tokens / secrets
App "AI Playbooks Publisher" (Live), Page id 1283376908201081, IG user id 17841424416174844. `.env` (gitignored) holds all
tokens; **never print or commit token values**. If the Page token dies: new Graph API Explorer token with the FULL
permission list (see docs/PROJECT_NOTES.md "Meta setup"; fewer permissions invalidate every page token), then
`meta_token.py`, `gh secret set META_PAGE_TOKEN`, `python dm_setup.py`. The same Meta login also serves the Starseed
brand: run Starseed's fb_token.py BEFORE meta_token.py.

## Studio behaviour
Self-repair: a failing step retries, then the **doctor** (prompts/doctor.md, opus) fixes content/code and the step reruns.
Never restart the Studio while a run is active. Telegram: owner messages go to the Studio chat bot; the SessionStart hook
(`tools/tg_digest.py`) prints new ones: analyse them first each session.
