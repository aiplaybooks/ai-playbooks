Answer me with HTML 

 Super Fast&nbsp;&nbsp;|&nbsp;&nbsp;ASD-STE100&nbsp;&nbsp;|&nbsp;&nbsp;Explainer Videos&nbsp;&nbsp;|&nbsp;&nbsp;One File, Offline 

 An agent skill. Ask a hard question, get a page you can actually read instead of a wall of text. The model writes about 1/8 of the tokens it would need to hand-write the HTML. 

 Website · Install · Examples · Videos · Always-on mode · Reference · 简体中文 

Once installed, ask questions the way you always do:

```
> Explain the TCP three-way handshake
> Map out how the modules in this repo fit together
> Redis or Memcached for our cache?
```

The agent writes a short Markdown draft and hands it to the CLI that ships with the skill. About 50 ms later you have a page:

https://github.com/user-attachments/assets/d3063a28-5dfd-4c44-a562-be901c49b249

 24-second demo. Turn the sound on for the music. 

## Why not just ask for HTML?

You can. Models write decent HTML now. But most of what they write is not content. We counted the tokens in 9 pages the model wrote by hand, 4,893 tokens on average:

| Part of the page | Share | With this skill |
| :--- | ---: | :--- |
| SVG diagrams: coordinates and paths | 47% | The CLI writes it |
| CSS | 15% | The CLI writes it |
| HTML tags | 17% | The CLI writes it |
| Text | 21% | The model writes it, as Markdown |

With this skill the model writes only a Markdown draft. For the same questions that was 612 tokens on average, **about 1/8 of the hand-written HTML**. Less to write means less to wait for (3 topics × 3 runs, medians, Claude Sonnet 5.5, a plain Claude Code setup):

| | Ask for HTML directly | Answer me with HTML | |
| :--- | ---: | ---: | :--- |
| Tokens the model writes | 4,893 | **612** | **8× fewer** |
| Time | 31 s | **12 s** | **2.6× faster** |

 The same question, the same model, answered both ways. Both pages are usable. 

The token counts are saved in [bench/corpus/tokens.json](bench/corpus/tokens.json), so `node bench/corpus.mjs` gives the same numbers every time. The pages themselves are a [download](https://github.com/QingYunA/answer-me-with-html/releases/download/v0.4.14/bench-corpus-2026-10-07.zip). The bill drops less than the writing, about 15% here, because every turn also reads the system prompt, your question and the conversation, with or without the skill. See [where the cost goes](bench/README.md#where-the-cost-goes).

Explainer videos save even more: about 18× fewer output tokens and 12× faster in [a small test](bench/README.md#explainer-videos).

## Install

You need [Node.js](https://nodejs.org/) 20 or newer. There is no `npm install` step. The CLI is bundled inside the skill.

### Let your agent install it (recommended)

Paste this into Claude Code, Codex, Cursor, OpenCode or any other agent:

> Install Answer me with HTML: read https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/INSTALL.md and follow it.

[INSTALL.md](INSTALL.md) is written for agents. It installs the plugin in Claude Code and the skill in other agents, keeps an existing install, asks you nothing, and ends with one report after checking the result with the TCP three-way handshake page. If your agent cannot open links, use `npx -y skills add QingYunA/answer-me-with-html -g -y -a ` (for Claude Code, `-a claude-code`).

### Claude Code plugin

Run this inside Claude Code:

```
/plugin marketplace add QingYunA/answer-me-with-html
/plugin install answer-me-with-html@answer-me-with-html
```

### One command

```bash
npx skills add QingYunA/answer-me-with-html
```

It asks which agents to install into. The installer, [vercel-labs/skills](https://github.com/vercel-labs/skills), supports more than 70 agents.

 Manual install 

Copy the `skills/answer-me-with-html` folder into your agent's skill folder. For Claude Code:

```bash
git clone --depth 1 https://github.com/QingYunA/answer-me-with-html.git /tmp/answer-me-with-html
cp -R /tmp/answer-me-with-html/skills/answer-me-with-html ~/.claude/skills/answer-me-with-html
```

Skill folders for other agents: Codex `~/.codex/skills/`, Cursor `~/.cursor/skills/`, OpenCode `~/.config/opencode/skill/`.

No setup is needed after install. **We recommend turning on [always-on mode](#always-on-mode-recommended)**: the agent then adds a page to every conclusion, not only the hard ones. It takes one rule in your rules file.

## What you ask, what you get

| You ask | You get |
| :--- | :--- |
| "Explain the TCP three-way handshake" | A sequence diagram, a state diagram and a flag table |
| "How are the modules in this repo organized?" | A folder tree plus a call graph |
| "Redis or Memcached?" | A comparison table with ✓ and ✗, then a verdict |
| "What's wrong with this paragraph?" | Each sentence annotated, with the problem words and fixes |
| "How did Kubernetes come about?" | A timeline with the key moments highlighted |
| "Plan the cache change" | The real code from your files, and the open decisions as options you answer on the page |
| "How do I show hidden files with `ls`?" | No page. A one-line question gets a one-line answer |

The agent decides when a page is worth it: related concepts, multi-step flows, multi-way comparisons. You can also just say "explain it in HTML".

Pages are saved in `~/.answer-me-with-html/pages/`. The buttons in the top-right corner switch the theme and light/dark mode, collect your reply, and copy the Markdown that produced the page.

## How is this different from Archify or GenUI plugins?

[Archify](https://github.com/tt-a1i/archify) makes one interactive diagram from a JSON spec. GenUI plugins such as [dsh-genui](https://github.com/omdsh-dev/dsh-genui) show components inside one chat app. This skill answers the whole question as one page: text, tables, code and diagrams, from a Markdown draft, in any agent that can run a shell command. See the [full comparison](docs/compare.md).

## Explainer videos

Karpathy's ladder for understanding LLM output ends with explainer videos. Ask for one in 3Blue1Brown style: "make a 3b1b-style 