Language: 
 English |
 Português (Brasil) |
 简体中文 |
 繁體中文 |
 日本語 |
 한국어 |
 Türkçe |
 Русский |
 Tiếng Việt |
 ไทย |
 Deutsch |
 Español |
 Українська |
 Polski 

> [!WARNING]
> **Official sources only.** Install ECC only from verified channels: the GitHub repository [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC), the npm packages [`ecc-universal`](https://www.npmjs.com/package/ecc-universal) and [`ecc-agentshield`](https://www.npmjs.com/package/ecc-agentshield), the [GitHub App](https://github.com/apps/ecc-tools), the plugin slug `ecc@ecc`, and the project website [ecc.tools](https://ecc.tools). Third-party re-uploads and unofficial mirrors are not maintained or reviewed by the project and may contain malware.

## Install with Claude Code

Use the [guided setup](#install-ecc) or [native plugin commands](#claude-code-details). Both install the same `ecc@ecc` plugin. Choose one and do not stack a full manual Claude install on top.

 ECC Pro + GitHub App 

 Install free · Private repos from $19/seat/mo 

 Sponsor ECC 

 Fund the open-source project 

 Community 

 Discord · Q&amp;A · Show and Tell 

 **OSS stays free.** This repo is MIT-licensed forever. ECC Pro is the hosted GitHub App for private repos. Sponsors and Pro subscribers fund the work. That's why a single maintainer ships weekly across 7 harnesses. 

 Partners &amp; sponsors 

 &nbsp;&nbsp;&nbsp;
 &nbsp;&nbsp;&nbsp;
 &nbsp;&nbsp;&nbsp;
 &nbsp;&nbsp;&nbsp;

 Past sponsors: Atlas Cloud · Mike Morgan (inactive) 

 Community sponsors: @jasonwu513 · @1anter · @massimotodaro · @meadmccabe 

 Become a Sponsor · Sponsor Tiers · Sponsorship Program 

 Jump to install ↓ 

# ECC

Your agent can write code, but ECC gives it a coordinated engineering system and toolbox: it plans before it builds, verifies changes with tests, reviews its own work from a fresh context, remembers what matters, and turns repeated wins into reusable skills and workflows.

```text
plan -> test -> implement -> review -> verify -> remember -> improve
```

Instead of rebuilding that process in every prompt, you install it once and make it part of how your agent works.

> Optimize the context window. Persist everything else.

ECC is MIT-licensed open source. It works best with Claude Code today, has a supported Codex sync path, and provides capability-limited adapters for Cursor, OpenCode, Gemini, Zed, GitHub Copilot, Antigravity, Qwen, and other harnesses. See the [support status matrix](#platform-support) before assuming feature parity.

Access to 68 agents, 293 skills, and 94 legacy command shims, plus hooks, rules, memory, continuous learning, and AgentShield security scanning. The agents are specialized for planning, review, build repair, security, architecture, and domain work.

| Included | Count | What it gives you |
| ---------------- | ----------: | ------------------------------------------------------------------------------------ |
| Agents | 68 agents | Planning, review, build repair, security, architecture, and domain work |
| Skills | 293 skills | TDD, research, security, docs, frontend, data, ML, operations, and more |
| Commands | 94 commands | Convenient entry points while ECC moves to a skills-first surface |
| Hooks and memory | Runtime | Enforcement, session summaries, continuous learning, instincts, and context controls |
| Rules | Selective | Always-loaded standards you choose by language or project |
| AgentShield | Included | Scanning for prompts, hooks, MCP config, permissions, secrets, and agent files |

## Install ECC

> [!IMPORTANT]
> ECC 2.2 includes guided package setup for Claude Code, Codex, and Kimi Code.
> The universal package requires Node.js 18 or newer. Claude plugin setup also
> requires Git and Claude Code 2.1 or newer on `PATH`.

### Recommended: universal guided setup

For Claude Code plugin setup, updates, scope changes, and hook-profile changes:

```bash
npx ecc-universal@2.2.3 setup
```

#### Windows first-time walkthrough

If you are new to command-line tools, use this copy-and-paste path:

1. Install Node.js 18 or newer, Git, and Claude Code.
2. Open **PowerShell** from the Windows Start menu.
3. Confirm that each prerequisite is available:

 ```powershell
 node --version
 git --version
 claude --version
 ```

4. Run the guided installer:

 ```powershell
 npx ecc-universal@2.2.3 setup
 ```

5. For a typical personal setup, choose **Global user**, choose **Standard** hooks, and confirm.
6. Start a new Claude Code session and run `/plugin list` to verify that `ecc@ecc` is enabled.

This path does not require cloning the repository. If any prerequisite command is not found, install or repair that prerequisite before rerunning ECC setup.

If npm reports a version or cache error, confirm the registry version before retrying:

```bash
npm view ecc-universal version
```

ECC 2.2 supports the same guided setup through modern package runners:

| Package runner | Guided setup command |
|---|---|
| npm / npx | `npx ecc-universal@2.2.3 setup` |
| pnpm | `pnpm dlx ecc-universal@2.2.3 setup` |
| Yarn 2+ | `yarn dlx ecc-universal@2.2.3 setup` |
| Bun | `bunx ecc-universal@2.2.3 setup` |

The examples select [the published ECC 2.2.3 release](https://www.npmjs.com/package/ecc-universal/v/2.2.3), matching this repository's release version. A version pin is not a security audit or an integrity check. Review the release source and registry integrity before running package code; use a reviewed checkout for unreleased changes.

Yarn Classic 1 does not provide `yarn dlx`; use `npx`, install the package globally, or upgrade Yarn for a temporary one-shot run.

The wizard inventories the official marketplace and every native Claude install scope before making changes, then installs, updates, or safely moves `ecc@ecc` to the scope you choose. Rerun the same command whenever you want to update ECC, change scope, or change its hook profile. This setup wizard currently configures the Claude Code plugin; use the multi-harness wizard belo