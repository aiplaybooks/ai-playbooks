prompts.chat

 The world's largest open-source prompt library for AI 
 Works with ChatGPT, Claude, Gemini, Llama, Mistral, and more 

 formerly known as Awesome ChatGPT Prompts 

 🌐 Browse Prompts •
 📖 Read the Book •
 📄 View on GitHub •
 🚀 Self-Host 

 🏆 Featured in Forbes ·
 🎓 Referenced by Harvard , Columbia ·
 📄 40+ academic citations ·
 ❤️ Most liked dataset on Hugging Face 
 ⭐ 143k+ GitHub stars ·
 🏅 GitHub Staff Pick ·
 🚀 First prompt library (Dec 2022)

 Loved by AI pioneers: 

 Greg Brockman (OpenAI Co-Founder) ·
 Wojciech Zaremba (OpenAI Co-Founder) ·
 Clement Delangue (Hugging Face CEO) ·
 Thomas Dohmke (Former GitHub CEO)

---

## What is this?

A curated collection of **prompts** for AI chat models. Originally created for ChatGPT, these prompts work great with any modern AI assistant.

| Browse Prompts | Data Formats |
|----------------|--------------|
| [prompts.chat](https://prompts.chat/prompts) | [prompts.csv](prompts.csv) |
| [PROMPTS.md](https://raw.githubusercontent.com/f/prompts.chat/main/PROMPTS.md) | [Hugging Face Dataset](https://huggingface.co/datasets/fka/prompts.chat) |

**Want to contribute?** Add prompts at [prompts.chat/prompts/new](https://prompts.chat/prompts/new) — they sync here automatically.

---

## 📖 The Interactive Book of Prompting

Learn prompt engineering with our **free, interactive guide** — 28+ chapters covering everything from basics to advanced techniques like chain-of-thought reasoning, few-shot learning, and AI agents.

**[Start Reading →](https://fka.gumroad.com/l/art-of-chatgpt-prompting)** (Source: https://github.com/f/prompts.chat/tree/main/src/content/book)

---

## 🎮 Prompting for Kids

An interactive, game-based adventure to teach children (ages 8-14) how to communicate with AI through fun puzzles and stories.

**[Start Playing →](https://prompts.chat/kids)**

---

## 🚀 Self-Hosting

Deploy your own private prompt library with custom branding, themes, and authentication.

**Quick Start:**
```bash
npx prompts.chat new my-prompt-library
cd my-prompt-library
```

**Manual Setup:**
```bash
git clone https://github.com/f/prompts.chat.git
cd prompts.chat
npm install && npm run setup
```

The setup wizard configures branding, theme, authentication (GitHub/Google/Azure AD), and features.

**Recommended database:** prompts.chat uses PostgreSQL. For a hosted database, we recommend [Neon](https://get.neon.com/VqfnMo4).

 Sponsored by 

📖 **[Full Self-Hosting Guide](SELF-HOSTING.md)** • 🐳 **[Docker Guide](DOCKER.md)**

---

## 🔌 Integrations

### CLI
```bash
npx prompts.chat
```

### Claude Code Plugin
```
/plugin marketplace add f/prompts.chat
/plugin install prompts.chat@prompts.chat
```
📖 [Plugin Documentation](CLAUDE-PLUGIN.md)

### MCP Server
Use prompts.chat as an MCP server in your AI tools.

**Remote (recommended):**
```json
{
 "mcpServers": {
 "prompts.chat": {
 "url": "https://prompts.chat/api/mcp"
 }
 }
}
```

**Local:**
```json
{
 "mcpServers": {
 "prompts.chat": {
 "command": "npx",
 "args": ["-y", "prompts.chat", "mcp"]
 }
 }
}
```

📖 [MCP Documentation](https://prompts.chat/docs/api)

---

## 💖 Sponsors

 &nbsp;&nbsp;

 &nbsp;&nbsp;

 &nbsp;&nbsp;

 &nbsp;&nbsp;

 &nbsp;&nbsp;

 &nbsp;&nbsp;

 &nbsp;&nbsp;

 Built with Windsurf and Devin 
 Become a Sponsor → 

---

## 👥 Contributors

---

## 📜 License

This project is dual-licensed:

- **Source code and site-authored content** is licensed under the [MIT License](LICENSE-MIT),
 including the interactive book content in [`src/content/book`](src/content/book).
- **Prompt content and data** (prompts.csv, PROMPTS.md, user-submitted prompts) is dedicated to the public domain under [CC0 1.0 Universal](LICENSE-CC0).

See [LICENSE](LICENSE) for details.