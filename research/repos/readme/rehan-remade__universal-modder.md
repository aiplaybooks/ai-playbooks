Skills, tools and a shared knowledge base that let any AI coding agent mod almost any PC game you own. 
 The agent finds the game, works out the engine and the route, reads the real code, builds the mod, makes art, 3D and sound
 with fal , tests it in the running game, cuts the video, and writes down what it learned for the next agent.

 Coming next: the mod hub. Publish your mods, remix other people's, and make new ones. 
 Share what you make, get help, and follow along: 

## Install

Pick your agent. Each gets the same skills (Agent Skills format), the fal MCP server, and the `um` CLI.

| Agent | Install |
|---|---|
| **Claude Code** | `/plugin marketplace add rehan-remade/universal-modder` `/plugin install universal-modder@universal-modder` |
| **Codex** | `codex plugin marketplace add rehan-remade/universal-modder` `codex plugin add universal-modder@universal-modder` |
| **Gemini CLI** | `gemini extensions install https://github.com/rehan-remade/universal-modder` |
| **VS Code / Copilot** | Enable `chat.plugins.enabled`, run **Chat: Install Plugin From Source**, and enter this repo's URL |
| **Cursor** | Cursor Marketplace, or clone (Cursor reads `AGENTS.md` and `.cursor/mcp.json`) |
| **OpenCode** | Clone and run `opencode` inside it (`opencode.json` adds the skills and the fal MCP server) or, on OpenCode 2, `opencode plugin add 'github:rehan-remade/universal-modder#main::path:plugins/opencode'` (the `um` tool and fal MCP; add the skills with **Skills only**) |
| **Skills only** (any agent) | `npx skills add https://github.com/rehan-remade/universal-modder` |
| **Anything else** | `git clone https://github.com/rehan-remade/universal-modder` and start your agent inside it |

Inside a clone, each agent finds the skills where it looks for them: `.agents/skills` (Codex, Gemini CLI,
Copilot, Cursor, OpenCode) and `.claude/skills` (Claude Code) are copies of `skills/`. Instructions are in
`AGENTS.md`, which `CLAUDE.md` and `GEMINI.md` point to. MCP config is in `.mcp.json`, `.codex/config.toml`,
`.cursor/mcp.json`, `.vscode/mcp.json` and `opencode.json` (which also points OpenCode at `skills/`).

Without a clone, OpenCode 2 installs the plugin in `plugins/opencode/` with `opencode plugin add`: one
`um_run` tool that passes its arguments straight to the CLI and runs `um` from PATH (see below), plus the
fal MCP server when `FAL_KEY` is set and none is configured. A clone doesn't need it. See
`plugins/opencode/README.md`.

**The `um` CLI.** Plugin installs and clones put it on PATH (OpenCode's plugin install doesn't). Anywhere else:
```bash
uv tool install git+https://github.com/rehan-remade/universal-modder # or: pipx install git+...
```
**For assets,** get a [fal API key](https://fal.ai/dashboard/keys). It powers both the fal MCP server and
`um fal`. Rather than exporting it from a shell profile or a `.env`, store it once with `um fal key set`: on
Linux it goes into the desktop keyring (libsecret's `secret-tool`), elsewhere into an owner-only
`~/.secrets/fal-key`, and `um fal` finds it there (`um fal key status` shows which source is used). `FAL_KEY`
in the environment still works and wins. The agent configs read `FAL_KEY`, so start your agent with it set; on
Linux, take it from the keyring as below. With no key, fal's OAuth endpoint `https://mcp.fal.ai/mcp-relay`
signs you in through the browser instead ([fal's MCP guides](https://fal.ai/docs/documentation/setting-up/mcp)),
and `um comfy` makes images on a local ComfyUI server.
```bash
um fal key set # hidden prompt
export FAL_KEY="$(secret-tool lookup service fal.ai key api)" # Linux: before starting the agent
```
You also need Git, Python 3.10+ and ffmpeg. `uv` is recommended. Blender is needed for 3D → sprite renders.
Windows games are driven natively or from WSL.

## Try it
> Mod Terraria: add a homing missile launcher and a tactical nuke that craters the world. Make the sprites with fal.

> Make a new civilization for Age of Empires II with a unique unit rendered from 3D.

> Put real Minecraft inside GTA V story mode. Minecraft's camera should follow GTA's, and its TNT should blow up GTA cars.

> Port the Warthog from my Halo install into Minecraft, with a gunner on the turret.

> What engine is `C:\Games\Foo`, and has anyone modded it before?

The agent starts with the **mod-any-game** skill and runs the same loop every time:
1. search the knowledge base;
2. recon, then pick a route;
3. set up a safe lab (saves backed up);
4. read the actual code;
5. build one working slice;
6. generate assets;
7. verify in the real game;
8. record;
9. package;
10. write a field note for the next agent.

## A knowledge base that AIs write for AIs
[`knowledge/`](knowledge/) holds **field notes**: how specific games were actually modded, decompiled and
reverse-engineered. Each note gives:
- the exact versions that worked;
- the route, and why;
- what the engine really does;
- how it was verified;
- the gotchas (symptom → cause → fix).

**Every agent that finishes a mod can open a pull request with its note**, so the next agent starts where it
left off instead of rediscovering the same traps.

```bash
um kb search "grand theft auto" # before you start: prior art (works outside the repo too)
um kb new --game "Hades II" --title "A new boon god" --from-scan hades --agent "Codex (gpt-6)"
um kb check knowledge/games/hades-ii/a-new-boon-god.md
um kb pr knowledge/games/hades-ii/a-new-boon-god.md --yes # after your human says OK: branch, push, PR
```
Browse [`knowledge/INDEX.md`](knowledge/INDEX.md). Every game is welcome. Contribution rules, for humans and
AIs, are in [`CONTRIBUTING.md`](CONTRIBUTING.md): no game files, no decompiled dumps, no cheating other
players, and an honest status and verification.

A few notes from the community:
- [Portalcraft: real Minecraft inside Portal 2](knowledge/games/portal-2/portalcraft-minecraft-inside-portal-2.md)
- [Halo 3 weapons, Covenant, vehicles and maps ported into Minecraft](knowledge/games/halo-3-mcc/halo-3-weapon