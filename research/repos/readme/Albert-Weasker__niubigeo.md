# Refuse black-box GEO scores. Put the evidence back in your hands.

**An open-source GEO research tool for AI visibility, reproducible testing, competitors and evidence.**

Enter a domain, compare model answers, inspect citations and repeat the same research later.

> **Why pay $5,000+/year for a GEO SaaS dashboard?**
>
> NiubiGEO is open source and self-hosted. Run it with your own model API keys, keep your research data in your environment and inspect the answer behind every observation.

**Model API, hosting and infrastructure costs are separate.**

**[Self-host](#quick-start) · [Official promotion platform](https://niubigeo.ai/) · [AI advisor](https://video.niubistar.com/niubigeo)**

 Website · GitHub · 简体中文 · UI: English, 简体中文, Português (Brasil) · Quick start · 20 real cases · Releases · Packages · Docs 

 Features · How to use it · Monitoring · Compare tools · Why NiubiGEO · Sponsors · Official services · FAQ 

You have built a product, written the docs and worked to get the word out. When people ask AI for tools, does your product make it into the answer?

**NiubiGEO is an open-source tool for tracking brand visibility and competitors in AI answers.** Start with a domain to see how different models describe your product and which competitors they name. Then test keywords to find out who appears in the answers. Open any result to inspect the original response and returned sources.

 NiubiGEO 
 Open-source AI visibility. Human-powered growth. 
 Check it out on Product Hunt → 

---

## Why NiubiGEO exists

GEO tools can turn a complicated question into one unexplained number. NiubiGEO starts with the evidence instead:

```text
Question → AI model → Original answer → Mentions → Competitors → Citations → Historical run
```

You can inspect the answer, the conditions, the sources and the next run. A visibility result without its underlying answer is difficult to investigate.

## Self-hosted research and data ownership

Your keywords, competitor lists, positioning questions and research history may be commercially sensitive. Self-hosting lets you choose where the data is stored, who can access it and which model providers receive queries. It does not imply zero data exposure: external model APIs may receive the prompts you send to them.

## A project that keeps moving

NiubiGEO began with one question: **what does AI actually say about a product?** The project now connects multi-model testing, natural discovery, source evidence, repeatable runs and keyword monitoring. The next step is to make changes between runs easier to see.

## Project status

| Stage | Focus | Status |
| :--- | :--- | :--- |
| v0.1 | AI visibility testing | Shipped |
| v0.2 | Evidence and reproducibility | Shipped |
| v0.2.1 | Multi-provider model connections | Shipped |
| v0.3 | Keyword monitoring and structured research | Released |

See the [monitoring section](#monitoring) and [release history](https://github.com/Albert-Weasker/niubigeo/releases) for verifiable updates.

## New in v0.2.1

- **Connect through platform logos**: 16 platform shortcuts open an API key form with the applicable endpoint prefilled.
- **Mix model sources**: choose OpenRouter, direct provider APIs and custom OpenAI-compatible endpoints in the same test. Discover model IDs automatically or enter them manually.
- **Keep results separate**: answers, citations and failures retain their endpoint, model and search setting, even when model names match.
- **Browse the full model catalog**: filter by mainstream platform, source and search support. Custom search support is labeled unverified; structured analysis requires JSON Schema support.

[Connection guide](docs/model-connections.md) · [Download v0.3.0](https://github.com/Albert-Weasker/niubigeo/releases/tag/v0.3.0) · [Docker installation](docs/deployment/docker.md)

### v0.3 · Keyword Monitoring NEW / BETA

v0.3 adds a separate Keyword Monitoring module in the workbench: define custom keywords, import batches, classify prompts as Discovery, Alternative, Comparison, Brand or Use case, start from AI Coding/SaaS/GEO/comparison templates, choose hourly/daily/weekly frequency, keep independent history, configure an optional brand and aliases, and compare snapshots in Diff View. [English guide](docs/keyword-monitoring.md) · [中文指南](docs/keyword-monitoring.zh-CN.md).

This release does not include a separate competitor detection dashboard. The current v0.3 scope is keyword monitoring, independent history and change comparison.

## What can you find out?

- **How AI sees your product.** What does it call your brand, and what does it think you do? Do different models agree?
- **Who else appears.** Which products does each model associate with yours? Do you or your competitors appear in keyword tests?
- **Which words it associates with you.** Compare the keywords models connect to your brand and other products to find differences worth investigating.
- **Where the results come from.** Inspect original answers, returned citations and changes across repeated tests.

 See the workbench: PostHog model answers and evidence links 

[](examples/cases/R04/README.md)

*Read what each model actually said, then open the sources to check. An original screenshot from the September 8, 2026 study. [Read the PostHog case](examples/cases/R04/README.md).*

## Get started

**Want to see it in action first? [Explore 20 real cases](examples/README.md).** No installation or API key needed.

To test your own product, you will need Node.js 22.13+ and your own OpenRouter API key:

```bash
git clone --branch v0.3.0 --depth 1 https://github.com/Albert-Weasker/niubigeo.git
cd niubigeo
npm ci
cp .env.example .env
```

Set `OPENROUTER_API_KEY` in `.env`, then start the app:

```bash
npm run server
```

Open [**http://localhost:8787**](http://localhost:8787) to create your first project.

Prefer a container? Follow the [Docker guide](docs/deployment/docker.md). Existing users should read [Backups and upgrades](docs/upgrade.md).

## 