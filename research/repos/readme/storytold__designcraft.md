DesignCraft 

 Page layout and publishing; an open-source, clean-room reimplementation of Adobe InDesign, rebuilt in pure Rust. 

 A fast, open-source, clean-room take on the Adobe InDesign workflow. It runs natively on macOS,
 Windows and Linux, and in the browser via WebAssembly. 
 By the ArtCraft team. 

 DesignCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 Quarterly, Spring Issue : threaded three-column body text, a wrapped pull quote and parent-page folios, all set by DesignCraft's own paragraph composer. 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Digital, generative, music,
> games &mdash; if you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 The sample magazine ·
 Why DesignCraft ·
 Quick start ·
 Web ·
 Architecture ·
 Downloads ·
 The Crafting Apps ·
 License and credits 

## The sample magazine

Every page below was laid out by DesignCraft from code (`crates/engine/src/sample.rs`) and exported
by its own renderer. Try it yourself with `File → New → Sample Document`, or start the app with
`--sample`.

 Cover. A full-bleed graphic frame, display type and an italic deck. 
 Styles. Kicker rule, headline, deck, caption and justified two-column body. 

 Threading, columns and text wrap. One story flows through three columns and around the pull quote. 
 Swatches. Named colors and a CMYK process swatch, laid out as a palette. 

## Why DesignCraft

- **Familiar.** InDesign's layout, tools, menus, panels and shortcuts: spreads and parent pages,
 frames and threaded stories, the Control panel, paragraph and character styles, swatches, text
 wrap and more. If you know InDesign, you already know how to use it.
- **Beautiful type.** A Knuth–Plass paragraph composer (plus single-line), dictionary hyphenation
 (the public-domain Moby word list plus our own trained patterns), word, letter and glyph-scaling
 justification, keeps, optical margin alignment, columns, baseline grid, tabs, rules and shading.
 Line breaks are identical on screen and in PDF.
- **Fast.** Multithreaded SIMD rendering (vello_cpu), copy-on-write documents with O(1) undo
 snapshots, and cached composition.
- **Open.** A documented native format, IDML import and export, and PNG, PDF (PDF/X-4, PDF/A-2b)
 and EPUB export.
 No subscription, no licence server, no telemetry.
- **Agent-native.** Every menu item, tool gesture, panel control and dialog can be driven over a
 JSON control channel and an **MCP server**, so Claude and other agents can lay out and edit
 documents like a designer. See [`docs/control-protocol.md`](docs/control-protocol.md) and
 [`docs/mcp.md`](docs/mcp.md).
- **Everywhere.** One Rust codebase for desktop and the web.

## Quick start

The egui frontend requires Rust 1.95 or newer (including its shared `craft-ui` components).

```sh
cargo run --release -p designcraft # desktop app (start screen)
cargo run --release -p designcraft -- --sample # open the sample magazine
cargo run --release -p designcraft -- --sample --control 7979 # + JSON control channel
cargo run --release -p designcraft-cli -- run --sample --all-pages out/ # headless: render every page to PNG
cargo run --release -p designcraft-cli -- commands # list every command
cargo run --release -p designcraft-cli -- script --help # command script syntax (docs/agents.md)
cargo xtask ci # fmt, clippy, tests, assets, layering, wasm
```

Japanese text (UI and documents) uses fonts from
[storytold/craft-fonts](https://github.com/storytold/craft-fonts), an optional build input (font
files are never committed here; see craftrules
[`standards/fonts.md`](https://github.com/storytold/craftrules/blob/main/standards/fonts.md)):

```sh
git clone https://github.com/storytold/craft-fonts ../craft-fonts
CRAFT_FONTS_DIR="$PWD/../craft-fonts" cargo run --release -p designcraft # absolute path
```

Without it, Japanese falls back to the system's fonts (none on the web). Release builds always
include it.

To drive a running app, send JSON lines to `127.0.0.1:7979`. The protocol is described in
[`docs/control-protocol.md`](docs/control-protocol.md).

### Logs

The desktop app writes its `log` records to standard error and to `logs/designcraft.log` in the
settings directory, beside `ui.json` and `prefs.json` (Linux `~/.config/designcraft/logs/`, or
`$XDG_CONFIG_HOME/designcraft/logs/`; macOS `~/Library/Application Support/DesignCraft/logs/`;
Windows `%APPDATA%\DesignCraft\logs\`). A start launched from a desktop menu or the Dock has no
terminal, so this file is what to attach to a bug report: the crash guard's panic report and a
failed crash-recovery save land there. Each launch moves the previous log to `designcraft.1.log`
(and that one to `designcraft.2.log`), so the log of a run that crashed survives the next start.
The file stops growing at 16 MiB. `--version` writes no file.

| Variable | Effect |
|---|---|
| `RUST_LOG` | Log levels for standard error and the log file. Default: `info` for DesignCraft's own crates, `warn` for everything else. env_logger-style directives replace that, e.g. `RUST_LOG=debug`, `RUST_LOG=warn,designcraft_render=trace` or `RUST_LOG=info,wgpu_core=warn`; a directive ending in `*` covers every target starting with it (`designcraft*=debug`). |
| `WGPU_BACKEND` | The graphics backend that composites the window: `dx12`, `vulkan`, `gl` or `metal` (a comma-separated list lets wgpu choose among them). Default: DirectX 12 on Windows, Vulkan on Linux, Metal on macOS, with OpenGL as the fallback. Setting it also turns off the start-up fallback described below. |

The logger is `apps/designcraft/src/logging.rs`; the web build logs to the browser console instead.

### Graphics backend

The canvas is rendered on the CPU; the GPU only composites the interface, through wgpu. A
graphics driver that faults takes the process down before any Rust code can catch it, so the
backend is chosen before the window exists, and a start that never showed a frame is remembered:
`gp