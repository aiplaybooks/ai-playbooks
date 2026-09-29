"""One-time TikTok login for posting (Login Kit for Web + Content Posting API) -> refresh token in .env.

TikTok only redirects to https URIs, so the registered redirect is our gh-pages relay page
https://aiplaybooks.github.io/ai-playbooks/tiktok/callback/ , which forwards ?code=... to this script's loopback
server http://127.0.0.1:8767/tiktok (the page is on gh-pages: tiktok/callback/index.html).
1. developers.tiktok.com app "AI Playbooks Publisher": Login Kit (that redirect URI) + Content Posting API
   (Direct Post on), scopes user.info.basic, video.publish, video.upload.
2. TIKTOK_CLIENT_KEY + TIKTOK_CLIENT_SECRET in .env.
3. python tiktok_token.py      (browser: log in as @ai.playbooks and authorize)

Writes TIKTOK_REFRESH_TOKEN (365 days, rotates: refresh() saves the new one), TIKTOK_OPEN_ID, TIKTOK_USERNAME.
Access tokens live 24 h. Never prints token values.
"""
import sys, json, secrets, threading, webbrowser, urllib.parse, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from x_token import read_env, save_env, ENV

PORT, PATH = 8767, "/tiktok"
REDIRECT = "https://aiplaybooks.github.io/ai-playbooks/tiktok/callback/"
SCOPES = ["user.info.basic", "video.publish", "video.upload"]
API = "https://open.tiktokapis.com/v2"


def token_request(data):
    env = read_env()
    body = urllib.parse.urlencode({"client_key": env["TIKTOK_CLIENT_KEY"], "client_secret": env["TIKTOK_CLIENT_SECRET"], **data}).encode()
    req = urllib.request.Request(f"{API}/oauth/token/", body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: tok = json.loads(r.read())
    except urllib.error.HTTPError as ex:
        tok = json.loads(ex.read() or b"{}")
    if not tok.get("access_token"):
        raise RuntimeError(f"TikTok token request failed: {tok.get('error_description') or tok.get('error') or tok}")
    return tok


def refresh():
    """-> a fresh access token (24 h); saves the rotated refresh token."""
    env = read_env()
    if not env.get("TIKTOK_REFRESH_TOKEN"): raise RuntimeError("no TikTok login yet: run `python tiktok_token.py` once")
    tok = token_request({"grant_type": "refresh_token", "refresh_token": env["TIKTOK_REFRESH_TOKEN"]})
    if tok.get("refresh_token"): save_env(TIKTOK_REFRESH_TOKEN=tok["refresh_token"])
    return tok["access_token"]


def me(access):
    req = urllib.request.Request(f"{API}/user/info/?fields=open_id,display_name,username",
                                 headers={"Authorization": f"Bearer {access}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())["data"]["user"]
    except (urllib.error.HTTPError, KeyError):  # `username` needs user.info.profile on some apps: retry without it
        req = urllib.request.Request(f"{API}/user/info/?fields=open_id,display_name", headers={"Authorization": f"Bearer {access}"})
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())["data"]["user"]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    env = read_env()
    if not env.get("TIKTOK_CLIENT_KEY") or not env.get("TIKTOK_CLIENT_SECRET"): sys.exit("TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET missing in .env")
    state = secrets.token_urlsafe(16); got = {}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query))
            if u.path != PATH or ("code" not in q and "error" not in q): self.send_response(404); self.end_headers(); return
            got.update(q)
            ok = q.get("state") == state and "code" in q
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(("<h2>AI Playbooks: TikTok bağlandı. Bu sekmeyi kapatabilirsin.</h2>" if ok else
                              f"<h2>Giriş başarısız: {q.get('error_description') or q.get('error', 'state mismatch')}</h2>").encode())
            threading.Thread(target=srv.shutdown, daemon=True).start()

    srv = HTTPServer(("127.0.0.1", PORT), H)
    url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode({
        "client_key": env["TIKTOK_CLIENT_KEY"], "scope": ",".join(SCOPES), "response_type": "code",
        "redirect_uri": REDIRECT, "state": state})
    print("Opening the browser for the TikTok login (use @ai.playbooks). If it doesn't open, visit:\n" + url, flush=True)
    webbrowser.open(url)
    srv.serve_forever()
    if got.get("state") != state or "code" not in got: sys.exit(f"login failed: {got.get('error_description') or got.get('error', 'state mismatch')}")
    try:
        tok = token_request({"grant_type": "authorization_code", "code": got["code"], "redirect_uri": REDIRECT})
    except RuntimeError as ex: sys.exit(str(ex))
    user = me(tok["access_token"])
    granted = set(tok.get("scope", "").split(",")); missing = [s for s in SCOPES if s not in granted]
    save_env(TIKTOK_REFRESH_TOKEN=tok["refresh_token"], TIKTOK_OPEN_ID=tok["open_id"],
             TIKTOK_USERNAME=user.get("username") or user.get("display_name", ""))
    print(f"TikTok account : {user.get('display_name')} (@{user.get('username', '?')})")
    print(f"Permissions    : {'all granted' if not missing else 'MISSING ' + ', '.join(missing)}")
    print(f"saved to {ENV}")


if __name__ == "__main__":
    main()
