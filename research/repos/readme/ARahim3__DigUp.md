DigUp 

 Describe it. Dig it up. 
Search the files on your computer by what's in them, with Google DeepMind's
 EmbeddingGemma 2 . 

 Download for Mac ·
 Windows (beta) ·
 Linux (beta) 
 Free and open source. Everything runs on your computer. 

EmbeddingGemma 2 is the multimodal embedding model Google DeepMind released in October 2026. It puts text, images,
audio and video into one shared space: a photo of a dog on a beach lands next to the words "a dog on the beach", and a
recording of someone talking about sleep lands next to "where they talk about sleep". It understands more than 100
languages, it's open (Apache 2.0), and at 740M parameters it's small enough to run on a laptop.

DigUp brings that to the files on your computer, on a Mac, on Windows or on Linux. Pick the folders to search, and it
reads the pictures, PDFs, documents, recordings and videos in them. Then describe what you're looking for, in your own
words, and it finds the match, whatever kind of file it is.

## What you can find

- "zebra in a video" opens the clip at the moment the zebra shows up
- "where they talk about sleep" jumps to that minute of a podcast
- "the clause about pets in the lease" shows the PDF page
- "a dog on the beach" finds the photo, and "payment declined error" the screenshot
- a search in English can find a note written in Bengali, Arabic or any of the model's 100+ languages, and the other
 way around
- "code: retry a failed call with backoff" finds the function in your projects, if you turn on code search

Exact words count too. Invoice numbers, error codes and names are matched as written, in file names and document text,
so a search gets both the meaning and the exact string. On a Mac that includes the text inside screenshots.

## Private

Nothing you index leaves your computer. DigUp goes online only to download the model once and to check for updates
once a day. The update check sends nothing about your files, and you can turn it off. No account, no telemetry.

## Install

**Mac.** Download the DMG from [Releases](https://github.com/ARahim3/DigUp/releases/latest) and drag DigUp to
Applications, or use Homebrew: `brew install --cask arahim3/tap/digup`. It needs an Apple Silicon Mac with macOS 14 or
later.

**Windows.** Download `DigUp_x.y.z_x64-setup.exe` from the
[beta release](https://github.com/ARahim3/DigUp/releases/tag/v0.7.0-beta.2) and run it. It installs for you only, with
no admin rights. Windows may say it doesn't recognize the app, because the installer isn't signed yet: choose More
info, then Run anyway. It needs 64-bit Windows 10 or 11.

**Linux.** On Ubuntu, Debian, Mint and the like, download the .deb and install it:

```sh
sudo apt install ./DigUp_x.y.z_amd64.deb
```

The package is called `dig-up`, because Debian already has an unrelated `digup`. Anywhere else, download the
AppImage, make it executable and run it. Both are for 64-bit Intel and AMD processors and work on Ubuntu 22.04,
Debian 12, Mint 21 and newer.

Then, on any of them:

1. Open DigUp. While the model downloads (865 MB, once), pick the folders to search: whole folders, or only some of
 their subfolders. DigUp shows how long the first pass will take for each, measured on your computer.
2. Press the shortcut in any app and describe what you're looking for: **⇧⌘Space** on a Mac, **Ctrl+Shift+Space** on
 Windows and Linux.

DigUp keeps itself up to date: the Mac app, the Windows installer and the AppImage install updates with one click.
With the .deb, DigUp tells you when there's a new version and opens its release page.

## Using it

| Mac | Windows and Linux | What it does |
|---|---|---|
| ⇧⌘Space | Ctrl+Shift+Space | Opens the search panel from any app (you can change it) |
| ↓ ↑ | ↓ ↑ | Moves through the results |
| ↩ | Enter | Opens the result: PDFs at the page, recordings and videos at the moment, code in your editor at the line |
| Space | Space | A big preview, at the page or moment (once you've moved to a result) |
| ⌘↩ | Ctrl+Enter | Shows it in Finder, Explorer or your file manager |
| ⌘C | Ctrl+C (in the window) | Copies the file, to paste anywhere |
| ⌘O | Ctrl+O | The same search in a bigger window, with a picture grid and filters |

DigUp lives in the menu bar on a Mac and in the tray on Windows and Linux, where you can see how indexing is going,
pause it, or open Settings. Opening it from the Start menu or your app list shows the search window.

A few things differ by system:

- On a Mac, a video opens at its moment in QuickTime Player (macOS asks once whether DigUp may control it) or IINA,
 and a PDF opens in Preview with your words in its search. On Windows and Linux, PDFs open at the page in your PDF
 viewer if it's one that can be told a page (Edge, Chrome, Firefox, Acrobat, SumatraPDF, Evince, Okular), and
 recordings and videos at the moment in VLC, mpv or MPC-HC. Other apps open the file from the start; the big
 preview plays it from the moment either way.
- On GNOME and KDE under Wayland, which don't let apps set their own shortcuts, DigUp adds Ctrl+Shift+Space to the
 desktop's keyboard settings during setup, and you change it there. On other Wayland desktops, Settings shows the
 command to give a shortcut of your own.
- On GNOME, the tray icon needs the AppIndicator extension, which Ubuntu includes. Without it, the window's ⋯ menu has
 the same items.

## What it reads

Only the folders you choose:

- pictures and screenshots (JPEG, PNG, HEIC, WebP and more), by what they show, and on a Mac screenshots by their text
 too
- PDFs, page by page, scans included. A long one gets its first 30 pages right away and the rest once everything
 else is in (up to 5,000 pages a file)
- documents: txt, md, rtf, docx, odt, html, and on a Mac doc, long ones the same way. Text that's mostly numbers,
 like a data export, is matched by its exact text only
- audio of any length: the model listens to 30 seconds at a time, so DigUp takes overlapping 30-second windows and a
 match points to its moment
- video o