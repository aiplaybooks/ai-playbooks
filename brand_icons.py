"""Brand icons for the carousel cover (owner, 2026-09-26: like the reference pages, every cover carries the icon of the
tool the post is about, a different size / place / style each time, never dominating the photo).

Icons: Simple Icons (https://simpleicons.org, CC0 collection of brand SVGs + brand colors), fetched on first use from
jsDelivr and cached in icons/ (committed). Brands keep their own trademark rules: we only use a logo to say which
product the post is about.

cover.icons in the content JSON (all optional; missing values are picked per post, deterministic from the headline):
    [{"slug": "openai", "style": "tile|circle|brand|glass|plain", "pos": "tl|tr|ml|mr|bl|br|c", "size": 130-300}]
Without cover.icons the icon comes from the post's tools / topic (TOOL_SLUGS).
"""
import re, json, random, zlib, pathlib, urllib.request

ROOT = pathlib.Path(__file__).parent.resolve()
DIR = ROOT / "icons"
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@16/"
UA = {"User-Agent": "AIPlaybooks/0.1"}
STYLES = ["tile", "circle", "brand", "glass", "plain"]
POS = ["tl", "tr", "ml", "mr", "bl", "br", "c"]

# tool / product name (lower case, as it appears in `tools`, `topic` or the headline) -> Simple Icons slug
TOOL_SLUGS = {
    "chatgpt": "openai", "openai": "openai", "codex": "openai", "sora": "openai", "gpt": "openai",
    "claude": "claude", "claude code": "claude", "anthropic": "anthropic",
    "gemini": "googlegemini", "google": "google", "notebooklm": "google", "youtube": "youtube",
    "meta ai": "meta", "meta": "meta", "llama": "meta", "instagram": "instagram", "facebook": "facebook",
    "whatsapp": "whatsapp", "threads": "threads",
    "perplexity": "perplexity", "copilot": "githubcopilot", "github copilot": "githubcopilot", "github": "github",
    "mistral": "mistralai", "le chat": "mistralai", "deepseek": "deepseek",
    "cursor": "cursor", "qwen": "qwen", "kimi": "kimi", "minimax": "minimax", "nvidia": "nvidia", "apple": "apple",
    "grok": "x", "xai": "x", "x": "x", "n8n": "n8n", "zapier": "zapier", "make": "make", "notion": "notion",
    "hugging face": "huggingface", "ollama": "ollama", "replit": "replit", "vercel": "vercel", "v0": "v0",
    "windsurf": "windsurf", "suno": "suno", "elevenlabs": "elevenlabs", "figma": "figma", "telegram": "telegram",
    "discord": "discord", "reddit": "reddit", "tiktok": "tiktok", "spotify": "spotify", "tesla": "tesla",
}


OLD = "https://cdn.jsdelivr.net/npm/simple-icons@15/"  # some brands left the current set (e.g. OpenAI): take them from v15


def _data(cdn=CDN, name="_data.json"):
    f = DIR / name
    if f.exists(): return json.loads(f.read_text(encoding="utf-8"))
    with urllib.request.urlopen(urllib.request.Request(cdn + "data/simple-icons.json", headers=UA), timeout=40) as r:
        d = json.load(r)
    d = d if isinstance(d, list) else d.get("icons", [])
    slim = {x["slug"]: {"title": x["title"], "hex": x["hex"]} for x in d if x.get("slug")}
    DIR.mkdir(exist_ok=True); f.write_text(json.dumps(slim, ensure_ascii=False), encoding="utf-8")
    return slim


def get(slug):
    """(inner SVG path markup, brand hex, title) or None."""
    meta, cdn = _data().get(slug), CDN
    if not meta: meta, cdn = _data(OLD, "_data15.json").get(slug), OLD
    if not meta: return None
    f = DIR / f"{slug}.svg"
    if not f.exists():
        try:
            with urllib.request.urlopen(urllib.request.Request(cdn + f"icons/{slug}.svg", headers=UA), timeout=40) as r: f.write_bytes(r.read())
        except OSError: return None
    svg = f.read_text(encoding="utf-8")
    inner = re.sub(r"<title>.*?</title>", "", re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1), flags=re.S)
    return inner, HEX.get(slug, "#" + meta["hex"]), meta["title"]


