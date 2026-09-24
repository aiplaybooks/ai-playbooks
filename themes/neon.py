"""Theme 'neon': dark background, lime accent, chat-input prompt cards.
Slide types: cover, prompt, cta"""
import html, re, pathlib

FONTS = pathlib.Path(__file__).resolve().parent.parent / "fonts"
e = html.escape

def hl(t):  # highlight [PLACEHOLDERS]
    return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", e(t))

CSS = """
@font-face{font-family:Inter;src:url(%s);font-weight:100 900}
:root{--bg:#0B0B0F;--card:#16161D;--line:#2A2A35;--text:#F4F4F6;--muted:#8B8B99;--accent:#C8F560}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:var(--bg);font-family:Inter,sans-serif;color:var(--text);position:relative;overflow:hidden}
.glow{position:absolute;width:900px;height:900px;border-radius:50%%;right:-420px;top:-420px;background:radial-gradient(circle,rgba(200,245,96,.16),rgba(200,245,96,0) 65%%)}
.glow2{position:absolute;width:1000px;height:1000px;border-radius:50%%;left:-500px;bottom:-560px;background:radial-gradient(circle,rgba(200,245,96,.10),rgba(200,245,96,0) 65%%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px;
  -webkit-mask-image:radial-gradient(circle at 70%% 20%%,#000,transparent 70%%)}
.wrap{position:absolute;inset:72px 80px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:14px;font-weight:800;font-size:30px;letter-spacing:-.5px}
.logo{width:44px;height:44px;border-radius:12px;background:var(--accent);display:grid;place-items:center;color:#0B0B0F;font-weight:900;font-size:24px}
.count{font-size:24px;color:var(--muted);font-weight:600;font-variant-numeric:tabular-nums}
.tag{display:inline-flex;align-self:flex-start;gap:10px;align-items:center;border:1.5px solid var(--line);border-radius:100px;padding:10px 22px;font-size:22px;font-weight:600;color:var(--muted)}
.tag i{width:10px;height:10px;border-radius:50%%;background:var(--accent)}
.num{margin-top:34px;font-size:28px;font-weight:800;color:var(--accent);letter-spacing:.5px;text-transform:uppercase}
h1{margin-top:10px;font-size:70px;line-height:1.03;font-weight:850;letter-spacing:-2.5px}
.sub{margin-top:18px;font-size:31px;line-height:1.3;color:var(--muted);font-weight:500;max-width:880px}
.card{margin-top:44px;background:var(--card);border:1.5px solid var(--line);border-radius:36px;padding:42px 46px 28px}
.card p{font-size:31px;line-height:1.45;font-weight:500;color:#E6E6EA}
.card b{color:var(--accent);font-weight:700}
.bar{margin-top:28px;display:flex;justify-content:space-between;align-items:center}
.plus{font-size:44px;color:var(--muted);font-weight:300}
.send{width:62px;height:62px;border-radius:50%%;background:var(--text);display:grid;place-items:center}
.tip{margin-top:28px;display:flex;gap:18px;align-items:flex-start;padding:24px 28px;border-radius:24px;background:rgba(200,245,96,.07);border:1.5px solid rgba(200,245,96,.22)}
.tip .k{flex:none;font-size:20px;font-weight:800;color:#0B0B0F;background:var(--accent);border-radius:8px;padding:6px 10px;letter-spacing:.5px}
.tip .t{font-size:26px;line-height:1.35;color:#DADDE2;font-weight:500}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:24px;color:var(--muted);font-weight:600}
.swipe{display:flex;align-items:center;gap:12px;color:var(--text)}
.swipe span{width:52px;height:52px;border-radius:50%%;border:1.5px solid var(--line);display:grid;place-items:center}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:20px}
.kick{font-size:28px;font-weight:800;color:var(--accent);letter-spacing:3px}
.cover h1{font-size:112px;line-height:.98;letter-spacing:-4.5px;margin-top:26px}
.cover h1 em{font-style:normal;color:var(--accent)}
.cover .sub{font-size:38px;margin-top:34px;color:#C9C9D2}
.chips{margin-top:56px;display:flex;gap:14px;flex-wrap:wrap}
.chip{border:1.5px solid var(--line);background:var(--card);border-radius:100px;padding:14px 26px;font-size:26px;font-weight:650}
.cta h1{font-size:104px;line-height:1;letter-spacing:-4px;margin-top:0}
.cta h1 span{color:var(--muted)}
.rows{margin-top:70px;display:flex;flex-direction:column;gap:20px}
.row{display:flex;align-items:center;gap:26px;background:var(--card);border:1.5px solid var(--line);border-radius:28px;padding:30px 34px}
.row .v{flex:none;min-width:190px;font-size:34px;font-weight:850;color:var(--accent)}
.row .d{font-size:30px;font-weight:500;color:#DADDE2;line-height:1.3}
.big{margin-top:56px;font-size:40px;font-weight:800}
.big span{color:var(--accent)}
"""

