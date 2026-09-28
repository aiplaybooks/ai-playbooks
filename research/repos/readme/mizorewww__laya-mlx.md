# Laya-MLX

**Open-weight typed decisions, running natively on Apple Silicon.**

**13.4 ms** median end-to-end for a short English typed decision. **7.4 ms** with the multilingual checkpoint. **0 output tokens.** Local MLX inference, with no PyTorch, Transformers runtime, or cloud API.

[中文](https://github.com/mizorewww/laya-mlx/blob/main/README.zh-CN.md) · [Benchmarks](https://github.com/mizorewww/laya-mlx/blob/main/BENCHMARKS.md) · [Snake demo](https://github.com/mizorewww/laya-mlx/blob/main/docs/SNAKE_DEMO.md) · [Hugging Face weights](https://huggingface.co/aac6fef/laya-mlx)

The GIF is an original-speed render of a real local Snake run. Every move calls Laya; the visible cycle safety layer can correct unsafe proposals. The latency figures above are the separate **one-question API benchmark**, not the frame time of the three-question Snake loop. [Watch the 30-second MP4](https://github.com/mizorewww/laya-mlx/blob/main/docs/assets/snake-demo.mp4) · [Snake speed and stability](https://github.com/mizorewww/laya-mlx/blob/main/docs/SNAKE_BENCHMARKS.md).

## Quick start

```bash
pip install laya-mlx
```

```python
import laya_mlx as laya

agent = laya.load("aac6fef/laya-mlx")
result = agent.predict(
 "I was billed twice. Please refund the duplicate.",
 {
 "department": {
 "type": "choice",
 "instructions": "Who should handle this?",
 "criteria": ["billing", "technical", "sales"],
 }
 },
)
print(result["answers"]["department"])
```

Apple Silicon, Python 3.11+, macOS 14+. First load downloads the checkpoint; later inference is fully local. The measured environment is macOS 27.2, Python 3.12.13 and MLX 0.32.2. That MLX release supplies macOS 14, 15 and 26 wheels; the local installer selected the 26 wheel. Older supported macOS versions were not tested on this machine.

Run the terminal demo:

```bash
pip install 'laya-mlx[demo]'
hf download aac6fef/laya-multilingual-mlx
laya-snake
```

Download once before the offline demo. Use a terminal at least 104 × 35 cells. Space pauses, ↑/↓ changes speed, R resets and Q quits. `laya-snake --max-speed` makes a fresh decision for every move without pacing. [Recording, controls and exact metric meanings](https://github.com/mizorewww/laya-mlx/blob/main/docs/SNAKE_DEMO.md).

`laya-snake --optimize --max-speed` enables the tested compilation and prefix-reuse path: **75.40 moves/s across 2,400 moves**, zero deaths and 2 visible safety interventions in the paired M3 Max test. This was about **6.5% faster** than its same-run eager control. [Gameplay, performance and correctness evidence](https://github.com/mizorewww/laya-mlx/blob/main/docs/SNAKE_OPTIMIZATION.md).

## Performance on M3 Max

| FP16, end-to-end | Laya 421M | Multilingual 322M |
|---|---:|---:|
| One short question, P50 | **13.42 ms** | **7.39 ms** |
| One short question, P95 | **13.92 ms** | **7.79 ms** |
| 50-question throughput | **146.8 q/s** | **395.0 q/s** |
| Peak MLX allocation, one short question | **943.6 MiB** | **687.6 MiB** |

M3 Max, 40 GPU cores, 128 GiB memory. Timing includes prompt preparation, tokenization, tensors, synchronized inference, calibration and result formatting; model loading is excluded. The 50-question measurement uses `batch_size=64`; the API defaults to 16. Different lengths, question counts and runtime conditions change latency. [Full method and every timing sample](https://github.com/mizorewww/laya-mlx/blob/main/BENCHMARKS.md).

**Port fidelity:** all three checkpoints matched the upstream selected answer on **63/63 validation questions in both FP32 and FP16** — 378/378 comparisons. Each configuration also passed 100 repeated finite, deterministic calls with zero measured active-memory growth. This measures fidelity on those fixtures, not accuracy on every possible question. [Probability errors and validation](https://github.com/mizorewww/laya-mlx/blob/main/BENCHMARKS.md#numerical-parity-and-stability).

## Why typed decisions?

Software often needs a choice, a rubric score or a probability. Laya answers those constrained questions in a bidirectional forward pass, without token-by-token decoding or generated JSON.

```text
state + typed question → bidirectional encoder → decision heads → probabilities
```

- `choice`: probabilities over named options.
- `score`: probabilities over ordered rubric levels and their expected score.
- `noul`: P(true) for a proposition.

Question rows are batched independently. Their bidirectional encoder representations depend on both state and question; this runtime does not claim to encode the state once and reuse its hidden states across arbitrary questions.

The encoder, decision Transformer, scoring head and action head all run in MLX. Tokenization uses Hugging Face's Rust tokenizer. The original pretrained weights, question formatting, calibration and output schema are retained. This is an independent MLX port, not an official Convai Innovations release.

## Supported checkpoints

| Model | Encoder | Parameters | Context limit | Purpose |
|---|---|---:|---:|---|
| `convaiinnovations/laya` | ModernBERT-large | 421M | 512 | English |
| `convaiinnovations/laya-multilingual` | mmBERT-base | 322M | 1,024 | Multilingual input |
| `convaiinnovations/laya-typed-decisions` | ModernBERT-large | 421M | 1,024 | Upstream typed-decisions workflows |

Context includes instructions, options and state. All three use the original weights, prompt formatting, temperature calibration, and output schema. This repository provides inference and conversion; RLCD training and fine-tuning remain in the upstream project. It is an independent port, not an official Convai Innovations release.

Pre-converted FP16 checkpoints are published on Hugging Face:

- [aac6fef/laya-mlx](https://huggingface.co/aac6fef/laya-mlx)
- [aac6fef/laya-multilingual-mlx](https://huggingface.co/aac6fef/laya-multilingual-mlx)
- [aac6fef/laya-typed-decisions-mlx](https://huggingface.co/aac6fef/laya-typed-decisions-mlx)

Load these directly with `laya.load("aac6fef/laya-mlx")`, or u