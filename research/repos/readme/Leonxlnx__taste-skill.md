Taste Skill 

 The Anti-Slop Frontend Framework for AI Agents 

 &nbsp;

 From the Taste Skill team: TasteCode , a local desktop workspace for Codex, Claude Code and Grok with a design agent that briefs, builds and visually reviews your UI. Source on GitHub . 

 Sponsors 

 Sidrune AI : one API for GPT, Claude, and other leading AI models. Sign up through this link and get $3 in API credit. 

 interfaces.dev · A design engineering magazine by Jakub Krehel 

 React Bits · animated React components for creative interfaces 

 IMG.LY · CreativeEditor SDK 

 Sent.dm · messaging APIs for SMS, WhatsApp, and RCS 

 Become a sponsor 

Portable **Agent Skills** that upgrade AI-built interfaces: stronger layout, typography, motion, and spacing instead of boilerplate-looking UIs. This repo also includes **image-generation skills** for reference boards (web, mobile, brand kits). Pair them with **ChatGPT Images** or similar generators, then hand the frames to Codex, Cursor, or Claude Code for implementation.

 &nbsp;

 &nbsp;

 &nbsp;

## Disclaimer

Taste Skill has no official token, coin, or crypto project. Any token using my name, image, or project is unaffiliated and not endorsed by me.

 Disclaimer · Install · Skills · Settings · Examples · Sponsors · Research · FAQ · License 

## Feedback & Contributions

We would love your feedback. Suggestions and bug reports:

- Open a Pull Request or Issue on GitHub 
- DM [@lexnlin](https://x.com/lexnlin) or [@blueemi99](https://x.com/blueemi99) 
- Email us at [hello@tasteskill.dev](mailto:hello@tasteskill.dev)

## Installing

The [`npx skills add`](https://github.com/vercel-labs/agent-skills) CLI scans the `skills/` folder in this repo, so **all skills below (code and image-generation) install the same way.**

```bash
npx skills add https://github.com/Leonxlnx/taste-skill
```

Install a single skill by its **install name** (the `name:` field inside the SKILL frontmatter, not the folder name):

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

You can also copy any `SKILL.md` into your project or paste it into ChatGPT / Codex conversations.

### Install as a Claude Code plugin

If you only use Claude Code, you can install the whole repo as a plugin from the included `.claude-plugin/` manifests. Every skill is namespaced under `taste-skill:` (for example, `/taste-skill:imagegen-frontend-web`), so they won't collide with your other skills — no `npx skills` step required.

Run these inside Claude Code:

```
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```

Run `/plugin update` later to upgrade installed plugins to new versions. Claude Code also checks for updates automatically at startup.

### Updating from the previous version

The default `taste-skill` (install name `design-taste-frontend`) is now **v2 (experimental)**, a substantial rewrite of the original v1. If you already have v1 installed, just re-run the install command and you will be upgraded:

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

The install name did not change, so no script updates are needed. The newer SKILL.md replaces the older one in place.

If you depend on the exact behavior of v1 and want to pin to it explicitly:

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend-v1"
```

See [CHANGELOG.md](CHANGELOG.md) for the full v1 to v2 diff and the rationale.

## Skills

Each skill does one job; you do not need all of them at once. **Implementation skills** output code. **Image-generation skills** output reference images only.

The `Install name` column is the exact value you pass to `--skill`.

| Skill (folder) | Install name | Description |
| --- | --- | --- |
| **[taste-skill](skills/taste-skill/SKILL.md)** | `design-taste-frontend` | 🆕 **v2 (experimental)** - substantial rewrite of the default skill. Reads the brief, infers the design language, tunes three dials (VARIANCE / MOTION / DENSITY). Brief inference, design-system map, hard em-dash ban, canonical GSAP code skeletons, redesign-audit protocol, strict pre-flight check. Actively iterating toward v2.0.0 stable. |
| **[taste-skill-v1](skills/taste-skill-v1/SKILL.md)** | `design-taste-frontend-v1` | The original v1 of taste-skill, preserved for projects depending on its exact behavior. Use only if the v2 default breaks something specific in your workflow. |
| **[gpt-tasteskill](skills/gpt-tasteskill/SKILL.md)** | `gpt-taste` | Stricter variant for GPT/Codex: higher layout variance, stronger GSAP direction, aggressive anti-slop. |
| **[image-to-code-skill](skills/image-to-code-skill/SKILL.md)** | `image-to-code` | Image-first pipeline: generate site references, analyze them, then implement the frontend to match. |
| **[redesign-skill](skills/redesign-skill/SKILL.md)** | `redesign-existing-projects` | Existing projects: audit the UI first, then fix layout, spacing, hierarchy, styling. |
| **[soft-skill](skills/soft-skill/SKILL.md)** | `high-end-visual-design` | Polished, calm, expensive UI with softer contrast, whitespace, premium fonts, spring motion. |
| **[output-skill](skills/output-skill/SKILL.md)** | `full-output-enforcement` | When the model ships half-finished work: full output, no placeholder comments. |
| **[minimalist-skill](skills/minimalist-skill/SKILL.md)** | `minimalist-ui` | Editorial product UI (Notion/Linear vibes), restrained palette, crisp structure. |
| **[brutalist-skill](skills/brutalist-skill/SKILL.md)** | `industrial-brutalist-ui` | Hard mechanical language: Swiss type, sharp contrast, experimental layout. |
| **[stitch-skill](skills/stitch-skill/SKILL.md)** | `stitch-design-taste` | Google Stitch-compatible rules, including optional `DESIGN.md` export format. |

### Image generation skills

These produce design images only (no code). Use with ChatGPT Images, Codex image mode, or any agent that generates images.

| Skill (folder) 