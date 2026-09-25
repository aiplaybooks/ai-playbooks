# AI Playbooks — automated Instagram + Facebook page for AI tool tips & news

## Talk to the owner in Turkish
The owner (Cihat) communicates in **Turkish**. All published content is in **English** (international audience).

## What this project is
A fully automated, **zero-cost** pipeline for an Instagram + Facebook page — **AI Playbooks**, Instagram **@aiplaybooks.daily**, Facebook Page "AI Playbooks", GitHub `aiplaybooks/ai-playbooks` — that posts daily content about AI tools and agents: ChatGPT, Claude, Claude Code, Codex, Grok, Gemini, Cursor, etc.

Every day the pipeline should:
1. **Research** — `python news.py` collects the last ~36h from all sources in `sources.json` into `research/YYYY-MM-DD.json`; then web search covers the `manual` sources that block scripts (xAI/Grok news, ChatGPT release notes, Perplexity, Microsoft Copilot, big X announcements). Cover **all** tools on the owner's list — ChatGPT/OpenAI, Claude, Gemini, Grok, Codex, Cursor, Copilot, Perplexity, Meta AI, Mistral, DeepSeek + big open-weight/Chinese model releases (Qwen, Kimi, GLM, MiniMax ...) — up to 2 news candidates per tool (36 h, else up to 7 days back; none → say so), tagged with `tool` so the UI can filter. The owner will extend the list later (image/video/audio/no-code/productivity tools were offered, not taken yet).
2. **Select & verify** — pick the strongest topic (news if there is real news, otherwise an evergreen format: "X prompts for Y", Claude Code tips, tool comparisons). Check the last 30 days of `content/` to avoid repeats. **Every factual claim must be verified against an official source**; unverifiable claims don't go in. Put source URLs in the content JSON `sources` field.
3. **Write** — one content JSON in `content/YYYY-MM-DD_slug.json` (schema below), including the Instagram caption + hashtags.
4. **Produce** — `python carousel.py <content>` → PNG slides; `python reel.py <content>` → MP4 Reel.
5. **Approve** — first 2 weeks: owner approves every post (planned: via a GitHub Pull Request, merge = approve). Afterwards auto-approve.
6. **Publish** — Instagram Graph API (official, free, ~50 posts/24h) **and the linked Facebook Page** (Pages API, same Meta app/token): carousel + Reel. Planned to run in GitHub Actions on merge; images served via public URLs (GitHub Pages for a public repo, or Cloudflare R2 free tier for a private repo).
7. **Log** — append to a publish history (topic, date, IG link) for de-duplication and performance tracking.

## Decisions already made (don't re-litigate)
- **Free only.** No paid SaaS. Rejected: Metricool free plan (20 scheduled posts cap), vidIQ, Make/Zapier (need paid Metricool API). Chosen: direct Instagram Graph API.
- **Formats:** both carousel and Reel, generated from the same content JSON.
- **Design must vary — per topic** (owner, 2026-09-24): background, symbols, colors, fonts, shapes all come from the
  news itself. Default theme is `adaptive`: the write step (Claude) art-directs a `design` block per post (palette, font
  trio from the OFL pool, shape, pattern, label/prompt style, code-drawn SVG cover art + icon). `ledger`/`neon` stay as
  fixed looks but aren't the default.
- **Two pillars: news AND copy-paste prompt packs** (owner, 2026-09-24): the first posts were all news; the page's
  promise is also "copy-paste prompts". Scout adds 3 `kind: "prompts"` candidates per scan (different everyday areas);
  write.md renders them with the `prompts` theme. Prompts are our own wording, never copied from other accounts.
- **Reel/Short cover = the carousel's first slide** (owner, 2026-09-24): publish.py makes `cover.jpg` (9:16, slide centered
  on a blurred copy) → IG `cover_url`, FB reel thumbnail (needs pages_manage_engagement + pages_read_user_content; the
  token has them since 2026-09-25), YouTube thumbnails.set (works only once the channel may set Shorts covers; never fails the
  step). reel.py also starts the cover slide fully drawn so the first frame is a clean cover. The owner set the covers of
  the first (Gemini) post by hand.
