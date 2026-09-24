"""Theme 'adaptive': one flexible layout system whose whole look comes from the post's `design` block, so every
topic gets its own palette, fonts, shapes, background texture and code-drawn SVG art.

Slide types: cover, facts, steps, prompt, list, compare, stat, limits, cta

`design` (all optional; bad values fall back to safe defaults, low contrast is corrected automatically):
    mood        short text, what the look should feel like (for humans / QA)
    palette     bg, bg2 (gradient end), surface, ink, muted, accent, accent2   (hex colors)
    fonts       display, body, mono   (names from FONTS below)
    display     weight (100-900), case ("none" | "upper"), tracking (1/100 em, e.g. -3), scale (0.8-1.4), italic_em (bool)
    shape       radius (0-48 px), border (0-4 px), shadow ("none" | "hard" | "soft" | "glow")
    background  pattern (see PATTERNS), pattern_opacity (0-0.3), glow (bool), gradient (bool)
    label       "mono" | "pill" | "bar"          style of the small section labels
    prompt      "terminal" | "chat" | "card"     look of the prompt box
    art         <svg viewBox="0 0 900 460">  cover illustration (drawn in code, about the topic)
    icon        <svg viewBox="0 0 24 24">    small symbol: label marker, list bullets
    deco        <svg viewBox="0 0 1080 1350"> optional decoration layer behind the content (kept faint)
SVGs may use the CSS variables var(--accent), var(--accent2), var(--ink), var(--muted), var(--surface), var(--bg).
"""
import html, re, pathlib, colorsys

FONTS_DIR = pathlib.Path(__file__).resolve().parent.parent / "fonts"
e = html.escape

# name -> (file, weight range or fixed weight, italic file or None)
FONTS = {
    "Inter": ("InterVariable.ttf", "100 900", None),
    "Manrope": ("Manrope.ttf", "200 800", None),
    "DM Sans": ("DMSans.ttf", "100 1000", None),
    "Outfit": ("Outfit.ttf", "100 900", None),
    "Sora": ("Sora.ttf", "100 800", None),
    "Space Grotesk": ("SpaceGrotesk.ttf", "300 700", None),
    "Unbounded": ("Unbounded.ttf", "200 900", None),
    "Syne": ("Syne.ttf", "400 800", None),
    "Bricolage Grotesque": ("BricolageGrotesque.ttf", "200 800", None),
    "Archivo": ("Archivo.ttf", "100 900", None),
    "Anton": ("Anton.ttf", "400", None),
    "Bebas Neue": ("BebasNeue.ttf", "400", None),
    "Fraunces": ("Fraunces.ttf", "100 900", None),
    "Playfair Display": ("PlayfairDisplay.ttf", "400 900", "PlayfairDisplay-Italic.ttf"),
    "DM Serif Display": ("DMSerifDisplay.ttf", "400", None),
    "Instrument Serif": ("InstrumentSerif.ttf", "400", "InstrumentSerif-Italic.ttf"),
    "JetBrains Mono": ("JetBrainsMono.ttf", "100 800", None),
    "Space Mono": ("SpaceMono-Regular.ttf", "400", None),
    "IBM Plex Mono": ("IBMPlexMono-Regular.ttf", "400", None),
}
BOLD_FILES = {"Space Mono": "SpaceMono-Bold.ttf", "IBM Plex Mono": "IBMPlexMono-Bold.ttf"}
CONDENSED = {"Anton", "Bebas Neue"}  # tall narrow faces: need bigger sizes, always upper case
PATTERNS = ["none", "grid", "dots", "lines", "diagonal", "waves", "rings", "scanlines", "noise", "plus"]

DEFAULT = {
    "palette": {"bg": "#0E0F13", "bg2": "#171A22", "surface": "#181B23", "ink": "#F3F4F7", "muted": "#9AA0AE",
                "accent": "#7C5CFF", "accent2": "#2EE6A6"},
    "fonts": {"display": "Space Grotesk", "body": "Inter", "mono": "JetBrains Mono"},
    "display": {"weight": 700, "case": "none", "tracking": -3, "scale": 1.0, "italic_em": False},
    "shape": {"radius": 28, "border": 2, "shadow": "soft"},
    "background": {"pattern": "grid", "pattern_opacity": 0.08, "glow": True, "gradient": True},
    "label": "mono", "prompt": "terminal",
}


