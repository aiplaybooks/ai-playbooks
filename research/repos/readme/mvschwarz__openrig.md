# OpenRig

[](https://www.npmjs.com/package/@openrig/cli) [](https://www.npmjs.com/package/@openrig/cli) [](LICENSE) [](https://github.com/mvschwarz/openrig/stargazers)

A harness wraps a model. A rig wraps your harnesses. Define your agent team in YAML, boot it with one command. Claude Code and Codex in the same rig, managed as one system.

OpenRig is open-source software for building and running your own network of agents. It turns AI coding agents from a pile of terminal sessions into a persistent, organized team. Talk to a lead agent about the outcome you want; it can coordinate specialists across teams and bring you results and decisions that need your attention. Start with a repository and one useful change, then keep the team's work and context at the same addresses.

It's the open-source system behind my AI civilization experiments.

**Guide:** [Getting started](docs/reference/getting-started.md) · **Stuck?** [Help](docs/reference/help.md) · **Questions:** [Q&A](https://github.com/mvschwarz/openrig/discussions/92) · **Updates and demos:** [@_feralmachine on X](https://x.com/_feralmachine)

## See it running

**Start here:** [the guided first-use path](docs/reference/getting-started.md): install, launch a two-agent team in your repository, and get one reviewed change.

Not setting this up today? Get the next walkthrough and occasional OpenRig updates → https://openrig.dev/follow

## Install and first run

Requires Node.js 22 or 24 and tmux, on macOS or Linux. On a Mac with Apple silicon, use Node.js 22 ([compatibility history](docs/releases/v0.5.15.md#known-compatibility-limitation)). Native Windows is not supported yet, and WSL2 has not been tested. Launching a rig writes provider hooks and workspace trust settings. Before running the commands below, read [what OpenRig changes on your machine](#what-openrig-changes-on-your-machine) and back up the relevant files.

```bash
npm install -g @openrig/cli
rig setup --dry-run
```

To install with Bun instead, run `bun add -g @openrig/cli`. OpenRig still runs on Node.js, so install Node.js 22 as well. Bun may block this package's postinstall script, in which case the Node.js and SQLite check described under [what OpenRig changes on your machine](#what-openrig-changes-on-your-machine) does not run at install time.

Choose the working account you already have: **Claude Code, Codex, or both**. Reuse an explicit choice; no second subscription is required. `rig setup --dry-run` previews the broader setup, but applying `rig setup` checks both harnesses and cmux. It is optional for the [selected-provider path](docs/reference/getting-started.md#choose-your-providers).

Before launching, your agent asks once: **“Allow your agents to run OpenRig commands without repeated permission prompts?” Yes — recommended / No — keep prompts.** This covers every `rig` command, including starting/stopping agents and configuration, at personal project scope unless you explicitly choose user-wide sessions. It is not global YOLO or permission to invent work. On Yes, the agent [adds and verifies native rules](docs/reference/getting-started.md#have-your-agent-configure-permissions); No or no answer leaves settings unchanged. An existing explicit choice is reused. Say “Undo the OpenRig command allowances added by this setup” to remove only its additions.

Check `tmux -V` and only your selected CLI/login: `claude --version` plus
`claude auth status`, or `codex --version` plus `codex login status`. If needed,
sign in once with `claude auth login` or `codex login`; do not install or log in
to an unused provider.

| Team | Starter | Models |
| --- | --- | --- |
| Two Codex agents | `first-project` | Both `gpt-6-astra` (unchanged) |
| Two Claude agents | `first-project-claude` | Configured native Claude default |
| Claude owner + Codex checker | `first-project-mixed` | Claude default + `gpt-6-astra` |

All three use the same owner/checker roles and task. Show the selected runtime,
configured model and command before launch; confirm the account supports the
model instead of silently falling back. The kernel starts automatically and
selects from available authenticated providers independently of these two project
agents. A missing unused provider is not a setup requirement.

```bash
cd /path/to/your/repository
starter=first-project # or first-project-claude or first-project-mixed
rig specs preview "$starter" --kind rig
rig up "$starter" --cwd . --plan
rig up "$starter" --cwd .
rig tui --shared
```

The kernel provides separate operational support and the shared dashboard. To detach without stopping the dashboard, press Ctrl-b then d; `rig tui --shared` returns to that view. Plain `rig tui` opens an independent view. Closing a viewing terminal does not mean you should relaunch the team.

Check project-seat readiness with `rig ps --nodes --rig "$starter"` and resolve any authentication, trust or permission prompt before assigning work. Then give the owner one bounded outcome from your repository:

```bash
rig send "dev-owner@$starter" 'Implement . Track the task in the queue and return its ID. Keep it local, verify the behavior, ask dev-check in this rig to check the exact candidate, and record the result and how I can try it.'
rig queue list --destination "dev-owner@$starter" --limit 1000
```

Sending a message does not itself create a queue item; the owner records the task. Read the final artifact and the review of its exact candidate, then return to the same owner for the next change. [The guided first-use path](docs/reference/getting-started.md) covers readiness, a useful task, a reviewed result, Herdr/cmux terminals and recovery.

Not setting this up today? Get the next walkthrough and occasional OpenRig updates → https://openrig.dev/follow

## Community

- **Questions:** [Discussions › Q&A](https://github.com/mvschwarz/openrig/discussions/categories/q-a)
- **Bugs and feature requests:** [open an issue](https://github.com/mvschwarz/openrig/issues/new/choose)
- **Contribu