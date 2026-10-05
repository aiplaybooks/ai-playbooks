# anything2explainer

[](https://claude.com/claude-code)
[](https://openai.com/codex)
[](https://remotion.dev)
[](LICENSE)

**English** | [简体中文](README_ZH.md)

**Topic in, narrated explainer video out.** anything2explainer is a [Claude Code](https://claude.com/claude-code) / [Codex](https://openai.com/codex) skill that turns any topic into a black-canvas motion-graphics explainer video with TTS voiceover, subtitles and a chapter progress bar, in Chinese or English. Every frame is drawn in code with [Remotion](https://remotion.dev) (React + TypeScript). No stock footage, no generative video model, no frames lifted from anyone else's work.

It is not a CLI. What ships here is the whole method an AI coding agent needs to finish the film: a compilable Remotion template, a primitives and lighting library, tooling for voiceover / storyboard / rendering / quantitative QC, written style and motion specs, a multi-agent division-of-labour protocol, and one complete reference film as the quality bar.

**English cut** — *RAG & Knowledge Bases*, 5′02″, 44 lines / 785 words, voiced by kokoro-82m `am_liam` at natural speed:

https://github.com/user-attachments/assets/e2771c68-a28c-4459-ac5a-a5b685181eeb

**Chinese cut** — *RAG 与知识库* v2, 4′54″, 44 lines / 1490 characters, dot-field backdrop (`bg: 'dots'`), voiced through the bring-your-own-TTS path (Volcengine TTS 2.0 + forced alignment):

https://github.com/user-attachments/assets/5c213990-cbba-439e-8371-fbb3aa348e05

Both cuts share one storyboard and 44 shots; the English cut re-times every shot to the English voiceover. The full paper trail of the original Chinese cut (4′35″, star-field backdrop, 8 build agents in parallel for 40 minutes, two QC rounds) lives in [`examples/rag/`](examples/rag/) (research → narration → storyboard → shot source → QC reports → delivery notes); rendered frames are in [`examples/rag/frames/`](examples/rag/frames/).

## What it does

- **Input**: a topic ("explain vector databases"), or an article / document you want turned into a video. You also pick the length and the language.
- **Output**: a 1280×720 H.264 MP4 with synchronized voiceover, word-boundary-aligned subtitles, chapter cards, a top HUD and a bottom chapter progress bar, plus the full paper trail (research doc with sources, narration, storyboard, per-shot source code, QC reports).
- **How**: the agent researches the topic with sources, writes the narration, generates the voiceover and frame-accurate timeline, storyboards every shot, then dispatches parallel build agents that write one Remotion component per shot. QC agents review the rendered frames against written criteria before delivery.
- **Time**: roughly 1 to 3 hours of wall clock depending on length, most of it agents building shots in parallel. You are consulted at exactly four checkpoints.

## Output spec

| | |
|---|---|
| Frame / rate | 1280×720 @ 30fps, H.264 |
| Length | your call (see table below); 2–8 minutes all work |
| Language | Chinese or English (`lang` in `src/config.ts`); typography, subtitle budgets and TTS switch with it |
| Look | black canvas with one of two backdrops, star field + fog gradient or dot-field wave (`bg` in `src/config.ts`; the dot-field wave is ported from video-talkcraft); white line art + purple accents; ultra-bold headline type |
| Persistent layers | 44px white-on-black-stroke subtitles, bottom chapter progress bar, top capsule HUD, optional pipeline rail, `built by Anything2Explainer skill` end credit (`builtBy`, set to `''` to drop) |
| Voiceover | Chinese: edge-tts `zh-CN-YunxiNeural` (Yunxi, male, unmodified rate ≈5.5 chars/s). English: kokoro-82m `am_liam` (Liam, male). Or bring your own TTS / finished audio |

Length drives how much ground the film covers, and the size of the whole pipeline:

| Length | Chinese chars | English words | Lines / shots | Build agents | Wall clock | Disk |
|---|---|---|---|---|---|---|
| 2–3 min | 650–880 | 280–420 | 24–32 | 4–6 | ≈1 h | ≈2 GB |
| 3–5 min (reference tier) | 1100–1400 | 420–700 | 40–50 | 8 | ≈2 h | ≈2 GB |
| 5–8 min | 1650–2200 | 700–1150 | 60–80 | 10–14 | ≈2–3 h | ≈3 GB |

Chapter count follows the content, within limits set by length: under 3 minutes use a single chapter (no chapter cards), 3–5 minutes 3–4 chapters of at least 60 s each, 5–8 minutes 4–6. The progress bar splits evenly across however many chapters the narration declares. A blank line in the narration marks a paragraph, which is also one shot: sentences inside a paragraph are separated by 10 frames, paragraph ends by 30, so the pause lands where the picture changes and every shot holds 1–1.5 s after its last element lands. The finished video runs 5–8% longer than the raw speech by design.

## Install

```bash
git clone https://github.com/Vincentwei1021/anything2explainer.git
ln -s "$PWD/anything2explainer" ~/.claude/skills/anything2explainer # Claude Code
ln -s "$PWD/anything2explainer" ~/.codex/skills/anything2explainer # Codex
```

Dependencies:

```bash
# Node ≥18 (the template's npm install pulls remotion 4.0.507 / react 19)
brew install ffmpeg # frame extraction / transcoding, required

python3 -m venv ~/.venvs/a2e && source ~/.venvs/a2e/bin/activate
pip install 'edge-tts==7.2.8' numpy pillow scipy # pin edge-tts: it tracks a Microsoft endpoint and breaks across upgrades (7.2.0+ needs word boundaries requested explicitly; the script does)

# only needed for English narration (kokoro-82m runs locally)
pip install kokoro soundfile && brew install espeak-ng
```

`scipy` is only used by the QC script `frame_metrics.py`. The shell scripts are zsh + Python 3, developed and verified on macOS; Linux should work, Windows is untested.

### Linux / Raspberry Pi (ARM)

Verified on a Raspberry Pi 5 (ARM64, Python 3.13). Three things differ from macOS:

```bash
sudo apt install zsh espeak-ng # scripts are #!/bin/zsh; espeak-ng for kokoro/piper G2P

# Remotion has no linux-arm64 headless browser → point it at system Chromium:
sudo apt install chromium # or 