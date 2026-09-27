"""YouTube channel rules shared by publish.py (new Shorts) and this script (the videos already on the channel).

Every video (owner, 2026-09-27):
  - paid promotion: no            -> paidProductPlacementDetails.hasPaidProductPlacement = false
  - altered/synthetic (AI) content: yes -> status.containsSyntheticMedia = true
  - video location: United States -> recordingDetails.location (the API marks it deprecated; sent anyway, and an
                                     upload never fails because of it)
  - tags always include "ai" and "artificial intelligence" (lower case, first)
  - added to the channel playlist (PLAYLIST_TITLE; id cached as YT_PLAYLIST_ID in .env)
  - caption certification ("never aired on US television") has no API field: set it once in YouTube Studio ->
    Settings -> Upload defaults -> Advanced settings (and per video in Studio for older uploads).

Usage:
    python youtube.py            playlist (created if missing) + every channel upload added and brought up to the rules
    python youtube.py --check    only report what would change
Needs the `youtube` scope (python yt_token.py after 2026-09-27). Never prints token values.
"""
import sys, json, pathlib, argparse, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).parent.resolve()
API = "https://www.googleapis.com/youtube/v3"
REQUIRED_TAGS = ["ai", "artificial intelligence"]
US_LOCATION = {"latitude": 39.8283, "longitude": -98.5795}  # geographic centre of the contiguous United States
PLAYLIST_TITLE = "AI Playbooks: AI Tools, Prompts & News"
PLAYLIST_DESC = ("Every AI Playbooks Short in one place: copy-paste prompts that save you hours, ChatGPT, Claude, "
                 "Gemini, Grok and Cursor tips, and the AI news that actually changes how you work. "
                 "New videos every day. Subscribe so you don't miss the next playbook.")


class YTError(Exception):
    pass


def read_env():
    env = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def set_env(key, value):
    f = ROOT / ".env"; lines = f.read_text(encoding="utf-8").splitlines() if f.exists() else []
    lines = [l for l in lines if not l.startswith(key + "=")] + [f"{key}={value}"]
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")


