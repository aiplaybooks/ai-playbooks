Read this in other languages 

🇺🇸 English | 🇨🇳 简体中文 | 🇯🇵 日本語 | 🇰🇷 한국어 | 🇩🇪 Deutsch | 🇫🇷 Français | 🇪🇸 Español | 🇮🇳 हिन्दी | 🇧🇷 Português | 🇷🇺 Русский | 🇸🇦 العربية | 🇮🇷 فارسی | 🇮🇹 Italiano | 🇵🇱 Polski | 🇳🇱 Nederlands | 🇹🇷 Türkçe | 🇺🇦 Українська | 🇻🇳 Tiếng Việt | 🇮🇩 Bahasa Indonesia | 🇸🇪 Svenska | 🇬🇷 Ελληνικά | 🇷🇴 Română | 🇨🇿 Čeština | 🇫🇮 Suomi | 🇩🇰 Dansk | 🇳🇴 Norsk | 🇭🇺 Magyar | 🇹🇭 ภาษาไทย | 🇺🇿 Oʻzbekcha | 🇹🇼 繁體中文 | 🇵🇭 Filipino | 🇮🇱 עברית 

 Try the graphify platform free for 14 days: app.graphify.com 

Type `/graphify` in your AI coding assistant and it maps your entire project (code, docs, PDFs, images, videos) into a **knowledge graph** you can **query instead of grepping** through files.

- **Code maps for free, fully local.** Code is parsed with tree-sitter AST: deterministic, no LLM, nothing leaves your machine. (Docs, PDFs, images and video use your assistant's model, or a configured API key, for a semantic pass.)
- **Every edge is explained.** Each connection is tagged `EXTRACTED` (explicit in the source) or `INFERRED` (resolved by graphify), so you can tell what was read directly from what was inferred.
- **Not a vector index.** No embeddings, no vector store: a real graph you traverse. Ask a question, trace the path between two things, or explain one concept.

> Want this always-on, updating in the background across your code, docs, and meetings rather than only on demand? That is what we are building at **[graphify.com](https://graphify.com)**, and early access is open now at **[app.graphify.com](https://app.graphify.com/login)**.

 The FastAPI codebase mapped by graphify. Every node is a concept, colors are detected communities, and the whole thing is clickable in graph.html. 

**Get started** (30 seconds):

```bash
uv tool install graphifyy # install the CLI (or: pipx install graphifyy)
graphify install # register the skill with your AI assistant
```

Then, in your AI assistant:

```
/graphify .
```

That's it. You get **three files**:

```
graphify-out/
├── graph.html open in any browser — click nodes, filter, search
├── GRAPH_REPORT.md the highlights: key concepts, surprising connections, suggested questions
└── graph.json the full graph — query it anytime without re-reading your files
```

The persisted graph includes `graph.schema_version` so integrations can detect
incompatible format changes, plus `graph.graphify_version` identifying the
Graphify release that produced it.

**Works in** Claude Code, Cursor, Codex, Gemini CLI, GitHub Copilot, and 15+ more — [pick your platform](#install).

---

## See it in action

Once the graph is built you query it instead of reading files. Real output, graphify run on the FastAPI codebase shown above:

```text
$ graphify explain "APIRouter"
Node: APIRouter
 Source: routing.py L2210
 Community: 2
 Degree: 47

Connections (47):
 --> RequestValidationError [uses] [INFERRED]
 --> Dependant [uses] [INFERRED]
 --> .get() [method] [EXTRACTED]
 DefaultPlaceholder ModelField
```

Every edge carries a **confidence tag** (`EXTRACTED` = explicit in the source, `INFERRED` = derived by resolution), so you can tell what was read directly from what was inferred. `graphify query " "` returns a scoped subgraph for a plain-language question, and `graphify path A B` traces how any two things connect.

---

## What it does

What you get out of the box:

| Capability | What you get |
|---|---|
| **God nodes** | The most-connected concepts, so you see what everything flows through |
| **Communities** | The graph split into subsystems (Leiden), with LLM-free labels |
| **Cross-file links** | `calls` / `imports` / `inherits` / `mixes_in` resolved across ~40 languages via tree-sitter AST |
| **Query, path, explain** | Ask a question, trace the path between two things, or explain one concept, all against `graph.json` |
| **Rationale + doc refs** | `# NOTE:` / `# WHY:` comments and ADR/RFC citations become first-class nodes linked to the code |
| **Beyond code** | Docs, PDFs, images, and video/audio all map into the same graph |
| **Local-first** | Code is parsed locally with tree-sitter (no LLM, nothing leaves your machine); only the semantic pass over docs/media calls a backend, and only if you configure one |

---

## Benchmarks

| Benchmark | Metric | graphify | Field |
|---|---|---|---|
| LOCOMO (n=300) | recall@10 | **0.497** | mem0 0.048, supermemory 0.149 |
| LOCOMO (n=300) | QA accuracy | 45.3% | supermemory 49.7%, mem0 27.3% |
| LongMemEval-S (n=50) | QA accuracy | **76%** | tied with dense RAG |
| ERPNext cross-tool (n=6) | key-fact coverage | **82.0%** | grep/read baseline 70.8% |
| Graph build | LLM credits | **0** | per-token for most systems |

Every system ran on the same harness with the same model and budgets, scored by a judge blind-validated against a second judge (90.6% agreement, Cohen's kappa 0.81). Full per-system tables, the code-intelligence result, and reproduction commands: **[BENCHMARKS.md](./BENCHMARKS.md)**.

---

## Prerequisites

| Requirement | Minimum | Check | Install |
|---|---|---|---|
| Python | 3.10+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| uv *(recommended)* | any | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| pipx *(alternative)* | any | `pipx --version` | `pip install pipx` |

**macOS quick install (Homebrew):**
```bash
brew install python@3.12 uv
```

**Windows quick install:**
```powershell
winget install astral-sh.uv
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.12 python3-pip pipx
# or install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Install

> **Official package:** The PyPI package is `graphifyy` (double-y). Other `graphify*` packages on PyPI are not affiliated. The CLI command is still `graphify`.

The official source repository is [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify).

**Step 1 — install the package:**

```bash
# Recommended (isolated env; if 'graphify' isn't found after, run: uv tool upd