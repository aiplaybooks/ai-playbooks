"""Theme 'ledger': editorial / market-terminal look. Cream paper, ink, serif headlines, mono labels."""
import html, re, random, pathlib

FONTS = pathlib.Path(__file__).resolve().parent.parent / "fonts"
e = html.escape

def hl(t):
    return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", e(t))

CSS = """
@font-face{font-family:Fraunces;src:url(%(fr)s);font-weight:100 900}
@font-face{font-family:Mono;src:url(%(mo)s);font-weight:100 800}
@font-face{font-family:Inter;src:url(%(in)s);font-weight:100 900}
:root{--paper:#F1ECE2;--ink:#14130F;--soft:#6B665C;--rule:#CFC7B8;--up:#0F8A5F;--down:#D1463B;--hi:#DDF3E6}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:var(--paper);color:var(--ink);font-family:Inter,sans-serif;position:relative;overflow:hidden}
body:before{content:"";position:absolute;inset:0;opacity:.35;
 background-image:radial-gradient(rgba(0,0,0,.08) 1px,transparent 1px);background-size:6px 6px}
.wrap{position:absolute;inset:64px 76px 60px;display:flex;flex-direction:column}
.mast{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:18px;border-bottom:3px solid var(--ink)}
.mast .b{font-family:Fraunces;font-weight:800;font-size:38px;letter-spacing:-1px;font-variation-settings:"opsz" 144,"SOFT" 0}
.mast .b i{font-style:normal;color:var(--up)}
.mast .m{font-family:Mono;font-size:20px;color:var(--soft);letter-spacing:1px;text-transform:uppercase}
.sub-rule{height:0;border-bottom:1px solid var(--ink);margin-top:5px}
.tape{margin-top:18px;display:flex;gap:26px;font-family:Mono;font-size:19px;color:var(--soft);white-space:nowrap;overflow:hidden}
.tape span b{color:var(--ink);font-weight:700} .tape .u{color:var(--up)} .tape .d{color:var(--down)}
.lab{font-family:Mono;font-size:22px;font-weight:700;letter-spacing:2px;text-transform:uppercase;display:flex;align-items:center;gap:14px}
.lab:before{content:"";width:14px;height:14px;background:var(--up)}
h1{font-family:Fraunces;font-weight:700;letter-spacing:-2.5px;line-height:1;font-variation-settings:"opsz" 144,"SOFT" 30}
.body{flex:1;display:flex;flex-direction:column;justify-content:center}
.foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--ink);padding-top:18px;font-family:Mono;font-size:20px;color:var(--soft);letter-spacing:1px;text-transform:uppercase}
.foot .n{color:var(--ink);font-weight:700}
.foot .arr{color:var(--ink);font-weight:700}
/* cover */
.cover h1{font-size:136px;letter-spacing:-5px;margin-top:30px}
.cover h1 em{font-style:italic;color:var(--up);font-weight:600}
.cover .dek{margin-top:40px;font-size:36px;line-height:1.35;max-width:860px;color:#2E2C27}
.candles{margin-top:56px}
/* facts */
.facts h1{font-size:74px;margin-top:26px}
.tbl{margin-top:50px;border-top:2px solid var(--ink)}
.tr{display:flex;padding:26px 0;border-bottom:1px solid var(--rule);align-items:baseline}
.tr .k{width:250px;font-family:Mono;font-size:22px;color:var(--soft);letter-spacing:1px;text-transform:uppercase}
.tr .v{flex:1;font-size:36px;font-weight:600;letter-spacing:-.5px}
/* steps */
.steps h1{font-size:90px;margin-top:26px}
.st{margin-top:54px;display:flex;flex-direction:column;gap:22px}
.s{display:flex;gap:34px;align-items:flex-start;padding:34px 36px;background:#FBF8F2;border:1.5px solid var(--ink);box-shadow:8px 8px 0 var(--ink)}
.s .no{font-family:Fraunces;font-size:80px;font-weight:800;line-height:.8;color:var(--up);width:70px}
.s .t{font-size:38px;font-weight:700;letter-spacing:-.5px}
.s .d{margin-top:10px;font-size:28px;color:#3B3832;line-height:1.3}
.s .d code{font-family:Mono;font-size:26px;background:var(--hi);padding:3px 10px;color:var(--ink)}
/* prompt */
.pn{font-family:Fraunces;font-size:200px;font-weight:800;line-height:.8;color:transparent;-webkit-text-stroke:2.5px var(--ink);letter-spacing:-8px}
.prompt h1{font-size:84px;margin-top:22px}
.term{margin-top:44px;background:var(--ink);color:#EDE8DE;padding:0 0 40px;box-shadow:10px 10px 0 var(--up)}
.term .bar{display:flex;gap:10px;padding:20px 26px;border-bottom:1px solid #34322C;font-family:Mono;font-size:18px;color:#8C877B;align-items:center}
.term .bar i{width:13px;height:13px;border-radius:50%%;background:#48453D}
.term .bar i:nth-child(1){background:var(--down)} .term .bar i:nth-child(2){background:#D9A441} .term .bar i:nth-child(3){background:var(--up)}
.term .bar span{margin-left:14px}
.term p{padding:34px 40px 0;font-family:Mono;font-size:29px;line-height:1.5}
.term p:before{content:"> ";color:var(--up);font-weight:700}
.term b{color:#0B0B0B;background:#7FE0B0;font-weight:700;padding:0 6px}
.note{margin-top:40px;display:flex;gap:16px;font-size:28px;line-height:1.35;color:#2E2C27;align-items:flex-start}
.note:before{content:"↳";font-family:Mono;color:var(--up);font-weight:800}
/* limits */
.limits h1{font-size:96px;margin-top:26px}
.lim{margin-top:50px}
.li{display:flex;gap:26px;padding:26px 0;border-bottom:1px solid var(--rule);font-size:34px;font-weight:550;line-height:1.3;align-items:flex-start}
.li .x{flex:none;width:44px;height:44px;border:2px solid var(--down);color:var(--down);display:grid;place-items:center;font-family:Mono;font-size:24px;font-weight:800;margin-top:2px}
.ctab{margin-top:52px;display:flex;justify-content:space-between;align-items:center;background:var(--ink);color:var(--paper);padding:34px 40px}
.ctab .t{font-family:Fraunces;font-size:44px;font-weight:700;letter-spacing:-1px}
.ctab .h{font-family:Mono;font-size:26px;color:#7FE0B0}
"""

