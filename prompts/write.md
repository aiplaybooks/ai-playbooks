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
2. Pick the theme. Available themes (check each module's docstring in `themes/` for the slide types it supports):
   `ledger` (news, launches, how-tos: cover, facts, steps, prompt, limits) and `neon` (prompt collections: cover,
   prompt, cta). Use the one that fits; if both fit, pick the one NOT used by the most recent file in `content/`.
3. Write `{content}` following the schema in CLAUDE.md and the existing files in `content/` as examples:
   - 7-10 slides (Instagram carousel max is 10). First slide `cover`.
   - `caption`: English, hook in the first line, 2-4 short lines, a save/follow nudge, 4-8 relevant hashtags.
     Financial topics: add "Not financial advice."
   - `sources`: the official URLs you used.
   - `voiceover` on every slide: conversational, 7-15 words, only verified claims; whole Reel ~30-40 s.
   - Leave out `voice` (reel.py assigns one).
   - Keep texts short enough for the slide design (look at how long the fields are in the example files).
4. Write `{result}`: `{{"content": "{content}", "verified": ["claim -> source url", ...], "left_out": ["claims you
   could not verify"]}}`.
Do not render or publish; the pipeline does that next. When done, reply with one line: the content file path.