# ---------------------------------------------------------------- color helpers

def _hex(c, fallback):
    c = str(c or "").strip()
    if re.fullmatch(r"#[0-9a-fA-F]{3}", c): c = "#" + "".join(ch * 2 for ch in c[1:])
    return c.upper() if re.fullmatch(r"#[0-9a-fA-F]{6}", c) else fallback


def _rgb(c):
    return tuple(int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))


def _lum(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in _rgb(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _mix(c, d, t):
    a, b = _rgb(c), _rgb(d)
    return "#" + "".join(f"{round((x + (y - x) * t) * 255):02X}" for x, y in zip(a, b))


def ensure(fg, bg, target):
    """Move fg toward white or black until it reaches the contrast target against bg."""
    if contrast(fg, bg) >= target: return fg
    to = "#FFFFFF" if _lum(bg) < 0.4 else "#000000"
    for i in range(1, 21):
        c = _mix(fg, to, i / 20)
        if contrast(c, bg) >= target: return c
    return to


def on(c):
    return "#FFFFFF" if contrast("#FFFFFF", c) >= contrast("#0B0B0B", c) else "#0B0B0B"


# ---------------------------------------------------------------- design resolution

def _clamp(v, lo, hi, d):
    try: return max(lo, min(hi, float(v)))
    except (TypeError, ValueError): return d


def resolve(data):
    """The post's design merged over the defaults, validated and contrast-fixed."""
    d = data.get("design") or {}
    P = {**DEFAULT["palette"], **{k: v for k, v in (d.get("palette") or {}).items() if v}}
    p = {k: _hex(P.get(k), DEFAULT["palette"][k]) for k in DEFAULT["palette"]}
    dark = _lum(p["bg"]) < 0.4
    p["bg2"] = p["bg2"] if abs(_lum(p["bg2"]) - _lum(p["bg"])) < 0.25 else p["bg"]
    for k in ("surface",):
        if contrast(p[k], p["bg"]) > 2.2: p[k] = _mix(p["bg"], p["ink"], 0.06)
    p["ink"] = ensure(p["ink"], p["surface"], 7) if contrast(p["ink"], p["bg"]) >= 7 else ensure(ensure(p["ink"], p["bg"], 7), p["surface"], 7)
    p["muted"] = ensure(ensure(p["muted"], p["bg"], 4.6), p["surface"], 4.5)
    p["accent"] = ensure(p["accent"], p["bg"], 3.2)  # used for big text and marks
    p["accent2"] = ensure(p["accent2"], p["bg"], 2.2)
    p["accent_text"] = ensure(p["accent"], p["bg"], 4.6)  # accent used for small text
    p["on_accent"] = on(p["accent"])

    F = {**DEFAULT["fonts"], **(d.get("fonts") or {})}
    f = {k: (F[k] if F.get(k) in FONTS else DEFAULT["fonts"][k]) for k in DEFAULT["fonts"]}
    if f["mono"] not in ("JetBrains Mono", "Space Mono", "IBM Plex Mono"): f["mono"] = "JetBrains Mono"
    if f["body"] in CONDENSED or f["body"] in ("DM Serif Display", "Instrument Serif", "Unbounded", "Syne"):
        f["body"] = "Inter"  # body text must stay readable at small sizes

    D = {**DEFAULT["display"], **(d.get("display") or {})}
    disp = {"weight": int(_clamp(D.get("weight"), 100, 900, 700)), "case": "upper" if D.get("case") == "upper" else "none",
            "tracking": _clamp(D.get("tracking"), -8, 6, -3), "scale": _clamp(D.get("scale"), 0.8, 1.4, 1.0),
            "italic_em": bool(D.get("italic_em"))}
    if f["display"] in CONDENSED: disp["case"] = "upper"; disp["scale"] = max(disp["scale"], 1.2); disp["tracking"] = max(disp["tracking"], 0)
    if FONTS[f["display"]][1].isdigit(): disp["weight"] = int(FONTS[f["display"]][1])

    S = {**DEFAULT["shape"], **(d.get("shape") or {})}
    shape = {"radius": int(_clamp(S.get("radius"), 0, 48, 28)), "border": _clamp(S.get("border"), 0, 4, 2),
             "shadow": S.get("shadow") if S.get("shadow") in ("none", "hard", "soft", "glow") else "soft"}
    B = {**DEFAULT["background"], **(d.get("background") or {})}
    bgd = {"pattern": B.get("pattern") if B.get("pattern") in PATTERNS else "none",
           "pattern_opacity": _clamp(B.get("pattern_opacity"), 0, 0.2, 0.08), "glow": bool(B.get("glow")),
           "gradient": bool(B.get("gradient"))}
    return {"palette": p, "dark": dark, "fonts": f, "display": disp, "shape": shape, "background": bgd,
            "label": d.get("label") if d.get("label") in ("mono", "pill", "bar") else "mono",
            "prompt": d.get("prompt") if d.get("prompt") in ("terminal", "chat", "card") else "terminal",
            "art": clean_svg(d.get("art")), "icon": clean_svg(d.get("icon")), "deco": clean_svg(d.get("deco")),
            "mood": str(d.get("mood", ""))}


def clean_svg(s):
    """Keep only a single inline <svg>; drop scripts, event handlers, external references, embedded HTML."""
    s = str(s or "").strip()
    m = re.search(r"<svg\b.*</svg>", s, re.S | re.I)
    if not m or len(s) > 60000: return ""
    s = m.group(0)
    s = re.sub(r"<(script|foreignObject|image|iframe|style)\b.*?(</\1>|/>)", "", s, flags=re.S | re.I)
    s = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", s, flags=re.I)
    s = re.sub(r"\s(xlink:)?href\s*=\s*(\"(?!#)[^\"]*\"|'(?!#)[^']*')", "", s, flags=re.I)
    s = re.sub(r"url\((?!\s*#)[^)]*\)", "none", s, flags=re.I)
    return s


# ---------------------------------------------------------------- css

def _face(name, family):
    file, weight, italic = FONTS[name]
    out = f"@font-face{{font-family:'{family}';src:url({(FONTS_DIR / file).as_uri()});font-weight:{weight}}}"
    if name in BOLD_FILES:
        out += f"@font-face{{font-family:'{family}';src:url({(FONTS_DIR / BOLD_FILES[name]).as_uri()});font-weight:700}}"
    if italic:
        out += f"@font-face{{font-family:'{family}';src:url({(FONTS_DIR / italic).as_uri()});font-weight:{weight};font-style:italic}}"
    return out


def _svg_uri(svg):
    return "url(\"data:image/svg+xml;utf8," + svg.replace("#", "%23").replace('"', "'").replace("\n", "") + "\")"


def _pattern(bg, ink, accent):
    k, o = bg["pattern"], bg["pattern_opacity"]
    c = f"color-mix(in srgb,{ink} {o * 100:.0f}%,transparent)"
    if k == "grid": return f"background-image:linear-gradient({c} 1.5px,transparent 1.5px),linear-gradient(90deg,{c} 1.5px,transparent 1.5px);background-size:72px 72px"
    if k == "dots": return f"background-image:radial-gradient({c} 2.2px,transparent 2.6px);background-size:36px 36px"
    if k == "lines": return f"background-image:repeating-linear-gradient(0deg,{c} 0 1.5px,transparent 1.5px 54px)"
    if k == "diagonal": return f"background-image:repeating-linear-gradient(45deg,{c} 0 2px,transparent 2px 28px)"
    if k == "scanlines": return f"background-image:repeating-linear-gradient(0deg,{c} 0 2px,transparent 2px 7px)"
    if k == "rings": return f"background-image:repeating-radial-gradient(circle at 88% 8%,transparent 0 46px,{c} 46px 48px)"
    if k == "plus":
        svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64'><path d='M32 24v16M24 32h16' stroke='{ink}' stroke-opacity='{o * 2.2:.2f}' stroke-width='2'/></svg>"
        return f"background-image:{_svg_uri(svg)}"
    if k == "waves":
        svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='240' height='60'><path d='M0 30 C 40 5, 80 5, 120 30 S 200 55, 240 30' "
               f"fill='none' stroke='{ink}' stroke-opacity='{o * 1.6:.2f}' stroke-width='2'/></svg>")
        return f"background-image:{_svg_uri(svg)}"
    if k == "noise":
        svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' "
               f"baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 {o * 4:.2f} 0'/></filter>"
               f"<rect width='100%' height='100%' filter='url(%23n)'/></svg>")
        return f"background-image:{_svg_uri(svg)}"
    return ""


