&nbsp;&nbsp;&nbsp;

 &nbsp;&nbsp;&nbsp;

 🇨🇳 中文 •
 🇹🇼 繁體中文 •
 🇯🇵 日本語 •
 🇵🇹 Português •
 🇧🇷 Português •
 🇰🇷 한국어 •
 🇪🇸 Español •
 🇩🇪 Deutsch •
 🇫🇷 Français •
 🇮🇱 עברית •
 🇸🇦 العربية •
 🇷🇺 Русский •
 🇵🇱 Polski •
 🇨🇿 Čeština •
 🇳🇱 Nederlands •
 🇹🇷 Türkçe •
 🇺🇦 Українська •
 🇻🇳 Tiếng Việt •
 🇵🇭 Tagalog •
 🇮🇩 Indonesia •
 🇹🇭 ไทย •
 🇮🇳 हिन्दी •
 🇧🇩 বাংলা •
 🇵🇰 اردو •
 🇷🇴 Română •
 🇸🇪 Svenska •
 🇮🇹 Italiano •
 🇬🇷 Ελληνικά •
 🇭🇺 Magyar •
 🇫🇮 Suomi •
 🇩🇰 Dansk •
 🇳🇴 Norsk 

 Persistent memory compression system built for Claude Code . 

 Quick Start •
 How It Works •
 Search Tools •
 Documentation •
 Configuration •
 Troubleshooting •
 License 

 Claude-Mem seamlessly preserves context across sessions by automatically capturing tool usage observations, generating semantic summaries, and making them available to future sessions. This enables Claude to maintain continuity of knowledge about projects even after sessions end or reconnect.

---

## Quick Start

Install claude-mem for Grok Bot:

```bash
npx claude-mem install --ide grok-bot
```

Grok Bot has no host hooks, so we watch the chat log files. Default is CMEM Pro, the hosted memory. Local observer is opt-in: `--provider host`. Installing this plugin does not install Cursor.

**Awareness push pilot (LFG + Orifice):** needle observations (`decision`, `bugfix`, `security_alert`, `sensitive`) are appended as dated `- YYYY-MM-DD [awareness] …` lines into that bot's `memory/log/YYYY-MM.md`. Grok Bot already re-reads the log from disk. This does not write `profile.md`, user-memory, or project memory. Disable with `CLAUDE_MEM_GROK_BOT_AWARENESS_ENABLED=false`.

Install with a single command:

```bash
npx claude-mem install
```

The installer sets everything up first, then asks you to sign in to claude-mem in your browser (email magic link — no card required). Signing in provisions a memory key for your account and unlocks the **claude-mem observer** with a **30 Day Free Trial**: memory runs off-plan, so you get up to 100% more usage from your plan. When the free trial ends, memory automatically falls back to your Anthropic plan unless you subscribe. After sign-in you pick your memory provider — the claude-mem observer, your own OpenRouter or Gemini key, or your Anthropic plan.

Prefer to skip the sign-in? Pass an explicit `--provider` flag, set `CLAUDE_MEM_ONLINE_OPTIN=false`, or run in CI/non-interactive shells — the installer completes without any account interaction.

Or install for OpenCode:

```bash
npx claude-mem install --ide opencode
```

Or install for **T3 Code** (Codex and Claude Code providers):

```bash
npx claude-mem install --ide t3code
```

The installer discovers T3 Code's enabled providers, registers native Claude-Mem plugins in their configured homes, and supports T3-managed Codex. Restart T3 Code, trust the provider's hooks when prompted, and start a new thread. See the [T3 Code integration guide](https://docs.claude-mem.ai/t3code-integration) for custom server settings, status, and removal.

Or install for Antigravity CLI ([setup guide](https://docs.claude-mem.ai/antigravity-cli/setup)):

```bash
npx claude-mem install --ide antigravity
```

Or install for OMP (Oh My Pi):

```bash
npx claude-mem install --ide omp
```

Or install the native Pi extension or DeepSeek Harness plugin:

```bash
npx claude-mem install --ide pi
npx claude-mem install --ide dsh --dsh-profile tui
```

Pi and DeepSeek Harness use the worker runtime. See [native harness setup](docs/native-harness-integrations.md) for capture, recall, and troubleshooting.

Or install from the plugin marketplace inside Claude Code:

```bash
/plugin marketplace add thedotmack/claude-mem

/plugin install claude-mem
```

Restart Claude Code. Context from previous sessions will automatically appear in new sessions.

> **Note:** Claude-Mem is also published on npm, but `npm install -g claude-mem` installs the **SDK/library only** — it does not register the plugin hooks or set up the worker service. Always install via `npx claude-mem install` or the `/plugin` commands above.

### 🦞 OpenClaw Gateway

Install claude-mem as a persistent memory plugin on [OpenClaw](https://openclaw.ai) gateways with a single command:

```bash
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

The installer handles dependencies, plugin setup, AI provider configuration, worker startup, and optional real-time observation feeds to Telegram, Discord, Slack, and more. See the [OpenClaw Integration Guide](https://docs.claude-mem.ai/openclaw-integration) for details.

**Key Features:**

- 🧠 **Persistent Memory** - Context survives across sessions
- 📊 **Progressive Disclosure** - Layered memory retrieval with token cost visibility
- 🔍 **Skill-Based Search** - Query your project history with mem-search skill
- 🖥️ **Web Viewer UI** - Real-time memory stream at the worker URL printed on startup
- 💻 **Claude Desktop Skill** - Search memory from Claude Desktop conversations
- 🔒 **Privacy Control** - Use ` ` tags to exclude sensitive content from storage
- ⚙️ **Context Configuration** - Fine-grained control over what context gets injected
- 🤖 **Automatic Operation** - No manual intervention required
- 🔗 **Citations** - Reference past observations with IDs through the worker API or view all in the web viewer

---

## Documentation

📚 **[View Full Documentation](https://docs.claude-mem.ai/)** - Browse on official website

### Getting Started

- **[Installation Guide](https://docs.claude-mem.ai/installation)** - Quick start & advanced installation
- **[Usage Guide](https://docs.claude-mem.ai/usage/getting-started)** - How Claude-Mem works automatically
- **[Search Tools](https://docs.claude-mem.ai/usage/search-tools)** - Query your project history with natural language
- **[Cloud Sync](https://docs.claude-mem.ai/cloud-sync)** - Back up your memories to cmem.ai — no daemon, the worker syncs on write

### Best Practices

- **[Context Engineering](https://docs.claude-mem.ai/context-engineering)** - AI agent context 