def token(env=None):
    env = env or read_env()
    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not env.get(k)]
    if missing: raise YTError(f"missing in .env: {', '.join(missing)} (run yt_token.py)")
    data = urllib.parse.urlencode({"client_id": env["YT_CLIENT_ID"], "client_secret": env["YT_CLIENT_SECRET"],
                                   "refresh_token": env["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data), timeout=30) as r:
            return json.loads(r.read())["access_token"]
    except urllib.error.HTTPError as ex:
        raise YTError(f"token refresh failed: {json.loads(ex.read() or b'{}').get('error_description', ex)}") from None


def call(tok, method, path, params=None, body=None):
    url = f"{API}/{path}?" + urllib.parse.urlencode(params or {})
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as ex:
        raw = ex.read() or b"{}"
        try: err = json.loads(raw).get("error", {}); msg = err.get("message") or str(err)
        except ValueError: msg = raw[:300].decode("utf-8", "replace")
        raise YTError(f"{method} {path}: {msg} (HTTP {ex.code})") from None


def with_tags(tags):
    """Required tags first, then the rest (no duplicates); YouTube caps the tag list at 500 characters."""
    out = list(REQUIRED_TAGS)
    for t in tags or []:
        t = str(t).strip().lstrip("#")
        if t and t.lower() not in (x.lower() for x in out): out.append(t)
    while len(",".join(f'"{t}"' if " " in t else t for t in out)) > 480: out.pop()
    return out


def upload_body(snippet, status):
    """The metadata parts of a new upload (publish.py). recordingDetails is left out by `drop_location`."""
    return {"snippet": {**snippet, "tags": with_tags(snippet.get("tags"))},
            "status": {**status, "containsSyntheticMedia": True},
            "paidProductPlacementDetails": {"hasPaidProductPlacement": False},
            "recordingDetails": {"location": US_LOCATION, "locationDescription": "United States"}}


def parts(body):
    return ",".join(body)


def drop_location(body):
    return {k: v for k, v in body.items() if k != "recordingDetails"}


# ---------------------------------------------------------------- playlist

def playlist_id(tok, create=True):
    env = read_env()
    pid = env.get("YT_PLAYLIST_ID")
    if pid and call(tok, "GET", "playlists", {"part": "id", "id": pid}).get("items"): return pid
    page = None
    while True:  # an existing playlist with our title (e.g. .env lost) is reused
        r = call(tok, "GET", "playlists", {"part": "snippet", "mine": "true", "maxResults": 50, **({"pageToken": page} if page else {})})
        hit = next((p["id"] for p in r.get("items", []) if p["snippet"]["title"] == PLAYLIST_TITLE), None)
        if hit: set_env("YT_PLAYLIST_ID", hit); return hit
        page = r.get("nextPageToken")
        if not page: break
    if not create: return None
    p = call(tok, "POST", "playlists", {"part": "snippet,status"},
             {"snippet": {"title": PLAYLIST_TITLE, "description": PLAYLIST_DESC, "defaultLanguage": "en"},
              "status": {"privacyStatus": "public"}})
    set_env("YT_PLAYLIST_ID", p["id"])
    return p["id"]


def playlist_videos(tok, pid):
    ids, page = set(), None
    while True:
        try: r = call(tok, "GET", "playlistItems", {"part": "contentDetails", "playlistId": pid, "maxResults": 50, **({"pageToken": page} if page else {})})
        except YTError as ex:
            if "HTTP 404" in str(ex): return ids  # a just-created playlist isn't readable for a few seconds
            raise
        ids |= {i["contentDetails"]["videoId"] for i in r.get("items", [])}
        page = r.get("nextPageToken")
        if not page: return ids


def add_to_playlist(tok, vid, pid=None):
    """Add one video to the channel playlist (first position = newest on top). Returns the playlist id."""
    pid = pid or playlist_id(tok)
    if vid not in playlist_videos(tok, pid):
        call(tok, "POST", "playlistItems", {"part": "snippet"},
             {"snippet": {"playlistId": pid, "position": 0, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
    return pid


# ---------------------------------------------------------------- existing videos

def channel_uploads(tok):
    ch = call(tok, "GET", "channels", {"part": "contentDetails", "mine": "true"})["items"][0]
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    vids, page = [], None
    while True:
        r = call(tok, "GET", "playlistItems", {"part": "contentDetails", "playlistId": up, "maxResults": 50, **({"pageToken": page} if page else {})})
        vids += [(i["contentDetails"]["videoId"], i["contentDetails"].get("videoPublishedAt", "")) for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page: return sorted(vids, key=lambda v: v[1])  # oldest first


DONE = ROOT / "runs" / "youtube_rules.json"  # videos whose AI disclosure YouTube confirmed (GET never returns the flag)


def fix_video(tok, vid, dry=False):
    """Bring one video up to the rules. Returns the list of changes (empty = already fine).
    Notes from the 2026-09-27 run: YouTube stores tags in its own (sorted) order, so only their presence is checked;
    `containsSyntheticMedia` comes back in the PUT response but never in a GET; the deprecated recordingDetails.location
    is accepted and silently dropped, so the location can't be set through the API (only in YouTube Studio)."""
    v = call(tok, "GET", "videos", {"part": "snippet,status,paidProductPlacementDetails", "id": vid})["items"][0]
    sn, st = v["snippet"], v["status"]
    done = set(json.loads(DONE.read_text(encoding="utf-8"))) if DONE.exists() else set()
    changes, body = [], {}
    have = {t.lower() for t in sn.get("tags") or []}
    if not all(t in have for t in REQUIRED_TAGS):
        changes.append("tags")
        body["snippet"] = {k: sn[k] for k in ("title", "description", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in sn}
        body["snippet"]["tags"] = with_tags(sn.get("tags"))
    if vid not in done and not st.get("containsSyntheticMedia"):
        changes.append("AI beyanı")
        body["status"] = {k: st[k] for k in ("privacyStatus", "embeddable", "license", "publicStatsViewable",
                                              "selfDeclaredMadeForKids") if k in st}
        body["status"]["containsSyntheticMedia"] = True
    if (v.get("paidProductPlacementDetails") or {}).get("hasPaidProductPlacement") is not False:
        changes.append("ücretli tanıtım: hayır")
        body["paidProductPlacementDetails"] = {"hasPaidProductPlacement": False}
    if changes and not dry:
        body["id"] = vid
        r = call(tok, "PUT", "videos", {"part": parts(k for k in body if k != "id")}, body)
        if (r.get("status") or {}).get("containsSyntheticMedia"):
            DONE.parent.mkdir(exist_ok=True); DONE.write_text(json.dumps(sorted(done | {vid})), encoding="utf-8")
    return changes


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true"); a = ap.parse_args()
    tok = token()
    pid = playlist_id(tok, create=not a.check)
    have = playlist_videos(tok, pid) if pid else set()
    print(f"playlist: {PLAYLIST_TITLE} ({pid or 'yok, oluşturulacak'})")
    for vid, when in channel_uploads(tok):
        todo = fix_video(tok, vid, dry=a.check)
        if vid not in have:
            todo.append("oynatma listesine ekle")
            if not a.check: add_to_playlist(tok, vid, pid)
        print(f"{when[:10]} {vid}: {', '.join(todo) or 'tamam'}")
    if pid: print(f"https://www.youtube.com/playlist?list={pid}")


if __name__ == "__main__":
    try: main()
    except YTError as ex: sys.exit(f"hata: {ex}")
