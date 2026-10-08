# magpie

### Every agent's model. One place.

Claude Code on Kimi, Codex on DeepSeek, Gemini CLI on GLM, OpenCode on your ChatGPT plan. 
Switch them from the menu bar. One local gateway serves them all, and it moves to another account when a quota runs out.

[](https://github.com/yetone/magpie-releases/releases/latest) [](https://github.com/yetone/magpie/stargazers) [](https://discord.gg/vGSnD3ZKQF) [](LICENSE) 

**[Download](https://usemagpie.ai)** · **[Docs](https://usemagpie.ai/docs/start)** · **[Reference](docs/reference.md)** · **[Discord](https://discord.gg/vGSnD3ZKQF)** · **English** · [简体中文](README.zh-CN.md)

## Why magpie

You probably use more than one coding agent. Each one keeps its model in its own file, in its own format, with its own keys and base URLs. Each one also has its own idea of which vendors it supports. A subscription you pay for works in one agent and nowhere else. When it runs out at 3 pm, you start editing config files.

magpie puts all of it in one place:

**🎛 One screen for every agent** 
Over 35 agents in one list. Click a model and pick another. magpie changes only that one key in the agent's own config file. Comments, ordering and formatting stay as they were.

**🔌 One gateway for every API** 
`127.0.0.1:3425` speaks OpenAI Chat, OpenAI Responses, Anthropic Messages and Gemini. It translates between them, streaming, tool calls and reasoning included.

**🔀 Routing that keeps going** 
Put several models from several providers in a routing group. When one hits a rate limit or runs out of quota, the next one answers. Your agent never sees the error.

**🔑 Subscriptions you can share** 
Your Claude, ChatGPT, Copilot, Gemini or Grok sign-in becomes a provider that every other agent can use. There is no key to copy.

**🧩 Plugins** 
OpenCode auth plugins and pi provider packages from npm run in magpie as they do in their own apps. Any plan a plugin signs in to works in every agent. A plugin can also be gateway middleware that reads and rewrites every request and reply.

**📊 Usage and cost tracking** 
See tokens, cache hits, cost at list price, balances and quota windows for every provider and account. You can also set a limit for each key.

## Pick any model for any agent

Click a value and a filtered list opens. It holds every model of every provider you added, as `provider/model`. Pick one and the agent's config file is rewritten safely and atomically. Use **Profiles** to save the setup of every agent under one name ("Budget", "Focus") and switch them all at once.

magpie also lives in the **menu bar**. There is a tray panel on macOS, Windows and Linux, a full window, a **TUI** (`magpie tui`), a **web UI** (`magpie web`) and a plain **CLI**.

## Add providers with one field

Pick a preset and paste a key. That's it. The model list comes from the vendor itself, with names and reasoning levels filled in from [models.dev](https://models.dev), so a model released this morning shows up on the next refresh. No model list is built into magpie.

**Presets include** Anthropic · OpenAI · Google Gemini · DeepSeek · Kimi · Zhipu GLM · MiniMax · StepFun · Qwen · Baidu Qianfan · Tencent Cloud · Huawei Cloud MaaS · Volcengine Ark · Mistral · Groq · xAI · OpenRouter · Together · Fireworks · SiliconFlow · NVIDIA NIM · ModelScope · Ollama · LM Studio … and any OpenAI-compatible or Anthropic-compatible URL.

Already set up somewhere else? **Import** reads the providers you set up in CC Switch, Claude Code, Codex and Alma. **[Add to magpie](https://usemagpie.ai/docs/import)** links let a provider's website hand its config to magpie in one click.

## Routing that keeps going

A **routing group** is several models that an agent picks as one: `group/daily-coding`. The gateway spreads requests over every member's keys and accounts:

| Mode | What it does |
| --- | --- |
| `smart` | Of the subscriptions with quota left, use the one whose allowance renews soonest, so less is lost at the reset |
| `order` | Use the first model until it can't answer, then the next |
| `rotate` | Move to the next member on each turn |
| `usage` | Use the least-used member first |
| `pace` | Use the account with the most of its week left per hour until its reset |

Conversations **stay with the account that answered them** while the vendor's prompt cache is still worth keeping. **Intent routing** goes further: a small model you choose reads each new turn, so tests can go to the strong model and quick questions to the fast, cheap one. Groups can contain other groups. The Routing tab shows each decision live.

→ [Intent routing, in depth](https://usemagpie.ai/docs/intent)

## Sign in once, use it everywhere

An agent you're signed in to is a subscription with models behind it, so magpie offers it as a provider. Several accounts per subscription are supported, and magpie fails over between them.

- **Claude**: drives the real local `claude` binary and bridges your agent's tools over MCP
- **Codex / ChatGPT**: your ChatGPT plan's models in every other agent
- **GitHub Copilot**, **Gemini (Code Assist)**, **Antigravity**, **Grok (SuperGrok)**, **Devin**, **Cursor** and others
- **Any OpenCode auth plugin or pi package** from npm:

```sh
magpie plugin add opencode-gemini-auth # an OpenCode plugin from npm
magpie plugin add pi-antigravity # a pi package, the same way
magpie plugin login google-plugin # its own sign-in flow, in magpie
```

magpie runs plugins on [Bun](https://bun.sh), which it downloads the first time a plugin needs it. A plugin signs in, lists its models and makes each request. Agents use its models like any other provider's. Browse the community plugins at **[magpie-community/plugins](https://github.com/magpie-community/plugins)**, or [write your own](https://usemagpie.ai/docs/plugins).

A plugin can also be **gateway middleware**: JavaScript run inside magpie's gateway on what every agent sends and gets back, whatever the provider. `onRequest` can rewrite a request or turn it away, `onEvent` see