[Documentation](https://hindsight.vectorize.io) • [Integrations](https://hindsight.vectorize.io/integrations) • [Cookbook](https://hindsight.vectorize.io/cookbook) • [Benchmarks](https://benchmarks.hindsight.vectorize.io/) • [Paper](https://arxiv.org/abs/2512.12818) • [Hindsight Cloud](https://ui.hindsight.vectorize.io/signup)

[](https://github.com/vectorize-io/hindsight/actions/workflows/release.yml)
[](https://pypi.org/project/hindsight-api/)
[](https://pypi.org/project/hindsight-client/)
[](https://www.npmjs.com/package/@vectorize-io/hindsight-client)
[](https://vectorize.io/slack)
[](https://opensource.org/licenses/MIT)

---

## What is Hindsight?

Hindsight™ is an agent memory system built to create smarter agents that learn over time. Most agent memory systems focus on recalling conversation history. Hindsight is focused on making agents that learn, not just remember.

It eliminates the shortcomings of alternative techniques such as RAG and knowledge graph and delivers state-of-the-art performance on long term memory tasks.

**Contents**

- [Memory Performance & Accuracy](#memory-performance--accuracy)
- [Quick Start](#quick-start) — [server](#1-start-a-server) · [clients](#2-connect-a-client) · [platforms](#supported-platforms) · [embedded](#python-embedded-no-server-required)
- [Adding Hindsight to Your Agent](#adding-hindsight-to-your-agent) — [LLM Wrapper](#llm-wrapper-2-lines-of-code) · [integrations](#integrations) · [coding agents](#coding-agents) · [MCP](#mcp-server)
- [Core Concepts](#core-concepts) — [memory types](#memory-types) · [retain / recall / reflect](#the-three-operations) · [observations](#observations) · [mental models & knowledge pages](#mental-models--knowledge-pages) · [banks](#memory-banks)
- [Use Cases](#use-cases)
- [Running in Production](#running-in-production)
- [Resources](#resources)

---

## Memory Performance & Accuracy

Hindsight is the most accurate agent memory system ever tested according to benchmark performance. It has achieved state-of-the-art performance on the LongMemEval benchmark, widely used to assess memory system performance across a variety of conversational AI scenarios. The current reported performance of Hindsight and other agent memory solutions as of January 2026 is shown here:

> Live, continuously updated results — including per-model accuracy, latency and cost — are published at [benchmarks.hindsight.vectorize.io](https://benchmarks.hindsight.vectorize.io/).

The benchmark performance data for Hindsight has been independently reproduced by research collaborators at the Virginia Tech [Sanghani Center for Artificial Intelligence and Data Analytics](https://sanghani.cs.vt.edu/) and The Washington Post. Other scores are self-reported by software vendors.

Hindsight is being used in production at Fortune 500 enterprises and by a growing number of AI startups.

---

> 🤖 **Using a coding agent?** Install the Hindsight documentation skill for instant access to docs while you code:
> ```bash
> npx skills add https://github.com/vectorize-io/hindsight --skill hindsight-docs
> ```
> Works with Claude Code, Cursor, and other AI coding assistants.

---

## Quick Start

### 1. Start a server

#### Docker (recommended)

```bash
export OPENAI_API_KEY=sk-xxx

docker run -it --pull always --name hindsight --restart unless-stopped -p 8888:8888 -p 9999:9999 \
 -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
 -v hindsight-data:/home/hindsight/.pg0 \
 ghcr.io/vectorize-io/hindsight:latest
```

>API: http://localhost:8888
>UI: http://localhost:9999

Hindsight works with **25+ LLM providers** via `HINDSIGHT_API_LLM_PROVIDER` — hosted (`openai`, `anthropic`, `gemini`, `groq`, `bedrock`, `vertexai`, `minimax`, `deepseek`, `atlas`, `meta`, …), fully local (`ollama`, `lmstudio`, `llamacpp`), any OpenAI-compatible endpoint, and gateways (`litellm`, `litellmrouter`) that reach the rest. Existing subscriptions work too: `openai-codex` (ChatGPT Plus/Pro), `claude-code` (Claude Pro/Max), `cursor` (Cursor) and `github-copilot` (GitHub Copilot) need no API key. See [supported models](https://hindsight.vectorize.io/developer/models).

#### Docker (external PostgreSQL)

```bash
export OPENAI_API_KEY=sk-xxx
export HINDSIGHT_DB_PASSWORD=choose-a-password
cd docker/docker-compose
docker compose up
```

> Oracle AI Database is also supported for enterprise deployments with full feature parity. See the [storage documentation](https://hindsight.vectorize.io/developer/storage) for details.

#### Bare metal (pip)

```bash
pip install hindsight-api
export HINDSIGHT_API_LLM_API_KEY=sk-xxx

hindsight-api
```

#### Kubernetes (Helm)

```bash
helm install hindsight oci://ghcr.io/vectorize-io/charts/hindsight \
 --set api.llm.provider=openai \
 --set api.llm.apiKey=sk-xxx \
 --set postgresql.enabled=true
```

#### Managed (no server)

[Hindsight Cloud](https://vectorize.io/pricing) is the hosted option: managed infrastructure that scales automatically, plus a dashboard, backups, team collaboration and a 99.9% uptime SLA. Billing is usage-based with free credits to start — no fixed monthly or per-seat fee. Point any client at `https://api.hindsight.vectorize.io` with your API key and skip the deployment entirely.

[Compare self-hosted, Cloud and Enterprise →](https://vectorize.io/pricing) · [Sign up →](https://ui.hindsight.vectorize.io/signup)

All options, including Windows and air-gapped setups, are covered in the [installation guide](https://hindsight.vectorize.io/developer/installation).

### 2. Connect a client

```bash
pip install hindsight-client -U # Python
npm install @vectorize-io/hindsight-client # Node.js / TypeScript
go get github.com/vectorize-io/hindsight/hindsight-clients/go # Go
curl -fsSL https://hindsight.vectorize.io/get-cli | bash # CLI
```

#### Python

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# Retain: Store information
client.retain(bank_id="my-bank", content="Alice works at Google as a softw