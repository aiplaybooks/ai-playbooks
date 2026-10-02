# Kev

Small Jev-like decision models you can train and run yourself.

Kev is a family of small decision models built on Qwen3.5 and Qwen3.8 and based on the architecture described in [Jev's Architecture Unmasked](https://archerhume.com/posts/jevs-architecture-unmasked). You can use the pretrained weights or train your own. The API matches TypeSafe's [System One](https://docs.typesafe.ai/api), so you can point their Python SDK at your local server.

## Highlights

- Yes/no (`noul`), multiple-choice (`choice`) and rating (`score`) questions in one request. The questions share the text but can't read each other.
- Calibrated probabilities by default: each checkpoint ships with a fitted temperature.
- Drop-in for Jev: the TypeSafe Python SDK works against a Kev server unchanged.
- Four sizes, versioned together as Kev 1.0: from a 0.8B that runs on a laptop to a 27B for a single data-centre GPU.
- Documents of up to 65,536 tokens, on CUDA and on Apple Silicon through MLX. Each model card says how long a document can get before accuracy drops.
- Fine-tune on your own labelled examples. A coding-agent skill runs the whole loop on Modal, from finding your questions to serving the result.
- Deploy your own HTTPS endpoint with one command. It scales to zero when idle.
- Try it in the browser first: [huggingface.co/spaces/jaredpalmer/kev](https://huggingface.co/spaces/jaredpalmer/kev).

## Models

Start with Kev-4B. Move to Kev-9B if you have a bigger GPU, or to Kev-27B if you have an 80 GB GPU and want the most accurate Kev. Use Kev-0.8B when size matters more than accuracy.

| Model | Base (license) | Runs on: CUDA | Runs on: Mac (MLX) | Validated context | Held-out datasets: index | Card |
|---|---|---|---|---|---|---|
| [Kev-0.8B](https://huggingface.co/jaredpalmer/kev-0.8b) | Qwen3.5-0.8B-Base (Apache-2.0) | L4, any 4 GB GPU | Any Apple Silicon Mac; measured to 65k tokens | 8,192 | 23.3 | [Details](docs/model-cards/kev-0.8b.md) |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | Qwen3.5-4B-Base (Apache-2.0) | L40S, H100 | 32 GB Mac; measured to 65k tokens | 8,192 | 38.0 | [Details](docs/model-cards/kev-4b.md) |
| [Kev-9B](https://huggingface.co/jaredpalmer/kev-9b) | Qwen3.5-9B-Base (Apache-2.0) | L40S, H100 | 32 GB Mac or larger (expected, not measured) | 8,192 | 41.0 | [Details](docs/model-cards/kev-9b.md) |
| [Kev-27B](https://huggingface.co/jaredpalmer/kev-27b) | Qwen3.8-27B, post-trained (Apache-2.0) | B200, H200, H100 80 GB | 96–128 GB Mac (expected, not measured) | 65,536 | **52.3** | [Details](docs/model-cards/kev-27b.md) |
| Jev | Hosted | TypeSafe's API | – | – | 54.0 | – |

"Held-out datasets" is the chance-corrected index of the community Decision Index, scored on the test split of `breadth-v1`: 14 public datasets in five areas that no Kev trained on. "Validated context" is the longest document, in tokens, for which accuracy on real contracts (CUAD) stays within 3 points of the same model's accuracy at 8k tokens, at the 95 % lower bound; each model card has the measurement by length.

| Model | Accuracy: New Sources | Accuracy: Trained Sources | Brier: New Sources |
|---|---|---|---|
| Kev-0.8B | 0.648 / 0.697 | 0.827 / 0.838 | 0.481 / 0.416 |
| Kev-4B | 0.817 / 0.838 | 0.873 / 0.865 | 0.269 / 0.242 |
| Kev-9B | 0.820 / 0.852 | 0.874 / 0.873 | 0.289 / 0.217 |
| Kev-27B | **0.851 / 0.889** | 0.865 / 0.866 | **0.225 / 0.156** |
| Jev | 0.857 / – | 0.845 / – | 0.211 / – |

Each cell is **development / test**. "New sources" means datasets and policy rules Kev never saw during training. It is the closest thing here to your own questions. "Trained sources" means held-out examples from the datasets Kev was trained on. We pick checkpoints using the development sets and read each test set only once per released model. Jev has only been run on the development sets of these two suites. Brier scores the whole probability distribution, not just the top answer; lower is better.

On new sources Kev-27B is within a point of Jev (0.851 vs 0.857), and Kev-4B and Kev-9B are within four points. We don't know what Jev was trained on, so this isn't a controlled comparison of the two architectures. [What to Expect](#what-to-expect) says where Kev is as good as Jev and where it isn't.

Kev-0.8B, 4B and 9B start from Qwen base models and share one training recipe: a small adapter on a frozen base. Kev-27B starts from Qwen's post-trained release, and we don't know what that was trained on; every one of its weights is fine-tuned, so it ships as 51 GB of full weights rather than an adapter. Each model card has the full recipe, all results, and the earlier versions kept as Hub tags.

## Kev 1.0

The four models above are released together as Kev 1.0. Each Hub repo has a `v1.0` tag, so `--run jaredpalmer/kev-4b@v1.0` always loads the same weights, and the GitHub release [`kev-1.0`](https://github.com/jaredpalmer/kev/releases/tag/kev-1.0) has the 0.8B, 4B and 9B checkpoints with SHA-256 checksums. Kev-27B's 51 GB of weights are too large for a release asset and are on the Hub only.

| Model | Hub revision of the weights | Temperature | Trained on states up to |
|---|---|---|---|
| Kev-0.8B | `9a45d25e` | 2.35 | 7,552 tokens |
| Kev-4B | `139fdd94` | 2.41 | 7,552 tokens |
| Kev-9B | `b5d8c18e` (v2) | 2.19 | 7,552 tokens |
| Kev-27B | `28be62e9` (v2, full weights) | 1.32 | 32,768 tokens |

Kev 1.0 trains nothing new. It fixes the checkpoints, cards, evaluation suites and serving code that the next generation of Kev will be compared against. The [release notes](docs/releases/kev-1.0.md) list what changed since the previous family release and what is known not to work well.

## Quick Start

### Try It in the Browser

The [Hugging Face Space](https://huggingface.co/spaces/jaredpalmer/kev) runs Kev-4B and Kev-0.8B, with nothing to install.

### Run It Locally

You'll need Python 3.12 or 3.13 and [uv](https://docs.astral.sh/uv/). The repo's `.python-version` makes `uv sync` use 3.13; torch has no wheels for 3.14 