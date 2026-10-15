| Windows | macOS | Linux | Community Results | Gallery | Discord | QQ Group | WeChat Group |

 English · 中文 

Make videos on the computer you already own. Powered by [Video DeltaNet (VDN)](https://openvdn.github.io/), FreeVideo runs MiniMax H3 in as little as 8 GB of VRAM and 16 GB of RAM, with acceleration adapted to your&nbsp;hardware.

https://github.com/user-attachments/assets/ecda7d0d-7fbe-4e0c-8c29-8f3315bafc15

 More clips and the four quality levels side by side in the gallery → 

## News

- **2026-10-13** · **[v0.4.0](https://github.com/FlashML-org/FreeVideo/releases/tag/v0.4.0): AI agents, minute-long videos and an editing view.** Let an AI agent such as Claude Code or Codex make videos on its own, generate videos over a minute long, and edit them on a timeline.
- **2026-10-07** · **[v0.3.2](https://github.com/FlashML-org/FreeVideo/releases/tag/v0.3.2): preview first.** See a half-resolution preview first and finish only the videos you like.
- **2026-10-07** · **[v0.3.0](https://github.com/FlashML-org/FreeVideo/releases/tag/v0.3.0): a faster int8 model.** GeForce and RTX 30-series cards switch to int8; an RTX 3090 makes a 5-second video about 2.3x faster.
- **2026-10-06** · **[Gallery](https://freevideo-community.pages.dev/#gallery) is live.** Watch 20-second clips made with FreeVideo, and the four quality levels side by side.
- **2026-10-06** · **[v0.2.3](https://github.com/FlashML-org/FreeVideo/releases/tag/v0.2.3): videos carry their workflow.** Drop a FreeVideo video onto the ComfyUI canvas to restore its prompt, seed and settings. Earlier videos can get theirs too.
- **2026-10-05** · **[v0.2.0](https://github.com/FlashML-org/FreeVideo/releases/tag/v0.2.0): four quality levels.** Choose Light, Medium, High or Max for each video; higher levels give higher quality but take longer. Results can be exported as sharing images or videos with the generation time and GPU.
- **2026-10-05** · **[v0.1.2](https://github.com/FlashML-org/FreeVideo/releases/tag/v0.1.2): FreeVideo on Mac.** Apple silicon Macs generate MiniMax H3 videos locally (preview).
- **2026-10-03** · **Community LoRAs.** Use MiniMax H3 LoRAs right in your workflow. See [examples](docs/LoRA.md).
- **2026-10-02** · **FreeVideo is open source.** MiniMax H3 on consumer GPUs with as little as 8 GB of VRAM.

## About

FreeVideo is a local inference engine for MiniMax H3 on consumer GPUs, built on [OpenVDN](https://github.com/OpenVDN)'s 8-step [VDN-H3](https://huggingface.co/OpenVDN/vdn-minimax-h3) model with [Video DeltaNet](https://openvdn.github.io/)'s hybrid attention.

It coordinates VRAM, system memory and disk, adapting weight placement, compute precision and attention kernels to the available hardware. FreeVideo runs as a ComfyUI plugin, with launchers for Windows, macOS and Linux. Its core features include:

- **Hardware-adaptive execution**: Chooses the weight format for each GPU, int8 on GeForce and RTX 30-series cards and FP8 on workstation and datacenter cards, and automatically probes the available attention kernels.
- **Low-memory inference**: Weight streaming, asynchronous prefetching and chunked computation keep peak memory low, enabling inference with as little as 8 GB of VRAM and 16 GB of RAM.
- **Multimodal inputs**: Text prompts, first and last frames, and image, video and audio references.
- **Community LoRAs**: Use MiniMax H3 LoRAs in your workflow. See [examples](docs/LoRA.md).
- **ComfyUI integration**: A dedicated creative workspace inside ComfyUI that supports two-pass sampling and batch generation and keeps a history of past creations. For finer control, switch to the node view to add LoRAs or customize the workflow.
- **One-click deployment**: The Windows, Mac and Linux launchers set up ComfyUI, the runtime environment and the models, reuse existing models, and support offline installation.

## Getting Started

### Windows

1. [Download FreeVideo.exe](https://github.com/FlashML-org/FreeVideo/releases/latest/download/FreeVideo.exe) and run it.
2. Select an existing ComfyUI folder or install a new one. Existing model folders can be added for reuse; missing models are downloaded automatically.
3. Click **Install & launch**. ComfyUI opens in the browser with the FreeVideo workspace.

**Offline installation:** Download the packages from [Quark](https://pan.quark.cn/s/c51235b84618) and drag the ZIP files into the launcher without extracting them. A fully offline installation needs the four model packs (video model, text encoder, video & audio decoder, and sampling caches), plus the environment package for a new ComfyUI installation. After importing only the environment package, you can also choose **Automatic download** for the models (v0.3.12 or newer). The audio reference cache is optional and is used only when a reference includes audio.

### macOS (Apple silicon preview)

1. [Download FreeVideo-Mac-arm64.dmg](https://github.com/FlashML-org/FreeVideo/releases/latest/download/FreeVideo-Mac-arm64.dmg), open it and drag **FreeVideo.app** into **Applications**.
2. Open FreeVideo, then select an existing ComfyUI folder or install a new one. Existing model folders can be added for reuse; the runtime environment and missing models are downloaded automatically.
3. Click **Install & launch**. ComfyUI opens in the browser with the FreeVideo workspace.

This preview has been tested on an M5 Mac with 24 GB of unified memory. See the [Mac&nbsp;guide](docs/Mac.md) for generation times and memory.

The Mac preview isn't notarized by Apple yet, so macOS blocks it the first time you open it. Download it only from the Releases page, then check the file and approve it as described in the [Mac guide](docs/Mac.md#first-open). This approves FreeVideo only; your other security settings stay as they are.

### Existing ComfyUI

Install FreeVideo as a custom node:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/FlashML-org/FreeVideo.git
```

Restart ComfyUI, open **Workflow → Browse Templates → FreeVideo → Fre