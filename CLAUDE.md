# AI Playbooks — automated Instagram + Facebook page for AI tool tips & news

## Talk to the owner in Turkish
The owner (Cihat) communicates in **Turkish**. All published content is in **English** (international audience).

## What this project is
A fully automated, **zero-cost** pipeline for an Instagram + Facebook page — **AI Playbooks**, Instagram **@aiplaybooks.daily**, Facebook Page "AI Playbooks", GitHub `aiplaybooks/ai-playbooks` — that posts daily content about AI tools and agents: ChatGPT, Claude, Claude Code, Codex, Grok, Gemini, Cursor, etc.

Every day the pipeline should:
1. **Research** — `python news.py` collects the last ~36h from all sources in `sources.json` into `research/YYYY-MM-DD.json`; then web search covers the `manual` sources that block scripts (xAI/Grok news, ChatGPT release notes, Perplexity, Microsoft Copilot, big X announcements). Cover **all** popular tools (ChatGPT/OpenAI, Claude, Gemini, Grok, Codex, Cursor, Copilot, Perplexity, Meta AI, Mistral, DeepSeek ...), not just Anthropic.
2. **Select & verify** — pick the strongest topic (news if there is real news, otherwise an evergreen format: "X prompts for Y", Claude Code tips, tool comparisons). Check the last 30 days of `content/` to avoid repeats. **Every factual claim must be verified against an official source**; unverifiable claims don't go in. Put source URLs in the content JSON `sources` field.
3. **Write** — one content JSON in `content/YYYY-MM-DD_slug.json` (schema below), including the Instagram caption + hashtags.
4. **Produce** — `python carousel.py <content>` → PNG slides; `python reel.py <content>` → MP4 Reel.
5. **Approve** — first 2 weeks: owner approves every post (planned: via a GitHub Pull Request, merge = approve). Afterwards auto-approve.
6. **Publish** — Instagram Graph API (official, free, ~50 posts/24h) **and the linked Facebook Page** (Pages API, same Meta app/token): carousel + Reel. Planned to run in GitHub Actions on merge; images served via public URLs (GitHub Pages for a public repo, or Cloudflare R2 free tier for a private repo).
7. **Log** — append to a publish history (topic, date, IG link) for de-duplication and performance tracking.

## Decisions already made (don't re-litigate)
- **Free only.** No paid SaaS. Rejected: Metricool free plan (20 scheduled posts cap), vidIQ, Make/Zapier (need paid Metricool API). Chosen: direct Instagram Graph API.
- **Formats:** both carousel and Reel, generated from the same content JSON.
- **Design must vary**: each post can use a different theme (`themes/*.py`). Build a larger theme pool over time; pick theme by topic or rotate.
- **Images are code-rendered**, not AI-generated: HTML/CSS template → headless Chromium (Playwright) screenshot. Fonts are open-source (OFL/Inter license) and live in `fonts/`.
- **Music is generated in code** (`music.py`, procedural lo-fi) → no copyright issues. Optional: a folder of royalty-free tracks (YouTube Audio Library / Pixabay) via `reel.py --music`.
- **No real people's photos**, no brand logos imitation, no exaggerated/false claims. Financial topics get a "not financial advice" line.
- Reels: 1080x1920, 30fps, H.264 + AAC. Content kept inside IG safe zones (top ~190px, bottom ~330px reserved).

## Repo layout
```
carousel.py        render carousel PNGs (1080x1350) + contact.png overview
reel.py            render animated Reel (typewriter prompts, staggered fade-ups, progress bar, music,
                   Kokoro voice-over + word-level burned-in captions + music ducking)
voice.py           Kokoro TTS per slide -> vo_NN.wav + voice.json (word timings). Runs in Pinokio's env, called by reel.py
music.py           procedural royalty-free background track: python music.py out.wav <seconds>
news.py            daily news collector (stdlib only): RSS/Atom feeds, changelog pages, Hacker News -> research/<date>.json
publish.py         IG carousel + Reel and FB Page photo post + Reel via Graph API v25.0; media via gh-pages.
                   Resumable/idempotent (output/<name>/publish.json); --dry-run checks token + quota, posts nothing
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
fonts/             InterVariable, Fraunces, JetBrainsMono (+ licenses)
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
- `cta` (neon): title, title2, lines [[verb, text], ...]

## Theme contract (for adding new themes)
A theme module in `themes/` must export:
- `render(data) -> list[str]` — one full HTML document per slide, 1080x1350, content wrapped in an element with class `body` (reel.py fades it out between slides).
- `ACCENT` (progress bar color), `ANIM_SEL` (CSS selector list animated in order), `TYPE_SEL` (element that gets the typewriter effect, or ""), `DRAW_SEL` (element revealed left→right, or ""), `REEL_CSS` (overrides for 1080x1920: bigger type, safe-zone insets, hide swipe hints).
- `CC_ACTIVE` (caption color of the word being spoken; optional `CC_CSS` to restyle captions `#cc`).
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
- **post** flow (one at a time): write (prompts/write.md → content JSON + runs/<id>/write.json) → carousel → reel →
  qa (8 Reel frames + slides, prompts/qa.md, may fix + re-render) → approve (owner: Yayınla / Revize et (note → back to
  write) / Reddet (content JSON moved into the run dir)) → publish.py steps → log (publish_log.jsonl + git commit/push).
- Settings (UI ⚙): scan times, "Yayından önce onay" switch (owner wants it ON for now; if QA finds a problem the gate
  applies anyway). Windows toasts when candidates are ready / approval needed / errors.
- Claude steps run with `--permission-mode acceptEdits` and an allowlist (web, file tools, python carousel/reel/news).
- A failed node shows red; "Tekrar dene" resumes from that node. publish.py never double-posts on a retry.

## Where we left off (2026-09-24)
publish.py tested up to `upload` (media live on Pages); **no post has been published yet**. Studio built; first real
scan worked (7 candidates). **Next:** the owner picks a candidate → first full post run → owner approves the first real
post → check FB post visibility (dev mode; the app probably must be published: needs a 1024x1024 icon).

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
