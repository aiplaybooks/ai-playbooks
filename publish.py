"""Publish a rendered post to Instagram (carousel + Reel) and the Facebook Page (multi-photo post + Reel).

Usage:
    python publish.py content/2026-09-24_claude-tradingview.json --dry-run     (checks only, posts nothing)
    python publish.py content/2026-09-24_claude-tradingview.json [--steps ig_carousel,ig_reel]

Needs carousel.py + reel.py output in output/<name>/ and META_PAGE_TOKEN, FB_PAGE_ID, IG_USER_ID in .env
(or the environment). Steps, in order:
    prepare      slide PNGs -> JPEG (Instagram takes JPEG only), checks caption, slide count, Reel
    upload       copies media to the gh-pages branch (media/<name>/), pushes, waits until the URLs are live
    ig_carousel  Instagram carousel: child containers -> CAROUSEL container -> media_publish
    ig_reel      Instagram Reel: REELS container -> poll until FINISHED -> media_publish
    fb_photos    Facebook Page multi-photo post: unpublished photos -> /feed with attached_media
    fb_reel      Facebook Page Reel: video_reels start -> rupload from the public URL -> finish
    yt_short     YouTube Short: resumable upload of the Reel (YouTube Data API v3). Until the API project passes
                 YouTube's audit, YouTube keeps API uploads private: then make it public in YouTube Studio.
    log          appends the post to publish_log.jsonl
Progress is saved to output/<name>/publish.json after every step, so a rerun resumes and never posts twice.
Token values are never printed.
"""
import sys, os, re, json, time, shutil, pathlib, argparse, subprocess, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone
from PIL import Image, ImageFilter, ImageEnhance

ROOT = pathlib.Path(__file__).parent.resolve()
GRAPH = "https://graph.facebook.com/v25.0"
RUPLOAD = "https://rupload.facebook.com/video-upload/v25.0"
PAGES_URL = "https://aiplaybooks.github.io/ai-playbooks"
PAGES_DIR = ROOT / ".pages"  # git worktree of the gh-pages branch (gitignored)
LOG = ROOT / "publish_log.jsonl"
STEPS = ["prepare", "upload", "ig_carousel", "ig_reel", "fb_photos", "fb_reel", "yt_short", "log"]
POSTS = ["ig_carousel", "ig_reel", "fb_photos", "fb_reel", "yt_short"]


class PublishError(Exception):
    pass


def say(*a):
    print(*a, flush=True)


def read_env():
    env = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("META_PAGE_TOKEN", "FB_PAGE_ID", "IG_USER_ID", "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"):
        if os.environ.get(k): env[k] = os.environ[k]
    return env


def api(method, url, params=None, headers=None):
    """Graph API call. Errors show Meta's message, never the URL or the token."""
    params = dict(params or {})
    data = None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as ex:
        body = ex.read() or b"{}"
        try: err = json.loads(body).get("error", {})
        except ValueError: err = {"message": body[:300].decode("utf-8", "replace")}
        path = urllib.parse.urlparse(url).path
        raise PublishError(f"{method} {path}: {err.get('message', ex)} "
                           f"(code {err.get('code')}, subcode {err.get('error_subcode')})") from None


def multipart(url, fields, file_field, path, headers=None):
    """POST multipart/form-data with one file (for thumbnail uploads)."""
    b = "----aiplaybooks" + os.urandom(8).hex(); body = b""
    CRLF = "\r\n"
    for k, v in fields.items():
        body += f'--{b}{CRLF}Content-Disposition: form-data; name="{k}"{CRLF}{CRLF}{v}{CRLF}'.encode()
    body += (f'--{b}{CRLF}Content-Disposition: form-data; name="{file_field}"; filename="{path.name}"{CRLF}'
             f'Content-Type: image/jpeg{CRLF}{CRLF}').encode() + path.read_bytes() + f"{CRLF}--{b}--{CRLF}".encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as ex:
        body = ex.read() or b"{}"
        try: err = json.loads(body).get("error", {}); msg = err.get("message") if isinstance(err, dict) else str(err)
        except ValueError: msg = body[:300].decode("utf-8", "replace")
        raise PublishError(f"POST {urllib.parse.urlparse(url).path}: {msg}") from None


