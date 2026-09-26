"""Cover image for a carousel post, always a real photo (image generation is OFF until the owner turns it back on):
1. a freely licensed photo of the well-known person the post is about (Wikimedia Commons), else
2. a freely licensed photo that fits the topic (Openverse: Flickr, Wikimedia and other open collections), else
3. the step fails, so the owner can revise the post (e.g. give another `photo_query` or a `photo_url`).
carousel.py then draws the hook cover (themes/hookcover.py) with it.

Usage:
    python cover.py content/<post>.json

Reads the post's `cover` block (written by the write step):
    headline    the hook, e.g. "Claude can now teach you any language. Here are 7 prompts to try:"
    em          part of the headline to highlight (optional)
    person      "Sam Altman" | null: someone well known and directly tied to the topic (the company's CEO ...)
    photo_file  optional Commons file title to force ("File:....jpg"), e.g. after the owner asked for another photo
    photo_query 2-4 English search words for a topic photo ("laptop night desk"), or a list of them, best first
    photo_pick  {url, page, author, license, license_url, source}: the photo the write step chose after looking at the
                previews of `python cover.py --search <post name> "query one" "query two"` (output/<post>/photo_cands/)
    photo_url   optional: an image URL the owner picked (used as is; `photo_credit` = the credit line text)
    scene       old field (Flux prompt); only used as a last search query when photo_query is missing
    focus       optional CSS background-position of the image (default "50% 20%": faces sit in the upper part)
Writes output/<post>/cover_image.jpg and `cover.photo` = {file, page, author, license, license_url, source} back into
the JSON + a credit line in the caption ("📷 Photo: <author> · <license> via <source>").
Licenses: only ones that allow reuse with edits (crop + text): CC BY, CC BY-SA, CC0, public domain. No NC/ND.
A photo already used on another post's cover is skipped.
"""
import sys, re, json, time, base64, pathlib, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).parent.resolve()
UA = {"User-Agent": "AIPlaybooks/0.1 (https://aiplaybooks.github.io/ai-playbooks/; yurttas.cihat55@gmail.com)"}
FORGE = "http://127.0.0.1:7860"
FLUX = "flux1-schnell-fp8.safetensors"
FLUX_ENABLED = False  # owner, 2026-09-26: no image generation until they say otherwise
OPENVERSE = "https://api.openverse.org/v1/images/"
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


def used_photos(skip):
    """Photo pages already used on other posts' covers."""
    out = set()
    for f in (ROOT / "content").rglob("*.json"):
        if f.resolve() == skip: continue
        try: ph = (json.loads(f.read_text(encoding="utf-8")).get("cover") or {}).get("photo") or {}
        except ValueError: continue
        if ph.get("page"): out.add(ph["page"])
    return out


def openverse(query):
    """Freely licensed photos for a topic (reuse with edits allowed), best first."""
    q = urllib.parse.urlencode({"q": query, "license_type": "commercial,modification", "page_size": 20})
    try:
        with urllib.request.urlopen(urllib.request.Request(OPENVERSE + "?" + q, headers=UA), timeout=40) as r: res = json.load(r)["results"]
    except (urllib.error.URLError, ValueError, KeyError, TimeoutError) as ex:
        print(f"openverse {query!r}: {ex}"); return []
    out = []
    for x in res:
        w, h = x.get("width") or 0, x.get("height") or 0
        lic = x.get("license", ""); ver = x.get("license_version") or ""
        if re.search(r"nc|nd", lic) or min(w, h) < 700: continue
        name = {"cc0": "CC0", "pdm": "Public domain"}.get(lic) or f"CC {lic.upper()} {ver}".strip()
        words = [t for t in re.findall(r"[a-z]+", query.lower()) if len(t) > 2]
        text = " ".join([(x.get("title") or "").lower()] + [(t.get("name") or "").lower() for t in x.get("tags") or []])
        hit = sum(w_[:5] in text for w_ in words) / max(1, len(words))  # how well it matches the topic
        if hit < 0.5: continue
        score = hit * 40 + min(min(w, h), 2000) / 100 + (10 if 0.8 <= w / h <= 1.8 else 0)
        if re.search(r"logo|screenshot|poster|diagram|map|drawing", (x.get("title") or "").lower()): score -= 30
        src = {"wikimedia": "Wikimedia Commons", "flickr": "Flickr", "stocksnap": "StockSnap", "rawpixel": "rawpixel"}.get(x.get("source"), x.get("source") or "Openverse")
        out.append({"score": score, "file": x.get("title") or "photo", "page": x.get("foreign_landing_url") or x["url"], "url": x["url"],
                    "id": x.get("id"), "author": (x.get("creator") or "unknown")[:80], "license": name, "license_url": x.get("license_url") or "", "source": src})
    return sorted(out, key=lambda c: -c["score"])