BASE = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:var(--bg);color:var(--ink);font-family:var(--fb),sans-serif;position:relative;overflow:hidden;
 -webkit-font-smoothing:antialiased}
.bgp{position:absolute;inset:0}
.glow{position:absolute;inset:0;background:radial-gradient(900px 700px at 100% 0%,color-mix(in srgb,var(--accent) 22%,transparent),transparent 70%),
 radial-gradient(900px 800px at 0% 100%,color-mix(in srgb,var(--accent2) 16%,transparent),transparent 70%)}
.deco{position:absolute;inset:0;opacity:.18}
.deco svg{width:100%;height:100%}
.wrap{position:absolute;inset:68px 76px 60px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;gap:20px}
.brand{display:flex;align-items:center;gap:14px;font-family:var(--fd),sans-serif;font-weight:700;font-size:29px;letter-spacing:-.5px;text-transform:none}
.logo{width:44px;height:44px;border-radius:calc(var(--r)*.45);background:var(--accent);color:var(--on-accent);display:grid;place-items:center;font-weight:900;font-size:22px;font-family:var(--fb)}
.topic{font-family:var(--fm),monospace;font-size:19px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:520px}
.count{font-family:var(--fm),monospace;font-size:21px;color:var(--muted);font-variant-numeric:tabular-nums}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:22px;color:var(--muted);font-weight:600}
.swipe{display:flex;align-items:center;gap:12px;color:var(--ink)}
.swipe span{width:50px;height:50px;border-radius:50%;border:var(--bw) solid color-mix(in srgb,var(--ink) 25%,transparent);display:grid;place-items:center}
h1{font-family:var(--fd),sans-serif;font-weight:var(--dw);letter-spacing:var(--dt);line-height:1.02;text-transform:var(--dc);text-wrap:balance}
h1 em{font-style:var(--emi);color:var(--accent)}
.sub{margin-top:26px;font-size:34px;line-height:1.35;color:var(--muted);font-weight:500;max-width:900px;text-wrap:pretty}
/* labels */
.lab{align-self:flex-start;display:inline-flex;align-items:center;gap:14px;font-family:var(--fm),monospace;font-size:22px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--accent-text)}
.lab .ic{width:30px;height:30px;color:var(--accent)}
.lab .ic svg{width:100%;height:100%}
.lab-pill .lab{border:var(--bw) solid color-mix(in srgb,var(--accent) 60%,transparent);border-radius:99px;padding:10px 22px 10px 16px;background:color-mix(in srgb,var(--accent) 10%,transparent)}
.lab-bar .lab{border-left:8px solid var(--accent);padding-left:18px;color:var(--ink)}
.lab + h1{margin-top:26px}
/* surfaces */
.box{background:var(--surface);border:var(--bw) solid color-mix(in srgb,var(--ink) 14%,transparent);border-radius:var(--r);box-shadow:var(--sh)}
/* cover */
.cover .kick{font-family:var(--fm),monospace;font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--accent-text);display:flex;gap:14px;align-items:center}
.cover .kick .ic{width:32px;height:32px;color:var(--accent)}
.cover .kick .ic svg{width:100%;height:100%}
.cover h1{margin-top:26px}
.art{margin-top:40px;height:420px;display:flex;align-items:center;justify-content:center}
.art svg{width:100%;height:100%}
.chips{margin-top:40px;display:flex;gap:14px;flex-wrap:wrap}
.chip{border:var(--bw) solid color-mix(in srgb,var(--ink) 20%,transparent);background:var(--surface);border-radius:calc(var(--r)*1.4 + 8px);padding:12px 24px;font-size:25px;font-weight:650}
/* facts */
.tbl{margin-top:46px;padding:10px 40px}
.tr{display:flex;gap:30px;padding:24px 0;align-items:baseline;border-bottom:1.5px solid color-mix(in srgb,var(--ink) 12%,transparent)}
.tr:last-child{border-bottom:0}
.tr .k{flex:none;width:230px;font-family:var(--fm),monospace;font-size:21px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase}
.tr .v{flex:1;font-size:37px;font-weight:650;letter-spacing:-.3px;line-height:1.25}
/* steps + list */
.st{margin-top:44px;display:flex;flex-direction:column;gap:20px}
.step{display:flex;gap:30px;align-items:flex-start;padding:32px 36px}
.step .no{flex:none;font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:78px;line-height:.85;color:var(--accent);min-width:64px;letter-spacing:-2px}
.step .t{font-size:37px;font-weight:700;letter-spacing:-.4px;line-height:1.2}
.step .d{margin-top:8px;font-size:28px;color:var(--muted);line-height:1.35}
code{font-family:var(--fm),monospace;font-size:.92em;background:color-mix(in srgb,var(--accent) 16%,transparent);color:var(--ink);padding:2px 10px;border-radius:calc(var(--r)*.25)}
.bul{flex:none;width:52px;height:52px;border-radius:calc(var(--r)*.5);background:color-mix(in srgb,var(--accent) 16%,transparent);color:var(--accent);display:grid;place-items:center;margin-top:2px}
.bul svg{width:30px;height:30px}
/* prompt */
.phead{display:flex;justify-content:space-between;align-items:flex-end}
.pn{font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:190px;line-height:.8;color:transparent;-webkit-text-stroke:3px var(--accent);letter-spacing:-6px}
.prompt h1{margin-top:26px}
.pbox{margin-top:40px;overflow:hidden}
.pbox .bar{display:flex;gap:10px;align-items:center;padding:20px 28px;border-bottom:1.5px solid color-mix(in srgb,var(--ink) 12%,transparent);font-family:var(--fm),monospace;font-size:19px;color:var(--muted)}
.pbox .bar i{width:13px;height:13px;border-radius:50%;background:color-mix(in srgb,var(--ink) 25%,transparent)}
.pbox .bar i:first-child{background:var(--accent)}
.pbox .bar span{margin-left:12px}
.pbox p{padding:34px 40px 40px;font-family:var(--fm),monospace;font-size:31px;line-height:1.5}
.pbox.chat p,.pbox.card p{font-family:var(--fb),sans-serif;font-size:34px;font-weight:500;line-height:1.45}
.pbox.terminal p:before{content:"> ";color:var(--accent);font-weight:700}
.pbox b{background:var(--accent);color:var(--on-accent);font-weight:700;padding:0 8px;border-radius:calc(var(--r)*.2)}
.pbox .send{display:flex;justify-content:space-between;align-items:center;padding:0 34px 28px;color:var(--muted);font-size:40px}
.pbox .send span{width:58px;height:58px;border-radius:50%;background:var(--ink);display:grid;place-items:center}
.note{margin-top:34px;display:flex;gap:18px;align-items:flex-start;font-size:30px;line-height:1.38;color:var(--muted)}
.note .k{flex:none;font-family:var(--fm),monospace;font-size:19px;font-weight:700;letter-spacing:1px;color:var(--on-accent);background:var(--accent);border-radius:calc(var(--r)*.25);padding:6px 11px;margin-top:3px}
/* compare */
.cols{margin-top:44px;display:grid;gap:18px}
.col{padding:30px 32px}
.col h3{font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:40px;letter-spacing:-.5px;color:var(--accent);text-transform:var(--dc)}
.col ul{margin-top:16px;list-style:none;display:flex;flex-direction:column;gap:12px}
.col li{font-size:27px;line-height:1.3;padding-left:28px;position:relative}
.col li:before{content:"";position:absolute;left:0;top:13px;width:12px;height:12px;border-radius:3px;background:var(--accent2)}
/* stat */
.stat .v{font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:250px;line-height:.9;letter-spacing:-8px;color:var(--accent);margin-top:30px;text-transform:var(--dc)}
.stat h1{margin-top:28px}
/* limits */
.lim{margin-top:40px}
.li{display:flex;gap:24px;padding:24px 0;font-size:34px;font-weight:550;line-height:1.3;align-items:flex-start;border-bottom:1.5px solid color-mix(in srgb,var(--ink) 12%,transparent)}
.li .x{flex:none;width:44px;height:44px;border-radius:calc(var(--r)*.3);border:2.5px solid var(--accent);color:var(--accent);display:grid;place-items:center;font-family:var(--fm);font-size:24px;font-weight:800;margin-top:2px}
.ctab{margin-top:42px;padding:32px 38px;background:var(--accent);color:var(--on-accent);border-radius:var(--r);display:flex;justify-content:space-between;align-items:center;gap:20px}
.ctab .t{font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:40px;letter-spacing:-.5px;text-transform:var(--dc)}
.ctab .h{font-family:var(--fm),monospace;font-size:24px;font-weight:700}
/* cta */
.cta h1 span{color:var(--muted)}
.rows{margin-top:60px;display:flex;flex-direction:column;gap:18px}
.row{display:flex;align-items:center;gap:26px;padding:28px 34px}
.row .v{flex:none;min-width:180px;font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:34px;color:var(--accent);text-transform:var(--dc)}
.row .d{font-size:29px;font-weight:500;line-height:1.3}
.big{margin-top:50px;font-size:38px;font-weight:800}
.big span{color:var(--accent)}
"""


def css(ds):
    p, f, d, s, b = ds["palette"], ds["fonts"], ds["display"], ds["shape"], ds["background"]
    faces = "".join(_face(n, fam) for n, fam in ((f["display"], "FD"), (f["body"], "FB"), (f["mono"], "FM")))
    sh = {"none": "none", "hard": f"8px 8px 0 {p['ink']}", "glow": f"0 0 44px color-mix(in srgb,{p['accent']} 35%,transparent)",
          "soft": f"0 24px 60px rgba(0,0,0,{0.45 if ds['dark'] else 0.14})"}[s["shadow"]]
    root = (f":root{{--bg:{p['bg']};--bg2:{p['bg2']};--surface:{p['surface']};--ink:{p['ink']};--muted:{p['muted']};"
            f"--accent:{p['accent']};--accent2:{p['accent2']};--accent-text:{p['accent_text']};--on-accent:{p['on_accent']};"
            f"--fd:'FD';--fb:'FB';--fm:'FM';--dw:{d['weight']};--dt:{d['tracking'] / 100:.3f}em;--dc:{'uppercase' if d['case'] == 'upper' else 'none'};"
            f"--emi:{'italic' if d['italic_em'] else 'normal'};--r:{s['radius']}px;--bw:{s['border']}px;--sh:{sh}}}")
    bgc = f"body{{background:{'linear-gradient(160deg,var(--bg),var(--bg2))' if b['gradient'] else 'var(--bg)'}}}"
    pat = f".bgp{{{_pattern(b, p['ink'], p['accent'])}}}"
    return faces + root + BASE + bgc + pat


# ---------------------------------------------------------------- slides

def hl(t):
    return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", e(t))


def rich(t):
    """Escape, then render `code` spans."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", e(t))