class Post:
    def __init__(self, content):
        self.content = pathlib.Path(content).resolve()
        self.data = json.loads(self.content.read_text(encoding="utf-8"))
        self.name = self.content.stem
        self.out = ROOT / "output" / self.name
        self.pub = self.out / "publish"
        self.state_file = self.out / "publish.json"
        self.state = json.loads(self.state_file.read_text(encoding="utf-8")) if self.state_file.exists() else {}
        self.env = read_env()

    def save(self):
        self.state_file.write_text(json.dumps(self.state, indent=1, ensure_ascii=False), encoding="utf-8")

    def done(self, step, **info):
        self.state[step] = {"done": datetime.now(timezone.utc).isoformat(timespec="seconds"), **info}
        self.save()

    @property
    def token(self):
        return self.env["META_PAGE_TOKEN"]

    def images(self):
        return sorted(self.pub.glob("slide_*.jpg"))

    def url(self, f):
        return f"{PAGES_URL}/media/{self.name}/{f.name}"


# ---------------------------------------------------------------- steps

def prepare(p, dry=False):
    pngs = sorted(p.out.glob("slide_*.png"))
    reel = p.out / "reel.mp4"
    if not pngs: raise PublishError(f"no slides in {p.out}: run carousel.py first")
    if not 2 <= len(pngs) <= 10: raise PublishError(f"Instagram carousels take 2-10 images, this post has {len(pngs)}")
    if not reel.exists(): raise PublishError(f"no {reel.name} in {p.out}: run reel.py first")
    cap = p.data.get("caption", "")
    if not cap.strip(): raise PublishError("caption is empty")
    if len(cap) > 2200: raise PublishError(f"caption is {len(cap)} characters (Instagram max 2200)")
    if cap.count("#") > 30: raise PublishError(f"caption has {cap.count('#')} hashtags (Instagram max 30)")
    shutil.rmtree(p.pub, ignore_errors=True); p.pub.mkdir(parents=True)
    for f in pngs:
        j = p.pub / (f.stem + ".jpg")
        Image.open(f).convert("RGB").save(j, "JPEG", quality=92, optimize=True)
        if j.stat().st_size > 8 * 2**20: raise PublishError(f"{j.name} is over 8 MB")
    shutil.copy2(reel, p.pub / "reel.mp4")
    make_cover(pngs[0], p.pub / "cover.jpg")
    mb = (p.pub / "reel.mp4").stat().st_size / 2**20
    say(f"prepare: {len(pngs)} slides -> JPEG, reel {mb:.1f} MB, caption {len(cap)} chars")
    if not dry: p.done("prepare", slides=len(pngs))


