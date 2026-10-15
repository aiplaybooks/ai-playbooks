# Lemo-Opuscar

**English** · [简体中文](README.zh-CN.md)

**43 film styles, each with a short film made entirely in code.** 
**43 种影片风格，每种都配一支完全用代码做出来的短片。**

Pick a style, bring your own story, and let your coding agent direct the film. 
选一个风格，带上你自己的故事，让你的编程 agent 来当导演。

**🇨🇳 中文用户请看这里 → [简体中文说明 README.zh-CN.md](README.zh-CN.md)**

[**▶ Watch the gallery**](https://lemomo-ai.github.io/lemo-opuscar/)

 Official repo: [github.com/lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) · by Lemomo ([@lemomo_ai](https://x.com/lemomo_ai)) 

**New: [all 98 styles of OPUSCAR 98](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/#styles)**: for every film, its style (2D or 3D), a frame, a style prompt you can reuse, and how its shots were directed.

## 🎬 Feature presentation: OPUSCAR 98

**98 Years of Best Picture · 1927 – 2025 · 6:31**

One Clawd walks through all 98 Best Picture winners, each one redrawn in a style that fits the film. 
Every frame, every note and every cut was written in code by Claude Opus 5.5.

All 98 styles are now public: each film's style and 2D/3D tag, a frame, a style prompt to reuse on your own topic, and the shots and direction (77 in 2D, 4 in 2.5D, 17 in 3D). The same list is on the film page and as [JSON](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/styles.json).

[**▶ Watch**](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/) · [**All 98 styles**](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/#styles) · [**Download 1080p**](https://github.com/lemomo-ai/lemo-opuscar/releases/download/films/opuscar98.mp4)

## 👋 About me

I'm **Lemomo** ([@lemomo-ai](https://github.com/lemomo-ai)). More about me on my profile.

> **Not an awesome list.** Every film here was made by me, with Claude Opus 5.5. The styles are tuned for Opus 5.5; other models may not reproduce them.

Every film was directed, drawn, scored and mixed by an AI agent writing code: canvas and WebGL pages rendered frame by frame, original music from free sample libraries, text-to-speech narration. No video generation, no stock footage.

## How to use

Two ways in; the skill is the easiest.

### Option 1: install the skill (recommended)

In your terminal:

```sh
claude plugin marketplace add lemomo-ai/lemo-opuscar
claude plugin install lemo-opuscar@lemolab
```

Then use it from any folder. On first use it downloads the guides, tools and style prompts to `~/lemo-opuscar`, shared by all your films. Each film's project, from source to finished video, goes in the folder you started from. For other agents, copy [`plugin/skills/lemo-opuscar/`](plugin/skills/lemo-opuscar/) into their skills folder.

### Option 2: clone the repo

```sh
git clone https://github.com/lemomo-ai/lemo-opuscar.git
cd lemo-opuscar
claude
```

Films go into `films/ /` inside the repo.

### Then just say what you want

> Make a 45-second film in the **watercolor** style about the coffee farm my family runs. Warm female narrator.

Name the style in English or Chinese; the [style index](styles/README.md) lists them all.

It asks you once, up front: anything it can't decide about your topic, whether you have your own **voice, music or other material**, and whether you want to see a **storyboard** first. Say yes and it stops once to show you the key shots in the real style; otherwise it goes straight to the finished film.

The agent reads three guides and works like a small studio:

| File | What it gives the agent |
|---|---|
| [`DIRECTOR.md`](DIRECTOR.md) | how to direct: story, sound, rhythm, camera, performance, self-checks |
| [`TECHNIQUE.md`](TECHNIQUE.md) | how to build: frame-by-frame rendering, voice, music, mixing |
| `styles/ /STYLE.md` | what the style looks and sounds like; the story is yours |

### Before you start

- A film takes an agent about 30–60 minutes and a fair amount of tokens.
- You need Node 20+, ffmpeg and Python 3.11+ (or [uv](https://docs.astral.sh/uv/)); the agent installs the rest.
- Default output 1920×1080, 24 fps; other sizes on request.

Update: `claude plugin marketplace update lemolab && claude plugin update lemo-opuscar@lemolab`, then restart Claude Code (the library in `~/lemo-opuscar` updates itself on the next film); uninstall with `claude plugin uninstall lemo-opuscar@lemolab` and delete `~/lemo-opuscar`. If a step stays stuck, [open an issue](https://github.com/lemomo-ai/lemo-opuscar/issues).

## The styles

Click a frame for its `STYLE.md`.

### Hand-drawn & Painting

 Crayon Picture Book The Moon Can&#x27;t Sleep The moon can&#x27;t sleep, so a little girl climbs onto the roof to sing it a lullaby. 
 Watercolor Brush Follow the Rain Follow the rain from Australia&#x27;s red desert heart to its green coast in one unbroken painted walk. 
 Chinese Ink Wash The Swordsman and the River A swordsman crosses the river on the water and splits the current with a single stroke. 

 Impasto Oil Painting The Colour of Rain In a grey, rainy square one red umbrella opens, and a waltz paints the whole plaza in colour. 
 One-line Drawing The Line That Never Lifted One unbroken line draws a whole life, then the pen passes to a child. 
 Whiteboard Explainer Einstein in Your Pocket How your phone knows where you are: GPS, atomic clocks, and the 38 microseconds relativity adds every day. 

 Urban Sketch · Pen &amp; Wash Where the Wind Went A park that is only a pen sketch; wherever the wind carries her straw hat, colour follows. 

### East Asian Traditions

 Shadow Puppetry Hou Yi Shoots the Suns Ten suns scorch the earth until the archer Hou Yi draws his bow, told with leather puppets on a lit screen. 
 Ukiyo-e A Journey Toward the Mountain A traveller walks toward a distant mountain; every shot is a woodblock print, ending in a great wave. 
 Red Paper-cut Nian Comes to Town On New Year&#x27;s Eve the beast Nian comes to town, and one girl&#x27;s giant paper-cut lights up the village to scare it off. 

 Paper-cut Lightbox A Mooncake&#x27;s Longing A single mooncake tells the Mid-Autumn story of reunion and