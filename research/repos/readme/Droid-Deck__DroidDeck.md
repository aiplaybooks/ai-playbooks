DroidDeck brings the SteamOS experience to Android: Valve's Steam client in Big Picture on your Adreno handheld, with Windows games through Valve's ARM64 Proton.

> Note: DroidDeck does not have a stand-alone website. Do not click on any download links from websites claiming to be the DroidDeck team. 

## Requirements and install

Use Android 9 or newer on a supported Adreno device (730 or newer, or 8xx). Adreno 6xx is experimental: DirectX 11 uses DXVK 2 and may run, and DirectX 12 games can still crash. Mali, Xclipse, PowerVR, and Adreno 710 are unsupported. No root is required. Allow about 3 GB for the runtime and 1.1 GB more for the desktop and emulators. Install the APK from [Releases](https://github.com/Droid-Deck/DroidDeck/releases), install the Linux runtime, then press **Play** and sign in. Steam downloads on first launch. Install **Desktop & apps** to use the desktop and emulators. The **Store** installs Linux apps and games from Flathub (ARM64 builds) with Flatpak; with additional options to install Appimages and set up scripts. **Stores** (Setup › Stores › "Show Stores in the rail") signs in to GOG, Epic Games and Amazon Games and downloads games into the Games storage. Epic keeps its direct API install path. Opening Epic Stores prepares Epic’s official Linux launcher preview. When installed, Epic games launched from DroidDeck use that client, and games installed in the client are imported into DroidDeck’s library and shortcuts. The x86-64 client runs through FEX on ARM and DroidDeck retains its Proton hooks; this preview and ARM setup are outside Epic’s listed Linux support. The cog on a store’s chip row sets its opening tab and download speed tier.

On Android 14 and newer, before Steam launches, you must turn on **Disable child process restrictions** in Developer options. If this option is not available in developer settings (Android 12 and 13 devices), first launch of Steam will present a "Fix it for me" button, which will help automate the setup process.

## Smart glasses

Use **Setup → Smart glasses** for app-wide virtual-screen settings across DroidDeck menus, launchers, desktop sessions, and games. Supported VITURE, RayNeo, and XREAL connections provide 3DoF; Luma Ultra adds optional experimental 6DoF and stereo-assisted hand/Joy-Con tracking. Model support and SDK requirements differ: see the [smart-glasses support matrix](docs/smart-glasses-support.md) for supported devices, controls, setup, and limitations.

## Community

Join the [DroidDeck Discord](https://discord.gg/JRGAvawjsm) for help, Preview builds, and device reports. Bug reports go in its **#bug-reports** forum; attach the zip from **Share logs** (Setup, or the session drawer) so the logs come with it.

## Build

Run `tools/build_local.sh` with Docker, Java 17, the Android SDK/NDK, Rust through rustup, GitHub CLI, Python 3, and `zstd` installed. It prepares the same native libraries, pinned components and audio sinks as CI, then checks the APK's assets, JNI exports and dependencies. The APK is at `app/build/outputs/apk/release/app-release.apk`. Set `DROIDDECK_PA13_SOURCE_DIR` to an existing PulseAudio 13.0 source directory to skip downloading it. Set `DROIDDECK_SIGNING_ENV` to a signing environment file to install over a release build; relative keystore paths resolve beside that file. To install on an attached device, run `tools/deploy_local.sh`.

After preparation, ordinary `./gradlew :app:assembleRelease` builds can reuse the verified inputs. If native sources, component pins or staged files change, packaging stops with instructions to rerun the helper. Generated audio stays under `app/build/`; the tracked base bundle is never modified. `./gradlew -PskipRust=true :app:testDebugUnitTest` needs no native preparation. For an APK without store engines, use `DROIDDECK_SKIP_RUST=1 tools/build_local.sh`; it omits cached engine libraries too.

For the prepared Windows checkout, run `./tools/run_windows.ps1` (optionally with `-Serial `), or select **DroidDeck XR** in Android Studio and run the **app** module on the connected phone. Machine-specific options live in the ignored `local.properties`: `droiddeck.python` selects a Python executable, `droiddeck.skipRust=true` omits the optional store download engines, and `droiddeck.debugApplicationIdSuffix=.xr` installs **DroidDeck XR Dev** alongside the signed release. The development app has its own runtime and Steam login. The local Java selection is in `.gradle/config.properties`.

`python tools/prepare_windows_runtime.py` restores this checkout's audited runtime inputs from the pinned CI APK, three locally rebuilt preload libraries, and the checksum-pinned Gamescope archive in `build/windows-setup/`. Start Docker Desktop's Linux engine first: preparation now rebuilds DroidDeck's ARM64 VR driver and Vulkan layer from current source and runs their native regression tests. The compiler image is built automatically on first use. Vulkan headers come from the NDK beside `--llvm-strip`, or from an explicit `--vk-include ` directory.

To reuse that build, pass `--rebuilt-vr build/windows-setup/vr`. Preparation verifies its `vr-build.json` against the current Git revision, source files, Vulkan headers, output checksums, and ARM64 architecture; missing or stale builds fail instead of falling back to the donor's VR libraries. The script checks the actual donor CI merge tree, still rejects unrelated unaudited runtime changes, and records component provenance in `app/build/windows-runtime-provenance.json`. Preserve these ignored preparation files when rebuilding locally; `clean` removes the prepared assets and their verification manifest.

Run the helper and preload regression suite with `bash tools/test_local.sh`. On macOS it runs in Linux through Docker, matching the helpers' runtime and CI instead of compiling Linux preloads against macOS headers.

## Limits

Compatibility and performance vary by device; hardware validation is limited. Desktop compositing uses software rende