def candles(n=34, w=928, h=150, seed=7):
    rnd = random.Random(seed); step = w / n; v = h * .6; out = []
    for i in range(n):
        o = v; c = max(18, min(h - 18, o + rnd.uniform(-22, 26)))
        hi = max(o, c) + rnd.uniform(4, 16); lo = min(o, c) - rnd.uniform(4, 16)
        col = "#0F8A5F" if c <= o else "#D1463B"  # svg y is inverted: smaller y = higher price
        x = i * step + step / 2
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{lo:.1f}" y2="{hi:.1f}" stroke="{col}" stroke-width="2"/>'
                   f'<rect x="{x-step*.3:.1f}" y="{min(o,c):.1f}" width="{step*.6:.1f}" height="{max(3,abs(c-o)):.1f}" fill="{col}"/>')
        v = c
    return f'<svg class="candles" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(out)}</svg>'

def render(data):
    css = CSS % {"fr": (FONTS / "Fraunces.ttf").as_uri(), "mo": (FONTS / "JetBrainsMono.ttf").as_uri(),
                 "in": (FONTS / "InterVariable.ttf").as_uri()}
    slides = data["slides"]; total = len(slides); pages = []
    brand = e(data["brand"]); b2 = brand[:5] + "<i>" + brand[5:] + "</i>" if len(brand) > 5 else brand
    for n, s in enumerate(slides, 1):
        t = s["type"]
        if t == "cover":
            title = e(s["title"])
            if s.get("em"): title = title.replace(e(s["em"]), f'<em>{e(s["em"])}</em>')
            body = f'<div class="lab">{e(s["kicker"])}</div><h1>{title}</h1><div class="dek">{e(s["sub"])}</div>{candles()}'
        elif t == "facts":
            rows = "".join(f'<div class="tr"><div class="k">{e(k)}</div><div class="v">{e(v)}</div></div>' for k, v in s["items"])
            body = f'<div class="lab">{e(s["label"])}</div><h1>{e(s["title"])}</h1><div class="tbl">{rows}</div>'
        elif t == "steps":
            st = ""
            for i, (a, d) in enumerate(s["steps"], 1):
                d = e(d)
                if "mcp." in d: d = f"<code>{d}</code>"
                st += f'<div class="s"><div class="no">{i}</div><div><div class="t">{e(a)}</div><div class="d">{d}</div></div></div>'
            body = f'<div class="lab">{e(s["label"])}</div><h1>{e(s["title"])}</h1><div class="st">{st}</div>'
        elif t == "prompt":
            idx = sum(1 for x in slides[:n] if x["type"] == "prompt")
            body = (f'<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="pn">{idx:02d}</div>'
                    f'<div class="lab" style="margin-bottom:14px">{e(s["label"])}</div></div>'
                    f'<h1>{e(s["name"])}</h1>'
                    f'<div class="term"><div class="bar"><i></i><i></i><i></i><span>{e(data.get("window", "claude"))}</span></div><p>{hl(s["prompt"])}</p></div>'
                    f'<div class="note">{e(s["note"])}</div>')
        elif t == "limits":
            li = "".join(f'<div class="li"><div class="x">!</div><div>{e(x)}</div></div>' for x in s["items"])
            body = (f'<div class="lab">{e(s["label"])}</div><h1>{e(s["title"])}</h1><div class="lim">{li}</div>'
                    f'<div class="ctab"><div class="t">{e(s["cta"])}</div><div class="h">{e(data["handle"])}</div></div>')
        tape = '<div class="tape">' + "".join(
            f'<span><b>{e(k)}</b> <span class="{"u" if up else "d"}">{"▲" if up else "▼"} {e(v)}</span></span>'
            for k, v, up in data.get("tape", [])) + '</div>'
        right = "Swipe →" if n < total else "Save · Share"
        pages.append(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body class="{t}"><div class="wrap">
<div class="mast"><div class="b">{b2}</div><div class="m">{e(data.get("topic", ""))}</div></div><div class="sub-rule"></div>{tape}
<div class="body">{body}</div>
<div class="foot"><div><span class="n">{n:02d}</span> / {total:02d}</div><div>{e(data["handle"])}</div><div class="arr">{right}</div></div>
</div></body></html>''')
    return pages

# ---- Reel (9:16) settings used by reel.py ----
ACCENT = "#0F8A5F"
CC_ACTIVE = "#7FE0B0"   # caption highlight for the spoken word
ANIM_SEL = ".lab,.body h1,.dek,.pn,.tr,.s,.term,.note,.li,.ctab"
TYPE_SEL = ".term p"          # element that gets the typewriter effect
DRAW_SEL = ".candles"         # element revealed left-to-right
REEL_CSS = """
.wrap{inset:190px 76px 330px !important}
.cover h1{font-size:150px !important}.cover .dek{font-size:41px !important}
.facts h1{font-size:86px !important}.tr{padding:32px 0 !important}.tr .v{font-size:41px !important}.tr .k{font-size:24px !important}
.steps h1{font-size:100px !important}.s .t{font-size:43px !important}.s .d{font-size:32px !important}.s{padding:42px 38px !important}
.prompt h1{font-size:98px !important}.term p{font-size:33px !important}.note{font-size:32px !important}.pn{font-size:230px !important}
.limits h1{font-size:104px !important}.li{font-size:39px !important;padding:32px 0 !important}.ctab .t{font-size:48px !important}
.lab{font-size:25px !important}
.caret{background:#7FE0B0}
"""
