# Sprix SAGE Router

### Checkpoint-aware mid-execution rerouting for open A2A networks

[](https://github.com/wang2122/sprix-sage-router/actions/workflows/tests.yml)
[](https://www.python.org/)
[](LICENSE)
[](#project-status)

**An open-source research output of [Sprix AI](#about-sprix-ai) at 屿智同行.**

Choose whether an in-flight task should **continue**, **recruit collaborators**, or **hand off** after accounting for completed DAG nodes, reusable artifacts, observed partial quality, remaining work, failures, budget, and deadline.

[Quick start](#quick-start) · [Algorithm](ALGORITHM.md) · [Related work](RELATED_WORK.md) · [A2A integration](docs/INTEGRATION.md) · [Operations](docs/OPERATIONS.md) · [Benchmark](#benchmark) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md)

---

## Why SAGE?

Agent discovery tells a system which agents exist. It does not answer the harder runtime question: **who should work with whom after execution has already begun?**

SAGE—**State-Aware Graph Exchange**—is the decision layer between A2A discovery and task execution. It evaluates three routes in one auditable objective:

| Route | Ownership | Best used when |
|---|---|---|
| **SELF** | Incumbent agent | Existing capability and accumulated context are sufficient |
| **COLLABORATE** | Incumbent retains ownership | A small complementary team covers missing requirements |
| **HANDOFF** | A peer takes full ownership | Specialist advantage exceeds context-transfer loss |

SAGE is designed to sit above the [Agent2Agent (A2A) protocol](https://a2a-protocol.org/latest/). A2A provides Agent Cards, messages, tasks, artifacts, authentication, and transport. SAGE decides **which feasible agent configuration should execute the task, in which mode, and why**.

 Figure 1. SAGE filters candidates, compares all three routing modes, jointly searches assignments and schedules, ranks feasible plans, and learns from execution evidence. 

## Research focus

SAGE is deliberately narrow: **checkpoint-aware reconfiguration after execution has begun**.

- **Concrete continuation value.** The router preserves completed requirements and combines in-flight completion, observed partial quality, current ownership, and artifact portability to estimate how much work each candidate must actually redo.
- **Comparable runtime actions.** SELF, COLLABORATE, and HANDOFF share one permission-, budget-, and deadline-constrained action space. Progress-masked and static-coalition baselines receive the same registry and limits.
- **Requirement-conditioned evidence.** Reliability is tracked per agent and requirement instead of assuming that one reputation score transfers across skills.
- **Trajectory-level falsification.** A separate evaluator replays checkpoints and scores artifact reuse, added cost, recovery latency, wasted work, and final quality without calling SAGE's switching equation.

Noisy-OR, beam search, a linear utility, Beta beliefs, online logistic regression, and DAG-induced communication edges are not claimed as inventions. They are replaceable implementation mechanisms. The repository also provides permission-first filtering, bounded candidate search, workload-sensitive quotes, auditable alternatives, degraded-route flags, state persistence, and transport-neutral A2A plans as engineering features.

## Core algorithm

For task requirement \(r\), SAGE combines global and requirement-conditioned trust into calibrated capability \(q_{a,r}\). If the current owner has completed fraction \(f_r\), a candidate owner reuses fraction \(\eta_r\):

$$
\eta_r=\begin{cases}f_r,&\text{owner retained}\\f_r\tau_r,&\text{owner changed}\end{cases},\qquad
\bar q_{a,r}=\eta_r q^{\mathrm{current}}_r+(1-\eta_r)q_{a,r}
$$

Here \(\tau_r\) is artifact portability. Only the assigned owner contributes requirement coverage; adding an unassigned teammate no longer creates a noisy-OR quality gain. The same reused fraction reduces projected remaining cost and duration, so lost work is not charged again inside the learned success probability.

SAGE jointly searches calibrated requirement owners and their schedule. Work assigned to one agent is serialized, work on independent agents can run concurrently, and team-level cost and critical-path latency are checked again after construction.

Every feasible route is ranked by:

$$
U(m,S,z,E)=V\hat p_\theta(y=1\mid x,m,S,z,E)-\lambda_c C-\lambda_l L-\lambda_r R-\lambda_h H-\lambda_o O-\lambda_u\mathcal U+\beta\mathcal B
$$

Here \(z\) is role assignment, \(E\) is the induced communication topology, \(H\) is context-transfer loss, \(O\) is coordination overhead, and \(\mathcal U/\mathcal B\) support uncertainty-aware exploration. The full design and limitations are documented in [ALGORITHM.md](ALGORITHM.md).

## Quick start

The reference implementation requires Python 3.10+ and has no runtime dependencies.

```bash
git clone https://github.com/wang2122/sprix-sage-router.git
cd sprix-sage-router
python demo.py
```

Run the verification suite:

```bash
python -m unittest -v
python benchmark.py
python benchmark_dynamic.py
python benchmark_trust.py
```

Minimal usage:

```python
from sprix_sage import (
 Agent,
 ExecutionOutcome,
 ExecutionState,
 Requirement,
 SAGERouter,
 Task,
)

agents = [
 Agent("planner", {"planning": 0.92, "coding": 0.55}, cost=0.08, latency_ms=900),
 Agent("coder", {"planning": 0.35, "coding": 0.96}, cost=0.12, latency_ms=1200),
]

task = Task(
 "build-feature",
 requirements=(
 Requirement("planning", 0.4),
 Requirement("coding", 0.6, depends_on=("planning",)),
 ),
 value=1.0,
 budget=0.30,
 deadline_ms=4000,
 progress=0.35,
)

router = SAGERouter(agents, incumbent_id="planner")
state = ExecutionState(
 active_agents=("planner",),
 active_assignments={"planning": "planner", "coding": "planner"},
 completed_requirements=frozenset({"planning"}),
 inflight_requirement="coding",
 inflight_progress=0.35,
 inflight_quality=0.72,
 artifact_transferability={"planning": 0.95, "coding": 0.40},
)
trac