Unsloth is the first desktop app to run and train models.

 Features •
 Quickstart •
 Notebooks •
 Documentation 

## ⚡ Get started
Download the native Unsloth Desktop app for your operating system:

 Platform 
 Link 

 Windows 
 Download 

 macOS 
 Download 

 Linux / Ubuntu (deb) 
 Download 

 Linux / Ubuntu (ARM64) (deb) 
 Download 

 Linux (AppImage) 
 Download 

 Windows (ARM64) 
 Download 

Download from [Unsloth](https://unsloth.ai/download) or [GitHub Releases](https://github.com/unslothai/unsloth/releases).

Or if you prefer to install manually:

#### macOS, Linux, WSL:
```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

#### Windows:
```powershell
irm https://unsloth.ai/install.ps1 | iex
```
#### Docker:

The [Unsloth Docker image](https://hub.docker.com/r/unsloth/unsloth) `unsloth/unsloth` is available on Docker. [Read guide.](https://unsloth.ai/docs/get-started/install/docker)

#### Homebrew:
```bash
brew install --cask unsloth
```

#### Winget (Windows):
```powershell
winget install --id UnslothAI.Unsloth -e
```

#### Community:

- [Discord](https://discord.gg/unsloth)
- [𝕏 (Twitter)](https://x.com/UnslothAI)
- [Reddit](https://reddit.com/r/unsloth)

## ⭐ Features
Unsloth works on **Windows, Linux, WSL** and **macOS**. We support **Multi GPU setups, NVIDIA, AMD, Intel GPUs, CPUs** and the **Vulkan** backend.

### Run & Build with AI
* Run and train LLMs, MLX, GGUF, diffusion, decision, embedding, audio models: [Qwen3.8](https://unsloth.ai/docs/models/qwen3.8), [GLM-5.3-Flash](https://unsloth.ai/docs/models/glm-5.3-flash), [Kimi K3](https://unsloth.ai/docs/models/kimi-k3), [Qwen-Image-2.1](https://unsloth.ai/docs/models/qwen-image-2.1), MiniMax-H3, [DeepSeek-V4](https://unsloth.ai/docs/models/deepseek-v4), [Gemma 4](https://unsloth.ai/docs/models/gemma-4).
* **Agents & Tools:** Use local models with [Claude Code](https://unsloth.ai/docs/basics/claude-code), [Codex](https://unsloth.ai/docs/basics/codex), and [MCP](https://unsloth.ai/docs/basics/mcp), including tool calling and code execution.
* **Search & RAG:** Use private and unlimited web search, deep research, auto-compaction (rolling context window) and RAG.
* **Image and video:** Run and train [image](https://unsloth.ai/docs/basics/diffusion-image) and video diffusion or multimodal models
* **Remote & LAN:** Access your local models from any device on [LAN](https://unsloth.ai/docs/basics/lan) or remotely through secure [Cloudflare](https://unsloth.ai/docs/basics/how-to-serve-local-llms-anywhere-secure-remote-access-with-cloudflare-and-unsloth) HTTPS.
* **Connect:** Serve models through an [OpenAI compatible API](https://unsloth.ai/docs/basics/api). Also connect your ChatGPT/Codex subscription and [cloud providers](https://unsloth.ai/docs/integrations/connections)

### Train & Deploy
* **Fine-tuning:** Train LLMs, diffusion, decision, TTS, and embedding models 2× faster with 70% less VRAM with [no accuracy loss](https://unsloth.ai/blog#training)
* **Complete support:** Supports [reinforcement learning](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide), LoRA, QLoRA, full fine tuning, pretraining, RL, GRPO, DPO, and FP8.
* **Export & Deploy:** [Export](https://unsloth.ai/docs/new/studio/export) or Deploy models including [GGUF](https://unsloth.ai/docs/basics/inference-and-deployment/saving-to-gguf), NVFP4, FP8 and more formats.
* **Datasets:** Build datasets from PDFs, CSVs, DOCX files, and more with [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe).

## 🚀 Unsloth Start

[Unsloth Start](https://unsloth.ai/docs/integrations/unsloth-start) connects [Claude Code](https://unsloth.ai/docs/basics/claude-code), [Codex](https://unsloth.ai/docs/basics/codex) and other agents to local models with one command.

```bash
unsloth start claude --model unsloth/Qwen3.8-27B-GGUF:UD-Q4_K_XL
```

| Agent | Command |
| --- | --- |
| Claude Code | `unsloth start claude` |
| OpenAI Codex | `unsloth start codex` |
| Visual Studio Code | `unsloth start vscode` |
| DeepSeek Harness | `unsloth start dsh` |
| OpenCode | `unsloth start opencode` |
| Hermes Agent | `unsloth start hermes` |
| Pi | `unsloth start pi` |
| OpenClaw | `unsloth start openclaw` |

## 📥 Install
Unsloth can be used in three ways: **[Unsloth Desktop](https://unsloth.ai/download)**, the desktop app; **[Unsloth Studio](https://unsloth.ai/docs/new/studio/)**, the web UI; or **Unsloth Core**, the code based version.

### Unsloth Desktop (recommended)

 Platform 
 Link 

 Windows 
 Download 

 macOS 
 Download 

 Linux / Ubuntu (deb) 
 Download 

 Linux / Ubuntu (ARM64) (deb) 
 Download 

 Linux (AppImage) 
 Download 

 Windows (ARM64) 
 Download 

### Unsloth Studio (web UI)

#### macOS, Linux, WSL:
```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

#### Windows:
```powershell
irm https://unsloth.ai/install.ps1 | iex
```

#### Homebrew:
```bash
brew install --cask unsloth
```

#### Docker
Use our [Docker image](https://hub.docker.com/r/unsloth/unsloth) ```unsloth/unsloth```. On Linux and Mac, set up GPU access once with
```bash
curl -fsSL https://raw.githubusercontent.com/unslothai/unsloth/main/docker/install_nvidia_toolkit.sh -o install_nvidia_toolkit.sh && sudo -E bash install_nvidia_toolkit.sh
```
For Windows instructions and more information, read our [Unsloth Docker Guide](https://unsloth.ai/docs/get-started/install/docker).

**Linux / WSL (Bash):**
```bash
# for a public Cloudflare HTTPS link: use -e UNSLOTH_STUDIO_SECURE=1 instead of -p 8000:8000, and -p 127.0.0.1:8888:8888 instead of -p 8888:8888
docker run -d --name unsloth --gpus all --ipc=host \
 -p 8000:8000 -p 8888:8888 \
 -v "$PWD":/workspace/host \
 -v unsloth-workspace:/workspace \
 -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
 -v unsloth-studio:/opt/unsloth-studio \
 unsloth/unsloth && docker logs -f unsloth
```
See [Docker docs](https://unsloth.ai/docs/get-started/install/docker) for more information. For notebooks only, use the `unsloth/unsloth:core` t