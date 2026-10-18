Anatomy 

 A Claude skill that explains an idea by building it as a real, working object. Also runs in Antigravity, OpenCode, Codex and MiniMax Code. Crafted, interactive isometric figures with many small precise parts, in SVG, WebGL and 3D. 

 &nbsp;

 &nbsp;

 Quick start ·
 Gallery ·
 What it makes ·
 Install ·
 Usage ·
 Examples ·
 How it works ·
 Limits 

 examples/raptor-engine , light theme, firing. The engine and stand are SVG; the plume is a WebGL shader in the same isometric camera. 

---

Ask Claude for a figure that explains a technical idea, and Anatomy has it invent a physical thing whose working *is* the concept. A cache key that skips work when nothing changed becomes a pin-tumbler lock that only turns when every pin matches. One GPU context serving many canvases becomes a gantry plotter whose single print head visits 16 wells.

Then Claude builds that thing out of dozens of small, solid, shaded parts, puts it in a framed card with a title, a hint and a live readout, makes it move calmly under the pointer and the keyboard, and checks its own work by zooming in on every joint. Every number the figure shows comes from the same small model that moves its parts.

## Quick start

```sh
npx skills add wheresryan22/anatomy -g
```

The CLI asks which agents to set up (Claude Code, Antigravity, OpenCode, Codex, MiniMax Code). To skip the question, add `-a claude-code`, `-a antigravity`, `-a opencode`, `-a codex`, or `-a minimax-code`.

Then, in Claude Code:

```text
/anatomy explain how a token bucket rate limiter works, interactive
```

For Antigravity, OpenCode, Codex, or MiniMax Code, target that agent: `-a antigravity`, `-a opencode`, `-a codex`, or `-a minimax-code`. Antigravity, OpenCode and MiniMax Code take the same `/anatomy` command; in Codex, type `$anatomy`.

That's it. No API keys and nothing to `npm install`: the kit uses only Node's built-in modules.

## Gallery

 raptor-engine : hover to take it apart into 11 assemblies. An audit proves that no pipe passes through anything, at rest, apart and in every frame between. 
 ripple-tank : SVG apparatus over two WebGL layers (lamp light and caustics on the paper, reflections in the water) driven by a dispersion and optics model. 

 turning-dial : the 3D mode (beta). About 90 parts are re-projected and re-shaded every frame as you drag the dial. 
 dial-indicator : the smallest example, about 300 lines. Hover to slide the carriage; the needle reads each block. 

Every screenshot is the light theme of a page in [`examples/`](examples), captured with the skill's own [`scripts/capture.mjs`](scripts/capture.mjs) and [`scripts/drive.mjs`](scripts/drive.mjs). The built pages are committed: open any `.html` in `examples/` to try it.

## What it makes

Three kinds of figure. All three share one kit, one camera and one set of craft rules.

| Kind | What it is | Example |
|---|---|---|
| **SVG** | The core. Solid isometric parts with four-tone shading, painted back to front, in a card with a live readout and eased motion. It ships as a standalone HTML page, a lone `.svg` file with its styles embedded, or React/Next.js components. | `dial-indicator`, `desk-computer`, `arcade-cabinet`, `test-rig` |
| **SVG + WebGL** | For what lines can't draw: fire, exhaust, water, caustics, lamp light, glow, steam. The shader runs in a canvas between a back and a front SVG, in the figure's own isometric camera, so it sits inside the drawing. The SVG still reads without WebGL. | `raptor-engine`, `ripple-tank` |
| **3D** beta | Parts that turn in true 3D: a dial or turntable that spins, fingers that flex, a piece that breaks off and falls. The moving parts are re-projected and re-shaded by the kit's own rules every frame; the rest of the figure stays static art. | `turning-dial` |

Each figure is light or dark. Light is the theme the skill designs for first, shaders included.

## Install

Anatomy is a standard [Agent Skill](https://agentskills.io): a folder with a `SKILL.md` at its root. This repository is that folder. Pick one way in:

| | Command | Installs to |
|---|---|---|
| **skills CLI**, for you (Claude Code) | `npx skills add wheresryan22/anatomy -g -a claude-code` | `~/.claude/skills/anatomy` |
| **skills CLI**, for you (Antigravity) | `npx skills add wheresryan22/anatomy -g -a antigravity` | `~/.gemini/antigravity/skills/anatomy` |
| **skills CLI**, for you (OpenCode) | `npx skills add wheresryan22/anatomy -g -a opencode` | `~/.config/opencode/skills/anatomy` |
| **skills CLI**, for you (Codex) | `npx skills add wheresryan22/anatomy -g -a codex` | `~/.agents/skills/anatomy` |
| **skills CLI**, for you (MiniMax Code) | `npx skills add wheresryan22/anatomy -g -a minimax-code` | `~/.minimax/skills/anatomy` |
| **skills CLI**, for one project | `npx skills add wheresryan22/anatomy` | `.claude/skills/anatomy` for Claude Code, `.agents/skills/anatomy` for Antigravity, OpenCode and Codex, `.minimax/skills/anatomy` for MiniMax Code |
| **git**, for you (Claude Code) | `git clone https://github.com/wheresryan22/anatomy.git ~/.claude/skills/anatomy` | `~/.claude/skills/anatomy` |
| **git**, for you (Antigravity) | `git clone https://github.com/wheresryan22/anatomy.git ~/.gemini/antigravity/skills/anatomy` | `~/.gemini/antigravity/skills/anatomy` |
| **git**, for you (OpenCode) | `git clone https://github.com/wheresryan22/anatomy.git ~/.config/opencode/skills/anatomy` | `~/.config/opencode/skills/anatomy` |
| **git**, for you (Codex) | `git clone https://github.com/wheresryan22/anatomy.git ~/.agents/skills/anatomy` | `~/.agents/skills/anatomy` |
| **git**, for you (MiniMax Code) | `git clone https://github.com/wheresryan22/anatomy.git ~/.minimax/skills/anatomy` | `~/.minimax/skills/anatomy` |
| **git**, for one project | `git clone https://github.com/wheresryan22/anatomy.git .claude/skills/anatomy` | `.claude/skills/anatomy` (Claude Code and OpenCode) or `.agents/skills/anatomy` (Antigravity, OpenCode, Codex and MiniMax Code) |
| **Download**, no git | 