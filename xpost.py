"""X (Twitter) posting via the official API (pay-per-use, owner 2026-09-29: ~$0.015 per post, $0.20 when the post
contains a URL -> we NEVER put links in X posts; repo posts name the repo as plain text "owner/repo").

Used by publish.py's `x_post` step (all flows): the post's video (reel.mp4) or, without one, its first image, with
`captions.x` (the caption agent) or a text derived from the Instagram caption (x_text): no URLs, no "Comment WORD"
CTA (the DM bot is Instagram only), no follow line, <= 2 hashtags, <= 280 weighted characters; clips credit the
creator with an @mention. Auth: OAuth 2.0 user token of our X account (x_token.py; refresh token rotates in .env).

    python xpost.py text content/<post>.json      prints the X text (no API call)
    python xpost.py me                            which account we post as (one read, ~$0.005)
"""
import sys, re, json, time, pathlib, urllib.request, urllib.error, urllib.parse
import captions as CAP
import x_token as XT

API = "https://api.x.com/2"
LIMIT = 280
CHUNK = 4 * 2**20
URL = re.compile(r"(https?://\S+|www\.\S+|\b[\w-]+\.(?:com|io|ai|dev|org|net|app|co)(?:/\S*)?)", re.I)
CTA = re.compile(r"(\bcomment\b.*\b(dm|send|link|repo|prompt)|\bdm (me|us)\b|link in (the )?(first )?comment|in the comments"
                 r"|\bfollow @|\btap the link\b)", re.I)


class XError(Exception):
    pass


def weight(s):
    """X counts most characters as 1 and emoji / CJK as 2 (URLs as 23, but we have none)."""
    return sum(2 if ord(c) > 0x10FF else 1 for c in s)


def fit(text, limit):
    if weight(text) <= limit: return text
    out = ""
    for w in text.split(" "):
        if weight(out + " " + w + "…") > limit: break
        out = (out + " " + w).strip()
    return out.rstrip(".,;:—-") + "…"


def x_text(data):
    """The X post text (see the module docstring)."""
    own = ((data.get("captions") or {}).get("x") or "").strip()
    if own: return fit(URL.sub("", own).strip(), LIMIT)
    cap = CAP.text_for(data, "instagram")
    tags = CAP.tags_in(cap)
    paras = []
    for p in cap.split("\n\n"):
        p = p.strip()
        if not p or re.fullmatch(r"(#\w+\s*)+", p): continue
        p = "\n".join(l for l in p.split("\n") if not CTA.search(l))
        p = re.sub(r"\s{2,}", " ", URL.sub("", p)).strip()
        if p: paras.append(p)
    tail = []
    if data.get("kind") == "repo" and (data.get("repo") or {}).get("full_name"):
        tail.append(f"📦 {data['repo']['full_name']} on GitHub")
    if data.get("kind") == "clip" and (m := re.match(r"@\w+", (data.get("credit") or "").strip())):
        tail.append(f"🎥 {m.group(0)}")
    tagline = " ".join(tags[:2])
    end = "\n\n".join(tail)
    budget = LIMIT - weight(end) - (2 if end else 0)
    body = ""
    for i, p in enumerate(paras):
        cand = (body + "\n\n" + p) if body else p
        if weight(cand) <= budget: body = cand
        elif not body: body = fit(p, budget)  # a paragraph that doesn't fit is skipped, later short ones still can
    text = body + ("\n\n" + end if end else "")
    if tagline and weight(text + "\n\n" + tagline) <= LIMIT: text += "\n\n" + tagline
    return text.strip()


def call(method, url, token, body=None, ctype="application/json"):
    req = urllib.request.Request(url, data=body, method=method, headers={"Authorization": f"Bearer {token}",
                                                                          **({"Content-Type": ctype} if body else {})})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as ex:
        raw = (ex.read() or b"")[:600].decode("utf-8", "replace")
        hint = " (X API credits used up: top up in the developer console)" if ex.code == 402 else ""
        raise XError(f"{method} {urllib.parse.urlparse(url).path}: HTTP {ex.code} {raw}{hint}") from None


def upload(path, token, say=print):
    """Chunked v2 media upload -> media id (waits until X has processed a video)."""
    path = pathlib.Path(path); size = path.stat().st_size
    video = path.suffix.lower() == ".mp4"
    mtype = "video/mp4" if video else "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    init = call("POST", f"{API}/media/upload/initialize", token, json.dumps(
        {"media_type": mtype, "total_bytes": size, "media_category": "tweet_video" if video else "tweet_image"}).encode())
    mid = init["data"]["id"]
    with path.open("rb") as f:
        for i, chunk in enumerate(iter(lambda: f.read(CHUNK), b"")):
            b = "----xpost" + str(time.time_ns())
            body = (f'--{b}\r\nContent-Disposition: form-data; name="segment_index"\r\n\r\n{i}\r\n'
                    f'--{b}\r\nContent-Disposition: form-data; name="media"; filename="{path.name}"\r\n'
                    f'Content-Type: application/octet-stream\r\n\r\n').encode() + chunk + f"\r\n--{b}--\r\n".encode()
            call("POST", f"{API}/media/upload/{mid}/append", token, body, f"multipart/form-data; boundary={b}")
    info = (call("POST", f"{API}/media/upload/{mid}/finalize", token).get("data") or {}).get("processing_info")
    t0 = time.time()
    while info and info.get("state") in ("pending", "in_progress"):
        if time.time() - t0 > 600: raise XError("X is still processing the video after 10 minutes")
        time.sleep(max(2, int(info.get("check_after_secs") or 5)))
        st = call("GET", f"{API}/media/upload?command=STATUS&media_id={mid}", token)
        info = (st.get("data") or {}).get("processing_info")
    if info and info.get("state") == "failed": raise XError(f"X could not process the media: {info.get('error')}")
    say(f"x_post: uploaded {path.name} ({size / 2**20:.1f} MB)")
    return mid


def post(text, media_id, token):
    d = call("POST", f"{API}/tweets", token, json.dumps({"text": text, "media": {"media_ids": [media_id]}}).encode())["data"]
    return d["id"]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) >= 3 and sys.argv[1] == "text":
        t = x_text(json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")))
        print(t); print(f"--- {weight(t)}/{LIMIT}")
    elif sys.argv[1:] == ["me"]:
        u = XT.me(XT.refresh()); print(f"@{u['username']} ({u['name']}, {u['id']})")
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main()