def fetch(cands, dest, used):
    """Download the best candidate not used on another cover yet."""
    for best in cands:
        if best["page"] in used: continue
        try:
            with urllib.request.urlopen(urllib.request.Request(best["url"], headers=UA), timeout=60) as r: dest.write_bytes(r.read())
        except (urllib.error.URLError, TimeoutError) as ex:
            print(f"download failed {best['url']}: {ex}"); continue
        src = best.get("source") or "Wikimedia Commons"
        print(f"photo: {best['file']} ({best['license']}, {best['author']}, {src})")
        return {**{k: best[k] for k in ("file", "page", "author", "license", "license_url")}, "source": src}
    return None


def photo(person, forced, dest, used=()):
    return fetch(candidates(person, forced), dest, used)


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
    line = (f"{CREDIT} {ph['author']} · {ph['license']} via {ph.get('source') or 'Wikimedia Commons'}" if ph.get("license")
            else f"{CREDIT} {ph['author']}")
    tags = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].lstrip().startswith("#")), None)
    if tags is None: return "\n".join(lines).rstrip() + "\n\n" + line
    return "\n".join(lines[:tags]).rstrip() + "\n\n" + line + "\n\n" + "\n".join(lines[tags:])


def search(post, queries):
    """For the write step: download the top topic photos as previews (output/<post>/photo_cands/NN.jpg) and print
    each one's `photo_pick` JSON, so Claude can look at them and put the best into cover.photo_pick."""
    out = ROOT / "output" / post / "photo_cands"; out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.jpg"): f.unlink()
    used = used_photos(ROOT / "content" / f"{post}.json"); n = 0
    per = max(2, -(-8 // max(1, len(queries))))  # spread the 8 previews over the queries
    for q in queries:
        k = 0
        for c in openverse(q):
            if c["page"] in used or n >= 8 or k >= per: continue
            thumb = f"https://api.openverse.org/v1/images/{c['id']}/thumb/" if c.get("id") else c["url"]
            try:
                with urllib.request.urlopen(urllib.request.Request(thumb, headers=UA), timeout=40) as r: (out / f"{n + 1:02d}.jpg").write_bytes(r.read())
            except (urllib.error.URLError, TimeoutError): continue
            n += 1; k += 1; used = {*used, c["page"]}
            print(f"{n:02d} [{q}] " + json.dumps({k: c[k] for k in ("url", "page", "author", "license", "license_url", "source", "file")}, ensure_ascii=False))
    print(f"{n} previews in {out.relative_to(ROOT)}" if n else "nothing found: try other words (2-3 plain English nouns)")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1] == "--search": return search(sys.argv[2], sys.argv[3:])
    content = pathlib.Path(sys.argv[1]).resolve()
    data = json.loads(content.read_text(encoding="utf-8"))
    cv = data.get("cover") or {}
    if not cv.get("headline"): sys.exit("content JSON has no cover.headline")
    out = ROOT / "output" / content.stem; out.mkdir(parents=True, exist_ok=True)
    dest = out / "cover_image.jpg"
    used = used_photos(content); ph = None
    pick = cv.get("photo_pick")
    if pick and pick.get("url"):  # chosen by the write step from `cover.py --search` previews
        ph = fetch([pick], dest, ())
    if not ph and cv.get("photo_url"):  # the owner's own pick
        with urllib.request.urlopen(urllib.request.Request(cv["photo_url"], headers=UA), timeout=60) as r: dest.write_bytes(r.read())
        ph = {"file": cv["photo_url"], "page": cv["photo_url"], "author": cv.get("photo_credit") or "", "license": "", "source": ""}
        print(f"photo: {cv['photo_url']} (owner's pick)")
    if not ph and (cv.get("person") or cv.get("photo_file")):
        ph = photo(cv.get("person"), cv.get("photo_file"), dest, used)
        if not ph: print(f"no freely licensed Commons photo of {cv.get('photo_file') or cv['person']!r}: searching a topic photo")
    if not ph:
        qs = cv.get("photo_query") or []
        qs = [qs] if isinstance(qs, str) else list(qs)
        if cv.get("scene"): qs.append(" ".join(re.findall(r"[A-Za-z]+", cv["scene"].split(",")[0])[-3:]))
        for q in qs:
            ph = fetch(openverse(q), dest, used)
            if ph: break
    if ph:
        cv["photo"] = ph
        cap = "\n".join(l for l in data.get("caption", "").split("\n") if not l.startswith(CREDIT))
        data["caption"] = credit_caption(cap, ph) if ph.get("author") else cap
    elif FLUX_ENABLED and cv.get("scene"):
        cv.pop("photo", None)
        data["caption"] = "\n".join(l for l in data.get("caption", "").split("\n") if not l.startswith(CREDIT))
        flux(cv["scene"], dest)
    else:
        sys.exit("Kapak için uygun fotoğraf bulunamadı: revize et, cover.photo_query (2-4 İngilizce kelime) ya da photo_url ver")
    data["cover"] = cv
    content.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", dest)


if __name__ == "__main__":
    main()
