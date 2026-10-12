SCSKiller 

 Shader Compilation Stutter Killer. SCSKiller compiles your games' shaders into your GPU driver's
 cache before you play, so the game doesn't stop to compile them mid-game. Free and open source, for Windows.

 Website 
 ·
 Download 
 ·
 Patreon 
 ·
 Discord 
 ·
 X 
 ·
 Report a bug 
 ·
 Request a game 

> [!WARNING]
> The only official downloads are this repository's [Releases](https://github.com/BlueHeisenberg/SCSKiller/releases).
> See [official links](#official-links) for the accounts and sites that belong to SCSKiller.

## Why

A game that meets a new effect has the GPU driver compile its shader on the spot, and the frame waits: that's shader
compilation stutter. SCSKiller reads the shaders a game ships with, works out the pipelines it will build, and compiles
them into the driver's cache ahead of time, in its own process with the game closed.

## Results

About 5 minutes of play per game, from a cold driver cache and after compiling with SCSKiller. A stutter is a shader
compile the game waited 20 ms or more for.

 Game GPU Measurement Cold With SCSKiller 
 Final Fantasy VII Rebirth NVIDIA RTX 5090 Stutters (≥ 20 ms) 19 0 
 Worst stall 76 ms 5 ms 
 AMD Ryzen AI Max+ 395 (Strix Halo) Stutters (≥ 20 ms) 162 0 
 Worst stall 291 ms 7 ms 
 Silent Hill: Townfall NVIDIA RTX 5090 Stutters (≥ 20 ms) 24 0 
 Worst stall 347 ms 8 ms 
 Hogwarts Legacy NVIDIA RTX 5090 Stutters (≥ 20 ms) 1,014 87 
 Worst stall 2,400 ms 100 ms 
 AMD Ryzen AI Max+ 395 (Strix Halo) Stutters (≥ 20 ms) 27,743 206 
 Worst stall 2,146 ms 104 ms 
 Tiny Tina's Wonderlands NVIDIA RTX 5090 Stutters (≥ 20 ms) 583 0 
 Worst stall 315 ms 13 ms 
 Star Wars Jedi: Survivor NVIDIA RTX 5090 Stutters (≥ 20 ms) 9,038 11 

Measured with SCSKiller's recorder. Your numbers depend on the game, GPU and driver. SCSKiller fixes shader compilation
stutter only, not traversal or streaming stutter, and a shader it couldn't find or record can still compile in game.

## Features

- **NVIDIA and AMD**, DirectX 12 games, and DirectX 11 games on NVIDIA.
- **Finds your games** in Steam, Epic Games, EA app, GOG, Ubisoft Connect, Xbox (PC), Battle.net, PURPLE, HoYoPlay and
 Gaijin, plus games you add yourself.
- **Puts games known to stutter on top**, with the reason, and marks games whose engine prepares its shaders itself.
- **Compiles again after a driver update**, which clears the shader cache, on its own if you let it.
- **Optional recorder** for games whose pipelines its files don't give: play a few minutes with it on, then compile. It
 also records alongside a mod that replaces shaders.
- **Frame times per session**: with the recorder on, a game's page graphs your last session and marks shader stutters
 apart from other hitches. They stay on your PC.
- **Play button** that starts the game through its store.
- **Community shader hash database** for Patreon supporters: other players' recordings, so your games are covered
 without recording them first. Sharing yours is opt-in, anonymous and hash-only.
- **Leaves anti-cheat games alone** beyond reading their files: no launching, no injecting, no recorder. The one
 exception is opt-in per game and confirmed every time: an offline session without EasyAntiCheat for ELDEN RING and
 ARMORED CORE VI, at your own risk.

## Install

| Requirement | |
|---|---|
| OS | Windows 10 (version 2004) or 11, 64-bit |
| GPU | NVIDIA or AMD |
| Games | DirectX 12, DirectX 11 on NVIDIA |

Intel GPUs aren't supported yet: I don't have one to test on. If you'd like to sponsor an Intel Arc GPU, get in touch at
[contact@scskiller.com](mailto:contact@scskiller.com).

Download `SCSKiller-Setup.exe` from [Releases](https://github.com/BlueHeisenberg/SCSKiller/releases/latest) and run it.
It installs for your user only, needs no admin rights and updates itself.

Or unzip `SCSKiller- -Portable.zip` to any folder you can write to and run `SCSKiller.exe`. It updates itself
too, and keeps its settings and data in a `data` folder beside the exe. Turn recording off for your games before you
delete the folder, so the recorder leaves the game folders.

> [!IMPORTANT]
> **Releases aren't code-signed yet**, so the first run will probably show SmartScreen's "Windows protected your PC".
> Click **More info**, then **Run anyway**. Updates never show it. Signing through the SignPath Foundation is in
> progress. To check a download, compare its SHA-256 with the one in the release notes (PowerShell:
> `Get-FileHash `). Smart App Control (Windows 11) blocks unsigned apps outright: if it's on, wait for a signed
> release.

## How to use it

1. **Open SCSKiller.** It finds your games and the shaders they ship with.
2. **Queue games and press Compile.** "Add all recommended" is a good start. Keep the game closed while it compiles.
3. **Play**, from your store or with the Play button. SCSKiller can be closed. Left open, it checks that the compile
 reached the cache the game really uses, and with the recorder on, the game's page shows your session's frame times
 and anything that still compiled.

If a game needs a recording, turn on **Record**, play it for a few minutes, then compile it.

## FAQ

**Can I get banned?** SCSKiller only reads the files of games with anti-cheat and never adds its recorder to them. Its
anti-cheat check can still miss a game, so you use SCSKiller at your own risk, and its authors are not responsible for
bans, crashes or lost data.

**Is it safe with anti-cheat games?** SCSKiller never launches them, injects into them or gives them the recorder. It
only reads their files. The exception is the offline session for ELDEN RING and ARMORED CORE VI, which run offline
without EasyAntiCheat when their exe is started directly. You allow it per game and confirm every launch, at your own
risk. Steam must be running (offline mode is fine). SCSKiller adds `d3d12.dll`, `scskiller.ini`, `scskiller.armed` and
`steam_appid.txt` to the game's folder and starts the exe itself, and the recorder records only that process. When the
ga