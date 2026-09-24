"""Render an Instagram carousel (1080x1350 PNGs) from a content JSON.

Usage:
    python carousel.py content/2026-09-24_claude-tradingview.json [--theme ledger]

Output: output/<content-name>/slide_01.png ... + contact.png (overview sheet)
"""
import sys, json, pathlib, importlib, argparse
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))


def load(content_path, theme_name=None):
    data = json.loads(pathlib.Path(content_path).read_text(encoding="utf-8"))
    theme = importlib.import_module(f"themes.{theme_name or data['theme']}")
    return data, theme


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content"); ap.add_argument("--theme")
    a = ap.parse_args()
    data, theme = load(a.content, a.theme)
    out = ROOT / "output" / pathlib.Path(a.content).stem
    out.mkdir(parents=True, exist_ok=True)
    pages = theme.render(data)
    img = out / "cover_image.jpg"
    if (data.get("cover") or {}).get("headline") and img.exists():  # photo + hook cover (cover.py) replaces the theme's
        from themes import hookcover
        pages[0] = hookcover.render(data, img)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(pages, 1):
            f = out / f"slide_{n:02d}.html"; f.write_text(h, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"slide_{n:02d}.png"))
        br.close()
    cols = 5 if len(pages) > 9 else 3; rows = -(-len(pages) // cols)
    sheet = Image.new("RGB", (cols * 370 + 10, rows * 460 + 10), "white")
    for k in range(len(pages)):
        im = Image.open(out / f"slide_{k+1:02d}.png").resize((360, 450))
        sheet.paste(im, (10 + (k % cols) * 370, 10 + (k // cols) * 460))
    sheet.save(out / "contact.png")
    print(f"rendered {len(pages)} slides -> {out}")


if __name__ == "__main__":
    main()
