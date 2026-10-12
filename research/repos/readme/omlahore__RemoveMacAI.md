# RemoveMacAI

Debloat macOS. Turn off Apple Intelligence and delete its models, stop the analytics and ads, quiet the pop-ups, switch off other apps' background updaters and get disk space back. You see every change before it happens, and every change can be undone.

 omlahore.github.io/RemoveMacAI 

Built on [pared](https://github.com/4evy/pared) by 4evy, who did the hard work first: mapping Apple's asset service, the model sets and the settings keys the Apple Intelligence part relies on.

[The Verge](https://www.theverge.com/ai-artificial-intelligence/1004672/mac-delete-apple-intelligence-ai-tool), [Ars Technica](https://arstechnica.com/apple/2026/10/command-line-tool-quickly-removes-apple-intelligence-from-macos-27/), [The Register](https://www.theregister.com/ai-and-ml/2026/10/05/get-rid-of-apples-ai-bloatware-and-reclaim-12-gb-of-storage-with-this-open-source-tool/5301213), [MacRumors](https://www.macrumors.com/2026/10/05/apple-intelligence-removal-tool-frees-mac-storage/), [AppleInsider](https://appleinsider.com/articles/26/10/05/dumb-down-your-mac-save-12gb-by-removing-apple-intelligence) and [Help Net Security](https://www.helpnetsecurity.com/2026/10/05/removemacai-turn-off-apple-intelligence/) have written about RemoveMacAI, and [Daring Fireball](https://daringfireball.net/linked/2026/10/06/cli-tool-removes-apple-intelligence-from-macos-27) linked to it.

## Install

### The app

Open Terminal (Applications > Utilities), paste this line and press Return:

```sh
curl -fsSL https://raw.githubusercontent.com/omlahore/RemoveMacAI/main/install.sh | bash -s app
```

It downloads the latest release, checks its SHA-256 checksum, puts RemoveMacAI in Applications and opens it.

To download it yourself instead, get `RemoveMacAI.zip` from the [latest release](https://github.com/omlahore/RemoveMacAI/releases/latest), unzip it and drag RemoveMacAI to Applications. The app is not notarized, so the first time you open it macOS says it can't verify it. Open System Settings > Privacy & Security, scroll down and click Open Anyway.

### The command line

```sh
curl -fsSL https://raw.githubusercontent.com/omlahore/RemoveMacAI/main/install.sh | bash
```

This runs the command-line version from a temporary folder and installs nothing. With Homebrew:

```sh
brew install omlahore/tap/removemacai
```

The app and the command line are the same program and share the same undo history.

## What it does

| Section | What you can turn off or change |
|---|---|
| Apple Intelligence | Siri, Writing Tools, Genmoji, Image Playground, ChatGPT, summaries in Mail, Messages, Safari, Notes and notifications, inline predictions, Spatial Photos, Photos Clean Up, Xcode predictive completion. The models are deleted and blocked from downloading again. Keep any feature you use. |
| Privacy | Mac Analytics, personalized ads, Improve Siri and Dictation, Improve Search, Spotlight internet results, Look Up suggestions, Safari search suggestions, Game Center |
| Annoyances | Clicking the wallpaper hiding every window, desktop widgets, the media keys, all Music launches (including AirPods; opt-in), iPhone Mirroring |
| Apple apps | Apple Music in the Music app, the Book Store, unused Apple apps in the Dock |
| Finder | File extensions, hidden files, the path and status bars, folders first, searching the current folder, the extension warning, `.DS_Store` files on network drives, emptying the Trash after 30 days, saving to your Mac instead of iCloud, the Library folder |
| Dock and windows | Recent apps, the auto-hide delay, bouncing icons, minimizing into the app icon, window animations, gaps between tiled windows, screenshot shadows |
| Typing | Autocorrect, smart quotes and dashes, the double-space period, automatic capitals, the accent menu on held keys |
| Background items | Updaters and helpers other apps install, such as Google's updater, shown with what they run and switched off one by one |
| Storage | Old macOS installers, aerial wallpaper videos, iPhone and iPad update files, Xcode build data and device support, unavailable simulators, app caches, Time Machine local snapshots, and Apple's optional apps (GarageBand and its sound library, iMovie, Keynote, Numbers, Pages) |

Two presets get you started. **Recommended** turns Apple Intelligence, analytics and ads off and removes the pop-ups, and leaves alone anything you rely on. **Maximum privacy** adds Game Center and Safari's search suggestions. Both add to what is already applied, and nothing changes until you review it.

## Command line

| Command | Description |
|---|---|
| `removemacai` | Show the state of Apple Intelligence, then turn it off |
| `removemacai status` | Show each Apple Intelligence feature and the size of its models |
| `removemacai off --keep ` | Turn Apple Intelligence off but leave the listed features on |
| `removemacai on` | Turn Apple Intelligence back on and keep the other changes |
| `removemacai tweaks` | List every tweak and whether it is applied (`--json` for scripts) |
| `removemacai apply ` | Apply tweaks by name |
| `removemacai apply --preset recommended` | Apply a preset, Apple Intelligence off included |
| `removemacai undo ` | Undo tweaks by name |
| `removemacai background` | List other apps' background items; `off` or `on` with their labels |
| `removemacai clean` | Show the space you can get back; name items to move them to the Trash |
| `removemacai export ` | Write the configuration profile for an MDM |
| `removemacai revert` | Undo everything RemoveMacAI changed |
| `removemacai app` | Open the app |

`apply`, `undo`, `background` and `clean` show the change first and ask. `--dry-run` shows it and stops, and `--yes` skips the question.

 Demo video 

## For Mac admins

`removemacai export` writes the same configuration profile the app installs, so you can deploy it with Jamf, Kandji, Intune or any other MDM:

```sh
removemacai export RemoveMacAI.mobileconfig --preset recommended
removemacai export AI-off.mobileconfig --keep wri