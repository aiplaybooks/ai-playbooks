# VibeWise

**You build. AI writes.**

A plugin for **Claude Code** and **Codex** that puts learning first and keeps you in control while AI writes the code you designed. The AI **asks for your approach first**, helps you examine tradeoffs, and explains unfamiliar concepts. You shape the design and decide when it's ready to implement. The AI writes the code, then explains what it changed and why.

For anyone who wants to learn as they build—whether you're an aspiring engineer, a junior developer, or an experienced engineer exploring an unfamiliar stack. Practice planning how the pieces fit together, anticipating failures, and checking the result while keeping ownership of the decisions.

## Table of Contents

- [Get started](#get-started)
 - [Claude Code](#claude-code)
 - [Codex](#codex)
- [What it feels like](#what-it-feels-like)
- [Make it yours](#make-it-yours)
- [Updating](#updating)
- [License](#license)

## Get started

You need an up-to-date [Claude Code](https://code.claude.com/docs/en/setup) or
[Codex](https://developers.openai.com/codex), and
[Python 3](https://www.python.org/downloads/). In Claude Code, VibeWise uses Python
to restore learning context and reset learning notes. In Codex, only reset needs it.
No extra Python packages are needed.

### Claude Code

Install from the built-in **Anthropic Directory**. In Claude Code, run:

```text
/plugin install vibe-wise@anthropic-plugin-directory
```

Choose an installation scope and confirm. No marketplace setup is needed.

Restart Claude Code in the project you want to work on, then run:

```text
/vibe-wise:learn
```

Setup asks one question at a time. Use the arrow keys and Enter for choices; pick **Use defaults** to skip preference setup. Then ask Claude to build something. Starting fresh or joining an unfamiliar repository both work. For an existing repository, Claude first inspects the code and sketches a small system map.

 Alternative: install through GitHub 

If Anthropic Directory isn't available in your Claude Code version, use the GitHub
marketplace. Choose one installation method; you don't need both.

Run these commands **one at a time** in Claude Code. First, add the marketplace:

```text
/plugin marketplace add nykooi1/vibe-wise
```

After it finishes, install the plugin:

```text
/plugin install vibe-wise@vibe-wise
```

Enable automatic updates through `/plugin` → **Marketplaces** → **vibe-wise** →
**Enable auto-update**. This is off by default for third-party marketplaces.
Restart Claude Code, then run `/vibe-wise:learn` in your project.

### Codex

In a terminal, run these commands **one at a time**. First, add the marketplace:

```sh
codex plugin marketplace add nykooi1/vibe-wise
```

After it finishes, install the plugin:

```sh
codex plugin add vibe-wise@vibe-wise
```

Start Codex in your project and run `$vibe-wise:learn`. Run it again at the start
of each Codex session, and whenever Codex seems to have lost track of learning
mode. It resumes from your saved notes without repeating setup. To reset, run
`$vibe-wise:reset`. Claude Code and Codex share the same `.vibe-wise/` notes.

In Codex, the commands in this guide use `$` instead of `/`: `/vibe-wise:learn`
becomes `$vibe-wise:learn`.

## What it feels like

You're building a Notion-style notes app: users sign in, create and edit private
notes, and organize them into folders. Here, you're working through how notes and
folders relate—and what should happen when someone deletes a folder.

This condensed example is adapted from a real learning session. Later implementation
steps are illustrative; intervening design discussions are omitted.

**You:**

```text
A note can be in several folders. Deleting a folder should delete its notes.
```

**Claude / Codex:**

```text
✦ Build checkpoint: Deleting a shared note

"Trip ideas" is in both Travel and Summer. Deleting it removes it from both.

When someone deletes Travel, what should happen to that note in Summer?
```

**You:**

```text
Keep it in Summer. If it has no folders left, keep the note outside any folder.
```

**Claude / Codex:**

```text
That separates deleting a folder from deleting a note.

✦ Build checkpoint: Connecting notes and folders

How would you represent which folders a note belongs to, without copying the note?
```

**You:**

```text
A links table with note_id and folder_id. Deleting a folder removes its links,
not the notes.
```

**Claude / Codex:**

```text
Each link records one membership. Several links can point to the same note;
a note with no links is unfiled.

notes ← folder links → folders

✦ Design checkpoint: Folder membership

Proposed: store notes once and track folder membership in a links table.
Deleting a folder removes its links and keeps the notes. This supports multiple
folders per note; loading a folder's notes needs a lookup through those links.

Confirming records this design. We still need to work through access rules
and technology choices before writing code.

❯ 1. Confirm and continue
 This approach makes sense to me; move to the next piece.
 2. Discuss
 Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Confirm and continue.
```

*Later, after the remaining choices for this step are worked through...*

**Claude / Codex:**

```text
✦ Implementation checkpoint: Folder membership

I'll add the agreed tables and folder-deletion operation, then test that deleting
a folder preserves its notes and their membership in other folders.
This step builds storage behavior; the UI comes later.

❯ 1. Implement this step
 This approach makes sense to me; write the code for this step.
 2. Discuss
 Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Implement this step.
```

*Claude or Codex writes the code and runs the tests.*

**Claude / Codex:**

```text
✦ Implementation report: Folder membership

- Added the schema migration: each membership references one note and one folder.
- Added folder 