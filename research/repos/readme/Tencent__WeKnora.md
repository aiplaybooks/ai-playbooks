English · 简体中文 · 日本語 · 한국어 

 Overview ·
 Quick Start ·
 What's New ·
 Features ·
 Clients ·
 Docs ·
 Development 

## Overview

[WeKnora](https://weknora.weixin.qq.com) is an open-source, LLM-powered knowledge framework for enterprise document understanding, semantic retrieval and reasoning. It brings a team's documents together so they can be searched, reasoned over and kept up to date.

https://github.com/user-attachments/assets/5722b10d-d04d-49ed-a6cc-635a8c77d91f

 1:52 · 1080p · No narration, English on-screen text 

Use RAG to look things up, the agent for multi-step tasks, and the wiki to organize knowledge. All three work on the same knowledge bases.

**The agent's toolbox.** Skills installed from ClawHub / SkillHub / Git / ZIP run in session-persistent Docker / E2B / Cube sandboxes, with an interactive terminal and graphical desktop beside the chat. Through the BrowserSkill extension the agent operates the user's own Chrome or Edge, and external MCP services (OAuth included) can be connected and enabled tool by tool.

Beyond the three modes:

- **Memory and curation**: cross-session long-term memory keeps the profile, preferences and facts a user has confirmed. Folder uploads keep their directory tree, and retrieval chunks can be edited, diffed and rolled back.
- **Data sources and formats**: auto-sync from Feishu wiki / Feishu Drive / Confluence / GitLab / Tencent IMA / Notion / Yuque / DingTalk Docs / RSS, with more on the way. 10+ document formats including PDF, Word, images, Excel and XMind; Office files are parsed in-process by anydoc.
- **Channels and integrations**: Q&A in WeCom, Feishu, Slack, Telegram and other IM apps; an embed widget for external websites; a built-in MCP Server for Cursor, Claude and other AI tools; scoped API keys with a principal model for programmatic access.
- **Models**: 27 built-in vendors with a generated model catalog, including OpenAI, DeepSeek, Qwen (Alibaba Cloud), Zhipu, Hunyuan, Gemini, MiniMax, NVIDIA, LiteLLM and Ollama.
- **Permissions and operations**: multi-workspace RBAC (four roles, per-resource ownership, per-workspace audit log), several storage instances per workspace, a runtime task-queue dashboard with worker-pool governance, and Langfuse tracing for agent steps, token usage and pipelines.
- **Deployment**: LLMs, vector databases and storage backends are all swappable. Deploy locally or on a private cloud and keep the data in your own environment.

## Quick Start

 ONLINE 
 WeChat Dialog Open Platform 
 Manage knowledge bases online and connect Q&A to Official Accounts, Mini Programs and other WeChat scenarios. 
 Open the platform → 

 CLOUD 
 Tencent Cloud Lighthouse 
 Deploy WeKnora from an application template and run it on your own cloud server. 
 Deploy on Tencent Cloud → 

 SELF-HOSTED 
 Your own environment 
 Deploy with Docker or Kubernetes and configure models, storage and networking yourself. 
 Run with Docker Compose ↓ 

### Run with Docker Compose

Requires [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/) and [Git](https://git-scm.com/).

```bash
git clone https://github.com/Tencent/WeKnora.git
cd WeKnora
cp .env.example .env # Edit .env as needed, see comments in the file
docker compose pull # Pull the latest images
docker compose up -d # Start core services
```

Then open **http://localhost** and follow the onboarding guide. A walkthrough with sample data is in the [Quickstart](https://weknora.weixin.qq.com/docs/01-getting-started/03-quickstart).

> [!TIP]
> To use a local Ollama model, run `ollama serve > /dev/null 2>&1 &` first. For the Ollama embedding model name, `OLLAMA_BASE_URL`, and RAM notes, see [Configuration](https://weknora.weixin.qq.com/docs/01-getting-started/04-configuration).

| Service | URL |
|---------|-----|
| Web UI | `http://localhost` |
| Backend API | `http://localhost:8080` |
| Langfuse Tracing | `http://localhost:3000` |

### Optional services

Add `--profile` flags to enable additional components; multiple profiles can be combined.

| Profile | Adds |
|---------|------|
| _(default)_ | Core services |
| `full` | All features |
| `neo4j` | Knowledge Graph (Neo4j) |
| `minio` | Object Storage (MinIO) |
| `langfuse` | Tracing (Langfuse) |

```bash
docker compose --profile neo4j --profile minio pull
docker compose --profile neo4j --profile minio up -d
docker compose down # Stop services
```

### Upgrading

If you already have WeKnora running and downloaded a newer release:

```bash
# Set WEKNORA_VERSION in .env to the target release (e.g. 0.8.2), or keep latest
docker compose pull # Pull images matching WEKNORA_VERSION
docker compose up -d # Recreate containers with new images
```

> [!NOTE]
> `docker compose up -d` alone reuses locally cached images and may leave the UI version out of sync with the release you downloaded. Read the [upgrade notes](https://weknora.weixin.qq.com/docs/07-releases/v0.8.2#upgrade-notes) before moving from v0.8.0.

### Other ways to deploy

| Option | When to use it |
|--------|----------------|
| **Docker Compose** | The standard deployment above: all features, multiple services |
| **Kubernetes (Helm)** | Production clusters; the chart is in [`helm/`](./helm) |
| **Lite single binary** | Local or low-resource use with no external dependencies (SQLite + in-memory queue); see [Lite vs. standard](./docs/LITE.md) |
| **Desktop app** | The Lite runtime with a GUI, login-free start and a macOS host sandbox; no installer is published yet, so build it from source |

All options, hardware requirements and deployment topologies: [Installation guide](https://weknora.weixin.qq.com/docs/01-getting-started/02-installation).

> [!WARNING]
> WeKnora ships with login authentication, but for production deployments we strongly recommend that you:
> - deploy it in an internal / private network rather than on the public internet;
> - avoid exposing the service directly to public networks, to prevent information leakage;
> - configure proper fir