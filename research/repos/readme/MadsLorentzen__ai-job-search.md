# AI Job Search

*The job search that runs on your machine.*

[](https://github.com/MadsLorentzen/ai-job-search/actions/workflows/ci.yml)

An AI-powered job application framework built on [Claude Code](https://claude.com/claude-code). Fork it, fill in your profile, and let Claude evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews.

> Note: This is an independent open-source project and is not affiliated with, endorsed by, sponsored by, or maintained by Anthropic. Anthropic and Claude Code are referenced only to describe the toolchain this workflow uses.
>
> This project has **no affiliated cryptocurrency, token, or paid sponsorship program**. Anything claiming otherwise is unauthorized and should be treated as a scam. The only ways to support the project are the Ko-fi link below and contributing on GitHub.

## Does it actually work?

I'm a geophysicist by training. When my position was cut in late 2025, I built this framework to run my own job search - the same `/scrape`, `/apply`, and `/interview` workflow in this repo, used weekly, on my own career. I was upfront about it with every employer I spoke to, and instead of counting against me, it usually sparked a genuine technical conversation.

Sixty-nine tailored applications, twenty first interviews, and one signed contract later, I started as an AI engineer in June 2026. People kept asking whether this actually works. It got me hired. Now it's yours.

*The longer version, including the full application funnel, is on [LinkedIn](https://www.linkedin.com/in/mads-lorentzen/).*

 Did this save you a Sunday of cover-letter writing? Consider a coffee. 
 Did it land you the job? Maybe two. ☕

## What this is

A structured workflow that turns Claude Code into a full-stack job application assistant. The core workflow (self-profiling, fit evaluation, and the drafter-reviewer application pipeline) is **language- and country-agnostic**. The job portal search skills are built for the Danish market (Jobindex, Jobnet, Akademikernes Jobbank, etc.), but the pattern is designed to be swapped for your local job boards.

```
/setup /scrape /apply 
 | | |
 v v v
Fill in Search job Evaluate fit
your profile portals Score & recommend
 | | |
 v v v
Profile Present matches Draft CV + Cover Letter
files ready with fit ratings (LaTeX, tailored)
 | |
 v v
 Pick a match Reviewer agent critiques
 -> /apply -> Revise -> Final output
```

The framework encodes career guidance best practices, including structured evaluation criteria, forward-looking cover letter framing, and optional salary benchmarking.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) (CLI). Claude Code has no free tier: you need a Claude Pro/Max/Team subscription or Anthropic API credits (pay-per-token, usually cheaper for occasional use). Using a different agent tool (Codex, Antigravity, Gemini CLI)? Start at [`AGENTS.md`](AGENTS.md) - the portal search skills work there out of the box, and [community forks](https://github.com/MadsLorentzen/ai-job-search/discussions/78) adapt the full workflow.
- Python 3.10+
- [Bun](https://bun.sh) (for job search CLI tools)
- LaTeX distribution with `lualatex` and `xelatex`: [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), [TinyTeX](https://yihui.org/tinytex/), or [MiKTeX](https://miktex.org/). The CV compiles with `lualatex` (pdflatex often fails on modern MiKTeX installs with `fontawesome5` font-expansion errors); the cover letter compiles with `xelatex` because `cover.cls` requires `fontspec`. If using a minimal TeX install such as TinyTeX or BasicTeX, install the extra packages listed in [SETUP.md](SETUP.md#minimal-tex-install-tinytexbasictex).
- Optional: `pip install pypdf` for `/apply`'s ATS parseability check (BSD; no Poppler required). Poppler `pdftotext` remains a fallback (macOS: `brew install poppler`, Debian/Ubuntu: `apt install poppler-utils`, Windows: `choco install poppler`). If both are missing, the check degrades to a visual keyword review.

## Quick start

> 🎥 **Prefer to see it in action first?** [The Next New Thing did a hands-on walkthrough](https://www.youtube.com/watch?v=HoVxjMNFYv4) of how the workflow is actually used, from setup to a finished application (recorded August 2026 - commands may have evolved since).

### 1. Fork and clone

```bash
gh repo fork MadsLorentzen/ai-job-search --clone
cd ai-job-search
```

> [!IMPORTANT]
> **A fork of this repo is always public** — GitHub does not allow private forks of
> public repositories — and `/setup` (step 3 below) writes your personal data (name,
> contact details, employment history, salary expectations) into **tracked** files.
> If this copy is for your own job search rather than for contributing changes back,
> use a **private repository** with this repo as `upstream` instead — the two-minute
> recipe is in [SETUP.md section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork),
> and every update workflow works identically. Fork only to contribute.

### 2. Install job search tools

```bash
python3 tools/install_portal_clis.py # Windows: python tools\install_portal_clis.py
```

It runs `bun install` in every portal CLI under `.agents/skills/*/cli/` - discovered, not listed, so a portal you add with `/add-portal` or copy from another fork is included on a fresh clone. A CLI whose `package.json` declares an install-time lifecycle script is skipped and reported rather than run. `--dry-run` shows what it would install.

For `linkedin-search` and `freehire-search` the install is optional: both have zero runtime dependencies and run with plain `bun`; `bun install` only pulls TypeScript dev types.

### 3. Set up your profile

```bash
claude
# Then inside Claude Code:
/setup
```

`/setup` offers three paths: read your `documents/` folder if you have one populated (CV PDF, LinkedIn export, diplomas, reference letters, past applications), import a single CV pasted in chat, or walk through an interview. It auto-detect