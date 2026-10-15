# why many token when few do trick

**Caveman make your AI agent say less and read less. Code stay exact. Brain still big.**

 33.2% fewer input tokens, whole sessions 54 Claude Code runs , 18 of 18 answers right 
 54% cheaper with Auto, same score 85 coding tasks vs Opus 5.5 at xhigh, interim 
 397 → 76 tokens for one test run Blocks vs | tail -20 
 1.4 to 2.4× cheaper with caveman-style output Adobe Research , eight models 

Cited by **[Adobe Research](https://arxiv.org/abs/2606.24083)** · A/B tested by **[JetBrains](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/)** · Remade for Elasticsearch on **[Elasticsearch Labs](https://www.elastic.co/search-labs/blog/elastic-caveman-ai-token-reduction)** 
**#1** on [Hacker News](https://news.ycombinator.com/item?id=47647455) · **#1** on GitHub Trending · *"No way this actually works."* [ThePrimeagen](https://www.youtube.com/watch?v=L29q2LRiMRc)

**[Install](#install) · [Six rocks](#six-rocks-one-install) · [Proof](#proof) · [Say less](#say-less-the-caveman-voice) · [Read less](#read-less-332-fewer-input-tokens) · [Auto](#auto-54-cheaper-same-score) · [Blocks](#blocks-code-mode-script-written-once) · [Commands](#commands) · [Caveman Cloud](#caveman-cloud)**

---

 Normal agent · 63 tokens 
 Caveman agent · 20 tokens 

> The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using useMemo to memoize the object.

> New object ref each render, so React re-renders. Wrap the prop in `useMemo`.

**Same fix. 63 token become 20. Brain still big.**

Pick your club:

| Skill | Same answer | Tokens |
|---|---|---:|
| `/caveman` | New object ref each render, so React re-renders. Wrap the prop in `useMemo`. | 20 |
| `/ultracave` | Inline object prop, new ref, re-render. `useMemo`. | 14 |
| `/megacave` | 新參照致重繪。`useMemo`。 | **13** |

 Token counts: tiktoken o200k. 

## Install

```bash
npx @caveman-ai/cli@latest
```

One command. Mac, Linux, Windows. Caveman find your agents and your logins, show what it change. Press Enter. Done. Needs Node.js 22.13+.

After that, plain `claude` stays caveman'd. So do Codex, Gemini CLI, OpenCode, and [30+ more](./INSTALL.md). It runs on your machine, with your keys and your Claude Pro/Max login. One rock. That it.

 Had caveman before 4.0? Say @latest , or the old copy on your machine wins. Already set up? caveman setup opens the screen again. Only want shorter answers? Get just the skill . 

## Six rocks, one install

New in 4.0: caveman is six parts. All on after install. Each has its own switch.

| Rock | What it does | Measured |
|---|---|---|
| **[Say less](#say-less-the-caveman-voice)** | Agent answers short. Code stays exact | 63 → 20 tokens, same fix |
| **[Read less](#read-less-332-fewer-input-tokens)** | Logs, JSON, CSV, test output shrink before the model reads them | **33.2%** fewer input tokens per session |
| **[Auto](#auto-54-cheaper-same-score)** · new | Picks the model and the effort for each ask | **54%** cheaper than Opus at xhigh, same score |
| **[Blocks](#blocks-code-mode-script-written-once)** · new | Code mode: agent keeps the scripts it writes and runs them again | **397 → 76** tokens for one test run |
| **[Waste fixes](#smaller-rocks)** | Finds where your tokens go and fixes it. New: keeps the prompt cache warm while you pause | Not measured yet |
| **[Browse](#smaller-rocks)** | Web pages come back compressed | **129.8×** smaller page |

`caveman status` shows what is on. `caveman off browse` turns one off. Only Auto needs an account, and it is free. [4.0.0 release notes](https://github.com/JuliusBrussee/caveman/releases/tag/v4.0.0)

## Proof

Outside labs first. Ours come with each rock below. Nothing rounded up. Red rows stay red.

| Who | Setup | Result |
|---|---|---|
| **[Adobe Research](https://arxiv.org/abs/2606.24083)**, CAVEWOMAN paper (cites this repo) | Caveman-style output, eight models, five datasets | **Cost cut 1.4 to 2.4× per model, up to 3×** |
| **[Elastic](https://www.elastic.co/search-labs/blog/elastic-caveman-ai-token-reduction)**, Elasticsearch Labs | Caveman mode remade for Elasticsearch, eight live MCP scenarios | **63.6% fewer response tokens.** *"Zero information loss."* |
| **[JetBrains](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/)** | 86 real coding tasks, paired A/B | **No measurable quality loss** (p = 0.82). 8.5% fewer output tokens |

Two findings shaped caveman. Adobe: cavemanning *your* prompt makes answers worse, so caveman never touches your prompt. JetBrains: agent sessions are mostly code and tool calls, which the voice leaves alone. So caveman grew rocks that shrink what the agent *reads* and what it *runs on*.

## Say less: the caveman voice

**A voice, not broken grammar. Every reply follows the same structure.**

| Rule | What it means |
|---|---|
| **Answer first** | `[thing] [action] [reason]. [next step].` No greeting, no "let me", no recap |
| **One idea per sentence** | Built on [ASD-STE100](https://www.asd-ste100.org/), the controlled English of aircraft maintenance manuals: 20 words max, active voice, one term per thing |
| **Meaning never dropped** | Articles can go. *not*, *never*, *no*, *only* never go. Numbers and units stay exact |
| **Payload verbatim** | Code, commands, paths, and error messages untouched, character for character |
| **No theater** | No "me think". No chatter between tool calls. If caveman phrasing isn't shorter, plain wins |
| **Knows when to stop** | Security warnings, irreversible actions, and confused users get full sentences. Then grunt resumes |
| **Your prompts stay yours** | Never rewritten. [Research say that backfire](#proof) |

Ten dev questions on claude-opus-5-5:

| Instruction | Output tokens |
|---|---:|
| None | 