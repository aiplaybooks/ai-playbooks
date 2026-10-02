# Spotifast

Previously **Fastpotify**. Same native Spotify client, now at
[spotifast.rocks](https://spotifast.rocks/). The new name starts with version 0.8.0;
your existing settings and sign-ins carry over, except when
[switching the Flatpak installation](docs/_reference/renaming.md#flatpak).

**Spotify, native and fast.** Spotifast is a Spotify client written in
Rust with [egui](https://github.com/emilk/egui). It plays music through
[librespot](https://github.com/librespot-org/librespot). It typically uses
100–250 MB of RAM, while Spotify's desktop app often uses 600 MB to over 1 GB.
It runs on Linux, macOS, and Windows, starts in well under a second, and has no
browser engine.

**Want WhatsApp just as fast and native?** [ZapFast](https://zapfast.rocks) is
Spotifast's sibling: the same native interface, for WhatsApp. Both are built on [fastframe](https://github.com/crmne/fastframe), the shared
foundation for native Rust apps built with egui.

**Playback needs Spotify Premium.** Free accounts can browse and search, but
cannot play music through Spotifast on this computer or another device.

https://github.com/user-attachments/assets/a5f669ce-b3b7-4f8e-9933-976a78876c7e

See [spotifast.rocks](https://spotifast.rocks/) for installation, setup,
everyday use, and connection details.

`spotifast` is the main command and `fastpotify` remains available
for existing scripts. Starting with 0.9.1, the existing profile and protected
sign-ins migrate to Spotifast's names. Existing destination profiles are preserved.
AUR and Homebrew packages now use the Spotifast name. See [rename compatibility](docs/_reference/renaming.md).

## What it does

- **Plays music on this computer.** Spotifast appears as a Spotify Connect
 device. Select it from your phone or play music in the app. Playback is
 gapless and supports up to 320 kbps, with
 optional volume normalisation and an on-disk audio cache.
 Stalled Spotify connections time out after five seconds per attempt so
 playback can try another endpoint.
 Since 0.8.0, a confirmed local seek discards audio queued from
 the old position. Decoder, download, and device-buffer delays can still apply.
 Starting a sorted playlist or Liked Songs view shows the requested song
 immediately while playback connects, using its loaded metadata (available since 0.8.0). Sorted views start at their first playable row. Filtering a
 playlist or Liked Songs keeps playback within the shown songs and preserves
 repeated songs; Play is unavailable when no shown song can play.
- **Controls other devices.** Move playback to a speaker, a phone, or
 another computer from the device picker, and keep controlling it: play,
 pause, skip, seek, shuffle, repeat, volume. The picker expands upward to
 show several devices at once, fitting the window; longer lists scroll.
 Since 0.9.0, switching back to this computer transfers the active
 Connect session with its song, position, queue, and paused or playing state.
- **Finds speakers on your network.** Spotifast finds librespot, spotifyd,
 and supported hardware receivers over mDNS. Once connected, they appear as
 Spotify Connect devices. The picker uses responding receivers' names and
 combines entries with the same device ID.
- **Library.** Browse playlists, Liked Songs, saved albums, followed artists,
 podcasts, and saved episodes. Filter, pin, and reorder sidebar items.
 Since 0.10.0, the Library header switches between a list and a
 responsive cover grid.
 Since 0.10.0, with local playback enabled, audiobooks saved in
 Spotify stay out of Podcasts, since they can't be played here.
 Since 0.8.0, double-click a playlist row in Library to start playback;
 a single click opens it. In the grid, a card's corner button plays it.
 Settings offers a compact track list with one line per song and spaced
 separators between its name, artists and added date.
 Since 0.8.0, choose name, recent plays, or saved-date order where
 available. Follow Spotify’s playlist order or keep a separate local arrangement.
 Spotify doesn't let apps change its order, so since 0.10.0,
 dragging a playlist while following it switches to the local arrangement
 and says so.
 Move Liked Songs among your pins or unpin it and choose its local position;
 the placement survives restarts.
 With local playback enabled, releases that the Web API groups as singles
 are labelled EP when librespot confirms that type.
 Liked Songs reopens from an account-specific metadata cache. Older rows
 refresh in the background while Like and Unlike take effect immediately.
 Right-click album, artist, and podcast cards for their actions (available since 0.8.0).
- **Search** across songs, artists, albums, playlists, podcasts, and episodes,
 with a top result and per-type views. Right-click results and cards for their actions.
 When Spotify provides an artist profile, its name on a song opens that page,
 including from the top result.
 Text fields offer Cut, Copy, Paste and Select all from their right-click menu.
 Since 0.8.0, a personal app searches the catalogue while shared
 access finds playlists. Each part appears independently, even if the other fails.

 Since 0.8.0, the search field stays clear of the device and update
 badges in narrow windows; hover their icons to read the labels.
- **Home** with Made for you, Recently played, your top artists and songs, and
 recommendations. Right-click playlist shortcuts and shelf cards for their actions.
 Since 0.10.0, **Your podcasts** lists episodes of your saved
 podcasts that you have started, then new ones you have not.
 Playing an episode you have started, from Home, a podcast page, your saved
 episodes or search, continues where you left it.
- **Artist pages** with popular songs, a filterable discography, and related
 artists. **Album**, **playlist**, and **podcast** pages support playback
 from any row. Since 0.8.0, album and playlist scrollbars represent the full track count;
 dragging to an unloaded section fetches that section directly.
 Discogra