HEX = {"openai": "#0B0B0F", "x": "#0B0B0F"}  # the colors people know these icons in (ChatGPT's black/white knot)


def guess(data):
    """Slugs for the post from its tools / topic / headline, most specific first."""
    cv = data.get("cover") or {}
    s0 = next((s for s in data.get("slides", []) if s.get("type") == "cover"), {})
    names = [t.lower() for t in s0.get("tools") or []]
    text = " ".join([cv.get("headline", ""), data.get("topic", ""), data.get("hook", "") or ""]).lower()
    names += [k for k in sorted(TOOL_SLUGS, key=len, reverse=True) if re.search(rf"(?<![a-z]){re.escape(k)}(?![a-z])", text)]
    out = []
    for n in names:
        sl = TOOL_SLUGS.get(n)
        if sl and sl not in out: out.append(sl)
    return out


def _lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def plan(data, avoid=()):
    """Final icon list (1, sometimes 2) with style / pos / size filled in, deterministic per headline."""
    cv = data.get("cover") or {}
    rnd = random.Random(zlib.crc32((cv.get("headline") or data.get("topic") or "").encode()))
    given = cv.get("icons")
    if given == []: return []  # the writer said: no icon on this cover
    items = [dict(x) for x in given] if given else [{"slug": s} for s in guess(data)[:1]]
    free = [p for p in POS if p not in avoid]
    for it in items:
        it.setdefault("style", rnd.choice(STYLES))
        if it.get("pos") not in POS: it["pos"] = rnd.choice(free or POS)
        if it["pos"] in free: free.remove(it["pos"])
        it["size"] = max(110, min(320, int(it.get("size") or rnd.randint(150, 270))))
    return [it for it in items if get(it["slug"])]


def html(items, seed=""):
    """Absolutely positioned icon badges for the cover's image area (1080 x 960)."""
    rnd = random.Random(zlib.crc32(seed.encode()) + 7)
    out = []
    for it in items:
        inner, hexc, title = get(it["slug"]); s = it["size"]; st = it["style"]
        m = 54; jx, jy = rnd.randint(-22, 22), rnd.randint(-22, 22)
        x = {"tl": m, "ml": m, "bl": m, "tr": 1080 - m - s, "mr": 1080 - m - s, "br": 1080 - m - s, "c": 540 - s // 2}[it["pos"]] + jx
        y = {"tl": m + 20, "tr": m + 20, "ml": 330 - s // 2, "mr": 330 - s // 2, "bl": 640 - s, "br": 640 - s, "c": 400 - s // 2}[it["pos"]] + jy
        dark = _lum(hexc) < 0.18
        if st == "tile":   bg, fg, rad, ring = "#FFFFFF", ("#111111" if _lum(hexc) > 0.8 else hexc), "23%", "none"
        elif st == "circle": bg, fg, rad, ring = "#0B0B0F", "#FFFFFF", "50%", f"{max(4, s // 28)}px solid #FFFFFF"
        elif st == "brand":  bg, fg, rad, ring = hexc, ("#111111" if _lum(hexc) > 0.6 else "#FFFFFF"), "50%", f"{max(3, s // 40)}px solid rgba(255,255,255,.85)"
        elif st == "glass":  bg, fg, rad, ring = "rgba(255,255,255,.16)", "#FFFFFF", "28%", "2px solid rgba(255,255,255,.45)"
        else:                bg, fg, rad, ring = "transparent", "#FFFFFF", "0", "none"
        if st == "brand" and dark: bg = "#0B0B0F"
        pad = 0 if st == "plain" else int(s * 0.2)
        shadow = "drop-shadow(0 10px 26px rgba(0,0,0,.55))" if st == "plain" else "none"
        out.append(f'<div class="bi" title="{title}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{bg};'
                   f'border-radius:{rad};border:{ring};padding:{pad}px;filter:{shadow};'
                   f'{"backdrop-filter:blur(14px);" if st == "glass" else ""}">'
                   f'<svg viewBox="0 0 24 24" fill="{fg}">{inner}</svg></div>')
    return "".join(out)


CSS = """.bi{position:absolute;z-index:3;display:grid;place-items:center;box-shadow:0 14px 40px rgba(0,0,0,.35)}
.bi svg{width:100%;height:100%;display:block}"""
