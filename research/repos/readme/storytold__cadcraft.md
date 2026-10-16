CADCraft 

 Computer-aided design and drafting; an open-source, clean-room reimplementation of Autodesk AutoCAD, rebuilt in pure Rust. 

 A fast, open-source take on the AutoCAD workflow: the command line, object snaps, layers,
 dimensions, hatches, blocks and DXF drawings you already know. It runs natively on macOS,
 Windows, Linux and FreeBSD, and in the browser via WebAssembly. 
 By the ArtCraft team. 

 CADCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 Apartment plan ( examples/apartment.dxf ): walls with pick-point hatching, TrueType MTEXT room labels, a TABLE, a multileader and architectural dimensions — built entirely from CADCraft commands. 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Painters, photographers,
> filmmakers, illustrators, designers, animators, hobbyists, and people who picked up a pencil
> last week. If you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 Screenshots ·
 Why CADCraft ·
 What works today ·
 Quick start ·
 Agents, MCP and the CLI ·
 Architecture ·
 Roadmap ·
 Downloads ·
 The Crafting Apps ·
 License and credits 

## Screenshots

 Layouts : paper space with viewports, page setups and PLOT to PDF. Double-click a viewport to work in model space through it. 
 Mounting bracket : a two-view part drawing with centre lines, hidden lines, an ANSI31 section hatch and a title block. 

## Why CADCraft

- **The workflow you know.** Type `L`, click two points, type `@5 cargo build --release`) also embed its
fonts: BIZ UDPGothic, BIZ UDMincho and Shippori Mincho (Japanese) and Noto Sans Arabic (the web
build, which has no system fonts, only BIZ UDPGothic Regular and Noto Sans Arabic). A text style
can use them by family name, and they draw characters a text's font lacks when no installed
wide-coverage CJK font has them. Without `CRAFT_FONTS_DIR` nothing is embedded. SHX
fonts (including big fonts such as `chineset.shx`) aren't read yet: text in an SHX style is drawn
with our own stroke font, and any character a text's font lacks (CJK, for example) is drawn from
an installed font that has it, preferring wide-coverage fonts such as Noto Sans CJK, Source Han
Sans, WenQuanYi, PingFang or Microsoft JhengHei. Two settings, set with `SETVAR` or (for every
run) an environment variable, steer this:

| Variable | Environment | Meaning |
|---|---|---|
| `FONTALT` | `CADCRAFT_FONTALT` | Font used instead of a text style font that can't be found (an SHX file, a missing TTF), by file or family name, e.g. `Noto Sans CJK TC`. Empty (default) = our stroke font. |
| `FONTFALLBACK` | `CADCRAFT_FONTFALLBACK` | Fonts tried first for characters a text's font lacks, comma-separated, e.g. `Noto Sans CJK TC, msjh.ttc`. |

`.` clears either one.

**Your own fonts.** Any `.ttf`, `.otf` or `.ttc` font works: install it in the system font folder
(Windows `C:\Windows\Fonts` or per-user fonts, macOS `/Library/Fonts` or `~/Library/Fonts`,
Linux and the BSDs `/usr/share/fonts`, `/usr/local/share/fonts`, `~/.local/share/fonts` or
`~/.fonts`) and name it in a text style (`STYLE`, or `style {"name":"FA","font":"Vazirmatn"}`)
by file name (`Vazirmatn-Regular.ttf`) or family name (`Vazirmatn`), or inline in MTEXT with
`\fVazirmatn;`. Restart CADCraft after installing a font: the font folders are scanned once.

**Right-to-left text (Persian, Arabic, Urdu, Hebrew).** TEXT and MTEXT lines are laid out with the
Unicode Bidirectional Algorithm (the paragraph direction comes from its first letter, so numbers
and Latin words inside Persian text keep their own order), and Arabic-script text is shaped with
OpenType (contextual letter forms, lam-alef and other ligatures, ZWNJ / ZWJ, mark positioning).
Justification (left, centre, right, MTEXT attachment and wrapping) still refers to the text's box.
Our stroke font has no Arabic letters, so Persian in a stroke-font style is drawn from an
installed font that has them: Vazirmatn, Noto Naskh Arabic, Noto Sans Arabic, Segoe UI, Tahoma,
Arial and DejaVu Sans are looked for first. To choose the font, install a free Persian font such
as [Vazirmatn](https://github.com/rastikerdar/vazirmatn) (SIL Open Font License) and either use it
in the text style or set `FONTFALLBACK` (`CADCRAFT_FONTFALLBACK="Vazirmatn"`). Formatting changes
inside a word (an MTEXT colour change in the middle of a Persian word) break the joining at that
point.

### Logs

The desktop app writes its `log` records to standard error and to `logs/cadcraft.log` in the
settings directory (Linux and the BSDs `~/.config/cadcraft/logs/`, or
`$XDG_CONFIG_HOME/cadcraft/logs/`; macOS `~/Library/Application Support/CADCraft/logs/`; Windows
`%APPDATA%\CADCraft\logs\`; or under `CADCRAFT_CONFIG_DIR`). A start from a desktop menu or the
Dock has no terminal, so this file is what to attach to a bug report. Each launch moves the
previous log to `cadcraft.1.log` (and that one to `cadcraft.2.log`), so the log of a run that
crashed survives the next start. The file stops growing at 16 MiB. `--version` writes no file.

| Variable | Effect |
|---|---|
| `CADCRAFT_CONFIG_DIR` | Use this directory instead of the platform settings directory (the log goes to its `logs/`) |
| `RUST_LOG` | Log levels for standard error and the log file. Default: `info` for CADCraft's own crates, `warn` for everything else. env_logger-style directives replace that, e.g. `RUST_LOG=debug`, `RUST_LOG=warn,cadcraft_io=trace` or `RUST_LOG=info,wgpu_core=warn`; a directive ending in `*` covers every target starting with it (`cadcraft*=debug`). `cadcraft_engine=debug` also logs every command-line message. |

The logger is `apps/cadcraft/src/logging.rs`; the web build logs to the browser console instead.

## Drive it from agents, MCP and the CLI

```sh
# MCP server on stdio, headless:
cadcraft-cli mcp
# …or bridged to the running app (start it with --control 7979):
cadcraft-cli mcp --connect 127.0.0.1:7979

# One-shot headless runs:
cadcraft-cli run --sample --script '