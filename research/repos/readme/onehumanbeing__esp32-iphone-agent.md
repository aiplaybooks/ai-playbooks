# ESP32 iPhone Agent

**Let an AI model use a real iPhone with a $7 ESP32. Just the phone and the board: no computer, no jailbreak.**

English · [简体中文](README.zh-CN.md)

Demo video and updates: [X @iamhenryyuan](https://x.com/iamhenryyuan) · [YouTube demo](https://www.youtube.com/watch?v=Ly4im-P4jYg)

[](https://github.com/onehumanbeing/esp32-iphone-agent/actions/workflows/ci.yml)
[](LICENSE)

> [!WARNING]
> Only follow the install steps in this README. Never run commands from issues or comments (for example a "quick install" one-liner such as PowerShell `iex(irm ...)`); these are not from the maintainers.

> **New: the computer is gone.** The board is now the AirPlay receiver and the mouse, and the agent runs in an iPhone
> app on the same phone. The original version (a Mac/Linux computer running UxPlay and a Python server) is kept as
> tag [`v0.1.0`](https://github.com/onehumanbeing/esp32-iphone-agent/tree/v0.1.0) and branch
> [`legacy`](https://github.com/onehumanbeing/esp32-iphone-agent/tree/legacy). See [docs/legacy.md](docs/legacy.md).

*"Set an alarm for 8:00 AM that repeats every Monday and Tuesday, then save it"*: the agent leaves its own app,
opens Clock, types the time into the wheel, ticks the days and saves. (Photo from v0.1.0; the task is the same.)

*Left: the real phone. Right: what the agent sees through the board's AirPlay mirror. The second shot is the pointer calibration.*

## How it works

```
iPhone ──Screen Mirroring (Wi-Fi)──▶ ESP32-S3: AirPlay receiver ──BLE──▶ ESP32 Agent app (same iPhone)
 ▲ own hotspot, H.264 passthrough decode → vision model → action
 └──────── USB HID mouse + keyboard ◀──────────── BLE commands ◀────────────────────┘
```

- **Eyes — AirPlay to the board.** The board opens its own Wi-Fi hotspot and appears in the phone's Screen Mirroring
 list as *ESP32 Agent*. It keeps the H.264 stream (no decoding on the board) and forwards it to the app over BLE.
 The phone keeps using cellular data for the model while it is on the board's hotspot.
- **Hands — USB HID.** The board is a standard USB mouse and keyboard. With AssistiveTouch on, the mouse moves an
 on-screen pointer, so a click is a tap and a drag is a swipe.
- **Brain — the app.** The app decodes the stream, sends screenshots to any OpenAI-compatible vision model, and runs
 a planner and an actor: tap, swipe, draw, type, press keys, go home, finish. It runs in the background while it
 works; the Dynamic Island shows what it is doing.
- **Closing the loop.** The pointer is relative, so the app tracks it and re-homes it in a corner; before precise taps
 it wiggles the pointer, finds it on screen and corrects the miss. After each action it waits for the screen to
 settle and tells the model whether anything changed. A lost board, hotspot or mirroring link pauses the run and
 resumes it from the same step.
- **Review.** Every run is kept on the phone: replay it step by step with the taps and swipes drawn on top.
 Export the screenshots, actions and saved annotations from **Runs → open a run → ⋯ → Export trace** for analysis
 by another agent. See [Export runs for agent review](docs/run-data-export.md) for batch export, USB copying and file details.

## Hardware

| Part | Notes |
|---|---|
| **ESP32-S3 board** | Tested with a [Seeed Studio XIAO ESP32S3](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) (plain version, 8 MB PSRAM; not Sense, not Plus). About $7. Any ESP32-S3 with native USB on its USB-C port and PSRAM should work. |
| **iPhone** | iOS 18 or later, with cellular data (the Wi-Fi is taken by the board's hotspot). USB-C models plug in directly; Lightning models need a Lightning to USB Camera Adapter. The phone powers the board. |
| **Vision model** | Any OpenAI-compatible chat API that accepts images: a cloud API or your own server. |
| **Mac with Xcode** | Only to flash the board and build the app once. Not needed at run time. |

## Quick start

### 1. Flash the board (plugged into the Mac)

Install [arduino-cli](https://arduino.github.io/arduino-cli/), the ESP32 core 3.3.x and NimBLE-Arduino 2.5.x, then:

```bash
arduino-cli lib install "NimBLE-Arduino@2.5.1"
hardware/flash.sh # optional: [serial port] [--debug]
```

Always build with `flash.sh`: it applies the BLE buffer sizes in `hardware/hid_bridge/nimble_cfg.h`.

### 2. Install the app

```bash
cp ios/Config/Local.xcconfig.example ios/Config/Local.xcconfig # set DEVELOPMENT_TEAM and IA_BUNDLE_ID
open ios/IPhoneAgent.xcodeproj # run the IPhoneAgent scheme on your iPhone
```

The project is generated with [XcodeGen](https://github.com/yonaskolb/XcodeGen) from `ios/project.yml`
(`cd ios && xcodegen`). A free Apple ID can sign it (re-sign every 7 days). The one-tap hotspot join needs the
Hotspot Configuration capability (a paid account); without it the app shows the hotspot password to join by hand.

### 3. Set up (once, in the app)

Plug the board into the iPhone and open **ESP32 Agent**. Setup walks through four steps and checks each one itself:

1. **Plug Me In** — pair the board over Bluetooth.
2. **Let Me See the Screen** — join the board's Wi-Fi, then Control Center → Screen Mirroring → *ESP32 Agent*.
3. **Let Me Use the Pointer** — turn on AssistiveTouch; the app calibrates the pointer by itself.
4. **Give Me a Brain** — enter your model endpoint and key (stored in the Keychain), then choose a vision model
 from the endpoint's model list (or enter its model ID).

### 4. Give it a task

Type a goal (for example *"Open Settings and go to Wi-Fi"*) and press **Start**. Stop it from the Dynamic Island,
or come back to the app. Siri, Shortcuts, widgets and Control Center can run saved tasks.

## Model and prompts

- Any OpenAI-compatible vision endpoint works (vLLM, SGLang, llama.cpp, Ollama, cloud APIs). The app lists the
 endpoint's models for you to choose one explicitly; you can also enter a model ID, and set a separate planner
 and actor model.
- The prompts are plain text in [`prompts/`](prompts/) and bundled with th