You are the quality check for an AI Playbooks post before the owner sees it. Read CLAUDE.md first.

Post: `{content}`. Rendered output: `output/{name}/` (slide_NN.png, contact.png, reel.mp4).
Reel frames sampled for you: {frames}

## Check
Open `output/{name}/contact.png`, every `slide_NN.png` and the sampled Reel frames. Look for:
- text cut off, overflowing its box, overlapping other elements, or too small to read on a phone
- empty or broken slides, wrong characters (� boxes), placeholder text left in
- in Reel frames: text inside the Instagram safe zones (top ~190px, bottom ~330px), captions covering content
- typos, and claims in the slides/caption that go beyond the `sources` of the content JSON

## Fix
If something is wrong, edit `{content}` (usually shorten a text) and re-render with `python carousel.py {content}`
and, if the Reel is affected, `python reel.py {content}` (takes ~3 min). Check again. At most 2 fix rounds.
Don't change the theme or the `voice`.

## Output
Write `{result}`: `{{"ok": true|false, "fixed": ["what you changed"], "problems": ["what is still wrong"],
"summary_tr": "1-2 Turkish sentences for the owner"}}`. `ok` is false only if a problem remains that the owner must
see. Reply with one line: ok or not ok.
