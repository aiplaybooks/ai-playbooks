"""The carousel's first slide for every theme: full-bleed image (cover.py) + big upper-case hook headline, brand line,
"SWIPE FOR MORE", photo credit. carousel.py uses it instead of the theme's own cover when the post has a `cover` block
and output/<post>/cover_image.jpg exists. The headline shrinks until it fits."""
import html, pathlib

FONTS = pathlib.Path(__file__).resolve().parent.parent / "fonts"
e = html.escape

CSS = """
@font-face{font-family:Anton;src:url(%(anton)s)}
@font-face{font-family:Inter;src:url(%(inter)s);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#050507;position:relative;overflow:hidden;font-family:Inter,sans-serif}
.img{position:absolute;left:0;right:0;top:0;height:960px;background:url(%(img)s) %(focus)s/cover}
.fade{position:absolute;left:0;right:0;top:600px;height:380px;background:linear-gradient(transparent,#050507 88%%)}
.cr{position:absolute;right:18px;top:872px;max-width:640px;text-align:right;color:rgba(255,255,255,.62);font-size:15px;font-weight:500;
 text-shadow:0 1px 3px rgba(0,0,0,.6)}
.low{position:absolute;left:40px;right:40px;top:918px;bottom:84px;display:flex;flex-direction:column;align-items:center}
.brand{display:flex;align-items:center;gap:10px;color:#cfcfd6;font-size:22px;font-weight:700;letter-spacing:.5px}
.brand i{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#C06BFF,#4F9BFF);display:grid;place-items:center;
 font-style:normal;color:#fff;font-weight:900;font-size:17px}
h1{margin-top:14px;text-align:center;font-family:Anton;font-weight:400;font-size:calc(74px*var(--k));line-height:1.02;color:#fff;
 text-transform:uppercase;letter-spacing:.3px;text-wrap:balance}
h1 em{font-style:normal;color:#FFD23F}
.sw{position:absolute;left:0;right:0;bottom:34px;text-align:center;color:#9b9ba6;font-size:19px;font-weight:700;letter-spacing:3px}
:root{--k:1}
"""
FIT = """<script>(()=>{const l=document.querySelector('.low'),r=document.documentElement;
for(let k=1;k>=0.55;k-=0.03){r.style.setProperty('--k',k.toFixed(2));if(l.scrollHeight<=l.clientHeight+1)break;}})();</script>"""


def render(data, image):
    cv = data["cover"]
    title = e(cv["headline"])
    if cv.get("em") and e(cv["em"]) in title: title = title.replace(e(cv["em"]), f"<em>{e(cv['em'])}</em>", 1)
    ph = cv.get("photo")
    credit = f'<div class="cr">Photo: {e(ph["author"])} · {e(ph["license"])}</div>' if ph else ""
    css = CSS % {"anton": (FONTS / "Anton.ttf").as_uri(), "inter": (FONTS / "InterVariable.ttf").as_uri(),
                 "img": pathlib.Path(image).resolve().as_uri(), "focus": cv.get("focus") or "50% 20%"}
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'<div class="img"></div><div class="fade"></div>{credit}'
            f'<div class="low"><div class="brand"><i>{e(data["brand"][0])}</i>{e(data["brand"].upper())}</div><h1>{title}</h1></div>'
            f'<div class="sw">SWIPE FOR MORE →</div>{FIT}</body></html>')
