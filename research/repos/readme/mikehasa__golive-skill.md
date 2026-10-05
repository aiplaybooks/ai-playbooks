# GoLive

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Deutsch](README.de.md)

**Take your agent-built product live: hosting, database, auth, domain, email, payments — on your own accounts. Then hand it over, or tear it all down.**

Your coding agent can build an app in minutes. Getting it to real users still means accounts,
hosting, databases, domains, secrets and connected services. GoLive is the open-source Agent Skill
for that work: it **detects what your app needs, plans the exact changes, asks for your approval,
applies them with your own logins, and verifies what actually works** — then records what it
created, re-checks it for drift on demand, and can remove it again.

Automate the parts providers expose. Guide you through the parts that need a human. Verify what
can be observed, and make unfinished work clear. No GoLive account, hosted backend or product telemetry.

> **Early alpha · 0.1.0-alpha.8**
> Disposable live tests now cover six journeys: **hosting** (Vercel, Netlify), **database**
> (Supabase, Neon), **custom-domain DNS** (Porkbun, GoDaddy), **transactional email** (Resend),
> **test-mode payments** (Stripe) and **Supabase authentication**, plus the `teardown` uninstall
> path. The ownership document and the on-demand `golive status` drift check are implemented
> with test coverage (`golive status` also ran read-only in a live validation), while the broader
> [roadmap](#the-full-go-live-checklist-and-roadmap) is our direction, not a claim that it is all built.

## Before you hand over production access

Whether to give an agent your provider accounts comes down to four questions. These are this
project's answers, with the limits stated where they exist.

- **You still approve every write.** Nothing reaches a real account without a plan you have seen and
 approved: `apply` refuses without that plan's id and `--yes`, and it re-checks the plan's identity
 before writing, so a changed release or config invalidates the old approval. DNS writes need
 `--confirm-dns`, deletions need `--confirm-destroy`, and live-mode steps — live payments, production
 data, a real account — need `--confirm-live`, which now includes a project's **first production
 deploy**, because approving a plan alone used to be enough to write production for the first time.
 Credential values are read only in-process, never printed, and never in arguments, plans, state or
 reports; the file golive stores them in is plaintext at mode 0600 outside your repo, not a keychain.
 One limit worth naming: those flags are arguments the agent passes on your behalf, and an agent
 already logged in to your provider can write there with no golive plan at all.
 [Trust, access and control](docs/TRUST.md) separates what the code enforces from what is only an
 instruction the agent is asked to follow.
- **A run stops rather than pushing on.** `apply` stops at the first failed check, missing
 confirmation, missing prerequisite or provider that contradicts the plan. Later steps do not run,
 and the next `apply` resumes at that step. [Recovery](docs/RECOVERY.md#the-run-stopped) covers
 reading the failure, which steps resume, and the cases that need a reviewed decision first.
- **Rollback is narrow, opt-in and never automatic.** A failed check never triggers a rollback.
 `release.rollback: true` plans one step that re-points production at an earlier deployment golive
 itself recorded; a deployment built by a dashboard, a Git push or a pull request is not a target,
 and it touches no data, DNS, payment or email resource. Only Netlify supports these re-points
 today — on Vercel you correct production in the dashboard (Vercel's adapter has no read of what
 production serves). Promotion and rollback are implemented and mock-covered, **not live-validated**.
- **Nothing is left behind silently — which is not the same as nothing being left behind.**
 `golive teardown` removes only resources it can prove it created, re-reads the DNS zone and the
 host project after deleting, and names every leftover it cannot remove — Supabase and Neon
 projects, the Resend sending domain, a zone or host project it cannot read — as a handoff saying
 what remains and how to remove it by hand. A removal also forgets the baseline golive recorded for
 that resource, so `golive status` does not report golive's own teardown as drift.

Those answers in full: [trust, access and control](docs/TRUST.md) and
[recovery](docs/RECOVERY.md). The [architecture](docs/ARCHITECTURE.md) is the product contract,
[provider scope](docs/PROVIDERS.md) says what each provider can do today, the
[validation record](docs/VALIDATION.md) separates what has been exercised live from what is only
mock-covered, and [distribution](docs/DISTRIBUTION.md) covers installation and updates.

[Install](#install) · [Use GoLive](#use-golive) · [See the workflow](#what-a-run-looks-like) · [Alpha scope](#what-this-alpha-supports) · [Roadmap](#the-full-go-live-checklist-and-roadmap) · [Contribute](CONTRIBUTING.md)

## Install

You need **Node.js 20+**, npm/npx, Git, and a coding agent that can load skills and run commands.
Installation has been checked for Codex and Claude Code; other clients are unverified.

**Install once for all your projects.** Run this from any directory:

```bash
npx skills add https://github.com/mikehasa/golive-skill --skill golive --global
```

Select your agent when prompted: use the arrow keys to move, Space to select, and Enter to
confirm. That screen is waiting for input; installation continues after you confirm.

To skip the agent picker, use the command for your agent:

```bash
# Codex
npx skills add https://github.com/mikehasa/golive-skill --skill golive --global --agent codex --yes

# Claude Code
npx skills add https://github.com/mikehasa/golive-skill --skill golive --global --agent claude-code --yes
```

For installation in just one project, run from th