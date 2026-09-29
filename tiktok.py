"""TikTok posting via the official Content Posting API (free). Used by publish.py's `tiktok` step.

What goes out (owner, 2026-09-29): only OUR OWN content (TikTok's originality rules + what we told TikTok's review):
    carousel posts (news, prompt packs)  -> a PHOTO post (TikTok photo mode) of the slides, pulled from gh-pages
                                            (URL prefix https://aiplaybooks.github.io/ai-playbooks/ is verified)
    repo posts                           -> the scrolling repo Reel (reel.mp4), else the single photo
    viral clips (other people's videos)  -> never (skipped)
Mode (.env TIKTOK_MODE):
    inbox   (default) the post lands in the TikTok app's inbox as a draft; the owner taps "Post" on the phone.
            Needed while the app is unaudited: TikTok makes every direct post of an unaudited app private.
    direct  only for an audited app (posted publicly right away). We never apply for the audit: TikTok's guidelines
            reject "a utility tool to upload contents to the account(s) you or your team manages" (2026-09-29).
Text: `captions.tiktok` (caption agent) or the Instagram caption without the "Comment WORD" CTA (no DM bot on TikTok)
and without links; max 5 hashtags. Auth: tiktok_token.py (refresh token rotates in .env).

    python tiktok.py text content/<post>.json     prints the TikTok text (no API call)
"""
import sys, re, json, time, pathlib, urllib.request, urllib.error
import captions as CAP
import tiktok_token as TT
from xpost import URL, CTA

API = "https://open.tiktokapis.com/v2"
MAX_SINGLE = 64 * 2**20  # TikTok: a file up to 64 MB may go up as one chunk


class TikTokError(Exception):
    pass


def mode():
    return (TT.read_env().get("TIKTOK_MODE") or "inbox").strip().lower()


def text(data, limit=2200):
    own = ((data.get("captions") or {}).get("tiktok") or "").strip()
    cap = own or CAP.text_for(data, "instagram")
    out = []
    for p in cap.split("\n\n"):
        p = "\n".join(l for l in p.split("\n") if own or not CTA.search(l))
        p = re.sub(r"[ \t]{2,}", " ", URL.sub("", p)).strip()
        if p: out.append(p)
    t = "\n\n".join(out)
    tags = CAP.tags_in(t)
    for extra in tags[5:]: t = t.replace(" " + extra, "").replace(extra, "")  # TikTok: keep it to 5 hashtags
    if data.get("kind") == "repo" and (full := (data.get("repo") or {}).get("full_name")) and full.lower() not in t.lower():
        m = re.search(r"\n\n((?:#\w+\s*)+)$", t)  # before the hashtag line
        line = f"\n\n📦 {full} on GitHub"
        t = t[:m.start()] + line + t[m.start():] if m else t.rstrip() + line
    return t.strip()[:limit]


def call(path, token, body):
    req = urllib.request.Request(f"{API}{path}", json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: d = json.loads(r.read())
    except urllib.error.HTTPError as ex:
        d = json.loads(ex.read() or b"{}")
    err = d.get("error") or {}
    if err.get("code") not in (None, "ok"):
        raise TikTokError(f"{path}: {err.get('code')}: {err.get('message')}")
    return d.get("data") or {}


def post_info(data, token):
    info = call("/post/publish/creator_info/query/", token, {})
    privacy = "PUBLIC_TO_EVERYONE" if "PUBLIC_TO_EVERYONE" in info.get("privacy_level_options", []) else info["privacy_level_options"][0]
    return privacy


def video(path, data, token, say=print):
    """reel.mp4 -> inbox draft or direct post. Returns the publish_id."""
    path = pathlib.Path(path); size = path.stat().st_size
    if size > MAX_SINGLE: raise TikTokError(f"{path.name} is {size / 2**20:.0f} MB: over the single-chunk limit")
    src = {"source": "FILE_UPLOAD", "video_size": size, "chunk_size": size, "total_chunk_count": 1}
    if mode() == "direct":
        body = {"post_info": {"title": text(data), "privacy_level": post_info(data, token), "disable_comment": False,
                              "disable_duet": False, "disable_stitch": False, "video_cover_timestamp_ms": 500,
                              "brand_content_toggle": False, "brand_organic_toggle": False, "is_aigc": False},
                "source_info": src}
        d = call("/post/publish/video/init/", token, body)
    else:
        d = call("/post/publish/inbox/video/init/", token, {"source_info": src})
    req = urllib.request.Request(d["upload_url"], path.read_bytes(), method="PUT", headers={
        "Content-Type": "video/mp4", "Content-Length": str(size), "Content-Range": f"bytes 0-{size - 1}/{size}"})
    try:
        urllib.request.urlopen(req, timeout=600).read()
    except urllib.error.HTTPError as ex:
        raise TikTokError(f"video upload: HTTP {ex.code} {(ex.read() or b'')[:300]!r}") from None
    say(f"tiktok: uploaded {path.name} ({size / 2**20:.1f} MB, {mode()})")
    return d["publish_id"]


def photos(urls, data, token, say=print):
    """Carousel slides (public JPEG URLs under the verified prefix) -> TikTok photo post. Returns the publish_id."""
    t = text(data, 4000)
    title = t.split("\n", 1)[0][:90]
    direct = mode() == "direct"
    body = {"post_info": {"title": title, "description": t, "disable_comment": False, "auto_add_music": True,
                          **({"privacy_level": post_info(data, token), "brand_content_toggle": False,
                              "brand_organic_toggle": False} if direct else {})},
            "source_info": {"source": "PULL_FROM_URL", "photo_cover_index": 0, "photo_images": urls[:35]},
            "post_mode": "DIRECT_POST" if direct else "MEDIA_UPLOAD", "media_type": "PHOTO"}
    d = call("/post/publish/content/init/", token, body)
    say(f"tiktok: {len(urls)} photos handed to TikTok ({mode()})")
    return d["publish_id"]


def wait(publish_id, token, say=print, limit=600):
    """-> final status: PUBLISH_COMPLETE (direct) or SEND_TO_USER_INBOX (inbox draft)."""
    t0 = time.time(); st = {}
    while time.time() - t0 < limit:
        st = call("/post/publish/status/fetch/", token, {"publish_id": publish_id})
        s = st.get("status")
        if s in ("PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"): return st
        if s == "FAILED": raise TikTokError(f"TikTok could not process the post: {st.get('fail_reason')}")
        time.sleep(8)
    raise TikTokError(f"TikTok still processing after {limit}s (last status {st.get('status')})")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) >= 3 and sys.argv[1] == "text":
        print(text(json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))))
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main()
