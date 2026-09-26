"""Caption rules in code: tidy + check the per-platform captions the caption agent writes (prompts/caption.md).

Content JSON:
    "captions": {"instagram": "...", "facebook": "...",
                 "youtube": {"title": "...", "description": "...", "tags": ["...", ...]}}
    "caption": same text as captions.instagram (older code and the UI read it)

Usage:
    python captions.py check content/<post>.json     prints problems (exit 1 if any), used by the agent + the Studio
    python captions.py tidy content/<post>.json      fixes spacing / removes source lines in place

publish.py uses text_for(data, platform) and yt fields from here, always tidied.
"""
import sys, re, json, pathlib

LIMITS = {"instagram": {"chars": 2200, "tags": 5, "first": 125},   # IG: max 5 hashtags since Dec 2025
          "facebook": {"chars": 5000, "tags": 5, "first": 150},
          "youtube": {"chars": 4800, "tags": 5, "first": 120, "title": 100}}
SOURCE_LINE = re.compile(r"^\s*(📷\s*)?(photo|source|credit|image|video|via)\s*[:：]", re.I)


def tidy(text):
    """Readable paragraphs: no trailing spaces, no source/credit lines, max one blank line, hashtags on one line."""
    lines = [l.rstrip() for l in (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    lines = [l for l in lines if not SOURCE_LINE.match(l)]
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    # a hashtag-only block at the end becomes one line
    m = re.search(r"((?:\n\s*#\w+(?:\s+#\w+)*\s*)+)$", "\n" + out)
    if m and m.group(1).count("\n") > 1:
        tags = " ".join(re.findall(r"#\w+", m.group(1)))
        out = out[: len(out) - len(m.group(1)) + 1].rstrip() + "\n\n" + tags
    return out


def tags_in(text):
    return re.findall(r"#\w+", text or "")


def text_for(data, platform):
    """Caption text for instagram / facebook (falls back to the old single `caption`)."""
    c = (data.get("captions") or {}).get(platform) or data.get("caption", "")
    return tidy(c)


def check(data):
    probs = []
    caps = data.get("captions") or {}
    for pf in ("instagram", "facebook"):
        t = caps.get(pf)
        if not t: probs.append(f"captions.{pf} is missing"); continue
        lim = LIMITS[pf]; tidied = tidy(t)
        if tidied != t.strip(): probs.append(f"{pf}: not tidy (source/credit lines, extra blank lines or trailing spaces): run `python captions.py tidy`")
        if len(t) > lim["chars"]: probs.append(f"{pf}: {len(t)} chars (max {lim['chars']})")
        n = len(tags_in(t))
        if n > lim["tags"]: probs.append(f"{pf}: {n} hashtags (max {lim['tags']})")
        if n < 2: probs.append(f"{pf}: only {n} hashtags (use 3-5)")
        first = t.strip().split("\n", 1)[0]
        if len(first) > lim["first"]: probs.append(f"{pf}: first line is {len(first)} chars; the hook must fit before 'more' (<= {lim['first']})")
        paras = [p for p in t.split("\n\n") if p.strip()]
        if len(paras) < 3: probs.append(f"{pf}: {len(paras)} paragraph(s); use short paragraphs separated by a blank line")
        long = [p[:40] for p in paras if len(p) > 330 and not p.lstrip().startswith("#")]
        if long: probs.append(f"{pf}: paragraph too long (> 330 chars): {long[0]!r}...")
        if "?" not in t and not re.search(r"(?i)\bcomment\b", t): probs.append(f"{pf}: no question / comment prompt for the audience")
    yt = caps.get("youtube") or {}
    if not yt: probs.append("captions.youtube is missing")
    else:
        if not yt.get("title"): probs.append("youtube.title is missing")
        elif len(yt["title"]) > LIMITS["youtube"]["title"]: probs.append(f"youtube.title is {len(yt['title'])} chars (max 100 incl. #Shorts)")
        if re.search(r"[<>]", (yt.get("title") or "") + (yt.get("description") or "")): probs.append("youtube: < and > are not allowed")
        n = len(tags_in(yt.get("title", "") + " " + yt.get("description", "")))
        if n > 15: probs.append(f"youtube: {n} hashtags in title + description: over 15 YouTube ignores ALL of them")
        if len(yt.get("description") or "") > LIMITS["youtube"]["chars"]: probs.append("youtube.description too long")
        if len(",".join(yt.get("tags") or [])) > 450: probs.append("youtube.tags: over ~450 characters together (limit 500)")
    if caps.get("instagram") and data.get("caption") != caps["instagram"]:
        probs.append("`caption` must equal captions.instagram")
    kw = (data.get("dm") or {}).get("keyword")
    if kw and kw.lower() not in (caps.get("instagram") or "").lower():
        probs.append(f"instagram: the post has dm.keyword {kw!r}: the caption must tell people to comment it")
    if kw and kw.lower() in (caps.get("facebook") or "").lower():
        probs.append("facebook: no 'Comment WORD' there (the DM bot is Instagram only); ask a real question instead")
    if data.get("comments") and not kw and not re.search(r"(?i)comment", caps.get("instagram", "")):
        probs.append("the post has `comments` (e.g. the prompts): the caption should say they're in the comments")
    return probs


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd, path = sys.argv[1], pathlib.Path(sys.argv[2])
    data = json.loads(path.read_text(encoding="utf-8"))
    if cmd == "tidy":
        caps = data.get("captions") or {}
        for pf in ("instagram", "facebook"):
            if caps.get(pf): caps[pf] = tidy(caps[pf])
        if caps.get("youtube", {}).get("description"): caps["youtube"]["description"] = tidy(caps["youtube"]["description"])
        if caps.get("instagram"): data["caption"] = caps["instagram"]
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("tidied")
    probs = check(data)
    for p in probs: print("problem:", p)
    if cmd == "check":
        if not probs:
            for pf in ("instagram", "facebook"):
                t = data["captions"][pf]; print(f"{pf}: {len(t)} chars, {len(tags_in(t))} hashtags: {' '.join(tags_in(t))}")
            print(f"youtube: {data['captions']['youtube']['title']!r}")
            print("ok")
        sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
