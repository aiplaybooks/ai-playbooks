Quickstart &middot;
 Docs &middot;
 GitHub &middot;
 Discord &middot;
 Twitter &middot;
 Website 

# Paperclip is the app people use to manage AI agents for work.

Open-source orchestration for teams of AI agents.

**If OpenClaw is an _employee_, Paperclip is the _company_.**

Paperclip is a Node.js server and React UI that orchestrates a team of AI agents to run a business. Bring your own agents, assign goals, and track work and costs from one dashboard.

It looks like a task manager. Under the hood: org charts, budgets, governance, goal alignment, and agent coordination.

**Manage business goals, not pull requests.**

| | Step | Example |
| ------ | --------------- | ------------------------------------------------------------------ |
| **01** | Define the goal | _"Build the #1 AI note-taking app to $1M MRR."_ |
| **02** | Hire the team | CEO, CTO, engineers, designers, marketers — any bot, any provider. |
| **03** | Approve and run | Review strategy. Set budgets. Hit go. Monitor from the dashboard. |

 Works with 
 OpenClaw 
 Claude Code 
 Codex 
 Cursor 
 Bash 
 HTTP 

 If it can receive a heartbeat, it's hired. 

## Paperclip is right for you if

- ✅ You want to build **autonomous AI organizations**
- ✅ You **coordinate many different agents** (OpenClaw, Codex, Claude, Cursor) toward a common goal
- ✅ You have **20 simultaneous Claude Code terminals** open and lose track of what everyone is doing
- ✅ You want agents running **autonomously 24/7**, but still want to audit work and chime in when needed
- ✅ You want to **monitor costs** and enforce budgets
- ✅ You want a process for managing agents that **feels like using a task manager**
- ✅ You want to manage your autonomous businesses **from your phone**

## The four pillars

Four things have to work for an organization of AI agents to actually produce: the tasks, the org, the training, and the infrastructure. Paperclip is built around exactly those four pillars.

| Pillar | Built for | What it covers |
| --- | --- | --- |
| **Agentic Task Manager** — Declare intent. Agents work. You verify the output. | Everyone, daily | Tasks, approvals & review gates · proactive agent coworkers · auditable routines & workflows · verify from diffs, screenshots & tests |
| **Org Chart for Agents** — Roles, permissions & boundaries for humans and agents. | Managers | Mixed human + agent org chart · responsibilities, delegation, specialization · governance: who can do what · scoped secrets & company boundaries |
| **Agent Employee Training** — Design, train & evaluate your AI employees. | Enablers | Skill Studio & shared org-wide skills · evals & saved test runs · active learning loops & quality metrics · performance reviews for agents |
| **Agentic OS** — The infrastructure that makes the work run. | IT & platform | Cross-provider runtime: any model, any agent · sandboxing, integrations & MCP servers · SSO, GRC, RBAC & cost controls · data privacy, internal trace collection, compounding data value |

## Features

 🔌 Bring Your Own Agent 
Any agent, any runtime, one org chart. If it can receive a heartbeat, it's hired.

 🎯 Goal Alignment 
Every task traces back to the organization mission. Agents know what to do and why .

 💓 Heartbeats 
Agents wake on a schedule, check work, and act. Delegation flows up and down the org chart.

 💰 Cost Control 
Monthly budgets per agent. When they hit the limit, they stop. No runaway costs.

 🏢 Multi-Organization 
One deployment, many organizations. Complete data isolation. One control plane for your portfolio.

 🎫 Ticket System 
Every conversation traced. Every decision explained. Full tool-call tracing and immutable audit log.

 🛡️ Governance 
Approve hires, override strategy, pause or terminate any agent — at any time.

 📊 Org Chart 
Hierarchies, roles, reporting lines. Your agents have a boss, a title, and a job description.

 📱 Mobile Ready 
Monitor and manage your autonomous businesses from anywhere.

## Problems Paperclip solves

| Without Paperclip | With Paperclip |
| ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| ❌ You have 20 Claude Code tabs open and can't track which one does what. On reboot you lose everything. | ✅ Tasks are ticket-based, conversations are threaded, sessions persist across reboots. |
| ❌ You manually gather context from several places to remind your bot what you're actually doing. | ✅ Context flows from the task up through the project and company goals — your agent always knows what to do and why. |
| ❌ Folders of agent configs are disorganized and you're re-inventing task management, communication, and coordination between agents. | ✅ Paperclip gives you org charts, ticketing, delegation, and governance out of the box — so you run a company, not a pile of scripts. |
| ❌ Runaway loops waste hundreds of dollars of tokens and max your quota before you even know what happened. | ✅ Cost tracking surfaces token budgets and throttles agents when they're out. Management prioritizes with budgets. |
| ❌ You have recurring jobs (customer support, social, reports) and have to remember to manually kick them off. | ✅ Heartbeats handle regular work on a schedule. Management supervises. |
| ❌ You have an idea, you have to find your repo, fire up Claude Code, keep a tab open, and babysit it. | ✅ Add a task in Paperclip. Your coding agent works on it until it's done. Management reviews their work. |

## Why Paperclip is special

Paperclip handles the hard orchestration details correctly.

| | |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Atomic execution.** | Task checkout and budget enforcement are atomic, so no double-work and no runaway spend. |
| **Persistent agent st