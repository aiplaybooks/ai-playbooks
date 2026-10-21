LightCraft 

 Your photos. Your pixels. Your machine. 

 English ·
 简体中文 

 Photo library and raw development; an open-source, non-destructive photo library and raw developer, built in pure Rust. 
 Native on macOS, Windows and Linux. In the browser via WebAssembly. Drivable end to end by AI agents over MCP.

 LightCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 Ansel Adams, "The Tetons and the Snake River" (1942). Public domain, U.S. National Archives. Developed in LightCraft. 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Digital, generative, music,
> games &mdash; if you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 Editing ·
 Color grading ·
 Before &amp; after ·
 Masking ·
 Presets ·
 Library ·
 Agents &amp; MCP ·
 Performance ·
 Status ·
 Quick start ·
 Roadmap ·
 Downloads ·
 Crafting Apps 

## Edit like you mean it

LightCraft is a complete darkroom in a single native app. Every adjustment is **non-destructive**, so your originals
are never touched. Every slider renders through a **scene-referred, wide-gamut, 32-bit float pipeline**: highlights
roll off like film, shadows open up without halos, and colour stays clean from capture to export.

### ☀️ Light
**Exposure, Contrast, Highlights, Shadows, Whites, Blacks**, with edge-aware local tone mapping (a guided filter on
log-luminance). Pulling −100 Highlights recovers a blown sky without the grey halos you'd get from a naive curve.

### 🎨 Color
**White balance** by temperature and tint (Kelvin for raw, relative for JPEG) with presets, Auto and a
click-to-neutralise **eyedropper**. **Vibrance** that protects skin tones, **Saturation**, an 8-band **Color Mixer**
(hue / saturation / luminance) and 3-way **Color Grading** wheels with blending and balance. All of it is computed in
OkLCh, a modern perceptual colour space.

### ✨ Effects
**Texture** for fine detail, **Clarity** for mid-tone punch, **Dehaze** (dark-channel prior with guided refinement;
push it negative to add atmosphere), post-crop **Vignette** with highlight priority, roundness and feather, and
resolution-independent film **Grain** with size and roughness.

### 📈 Tone Curve
Parametric region curve with movable splits **plus** point curves for RGB, Red, Green and Blue. Curves are monotone by
construction, so you never get an accidental tone inversion.

 A gentle S on the RGB point curve, right under the Light sliders. Ansel Adams, 1942 (public domain). 

## Color grading, the cinematic way

Split-tone shadows, midtones and highlights independently with drag-anywhere colour wheels. Below, Dorothea Lange's
*Migrant Mother* gets a warm, print-like tone (highlights at 42°, shadows at 28°) in two drags.

 Shadows, midtones and highlights wheels in the Color panel. Dorothea Lange, "Migrant Mother" (1936). Public domain, Library of Congress. 

## Before & after

Press \\ to toggle the Before view, Y for side by side, or Shift + Y for a
split view. Every image below is a real screenshot of LightCraft, captured automatically by an agent through the
[control channel](#built-for-agents).

 The Tetons and the Snake River. Highlights −45, Shadows +38, Clarity +28, Dehaze +18. Ansel Adams, 1942 (public domain). 
 Migrant Mother. Shadows +42, Texture +18, split-toned grade, vignette. Dorothea Lange, 1936 (public domain). 

 Earthrise. Dehaze +22, Highlights −30, warmer white balance, Vibrance +22. NASA / Bill Anders, Apollo 8, 1968 (public domain). 
 The Blue Marble. Highlights −38, Blacks −20, Dehaze +15, Vibrance +30. NASA, Apollo 17, 1972 (public domain). 

## Masking that goes where you point

Paint with a **Brush** (size, feather, flow, density, erase), drop **Linear** and **Radial Gradients** with draggable
pins, or select by **Luminance Range**, **Color Range**, **Sky**, **Subject** and **Background**. Combine components
with **Add / Subtract / Intersect**, invert any of them, and dial in 17 local adjustments per mask (Temp, Tint,
Exposure, Contrast, Highlights, Shadows, Whites, Blacks, Texture, Clarity, Dehaze, Hue, Saturation, Sharpness, Noise,
Moiré, Defringe), plus an overall Amount.

Desktop **Object** and **Describe** masks use SAM 3 for click-based and text-prompt selection, with a separately
installed model; see [model setup and terms](docs/ai-masks.md). Subject, Sky and Background selections still use
classical heuristics. Existing model-generated masks render and export without the model installed.

 A radial "Sun glow" mask (Temp +40, Exposure +0.50) layered over a linear "Sky" mask. Photo from LightCraft's procedurally generated demo library. 

## Presets, profiles & the Color Mixer

Forty-one hand-built presets ship in the box (*Golden Hour, Teal & Orange, Faded Matte, Selenium Tone, Crisp
Landscape* and more), each with an **Amount** slider from 0 to 200 %. Save your own from any group of settings, mark
favourites, and copy, paste or sync edits across a whole selection with exactly the groups you choose.

 The Presets column next to the 8-band Color Mixer. Photo from the demo library. 

### ✂️ Crop, straighten & geometry
Free or locked aspect ratios (1:1, 4:5, 5:7, 2:3, 4:3, 16:9, 16:10, original), drag-to-rotate straightening that always
keeps the largest crop inside the image, thirds / grid / golden-ratio overlays, flips and 90° rotations, plus
manual Vertical, Horizontal, Rotate, Aspect, Scale and Offset transforms.

### ⚫️ Black & White
One click ( V ) to monochrome, with an 8-band **B&W Mix** that lets you darken skies or make foliage glow.
Then tone it with Color Grading for selenium, sepia or split-tone prints.

 A 16:9 crop straightened +2.5° with the thirds overlay. Ansel Adams, 1942 (public domain). 
 Split view: colour original on the left, B&W with Clarity, Vignette and Grain on the right. Demo library. 

## Organize everything

A library that stays out of your way: **All Photos**, **Recently Added**, **Picks**, **By Date**, **Albums** nested in
**Folders**, and **Rece