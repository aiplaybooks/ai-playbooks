# Does AI recommend your product? Who shows up instead?

**Enter a domain. Compare how models describe your product, who they recommend, and which sources they cite.**

> **Open the GEO reporting black box. Put evidence in your hands.**

**[Self-host](#quick-start) · [Official promotion platform](https://niubigeo.ai/) · [AI advisor](https://video.niubistar.com/niubigeo)**

 Website · GitHub · 简体中文 · UI: English, 简体中文, Português (Brasil) · Quick start · 20 real cases · Releases · Packages · Docs 

 Features · How to use it · Monitoring · Compare tools · Why NiubiGEO · Sponsors · Official services · FAQ 

You have built a product, written the docs and worked to get the word out. When people ask AI for tools, does your product make it into the answer?

**NiubiGEO is an open-source tool for tracking brand visibility and competitors in AI answers.** Start with a domain to see how different models describe your product and which competitors they name. Then test keywords to find out who appears in the answers. Open any result to inspect the original response and returned sources.

 NiubiGEO 
 Open-source AI visibility. Human-powered growth. 
 Check it out on Product Hunt → 

---

## New in v0.2.1

- **Connect through platform logos**: 16 platform shortcuts open an API key form with the applicable endpoint prefilled.
- **Mix model sources**: choose OpenRouter, direct provider APIs and custom OpenAI-compatible endpoints in the same test. Discover model IDs automatically or enter them manually.
- **Keep results separate**: answers, citations and failures retain their endpoint, model and search setting, even when model names match.
- **Browse the full model catalog**: filter by mainstream platform, source and search support. Custom search support is labeled unverified; structured analysis requires JSON Schema support.

[Connection guide](docs/model-connections.md) · [Download v0.2.1](https://github.com/Albert-Weasker/niubigeo/releases/tag/v0.2.1) · [Docker installation](docs/deployment/docker.md)

### Coming in v0.3

A **competitor detection dashboard** and a **continuous keyword monitoring dashboard** are planned for **late October 2026**. This is a tentative target and may change; these planned dashboards are not included in v0.2.1.

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
git clone --branch v0.2.1 --depth 1 https://github.com/Albert-Weasker/niubigeo.git
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

## How to use it

1. **Enter a domain.** Create a project for your product. It is saved before you start testing.
2. **Choose your models.** Search for and select one or more models, then set web search separately for each.
3. **Save your configuration and start a test.** Models answer independently. If one fails, the other results remain available.
4. **Open the results.** Review descriptions, competitors, keywords and sources. Open the original answer to check a finding.
5. **Keep observing.** Confirm the keywords you want to test, then run keyword tests. Repeat measurements or set up scheduled monitoring to collect comparable records.

Start with one model, then add more once you know what to look for. Reading the cases is free; testing your own project incurs model and search API charges.

### Talk to the video advisor

The workbench shows a small advisor card by default. Click it to open the [official advisor entry point](https://niubigeo.ai/advisor), which redirects to the [NiubiStar-hosted video advisor](https://video.niubistar.com/niubigeo). You do not need to provide an API key to use the advisor.

The local workbench loads no third-party script, iframe or video for this card, and the link does not include project data or model API keys. Choose which project details to share during your conversation on the external service.

To hide the card, set `NIUBIGEO_VIDEO_ADVISOR_ENABLED=false` in `.env` and restart the server, or recreate the web container with `docker compose up -d`. `0` and `off` also hide it. Local diagnostics continue to work with the card disabled. This link adds no payment requirement and does not change the Apache-2.0 license.

## From one answer to ongoing observation

| What you want to do | What NiubiGEO provides |
| :--- | :--- |
| **Manage several products** | Each domain has its own project, configuration, runs and evidence. Switch projects without mixing products into one report. |
| **Compare models** | Search, filter and select OpenRouter models. Inspect each model’s answer, result and errors, and retry a failed model separately. |
| **Choose whether to use web search** | Set each model to offline or its supported native search mode. Results retain the actual executi