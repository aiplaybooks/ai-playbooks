"""Theme 'prompts': the copy-paste prompt pack series ("7 prompts to ..."). Same per-topic `design` block as the
adaptive theme (palette, fonts, pattern, shape, icon; see themes/adaptive.py), but one fixed layout built for prompts,
so the series is recognisable while every pack still gets its own colors.

Slide types:
    cover   kicker, title, em, sub, tools[] ("works in" chips). A fanned stack of the pack's prompt cards is drawn
            automatically from the prompt slides' names; `count` overrides the big number (default: number of prompts).
    prompt  name ("Teacher mode"), sub (the benefit, one line), prompt (the copy-paste text; [PLACEHOLDERS] in caps, **KEY WORDS** in bold with a marker line),
            optional tip, optional demo (what the prompt gives you, drawn in code, never real photos):
              {"kind": "reply", "lines": ["short line of the AI's answer", ...]}         2-4 lines, illustrative
              {"kind": "before_after", "before": "<svg viewBox='0 0 400 250'>", "after": "<svg ...>",
               "labels": ["Before", "After"]}                                           for image/editing prompts
    howto   title, items [[title, detail], ...]  how to use the pack (fill the brackets, follow-ups ...)
    cta     title, title2, lines [[verb, text], ...]
Any other adaptive slide type (list, steps, facts, limits ...) is rendered by the adaptive theme.
Long prompts shrink to fit: a small script scales the slide's --k until the content fits (carousel and Reel).
"""
import re
from themes import adaptive as A

e = A.e

# prompt-series defaults, used where the post's design leaves a field out
DEFAULT_DESIGN = {
    "palette": {"bg": "#0B0816", "bg2": "#140E26", "surface": "#191330", "ink": "#F5F2FF", "muted": "#A39DBD",
                "accent": "#C06BFF", "accent2": "#4F9BFF"},  # the channel banner's neon violet + electric blue
    "fonts": {"display": "Sora", "body": "Inter", "mono": "JetBrains Mono"},
    "display": {"weight": 700, "tracking": -2},
    "shape": {"radius": 34, "border": 2, "shadow": "soft"},
    "background": {"pattern": "dots", "pattern_opacity": 0.07, "glow": True, "gradient": True},
    "label": "pill", "prompt": "chat",
}

COPY = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>')
SPARK = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.2 6.3L20.5 10.5l-6.3 2.2L12 19l-2.2-6.3L3.5 10.5l6.3-2.2z"/>'
         '<path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/></svg>')
BOOK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M6 3h12v18l-6-4-6 4z"/></svg>')

