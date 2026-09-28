# OpenBot

**The AI assistant your company can actually own.** Same shape as ChatGPT, Claude or Grok, with one difference that matters: it runs on your infrastructure and you can change anything about it. Any agent stack, through AG-UI.

Each coworker gets a computer of its own: a real browser with its own logins, its own files, and only the tools you grant. Every action decided before it happens and recorded after.

[**Talk to an engineer**](https://copilotkit.ai/talk-to-an-engineer?ref=openbot_readme) · [**Have us build it with you**](https://copilotkit.ai/talk-to-an-engineer?ref=openbot_readme) · [**copilotkit.ai/openbot**](https://copilotkit.ai/openbot) · [**Quick start**](#quick-start) · [**Docs**](docs/README.md)

[](https://github.com/CopilotKit/openbot/actions/workflows/ci.yml)
[](https://github.com/CopilotKit/openbot/actions/workflows/security_zizmor.yml)
[](./LICENSE)

[](https://trendshift.io/repositories/175080)

https://github.com/user-attachments/assets/535ef7ee-1631-4a69-b839-564c56cf90b4

Bring any AG-UI agent, written on a framework or by hand, and it arrives as a
coworker with a channel of its own. Watch it work on its own screen, take the
wheel when it reaches something it should not do alone, then hand it back. It
answers with components rather than only prose, and the whole thing runs on
your own machine.

> **A template, not a product.** OpenBot is meant to be cloned and made your own. There is no hosted version to sign up for, and nothing here is published as a package to depend on: every workspace in this repository is private. You take the repository, replace the example tenant package under `examples/` with your own coworkers, channels and skills, and run it. Everything below describes a starting point, not a finished thing somebody operates for you.

> **Alpha, and under active development.** OpenBot is early. Expect rough edges and bugs, and expect things to move. Issues and pull requests are welcome.

> **Runs on your machine.** Everything below is written for a laptop. `.env.example` carries `OPENBOT_SINGLE_USER=true`, which admits every request as one administrator, so a fresh clone reaches the product without registering an OAuth client first. [Sign-in](#sign-in) turns that off, and is required before anybody else can reach the deployment.

> **Do not want to build it yourself?** We will. Our engineers will stand OpenBot up inside your
> infrastructure, customize it into something that looks like your own product, and hand it back to you to
> keep changing. [**Start the conversation**](https://copilotkit.ai/talk-to-an-engineer?ref=openbot_readme).

## What it is

An agent platform that runs inside your own infrastructure. Docker Compose brings up every part of it, the data sits in your PostgreSQL, and the model is yours to choose: no model ships in the box, and an administrator supplies the credential, which is encrypted at rest and never logged.

Thirteen coworkers ship in the example package, and they are configuration rather than code: **General Assistant** for everyday work and **Knowledge** for company questions, a **Risk Analyst** reached as an endpoint, and ten in `examples/fintech/agents/` that each do one job — reading an expense claim against the policy as written, turning a meeting note into the follow-ups actually in it, drafting release notes from what shipped, triaging a ticket, answering a new starter from the handbook, writing a brief that names what it could not find, writing up an interview, handing an on-call shift over, assembling what is known before a renewal, and grouping customer feedback into themes it can cite. Add your own by dropping a file in that directory, by editing `agents.yaml`, or from `/agents` in the UI.

Anything a Bot does to a computer, a file, an MCP server or a component goes through one gateway that decides and records it. That is the difference between an agent that can use your tools and an agent you can let near them.

More at [copilotkit.ai/openbot](https://copilotkit.ai/openbot).

## Built on AG-UI

A Bot is any endpoint speaking [AG-UI](https://github.com/ag-ui-protocol/ag-ui), the open protocol for agent-to-user interaction, so OpenBot is not tied to a framework and neither are you. Agents built with LangGraph, Mastra, CrewAI, Pydantic AI, Google ADK or written by hand all arrive the same way, and the governance rides the protocol rather than the framework.

## Requirements

- Docker, for PostgreSQL and the shipped Bots.
- [Bun](https://bun.sh) 1.3+, for the app and API server.
- A CopilotKit Intelligence project and license. A free plan is available, and Intelligence can be self-hosted.
- A model key. The proof-of-concept Bot uses OpenAI; the LangGraph Bot can use OpenAI, Anthropic, or Google.

## Quick start

> **Setting up with an AI assistant?** Paste [`prompt.txt`](prompt.txt) into it first. It carries the
> same steps as below plus the things that are easy to get wrong: which of the ten blank keys in
> `.env.example` are actually yours to fill (three), which the start script generates for you, and
> what each start-up refusal means. Every claim in it is checked against this repository.

1. Create `.env`:

 ```sh
 cp .env.example .env
 bun install
 ```

2. Connect a fresh managed Intelligence project:

 ```sh
 npx --yes copilotkit@latest login
 npx --yes copilotkit@latest project select
 bun scripts/setup-learning.ts
 ```

 The helper provisions the selected project's runtime key, creates or reuses its
 `openbot` Learning container, then writes both settings to `.env`. It preserves
 custom container assignments and refuses to replace an existing OpenBot key.
 For fresh self-hosted setup, set `INTELLIGENCE_API_URL` to that deployment's
 HTTPS API origin and run the helper without the two `npx` commands. It opens
 an isolated Chrome or Edge window for your usual sign-in and project choice;
 install either browser first. Existing key-only setups can assign a container
 through [Admin → Automatic Learning]