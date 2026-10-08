Orca

 中文 · 日本語 · 한국어 · Español · Français · Português 

 The AI Orchestrator for 100x builders. 
 Run Codex, ClaudeCode, OpenCode or Pi side-by-side — each in its own worktree, tracked in one place.

 Download Orca 

## Features

### Mobile Companion

Monitor and steer your agents from your phone — get notified when an agent finishes and send follow-ups from anywhere.

[iOS App Store](https://apps.apple.com/us/app/orca-ide/id6766130217) · [Android APK 0.0.52](https://github.com/stablyai/orca/releases/download/mobile-android-v0.0.52/app-release.apk) · [Docs →](https://www.onorca.dev/docs/mobile)

### Parallel Worktrees

Fan one prompt across five agents, each in its own isolated git worktree — compare the results and merge the winner.

[Docs →](https://www.onorca.dev/docs/model/worktrees)

### Terminal Splits

Ghostty-class terminals with WebGL rendering, infinite splits, and scrollback that survives restarts.

[Docs →](https://www.onorca.dev/docs/terminal)

### Design Mode

Click any UI element in a real Chromium window to send its HTML, CSS, and a cropped screenshot straight into your agent's prompt.

[Docs →](https://www.onorca.dev/docs/browser/design-mode)

### GitHub &amp; Linear, Native

Browse PRs, issues, and project boards in-app — open a worktree from any task and review without a context switch.

[Docs →](https://www.onorca.dev/docs/review/linear)

### SSH Worktrees

Run agents on a beefy remote box with full file editing, git, and terminals — auto-reconnect and port forwarding included.

[Docs →](https://www.onorca.dev/docs/ssh)

### Annotate AI Diffs

Drop comments on any diff line and ship them back to the agent — review, edit, and commit without leaving Orca.

[Docs →](https://www.onorca.dev/docs/review/annotate-ai-diff)

### Drag Files to Agents

VS Code's editor with autosave everywhere — drag files or images straight into an agent prompt.

[Docs →](https://www.onorca.dev/docs/editing/file-explorer)

### Orca CLI

Agents drive Orca too — script every workflow with `orca worktree create`, `snapshot`, `click`, and `fill`.

[Docs →](https://www.onorca.dev/docs/cli/overview)

**Also in the box:**

- **[Quick open](https://www.onorca.dev/docs/model/quick-open)** — Search across worktrees, files, agents, commands, and repo context without leaving your flow.
- **[Account switcher &amp; usage tracking](https://www.onorca.dev/docs/agents/usage-tracking)** — See Claude and Codex usage and rate-limit resets, and hot-swap accounts without re-logging in.
- **[Rich repo previews](https://www.onorca.dev/docs/editing/markdown)** — Preview Markdown, images, PDFs, and repo docs in the workspace.
- **[Computer Use](https://www.onorca.dev/docs/cli/computer-use)** — Let agents operate desktop apps and visible UI when a workflow needs real interaction.
- **[Notifications and unread state](https://www.onorca.dev/docs/notifications)** — Know when an agent finishes or needs attention, then mark threads unread to come back later.
- **And many, many more** — we ship daily, so this list is perpetually behind. The [changelog](https://github.com/stablyai/orca/releases) is the real feature list.

---

## Supported Agents

Works with **any CLI agent** — if it runs in a terminal, it runs in Orca.

 Claude Code &nbsp;
 Codex &nbsp;
 Grok &nbsp;
 Cursor &nbsp;
 GitHub Copilot &nbsp;
 Muse &nbsp;
 DeepSeek Harness &nbsp;
 ZCode &nbsp;
 OpenCode &nbsp;
 MiMo Code &nbsp;
 Amp &nbsp;
 OpenClaude &nbsp;
 Antigravity &nbsp;
 Pi &nbsp;
 oh-my-pi &nbsp;
 Hermes Agent &nbsp;
 Devin &nbsp;
 Goose &nbsp;
 Auggie &nbsp;
 Autohand Code &nbsp;
 Charm &nbsp;
 Cline &nbsp;
 CodeBuddy &nbsp;
 Codebuff &nbsp;
 Freebuff &nbsp;
 Command Code &nbsp;
 Continue &nbsp;
 Droid &nbsp;
 Kilocode &nbsp;
 Kimi &nbsp;
 Kiro &nbsp;
 Mistral Vibe &nbsp;
 Qwen Code &nbsp;
 Rovo Dev &nbsp;
 + any CLI agent 

---

## Install

### Desktop — macOS, Windows, Linux

- **[Download from onOrca.dev](https://onorca.dev/download)**
- Or grab a build directly: [macOS Apple Silicon](https://github.com/stablyai/orca/releases/latest/download/orca-macos-arm64.dmg) · [macOS Intel](https://github.com/stablyai/orca/releases/latest/download/orca-macos-x64.dmg) · [Windows (.exe)](https://github.com/stablyai/orca/releases/latest/download/orca-windows-setup.exe) · [Linux AppImage](https://github.com/stablyai/orca/releases/latest/download/orca-linux.AppImage) · [All builds](https://github.com/stablyai/orca/releases/latest)

_Or via a package manager:_

```bash
# macOS (Homebrew)
brew install --cask stablyai/orca/orca

# Arch Linux (AUR) — or stably-orca-git to build from source
yay -S stably-orca-bin
```

### Mobile Companion — iOS, Android

Pair with your desktop app to monitor and steer your agents from your phone.

- **iOS:** [Download on the App Store](https://apps.apple.com/us/app/orca-ide/id6766130217)
- **Android:** [Download APK 0.0.52](https://github.com/stablyai/orca/releases/download/mobile-android-v0.0.52/app-release.apk) · [Install guide](https://www.onorca.dev/docs/android-apk)

---

## Community &amp; Support

- **Discord:** Join the community on **[Discord](https://discord.gg/fzjDKHxv8Q)**.
- **Twitter / X:** Follow **[@orca_build](https://x.com/orca_build)** for updates and announcements.
- **WeChat:** Scan to join the Orca community WeChat group 11.

- **Feedback &amp; Ideas:** We ship fast. Missing something? [Request a new feature](https://github.com/stablyai/orca/issues).
- **Privacy:** See the [privacy &amp; telemetry docs](https://www.onorca.dev/docs/telemetry) for what anonymous usage data Orca collects and how to opt out.
- **Show Support:** [Star](https://github.com/stablyai/orca) this repo to follow along with our daily ships.

---

## Developing

Want to contribute or run locally? See our [CONTRIBUTING.md](.github/CONTRIBUTING.md) guide.

The relay that pairs the mobile app with a desktop host is also in this repository under
[`cloud/`](cloud/README.md), with a separate pnpm workspace and setup guide.

## Signed Builds

Windows code 