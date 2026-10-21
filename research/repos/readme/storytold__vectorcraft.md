VectorCraft 

 Vector illustration; an open-source, modern vector art application, built in pure Rust. 

 A fast, open-source vector illustration workflow. It runs natively on
 macOS, Windows, Linux and FreeBSD, and in the browser via WebAssembly. Built by the ArtCraft team.

 VectorCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 Neon Drive : a Pathfinder-cut sun, live Outer Glow on the type and grid, and clipping masks · examples/neon-drive.vectorcraft 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Digital, generative, music,
> games &mdash; if you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 A look around ·
 Made in VectorCraft ·
 Why VectorCraft ·
 Quick start ·
 Status ·
 Downloads ·
 The Crafting Apps ·
 License 

## A look around

 Live Blends and Layers : editable key paths, smooth colour, every object a row 

 Pen and Direct Selection : real Bézier anchors and handles, plus a contextual task bar 

 3D Revolve : smooth vector shading, caps and a rotation gizmo · examples/still-life.vectorcraft 

 Dimension tool : lengths, angles and radii that follow the art they measure · examples/bracket-drawing.vectorcraft 

 Perspective Grid : art attached to its planes stays editable in perspective · examples/perspective-city.vectorcraft 

 Multiple artboards, light theme : Pathfinder · Gradient Mesh · live radial Repeat · Envelope Distort · examples/feature-sheet.vectorcraft 

## Made in VectorCraft

Every piece below was built entirely through VectorCraft's command API, the same one the MCP server
exposes to agents, and exported by VectorCraft's own renderer. The source files are in
[`examples/`](examples).

 Neon Drive : synthwave poster with glowing type and grid 

 Dusk : gradient sky, glowing sun, layered mountains 

 Live Blends : 70 steps, smooth colour, editable spines 

 Still Life : four revolved profiles with smooth vector shading 

 Radial Repeat : a live mandala 

 Envelope Distort : striped type warped into a flag 

 Gradient Mesh : shaded spheres 

 Pathfinder : a crescent and stars from exact booleans 

## Why VectorCraft

- **Familiar.** A familiar layout, tools, menus, panels and shortcuts: the Pen, Direct Selection,
 Pathfinder, Smart Guides, Appearance, Swatches, Layers and more. You already know how to use it.
- **Fast.** Multithreaded SIMD rendering off the UI thread. 20,000 shapes render in about 27 ms at
 full retina resolution while the interface stays at 120 fps.
- **Robust.** Exact curve booleans (no "cannot perform operation"), unlimited undo via structural
 sharing, and property-tested file round trips.
- **Open.** A documented native format (`.vectorcraft`, JSON), first-class SVG, PDF (and
 PDF-compatible `.ai`) import and export, PNG/JPEG/WebP export, Export for Screens, and SVGZ,
 templates, GIF, TIFF and BMP on open.
- **Agent-native.** Every menu item, tool gesture, panel and dialog can be driven over a JSON
 control channel and an **MCP server**, so Claude and other agents can draw, edit and export the
 way a person does.
- **Everywhere.** One codebase for the desktop apps and the same UI in the browser.

## Quick start

For posters and sewing patterns, see [Print a large poster across multiple pages](docs/print-tiling.md).

```sh
git clone https://github.com/storytold/vectorcraft
cd vectorcraft

cargo run --release -p vectorcraft # desktop app
cargo run --release -p vectorcraft -- examples/dusk-poster.vectorcraft
cargo run --release -p vectorcraft -- --control 7979 # + JSON control channel
cargo run --release -p vectorcraft-cli -- mcp # MCP server (stdio)
cargo run --release -p vectorcraft-cli -- run --in examples/ribbons.vectorcraft --export out.pdf # headless batch
cargo run --release -p vectorcraft-cli -- bench examples/neon-drive.vectorcraft # render timing
cargo xtask bundle # dist/VectorCraft.app (macOS)
cd apps/vectorcraft-web && trunk build --release # web build → dist/web
cargo xtask ci # fmt, clippy, tests, layering, wasm, vendor names
```

For text and custom letter shapes, see [Typography and Custom Lettering](docs/typography-lettering.md).

Japanese fonts come from [storytold/craft-fonts](https://github.com/storytold/craft-fonts), an optional
build input (releases always use it): `CRAFT_FONTS_DIR="$PWD/../craft-fonts" cargo run --release -p vectorcraft` (an absolute path).
Without it, Japanese text uses the installed system fonts. See [`docs/development.md`](docs/development.md#fonts-craft-fonts-optional-build-input).

On machines with two graphics processors, VectorCraft renders on the power-saving (integrated) one by default on
Windows and macOS, and on the one the desktop runs on under Linux. To choose, use **Preferences › Performance ›
Graphics Processor** and restart. If a graphics processor can't show the window, VectorCraft starts again on the
next one. To pick one when starting the app, set `WGPU_POWER_PREF=high` (or `low`), or `WGPU_ADAPTER_NAME` to part of
its name, such as `WGPU_ADAPTER_NAME=nvidia` (see [`docs/development.md`](docs/development.md#desktop-graphics-processor)).

On native Wayland, winit 0.30 does not deliver dropped files. To open an SVG, use File › Open;
to place artwork in the current document, copy and paste the file in a file manager. For file
drag-and-drop, set **Preferences › Performance › Linux Display Server** to **X11 (XWayland)** and restart, or start
the app with `WAYLAND_DISPLAY= vectorcraft`: the window then opens through XWayland, where drops work
(see [`docs/development.md`](docs/development.md#linux-wayland-and-x11)).

On Linux with Wayland, under KDE Plasma 6.3 or later and under GNOME, VectorCraft doesn't respond to a drawing tablet's
pen yet (#491, #2028). Open the window through XWayland instead, where the pen works as a mouse: set the same
preference to **X11 (XWayland)**, or to **X11 (XWayland) When a Pen Is Attached** to use XWayland only when a pen is
attached as VectorCraft starts, and restart; or start 