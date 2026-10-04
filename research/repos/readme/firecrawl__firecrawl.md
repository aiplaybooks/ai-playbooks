---

# **🔥 Firecrawl**

**Supercharge your AI agents with data from the web and beyond. Building the library for superintelligence. 🔥** Open source and available as a [hosted service](https://firecrawl.dev/?ref=github).

_Pst. Hey, you, join our stargazers :)_

---

## Why Firecrawl?

- **Industry-leading reliability**: Covers 96% of the web, including JS-heavy pages — no proxy headaches, just clean data ([see benchmarks](https://www.firecrawl.dev/blog/the-worlds-best-web-data-api-v25))
- **Blazingly fast**: P95 latency of 3.4s across millions of pages, built for real-time agents and dynamic apps
- **LLM-ready output**: Clean markdown, structured JSON, screenshots, and more — spend fewer tokens, build better AI apps
- **We handle the hard stuff**: Rotating proxies, orchestration, rate limits, JS-blocked content, and more — zero configuration
- **Agent ready**: Connect Firecrawl to any AI agent or MCP client with a single command
- **Media parsing**: Parse and extract content from web-hosted PDFs, DOCX, and more
- **Actions**: Click, scroll, write, wait, and press before extracting content
- **Open source**: Developed transparently and collaboratively — [join our community](https://discord.gg/firecrawl)

---

## Feature Overview

**Core Endpoints**

| Feature | Description |
|---------|-------------|
| [**Search**](#search) | Search the web and get full page content from results |
| [**Scrape**](#scrape) | Convert any URL to markdown, HTML, screenshots, or structured JSON |
| [**Interact**](#interact) | Scrape a page, then interact with it using AI prompts or code |

**More**

| Feature | Description |
|---------|-------------|
| [**Agent**](#agent) | Automated data gathering, just describe what you need |
| [**Crawl**](#crawl) | Scrape all URLs of a website with a single request |
| [**Map**](#map) | Discover all URLs on a website instantly |
| [**Batch Scrape**](#batch-scrape) | Scrape thousands of URLs asynchronously |

---

## Quick Start

Sign up at [firecrawl.dev](https://firecrawl.dev) to get your API key. Try the [playground](https://firecrawl.dev/playground) to test it out.

### Search

Search the web and get full content from results.

```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-YOUR_API_KEY")

search_result = app.search("firecrawl", limit=5)
```

 Node.js / cURL / CLI 

**Node.js**
```javascript
import { Firecrawl } from 'firecrawl';

const app = new Firecrawl({apiKey: "fc-YOUR_API_KEY"});

app.search("firecrawl", { limit: 5 })
```

**cURL**
```bash
curl -X POST 'https://api.firecrawl.dev/v2/search' \
-H 'Authorization: Bearer fc-YOUR_API_KEY' \
-H 'Content-Type: application/json' \
-d '{
 "query": "firecrawl",
 "limit": 5
}'
```

**CLI**
```bash
firecrawl search "firecrawl" --limit 5
```

Output:
```json
[
 {
 "url": "https://firecrawl.dev",
 "title": "Firecrawl",
 "markdown": "Turn websites into..."
 },
 {
 "url": "https://docs.firecrawl.dev",
 "title": "Firecrawl Docs",
 "markdown": "# Getting Started..."
 }
]
```

### Scrape

Get LLM-ready data from any website — markdown, JSON, screenshots, and more.

```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-YOUR_API_KEY")

result = app.scrape('firecrawl.dev')
```

 Node.js / cURL / CLI 

**Node.js**
```javascript
import { Firecrawl } from 'firecrawl';

const app = new Firecrawl({ apiKey: "fc-YOUR_API_KEY" });

app.scrape('firecrawl.dev')
```

**cURL**
```bash
curl -X POST 'https://api.firecrawl.dev/v2/scrape' \
-H 'Authorization: Bearer fc-YOUR_API_KEY' \
-H 'Content-Type: application/json' \
-d '{
 "url": "firecrawl.dev"
}'
```

**CLI**
```bash
firecrawl scrape https://firecrawl.dev
firecrawl https://firecrawl.dev --only-main-content
```

Output:
```
# Firecrawl

Firecrawl helps AI agents search, scrape, and interact with the web.

## Features
- Search: Find information across the web
- Scrape: Clean data from any page
- Interact: Click, navigate, and operate pages
- Agent: Autonomous data gathering
```

### Interact

Scrape a page, then interact with it using AI prompts or code.

```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-YOUR_API_KEY")

result = app.scrape("https://amazon.com")
scrape_id = result.metadata.scrape_id

app.interact(scrape_id, prompt="Search for 'mechanical keyboard'")
app.interact(scrape_id, prompt="Click the first result")
```

 Node.js / cURL / CLI 

**Node.js**
```javascript
import { Firecrawl } from 'firecrawl';

const app = new Firecrawl({apiKey: "fc-YOUR_API_KEY"});

const result = await app.scrape("https://amazon.com");

await app.interact(result.metadata.scrapeId, {
 prompt: "Search for 'mechanical keyboard'"
});
await app.interact(result.metadata.scrapeId, {
 prompt: "Click the first result"
});
```

**cURL**
```bash
# 1. Scrape the page
curl -X POST 'https://api.firecrawl.dev/v2/scrape' \
-H 'Authorization: Bearer fc-YOUR_API_KEY' \
-H 'Content-Type: application/json' \
-d '{"url": "https://amazon.com"}'

# 2. Interact with the page (use scrapeId from step 1)
curl -X POST 'https://api.firecrawl.dev/v2/scrape/SCRAPE_ID/interact' \
-H 'Authorization: Bearer fc-YOUR_API_KEY' \
-H 'Content-Type: application/json' \
-d '{"prompt": "Search for mechanical keyboard"}'
```

**CLI**
```bash
firecrawl scrape https://amazon.com
firecrawl interact exec --prompt "Search for 'mechanical keyboard'"
firecrawl interact exec --prompt "Click the first result"
```

Output:
```json
{
 "success": true,
 "output": "Keyboard available at $100",
 "liveViewUrl": "https://liveview.firecrawl.dev/..."
}
```

---

## Power Your Agent

Connect Firecrawl to any AI agent or MCP client in minutes.

### Skill

Give your agent easy access to real-time web data with one command.

```bash
npx -y firecrawl-cli@latest init --all --browser
```

Restart your agent after installing. Works with [Claude Code](https://claude.ai/code), [Antigravity](https://antigravity.google), [OpenCode](https://opencode.ai), and more.

### MCP

Connect any MCP-compatible client to the web i