PCSS = """
.body{overflow:hidden;justify-content:center}
.pill{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;font-family:var(--fm),monospace;font-size:21px;font-weight:700;
 letter-spacing:2.4px;text-transform:uppercase;color:var(--accent-text);border:var(--bw) solid color-mix(in srgb,var(--accent) 55%,transparent);
 background:color-mix(in srgb,var(--accent) 10%,transparent);border-radius:99px;padding:10px 22px 10px 16px}
.pill .ic{width:26px;height:26px;color:var(--accent)}.pill .ic svg{width:100%;height:100%}
/* cover */
.chead{display:flex;align-items:flex-end;gap:34px;margin-top:34px}
.bign{flex:none;font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:calc(300px*var(--k));line-height:.74;letter-spacing:-.06em;color:var(--accent)}
.cover h1{font-size:calc(var(--fs)*var(--k));padding-bottom:6px}
.cover h1 em{font-style:var(--emi);color:var(--accent)}
.cover .sub{font-size:calc(34px*var(--k))}
.stack{position:relative;height:calc(430px*var(--k));margin-top:calc(46px*var(--k))}
.mini{position:absolute;left:50%;width:720px;padding:24px 32px 22px;transform-origin:50% 0}
.mini .h{display:flex;justify-content:space-between;align-items:center;font-family:var(--fm),monospace;font-size:19px;letter-spacing:1.5px;
 text-transform:uppercase;color:var(--muted)}
.mini .h b{color:var(--accent-text)}
.mini .cp{width:26px;height:26px;color:var(--accent)}.mini .cp svg{width:100%;height:100%}
.mini .n{margin-top:12px;font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:40px;letter-spacing:var(--dt);line-height:1.05;color:var(--ink)}
.mini .ln{margin-top:18px;height:13px;border-radius:7px;background:color-mix(in srgb,var(--ink) 13%,transparent)}
.mini .ln.s{width:62%}.mini .ln b{display:inline-block;height:100%;width:24%;margin-left:30%;border-radius:7px;background:color-mix(in srgb,var(--accent) 70%,transparent)}
.mini .ft{margin-top:22px;display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:30px}
.mini .ft span{width:44px;height:44px;border-radius:50%;background:var(--ink);display:grid;place-items:center}
.works{margin-top:calc(40px*var(--k));display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.works .w{font-family:var(--fm),monospace;font-size:20px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-right:6px}
.chip{border:var(--bw) solid color-mix(in srgb,var(--ink) 20%,transparent);background:var(--surface);border-radius:99px;padding:11px 24px;font-size:25px;font-weight:650}
/* prompt */
.ph{display:flex;align-items:center;gap:26px}
.ph .no{flex:none;font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:calc(92px*var(--k));line-height:.8;letter-spacing:-.04em;color:var(--accent)}
.ph h1{font-size:calc(var(--fs)*var(--k));line-height:1}
.ph .of{font-family:var(--fm),monospace;font-size:19px;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:10px}
.prompt .sub{margin-top:calc(20px*var(--k));font-size:calc(33px*var(--k));line-height:1.3}
.pcard{position:relative;margin-top:calc(34px*var(--k));padding:calc(40px*var(--k)) 44px calc(24px*var(--k))}
.pcard .copy{position:absolute;right:26px;top:-22px;display:flex;align-items:center;gap:10px;background:var(--accent);color:var(--on-accent);
 border-radius:99px;padding:9px 20px 9px 16px;font-family:var(--fm),monospace;font-size:19px;font-weight:700;letter-spacing:1.5px}
.pcard .copy svg{width:22px;height:22px}
.ptxt{font-size:calc(var(--ps)*var(--k));line-height:1.42;font-weight:500;color:var(--ink);text-wrap:pretty}
.ptxt b{color:var(--accent-text);font-weight:800}
.ptxt b.em{color:var(--ink);font-weight:800;background:linear-gradient(transparent 62%,color-mix(in srgb,var(--accent) 38%,transparent) 62%)}
.pbar{margin-top:calc(26px*var(--k));display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:42px;font-weight:300}
.pbar span{width:60px;height:60px;border-radius:50%;background:var(--ink);display:grid;place-items:center}
.demo{margin-top:calc(26px*var(--k))}
.dlab{font-family:var(--fm),monospace;font-size:18px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);
 display:flex;align-items:center;gap:10px;margin-bottom:12px}
.dlab svg{width:22px;height:22px;color:var(--accent2)}
.reply{padding:calc(24px*var(--k)) 32px;border-radius:var(--r);background:color-mix(in srgb,var(--accent2) 9%,var(--bg));
 border:var(--bw) dashed color-mix(in srgb,var(--accent2) 45%,transparent)}
.reply div{font-size:calc(27px*var(--k));line-height:1.38;color:var(--ink);padding-left:30px;position:relative}
.reply div+div{margin-top:8px}
.reply div:before{content:"";position:absolute;left:2px;top:.55em;width:11px;height:11px;border-radius:3px;background:var(--accent2)}
.ba{display:flex;align-items:center;gap:18px}
.ba .pan{flex:1;position:relative;border-radius:calc(var(--r)*.7);overflow:hidden;aspect-ratio:400/250;max-height:calc(290px*var(--k));
 border:var(--bw) solid color-mix(in srgb,var(--ink) 14%,transparent);background:var(--surface)}
.ba .pan svg{width:100%;height:100%;display:block}
.ba .pan i{position:absolute;left:14px;top:12px;font-style:normal;font-family:var(--fm),monospace;font-size:17px;font-weight:700;letter-spacing:1.5px;
 text-transform:uppercase;background:rgba(0,0,0,.62);color:#fff;border-radius:8px;padding:5px 10px}
.ba .pan.after i{background:var(--accent);color:var(--on-accent)}
.ba .to{flex:none;color:var(--accent);width:40px;height:40px}.ba .to svg{width:100%;height:100%}
.tip{margin-top:calc(26px*var(--k));display:flex;gap:16px;align-items:flex-start;font-size:calc(27px*var(--k));line-height:1.36;color:var(--muted)}
.tip .k{flex:none;font-family:var(--fm),monospace;font-size:18px;font-weight:700;letter-spacing:1px;color:var(--on-accent);background:var(--accent);
 border-radius:calc(var(--r)*.25);padding:5px 10px;margin-top:3px}
/* howto */
.hw{margin-top:calc(44px*var(--k));display:flex;flex-direction:column;gap:18px}
.hw .it{display:flex;gap:26px;align-items:flex-start;padding:calc(28px*var(--k)) 34px}
.hw .n{flex:none;width:58px;height:58px;border-radius:50%;background:var(--accent);color:var(--on-accent);display:grid;place-items:center;
 font-family:var(--fd),sans-serif;font-weight:var(--dw);font-size:30px}
.hw .t{font-size:calc(35px*var(--k));font-weight:700;letter-spacing:-.3px;line-height:1.2}
.hw .d{margin-top:6px;font-size:calc(27px*var(--k));color:var(--muted);line-height:1.35}
.howto h1{margin-top:28px;font-size:calc(var(--fs)*var(--k))}
.cta h1{font-size:calc(var(--fs)*var(--k))}
"""

