&nbsp;

 &nbsp;

 &nbsp;

 &nbsp;

 &nbsp;

 The easiest way to get Taste Skill results: download TasteCode . Its design agent briefs, builds and visually reviews your UI. Source on GitHub . 

 Sponsors 

 Sidrune AI : one API for GPT, Claude, and other leading AI models. Sign up through this link and get $3 in API credit. 

 interfaces.dev · A design engineering magazine by Jakub Krehel 

 React Bits · animated React components for creative interfaces 

 IMG.LY · CreativeEditor SDK 

 Sent.dm · messaging APIs for SMS, WhatsApp, and RCS 

 Become a sponsor 

**Taste Skill** is a set of Agent Skills that make coding agents design websites instead of assembling the average landing page. The default skill gives the agent an art direction, real pictures and a way to check its own work in a real browser.

Pages it has built, each from one brief:

The photographs are real, found in open archives and credited by the skill ([credits](examples/v2/CREDITS.md)). Watch the [launch film](https://github.com/Leonxlnx/taste-skill/releases/tag/v2.0.0).

 Install · How it works · Skills · FAQ · Sponsors · License 

## Install

```bash
npx skills add https://github.com/Leonxlnx/taste-skill
```

That installs every skill in this repo with the [`npx skills`](https://github.com/vercel-labs/agent-skills) CLI. To install one, pass its install name:

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

The default skill runs its scripts with **Node 22+** and an installed **Chrome, Edge or Chromium**. It installs nothing and needs no API keys. Finding pictures needs network access.

 Claude Code plugin 

Run these inside Claude Code. Every skill is namespaced under `taste-skill:`, so they do not collide with your other skills.

```
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```

`/plugin update` upgrades it later.

 Codex plugin 

```bash
codex plugin marketplace add Leonxlnx/taste-skill
codex plugin add taste-skill@taste-skill
```

Start a new Codex session afterwards so the skills are loaded.

 From a clone, linked instead of copied 

`./install.sh` symlinks the skills into Claude Code (`--codex` for Codex, `--all-agents` for both), so a `git pull` updates them in place. `./install.sh --list` shows every install name.

Already have the skill? Run the install command again. The install name did not change, and the older versions stay available under their own names (see [Skills](#skills)).

## How v2 works

The default skill is built from a study of 247 curated sites. A build runs in six steps:

1. Reads the brief and lists what only this client has.
2. A script deals three of 20 researched directions and the agent picks one.
3. Finds the idea: one sentence tying the client's own material to that direction.
4. Builds with real pictures and footage from open collections, credited.
5. Checks the page in a real browser at three widths and fails it on slop.
6. Looks at its own screenshots and fixes the top three problems, up to three rounds.

A build takes roughly 30 to 45 minutes and a few hundred thousand tokens. Details are in the [changelog](CHANGELOG.md) and the [study](skills/taste-skill/references/research.md).

## Skills

Each skill does one job. You do not need all of them. The **install name** is the value you pass to `--skill`.

| Skill | Install name | What it does |
| --- | --- | --- |
| **[taste-skill](skills/taste-skill/SKILL.md)** | `design-taste-frontend` | v2. Art direction for landing pages, marketing sites, portfolios and product pages, in any stack. Works as described above. |

 Skills for a specific job (8) 

| Skill | Install name | What it does |
| --- | --- | --- |
| **[redesign-skill](skills/redesign-skill/SKILL.md)** | `redesign-existing-projects` | Existing projects: audit the UI first, then fix layout, spacing, hierarchy and styling. |
| **[image-to-code-skill](skills/image-to-code-skill/SKILL.md)** | `image-to-code` | Generate site references, analyse them, then build the frontend to match. |
| **[gpt-tasteskill](skills/gpt-tasteskill/SKILL.md)** | `gpt-taste` | A stricter variant for GPT and Codex: more layout variance, stronger motion direction. |
| **[soft-skill](skills/soft-skill/SKILL.md)** | `high-end-visual-design` | Calm, polished UI: soft contrast, whitespace, spring motion. |
| **[minimalist-skill](skills/minimalist-skill/SKILL.md)** | `minimalist-ui` | Editorial product UI with a restrained palette and crisp structure. |
| **[brutalist-skill](skills/brutalist-skill/SKILL.md)** | `industrial-brutalist-ui` | Hard mechanical language: Swiss type, sharp contrast, experimental layout. |
| **[stitch-skill](skills/stitch-skill/SKILL.md)** | `stitch-design-taste` | Rules for Google Stitch, with an optional `DESIGN.md` export. |
| **[output-skill](skills/output-skill/SKILL.md)** | `full-output-enforcement` | For when the model ships half-finished work: full output, no placeholder comments. |

 Image generation skills (3) 

These produce design images only, no code. Use them with ChatGPT Images, Codex image mode or any agent that generates images, then hand the frames to your coding agent.

| Skill | Install name | What it does |
| --- | --- | --- |
| **[imagegen-frontend-web](skills/imagegen-frontend-web/SKILL.md)** | `imagegen-frontend-web` | Website comps: hero, landing page, multi-section. |
| **[imagegen-frontend-mobile](skills/imagegen-frontend-mobile/SKILL.md)** | `imagegen-frontend-mobile` | Mobile screens and flows for iOS, Android and cross-platform. |
| **[brandkit](skills/brandkit/SKILL.md)** | `brandkit` | Brand-kit boards: logo directions, palettes, type, applications. |

### Which one should I use?

- Building a new public page: **taste-skill**.
- Improving a page that already exists: **redesign-skill**.
- The visual direction is already decided: **soft-skill**, **minimalist-skill** or **brutalist-skill**.
- You want images first, then code: an image-generation skill, or **image-to-c