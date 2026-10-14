[](https://github.com/Alishahryar1/free-claude-code/blob/main/LICENSE)
[](https://www.python.org/downloads/)
[](https://github.com/astral-sh/uv)
[](https://github.com/Alishahryar1/free-claude-code/actions/workflows/tests.yml)
[](https://pypi.org/project/ty/)
[](https://github.com/astral-sh/ruff)
[](https://github.com/Delgan/loguru)

[Quick Start](#quick-start) · [Providers](#choose-a-provider) · [Clients](#connect-your-client) · [Integrations](#optional-integrations) · [Manage](#manage-your-installation)

 Independent open-source project. Not affiliated with or endorsed by Anthropic. Claude and Claude Code are trademarks of Anthropic. 

## What You Get

- **61 ToS-friendly providers. 1.3B+ free tokens every month.** Use free, paid, subscription, and local models from one searchable UI without putting your account at risk. FCC follows provider terms and removes integrations if they stop being allowed.
- **11 coding agents. One model catalog.** Run [Claude Code](https://code.claude.com/docs/en/overview), [Codex](https://github.com/openai/codex), [Pi](https://github.com/earendil-works/pi), [OpenCode](https://github.com/anomalyco/opencode), [Cline](https://github.com/cline/cline), [Hermes](https://github.com/NousResearch/hermes-agent), [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), [Grok Build](https://github.com/xai-org/grok-build), [Muse Code](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2/), [Aider](https://aider.chat/), or [VS Code Chat](https://code.visualstudio.com/) with your FCC models.
- **Keep coding through provider outages.** After retries are exhausted, FCC automatically tries your next configured model without making you restart the turn. This works across every client.
- **Up to 90% lower token usage.** Optional [RTK](https://github.com/rtk-ai/rtk) filters common command output, and [Headroom](https://github.com/headroomlabs-ai/headroom) compresses tool results. Five FCC optimizations handle quota probes, command-prefix detection, titles, suggestions, and filepaths without calling a provider.
- **Native Code sessions in your browser.** Choose a folder and run Codex in the browser with real-time and background support. Freely switch providers/models in the same session. Support for switching harnesses in the same session coming soon!
- **Terminal, desktop, IDE, or phone.** Work through native launchers, [VS Code](https://code.visualstudio.com/), [Codex App](https://learn.chatgpt.com/docs/app), [JetBrains](https://www.jetbrains.com/), [Discord](https://discord.com/), or [Telegram](https://telegram.org/).
- **Voice notes in. Code out.** Talk to your agent using local [Whisper](https://github.com/openai/whisper) or [NVIDIA NIM](https://docs.nvidia.com/nim/speech/latest/asr/deploy-asr-models/whisper.html) transcription.
- **Agent capabilities stay intact.** Stream responses, use tools, preserve native interleaved thinking for maximum performance, send images, and route [Fable](https://www.anthropic.com/claude/fable), [Opus](https://www.anthropic.com/claude/opus), [Sonnet](https://www.anthropic.com/claude/sonnet), and [Haiku](https://www.anthropic.com/claude/haiku) independently with compatible models.

Free-tier availability and limits are controlled by each provider and may change.

 Claude Code running with FCC. 

 A native Codex session in FCC's browser UI. 

## Quick Start

### 1. Install

macOS/Linux:

```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh
```

Windows PowerShell:

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1")))
```

When prompted, choose at least one coding agent and optionally enable [RTK](https://github.com/rtk-ai/rtk) + [Headroom](https://github.com/headroomlabs-ai/headroom) token optimization for supported agents.

### 2. Start FCC

#### Windows

Open **Free Claude Code** from your desktop or Start menu.

#### macOS

Open **Free Claude Code** from your desktop or Applications folder.

#### Linux

Run:

```bash
fcc-server
```

FCC opens the Admin UI after starting. On Windows and macOS, use the tray or
menu-bar icon to open Admin, restart, or quit. When using `fcc-server`, keep its
terminal open.

### 3. Configure NVIDIA NIM

1. Create an API key at [build.nvidia.com/settings/api-keys](https://build.nvidia.com/settings/api-keys).
2. Open the Admin UI URL from the server log.
3. Open NVIDIA NIM in **Providers**, click **Add key**, paste the key, and click **Save**.
4. Leave `MODEL` on the default `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`, or search the model dropdown and select another model.
5. Click **Apply** to save your model selection.

To protect the local proxy with a bearer token, enable **Proxy Authentication**
in Admin.

### 4. Run Your Coding Agent

Claude Code:

```bash
fcc-claude
```

Codex:

```bash
fcc-codex
```

Pi:

```bash
fcc-pi
```

OpenCode 2:

```bash
fcc-opencode
```

Cline:

```bash
fcc-cline
```

Hermes:

```bash
fcc-hermes
```

DeepSeek Harness Web:

```bash
fcc-dsh
```

Grok Build:

```bash
fcc-grok
```

Muse Code:

```bash
fcc-muse
```

Aider:

```bash
fcc-aider
```

 Select an FCC model from Claude Code's native /model picker. 

## Choose A Provider

1. Open a provider link below for its key, models, or setup instructions.
2. In the Admin UI, configure the listed setting. For OpenAI / ChatGPT
 subscription access, use **Providers → OAuth providers** instead.
3. Search the `MODEL` dropdown and select a model. If the provider cannot list
 models, enter ` / ` manually.
4. Click **Apply**.

Optional: add an ordered **Fallback Models** list under **Model Config**. It
applies to every connected client. A failed request may reach and consume usage
from more than one provider before succeeding.

Provider modals support numbered API keys. Use **Add key**, remove rows, or drag their handles to reorder them. FCC uses key 1.

For another API en