SEND = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0B0B0F" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
ARROW = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#F4F4F6" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def render(data):
    css = CSS % (FONTS / "InterVariable.ttf").as_uri()
    slides = data["slides"]; total = len(slides); pages = []
    for n, s in enumerate(slides, 1):
        t = s["type"]; swipe = n < total
        if t == "cover":
            title = e(s["title"])
            if s.get("em"): title = title.replace(e(s["em"]), f'<em>{e(s["em"])}</em>')
            chips = "".join(f'<div class="chip">{e(x)}</div>' for x in s.get("tools", []))
            body = f'<div class="kick">{e(s["kicker"])}</div><h1>{title}</h1><div class="sub">{e(s["sub"])}</div><div class="chips">{chips}</div>'
            left = f'{data["handle"]} · Save for later'
        elif t == "prompt":
            idx = sum(1 for x in slides[:n] if x["type"] == "prompt")
            body = (f'<div class="tag"><i></i>{e(s["tag"])}</div>'
                    f'<div class="num">{idx:02d} — {e(s["name"])}</div><h1>{e(s["title"])}</h1><div class="sub">{e(s["sub"])}</div>'
                    f'<div class="card"><p>"{hl(s["prompt"])}"</p><div class="bar"><div class="plus">+</div><div class="send">{SEND}</div></div></div>'
                    + (f'<div class="tip"><div class="k">PRO TIP</div><div class="t">{e(s["tip"])}</div></div>' if s.get("tip") else ""))
            left = f'{data["handle"]} · Save this for later'
        elif t == "cta":
            rows = "".join(f'<div class="row"><div class="v">{e(a)}</div><div class="d">{e(b)}</div></div>' for a, b in s["lines"])
            body = (f'<h1>{e(s["title"])}<br><span>{e(s["title2"])}</span></h1><div class="rows">{rows}</div>'
                    f'<div class="big">New AI tips <span>every day</span> → {e(data["handle"])}</div>')
            left = "Follow for more"
        else:
            raise ValueError(f"neon theme has no slide type '{t}'")
        sw = f'<div class="swipe">Swipe <span>{ARROW}</span></div>' if swipe else ""
        top = f'<div class="top"><div class="brand"><div class="logo">{e(data["brand"][0])}</div>{e(data["brand"])}</div><div class="count">{n:02d} / {total:02d}</div></div>'
        pages.append(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body class="{t}">'
                     f'<div class="grid"></div><div class="glow"></div><div class="glow2"></div>'
                     f'<div class="wrap">{top}<div class="body">{body}</div><div class="foot"><div>{e(left)}</div>{sw}</div></div></body></html>')
    return pages


# ---- Reel (9:16) settings used by reel.py ----
ACCENT = "#C8F560"
CC_ACTIVE = "#C8F560"   # caption highlight for the spoken word
ANIM_SEL = ".kick,.body h1,.sub,.chip,.tag,.num,.card,.tip,.row,.big"
TYPE_SEL = ".card p"
DRAW_SEL = ""
REEL_CSS = """
.wrap{inset:190px 80px 330px !important}
.cover h1{font-size:124px !important}.cover .sub{font-size:42px !important}
.prompt h1{font-size:80px !important}.sub{font-size:35px !important}.card p{font-size:35px !important}.tip .t{font-size:30px !important}
.cta h1{font-size:112px !important}.row .d{font-size:33px !important}
.caret{background:#C8F560}
.swipe{display:none !important}
"""
