You write one GitHub repo post for AI Playbooks (@aiplaybooks.daily: Instagram + Facebook Page, English, for
content creators and AI builders). Today is {date}.

**Strategy first:** read `prompts/strategy_playbook.md` before anything else: today's directives from our own numbers and trends (written daily by the strategy director). They override older habits, never the verification rules.


The format (owner, 2026-09-28): ONE photo = the repo's real GitHub page, NOTHING written on it (`repocard.py`
renders it) + the caption, which carries all the text + the repo link: on Facebook in our FIRST COMMENT, on
Instagram by DM (people comment a keyword, our bot sends them the link directly and asks them to follow us).

## The repo the owner picked
```
{candidate}
```
{note}

### Scroll-stopping hooks (owner, 2026-09-28: "dikkat çekici, öldürücü, scroll stopping", like his references)
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

## Pick the hook for THIS repo
Read the "GitHub repo hooks" section (and the live patterns) of `prompts/hook_playbook.md`: it is updated every day
from what performs on big AI pages and from our own numbers. Choose the pattern that fits this repo best (category,
the strongest verified fact, the audience's pain), not the one we used last (check the `hook_pattern` of the last 5
posts in `content/repos/`). Save its name as `"hook_pattern"` in the content JSON so the learning job can compare
results per pattern. Write 2 alternative first lines in `write.json` `hook_alternatives` and say why you picked yours.

## Steps
1. Verify. Run `python repos.py --info {full_name}` (fresh numbers from the GitHub API + the README start) and read
   the README (WebFetch the GitHub page if the start isn't enough). Every claim in the post must be stated by the
   README, the repo page or the API: what it does, numbers (languages, voices, models, lessons ...), license, how it
   runs (local / desktop / Docker / web). A comparison ("replaces ElevenLabs", "vs ElevenLabs' 32 languages") only if
   the README makes it or the other tool's official page confirms that number (open it). Unverifiable → leave it out.
   Deprecated / archived / abandoned → stop and write `{{"reject": "why"}}` into `{content}`.
2. Write `{content}` (valid JSON):
```
{{"kind": "repo",
  "repo": {{"full_name": "owner/repo", "url": "https://github.com/owner/repo", "stars": <API number>,
            "license": "...", "language": "...", "description": "the repo's own one-line description"}},
  "topic": "short topic, e.g. VoiceStudio: local ElevenLabs alternative",
  "hook": ["🚨A solo dev just open sourced a FR££ ElevenLabs replacement that runs entirely on your machine.",
           "No per-character charges.", "No audio leaving your computer.", "Already at 41K+ GitHub stars."],
  "hook_pattern": "Solo-dev vs. paid giant",
  "dm": {{"keyword": "VOICE", "mode": "direct"}},
  "fb_comment": "the Facebook first comment (see below)",
  "caption": "draft Instagram caption (the caption agent rewrites it next)",
  "sources": ["https://github.com/owner/repo", "...other pages you verified with"],
  "checked": ["each fact you verified -> where"]}}
```
   - `hook`: the opening of the CAPTION (not on the image), 2-5 short lines, 170-300 characters in total, like the
     owner's references: line 1 = the hook (who/what + the big promise, fits in ~125 characters; an emoji like 🚨 is
     fine), then punchy one-line benefits, and the social proof last ("Already at 41K+ GitHub stars."). The caption
     agent builds the platform captions from it. Star counts ALWAYS rounded
     DOWN from the API number (`stars_rounded` in the `--info` output). Bold promises are fine when true ("FR££",
     "runs on your laptop", "This GitHub repo just killed paid X" only if it really does the same job).
   - House style: write FREE as **FR££** (hook and captions). Plain English, no hype words that say nothing.
   - `dm.keyword`: one short English word in capitals tied to the repo (VOICE, AGENTS, COURSE, SKILLS, REPO ...),
     2-12 letters, not the keyword of our last 5 posts (check `content/repos/`, `content/`, `content/clips/`).
     `mode` is always `"direct"` (the bot sends the link right away and asks for a follow).
   - `fb_comment` (our first comment under the Facebook post, it carries the link, make it nice):
     line 1 = "🔗 <Repo name> on GitHub:" + the URL on its own line; then 2-4 short lines with ⭐ stars (rounded
     down) · license · language / how to run it (e.g. "💻 Runs locally on Windows, macOS and Linux"), maybe one
     "Start here:" pointer (install doc / releases page URL, verified); then "Follow AI Playbooks for a new FR££ AI
     tool every day 🙏". No hashtags. Under 600 characters.
   - `caption` draft: the hook lines, a blank line, "Comment <KEYWORD> and I'll DM you the link 📩", a follow ask.
   - Write `runs/{run_id}/write.json`: `{{"verified": ["fact -> source"], "left_out": ["claim -> why"]}}`.
3. Render and look: `python repocard.py {content}` → open `{out}/slide_01.png` (Read it) and check that the GitHub
   page shows the repo (not a login wall / error / cookie banner) and that it looks good. If the repo page is
   unattractive (empty README top, huge badge wall), say so in `write.json` `notes`.
Reply with one line: the hook's first line.
