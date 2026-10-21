# edge0

**An open-source streaming MoE inference framework — SSD expert offload + Recover-LoRA + prerouter routing prediction.**

**Python** · **macOS** · **iOS** · **Android** — one recipe, every device.

[](https://huggingface.co/Edge0/Edge0-35B-A3B-preview)
[](https://huggingface.co/Edge0/Edge0-8B-A1B-preview)
[](https://www.modelscope.cn/models/Edge0/Edge0-35B-A3B-preview)
[](https://www.modelscope.cn/models/Edge0/Edge0-8B-A1B-preview)
[](https://arxiv.org/abs/2609.18063)
[](https://github.com/Edge0-AI/Edge0)
[](https://edge0.ai/discord)
[](LICENSE)

English | [中文](README_zh.md) | [日本語](README_ja.md) | [Español](README_es.md) | [Français](README_fr.md)

## News

- **[2026-09-30]** We released the **edge0 inference engines for four platforms — iOS, macOS, Android and Windows** — so users get the best inference experience across architectures and platforms. The source is open-sourced in this repo ([`ios/`](ios/) · [`macos/`](macos/) · [`android/`](android/) · [`windows/`](windows/)) — see each directory's README for details. The **unified inference framework** follows in **Q4 2026**; see the [Roadmap](#roadmap).
- **[2026-09-16]** Our technical report is on arXiv: [The Other Half of the Memory Wall: Serving 35B MoEs from SSD with Trained Routing Prediction](https://arxiv.org/abs/2609.18063).
- **[2026-09-08]** Initial open-source release of **edge0**, together with both model tiers — [`Edge0-35B-A3B-preview`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview) and [`Edge0-8B-A1B-preview`](https://huggingface.co/Edge0/Edge0-8B-A1B-preview) — on Hugging Face and ModelScope.

## About

**edge0** is an open-source streaming MoE inference framework. It
generalizes the production-proven recipe — **SSD expert offload +
Recover-LoRA + prerouter routing prediction** — into an extensible
framework that runs large sparse-MoE models on consumer hardware: peak
memory is bounded by the *active* expert set, not the parameter count.

### Core mechanisms

- **SSD expert offload**: expert weights are streamed from storage on
 demand; peak memory is bounded by the active set, not the parameter
 count.
- **Prerouter**: a trained head predicts expert routing one step
 ahead, so expert loads overlap the forward pass instead of stalling
 it — **up to +59%** decode throughput; the gain grows with storage
 latency, model size, and routed width *K*.
- **Recover-LoRA**: the int4 base is frozen and LoRA adapters are
 trained by distillation from the FP teacher, recovering most of the
 quantization loss at 4-bit (see [Quality](#quality)). Adapters stay
 unmerged: one read-only base serves multiple adapter sets.

### Platforms

One repo, one recipe, per-platform runtimes:

| Platform | Directory | Stack | Status |
|---|---|---|---|
| **Python** (macOS · Apple Silicon) | [`python/`](python/README.md) | Python + MLX | ✅ Available now |
| **macOS** app & CLI | [`macos/`](macos/README.md) | Rust | ✅ Open-sourced (2026-09-30) |
| **iOS** app | [`ios/`](ios/README.md) | Swift + MLX Swift | ✅ Open-sourced (2026-09-30) |
| **Android** app & engine | [`android/`](android/README.md) | Kotlin + native engine | ✅ Open-sourced (2026-09-30) |
| **Windows** app & engine | [`windows/`](windows/README.md) | C++ + Vulkan | ✅ Open-sourced (2026-09-30) |

### Models

Two model tiers ship with the framework. Each tier is an end-to-end
release: the released checkpoint, the trained LoRA adapters, and the
trained prerouter heads work together as one unit.

| Tier | Released checkpoint | Inference profile |
|---|---|---|
| `edge0-35b` | [`Edge0/Edge0-35B-A3B-preview`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview) · [ModelScope](https://www.modelscope.cn/models/Edge0/Edge0-35B-A3B-preview) | 4-bit, 40 layers, 256 experts, prerouter K=4 |
| `edge0-8b` | [`Edge0/Edge0-8B-A1B-preview`](https://huggingface.co/Edge0/Edge0-8B-A1B-preview) · [ModelScope](https://www.modelscope.cn/models/Edge0/Edge0-8B-A1B-preview) | 4-bit, 24 layers, 128 experts, prerouter K=8 |

Both checkpoints are built on open sparse-MoE base models (Qwen3.6-35B-A3B
and the Ling 3.0 bailing hybrid respectively) and ship with the
LoRA and prerouter training done for this framework — the adapter files
are co-located with each checkpoint and load automatically, so
`edge0 serve ` runs the trained pipeline out of the box.

### Design

- **transformers-style usage**: `AutoModel` / `AutoConfig` / `AutoEngine`
 resolve the tier from the model name;
- **Backend isolation (Python framework)**: within the Python framework,
 all MLX code lives under `python/src/edge0/backends/mlx/`; the core
 logic (model specs, prerouter, streaming expert pool, server) depends
 only on the backend facade (`backends/base.py`), so a new backend
 implements the same facade (`backends/cuda/` is a reserved slot) with
 zero changes to core code. The iOS / macOS / Android engines ship
 platform-native stacks today — bringing every platform under one
 access layer is exactly what the unified inference framework
 (see [Roadmap](#roadmap)) will deliver;
- **Adapters as safetensors**: LoRA and prerouter weights are
 `.safetensors` files with provenance metadata (source, version, owner
 layers), resolved from the model directory or `artifacts/`;
- **Model + adapters in one directory**: a model directory holds both
 the base checkpoint (`config.json` / `model*.safetensors` / tokenizer)
 and that model's adapters; upgrading adapters swaps adapter
 files only — the base stays read-only and is never merged.

### Quality

All benchmarks were run by us with [OpenCompass](https://github.com/open-compass/opencompass)
under identical settings and parameters for both the edge0 models (int4 +
trained adapters + prerouter routing) and the original fp16 base models.
The loss of the edge0 pipeline is small: **3.9 points on average for
edge0-35b, 2.8 for edge0-8b** (MMLU-Pro is even above the base). Max 100:

| Benchmark | edge0-35b (int4) | Qwen3.6-35B-A3B (fp16) | edge0-8b (int4) | Ling 3.0 tiny (fp16) |
|---|---:|---:|--