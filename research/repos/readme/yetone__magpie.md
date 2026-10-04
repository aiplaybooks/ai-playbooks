# magpie

One place to pick every agent's model: Codex on DeepSeek, Claude Code
on Kimi, Gemini CLI on GLM, from the menu bar. [usemagpie.ai](https://usemagpie.ai)

[](https://discord.gg/vGSnD3ZKQF)

`magpie` is a single screen that lists each AI agent on your machine and
the model it is set to. Click a value, pick a model. That is the whole app.

It lives in the menu bar: click the icon and a panel drops down; the same
screen also opens as a normal window (`magpie`, or *Open magpie* in the tray menu),
and there is a terminal version (`magpie tui`) and a plain CLI.

```
 ◉ magpie

 ▸ Claude Code claude-fable-5-1[1m] ~/.claude/settings.json
 Codex gpt-6-astra effort medium
 Gemini CLI gemini-3.1-pro
 OpenCode anthropic/claude-sonnet-5 small anthropic/claude-haiku-4-5
 MiMo Code anthropic/claude-sonnet-5
 Pi openrouter/z-ai/glm-5.2:batch
 Goose anthropic/claude-sonnet-5
 Cursor auto
 Copilot CLI claude-fable-5

 ↑↓ agent · ←→ field · ↵ change · s save profile · p profiles · q quit
```

- **One small binary.** Under 15 MB with the desktop app (it uses the system
 webview through [Wails](https://wails.io), nothing bundled), 7 MB for the
 terminal-only build. macOS, Linux and Windows.
- **Edits config files surgically.** Only the one key you change is touched;
 comments, ordering and indentation in your `settings.json`, `config.toml`,
 `opencode.jsonc` or `config.yaml` survive intact. Writes are atomic.
- **One endpoint for every agent.** magpie runs a local gateway that speaks
 OpenAI chat completions, OpenAI Responses and the Anthropic Messages API,
 and forwards to whichever vendor serves the model. Codex, Claude Code,
 OpenCode and the rest all point at `http://127.0.0.1:3425/v1` and pick
 from one catalog; the translation between APIs happens in magpie, streaming
 and tool calls included.
- **Your subscriptions, shared.** Sign in to Claude Code, Codex (ChatGPT)
 or Copilot and that login shows up as a provider: every other agent can
 use its models through the gateway, with nothing copied and no key to
 paste.
- **Providers with one field.** Pick a preset (Anthropic, OpenAI, Gemini,
 DeepSeek, Kimi, GLM, MiniMax, StepFun, Qwen, Baidu Qianfan, Tencent Cloud Token Plan,
 Huawei Cloud MaaS, Volcengine Ark, Mistral, Groq, xAI, OpenRouter, Together,
 Fireworks, SiliconFlow, NVIDIA NIM, ModelScope, AiHubMix, PipeLLM, 302.AI, Ollama, LM Studio…),
 paste a key, done. Custom vendors need a name and a base URL. magpie never
 reads keys from your shell environment.
- **Real model lists, nothing compiled in.** With a key in hand magpie asks
 the vendor which models it serves and offers exactly those; the
 [models.dev](https://models.dev) catalog fills in names, reasoning efforts
 and the list for vendors that have none, and refreshes itself in the
 background once it goes stale. Choose which models each provider exposes,
 or expose them all — a model released this morning is in the picker on
 the next refresh.
- **Each agent's own model list.** Under an agent's name on the Agents page,
 "Showing 5 / 32 models" opens its list: click a model to take it out of
 that agent's picker (Codex's `/model` included, its ChatGPT models too) or
 put it back; other agents still use it, and a new model is shown.
- **Profiles.** Snapshot every agent's settings under a name and switch all of
 them back in one move.
- **Real logos, no framework.** Plain HTML over the system webview; brand
 icons from [lobehub/icons](https://github.com/lobehub/lobe-icons).

## Agents

| Agent | File | Fields |
| ------------ | --------------------------------- | --------------- |
| Claude Code | `~/.claude/settings.json` | provider, model, opus/sonnet/haiku/fable (through magpie) |
| Claude Desktop | `Claude/` + `Claude-3p/configLibrary/` in `~/Library/Application Support` (`%LOCALAPPDATA%` on Windows, `~/.config` on Linux) | provider (its third-party gateway mode: Code and Cowork on magpie, no Anthropic sign-in; restart Desktop) |
| Codex | `~/.codex/config.toml` | provider, model, effort |
| Gemini CLI | `~/.gemini/settings.json`, `~/.gemini/.env` | auth, model |
| OpenCode | `~/.config/opencode/opencode.json(c)` (`$OPENCODE_CONFIG_DIR`) | model, small |
| OpenChamber | `~/.config/openchamber/preferences.json` (`$OPENCHAMBER_DATA_DIR`; magpie's provider in OpenCode's config) | model, small (its own defaults, over OpenCode's) |
| MiMo Code | `~/.config/mimocode/mimocode.json(c)` | model, small |
| Pi | `~/.pi/agent/settings.json` | model |
| OmO (omo-ai) | `~/.omo/agent/settings.json` (+ `models.json`; `$OMO_CODING_AGENT_DIR`, `$SENPI_CODING_AGENT_DIR`) | model |
| Goose | `~/.config/goose/config.yaml` | model |
| Cursor CLI | `~/.cursor/cli-config.json` | model |
| Zed | `~/.config/zed/settings.json` (`$XDG_CONFIG_HOME` on Linux, `%APPDATA%\Zed` on Windows) | model (a `magpie` OpenAI-compatible provider; its catalog in Zed's picker) |
| VS Code (Chat) | `~/Library/Application Support/Code/User/settings.json` + `chatLanguageModels.json` (`~/.config/Code/User` on Linux, `%APPDATA%\Code\User` on Windows) | model (`chat.defaultModel`; a `magpie` Custom Endpoint group, its catalog in Chat's model picker; VS Code 1.122+, no Copilot sign-in or key needed) |
| JetBrains Air | `acp.json` in `~/Library/Application Support/JetBrains/Air` (`~/.config/JetBrains/Air` on Linux, `%APPDATA%\JetBrains\Air` on Windows) + `magpie-opencode.json` beside it | model (a `Magpie` ACP agent: OpenCode's `opencode acp` on magpie's provider alone, its models and routing groups in Air's model menu; needs OpenCode installed) |
| Copilot CLI | `~/.copilot/settings.json` | model |
| Crush | `~/.config/crush/crush.json` | large, small |
| DeepSeek Harness (dsh) | `~/.dsh/profiles/*/cordis.patch.yml` (`$DSH_HOME`; a custom provider, Magpie), or `~/.dsh/config.yaml` before dsh 0.1.5 | model, effort |
| Command Code | `~/.commandcode/settings.json` (+ `providers.json`) | model |
| fx | `~/.fx/settings.json` | model (a keyless `magpie` provider) |
| omp (oh-my-pi) | `~/.