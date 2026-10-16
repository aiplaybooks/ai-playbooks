GridCraft 

 Spreadsheets and data; an open-source, clean-room reimplementation of Microsoft Excel, rebuilt in pure Rust. 

 A fast, open-source, clean-room take on the Excel workflow. It runs natively on macOS,
 Windows, Linux and BSD, and in the browser via WebAssembly. 
 By the ArtCraft team. 

 GridCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 Quarterly Sales Dashboard : a table with a totals row, conditional formatting, sparklines and two live charts — built entirely from GridCraft commands ( File → New → Sample ). 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Painters, photographers,
> filmmakers, illustrators, designers, animators, hobbyists, and people who picked up a pencil
> last week. If you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 A look around ·
 Why GridCraft ·
 Quick start ·
 For agents ·
 Architecture ·
 Roadmap ·
 The Crafting Apps ·
 License and credits 

## A look around

 Formatting. Accounting formats, cell styles, conditional rules and colour scales, frozen headers and a bar chart. 
 Formulas. 500+ functions, dynamic arrays, LET and LAMBDA, structured table references. 

 Dark mode and the Insert tab: tables, charts, sparklines, pictures, shapes, links and comments. 
 PivotTables. Field list, filters, layouts, date grouping and show-values-as, saved to and read from XLSX. 

 Charts. Seventeen chart types, Chart Design tab and a Format pane; selecting a chart outlines its source data. 
 Page Break Preview , print settings, and PDF export and printing. 

## Why GridCraft

- **Familiar.** Excel's ribbon, formula bar, Name Box, sheet tabs, keyboard shortcuts, fill
 handle, point-mode formula entry with coloured references, Format Cells, Paste Special,
 conditional formatting, tables, charts and more. If you know Excel, you already know GridCraft.
- **Compatible.** XLSX is the native format: styles, themes, formulas (including dynamic arrays),
 tables, conditional formats, validation, comments, hyperlinks, charts, pictures, sparklines,
 PivotTables and print settings round-trip. CSV and TSV too.
 Excel 97-2003 `.xls` workbooks open with their values, formulas and number formats (formatting and objects not yet).
 [XLSB worksheet data can be imported](docs/xlsb-import.md), using saved values instead of formulas.
 [ODS worksheet data can be imported](docs/ods-import.md), using saved values instead of formulas.
 [Static pictures can live inside cells](docs/cell-pictures.md), fitting their size and moving with the data.
- **Capable.** A dependency-graph calculation engine with dynamic arrays and spilling,
 500+ worksheet functions plus LET, LAMBDA, MAP, REDUCE, SCAN, BYROW, BYCOL and MAKEARRAY,
 structured table references, Excel's full number-format language, sort and AutoFilter,
 Flash Fill, data validation, outlining and subtotals.
- **Fast.** Copy-on-write workbooks (undo snapshots are nearly free), incremental recalculation,
 and a virtualised grid that only lays out what's on screen.
- **Agent-native.** Every ribbon button, menu item, dialog, keystroke and mouse gesture is a
 command that agents can run over a JSON control channel, an **MCP server**, or the CLI.
- **Everywhere.** One Rust codebase for desktop and the web. No subscription, no licence server,
 no telemetry.

## Quick start

```sh
cargo run --release -p gridcraft # desktop app
cargo run --release -p gridcraft -- --sample sales # open a sample (sales, budget, grades)
cargo run --release -p gridcraft -- book.xlsx # open a workbook
cargo run --release -p gridcraft -- --sample sales --control 7979 # + JSON control channel
cargo xtask ci # fmt, clippy, tests, assets, layering, wasm
```

Choose Español under View → Interface language for [Spanish formula names, decimal commas, and semicolon arguments](docs/formula-input.md).
Workbooks, clipboard exchange, and programmatic APIs retain canonical English syntax.

### Web

```sh
cd apps/gridcraft-web && trunk build --release # → dist/web (serve it with any static server)
cd apps/gridcraft-web && trunk serve --release # http://127.0.0.1:8771 (?sample=sales opens a sample)
```

You need [trunk](https://trunkrs.dev) and the `wasm32-unknown-unknown` target. Open uses the
browser's file picker (dropping files works too) and Save downloads the workbook.

### Ribbon access keys

Press and release **left Alt** on Windows/Linux/BSD, or press **F10** on any platform,
then type a sequence below one key at a time. Keytips appear on the supported Home
controls and menu items. On macOS, use F10 (Fn+F10 if required by your keyboard); Option
remains available for entering accented characters.

| Sequence after Alt/F10 | Action |
|---|---|
| `H A L` / `H A C` / `H A R` | Align left / center / right |
| `H V S` or legacy `E S` | Open Paste Special |
| `H O I` or legacy `O C A` | AutoFit selected columns |

In Paste Special, **T/V/F/C** select formats/values/formulas/comments, and **E** toggles
Transpose. **Enter** applies the selected options; **Escape** cancels the dialog.
These letters also work with Alt held on Windows/Linux/BSD.

Escape backs out one keytip level; Alt/F10 again exits keytips. Clicking, scrolling,
or switching windows cancels navigation. Access keys do not start while editing text
or using another dialog. This is initial support for these Home and legacy paths;
other ribbon commands and full mouse-free navigation remain to be implemented.
Browsers or desktop environments may reserve Alt/F10 for their own menus.

### Logs

The desktop app writes its log to standard error and to `gridcraft.log` in the `logs` folder
next to its settings: `~/.config/gridcraft/logs` on Linux and BSD (`$XDG_CONFIG_HOME/gridcraft/logs`
when set), `~/Library/Application Support/GridCraft/logs` on macOS and
`%APPDATA%\GridCraft\logs` on Windows. Each start moves the previous log to `gridcraft.1.log` and
that one to `gridcraft.2.log`, so the log of a run that crashed survives the next start; att