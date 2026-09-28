Praxist: meet your personal R&amp;D team 

Praxist is an autonomous research system for measurable, computer-executable
research. It coordinates parallel research peers, task-owned evaluation,
durable evidence, and generation-to-generation synthesis.

Praxist treats research as a persistent process rather than a sequence of
disconnected prompts. Use it when a project already runs and its objective is
measurable, but the best path forward is still unknown.

## Install Praxist

Install the complete runtime integrations and finish first-use setup with one
command:

```bash
python3 -m pip install --index-url https://pypi.org/simple "praxist[agents,codex]" && praxist setup --interactive --install-skills codex
```

The local wizard covers the Fair Source License, User Agreement, privacy,
runtime profile, masked credentials, Codex skills, writable examples,
and readiness checks. It does not select a research project or launch a run.
For Claude Code, use the
[host-specific one-line command](docs/getting-started/installation.md#install-and-configure).

For an agent-managed installation, open Codex:

```bash
codex --yolo
```

Then ask it to install and configure Praxist using the packaged OOBE runbook,
and to stop after readiness checks.

Before starting research, read the [Quickstart](docs/getting-started/quickstart.md)
and [Your First Task](docs/getting-started/first-task.md). They describe the
separate takeover step and the project contract it creates.

Choose **Codex-native mode** to use an existing Codex subscription without an
API key. For sustained research, Praxist generally favors
[open-source model APIs](docs/guides/open-source-model-apis.md) with a high
observed cache-hit rate. The setup wizard also supports other API-backed
profiles.

## Use Praxist Through Codex

We recommend Codex as the interface for operating Praxist. Praxist is not a
replacement for Codex: Codex remains the interactive agent that understands
your project, communicates with you, and uses development tools. Praxist adds
the persistent research loop, parallel peers, evidence protocols, scheduling,
and lifecycle control.

After installation, open Codex in the root of an already runnable research
project and invoke `$praxist-takeover`. The takeover skill inspects readiness,
creates or repairs the task harness, validates its evaluator and evidence
contract, and launches the run after the required gates pass. A precise brief
produces a better research plan; include the objective, metrics, constraints,
resources, exploration choices, and whether launch is authorized.

 Example takeover brief 

```text
$praxist-takeover

Treat the current directory as the existing runnable research project. Verify
the baseline and its evaluation path before changing anything.

Optimize while preserving .
Use peers for up to generations within
 . Use the runtime and model provider selected during
setup. literature search, QD, and
 generation-zero DIG.

Do not download new datasets or replace required project assets. Build a
separate task harness with explicit metric directions, baseline provenance,
protocol-integrity checks, evidence maturity rules, and justified retention
lanes. After readiness checks pass, . Report the task path, run ID, evidence contract, generation
close policy, and monitor command.
```

Other bundled skills:

| Skill | Purpose |
|---|---|
| `praxist-takeover-codex` | No-key takeover using the saved Codex login |
| `praxist-onboarding` | Explain Praxist and inspect local readiness |
| `praxist-task-initialization` | Build or repair a task harness without launching |
| `praxist-interactive-task-init` | Design a task through confirmation-first setup |
| `praxist-control` | Start, stop, resume, monitor, and inspect runs |
| `praxist-diagnostic` | Diagnose run health and produce reports |
| `praxist-scientific-research` | Gather sourced literature and benchmark context |
| `praxist-runtime-install` | Install or repair runtime dependencies and credentials |
| `terminal-line-plot` | Draw metric trends in the terminal |

See [Agent Skills](docs/user-guide/skills.md) for invocation syntax and the
generated [Skills Reference](docs/reference/skills.md) for the complete
contracts.

## What Praxist Provides

| Capability | Purpose |
|---|---|
| Parallel research peers | Explore competing hypotheses and implementations concurrently |
| Multi-generation synthesis | Carry useful evidence and strategy into later generations |
| Durable evidence lanes | Preserve candidates through incubator, frontier, and Gems state |
| Multi-metric evaluation | Rank task-defined evidence, including Pareto-optimal tradeoffs |
| [Quality-Diversity (QD)](docs/guides/qdig-cohort-allocator.md) and optional [Deep Innovation Gate (DIG)](docs/guides/deep-innovation-gate.md) | Maintain diversity without forcing one exploration policy |
| Central resource scheduling | Adapt experiment admission to observed resource pressure |
| Resume, replay, and monitoring | Keep long-running research inspectable and recoverable |
| Plugin boundaries | Support multiple runtimes, providers, tools, budgets, and workflows |

## Praxist And The Task Project

| Praxist owns | The task project owns |
|---|---|
| Research orchestration, lifecycle, evidence protocols, replay, scheduling, and extension interfaces | Research objective, executable code, evaluator, metrics, baselines, prompts, roles, and domain constraints |

Praxist contains no task-specific scientific assumptions. A task remains the
single source of truth for what should be tested and what counts as valid evidence.

## Operate A Run

```bash
praxist status --json
praxist --monitor --latest
praxist stop 
praxist resume 
```

`Ctrl-C` closes only the monitor; it does not stop the research run.

## Examples And Templates

```bash
praxist examples list
praxist examples install rocket_booster_recovery
praxist examples install rocket_booster_recovery_rust
```

Complete examples are writable reference projects. `templates/task