def make_cover(slide, out):
    """9:16 Reel/Short cover from the carousel's first slide: the slide centered, blurred copy of it above/below."""
    im = Image.open(slide).convert("RGB"); W, H = 1080, 1920
    k = max(W / im.width, H / im.height)
    bg = im.resize((round(im.width * k), round(im.height * k)))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(36))).enhance(0.55)
    fg = im.resize((W, round(im.height * W / im.width)))
    bg.paste(fg, (0, (H - fg.height) // 2))
    bg.save(out, "JPEG", quality=92, optimize=True)


def git(*args, cwd=ROOT):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: raise PublishError(f"git {' '.join(args)}: {(r.stderr or r.stdout).strip()}")
    return r.stdout.strip()


def pages_worktree():
    if not (PAGES_DIR / ".git").exists():
        git("worktree", "prune")
        git("fetch", "origin", "gh-pages")
        git("worktree", "add", str(PAGES_DIR), "gh-pages")
    git("pull", "--ff-only", "origin", "gh-pages", cwd=PAGES_DIR)
    return PAGES_DIR


def live(url, size):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
            return r.status == 200 and int(r.headers.get("Content-Length", -1)) == size
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False


def upload(p):
    prepare(p)  # always from the latest render (the Studio calls upload directly, and revisions re-render)
    files = p.images() + [p.pub / "reel.mp4", p.pub / "cover.jpg"]
    wt = pages_worktree()
    dest = wt / "media" / p.name
    shutil.rmtree(dest, ignore_errors=True); dest.mkdir(parents=True)
    for f in files: shutil.copy2(f, dest / f.name)
    git("add", "-A", "media", cwd=wt)
    if git("status", "--porcelain", cwd=wt):
        git("commit", "-q", "-m", f"media: {p.name}", cwd=wt)
        git("push", "-q", "origin", "gh-pages", cwd=wt)
        say(f"upload: pushed {len(files)} files to gh-pages")
    say("upload: waiting for GitHub Pages ...")
    t0 = time.time()
    while not all(live(p.url(f), f.stat().st_size) for f in files):
        if time.time() - t0 > 600: raise PublishError("media not live on GitHub Pages after 10 minutes")
        time.sleep(15)
    say(f"upload: live at {PAGES_URL}/media/{p.name}/ ({time.time() - t0:.0f}s)")
    p.done("upload", base=f"{PAGES_URL}/media/{p.name}/")


def ig_wait(p, cid, what, limit=900):
    t0 = time.time()
    while True:
        s = api("GET", f"{GRAPH}/{cid}", {"fields": "status_code,status", "access_token": p.token})
        code = s.get("status_code")
        if code in ("FINISHED", "PUBLISHED"): return
        if code in ("ERROR", "EXPIRED"): raise PublishError(f"{what} container {code}: {s.get('status')}")
        if time.time() - t0 > limit: raise PublishError(f"{what} container still {code} after {limit}s")
        time.sleep(10)


def ig_publish(p, cid, step):
    ig = p.env["IG_USER_ID"]
    mid = p.state.get(step + "_media")
    if not mid:  # saved right away: if anything after this fails, a rerun must not post again
        mid = api("POST", f"{GRAPH}/{ig}/media_publish", {"creation_id": cid, "access_token": p.token})["id"]
        p.state[step + "_media"] = mid; p.save()
    link = api("GET", f"{GRAPH}/{mid}", {"fields": "permalink", "access_token": p.token}).get("permalink")
    return mid, link


def ig_carousel(p):
    ig = p.env["IG_USER_ID"]; kids = p.state.get("ig_carousel_children") or []
    if not kids:
        for f in p.images():
            kids.append(api("POST", f"{GRAPH}/{ig}/media",
                            {"image_url": p.url(f), "is_carousel_item": "true", "access_token": p.token})["id"])
        p.state["ig_carousel_children"] = kids; p.save()
    cid = None
    if not p.state.get("ig_carousel_media"):
        for k in kids: ig_wait(p, k, "carousel item", 300)
        cid = api("POST", f"{GRAPH}/{ig}/media", {"media_type": "CAROUSEL", "children": ",".join(kids),
                                                  "caption": p.data["caption"], "access_token": p.token})["id"]
        ig_wait(p, cid, "carousel", 300)
    mid, link = ig_publish(p, cid, "ig_carousel")
    say(f"ig_carousel: published {link}")
    p.done("ig_carousel", id=mid, link=link)


def ig_reel(p):
    ig = p.env["IG_USER_ID"]
    cid = p.state.get("ig_reel_container")
    if not cid:
        cid = api("POST", f"{GRAPH}/{ig}/media", {"media_type": "REELS", "video_url": p.url(p.pub / "reel.mp4"),
                                                  "caption": p.data["caption"], "share_to_feed": "true",
                                                  "cover_url": p.url(p.pub / "cover.jpg"), "access_token": p.token})["id"]
        p.state["ig_reel_container"] = cid; p.save()
    if not p.state.get("ig_reel_media"):
        say("ig_reel: Instagram is processing the video ...")
        ig_wait(p, cid, "reel")
    mid, link = ig_publish(p, cid, "ig_reel")
    say(f"ig_reel: published {link}")
    p.done("ig_reel", id=mid, link=link)


def fb_photos(p):
    page = p.env["FB_PAGE_ID"]; ids = p.state.get("fb_photo_ids") or []
    if not ids:
        for f in p.images():
            ids.append(api("POST", f"{GRAPH}/{page}/photos",
                           {"url": p.url(f), "published": "false", "access_token": p.token})["id"])
        p.state["fb_photo_ids"] = ids; p.save()
    params = {"message": p.data["caption"], "access_token": p.token}
    for i, x in enumerate(ids): params[f"attached_media[{i}]"] = json.dumps({"media_fbid": x})
    pid = api("POST", f"{GRAPH}/{page}/feed", params)["id"]
    link = f"https://www.facebook.com/{pid}"
    p.done("fb_photos", id=pid, link=link)
    say(f"fb_photos: published {link}")


def fb_reel(p):
    page = p.env["FB_PAGE_ID"]
    vid = p.state.get("fb_reel_video")
    if not vid:
        vid = api("POST", f"{GRAPH}/{page}/video_reels", {"upload_phase": "start", "access_token": p.token})["video_id"]
        api("POST", f"{RUPLOAD}/{vid}", headers={"Authorization": f"OAuth {p.token}",
                                                  "file_url": p.url(p.pub / "reel.mp4")})
        p.state["fb_reel_video"] = vid; p.save()
    if not p.state.get("fb_reel_finished"):
        api("POST", f"{GRAPH}/{page}/video_reels", {"upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED",
                                                    "description": p.data["caption"], "access_token": p.token})
        p.state["fb_reel_finished"] = True; p.save()
    t0 = time.time(); st = {}
    while time.time() - t0 < 600:  # Facebook publishes asynchronously; wait for it, but don't fail on slowness
        st = api("GET", f"{GRAPH}/{vid}", {"fields": "status", "access_token": p.token}).get("status", {})
        if st.get("video_status") == "error" or st.get("processing_phase", {}).get("status") == "error":
            raise PublishError(f"Facebook Reel processing failed: {json.dumps(st)}")
        if st.get("publishing_phase", {}).get("status") == "complete": break
        time.sleep(10)
    cover = "skipped"
    try:  # custom cover; needs pages_manage_engagement + pages_read_user_content, so it must never fail the step
        multipart(f"{GRAPH}/{vid}/thumbnails", {"is_preferred": "true", "access_token": p.token}, "source", p.pub / "cover.jpg")
        cover = "set"
    except PublishError as ex:
        cover = f"not set: {str(ex)[:160]}"
    say(f"fb_reel: cover {cover}")
    link = f"https://www.facebook.com/reel/{vid}"
    state = st.get("publishing_phase", {}).get("status", "unknown")
    say(f"fb_reel: {link} (publishing: {state})")
    p.done("fb_reel", id=vid, link=link, status=state, cover=cover)


def yt_access(p):
    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not p.env.get(k)]
    if missing: raise PublishError(f"missing in .env: {', '.join(missing)} (run yt_token.py)")
    return api("POST", "https://oauth2.googleapis.com/token", {
        "client_id": p.env["YT_CLIENT_ID"], "client_secret": p.env["YT_CLIENT_SECRET"],
        "refresh_token": p.env["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"})["access_token"]


def yt_meta(p):
    """Title (<=100 chars), description and tags for the Short, from the content JSON."""
    cover = next((s for s in p.data["slides"] if s["type"] == "cover"), {})
    title = (cover.get("title") or p.data.get("topic") or p.name).replace("<", "").replace(">", "").strip()
    if len(title) > 90: title = title[:89].rsplit(" ", 1)[0] + "…"
    cap = p.data["caption"].replace("<", "").replace(">", "")
    tags = [t.lstrip("#") for t in re.findall(r"#\w+", cap)][:15]
    desc = cap + "\n\n" + "\n".join(p.data.get("sources", [])[:3]) + "\n\n#Shorts"
    return {"title": title + " #Shorts", "description": desc[:4900], "tags": tags, "categoryId": "28",
            "defaultLanguage": "en", "defaultAudioLanguage": "en"}


def yt_short(p):
    vid = p.state.get("yt_short_video")
    if not vid:  # one upload only: a retry after this point never uploads a second copy
        tok = yt_access(p); f = p.pub / "reel.mp4"
        if not f.exists(): prepare(p)
        body = json.dumps({"snippet": yt_meta(p), "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}).encode()
        req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                                     data=body, method="POST", headers={
            "Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(f.stat().st_size)})
        try:
            with urllib.request.urlopen(req, timeout=60) as r: session = r.headers["Location"]
        except urllib.error.HTTPError as ex:
            raise PublishError(f"YouTube upload start: {(ex.read() or b'')[:400].decode('utf-8', 'replace')}") from None
        req = urllib.request.Request(session, data=f.read_bytes(), method="PUT", headers={"Content-Type": "video/mp4"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r: v = json.loads(r.read())
        except urllib.error.HTTPError as ex:
            raise PublishError(f"YouTube upload: {(ex.read() or b'')[:400].decode('utf-8', 'replace')}") from None
        vid = v["id"]; p.state["yt_short_video"] = vid; p.save()
    tok = yt_access(p)
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/videos?part=status&id={vid}",
                                 headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r: items = json.loads(r.read()).get("items", [])
    privacy = items[0]["status"]["privacyStatus"] if items else "unknown"
    thumb = p.state.get("yt_thumb")
    if not thumb:  # custom Shorts covers are limited to Partner Program channels; try, never fail the step
        try:
            req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                         data=(p.pub / "cover.jpg").read_bytes(), method="POST",
                                         headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
            urllib.request.urlopen(req, timeout=120).read(); thumb = "set"
        except urllib.error.HTTPError as ex:
            thumb = "not set: " + (ex.read() or b"")[:160].decode("utf-8", "replace").replace("\n", " ")
        except (urllib.error.URLError, OSError) as ex:
            thumb = f"not set: {ex}"
        p.state["yt_thumb"] = thumb; p.save()
    say(f"yt_short: cover {thumb}")
    link = f"https://youtube.com/shorts/{vid}"
    p.done("yt_short", id=vid, link=link, privacy=privacy, cover=thumb, studio=f"https://studio.youtube.com/video/{vid}/edit")
    say(f"yt_short: {link} ({privacy}" + (": YouTube Studio'dan herkese açık yap)" if privacy != "public" else ")"))


def log(p):
    entry = {"date": datetime.now().astimezone().isoformat(timespec="minutes"), "post": p.name,
             "topic": p.data.get("topic"), "theme": p.data.get("theme"), "sources": p.data.get("sources", []),
             **{s: {k: v for k, v in p.state[s].items() if k in ("id", "link")} for s in POSTS if s in p.state}}
    with LOG.open("a", encoding="utf-8") as f: f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    say(f"log: appended to {LOG.name}")
    p.done("log")


# ---------------------------------------------------------------- checks

def dry_run(p):
    prepare(p, dry=True)
    missing = [k for k in ("META_PAGE_TOKEN", "FB_PAGE_ID", "IG_USER_ID") if not p.env.get(k)]
    if missing: raise PublishError(f"missing in .env: {', '.join(missing)}")
    ig = api("GET", f"{GRAPH}/{p.env['IG_USER_ID']}", {"fields": "username", "access_token": p.token})
    page = api("GET", f"{GRAPH}/{p.env['FB_PAGE_ID']}", {"fields": "name", "access_token": p.token})
    lim = api("GET", f"{GRAPH}/{p.env['IG_USER_ID']}/content_publishing_limit",
              {"fields": "quota_usage,config", "access_token": p.token}).get("data", [{}])[0]
    say(f"token ok: Instagram @{ig.get('username')}, Facebook Page '{page.get('name')}'")
    say(f"Instagram quota: {lim.get('quota_usage')} / {lim.get('config', {}).get('quota_total')} posts in 24h")
    tok = yt_access(p)
    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
                                 headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=30) as r: ch = (json.loads(r.read()).get("items") or [{}])[0]
    say(f"YouTube ok: {ch.get('snippet', {}).get('title')} ({ch.get('snippet', {}).get('customUrl')}); Short title: {yt_meta(p)['title']}")
    done = [s for s in STEPS if s in p.state]
    say(f"already done: {', '.join(done) or 'nothing'}")
    say("dry run ok: nothing was uploaded or posted")


def run(content, steps=None, dry=False):
    p = Post(content)
    if dry: return dry_run(p)
    for s in steps or STEPS:
        if s in p.state and "done" in p.state[s]:
            say(f"{s}: already done, skipping"); continue
        globals()[s](p)
    return p.state


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("content"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--steps", help=f"comma list, default all: {','.join(STEPS)}")
    a = ap.parse_args()
    steps = a.steps.split(",") if a.steps else None
    if steps and (bad := [s for s in steps if s not in STEPS]): sys.exit(f"unknown steps: {bad}")
    try:
        run(a.content, steps, a.dry_run)
    except PublishError as ex:
        sys.exit(f"ERROR: {ex}")


if __name__ == "__main__":
    main()
