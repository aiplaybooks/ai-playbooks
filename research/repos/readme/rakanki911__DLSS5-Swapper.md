DLSS 5 Swapper 

 Install and manage DLSS 5 Neural Rendering for compatible games and emulators.

## Download

[**Windows Installer**](https://github.com/rakanki911/DLSS5-Swapper/releases/latest) ·
[**Portable**](https://github.com/rakanki911/DLSS5-Swapper/releases/latest) ·
[Checksums](https://github.com/rakanki911/DLSS5-Swapper/releases/latest)

Both are on the latest release page, with `SHA256SUMS.txt` beside them.

## Features

- **Easy installation:** native DLSS games, or compatible non-DLSS games through DLSS5-Feeder.
- **Your library:** Steam, Epic, GOG, modern Xbox Game Pass folders, and manually added games/emulators.
- **Search and filters:** combine title, graphics API, DLSS status/version and add-ons; click counters to filter.
- **Flexible layout:** group by store or show everything in one list, with game artwork and light/dark themes.
- **Controlled scanning:** full-drive scanning is **off by default**. Added folders still scan normally; enable all-drive discovery or remove scan folders in Settings.
- **Right-click shortcuts:** open/copy folder, rescan, change cover, restore originals or hide a game.
- **Backups and History:** restore original files, keep installation records, and copy History/activity/install logs.
- **Save diagnostics:** one file with the install log, the game’s own ReShade and Feeder logs, the manifest and your driver - shown to you before it is written, and ready to attach to a report.
- **In-game overlay:** press **F8** to open the app's own panel over the running game and move the real DLSS Neural Rendering sliders while you play. Supports the **DLSS5-Feeder** and **RenoDX** routes only, and it knows both RenoDX builds the app ships (6.5.3 and the older 4.7). Drag the grip in its bottom right corner to resize it; each game remembers its own size.
- **Rendering API override:** optional, per game, with **Automatic** as the default; detection is never overwritten.
- **Custom add-ons:** the Add-ons page remains available alongside the integrated installation routes.
- **Multipass neural rendering:** an installation route that runs the neural pass up to ten times per frame, on DX12, DX11 and 64-bit DX9 - including games with no DLSS of their own.
- **Community (BETA):** read what worked for other people, narrowed to the games on your PC and the graphics card in it, leave your own report, and talk it over underneath it. Opt-in, and everything you leave can be edited, deleted or withdrawn.
- **Community chat:** one live room for everyone using the app - screenshots, game cards, replies with mentions and reactions.

## New in 2.2.9

Four faults from the tracker, fixed at the cause. Every one of them was reported by somebody in it.

| | |
|---|---|
| **The installer crashed before it opened** | On some machines the setup died instantly with `0xc0000005`, no window and no prompt, while the portable build was fine. The installer framework read past the end of a path Windows handed it. Fixed upstream, and this release is built with the fixed version ([#344]) |
| **Restore originals went dead with the files still in the game** | A finished restore renames the backup record aside, and everything that decides whether a game has anything installed read only the live one. The app now offers the newest retired record whose files are still in the game, and restores from the same backups ([#325]) |
| **dgVoodoo2 flagged by antivirus** | Upstream released 2.87.5 precisely because engines flag 2.87.4, and the app was pinned to 2.87.4 ([#390]) |
| **ReShade never started in a wrapped DirectX 8/9 game** | Inside dgVoodoo the game is a DirectX 11 one, and some setups load only `d3d11.dll`. The **ReShade file** choice is offered for these games now ([#343], [#374]) |

[#325]: https://github.com/rakanki911/DLSS5-Swapper/issues/325
[#343]: https://github.com/rakanki911/DLSS5-Swapper/issues/343
[#344]: https://github.com/rakanki911/DLSS5-Swapper/issues/344
[#374]: https://github.com/rakanki911/DLSS5-Swapper/issues/374
[#390]: https://github.com/rakanki911/DLSS5-Swapper/issues/390

## Earlier releases

Each one is written up in full - what broke, why, and what was changed.

| | |
|---|---|
| **2.2.8** | [A second theme, and every add-on brought current](docs/releases/v2.2.8.md) - a whole second design, DLSS5-Feeder 1.17.0, RenoDX 6.5.3, a second OptiScaler build per game, and ten faults fixed |
| **2.2.7** | [Find the reviews that matter to you](docs/releases/v2.2.7.md) - filter by your card, reviews for your games, notifications, and eight faults fixed |
| **2.2.6** | [Community chat](docs/releases/v2.2.6.md) - one live room for everyone, and the right add-on on every route |
| **2.2.5** | [Multipass](docs/releases/v2.2.5.md) - the neural pass up to ten times per frame, plus nine faults fixed at the cause |
| **2.2.4** | [The Community page](docs/releases/v2.2.4.md) - compare notes with everyone else, plus eight faults fixed at the cause |
| **2.2.3** | [Six reported faults, fixed at the cause](docs/releases/v2.2.3.md) - OptiScaler on older cards, a game's own stale shader compiler, the overlay on a scaled display |
| **2.2.2** | [The reports people sent](docs/releases/v2.2.2.md) - games it could not find, installs it refused, the overlay's own page |
| **2.2.1** | [The Overlay page](docs/releases/v2.2.1.md) - themes you can write yourself, and a preview that runs before you choose |
| **2.2.0** | [Optional OptiScaler and a smarter library](docs/releases/v2.2.0.md) |

Every release also carries its own notes and downloads on the
[releases page](https://github.com/rakanki911/DLSS5-Swapper/releases).

## Compatibility

| Category | Support |
| --- | --- |
| **System** | Windows 10/11 x64; compatible 32-bit and 64-bit games |
| **ReShade / Feeder GPUs** | RTX 20 / 30 / 40 / 50; older-series support is reported by the bundled modified runtime's author |
| **OptiScaler GPUs** | 64-bit games with native DLSS enabled. The bundled neural model runs on **Blackwell** (RTX 50 / RTX PRO Blac