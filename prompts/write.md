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
3. Write `{content}` following the schema in CLAUDE.md and the existing files in `content/` as examples:
   - 7-10 slides (Instagram carousel max is 10). First slide `cover`. Slide types of the adaptive theme: cover, facts,
     steps, prompt, list, compare, stat, limits, cta (fields in the theme docstring and CLAUDE.md). Wrap inline code in
     `backticks`. Use the slide types that tell the story best (e.g. `stat` for one striking number, `compare` for
     tool comparisons).
   - `caption`: English, hook in the first line, 2-4 short lines, a save/follow nudge, 4-8 relevant hashtags.
     Financial topics: add "Not financial advice."
   - `sources`: the official URLs you used.
   - `voiceover` on every slide: conversational, 7-15 words, only verified claims; whole Reel ~30-40 s.
   - Leave out `voice` (reel.py assigns one).
   - Keep texts short enough for the slide design (look at how long the fields are in the example files).
4. Write `{result}`: `{{"content": "{content}", "verified": ["claim -> source url", ...], "left_out": ["claims you
   could not verify"]}}`.
Do not render or publish; the pipeline does that next. When done, reply with one line: the content file path.