def size(text, base, ds, lo=0.62):
    """Headline size from its length (shorter = bigger), scaled for the display font."""
    n = len(text)
    k = 1.0 if n <= 22 else 0.9 if n <= 34 else 0.8 if n <= 48 else 0.7 if n <= 64 else lo
    if ds["display"]["case"] == "upper": k *= 0.9
    return round(base * k * ds["display"]["scale"])


ARROW = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
SEND = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--bg)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
DOT = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="6" fill="currentColor"/></svg>'


def label(text, ds):
    ic = f'<span class="ic">{ds["icon"] or DOT}</span>' if ds["label"] != "bar" else ""
    return f'<div class="lab">{ic}{e(text)}</div>'


def slide(s, n, slides, data, ds):
    t = s["type"]
    if t == "cover":
        title = e(s["title"])
        if s.get("em") and e(s["em"]) in title: title = title.replace(e(s["em"]), f'<em>{e(s["em"])}</em>', 1)
        fs = size(s["title"], 124 if ds["art"] else 138, ds)
        ic = f'<span class="ic">{ds["icon"]}</span>' if ds["icon"] else ""
        chips = "".join(f'<div class="chip">{e(x)}</div>' for x in s.get("tools", []))
        art = f'<div class="art">{ds["art"]}</div>' if ds["art"] else ""
        return (f'<div class="kick">{ic}{e(s.get("kicker", ""))}</div><h1 style="font-size:{fs}px">{title}</h1>'
                f'<div class="sub">{e(s.get("sub", ""))}</div>{art}' + (f'<div class="chips">{chips}</div>' if chips else ""))
    if t == "facts":
        rows = "".join(f'<div class="tr"><div class="k">{e(k)}</div><div class="v">{rich(v)}</div></div>' for k, v in s["items"])
        return f'{label(s.get("label", ""), ds)}<h1 style="font-size:{size(s["title"], 100, ds)}px">{e(s["title"])}</h1><div class="tbl box">{rows}</div>'
    if t == "steps":
        st = "".join(f'<div class="step box"><div class="no">{i}</div><div><div class="t">{rich(a)}</div><div class="d">{rich(d)}</div></div></div>'
                     for i, (a, d) in enumerate(s["steps"], 1))
        return f'{label(s.get("label", ""), ds)}<h1 style="font-size:{size(s["title"], 106, ds)}px">{e(s["title"])}</h1><div class="st">{st}</div>'
    if t == "list":
        bul = ds["icon"] or DOT
        st = "".join(f'<div class="step box"><div class="bul">{bul}</div><div><div class="t">{rich(a)}</div><div class="d">{rich(d)}</div></div></div>'
                     for a, d in s["items"])
        return f'{label(s.get("label", ""), ds)}<h1 style="font-size:{size(s["title"], 102, ds)}px">{e(s["title"])}</h1><div class="st">{st}</div>'
    if t == "prompt":
        idx = sum(1 for x in slides[:n] if x["type"] == "prompt")
        kind = ds["prompt"]
        head = (f'<div class="bar"><i></i><i></i><i></i><span>{e(data.get("window", "prompt"))}</span></div>' if kind == "terminal" else "")
        tail = f'<div class="send">+<span>{SEND}</span></div>' if kind == "chat" else ""
        note = s.get("note") or s.get("tip")
        return (f'<div class="phead"><div class="pn">{idx:02d}</div>{label(s.get("label") or s.get("tag", ""), ds)}</div>'
                f'<h1 style="font-size:{size(s.get("name") or s.get("title", ""), 104, ds)}px">{e(s.get("name") or s.get("title", ""))}</h1>'
                f'<div class="pbox box {kind}">{head}<p>{hl(s["prompt"])}</p>{tail}</div>'
                + (f'<div class="note"><span class="k">TIP</span><span>{rich(note)}</span></div>' if note else ""))
    if t == "compare":
        cols = s["cols"]
        cc = "".join(f'<div class="col box"><h3>{e(c["name"])}</h3><ul>{"".join(f"<li>{rich(x)}</li>" for x in c["points"])}</ul></div>' for c in cols)
        return (f'{label(s.get("label", ""), ds)}<h1 style="font-size:{size(s["title"], 98, ds)}px">{e(s["title"])}</h1>'
                f'<div class="cols" style="grid-template-columns:{"1fr" if len(cols) > 2 else "1fr 1fr"}">{cc}</div>')
    if t == "stat":
        return (f'{label(s.get("label", ""), ds)}<div class="v">{e(s["value"])}</div>'
                f'<h1 style="font-size:{size(s["title"], 90, ds)}px">{e(s["title"])}</h1>' + (f'<div class="sub">{rich(s["sub"])}</div>' if s.get("sub") else ""))
    if t == "limits":
        li = "".join(f'<div class="li"><div class="x">!</div><div>{rich(x)}</div></div>' for x in s["items"])
        cta = (f'<div class="ctab"><div class="t">{e(s["cta"])}</div><div class="h">{e(data["handle"])}</div></div>' if s.get("cta") else "")
        return f'{label(s.get("label", ""), ds)}<h1 style="font-size:{size(s["title"], 106, ds)}px">{e(s["title"])}</h1><div class="lim">{li}</div>{cta}'
    if t == "cta":
        rows = "".join(f'<div class="row box"><div class="v">{e(a)}</div><div class="d">{e(b)}</div></div>' for a, b in s["lines"])
        return (f'<h1 style="font-size:{size(s["title"] + s.get("title2", ""), 118, ds)}px">{e(s["title"])}<br><span>{e(s.get("title2", ""))}</span></h1>'
                f'<div class="rows">{rows}</div><div class="big">New AI tips <span>every day</span> → {e(data["handle"])}</div>')
    raise ValueError(f"adaptive theme has no slide type '{t}'")


