# disktree

Find what is filling a disk, mark what should go, and remove it — with the
volume's free space in view the whole time.

disktree is a treemap for Omarchy. It scans your home directory by default,
draws every directory as a nested mosaic sized by what it really costs on disk,
and lets you walk into it with the keyboard or the mouse. Mark as much as you
like; nothing happens until you review the list and commit, and the permanent
path always asks first.

Built with [GPUI](https://gpui-kit.com/) through
[gpui-omarchy](https://github.com/huacnlee/gpui-omarchy), so it follows your
Omarchy theme and behaves like the rest of the desktop.

## Install

Download `disktree-*-x86_64-linux.tar.gz` (`aarch64-linux` on ARM) from the
[latest release](https://github.com/tobi/disktree/releases/latest), unpack
it, and run `./install.sh` inside (or just copy `disktree` onto your
`PATH`). Or build it:

```sh
git clone https://github.com/tobi/disktree
cd disktree
make install
```

`make install` builds a release binary and puts three things under `~/.local`
(no root needed):

- `~/.local/bin/disktree`
- a desktop entry, so disktree is in the launcher and in a file manager's
 **Open with** for a directory (it adds a handler; it never becomes the
 default)
- an icon

`sudo make install PREFIX=/usr/local` installs system-wide; `make uninstall`
removes exactly what was installed.

On Arch, including Omarchy, disktree is in the AUR:
[`disktree`](https://aur.archlinux.org/packages/disktree) builds each release
from source, and
[`disktree-bin`](https://aur.archlinux.org/packages/disktree-bin) installs
the release binary:

```sh
yay -S disktree-bin
```

You need Rust 1.97 or newer and a Wayland or X11 session with a GPU that GPUI
can drive (Vulkan). Distributions often package an older Rust;
[rustup](https://rustup.rs) installs a current one. The repo pins 1.97 in
`rust-toolchain.toml`, so with rustup the right toolchain is fetched on the
first build even if `rustup default` points at something older.

### macOS

Download `disktree-*-aarch64-macos.zip` (`x86_64-macos` for an Intel Mac)
from the [latest release](https://github.com/tobi/disktree/releases/latest),
unzip it, and drag `disktree.app` into Applications. macOS 11 or newer.

A release that was not signed and notarized is stopped by Gatekeeper: macOS
says it "is damaged and can't be opened" or "cannot be verified". The app is
fine; the browser marked the download as quarantined. Clear the mark once:

```sh
xattr -dr com.apple.quarantine /Applications/disktree.app
```

(Or open it once, then choose **Open Anyway** in System Settings › Privacy &
Security.)

Or build it, with Rust 1.97 or newer and Xcode or its Command Line Tools.
macOS does not come with Rust; install it with [rustup](https://rustup.rs).

```sh
make install # ~/Applications/disktree.app, and ~/.local/bin/disktree
make uninstall
```

To see everything, give disktree **Full Disk Access** in System Settings ›
Privacy & Security (the panel offers a button when it is missing), then
reopen it. Without it macOS hides Mail, Messages, Safari, other apps' data
and the Trash, and disktree counts them as unreadable. Started from a
terminal, it is the terminal that needs the access. macOS also asks once
each for Desktop, Documents and Downloads.

What is different from Linux:

- **Free space** is what `df` reports. Finder's figure is larger: it counts
 purgeable space (caches and local snapshots macOS will clear on its own).
- **Cloned files** (copies APFS shares blocks between, as Finder's Duplicate
 makes) are each counted in full, so a total can exceed what deleting them
 frees.
- **Time Machine's local snapshots** are not files and do not appear; they
 are part of the gap between the scan and the disk's used space.
- **Cloud-only folders** (iCloud Drive, Dropbox and the like, evicted to the
 server) are not opened, so a scan never downloads them.

To sign and notarize a build for others, with a Developer ID certificate in
the keychain and credentials saved by `xcrun notarytool store-credentials`:

```sh
NOTARY_PROFILE= cargo xtask bundle \
 --sign "Developer ID Application: Name (TEAMID)" --notarize
```

### Windows

On Windows 10 or 11, download `disktree-*-x86_64-windows.zip`
(`aarch64-windows` on ARM) from the same release, unpack it anywhere and run
`disktree.exe`. Or build it with Rust 1.97 or newer, from
[rustup](https://rustup.rs), and the MSVC toolchain (Visual Studio Build
Tools, C++ workload):

```powershell
git clone https://github.com/tobi/disktree
cd disktree
cargo build --release # target\release\disktree.exe
```

See [On Windows](#on-windows) for what differs there.

## Use

```sh
disktree # scan the home directory
disktree --disk # the whole disk it lives on
disktree ~/src # or any directory
disktree --help # options: apparent size, follow links, skip hidden, …
```

### The screen

- **Top:** the trail from `/`, then what is measured — **Size**, **Files** or
 **Age**, **Hidden files**, **Apparent size**, and the depth drawn. In the
 tree a crumb goes there, and its ▾ lists its siblings, largest first with
 their share and size, to jump sideways (arrows and Enter work too). Above
 the scanned root a crumb is dimmer, and clicking it widens the scan to
 there (see below).
- **Under it:** the scan totals, the filter when one is typed, and the legend.
- **Mosaic:** colour is the *kind* of data — code, agent scratch,
 toolchains, synced files, git, media, documents, caches — at one muted
 level, lighter with depth. A diagonal hatch is space that can be had back
 (caches, sync history, package stores, build output), independent of
 colour. Top-level directories carry a strip of their colour and a name
 band; deeper open directories a slim label row. In **Age** mode colour is
 the last write instead, from this week to older.
- **Panel:** the selection (its size set large, share of the scan, files,
 last write, and for a checkout what git says — changes, stashes, unpushed
 commits); *W