You write one post for AI Playbooks (@aiplaybooks.daily). Read CLAUDE.md first (content JSON schema, voice-over
rules, voices, safe claims). Today is {date}.

## The topic the owner picked
```
{candidate}
```
{note}

## Steps
1. Verify. Open every official source above (and search for the official page if a claim needs one). Every factual
   claim in the post (names, dates, versions, plans/prices, availability, limits, how to enable it) must be confirmed on
   an official page. Anything you cannot confirm is left out. Evergreen posts: prompts and tips must be accurate for the
   tools they name; don't claim features a tool doesn't have.
2. Design the look for THIS topic. Use `"theme": "adaptive"` and write a `design` block; read the docstring at the top
   of `themes/adaptive.py` for every field, the font list (`FONTS`) and the patterns (`PATTERNS`).
   The owner wants every post to look made for its news: background, symbols, colors, fonts and shapes all come from
   the subject. Think like an art director:
   - `mood`: one line, the visual idea (e.g. "late-night recording studio, neon voice waveform" for a voice model,
     "clean terminal, green-on-black, sharp corners" for a CLI tool, "sunny spreadsheet grid, friendly" for Excel prompts).
   - `palette`: pick colors that evoke the subject and its product's world (an ambience, not a copy of a logo). Dark or
     light, as the idea needs. The theme fixes low contrast automatically, but aim for readable choices.
   - `fonts`: a display face with character that suits the mood + a readable body face + a mono.
   - `shape`, `background.pattern`, `label`, `prompt`: match the idea (a code tool: terminal prompt, sharp radius,
     grid/scanlines; a creative tool: rounded, glow, waves ...).
   - `art`: an SVG illustration for the cover (viewBox 0 0 900 460), drawn in code about the subject: e.g. a voice
     waveform, a terminal window with a command, a chat bubble stack, a chart, a sandbox box around a file tree.
     Simple, bold, geometric shapes with the palette (use var(--accent), var(--accent2), var(--ink), var(--muted),
     var(--surface)); no text in the art except short code or symbols; no real logos, no people.
   - `icon`: a tiny SVG symbol for the subject (viewBox 0 0 24 24, stroke="currentColor" or fill="currentColor").
   - `deco` is optional (a faint full-page ornament); leave it out unless it clearly adds to the idea.
   Don't repeat the look of the most recent posts in `content/` (check their `design`).
   **Prompt packs** (the candidate's `kind` is `"prompts"`): use `"theme": "prompts"` instead. Its layout is fixed (the
   series look); the `design` block (same fields, read the docstring of `themes/prompts.py`) only sets this pack's
   palette, fonts, pattern and `icon`: make them fit the pack's subject. Leave `design` out for the brand default
   (neon violet + blue from the channel banner). No `art` needed: the cover draws a deck of the pack's prompt cards.