def render(data):
    ds = resolve(data); style = css(ds)
    slides = data["slides"]; total = len(slides); pages = []
    for n, s in enumerate(slides, 1):
        body = slide(s, n, slides, data, ds)
        sw = f'<div class="swipe">Swipe <span>{ARROW}</span></div>' if n < total else "<div>Save · Share</div>"
        deco = f'<div class="deco">{ds["deco"]}</div>' if ds["deco"] else ""
        glow = '<div class="glow"></div>' if ds["background"]["glow"] else ""
        top = (f'<div class="top"><div class="brand"><div class="logo">{e(data["brand"][0])}</div>{e(data["brand"])}</div>'
               f'<div class="topic">{e(data.get("topic", ""))}</div><div class="count">{n:02d}/{total:02d}</div></div>')
        pages.append(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{style}</style></head>'
                     f'<body class="{s["type"]} lab-{ds["label"]}"><div class="bgp"></div>{glow}{deco}'
                     f'<div class="wrap">{top}<div class="body">{body}</div><div class="foot"><div>{e(data["handle"])}</div>{sw}</div></div></body></html>')
    return pages


# ---- Reel (9:16) settings used by reel.py; configure(data) sets the per-post colors ----
ACCENT = DEFAULT["palette"]["accent"]
CC_ACTIVE = DEFAULT["palette"]["accent"]
ANIM_SEL = ".kick,.lab,.body h1,.sub,.art,.chip,.tbl,.step,.pn,.pbox,.note,.col,.stat .v,.li,.ctab,.row,.big"
TYPE_SEL = ".pbox p"
DRAW_SEL = ".art"
REEL_CSS = """
.wrap{inset:190px 76px 330px !important}
.top .topic{display:none}
.sub{font-size:38px !important}.tr .v{font-size:39px !important}.tr{padding:28px 0 !important}
.step .t{font-size:41px !important}.step .d{font-size:31px !important}.pbox p{font-size:32px !important}.note{font-size:31px !important}
.li{font-size:36px !important;padding:26px 0 !important}.col li{font-size:30px !important}.row .d{font-size:32px !important}
.art{height:360px !important;margin-top:28px !important}.chips{margin-top:28px !important}
.swipe{display:none !important}
"""


def configure(data):
    """Per-post Reel colors (reel.py calls this before rendering)."""
    global ACCENT, CC_ACTIVE
    p = resolve(data)["palette"]
    ACCENT = p["accent"]
    CC_ACTIVE = ensure(p["accent"], "#0A0A0E", 4.5)  # captions sit on a dark band
    globals()["REEL_CSS"] = REEL_CSS.split("\n.caret")[0] + f"\n.caret{{background:{p['accent']}}}\n"
