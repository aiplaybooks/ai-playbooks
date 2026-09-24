"""Cover image for a carousel post: a freely licensed photo of the person the post is about (Wikimedia Commons),
or a Flux scene (Forge API) when no person fits. carousel.py then draws the hook cover (themes/hookcover.py) with it.

Usage:
    python cover.py content/<post>.json

Reads the post's `cover` block (written by the write step):
    headline   the hook, e.g. "Claude can now teach you any language. Here are 7 prompts to try:"
    em         part of the headline to highlight (optional)
    person     "Sam Altman" | null: someone well known and directly tied to the topic (the company's CEO ...)
    photo_file optional Commons file title to force ("File:....jpg"), e.g. after the owner asked for another photo
    scene      Flux prompt for when there is no person (English, no text, no logos, no real people)
    focus      optional CSS background-position of the image (default "50% 20%": faces sit in the upper part)
Writes output/<post>/cover_image.jpg and, for photos, `cover.photo` = {file, page, author, license, license_url} back
into the JSON + a credit line in the caption ("📷 Photo: <author> · <license> via Wikimedia Commons").
Only licenses that allow reuse with edits (crop + text): CC BY, CC BY-SA, CC0, public domain. No NC/ND.
"""
import sys, re, json, time, base64, pathlib, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).parent.resolve()
UA = {"User-Agent": "AIPlaybooks/0.1 (https://aiplaybooks.github.io/ai-playbooks/; yurttas.cihat55@gmail.com)"}
FORGE = "http://127.0.0.1:7860"
FLUX = "flux1-schnell-fp8.safetensors"
OK_LICENSE = re.compile(r"^(CC BY(-SA)? [\d.]+|CC0|Public domain|PD)", re.I)
CREDIT = "📷 Photo:"


def commons(params):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r: return json.load(r)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s or ""))).strip()


def candidates(person, forced=None):
    q = {"prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1600}
    if forced: r = commons({"action": "query", "titles": forced, **q})
    else: r = commons({"action": "query", "generator": "search", "gsrsearch": f'filetype:bitmap "{person}"',
                       "gsrnamespace": 6, "gsrlimit": 25, **q})
    out = []
    for p in (r.get("query", {}).get("pages") or {}).values():
        if "imageinfo" not in p: continue
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        lic = plain(m.get("LicenseShortName", {}).get("value"))
        if not OK_LICENSE.match(lic) or re.search(r"\b(NC|ND)\b", lic): continue
        w, h = ii["width"], ii["height"]
        if min(w, h) < 700: continue
        t = p["title"].lower(); name = person.lower() if person else ""
        score = 0
        if name and all(tok in t for tok in name.split()): score += 50
        if "crop" in t: score += 15                                   # tight portraits are usually "(cropped)"
        if 0.6 <= w / h <= 1.1: score += 15                            # portrait / square: a face that fills the cover
        yr = [int(y) for y in re.findall(r"(20[12]\d)", t)]
        score += (max(yr) - 2010) if yr else 0                         # newer photos first
        if re.search(r"logo|signature|building|headquarters|poster|screenshot", t): score -= 60
        out.append({"score": score, "file": p["title"], "page": ii["descriptionurl"], "url": ii.get("thumburl") or ii["url"],
                    "author": re.sub(r"^(photo(graph)?(er)?|author|by)\s*[:\-]\s*", "", plain(m.get("Artist", {}).get("value")), flags=re.I)[:80] or "unknown", "license": lic,
                    "license_url": plain(m.get("LicenseUrl", {}).get("value")), "size": [w, h]})
    return sorted(out, key=lambda x: -x["score"])


def photo(person, forced, dest):
    c = candidates(person, forced)
    if not c: raise SystemExit(f"no freely licensed Commons photo found for {forced or person!r}")
    best = c[0]
    with urllib.request.urlopen(urllib.request.Request(best["url"], headers=UA), timeout=60) as r: dest.write_bytes(r.read())
    print(f"photo: {best['file']} ({best['license']}, {best['author']}) score {best['score']}")
    return {k: best[k] for k in ("file", "page", "author", "license", "license_url")}


def flux(prompt, dest):
    body = {"prompt": prompt + ", cinematic, high detail, no text, no logos, no watermark", "steps": 4, "cfg_scale": 1,
            "distilled_cfg_scale": 3.5, "sampler_name": "Euler", "scheduler": "Simple", "width": 896, "height": 1120,
            "override_settings": {"sd_model_checkpoint": FLUX, "forge_additional_modules": []}}
    req = urllib.request.Request(FORGE + "/sdapi/v1/txt2img", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=1800) as r: img = json.load(r)["images"][0]
    except urllib.error.URLError as ex:
        raise SystemExit(f"Forge is not running at {FORGE} ({ex.reason}): start it from Pinokio, then retry") from None
    dest.write_bytes(base64.b64decode(img))
    print(f"flux: {time.time() - t:.0f}s")


def credit_caption(cap, ph):
    lines = [l for l in cap.split("\n") if not l.startswith(CREDIT)]
    line = f"{CREDIT} {ph['author']} · {ph['license']} via Wikimedia Commons"
    tags = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].lstrip().startswith("#")), None)
    if tags is None: return "\n".join(lines).rstrip() + "\n\n" + line
    return "\n".join(lines[:tags]).rstrip() + "\n\n" + line + "\n\n" + "\n".join(lines[tags:])


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    content = pathlib.Path(sys.argv[1]).resolve()
    data = json.loads(content.read_text(encoding="utf-8"))
    cv = data.get("cover") or {}
    if not cv.get("headline"): sys.exit("content JSON has no cover.headline")
    out = ROOT / "output" / content.stem; out.mkdir(parents=True, exist_ok=True)
    dest = out / "cover_image.jpg"
    if cv.get("person") or cv.get("photo_file"):
        cv["photo"] = photo(cv.get("person"), cv.get("photo_file"), dest)
        data["caption"] = credit_caption(data.get("caption", ""), cv["photo"])
    else:
        if not cv.get("scene"): sys.exit("cover needs `person` or `scene`")
        cv.pop("photo", None)
        data["caption"] = "\n".join(l for l in data.get("caption", "").split("\n") if not l.startswith(CREDIT))
        flux(cv["scene"], dest)
    data["cover"] = cv
    content.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", dest)


if __name__ == "__main__":
    main()
