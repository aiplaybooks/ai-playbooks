> **Motion films that never cut to the next slide.** A Claude Agent Skill that makes product launch films, teasers and feature demos where every beat grows out of the one before — one continuous take, not a stack of scenes.
> **一镜到底的连贯动效。** 做产品发布片、预告片、功能演示：每一个画面都从上一个画面里长出来，是一整条连续的镜头，而不是一张张轮流出场的"PPT"。

[](LICENSE)
[](SKILL.md)
[](cases/)
[](scripts/verify_promo.py)

**▶ See the films and get onetake Pro → [onetakemotion.com](https://onetakemotion.com)**
**▶ 看成片、获取 onetake Pro → [onetakemotion.com](https://onetakemotion.com)**

 From onetake's own launch film. A prompt bar opens into the ad it asked for; the next prompt collapses into a line that shoots across the desk and opens into a festival screen. No cut. [Full film with sound →](cases/onetake-launch-30s/onetake-launch.mp4) 

---

[English](#english) | [中文说明](#chinese)

---

## English

### The problem: motion that falls apart

Most motion videos an AI makes today — and most template tools — come out **loose**. Title card, fade, UI shot, fade,
feature card, fade, logo. Each shot can look fine and the whole still reads like a slideshow, because nothing
connects one beat to the next: scenes *replace* each other.

### What onetake does differently: every beat is carried

onetake treats the boundary between two beats as the thing to design. At every boundary, **something on screen
survives and visibly becomes the next beat**:

- the prompt bar **opens into** the app window; the window **reflows into** the phone;
- a bar **collapses into a line**, the line **shoots across** the desk and **becomes the first grid line** of the next film;
- a card **grows into** the page; a stage **opens from** the character; the camera **pushes through** a card until it *is* the next scene;
- at the end, the cast **folds into** the lockup — in the launch film, the block cursor **writes the name** in one stroke.

And **one camera holds it all together**. It never cuts: it follows the subject a beat ahead, whips to where the next
thing will land, floats like a hand-held operator and shakes when something hits — then holds dead still, because rests
are what make the moves land.

### Continuity is measured, not hoped for

Every film is checked by an oracle before a human watches it. `probe.py` records what is on screen in every frame, finds
each boundary, and asks what carried across it. A film whose beats replace each other fails.

| film | verdict | continuity (carry score) |
|---|---|---|
| an earlier launch film, v1 — perfect rhythm, still a slideshow | rejected | **0.00** |
| the same film, v2 | rejected | **0.40** |
| the same film, v3 — every beat grows out of the last | accepted | **0.75** |
| onetake launch film | accepted | **0.83** |

The same oracle fails uniform cadence (shots all the same length), no stillness, clipped audio, fast moves without
motion blur, and a subject that leaves the frame.

### What makes it look finished

- **Real UI, rebuilt.** The product's interface is rebuilt in HTML from screenshots and sits on the camera's plane, so the camera can fly into it at any zoom. No screen recording.
- **Measured moves.** ~38 moves (springs, entrances, carries, contact, sims, camera, fluid grounds), each a pure function of time with its speed curve measured — never a hand-rolled ease.
- **Real motion blur.** Every moving frame is several captures across an open 180° shutter, averaged in linear light. Fast moves smear instead of strobing.
- **Sound in one room.** Foley and synthesis placed from the film's own events, in one reverb, ducking the music under the hits.
- **Deterministic.** Seek to any time, get the same frame. Drafts at 1080p30, finals at 4K60.

### 🌟 Films made with it

Every case ships the finished film and a breakdown (concept, beat sheet, numbers, what was rejected and why). The
films' source code is not included.

 onetake launch 
 Three prompts, three films, one take — each prompt visibly becomes its film 
 ▶ Film | 📖 Breakdown 
 one-dot 
 One dot is the whole film: caret → menu → loading ring → spring curve → the dot on the i 
 ▶ Film | 📖 Breakdown 

 knockon 
 A chain reaction: every beat is the collision that starts the next 
 ▶ Film | 📖 Breakdown 
 clearing 
 One zoom from a year to a free half hour — 1× to 300× and back, never a cut 
 ▶ Film | 📖 Breakdown 

 pith 
 The window grows out of one phosphor pixel: 440× → 0.52× in one move 
 ▶ Film | 📖 Breakdown 
 ebb 
 A field of light carries the take through five places; each flood drains onto the next 
 ▶ Film | 📖 Breakdown 

 overlap 
 Two print passes slide into register — and an & appears that was hidden in both 
 ▶ Film | 📖 Breakdown 
 unbroken 
 One ink stroke that is never lifted: procedural brush, no textures 
 ▶ Film | 📖 Breakdown 

 motion-web 
 Where the rhythm rules came from: small UI, big ground, rests, then a burst 
 ▶ Film | 📖 Breakdown 
 skill-demo 
 An operation demo from nothing: the chosen menu row flies into the input as a chip, and on from there 
 ▶ Film | 📖 Breakdown 

> one-dot and skill-demo were made when the skill was still called *ohmymotion*; the films show that name.

### How a film is made

1. **Deconstruct the reference in numbers:** how much of it is still, where it cuts, how its moves ease.
2. **Three concepts, pick one.** Each is one sentence about the *picture* — "one dot becomes everything", "one zoom through scale" — not three stories told with the same cards.
3. **A beat sheet for rhythm *and* carry.** Shot lengths vary by ≥ 4×, and every boundary names what survives it.
4. **Compose** one HTML file on the move library. **Render** with motion blur. **Score** the sound from the film's events.
5. **Verify**, then show a human.

### 📦 Installation

```bash
# Claude Code
git clone https://github.com/feitangyuan/onetake.git ~/.claude/skills/onetake
# Codex / other agents that read skills
git clone https://github.com/feitangyuan/onetake.git ~/.agents/skills/onetake
```

Then ask: *"Make a 15 s launch video for my app"*, *"a feature demo rebuilt