Give your agent CAD superpowers.

[Docs](https://www.texttocad.dev)

[](https://github.com/earthtojake/text-to-cad/stargazers)
[](https://skills.sh/earthtojake/text-to-cad)
[](https://x.com/earthtojake)
[](https://discord.gg/5FGB9DwJYU)
[](LICENSE)
[](https://github.com/earthtojake/text-to-cad/actions/workflows/test.yml?query=branch%3Amain)
[](https://pypi.org/project/cadgen/)
[](https://github.com/gumyr/build123d)
[](https://dev.opencascade.org)
[](packages/cadgen/pyproject.toml)
[](https://nodejs.org)

# text-to-cad

The text-to-cad plugin gives your agent local workflows for generating 3D models
as STEP, GLB, STL or 3MF files. It also does design for manufacturing checks,
generates engineering drawings, and connects to popular 3D printing, sheet metal
and CNC fabrication services.

It is supported by all popular agents that support plugins or the
[skills](https://skills.sh) framework, including Claude Code, Codex, Cursor,
Gemini and Grok.

## 💻 Install

### Ask your agent (recommended)

Send this message to your agent and it will install text-to-cad for you.

```text
Install text-to-cad from https://github.com/earthtojake/text-to-cad
```

By default, text-to-cad sends usage stats and crash reports, tagged with a random
ID and never including your files, paths or prompts; turn them off with
`uvx cadgen telemetry off`, or ask your agent to. [Telemetry](#telemetry) says
the rest.

Or install it yourself:

1. CAD runs through [uv](https://docs.astral.sh/uv/): check that it is installed
 (`uv --version`), and if it is missing, install it with
 [uv's installer](https://docs.astral.sh/uv/getting-started/installation/).
2. Run the commands under your agent app's heading below, or under
 [Other Agents](#other-agents) if it has none.
3. Restart the app. Its first start downloads CAD's runtime, so it needs a network
 connection.

The plugin for your agent app brings the skills and CAD's viewer, a local server
(`cadgen mcp`). For an agent without a plugin, install the skills alone. Install
one or the other in an app, not both: two copies means every skill twice.

The install commands below take the `latest` branch: it holds the plugin alone
and gets each release once it is on PyPI. `main`, where development happens,
installs too, but can hold changes that aren't released yet. Each app names the
branch in its own way (`#latest`, `--ref latest`, `@latest` or
`--branch latest`); leave it out and the app installs `main`.

Each app's heading also says how to update text-to-cad, and how to reinstall it:
remove it, then install it again. Updating the plugin updates CAD: the new
release's cadgen is downloaded the first time it runs, and the skills and the
server share it. Earlier releases stay in uv's cache until you run `uv cache prune`.

### Claude Code

```bash
claude plugin marketplace add earthtojake/text-to-cad#latest
claude plugin install text-to-cad@earthtojake
```

The plugin also starts CAD's server. Where Claude Code can show app views, CAD
shows models as viewer cards in the conversation; otherwise, as in a terminal,
asking it to show a model gives you a link that opens the model in the CAD
Viewer in your browser.

To update, run these, then restart Claude Code:

```bash
claude plugin marketplace update earthtojake
claude plugin update text-to-cad@earthtojake
```

To reinstall, remove it with these, then run the install commands again:

```bash
claude plugin uninstall text-to-cad@earthtojake
claude plugin marketplace remove earthtojake
```

### Claude Desktop

CAD shows models in the chat: ask Claude to show one and it appears as a viewer
card you can orbit, add to your prompt, and open full size; Claude can read what
you selected and see what you see. It runs locally through uv: add the server to
Claude Desktop's config (Settings > Developer > Edit Config), then restart the
app. If Claude Desktop cannot find `uvx`, give its full path (`which uvx`).

```json
{
 "mcpServers": {
 "cad": {
 "command": "uvx",
 "args": ["--no-config", "--managed-python", "--python", "3.13", "--from", "cadgen==0.7.21", "cadgen", "mcp"],
 "env": {"CADGEN_INSTALL_CHANNEL": "claude-desktop"}
 }
 }
}
```

The config pins a cadgen release in `args`, and uvx keeps the version it first
downloads. To update, change that version to the
[latest release](https://pypi.org/project/cadgen/), then restart Claude Desktop.

### Codex

Install text-to-cad from Codex's plugin directory:
[text-to-cad for Codex](https://chatgpt.com/plugins/plugins_6ac09476ef008191a35887b22b0d048a),
then **Open in desktop app**.

In the Codex app the plugin also brings the CAD viewer: **CAD** in the sidebar
(recent models, and Open), a **CAD** tab beside each thread that the agent
drives, and *Open with CAD* for model files.

 Manual install 

```bash
codex plugin marketplace add earthtojake/text-to-cad --ref latest
codex plugin add text-to-cad@earthtojake
```

To update, upgrade the `earthtojake` marketplace (or use Plugins › Manage ›
Marketplace), then restart Codex:

```bash
codex plugin marketplace upgrade earthtojake
```

To reinstall, remove it with these, then run the install commands again:

```bash
codex plugin remove text-to-cad@earthtojake
codex plugin marketplace remove earthtojake
```

The marketplace was renamed from `text-to-cad` to `earthtojake`; if you added it
before, remove the old one first (`codex plugin marketplace remove text-to-cad`).

### Cursor

Cursor also loads the plugin installed with Claude Code. If the Claude Code plugin
is installed, Cursor already has text-to-cad: skip this.

```bash
git clone --depth 1 --branch latest https://github.com/earthtojake/text-to-cad ~/.cursor/plugins/local/text-to-cad
```

Cursor reads `.cursor-plugin/plugin.json`: restart Cursor after cloning. Teams
can import the repository instead, under **Dashboard → Plugins & MCPs → Team
Marketplaces**.

To update, pull the latest release, then restart Cursor:

```bash
git -C ~/.cursor/plugins/local/text-to-cad pull
```

To reinstall, delete the folder,