"""The carousel's first slide for every theme: full-bleed image (cover.py) + big upper-case hook headline, brand line,
"SWIPE FOR MORE", photo credit. carousel.py uses it instead of the theme's own cover when the post has a `cover` block
and output/<post>/cover_image.jpg exists. The headline shrinks until it fits.

On the image (owner, 2026-09-26, refs @chatgptips): the image must show what the post is about, plus
- the brand icon(s) of the tool the post is about (brand_icons.py): a different style, size and corner every post,
  helping the theme without dominating it; placed away from the person's face;
- layout "scene_person": the topic photo full-bleed + the well-known person in a ring-framed circle
  (output/<post>/cover_person.jpg), so the photo tells the story and the face still stops the scroll.
"""
import html, random, zlib, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import brand_icons as BI

FONTS = pathlib.Path(__file__).resolve().parent.parent / "fonts"
e = html.escape

CSS = """
@font-face{font-family:Anton;src:url(%(anton)s)}
@font-face{font-family:Inter;src:url(%(inter)s);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#050507;position:relative;overflow:hidden;font-family:Inter,sans-serif}
.img{position:absolute;left:0;right:0;top:0;height:960px;background:url(%(img)s) %(focus)s/cover}
.fade{position:absolute;left:0;right:0;top:600px;height:380px;background:linear-gradient(transparent,#050507 88%%);z-index:2}
.cr{position:absolute;right:18px;top:872px;max-width:760px;text-align:right;color:rgba(255,255,255,.62);font-size:15px;font-weight:500;
 text-shadow:0 1px 3px rgba(0,0,0,.6);z-index:4}
.low{position:absolute;left:40px;right:40px;top:918px;bottom:84px;display:flex;flex-direction:column;align-items:center;z-index:4}
.brand{display:flex;align-items:center;gap:10px;color:#cfcfd6;font-size:22px;font-weight:700;letter-spacing:.5px}
.brand i{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#C06BFF,#4F9BFF);display:grid;place-items:center;
 font-style:normal;color:#fff;font-weight:900;font-size:17px}
h1{margin-top:14px;text-align:center;font-family:Anton;font-weight:400;font-size:calc(74px*var(--k));line-height:1.02;color:#fff;
 text-transform:uppercase;letter-spacing:.3px;text-wrap:balance}
h1 em{font-style:normal;color:#FFD23F}
.sw{position:absolute;left:0;right:0;bottom:34px;text-align:center;color:#9b9ba6;font-size:19px;font-weight:700;letter-spacing:3px}
.pc{position:absolute;z-index:3;border-radius:50%%;padding:9px;background:conic-gradient(from 200deg,#FFD23F,#FF6B6B,#C06BFF,#4F9BFF,#FFD23F);
 box-shadow:0 18px 50px rgba(0,0,0,.5)}
.pc div{width:100%%;height:100%%;border-radius:50%%;background:url(%(person)s) %(pfocus)s/cover;border:6px solid #050507}
:root{--k:1}
"""
FIT = """<script>(()=>{const l=document.querySelector('.low'),r=document.documentElement;
for(let k=1;k>=0.55;k-=0.03){r.style.setProperty('--k',k.toFixed(2));if(l.scrollHeight<=l.clientHeight+1)break;}})();</script>"""


def credit(cv):
    parts = []
    for ph in (cv.get("photo"), cv.get("person_photo")):
        if ph and ph.get("author"): parts.append(f"{e(ph['author'])}" + (f" · {e(ph['license'])}" if ph.get("license") else ""))
    return f'<div class="cr">Photo{"s" if len(parts) > 1 else ""}: {" / ".join(parts)}</div>' if parts else ""


def render(data, image):
    cv = data["cover"]
    title = e(cv["headline"])
    if cv.get("em") and e(cv["em"]) in title: title = title.replace(e(cv["em"]), f"<em>{e(cv['em'])}</em>", 1)
    person = pathlib.Path(image).with_name("cover_person.jpg")
    scene_person = cv.get("layout_used") == "scene_person" and person.exists()
    rnd = random.Random(zlib.crc32(cv["headline"].encode()))
    pc, avoid = "", []
    if scene_person:  # the person's circle goes low on one side; icons keep away from it
        side = cv.get("person_pos") or rnd.choice(["bl", "br"])
        d = rnd.randint(330, 400); x = 60 if side == "bl" else 1080 - 60 - d
        pc = f'<div class="pc" style="left:{x}px;top:{600 - d // 2 + rnd.randint(-40, 30)}px;width:{d}px;height:{d}px"><div></div></div>'
        avoid = [side, "ml" if side == "bl" else "mr"]
    elif cv.get("person") and cv.get("photo"):  # a portrait fills the frame: keep the centre (the face) free
        avoid = ["c"]
    icons = BI.html(BI.plan(data, avoid), cv["headline"])
    css = CSS % {"anton": (FONTS / "Anton.ttf").as_uri(), "inter": (FONTS / "InterVariable.ttf").as_uri(),
                 "img": pathlib.Path(image).resolve().as_uri(), "focus": cv.get("focus") or "50% 20%",
                 "person": person.resolve().as_uri() if scene_person else "", "pfocus": cv.get("person_focus") or "50% 22%"} + BI.CSS
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'<div class="img"></div>{pc}{icons}<div class="fade"></div>{credit(cv)}'
            f'<div class="low"><div class="brand"><i>{e(data["brand"][0])}</i>{e(data["brand"].upper())}</div><h1>{title}</h1></div>'
            f'<div class="sw">SWIPE FOR MORE →</div>{FIT}</body></html>')
