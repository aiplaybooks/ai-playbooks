"""The page the Instagram DM bot sends (owner, 2026-09-26): one page per post on GitHub Pages, p/<post>/index.html,
with everything the post promised, copy-ready: the prompts (prompt packs, clip prompts from `comments`), or the
slides' steps / lists for other posts. Mobile first (it opens in Instagram's in-app browser), no external files.

Usage:
    python packpage.py content/<post>.json [out.html]      (publish.py's upload step calls page_html())
"""
import sys, re, json, html, pathlib

ROOT = pathlib.Path(__file__).parent.resolve()
PAGES_URL = "https://aiplaybooks.github.io/ai-playbooks"
IG = "https://www.instagram.com/aiplaybooks.daily/"
e = html.escape


def rich(t):
    t = e(t or "")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(\[[^\]]+\])", r'<span class="ph">\1</span>', t)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", t)


def blocks(data):
    """(kind, title, sub, body) per useful slide, in order."""
    out = []
    if data.get("kind") == "clip":
        for i, c in enumerate(data.get("comments") or [], 1):
            head, _, body = c.partition("\n\n")
            out.append(("prompt", head.strip(" :") if body else f"Prompt {i}", "", body or c))
        return out
    for s in data.get("slides", []):
        t = s.get("type")
        if t == "prompt":
            out.append(("prompt", s.get("name") or s.get("title") or s.get("label") or "Prompt", s.get("sub") or s.get("note") or "",
                        s.get("prompt", "")))
            if s.get("tip"): out.append(("tip", "Tip", "", s["tip"]))
        elif t in ("steps", "howto", "list"):
            items = s.get("steps") or s.get("items") or []
            out.append(("list", s.get("title", ""), s.get("label", ""), "\n".join(f"{a} — {b}" for a, b in items)))
        elif t in ("facts", "limits"):
            items = s.get("items") or []
            lines = [f"{x[0]}: {x[1]}" if isinstance(x, list) and len(x) > 1 else str(x) for x in items]
            out.append(("list", s.get("title", ""), s.get("label", ""), "\n".join(lines)))
        elif t == "compare":
            for c in s.get("cols", []): out.append(("list", c.get("name", ""), s.get("title", ""), "\n".join(c.get("points", []))))
        elif t == "stat":
            out.append(("note", s.get("value", ""), s.get("title", ""), s.get("sub", "")))
    return out


def page_html(data, name, cover_url=None):
    cv = data.get("cover") or {}
    title = cv.get("headline") or data.get("topic") or name
    n = 0; cards = []
    for kind, head, sub, body in blocks(data):
        if kind == "prompt":
            n += 1
            cards.append(f'<section class="card"><div class="no">{n:02d}</div><h2>{e(head)}</h2>' + (f'<p class="sub">{e(sub)}</p>' if sub else "")
                         + f'<div class="pbox"><p class="pt">{rich(body)}</p><button class="cp" data-t="{e(body)}">Copy prompt</button></div></section>')
        elif kind == "tip":
            cards.append(f'<p class="tip"><b>TIP</b> {rich(body)}</p>')
        elif body.strip():
            lis = "".join(f"<li>{rich(x)}</li>" for x in body.split("\n") if x.strip())
            cards.append(f'<section class="card"><h2>{e(head)}</h2>' + (f'<p class="sub">{e(sub)}</p>' if sub else "") + f"<ul>{lis}</ul></section>")
    img = f'<img class="cv" src="{e(cover_url)}" alt="">' if cover_url else ""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(data.get("topic") or title)} · AI Playbooks</title><meta name="description" content="{e(title)}">
<meta property="og:title" content="{e(title)}">{f'<meta property="og:image" content="{e(cover_url)}">' if cover_url else ""}
<style>
:root{{--bg:#0B0816;--card:#161127;--ink:#F5F2FF;--muted:#A39DBD;--acc:#C06BFF;--acc2:#4F9BFF;--line:#2A2340}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;padding:0 16px 64px}}
.wrap{{max-width:680px;margin:0 auto}}
.top{{display:flex;align-items:center;gap:10px;padding:18px 0;font-weight:800;letter-spacing:.3px}}
.top i{{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,var(--acc),var(--acc2));display:grid;place-items:center;font-style:normal}}
.cv{{width:100%;border-radius:18px;display:block;margin:4px 0 18px}}
h1{{font-size:26px;line-height:1.2;letter-spacing:-.3px}}
.lead{{color:var(--muted);margin:10px 0 22px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;margin:14px 0}}
.no{{color:var(--acc);font-weight:900;font-size:22px}}
h2{{font-size:19px;line-height:1.25;margin:2px 0 4px}}
.sub{{color:var(--muted);font-size:15px;margin-bottom:10px}}
.pbox{{background:#0E0A1C;border:1px solid var(--line);border-radius:14px;padding:14px;margin-top:8px}}
.pt{{white-space:pre-wrap;font-size:15.5px}}
.pt b{{color:#fff}} .ph{{color:var(--acc);font-weight:700}}
.cp{{margin-top:12px;width:100%;border:0;border-radius:12px;padding:12px;font-weight:800;font-size:15px;color:#fff;
 background:linear-gradient(135deg,var(--acc),var(--acc2));cursor:pointer}}
.cp.ok{{background:#1f9d62}}
ul{{padding-left:20px}} li{{margin:6px 0}}
code{{background:#0E0A1C;border-radius:6px;padding:1px 6px}}
.tip{{color:var(--muted);font-size:15px;margin:-4px 4px 14px}} .tip b{{color:var(--acc2);margin-right:6px}}
.follow{{display:block;text-align:center;margin:26px 0 8px;padding:14px;border-radius:14px;border:1px solid var(--acc);color:var(--ink);
 text-decoration:none;font-weight:800}}
.foot{{color:var(--muted);font-size:13px;text-align:center}}
</style></head><body><div class="wrap">
<div class="top"><i>A</i>AI Playbooks</div>{img}
<h1>{e(title)}</h1><p class="lead">Thanks for following! Everything from the post, ready to copy. Fill in the [BRACKETS] with your details.</p>
{"".join(cards)}
<a class="follow" href="{IG}">New playbook every day → @aiplaybooks.daily</a>
<p class="foot">AI Playbooks · <a href="{PAGES_URL}/" style="color:var(--muted)">aiplaybooks.github.io</a></p>
</div><script>
document.querySelectorAll('.cp').forEach(b=>b.onclick=async()=>{{const t=b.dataset.t;
 try{{await navigator.clipboard.writeText(t)}}catch(_){{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}
 b.textContent='Copied ✓';b.classList.add('ok');setTimeout(()=>{{b.textContent='Copy prompt';b.classList.remove('ok')}},1800)}});
</script></body></html>"""


def main():
    src = pathlib.Path(sys.argv[1]); data = json.loads(src.read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "output" / src.stem / "page.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_html(data, src.stem), encoding="utf-8"); print("wrote", out)


if __name__ == "__main__":
    main()
