# Kev

Small Jev-like decision models you can train and run yourself.

Kev is a family of small decision models built on Qwen3.5 and Qwen3.8 and based on the architecture described in [Jev's Architecture Unmasked](https://archerhume.com/posts/jevs-architecture-unmasked). You can use the pretrained weights or train your own. The API matches TypeSafe's [System One](https://docs.typesafe.ai/api), so you can point their Python SDK at your local server.

## Highlights

- Yes/no (`noul`), multiple-choice (`choice`) and rating (`score`) questions in one request. The questions share the text but can't read each other.
- Calibrated probabilities by default: each checkpoint ships with a temperature fitted on held-out data.
- Drop-in for Jev: the TypeSafe Python SDK works against a Kev server unchanged.
- Four sizes, from a 0.8B that runs on a laptop to a 27B for a single data-centre GPU.
- Fine-tune on your own labelled examples. A coding-agent skill runs the whole loop on Modal, from finding your questions to serving the result.
- Deploy your own HTTPS endpoint with one command. It scales to zero when idle.
- Try it in the browser first: [huggingface.co/spaces/jaredpalmer/kev](https://huggingface.co/spaces/jaredpalmer/kev).

## Models

Start with Kev-4B. Move to Kev-9B if you have a bigger GPU, or to Kev-27B if you have an 80 GB GPU and want the most accurate Kev. Use Kev-0.8B when size matters more than accuracy.

| Model | Base | Accuracy: New Sources | Accuracy: Trained Sources | Brier: New Sources | Runs on | Model Card |
|---|---|---|---|---|---|---|
| [Kev-0.8B](https://huggingface.co/jaredpalmer/kev-0.8b) | Qwen3.5-0.8B-Base | 0.648 / 0.697 | 0.827 / 0.838 | 0.481 / 0.416 | Any Apple Silicon Mac, L4 | [Details](docs/model-cards/kev-0.8b.md) |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | Qwen3.5-4B-Base | 0.817 / 0.838 | 0.873 / 0.865 | 0.269 / 0.242 | 32 GB Mac, L40S, H100 | [Details](docs/model-cards/kev-4b.md) |
| [Kev-9B](https://huggingface.co/jaredpalmer/kev-9b) | Qwen3.5-9B-Base | 0.822 / 0.852 | 0.872 / 0.874 | 0.286 / 0.237 | 32 GB Mac, L40S, H100 | [Details](docs/model-cards/kev-9b.md) |
| [Kev-27B](https://huggingface.co/jaredpalmer/kev-27b) | Qwen3.8-27B (post-trained) | **0.848 / 0.896** | 0.866 / 0.870 | **0.236 / 0.164** | B200, H200, H100 80 GB | [Details](docs/model-cards/kev-27b.md) |
| Jev | Hosted | 0.857 / – | 0.845 / – | 0.211 / – | TypeSafe's API | – |

Each cell is **development / test**. "New sources" means datasets and policy rules Kev never saw during training. It is the closest thing here to your own questions. "Trained sources" means held-out examples from the datasets Kev was trained on. We pick checkpoints using the development sets and read each test set only once per released model. Jev has only been run on the development sets. Brier scores the whole probability distribution, not just the top answer; lower is better.

On new sources Kev-27B is within a point of Jev (0.848 vs 0.857), and Kev-4B and Kev-9B are within four points. We don't know what Jev was trained on, so this isn't a controlled comparison of the two architectures. [What to Expect](#what-to-expect) says where Kev is as good as Jev and where it isn't.

Kev-0.8B, 4B and 9B start from Qwen base models and share one training recipe. Kev-27B starts from Qwen's post-trained release, and we don't know what that was trained on. Each model card has the full recipe, all results, and the earlier versions kept as Hub tags. The weights are also in the [GitHub release](https://github.com/jaredpalmer/kev/releases/tag/kev-family), with SHA-256 checksums.

## Quick Start

### Try It in the Browser

The [Hugging Face Space](https://huggingface.co/spaces/jaredpalmer/kev) runs Kev-4B and Kev-0.8B, with nothing to install.

### Run It Locally

You'll need Python 3.12 or 3.13 and [uv](https://docs.astral.sh/uv/). The repo's `.python-version` makes `uv sync` use 3.13; torch has no wheels for 3.14 yet.

```bash
git clone https://github.com/jaredpalmer/kev.git && cd kev
uv sync --extra serve
uv run --extra serve python -m kev.serve --run jaredpalmer/kev-4b --port 8009
```

This starts Kev-4B on your machine: CUDA or ROCm if you have a GPU, MLX on Apple Silicon. The first run downloads the adapter and the base model. `--run` also accepts a local checkpoint directory or a Hub revision like `jaredpalmer/kev-4b@qwen3`.

In another terminal, send it a ticket:

```bash
curl -s localhost:8009/v1/systemone -H 'content-type: application/json' -d '{
 "state": "Shoes arrived two weeks late and in the wrong size. Also I see two charges on my card.",
 "model": "kev-latest",
 "questions": {
 "department": {"type": "choice", "instructions": "Which team should handle this?",
 "criteria": {"returns": "Exchanges, refunds, wrong or damaged items",
 "shipping": "Delivery status, delays, lost packages",
 "billing": "Charges, invoices, payment problems"}},
 "escalate": {"type": "noul", "instructions": "Does this need urgent human attention?"},
 "frustration": {"type": "score", "instructions": "How frustrated is the customer?",
 "criteria": ["Calm", "Frustrated", "Very angry"]}
 }}'
```

Example response from Kev-4B, running in bf16 on an Apple M5:

```json
{
 "model": "kev-latest",
 "answers": {
 "department": { "type": "choice", "choice": "returns", "confidence": 0.21,
 "probabilities": { "returns": 0.47, "shipping": 0.28, "billing": 0.25 } },
 "escalate": { "type": "noul", "noul": 0.93 },
 "frustration": { "type": "score", "score": 1.44, "confidence": 0.34,
 "legend": { "0": "Calm", "1": "Frustrated", "2": "Very angry" },
 "probabilities": { "0": 0.00, "1": 0.56, "2": 0.44 } }
 },
 "usage": { "input_tokens": 101, "output_tokens": 161 },
 "latency_ms": 495
}
```

The ticket mentions a return, a late delivery and a billing problem, and the department probabilities say so. That's why Kev returns probabilities instead of a single label: your code can route the confident cases and send the rest to a person.

### Use It From Python