3. Write `{content}` following the schema in CLAUDE.md and the existing files in `content/` as examples:
   - 7-10 slides (Instagram carousel max is 10). First slide `cover`. Slide types of the adaptive theme: cover, facts,
     steps, prompt, list, compare, stat, limits, cta (fields in the theme docstring and CLAUDE.md). Wrap inline code in
     `backticks`. Use the slide types that tell the story best (e.g. `stat` for one striking number, `compare` for
     tool comparisons).
   - Prompt packs: `cover` (title WITHOUT the number, e.g. "prompts to learn any language with AI": the number is
     drawn big next to it), 5-8 `prompt` slides, optional `howto` (3 tips to get more out of the prompts), `cta`.
     Every prompt slide: `name` (2-4 words, e.g. "The conversation partner"), `sub` (the benefit in one line),
     `prompt` (your OWN wording, 150-330 characters, specific, copy-paste ready, [PLACEHOLDERS] in caps for what the
     reader fills in; never copy other accounts' prompts), plus `demo` or `tip` (not both on long prompts):
     Mark 1-3 key words per prompt as `**KEY WORDS**` (caps, bold with a marker line), like the library packs do.
     **Library packs** (the candidate has a `pack` block, from `prompt_packs.json`): the owner picked this ready-made
     pack. Use its 7 prompts in its order, with its `name`s, `sub`s and prompt texts (you may tighten wording or fix a
     claim, keep the [PLACEHOLDERS] and **KEY WORDS**); `cover` = headline / `headline_em` as `em` / person from the
     pack; the cover slide's title/em = the pack's `title`/`em`. Money / social media packs: a confident, practical
     design (not a pastel look); every pack still gets its own palette, fonts and pattern for its subject.
     `demo` shows what the prompt gives you: `{{"kind": "reply", "lines": [2-3 short lines of a realistic answer]}}`, or
     for image prompts `{{"kind": "before_after", "before": "<svg viewBox='0 0 400 250'>…", "after": "<svg …>"}}` (a
     simple code-drawn scene showing the edit; no people, no real photos, no logos).
   - **`cover` block (top level, required)**: the carousel's first slide is a photo + big hook headline (see CLAUDE.md,
     "Carousel cover"). It replaces the theme's own cover slide, but still write slide 1 as a normal `cover` slide.
     `{{"headline": "...", "em": "...", "person": "..." | null, "photo_query": ["..."], "photo_pick": {{...}} | null}}`
     - `headline`: the scroll-stopping hook in the style of big AI news pages, 8-22 words, ends with ":" when the
       carousel continues it ("Claude can now teach you any language like a private tutor. Here are 7 prompts to
       try:", "Google's new Gemini TTS can clone your voice from a 30-second clip"). News facts (what launched, versions,
       dates) must be verified. Prompt packs / money topics may promise the result boldly (owner, 2026-09-26): "This AI
       agent setup can make you $5,000 a month. 7 prompts to build it:" is fine. No disclaimer lines ("not financial
       advice" etc.), anywhere. `em`: 1-4 words of it to highlight in yellow.
     - `person`: the best-known real person directly tied to the topic, whose photo makes people stop: the company's
       CEO/founder (OpenAI: Sam Altman, Google/Gemini: Sundar Pichai or Demis Hassabis, Anthropic/Claude: Dario Amodei,
       xAI/Grok: Elon Musk, Microsoft/Copilot: Satya Nadella, Meta: Mark Zuckerberg, Nvidia: Jensen Huang, ...) or the
       person the news is about. The pipeline fetches a freely licensed photo from Wikimedia Commons and credits it.
       The headline must not put words in their mouth or suggest they endorse our post. `null` only when nobody fits.
     - Image generation is OFF: the cover is always a real, freely licensed photo. When `person` is null (or may have
       no photo on Commons), pick a topic photo yourself: run `python cover.py --search <content file name without
       .json> "query one" "query two"` (2-3 plain English nouns per query, e.g. "laptop desk night", "cash money",
       "stock chart screen"), look at the previews in `output/<name>/photo_cands/` (Read the jpgs) and copy the JSON
       line of the best one into `photo_pick`: sharp, bright or moody, tied to the topic, room at the bottom for the
       headline; no text/logos/watermarks, no screens showing someone else's content. Nothing fits → other words.
       Also write `photo_query` (the queries, best first) as the fallback.
   - `caption`: a short English draft (hook line + 2-3 lines). The next step (caption agent, prompts/caption.md)
     rewrites it per platform with researched hashtags; no sources, credits or hashtags needed here.
   - `sources`: the official URLs you used.
   - `voiceover` on every slide: conversational, 7-15 words, only verified claims; whole video ~30-40 s (it becomes
     a YouTube Short; Instagram/Facebook get only the carousel).
   - Leave out `voice` (reel.py assigns one).
   - Keep texts short enough for the slide design (look at how long the fields are in the example files).
4. Write `{result}`: `{{"content": "{content}", "verified": ["claim -> source url", ...], "left_out": ["claims you
   could not verify"]}}`.
Do not render or publish; the pipeline does that next. When done, reply with one line: the content file path.
