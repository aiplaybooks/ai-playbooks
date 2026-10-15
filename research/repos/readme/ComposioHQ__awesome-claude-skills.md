Awesome Claude Skills 

A comprehensive and curated list of 1000+ production ready and practical Claude Skills and Plugins for enhancing productivity across usecases on not just Claude.ai, Claude Code, but also across coding agents like Codex, Cursor, Gemini CLI, Antigravity and more.

## Give your skills real-world actions

Skills tell your agent **how** to work. An MCP Gateway gives it secure access to the tools it needs.

Composio [MCP Gateway](https://composio.dev/mcp-gateway) provides a single MCP endpoint for 1,000+ integrations with built-in authentication, team-based access controls, audit logs, and production-ready reliability.

---

## Quickstart: Connect Claude to 1000+ Apps

The **connect-apps** plugin lets Claude perform real actions - send emails, create issues, post to Slack. It handles auth and connects to 1000+ apps using Composio under the hood.

### 1. Install the Plugin

```bash
claude --plugin-dir ./connect-apps-plugin
```

### 2. Run Setup

```
/connect-apps:setup
```

Paste your API key when asked. (Get a free key at [dashboard.composio.dev](https://dashboard.composio.dev/login?utm_source=Github&utm_content=AwesomeSkills))

### 3. Restart & Try It

```bash
exit
claude
```

> **Want skills that do more than generate text?** Claude can send emails, create issues, post to Slack, and take actions across 1000+ apps. [See how →](./connect/)

If you receive the email, Claude is now connected to 1000+ apps.

**[See all supported apps →](https://composio.dev/toolkits)**

---

## Contents

- [What Are Claude Skills?](#what-are-claude-skills)
- [Skills](#skills)
 - [Document Processing](#document-processing)
 - [Development & Code Tools](#development--code-tools)
 - [Data & Analysis](#data--analysis)
 - [Business & Marketing](#business--marketing)
 - [Communication & Writing](#communication--writing)
 - [Creative & Media](#creative--media)
 - [Productivity & Organization](#productivity--organization)
 - [Collaboration & Project Management](#collaboration--project-management)
 - [Security & Systems](#security--systems)
 - [App Automation via Composio](#app-automation-via-composio)
- [Getting Started](#getting-started)
- [Creating Skills](#creating-skills)
- [Contributing](#contributing)
- [Resources](#resources)
- [License](#license)

## What Are Claude Skills?

Claude Skills are reusable instruction packages that teach an AI agent how to handle a specific class of tasks. Each skill is a folder containing a `SKILL.md` file with YAML frontmatter (name, description) and Markdown instructions, optionally bundled with scripts, references, and assets. Anthropic introduced the format in October 2025 and released it as an [open standard](https://github.com/anthropics/skills) in December 2025; it's now supported by Claude Code, Claude.ai, the Claude API, OpenAI Codex, Cursor, Gemini CLI, Antigravity, and Windsurf.

Skills load progressively. At session start, the agent sees only each skill's name and description — roughly 100 tokens per skill. The full SKILL.md body (typically under 5,000 tokens) loads only when the agent decides the skill is relevant to the current task. Auxiliary files in `scripts/` and `references/` load on demand. This is what lets a single agent host hundreds of skills without bloating its context window.

Skills are not MCP servers and not tools. MCP defines how an agent connects to external systems — auth, transport, tool discovery. Tools are the individual functions an agent invokes. Skills define the workflow — what to do, in what order, with what guardrails — once the agent has the connections and tools it needs. In production, all three layers run together: MCP for access, tools for actions, skills for behavior.

## Skills

### Document Processing

- [docx](https://github.com/anthropics/skills/tree/main/skills/docx) - Create, edit, analyze Word docs with tracked changes, comments, formatting.
- [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) - Extract text, tables, metadata, merge & annotate PDFs.
- [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) - Read, generate, and adjust slides, layouts, templates.
- [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) - Spreadsheet manipulation: formulas, charts, data transformations.
- [Markdown to EPUB Converter](https://github.com/smerchek/claude-epub-skill) - Converts markdown documents and chat summaries into professional EPUB ebook files. *By [@smerchek](https://github.com/smerchek)*
- [Master Claude for Legal](https://github.com/sboghossian/master-claude-for-legal) - Skill pack for legal teams. NDA triage, multi-party version diff, citation verifier, meeting brief, and the Friday-newsletter status synthesis pattern. Includes 10 reference docs (privilege, verification, long documents, practice areas) and 3 firm templates. Built from the public Anthropic Claude for Legal Teams webinar dataset. *By [@sboghossian](https://github.com/sboghossian)*

### Development & Code Tools

- [artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) - Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui).
- [aws-skills](https://github.com/zxkane/aws-skills) - AWS development with CDK best practices, cost optimization MCP servers, and serverless/event-driven architecture patterns.
- [building-blog](https://github.com/BuildShipGrowRepeat/nextjs-sanity-blog-skill) - Adds an SEO-first, i18n-ready blog to a Next.js + Sanity site via a 40-question intake, a one-page plan, and a 20-section spec. Includes a generator for AI hero images via Gemini 3 Pro Image (Nano Banana Pro). *By [@BuildShipGrowRepeat](https://github.com/BuildShipGrowRepeat)*
- [Changelog Generator](./changelog-generator/) - Automatically creates user-facing changelogs from git commits by analyzing history and transforming technical commits into customer-friendly release notes.
- [Chrom