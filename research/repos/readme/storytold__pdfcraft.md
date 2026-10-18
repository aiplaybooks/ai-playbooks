PdfCraft 

 The PDF workbench; an open-source, clean-room reimplementation of Adobe Acrobat, rebuilt in pure Rust. 
 Read, organize, combine, split and secure PDFs in a fast, native app, written in Rust from the ground up. 
 macOS · Windows · Linux · FreeBSD · the web

 PdfCraft on getartcraft.com ·
 ArtCraft ·
 All Crafting Apps 

 The PdfCraft Showcase, a 13-page specimen PDF, open with the All tools panel and threaded comments. 

> [!NOTE]
> **ArtCraft is a community of artists from all walks of life.** Digital, generative, music,
> games &mdash; if you make things, you're one of us. **[Come say hi on Discord](https://discord.gg/artcraft).**

 Highlights ·
 Read ·
 Find ·
 Organize ·
 Combine &amp; split ·
 Protect ·
 Forms &amp; layers ·
 Everywhere ·
 Agents ·
 How it's built ·
 Get started ·
 What's next ·
 Downloads ·
 Crafting Apps 

---

## Community

PdfCraft is part of [ArtCraft](https://getartcraft.com). Come say hello, get help and follow development:

- **Discord: [discord.gg/artcraft](https://discord.gg/artcraft)**. This is the fastest way to get help and share feedback. The app has a Discord button in its title bar.
- **Web page:** [getartcraft.com/apps/pdfcraft](https://getartcraft.com/apps/pdfcraft)
- **Source:** [github.com/storytold/pdfcraft](https://github.com/storytold/pdfcraft)

The ArtCraft name and logos in `docs/brand/` are trademarks of the ArtCraft Team and are not open source. They may be used only unmodified, and only as part of PdfCraft (see `docs/brand/LICENSE-brand.txt`). Forks and modified versions must remove them.

## Highlights

### Faithful
Real-world typography: world scripts, vertical Japanese, colour emoji, gradients, soft masks and transparency. All of it renders the way the author intended.

### Fearless
Every save appends your changes and leaves the original bytes untouched. Writes are atomic, undo runs deep, and nothing is lost if you close by mistake.

### Yours
No account, no telemetry, no cloud. It works offline and opens instantly. The engine, CLI and app are all open source.

---

## Read anything, beautifully

PdfCraft renders PDFs with care for the details that make a page feel right: kerning and ligatures, right-to-left and complex scripts, vertical CJK, colour emoji, shadings, blend modes, soft masks and optional content.

 Twelve writing systems on one page, plus vertical Japanese, at 125%. 

- **Deep zoom stays sharp.** Large pages render in tiles, so text stays crisp at any magnification.
- **Built to survive bad files.** Every page renders in isolation and damaged documents are repaired. Across the 983-file pdf.js test corpus the result is 0 crashes.
- **Layouts for every task:** continuous, single page, two-up, view rotation, full screen and a distraction-free Read mode.
- **Light and dark themes**, both designed to be easy on the eyes for long sessions.

 Two-up Read mode, ready for long reading 
 The dark theme, with the comments panel open 

## Find it, select it, copy it

Search the whole document as you type, step through matches with ⌘G , and select text that comes out in the right reading order. That holds for columns, right-to-left runs and CJK too.

## Navigate long documents

Right-click a PDF tab to close it, reopen the last closed file-backed tab, or reveal its file. Closing still asks about unsaved changes. Reopening reads the saved file from disk; it does not restore discarded edits. Reveal selects the file in Explorer or Finder. On Linux and FreeBSD it requests `org.freedesktop.FileManager1.ShowItems`, falling back to opening the containing directory with `xdg-open` when that service is unavailable. Reopen and Reveal are unavailable on the web; Reveal is also unavailable for pathless documents.

Bookmarks, page thumbnails and the document's own page labels (i, ii, 1, 2…) keep you oriented in long documents. Search bookmark titles in the Bookmarks panel to find nested entries even when their parents are collapsed. Matches keep their ancestors for context; Clear restores the unfiltered tree without changing its expansion state.

 Find as you type: match 10 of 16 
 Nested bookmarks with the document's own page labels 

---

## Organize pages like cards on a table

Open **Organize pages** to see every page at once:
- **Select pages:** click, ⌘ -click or ⇧ -click.
- **Change them:** rotate, delete, insert blank pages, insert pages from another file, and move them earlier or later.
- **Undo anything:** ⌘Z , then save.

 Organize pages with three pages selected and the page tools in the toolbar above. 

**Undo that goes the distance.** Each change is one step in a history you can walk backwards and forwards. The Edit menu names the step ("Undo Rotate pages"), and undo still works after you save.

**Saves you can trust:**
- *Incremental:* the original bytes stay byte-for-byte intact.
- *Atomic:* the file is written to a temporary copy, then swapped in.
- *Verified:* independently checked with qpdf, on every CI run.

When open documents exceed the window width, scroll over the tab strip with the mouse wheel or trackpad, or use its horizontal scrollbar. Opening or switching to a document brings its tab into view.

Unsaved documents carry a dot on their tab, and closing or quitting asks before anything is lost. Changes are autosaved every minute. If PdfCraft ever quits unexpectedly, it offers to recover your work the next time it opens. Encrypted documents stay encrypted on disk.

 Split document: one page per file makes 13 files. 

## Combine and split without losing a thing

**Combine files** merges any number of PDFs into one. Each file gets a bookmark, with its own bookmarks nested underneath.

**Extract** copies the pages you select into a new document. **Split** divides a document every *n* pages, or before the pages you choose.

Nothing quietly disappears along the way:
- links and named destinations are rewired to the copied pages;
- form fields stay interactive;
- layers keep their on/off defaults;
- attachments come