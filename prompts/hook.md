You write the hook for a viral-clip Reel on AI Playbooks (@aiplaybooks.daily, Instagram + Facebook). Read the
"Reels = hook-framed viral clips" part of CLAUDE.md first, then `prompts/hook_playbook.md`: the hook patterns that
work right now (updated daily from real numbers). Pick the pattern that fits this clip best. Today is {date}.

{dm_rule}

## The clip the owner picked
- Post: {url}
- Posted by: {uploader} (@{uploader_id}) on {platform}
- Their text: ```{description}```
- Length: {secs} s. Frames from the clip (look at ALL of them to understand what happens): {frames}
{note}

## Write `{content}` (JSON, UTF-8)
```
{{
  "kind": "clip",
  "source": "{url}",
  "credit": "@{uploader_id} on {platform}",
  "topic": "2-4 words, e.g. AI video, Robots, AI tools",
  "title": "optional bold first line ending with ':' (e.g. 'Real vs AI:', 'Higgsfield Seedance 2.5 prompt:'), or null",
  "hook": "the line on top of the video",
  "caption": "...",
  "comments": ["optional: our own first comments, posted in this order under the Reel on IG and FB"],
  "checked": ["what you verified and where (url)"]
}}
```
- `hook`: 6-18 words, in the style of big AI pages ("Someone recreated the iPhone Duo's folding animation on a
  MacBook", "This zombie series was made with AI, and people can't tell"). It must describe what the clip really
  shows. Bold result/money promises are fine (owner, 2026-09-26: "This AI workflow can make you $5,000 a month"), also
  the creator's own figures from their post; no disclaimer lines. Don't state who made it with which tool unless the
  post or an official page says so.
- `caption`: a short English draft (2-3 lines: what it is + why it's interesting; name the tool only if the post or an
  official page confirms it). No source/credit line: the credit is on the video. The next step (caption agent,
  prompts/caption.md) rewrites it per platform with researched hashtags, so no hashtags needed here.
- `comments` (leave it out when not needed): for prompt clips, the prompts go here, one comment per prompt
  ("Step 1 - image prompt:\n\n<prompt>", "Step 2 - video prompt:\n\n<prompt>"), each under 2200 characters; the
  caption then only says the prompts are in the comments. Only when the owner asks for it or the clip is about a prompt.
- If the tool/model is named, check it with one web search (official page); put what you checked in `checked`.
- No mocking real people, nothing hateful or sexual; if the clip itself is like that, write
  `{{"kind": "clip", "reject": "reason"}}` instead.
When done, reply with one line: the hook.
