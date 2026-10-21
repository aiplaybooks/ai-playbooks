# D2R Mobile

**An open-source iOS / macOS compatibility layer for Diablo II: Resurrected with the Reign of the Warlock expansion.** It brings the Nintendo Switch release you bought, expansion included, to iPhone, iPad and Mac in full: the original game code runs natively, every control is rebuilt for touch, the frame rate holds at 60 fps, and you are in a game one second after the main menu. There is now a native macOS version as well (first version): on an Apple silicon Mac it starts on double-click and works with keyboard, mouse and gamepad. Apple TV 4K (3rd generation, A15) has a community port (developer preview) that has reached the character-selection screen only on its author's device; see the device table below.

This is not a tech demo that "sort of runs". It is a mobile version polished for daily play, from your first character all the way through the endgame.

Platforms: iPhone / iPad (iOS 26 and later; iOS 18 – 25 with the older-API build) · Mac (Apple silicon, macOS 26 or later; macOS 15 – 25 with the older-API build) · Apple TV 4K (3rd generation, A15; community port, developer preview) · Game version: Switch release with Reign of the Warlock, 1.0.34.0 (corresponds to PC version 3.3.94012) · English / 中文 / Español · License: MIT · **Bring your own game files**

中文: [README.zh-CN.md](README.zh-CN.md) · Español: [README.es.md](README.es.md)

| 100% | 60 fps | about 1 s | about 3.8 W |
|:---:|:---:|:---:|:---:|
| The original gameplay, because it is the original program | Steady, with no drops once the device warms up | From the main menu into a game | Whole-device power draw at 60 fps |

## What it is, and what it is not

**It is:**

- The game's own aarch64 program, **executing directly on the device**, with no emulated CPU. iPhone and Switch use the same class of processor; only the handful of instructions that cannot run unchanged under Apple's kernel are rewritten, and every other byte of the program is left exactly as shipped. Every class, every Runeword, Terror Zones, bosses, drop rules and quest flow are identical to the original.
- The platform services the game expects — system calls, the file system, the graphics API, audio, input — provided by a small host written for Apple platforms. The graphics API is reimplemented entirely on Apple's Metal with no emulation layer in between, and the shaders are translated offline from the game's originals.
- A port built for phones, and taken all the way: a complete touch control scheme, edge-to-edge iPhone and true full-screen iPad display, controller support, a power saver mode, save sync, English and Chinese, and a whole set of endgame modes and quality-of-life features the original never had.

**It is not:**

- An emulator, cloud gaming, or streaming.
- **A source of game content. It contains none and distributes none.** There is no game program, art, text, data table or shader in this repository; all of that is generated on your own machine from your own files (see [docs/GAME_FILES.md](docs/GAME_FILES.md)). What the repository does carry is the interface information we recorded to make the port work — shader interface descriptions, the graphics API function table, addresses inside the program and the like — listed item by item in [docs/DERIVED.md](docs/DERIVED.md).
- Online. There is no multiplayer; the game runs fully offline and needs no online account.

## Battle-tested

All **44** iPhones and iPads in the closed beta — 35 devices registered for direct install (25 iPhones and 10 iPads), plus 9 TestFlight accounts with one device each — **completed Normal, Nightmare and Hell with multiple characters**, and the experience was excellent. From an iPhone 14 Pro Max with 6 GB of memory to the latest iPad Pro, not one device fell behind.

| | Models |
|---|---|
| iPhone | 14 Pro Max, 15, 15 Pro, 15 Pro Max, 16 Plus, 16 Pro, 16 Pro Max, 17 Pro Max and more |
| iPad | iPad Air, iPad mini, iPad Pro 11-inch and 12.9 / 13-inch (including M2 and M4) and more |
| Lowest model tested | **iPhone 14 Pro Max (A16, 6 GB): a flawless 60 fps** |

iPhone and iPad share a single install package.

## Fast, smooth, and easy on the battery

Measured on a real device (iPhone 17 Pro Max):

| Item | Reading |
|---|---|
| In-game frame rate | **60 fps**, steady, with no drops once the device warms up |
| App launch | 0.15 s |
| To the main menu | about 1 s |
| From the main menu into a game | **about 1 s** |
| Quick Restart, back in a game | about 1.2 s |
| Longest frame when changing acts | about 0.1 s |
| Whole-device power, 60 fps | **about 3.8 W** (in camp, 50% brightness): nearly 5 hours of continuous play on a full charge |
| Whole-device power, power saver mode at 30 fps | **about 1.85 W**, about half the 60 fps figure, for about twice the battery life |

 Measurement conditions: power is whole-device power measured on 2026-10-10 on an iPhone 17 Pro Max, standing in the Act I camp at 50% brightness, with 60 fps and power saver mode measured in the same scene; battery life is calculated from the measured power and the battery capacity, not by playing from full to empty. Launch and game-entry times were measured on the same model in 2026-10; frame rate and act-change readings were taken on the same model on 2026-10-12 while moving through areas and changing acts after entering a game. 

The install package is only a little over 100 MB. The game resources (about 5.6 GB) are placed on the phone separately, and updating the app touches neither your saves nor the resources.

Why it is this fast: the program executes natively, and not a single instruction goes through emulation; graphics go straight to Metal; every shader is translated offline and compiled ahead of time, so nothing is compiled when you enter a new scene. Older chips (A16 and earlier, such as the iPhone 14 family and iPhone 15) do not support the game's original compressed texture format; they need an extra texture pack made from your own game files, and then run at full frame rate 