FIT = """<script>(()=>{const b=document.querySelector('.body'),r=document.documentElement;
for(let k=1;k>=0.6;k-=0.03){r.style.setProperty('--k',k.toFixed(2));if(b.scrollHeight<=b.clientHeight+1)break;}})();</script>"""

TO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def resolve(data):
    """adaptive.resolve with the prompt-series defaults under the post's own design."""
    d = data.get("design") or {}
    merged = {k: ({**v, **(d.get(k) or {})} if isinstance(v, dict) else d.get(k, v)) for k, v in DEFAULT_DESIGN.items()}
    merged.update({k: v for k, v in d.items() if k not in DEFAULT_DESIGN})
    return A.resolve({**data, "design": merged})


def pill(text, ds, icon=None):
    return f'<div class="pill"><span class="ic">{icon or ds["icon"] or COPY}</span>{e(text)}</div>'


def prompt_size(text, has_extra):
    n = len(text)
    ps = 42 if n <= 170 else 38 if n <= 260 else 35 if n <= 360 else 32
    return ps - (3 if has_extra else 0)


def demo(d, ds):
    if not d: return ""
    if d.get("kind") == "before_after":
        b, a = A.clean_svg(d.get("before")), A.clean_svg(d.get("after"))
        if not (b and a): return ""
        lb, la = (d.get("labels") or ["Before", "After"])[:2]
        return (f'<div class="demo ba"><div class="pan before"><i>{e(lb)}</i>{b}</div><div class="to">{TO}</div>'
                f'<div class="pan after"><i>{e(la)}</i>{a}</div></div>')
    lines = "".join(f"<div>{A.rich(x)}</div>" for x in (d.get("lines") or [])[:4])
    return f'<div class="demo"><div class="dlab">{SPARK}{e(d.get("label", "What you get"))}</div><div class="reply">{lines}</div></div>' if lines else ""


