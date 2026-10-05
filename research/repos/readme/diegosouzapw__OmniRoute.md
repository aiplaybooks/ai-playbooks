# 🚀 OmniRoute — The Free AI Gateway

## 💰 ~1.62B Free Tokens / Month

> Stacking free tiers by hand is painful — dozens of SDKs, dozens of rate limits, and no idea how much you actually have. OmniRoute catalogs **489 free-tier entries across 35 recurring pool keys** and computes the token headline from the **17 pools with a published positive monthly budget plus five per-model Groq caps**, deduplicated by shared pool. Quotas that only open after a regional identity check (today: ModelScope) are shown apart, +~6M behind regional identity verification, and never summed into the headline. The result stays visible on the dashboard (`/dashboard/free-tiers`).

> Animated summary of the live `/dashboard/free-tiers` page. Full methodology (pool dedupe, credit tiers, provider terms): **[docs/reference/FREE_TIERS.md](docs/reference/FREE_TIERS.md)**.
>
> These figures are re-audited every two weeks against the live catalog and **move both ways** — a provider ends a free tier and the number drops; a new one lands and it climbs. We publish what the catalog actually computes, never a rounded-up best case. 

⭐ Star the repo if OMNIROUTE helped you save money and make your work easier.

[](https://github.com/diegosouzapw/OmniRoute)

[](https://www.star-history.com/diegosouzapw/omniroute)
[](https://olud.ai/project/diegosouzapw-omniroute.html)

### 💬 Join the community

**👋 Follow the maintainer — get new providers, releases & tips first:**

[](https://www.linkedin.com/in/diegosouzapw/)
[](https://github.com/diegosouzapw)

[](https://discord.gg/U47eFqAXCn)
[](https://t.me/omnirouteOficial)
[](https://chat.whatsapp.com/FvuCbrpZmQ6I85n2vW5QIC?s=cl&p=a&mlu=4)
[](https://chat.whatsapp.com/KWgatljAjmbELQory59Oti?s=cl&p=a&mlu=4)
[](https://omniroute.online)

**Questions, provider tips, roadmap & support → [Discord](https://discord.gg/U47eFqAXCn) · [Telegram](https://t.me/omnirouteOficial) · WhatsApp [🌍 Global](https://chat.whatsapp.com/FvuCbrpZmQ6I85n2vW5QIC?s=cl&p=a&mlu=4) / [🇧🇷 Brasil](https://chat.whatsapp.com/KWgatljAjmbELQory59Oti?s=cl&p=a&mlu=4) / [Portal](https://portal.sthub.com.br/communities/groups/st-hub/channels/Omniroute-World-8kRjmK)**

## 📈 The Gateway Keeps Growing

| | v3.8.49 | **v3.8.50** | `v3.8.51+` |
| ------------------------- | :-----: | :-----------------------: | :---------: |
| 🌐 Providers | 290 | **357** | more queued |
| 🧠 Unique chat model IDs | 1185 | **1312** | — |
| 🖼️ Modality Bridge | — | 🆕 vision + audio + video | — |
| 📡 Radar free catalog | — | 🆕 opt-in | — |
| ⚖️ Quota-aware scheduling | — | 🆕 Quota-Share | — |
| 📊 Quota telemetry | — | 🆕 live | — |

**→ [Roadmap](ROADMAP.md) — riding the rail to `v3.9.0 LTS`**

## 🧩 Available

[](https://www.npmjs.com/package/omniroute)

[](https://hub.docker.com/r/diegosouzapw/omniroute)
[](LICENSE)

 🚀 Start 
 🚀 Quick Start 
 📦 Install 
 🆓 Zero-config 

 💡 Learn 
 💥 The Promise 
 🤔 Why OmniRoute 
 🏆 What Sets Apart 

 ⚙️ Features 
 🎯 Combos 
 🌐 Providers 
 🔌 CLI &amp; MCP 

 🗜️ Compression 
 🖥️ Where It Runs 
 🔒 Private 

 👀 See it 
 🎬 In Action 
 ✨ What's New 
 🤖 Compatible CLIs 

 💚 Support 
 💚 Support / Donate 
 💬 Community 
 💖 Sponsors 

 📦 Project 
 🛠️ Tech Stack 
 📖 Docs 
 👥 Contributors 

 🌐 In 67 languages 

## 🆓 Works the second you install it — no keys, no config

```bash
# Fresh install, zero credentials — `auto` already works:
curl http://localhost:20128/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{"model":"auto","messages":[{"role":"user","content":"Hello!"}]}'
```

 Prefer a specific free backend? Call `oc/…` (OpenCode Free) directly. Then graduate to `auto` and let OmniRoute pick. 

 📦 Copy-paste quickstart scripts for **Python, Node.js, PHP, and cURL** → [`examples/quickstart/`](examples/quickstart/) 

# 💥 The Promise

# 🤔 Why OmniRoute?

## 🤝 Supported by our Open Source Friends

> **Want to join as an Open Source Friend?** These are the companies that back open source and help keep OmniRoute moving — and we say publicly where every token they give us goes. Reach out: [diegosouza.pw@outlook.com](mailto:diegosouza.pw@outlook.com)

 Kimi Moonshot AI 

 Thanks to Kimi (Moonshot AI) , our founding Open Source Friend, for backing this project! Kimi is the AI lab behind the open-weight K2 and K3 model families — Kimi K3 delivers a 1M-token context window, native vision and frontier-level coding at a fraction of closed-model prices, and works out of the box with Claude Code, Codex and every coding tool OmniRoute serves.

 What Kimi's support powers: Kimi's API credits power OmniRoute's AI-validated release pipeline — the merge validation powered by Kimi K3 stage that reviews every pull request before it ships — plus day-to-day feature development. First-class Kimi support ships on both rails: the direct Kimi API ( kimi-k3 ) and the Kimi Code coding plan (OAuth and API key). OmniRoute is also the first Brazilian open-source project in Kimi's support program. Get a Kimi API key with 15% extra credits → 

 Cheaper Inference cheaperinference.com 

 Thanks to Cheaper Inference , an OmniRoute Open Source Friend, for backing this project! Cheaper Inference is a cost-ranked gateway that resells 42 frontier models — Claude, GPT-5.x, Gemini, Kimi K3, GLM, DeepSeek, Grok and MiniMax — behind one OpenAI-compatible endpoint, routing each request to the cheapest eligible provider without ever charging above the model maker's list price.

 First-class support in OmniRoute: Chat Completions, the native /v1/responses endpoint, vision, tool calling and 3 image models ( grok-imagine , nano-banana-pro , nano-banana-2 , reachable as cheaperinference/&lt;model&gt; ). Get an API key → 

 Links tagged aff=omniroute are partner links. They fund the project at no extra cost to you. 

 🎟️ Affiliates Promo — free signup coupons from providers we don't sponsor (click to expand) 

 This section is for referral/coupon codes only. Sponsored partnerships live in 🤝 Supported by our Open Source Friends above. OmniRoute has no sponsorship 