- **Images are code-rendered**, not AI-generated: HTML/CSS template → headless Chromium (Playwright) screenshot. Fonts are open-source (OFL/Inter license) and live in `fonts/`.
- **Music is generated in code** (`music.py`, procedural lo-fi) → no copyright issues. Optional: a folder of royalty-free tracks (YouTube Audio Library / Pixabay) via `reel.py --music`.
- **Carousel cover = a photo + big hook headline** (owner, 2026-09-25; refs: @chatgptips style): full-bleed image on
  top, Anton upper-case headline with a yellow highlight, "SWIPE FOR MORE". The owner wants a **well-known person tied to
  the topic** on the cover (e.g. the company's CEO) for reach. Only freely licensed real photos: Wikimedia Commons
  (CC BY / CC BY-SA / public domain, via its API) with "Photo: <author> · <license>" on the cover and in the caption.
  Never AI-generated likenesses of real people, no fake quotes/endorsements. No fitting person → Flux image
  (Forge API, `flux1-schnell-fp8.safetensors`, ~85-90 s per image on the RTX 4060). Sample: output/flux-test/.
- **Reels = hook-framed viral clips, not the carousel's own Reel** (owner, 2026-09-25; refs: @chatgptips): black frame,
  brand line, hook text on top, the clip below, "Source: @creator on X" (`clip.py`). The owner picks the clip (pastes
  an X link); clip.py fetches that one post with yt-dlp. Risk the owner accepted: credit is not a license (takedowns
  possible); ask creators for permission where possible. They go to YouTube Shorts too (owner changed this on
  2026-09-25, accepting the Content ID / strike risk; carousels keep their own voiced video there): title = clip title +
  hook, the IG/FB comments (prompts) go into the YouTube description. Discovery: `viral.py`
  (YouTube API = signal only, never downloaded; Reddit API needs manual approval since 2025-11 → not available).
  Hooks must stay truthful (no unverified $/follower claims from the source post), no fake verified badge.
- No brand logo imitation, no exaggerated/false claims. Financial topics get a "not financial advice" line.
- Reels: 1080x1920, 30fps, H.264 + AAC. Content kept inside IG safe zones (top ~190px, bottom ~330px reserved).

## Repo layout
```
carousel.py        render carousel PNGs (1080x1350) + contact.png overview; slide 1 = themes/hookcover.py when the post
                   has a `cover` block + output/<post>/cover_image.jpg
cover.py           cover image: Wikimedia Commons photo of `cover.person` (licensed, credited) or Flux scene via Forge
reel.py            render the carousel as a voiced video: now only for YouTube Shorts (IG/FB Reels = viral clips) (typewriter prompts, staggered fade-ups, progress bar, music,
                   Kokoro voice-over + word-level burned-in captions + music ducking)
voice.py           Kokoro TTS per slide -> vo_NN.wav + voice.json (word timings). Runs in Pinokio's env, called by reel.py
clip.py            hook-frame Reel for a picked clip (file or X/post URL): python clip.py <src> --hook ".." [--title] [--credit]
viral.py           trending AI video finder -> research/<date>_viral.json (YouTube signal; Reddit when API approved)
music.py           procedural royalty-free background track: python music.py out.wav <seconds>
news.py            daily news collector (stdlib only): RSS/Atom feeds, changelog pages, Hacker News -> research/<date>.json
publish.py         IG carousel + Reel and FB Page photo post + Reel via Graph API v25.0; media via gh-pages.
                   Resumable/idempotent (output/<name>/publish.json); --dry-run checks token + quota, posts nothing
metrics.py         performance collector (YouTube Data+Analytics, IG media + insights, FB page/post/reel) -> runs/metrics.json
                   (local only, 30-day history; Studio runs it every 6 h; UI: 📊 Performans). A missing permission
                   is listed under "needs" (none since the 2026-09-25 token)
comments           publish.py step: the content JSON's optional `comments` list is posted as our first comments under
                   every IG/FB post of the run (clips: prompts go there, caption says "in the comments"). Needs
                   instagram_manage_comments + pages_manage_engagement; prepare checks before anything is posted
telegram_bot.py    Telegram remote control inside the Studio (@aiplaybooks_studio_bot, owner-only: TELEGRAM_BOT_TOKEN +
                   TELEGRAM_CHAT_ID in .env): candidates, approval previews, publish links, errors; text + voice commands
stt.py             speech to text for voice commands (faster-whisper in the Pinokio TTS env, model cache in .cache/)
yt_token.py        one-time YouTube OAuth -> YT_* in .env
studio.py          AI Playbooks Studio: local workflow engine + web UI at http://localhost:8787 (see below)
studio/index.html  the n8n-style UI (vanilla JS, no build)
prompts/           scout.md, write.md, qa.md: prompts for the headless `claude -p` steps of the Studio
runs/              Studio run state + logs + settings.json (gitignored)
publish_log.jsonl  one line per published post (links), committed by the Studio
sources.json       source list: feeds, pages (parser: anthropic_news | dated_sections), hn queries, manual (web-search only)
research/          one candidate list per day (commit it: history of what was available)
themes/
  neon.py          dark bg, lime accent, chat-input prompt cards. slide types: cover, prompt, cta
  ledger.py        cream "newspaper/market terminal": serif headlines, mono labels, ticker tape,
                   terminal prompt boxes. slide types: cover, facts, steps, prompt, limits
  prompts.py       copy-paste PROMPT PACK series ("7 prompts to ..."): fixed series layout (big number + card deck cover,
                   chat-box prompt cards with COPY badge, code-drawn `demo`: example reply or before/after SVG), colors/
                   fonts from the same `design` block as adaptive (default: banner violet + blue). slide types: cover,
                   prompt, howto, cta (+ any adaptive type). Long prompts auto-shrink to fit. samples/prompts_*.json
  adaptive.py      DEFAULT. Whole look from the post's `design` block (see its docstring); validates fonts, fixes
                   low contrast, sanitizes SVG. slide types: cover, facts, steps, prompt, list, compare, stat, limits, cta
fonts/             OFL pool (+ licenses): Inter, Manrope, DM Sans, Outfit, Sora, Space Grotesk, Unbounded, Syne,
                   Bricolage Grotesque, Archivo, Anton, Bebas Neue, Fraunces, Playfair Display, DM Serif Display,
                   Instrument Serif, JetBrains Mono, Space Mono, IBM Plex Mono (from github.com/google/fonts)
content/           one JSON per post (source of truth)
output/            generated files (gitignored)
samples/           reference outputs from the first session (overview PNGs + reels)
```

## Content JSON schema
Top level: `theme`, `brand`, `handle`, `topic` (shown in ledger masthead), `caption`, `sources` [urls],
optional `window` (terminal title in ledger), `tape` ([label, text, isUp] for ledger ticker),
`voice` (Kokoro voice; leave it out for new posts, reel.py assigns one), `voice_speed` (default 1.1), `slides` [...].

Every slide may have `voiceover`: a short spoken line (conversational, NOT a reading of the slide; only verified
claims; ~7–15 words, also on prompt slides: very short lines leave dead air). Target Reel length 30–40s.
Slides without it are silent.

**Voices (owner's choice, vary them):** only `af_sarah`, `af_jessica` (female), `am_liam`, `am_fenrir`, `am_puck`,
`am_eric`, `am_adam` (male) — the `VOICES` list in reel.py. Don't reuse the same voice every time: reel.py gives a post
without a valid `voice` the least-recently-used pool voice (by content file order) and saves it into the JSON.

Slide types (a theme supports a subset — see its docstring):
- `cover`: kicker, title, em (substring of title to highlight), sub, tools[] (neon chips)
- `prompt`: prompt (use `[PLACEHOLDERS]` in caps; they get highlighted), plus
  neon: tag, name, title, sub, tip | ledger: label, name, note
- `facts` (ledger): label, title, items [[key, value], ...]
- `steps` (ledger): label, title, steps [[title, detail], ...] (detail containing "mcp." renders as code)
- `limits` (ledger): label, title, items [..], cta
- `cta` (neon, adaptive): title, title2, lines [[verb, text], ...]
- adaptive only: `list`: label, title, items [[title, detail], ...] · `compare`: label, title, cols [{name, points[]}]
  (2-3 cols) · `stat`: label, value (big number/word), title, sub. Adaptive `prompt`: label, name, prompt, note.
  Text in `backticks` renders as code. Top-level `design` block: see themes/adaptive.py docstring.
- prompts theme: `prompt`: name, sub, prompt, tip, demo ({kind: reply, lines[]} | {kind: before_after, before, after
  svg}) · `howto`: title, items [[title, detail], ...] · cover title without the number (drawn big; `count` overrides).

## Theme contract (for adding new themes)
A theme module in `themes/` must export:
- `render(data) -> list[str]` — one full HTML document per slide, 1080x1350, content wrapped in an element with class `body` (reel.py fades it out between slides).
- `ACCENT` (progress bar color), `ANIM_SEL` (CSS selector list animated in order), `TYPE_SEL` (element that gets the typewriter effect, or ""), `DRAW_SEL` (element revealed left→right, or ""), `REEL_CSS` (overrides for 1080x1920: bigger type, safe-zone insets, hide swipe hints).
- `CC_ACTIVE` (caption color of the word being spoken; optional `CC_CSS` to restyle captions `#cc`).
- optional `configure(data)`: reel.py calls it first so a theme can set ACCENT/CC_ACTIVE/REEL_CSS per post.
  With voice-over, reel.py sets `.wrap` bottom to 540px and puts captions in a band above the IG bottom safe zone.
Always visually check output (open `contact.png` and a few Reel frames) before calling a theme done.

## Running locally (Windows)
```
pip install -r requirements.txt
python -m playwright install chromium
winget install ffmpeg        (or: conda install -c conda-forge ffmpeg)
python carousel.py content/2026-09-24_claude-tradingview.json
python reel.py content/2026-09-24_claude-tradingview.json
```
A Reel takes ~2–3 min (one screenshot per frame).
Voice-over: `python reel.py <content> [--voice am_liam] [--speed 1.1] [--no-voice]` (`--voice` overrides one render, not saved).

### Kokoro setup (don't pip-install it into the system Python)
Kokoro runs from the existing Pinokio app **Ultimate-TTS-Studio** at `E:\pinokio-new\api\Ultimate-TTS-Studio.git`
(conda env `app/tts_env`, Python 3.10, kokoro 0.9.4, torch CUDA). reel.py calls `app/tts_env/python.exe voice.py ...`
with `HF_HOME=<app>/cache/HF_HOME`, `HF_HUB_OFFLINE=1` and `CUDA_HOME=E:\pinokio-new\bin\miniforge\Library`
(transformers imports deepspeed, which crashes without CUDA_HOME; the `LNK1181 aio.lib/cufile.lib` lines it prints are harmless).
Override with env vars `KOKORO_PYTHON` / `KOKORO_HF_HOME`. Read-only use — never modify Pinokio folders.

## Meta (Instagram + Facebook) setup — done 2026-09-24
- Meta app **AI Playbooks Publisher** (App ID 1451989886792783), Business type, **Unpublished** (development mode).
  Use cases: Instagram (API setup with *Facebook login*), Manage everything on your Page (+ Messenger, unused).
  Facebook Login for Business configuration "Publisher" (916780787888379) — needed for Graph API Explorer user tokens.
- Facebook Page "AI Playbooks" id 1283376908201081; Instagram @aiplaybooks.daily (IG user id 17841424416174844). IG quota: 100 posts / 24h.
- `meta_token.py`: short-lived Explorer user token (in .env) → never-expiring Page token. `.env` (gitignored) holds
  META_APP_ID, META_APP_SECRET, META_PAGE_TOKEN, FB_PAGE_ID, IG_USER_ID. GitHub Secrets: META_PAGE_TOKEN, FB_PAGE_ID, IG_USER_ID.
  Never print or commit token values. If the token dies (password change, permissions removed): new Explorer token → rerun meta_token.py → `gh secret set`.
- Likely gotcha: Facebook posts made by an app in development mode may be visible only to app role users → the app
  probably has to be **published** (needs privacy policy URL, category, icon).
  Done 2026-09-24: Privacy Policy URL + Data deletion instructions URL set in App settings → Basic
  (both `https://aiplaybooks.github.io/ai-playbooks/privacy.html`). Still missing before publishing: app icon (1024x1024).

## YouTube (Shorts) — set up 2026-09-24
- Channel **AI Playbooks** @ai-playbooks-daily (UCBGx9BWEshj4Qe7inBbf3vQ). Google Cloud project skilled-mark-509618-e8
  (number 625929791406), YouTube Data API v3 + YouTube Analytics API, OAuth consent "In production" (unverified is fine
  for our own use), Desktop client in `client_secret.json` (gitignored). `yt_token.py` → YT_* keys in .env
  (scopes: youtube.upload, youtube.readonly, yt-analytics.readonly).
- `publish.py` step `yt_short` (Studio node "YouTube Short"): the Reel as a Short, title = cover title + #Shorts.
- **Until YouTube's API audit passes, API uploads are locked to private** → owner makes them public in YouTube Studio.
  Audit form answers + evidence screenshots: output/youtube-audit/ (FORM_CEVAPLARI.md). Submitted: not yet (2026-09-24).
- Promise in our privacy policy (keep it true when building analytics): YouTube API data is stored only locally,
  refreshed or deleted at least every 30 days, deleted within 7 days if access is revoked.
- Site pages on gh-pages: index.html (mentions the YouTube channel), privacy.html, terms.html.

## GitHub Pages (public media URLs) — done 2026-09-24
- Served from the orphan branch **`gh-pages`** (root), base URL **https://aiplaybooks.github.io/ai-playbooks/**.
  Contents: `index.html`, `privacy.html` (privacy policy + data deletion section, for publishing the Meta app), `.nojekyll`,
  `media/<post>/...` (media for Graph API; `media/test/slide.png` is a test file).
- To add media: `git worktree add <tmp> gh-pages` → copy files → commit → push; the Pages build takes ~1 min, check the URL
  returns 200 before handing it to Meta. Limits: 100 MB/file, ~1 GB site → prune old `media/` now and then.
- Instagram `image_url` officially supports **JPEG only** → publish.py must convert the PNG slides to JPEG.

## AI Playbooks Studio (the daily pipeline) — built 2026-09-24
Owner's design: an n8n-like local page showing the workflow node by node + today's news; the owner only picks a
candidate (and approves the preview), everything else is automatic.
- `pythonw studio.py --no-browser` starts at Windows logon (shortcut in the user's Startup folder); desktop shortcut
  "AI Playbooks Studio.url" opens http://localhost:8787. Only one instance (port check).
- **scan** flow, daily at `scan_times` (default 08:00 + 18:00, owner asked for 2 scans/day; a slot missed while the PC
  was off runs at startup): news.py → `claude -p` with prompts/scout.md → `research/<date>_<HHMM>_candidates.json`
  (4-8 candidates, Turkish summaries for the owner, official sources) → owner picks one in the UI.
- **post** flow (one at a time): write (prompts/write.md → content JSON + runs/<id>/write.json) → cover (cover.py:
  Wikimedia photo first, Flux when none) → carousel → reel (YouTube only) → qa (slides + video frames, prompts/qa.md,
  may fix + re-render) → approve (owner: Yayınla / Revize et (note → back to
  write) / Reddet (content JSON moved into the run dir)) → publish.py steps (ig_carousel, fb_photos, yt_short) → log (publish_log.jsonl + git commit/push).
- **clip** flow (UI tab "Viral": owner pastes a link): fetch (yt-dlp + info.json + 8 frames) → hook (prompts/hook.md →
  content/clips/<date>_clip-<id>.json, "kind": "clip") → frame (clip.py) → approve → upload → ig_reel → fb_reel →
  yt_short → comments → log.
  Output in output/clips/<name>/. The scan's collect step also runs viral.py (YouTube trend signals for the Viral tab).
- Settings (UI ⚙): scan times, "Yayından önce onay" switch (owner wants it ON for now; if QA finds a problem the gate
  applies anyway). Windows toasts when candidates are ready / approval needed / errors.
- Claude steps run with `--permission-mode acceptEdits` and an allowlist (web, file tools, python carousel/reel/news).
- A failed node shows red; "Tekrar dene" resumes from that node. publish.py never double-posts on a retry.

## Where we left off (2026-09-24)
**First real post is live** (Gemini 3.8 TTS, adaptive theme, 2026-09-24 21:00): IG carousel + Reel, FB photo post + Reel,
all via the Studio. Graph API reports the FB post privacy EVERYONE and the FB Reel published; still to confirm with
the owner that a logged-out / non-admin account really sees the FB posts (app is in development mode). If not: publish
the Meta app (needs a 1024x1024 icon; privacy policy URL is already set).
Timing of that first run (incl. a revision + one failed upload retry): stats/timings.jsonl.
Lessons: never restart the Studio while a run is active (now it resumes runs, but still check); the QA step is the
slowest (~5-7 min) because it re-renders the Reel after fixes.

## Next steps (in order — owner's priority, 2026-09-24)
1. ~~Voice-over with Kokoro~~ — done. ~~News sources + collector~~ — done (`news.py`, `sources.json`).
   Tiers: `official` can back a claim; `signal` (Simon Willison) and `community` (Hacker News) are hints only.
2. ~~Daily run~~ — done as the Studio (prompts/scout.md, write.md, qa.md).
3. **Publishing to Instagram + Facebook Page:** Repo: https://github.com/aiplaybooks/ai-playbooks (public, account
   `aiplaybooks`; media via GitHub Pages). Meta developer app, IG Professional account linked to a FB Page,
   long-lived token (GitHub Secrets), `publish.py` (IG: media containers → carousel container → publish; Reels: video
   container, poll status, publish; FB Page: multi-photo post + video/reel), public media URLs (GitHub Pages or R2),
   approval via PR for the first 2 weeks, publish log.
4. ~~Scheduling~~ — done: the Studio's own scheduler (PC must be on; missed slots catch up at logon).
5. **More themes** (3–4) + theme selection logic. (Name decided: brand "AI Playbooks", handle "@aiplaybooks.daily".)
