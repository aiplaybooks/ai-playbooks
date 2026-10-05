# why many token when few do trick

**Caveman make your AI agent say less and read less. Code stay exact. Brain still big.**

 33.2% fewer input tokens through the proxy 54 Claude Code runs, 18 of 18 answers right 
 129.8× smaller web pages for the agent caveman browse vs a Playwright snapshot 
 1.4 to 2.4× cheaper with caveman-style output Adobe Research , eight models 

Cited by **[Adobe Research](https://arxiv.org/abs/2606.24083)** · A/B tested by **[JetBrains](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/)** · Remade for Elasticsearch on **[Elasticsearch Labs](https://www.elastic.co/search-labs/blog/elastic-caveman-ai-token-reduction)** 
**#1** on [Hacker News](https://news.ycombinator.com/item?id=47647455) · **#1** on GitHub Trending · *"No way this actually works."* [ThePrimeagen](https://www.youtube.com/watch?v=L29q2LRiMRc)

**[How it talks](#how-caveman-talks) · [Install](#install) · [The numbers](#the-numbers) · [The proxy](#big-rock-the-proxy) · [What you get](#what-you-get) · [In the wild](#in-the-wild)**

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

## How caveman talks

Caveman is a voice, not broken grammar. Every reply follows the same structure:

| Rule | What it means |
|---|---|
| **Answer first** | `[thing] [action] [reason]. [next step].` No greeting, no "let me", no recap, no "hope this helps" |
| **One idea per sentence** | Built on [ASD-STE100](https://www.asd-ste100.org/), the controlled English written for aircraft maintenance manuals: 20 words max, active voice, one term per thing |
| **Meaning never dropped** | Articles can go. *not*, *never*, *no*, *only* never go. Numbers and units stay exact |
| **Payload verbatim** | Code, commands, paths, and error messages untouched, character for character |
| **Quiet tool runs** | No chatter between tool calls. One line per phase, one line with the result |
| **Knows when to stop** | Security warnings, irreversible actions, step-by-step orders, and confused users get full sentences. Then grunt resumes |
| **Never performs** | No "me think", no caveman prefix. If caveman phrasing isn't shorter, plain wins |
| **Your prompts stay yours** | Never rewritten. [Research say that backfire](#the-numbers) |

Every reply runs a check before it sends: opener that announces the plan, deleted; closer that recaps, deleted; every negation, path, and number still there.

## Install

```bash
npx skills add JuliusBrussee/caveman -g
```

Works in Claude Code, Codex, Gemini CLI, Cursor, Windsurf, Cline, Copilot, and [30+ more](./INSTALL.md). Type `/caveman` if it doesn't start on its own. Say `stop caveman` to go back. One rock. That it.

 Other ways in : Claude Code plugin, Gemini, every agent at once, Windows, uninstall 

```bash
# Claude Code plugin, auto-starts every session
claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman

# Gemini CLI
gemini extensions install https://github.com/JuliusBrussee/caveman

# Every agent on your machine at once, plus the Claude Code statusline badge (Node.js 22.13+)
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/v3.1.0/install.sh | bash
```

Windows, PowerShell 5.1+:

```powershell
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/v3.1.0/install.ps1 | iex
```

Changed your mind: `npx -y github:JuliusBrussee/caveman -- --uninstall`

Install broke? Open your agent in this repo and say *"Read CLAUDE.md and INSTALL.md, install caveman for me."* Agent fix own brain.

## The numbers

Outside labs first, then ours. Nothing rounded up. Red rows stay red.

| Who | Setup | Result |
|---|---|---|
| **[Adobe Research](https://arxiv.org/abs/2606.24083)**, CAVEWOMAN paper (cites this repo) | Caveman-style output, eight models, five datasets | **Cost cut 1.4 to 2.4× per model, up to 3×** |
| **[Elastic](https://www.elastic.co/search-labs/blog/elastic-caveman-ai-token-reduction)**, Elasticsearch Labs | Caveman mode remade for Elasticsearch, eight live MCP scenarios | **63.6% fewer response tokens.** *"Zero information loss."* |
| **[JetBrains](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/)** | 86 real coding tasks, paired A/B | **No measurable quality loss** (p = 0.82). 8.5% fewer output tokens |

Two findings shaped caveman. Adobe found that cavemanning *your* prompt makes answers longer and worse, so caveman never touches your prompt. JetBrains found that agent sessions are mostly code and tool calls, which the skill leaves alone. So caveman grew a second rock that shrinks what the agent *reads*: [the proxy](#big-rock-the-proxy).

### The proxy: 33.2% fewer input tokens

| File type | The file, through caveman | File saved | Whole Claude Code session, 3 runs | Session saved |
|---|---:|---:|---:|---:|
| CSV | 28,041 → **314** | **98.9%** | 165,823 → 74,484 | **55.1%** |
| Logs | 22,810 → **348** | **98.5%** | 148,807 → 74,068 | **50.2%** |
| YAML | 20,447 → **178** | **99.1%** | 132,124 → 71,027 | **46.2%** |
| Test output | 18,806 → **203** | **98.9%** | 150,377 → 108,514 | **27.8%** |
| JSON | 18,837 → **281** | **98.5%** | 147,975 → 108,939 | **26.4%** |
| HTML | 21,670 → 21,670 | none yet | 140,6