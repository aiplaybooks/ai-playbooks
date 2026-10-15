Clone any viral video with AI agents 
 1 command, 100 variants, 100M views. 

 Demo 
 &nbsp;&bull;&nbsp;
 Quickstart 
 &nbsp;&bull;&nbsp;
 Develop 
 &nbsp;&bull;&nbsp;
 简体中文 

 ⭐ Help more people find Hypit and grow the community. Star this repo! 

## Hypit

Hypit gives AI agents (Claude Code, Codex...) a language and system to create video. Drop in a video, and your agent clones it as a complete workflow: footage, captions, B-roll and effects, all anchored to words instead of seconds.

**To be clear:** cloning a video is the fastest way in, not the only one. You can start from our templates, or just describe the video you want and your agent writes the workflow from scratch. Generation models are optional too: a workflow can compile captions, motion graphics and code-rendered visuals into a finished video without calling a generation model or incurring its service charges.

 SVML source on the left, with the corresponding video rendered live on the right. 

## Install once

```bash
npx skills add hypit-ai/hypit -g
```

This installs the Skill. On first use, your agent checks for the Hypit executable and helps prepare
it if needed. Your video project can live anywhere.

Hypit is free to use; your Coding Agent and model services have their own accounts and charges.
HypiHub is our recommended hosted model service. You can also use your own API or local models;
tell your agent the service name and API documentation so it can set up the appropriate connection.

[Agent environments and entry partners](./docs/guide/agents.md) ·
[Model and deployment services](./docs/guide/service-partners.md)

## Examples

### UGC

[Generation source](examples/ranking-football/reference.svml) · [Run and production notes](examples/ranking-football/README.md)

 Reference 

 Clones 

 "GOAT DEBATE" — a 20-second football tier list that puts Ronaldo in D and Messi in S. Two Seedance 2 Mini 720p trolling A-rolls, a 2K goth girl portrait and ten 1K brain-rot B-rolls by GPT Image 2, WhisperX word alignment, a sound-synced ranking board, color-box karaoke captions, buttery-smooth animation and catchy background music, concurrently rendered in 64 headless Chromium processes. Three clones included: swap the narrator to banana cat, flip the rankings and Ronaldo becomes GOAT, or replace all players with tech founders — same viral structure, different viral video. Total cost: $1.15 . 

### Podcast

[Generation source](examples/podcast/reference.svml) · [Run and production notes](examples/podcast/README.md)

 Reference 

 Clones 

 "DAILY CREATINE" — an 18-second podcast clip where a muscle barbie forces creatine on a skinny college kid. Three confrontational A-rolls and an aspirational lifestyle B-roll by Seedance 2 Mini 720p, two 2K AI character portraits and three 1K montage panels by GPT Image 2, WhisperX word alignment, split-screen interview layout, speaker-aware karaoke captions, a product-handoff moment and background music, concurrently rendered in 64 headless Chromium processes. Three clones included: swap both hosts to Pepe and Doge arguing about doggy arms, replace the creatine with retinol where a pretty boy roasts a tomboy's pores, or ditch the physical product for a CheatGPT app where a himbo jock out-GPAs a PhD student — same podcast format, three ad verticals. Total cost: $1.07 . 

### Street Interview

[Generation source](examples/interview/reference.svml) · [Run and production notes](examples/interview/README.md)

 Reference 

 Clones 

 "NICE RIDE" — a 26-second street interview where a mob wife drops three rules for making her first million. Three A-rolls by Seedance 2 Mini 720p, one 2K AI character portrait by GPT Image 2, WhisperX word alignment, head-tracked speaker-colored captions driven by face bounding boxes from Google Video Intelligence and YOLOv8 AnimeFace, a sound-synced emoji reveal board with color flashes and reveal sound effects, plus background music, concurrently rendered in 64 headless Chromium processes. Three clones included: swap hosts to Wojak and Chad, translate everything to Spanish with exactly the same punchlines, or swap the Lambo for an F1 car where Ada explains to Leon how driving Uber led to an accidental Grand Prix win — same three-stage reveal, distinct street-interview remixes. Total cost: $1.09 . 

## Use the Hypit skill

The `/hypit` skill is available to coding agents. Start a session in any empty or existing project
directory and ask it to create videos for you:

```text
/hypit Clone this video: /path/to/video.mp4, and replace the ranking content with a comparison of Hypit (official website: hypit.ai) with other AI video products.
```

Or start without a reference video:

```text
/hypit Make a ranking video that puts Hypit in S tier.
```

Your agent can check the environment, request the credentials the video needs, generate the material, and build the finished composition.

### **👉 [Get 100 FREE AI Avatars with unique voices](https://drive.google.com/drive/u/2/folders/18J9Fz7mkU3OQNJ-2Res3eIyFQ2cemIK5)**

## Why Hypit

- **Clone any video:** drop in a video, get the whole workflow — footage, captions, B-roll, effects. Not a script breakdown.
- **One workflow, 100 variants:** reuse the composition and existing material; generate the parts that change.
- **Pluggable components:** swap the host without touching the captions. Use an installed package, adapt an example, or write your own.
- **Open source:** no Hypit seat pricing, per-render fees or added watermark. Model-service usage is billed by the service you choose.

## What Hypit Can Build

Drop in a video and your agent clones the whole workflow — or describe what you want and it writes one from scratch. Either way you get an editable, re-runnable composition, not a one-off render.

- **Paid social ads** — clone a winning ad from the Meta Ad Library, swap in your product, ship 50 hook variants the same day. When it fatigues in two weeks, re-run with fresh openings; the body never changes.
- **Viral clones** — any 