def slide(s, n, slides, data, ds):
    t = s["type"]
    prompts = [x for x in slides if x["type"] == "prompt"]
    if t == "cover":
        title = e(s["title"])
        if s.get("em") and e(s["em"]) in title: title = title.replace(e(s["em"]), f'<em>{e(s["em"])}</em>', 1)
        count = str(s.get("count") or len(prompts))
        cards = ""
        deck = prompts[:3]
        for i, p in enumerate(deck):  # a deck seen from the front: back cards peek out above, the last one on top
            k = len(deck) - 1 - i
            cards += (f'<div class="mini box" style="top:{i * 96}px;transform:translateX(-50%) scale({1 - k * 0.06:.2f});z-index:{i}">'
                      f'<div class="h"><span>Prompt <b>{i + 1:02d}</b></span><span class="cp">{COPY}</span></div>'
                      f'<div class="n">{e(p.get("name", ""))}</div><div class="ln"></div><div class="ln s"><b></b></div>'
                      f'<div class="ft">+<span>{A.SEND}</span></div></div>')
        tools = s.get("tools") or []
        works = (f'<div class="works"><span class="w">Works in</span>{"".join(f"<div class=chip>{e(x)}</div>" for x in tools)}</div>' if tools else "")
        fs = A.size(s["title"], 104, ds)
        return (f'{pill(s.get("kicker") or "Copy-paste prompts", ds)}'
                f'<div class="chead"><div class="bign">{e(count)}</div><h1 style="--fs:{fs}px">{title}</h1></div>'
                f'<div class="sub">{e(s.get("sub", ""))}</div><div class="stack">{cards}</div>{works}')
    if t == "prompt":
        idx = prompts.index(s) + 1
        name = s.get("name") or s.get("title", "")
        extra = bool(s.get("demo")) or bool(s.get("tip"))
        tip = f'<div class="tip"><span class="k">TIP</span><span>{A.rich(s["tip"])}</span></div>' if s.get("tip") else ""
        return (f'<div class="ph"><div class="no">{idx:02d}</div><div><div class="of">Prompt {idx} of {len(prompts)}</div>'
                f'<h1 style="--fs:{A.size(name, 84, ds)}px">{e(name)}</h1></div></div>'
                + (f'<div class="sub">{e(s["sub"])}</div>' if s.get("sub") else "")
                + f'<div class="pcard box" style="--ps:{prompt_size(s["prompt"], extra)}px"><div class="copy">{COPY}COPY</div>'
                  f'<p class="ptxt">{A.hl(s["prompt"])}</p><div class="pbar">+<span>{A.SEND}</span></div></div>'
                + demo(s.get("demo"), ds) + tip)
    if t == "howto":
        its = "".join(f'<div class="it box"><div class="n">{i}</div><div><div class="t">{A.rich(a)}</div><div class="d">{A.rich(d)}</div></div></div>'
                      for i, (a, d) in enumerate(s["items"], 1))
        return (f'{pill(s.get("label") or "How to use them", ds, BOOK)}<h1 style="--fs:{A.size(s["title"], 96, ds)}px">{e(s["title"])}</h1>'
                f'<div class="hw">{its}</div>')
    if t == "cta":
        rows = "".join(f'<div class="row box"><div class="v">{e(a)}</div><div class="d">{e(b)}</div></div>' for a, b in s["lines"])
        return (f'{pill("Prompt pack", ds)}<h1 style="margin-top:30px;--fs:{A.size(s["title"] + s.get("title2", ""), 112, ds)}px">'
                f'{e(s["title"])}<br><span>{e(s.get("title2", ""))}</span></h1>'
                f'<div class="rows">{rows}</div><div class="big">New prompts <span>every week</span> → {e(data["handle"])}</div>')
    return A.slide(s, n, slides, data, ds)


def render(data):
    ds = resolve(data); style = A.css(ds) + PCSS + ":root{--k:1}"
    slides = data["slides"]; total = len(slides); pages = []
    for n, s in enumerate(slides, 1):
        body = slide(s, n, slides, data, ds)
        sw = f'<div class="swipe">Swipe <span>{A.ARROW}</span></div>' if n < total else "<div>Save · Share</div>"
        glow = '<div class="glow"></div>' if ds["background"]["glow"] else ""
        deco = f'<div class="deco">{ds["deco"]}</div>' if ds["deco"] else ""
        top = (f'<div class="top"><div class="brand"><div class="logo">{e(data["brand"][0])}</div>{e(data["brand"])}</div>'
               f'<div class="topic">{e(data.get("topic", ""))}</div><div class="count">{n:02d}/{total:02d}</div></div>')
        left = f'{e(data["handle"])} · Save for later'
        pages.append(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{style}</style></head>'
                     f'<body class="{s["type"]} lab-{ds["label"]}"><div class="bgp"></div>{glow}{deco}'
                     f'<div class="wrap">{top}<div class="body">{body}</div><div class="foot"><div>{left}</div>{sw}</div></div>{FIT}</body></html>')
    return pages


# ---- Reel (9:16) settings used by reel.py; configure(data) sets the per-post colors ----
ACCENT = DEFAULT_DESIGN["palette"]["accent"]
CC_ACTIVE = ACCENT
ANIM_SEL = ".pill,.bign,.body h1,.sub,.stack,.works,.ph .no,.pcard,.demo,.tip,.it,.row,.big," + A.ANIM_SEL
TYPE_SEL = ".ptxt"
DRAW_SEL = ".pan.after"
REEL_CSS = """
.wrap{inset:190px 76px 330px !important}
.top .topic{display:none}
.swipe{display:none !important}
.foot{font-size:0 !important}
"""


def configure(data):
    """Per-post Reel colors (reel.py calls this before rendering)."""
    global ACCENT, CC_ACTIVE
    p = resolve(data)["palette"]
    ACCENT = p["accent"]
    CC_ACTIVE = A.ensure(p["accent"], "#0A0A0E", 4.5)
    globals()["REEL_CSS"] = REEL_CSS + f"\n.caret{{background:{p['accent']}}}\n"
