Infrastructure for continually self‑improving agents 

[](https://github.com/Human-Agent-Society/reef/actions/workflows/ci.yml)
[](https://pypi.org/project/reef-infra/)
[](pyproject.toml)
[](LICENSE)

English | [中文](README.zh.md)

Reef is the first open-source infrastructure for continual self-improving agents.
It connects agent inference, feedback, learning, and versioned delivery. Use it
to train model weights with Slime and SGLang, or improve an agent's harness, including its prompts, rules, and skills.

**🚀 [Get started](https://reefinfra.ai/docs/getting-started/quickstart/) |
🗺️ [Roadmap](https://github.com/Human-Agent-Society/reef/issues/25) |
📣 [Launch post](https://x.com/ao_qu18465/status/2094867930081337730) |
💬 [Join Discord](https://discord.gg/5y8e5f937k) |
📱 [Join WeChat Group](docs/community/wechat.md)**

## 🎯 When to use Reef

Use Reef when you want your agent to keep improving simply by learning from how you interact with your agent.

| Your goal | Learning path | What you need |
|---|---|---|
| Keep getting stronger model designed for you | Model weight training | A trainable model, a supported GPU stack, and feedback your recipe can use |
| Get your harness to self-improve | Harness optimization | A model endpoint, representative tasks, and an evaluator; no local training GPUs |
| Scientific discoveries | Test-time training | An execution environment, a correctness checker, and a measurable objective |

## 🧩 How Reef fits your stack

| Ability | Inference engine (vLLM, SGLang, …) | RL training framework (Slime, veRL, AReaL, …) | **Reef** |
|---|:---:|:---:|:---:|
| Serves live traffic | ✅ | ❌ | ✅ |
| Trains weights | ❌ | ✅ | ✅ |
| Version management | ❌ | ❌ | ✅ |
| Stays live through updates | ❌ | ❌ | ✅ |
| Evolves beyond weights (skills, harness) | ❌ | ❌ | ✅ |

## 🔄 How it works

Reef processes each learning cycle in four steps. The table also shows which
modules implement each step.

| Step | What happens | Where it lives |
|---|---|---|
| **1&nbsp;·&nbsp;Serve** | Serve agent requests and record interactions. | [`service/`](reef/service) — agent requests and interaction records [`runtime/`](reef/runtime) — inference and artifact updates |
| **2&nbsp;·&nbsp;Observe** | Match feedback to recorded interactions. | [`storage/records.py`](reef/storage/records.py) — stored interactions and feedback [`train/processors/`](reef/train/processors) — feedback matching and eligibility |
| **3&nbsp;·&nbsp;Grow** | Produce an update from eligible records. | [`recipe/`](reef/recipe) — recipe integration [`train/`](reef/train) — batches and update jobs |
| **4&nbsp;·&nbsp;Commit** | Apply the configured selection policy and publish accepted updates. | [`train/evaluation/`](reef/train/evaluation) — candidate evaluation [`artifact/`](reef/artifact) — version history [`surface/`](reef/surface) — artifact delivery |

## 📦 Installation

> 💡 **Note**
>
> Reef's artifact and checkpoint functionality requires the `git-lfs` system
> package. Reef initializes Git LFS locally for its artifact repositories.

We recommend [uv](https://docs.astral.sh/uv/) for managing packages, and the
commands below use it.

### From PyPI

```bash
uv venv && source .venv/bin/activate
uv pip install reef-infra
python3 -c "import reef; print(reef.__version__)"
```

### From source

```bash
git lfs install
git clone https://github.com/Human-Agent-Society/reef.git
cd reef
uv venv && source .venv/bin/activate
uv pip install -e .
python3 -c "import reef; print(reef.__version__)"
```

Use the source checkout for development and for the training examples below.

## 🔧 Using Reef

Reef supports two learning surfaces: model **weights** and agent **harnesses**.
The deployment's recipe determines which surface its scenarios update.

As a minimal example, start Reef as a pure inference server:

```bash
uv run reef serve --inference.model-path Qwen/Qwen2.5-1.5B-Instruct
```

### Weight-training deployment

#### Start the deployment

The following example starts the SAO (arXiv:2607.07508) example deployment. Run it
from a Reef checkout in an environment that satisfies the GPU requirements in
[Evolve your model](https://reefinfra.ai/docs/user-guide/evolve-your-model/).

```bash
uv pip install -e ".[slime]" && uv pip install --no-deps --group runtime

export MODEL_PATH="Qwen/Qwen2.5-1.5B-Instruct"
export REEF_TOKEN="reef-local"

reef serve -c recipes/sao/examples/imo_answerbench/serve.yaml \
 --inference.model-path "$MODEL_PATH" \
 --reef.port "8900"

curl -f http://127.0.0.1:8900/healthz # ready to serve
```

#### Send an inference request and report feedback

Send inference requests through Reef and report a score for each response. The
SAO recipe uses each eligible scored rollout to run a training step.

Reef's inference endpoint is OpenAI- and Anthropic-compatible: `/v1/chat/completions`
and `/v1/messages` take the provider's own request body. A request includes the
`x-reef-scenario` header; a new name creates a scenario using the deployment's
configured recipe. Requests do not select recipes.

The response body uses the provider's OpenAI-compatible format. Reef adds the
`x-reef-agent-record-id` response header. Its value is the **receipt** that a
later report uses to identify this interaction. A report can contain a numeric
`score`, textual or structured `feedback`, and the receipts it evaluates. This
example reports both a score and a short explanation.

```python
import os
import httpx

reef = httpx.Client(
 base_url="http://127.0.0.1:8900",
 headers={"Authorization": f"Bearer {os.environ['REEF_TOKEN']}", "x-reef-scenario": "hello-reef"},
 timeout=300,
)

# Send a provider-compatible inference request
response = reef.post(
 "/v1/chat/completions",
 json={
 "model": os.environ["MODEL_PATH"],
 "messages": [{"role": "user", "content": "Return exactly: reef is ready"}],
 },
)

response.raise_for_status()
receipt = response.headers["x-reef-agent-record-id"]
answer = response.json()["choices"][0]["message"]["content"]

# Sending re