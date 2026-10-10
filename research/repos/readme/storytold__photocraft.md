PhotoCraft 

 Image editing; an open-source, clean-room reimplementation of Adobe Photoshop, rebuilt in pure Rust. 
 Layers, masks, adjustment layers, layer styles, type, vectors, brushes and real PSD files, 
 in a native app written entirely in Rust. Open source, offline, and yours.

 PhotoCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 A caption card with a drop shadow, live type, and Vibrance and Curves adjustment layers, with the Curves editor open. 
 The Great Wave off Kanagawa , Katsushika Hokusai, c. 1831 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Digital, generative, music,
> games &mdash; if you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 Features ·
 Everything in the box ·
 PSD ·
 Agents ·
 Under the hood ·
 Get started ·
 Downloads ·
 Crafting Apps ·
 Discord 

 🎛️ Familiar by design 
 The menus, shortcuts, panels and tools are where your hands expect them, from ⌘J to ⇧⌘D. If you know Photoshop, you already know PhotoCraft.

 ⚡ Native and fast 
 A GPU compositor on wgpu (Metal, Vulkan, DX12, WebGPU), copy-on-write tiles and multithreaded filters. No Electron, no web view, no waiting.

 🗂️ Real PSD files 
 Open, edit and save layered Photoshop documents. Re-saving keeps the render of 307 of the 309 psd-tools test files.

 🤖 Agent-ready 
 Every action is a command, so you can drive the same engine from the UI, the CLI, a JSON control channel or an MCP server.

## Features

Every screenshot here is the real app at work on public-domain art, rendered offscreen through its control channel.

 Levels and Vibrance adjustment layers, with the live Histogram panel. Impression, Sunrise , Claude Monet, 1872 
 Edit without regret 
 Adjustment layers keep every edit live. Stack Levels, Curves, Vibrance, Hue/Saturation and a dozen more, mask them to an area, reorder them, or turn them off, and your original pixels never change.

 16 adjustment layers that also apply directly to pixels, including Curves with per-channel editing, Levels with a live histogram, Black &amp; White, Channel Mixer, Gradient Map, Photo Filter, Selective Color and Color Lookup (.cube, .3dl, .look). Plus Shadows/Highlights, Replace Color, Match Color, HDR Toning, Desaturate and Equalize.

 Outer Glow and Stroke on a live type layer, in the Layer Style dialog. Earthrise , William Anders / NASA, 1968 
 Styles that sell the shot 
 Drop Shadow, Inner Shadow, Outer and Inner Glow, Bevel &amp; Emboss, Satin, Stroke, and Color, Gradient and Pattern Overlay, live on any layer, including type. Patterns come from a library (built-ins, Edit › Define Pattern, .pat import/export) and PSD Patt blocks.

 Copy and paste styles between layers, hide all effects at once, and open styles straight from your PSDs, rendered to match Photoshop.

 An elliptical selection becomes the mask of a Hue/Saturation layer, so only the face keeps its color. Girl with a Pearl Earring , Johannes Vermeer, c. 1665 
 Selections that understand your image 
 Marquees, lassos and the Magic Wand for precision; Quick Selection, Object Selection and Select Subject when you want the computer to do the tracing; Select and Mask to refine hair-fine edges.

 Feather, expand, contract, smooth, grow, reselect. Turn any selection into a layer mask, a vector path or a shape. Smart selection runs on your machine, with no cloud and no account.

 A headline edited in place, with a byline and a paragraph of body text. Among the Sierra Nevada, California , Albert Bierstadt, 1868 
 Type that sets beautifully 
 Point and paragraph text, edited right on the canvas, with full Character and Paragraph controls: font, weight, size, leading, tracking, alignment and colour. The full Type Color Picker also supports screen sampling with a pixel loupe.

 Type layers stay editable, take layer styles, and round-trip through PSD.

 A badge made of shape layers: a gradient-filled lotus, a star and a dotted ring. Water Lilies , Claude Monet, 1906 
 Pixel-perfect vectors 
 Rectangle, Ellipse, Triangle, Polygon, Line and the Pen tool, with resolution-independent shape layers, gradient fills, and dashed, aligned strokes.

 Combine shapes (unite, subtract, intersect, exclude), keep paths in the Paths panel, use them as vector masks, or stroke and fill them. 116 of 116 shape layers in our PSD corpus match Photoshop's pixels.

 Twirl previews live on the canvas, only inside the selection. The Starry Night , Vincent van Gogh, 1889 
 See it before you commit 
 Every filter dialog previews live on the canvas, through your selection. Blurs (Gaussian, Box, Motion, Radial, Surface, Smart, Lens, Shape, and the Blur Gallery: Tilt-Shift, Iris, Field, Spin, Path), sharpening, Reduce Noise, distortions (Twirl, Wave, Ripple, Displace, Shear, Zig Zag…), Pixelate, Stylize (Oil Paint, Wind, Extrude…), Render (Clouds, Fibers, Lens Flare, Lighting Effects) and more.

 Run filters on a smart object and they stay editable: change, hide, reorder or mask them at any time.

 Large-radius blurs use running-sum box passes across all cores: a radius-180 Gaussian on 3.6 MP takes under a second.

 Free Transform on a rotated print, with every step listed in History. The Tetons and the Snake River , Ansel Adams, 1942 
 Shape it any way you like 
 Free Transform with scale, rotate, skew, distort and perspective; exact 90° and 180° rotations and flips; Transform Again. Layers, type, shapes, masks and selections all transform together.

 Full history, Toggle Last State and the History Brush mean every step can be undone, even one brush stroke at a time.

 Export As in the light theme, with a preview and a file-size estimate. The Kiss , Gustav Klimt, 1907–1908 
 Ship it anywhere 
 Export As with format, quality, transparency and scale, plus a preview and an instant file-size estimate. Quick Export to PNG in one click.

 Choose a dark Pro theme, the airy Studio themes, or a Classic look.

## Everything in the box

 🧰 52 tools 
 Move · Rect