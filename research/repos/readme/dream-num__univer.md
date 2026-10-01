**The Office Harness for AI Agents**

Spreadsheets · Documents · Presentations · Bases · Boards · PDFs

High-performance, fully customizable Office SDK

Build embeddable productivity experiences with a plugin architecture, Canvas-based rendering,
a formula engine, and one Facade API that works in the browser and on Node.js.

English | [简体中文](./docs/readme/zh-CN.md) | [繁體中文](./docs/readme/zh-TW.md) | [日本語](./docs/readme/ja-JP.md) | [한국어](./docs/readme/ko-KR.md) | [Español](./docs/readme/es-ES.md)

[🌐 Website](https://univer.ai/) | [📖 Documentation](https://docs.univer.ai) | [✨ Showcase](https://docs.univer.ai/showcase) | [📘 API Reference](https://docs.univer.ai/reference/classes/univer) | [📝 Blog](https://docs.univer.ai/blog)

[](https://github.com/dream-num/univer/releases)
[](./LICENSE)
[](https://github.com/dream-num/univer/actions/workflows/build-packages.yml)
[](https://www.codefactor.io/repository/github/dream-num/univer/overview/dev)
[](https://codecov.io/gh/dream-num/univer)

[](https://github.com/dream-num/univer/stargazers)
[](https://github.com/dream-num/univer/graphs/contributors)
[](https://github.com/dream-num/univer/issues)
[](https://github.com/dream-num/univer/commits/dev/)

[](https://discord.gg/z3NKNT6D2f)
[](https://twitter.com/univerhq)
[](https://opencollective.com/univer)

[](https://trendshift.io/repositories/4376)

## ✨ What is Univer?

Univer is an open-source SDK for creating office applications inside your own product. It gives you the building blocks for spreadsheet, document, and presentation experiences without forcing you into a hosted app or a fixed UI.

Use Univer when you need to:

- Embed spreadsheet or document editing into a SaaS product, internal tool, BI workflow, or AI application.
- Run workbook/document processing on the server with the same architecture used in the browser.
- Compose only the features you need through plugins or start quickly with presets.
- Extend behavior through custom plugins, commands, services, UI components, and Facade APIs.

Univer is not a spreadsheet file viewer only. It is a framework for building your own productivity surface.

Across the [Univer product family](https://univer.ai/), Office tools share a runtime for storage and computation. Content can be composed and embedded across tools, with linked data and references updating together. People and AI agents can work in the same files. See the [capability matrix](https://univer.ai/capabilities) for product coverage and [Open Source and Pro](#-open-source-and-pro) for this repository's scope.

### Build a collaborative tool with Univer Office SDK

[](https://www.youtube.com/watch?v=1p-SMEiK6Kg)

[Watch the demo](https://www.youtube.com/watch?v=1p-SMEiK6Kg)

## Built with Univer Office SDK

### Featured example: Univer Workspace

[Univer Workspace](https://github.com/dream-num/univer-workspace) is an open-source, self-hostable workspace built on Univer Office SDK, where people and AI agents create, collaborate on, and review Office content. Developers can use the complete implementation as a reference, learn how to integrate the SDK, and build their own products.

[](https://github.com/dream-num/univer-workspace)

- Agents can generate spreadsheet-based mini-apps, such as decision-making dashboards, interactive reports, and business dashboards.
- Metrics, charts, and controls on the web page are bound to cells, supporting data reads, writes, and collaborative updates.

[Explore Univer Workspace](https://github.com/dream-num/univer-workspace)

### Other examples

These open-source projects are built with Univer Office SDK:

| Project | Description |
| --- | --- |
| [Univer Office for DeepSeek Harness](https://github.com/dream-num/dsh-univer-office) | An Office plugin for DeepSeek Harness with connected content, validation, and isolated worktrees for agent collaboration. |
| [Univer CLI](https://github.com/dream-num/univer-cli) | A local command-line workspace for agents to create, edit, inspect, and deliver Office content. |
| [Univer Office for WorkBuddy](https://github.com/dream-num/workbuddy-univer-office) | A local Office integration for WorkBuddy with MCP previews and draft review. Development preview. |
| [Univer Office for OpenClaw](https://github.com/dream-num/openclaw-univer-office) | Tools for creating, reviewing, and delivering Office content in OpenClaw. |

Each project documents its own setup and SDK licensing requirements.

## 🌟 Highlights

 ⚡ 
 Built for large surfaces 
 Canvas-based rendering and a dedicated formula engine keep complex workbooks responsive. 

 🧩 
 Plugin-shaped by default 
 Compose, replace, lazy-load, or extend capabilities without taking the whole stack. 

 🤖 
 Headless for AI infrastructure 
 Run workbook and document logic in Node.js to power agents, automation, and server-side workflows. 

 🛠️ 
 Product-ready SDK 
 Framework adapters, Facade APIs, presets, and headless runtime fit real integration paths. 

 🌗 
 Dark-mode ready 
 UI components and the rendering engine both adapt to light and dark themes. 

 🔌 
 Unified Facade API 
 One consistent API surface for workbooks, ranges, formulas, and documents across browser and Node.js. 

## 🚀 Why Univer?

- **Isomorphic by design**: run UI apps in browsers and headless processing in Node.js.
- **Plugin-first architecture**: every capability is delivered as a composable plugin, so features can be added, removed, replaced, or lazy-loaded.
- **Preset mode for fast integration**: use the curated plugin collections in [`presets/`](./presets) when you want a working app quickly.
- **Plugin mode for full control**: manually compose packages when you need custom loading, smaller bundles, or deep integration.
- **Facade API**: work with workbooks, worksheets, ranges, documents, formulas, commands, and events through a higher-level API.
- **Canvas rendering engine**: support large editable document surfaces with a rendering layer shared across document types.
- **Extensible UI**: integrate with 