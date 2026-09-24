"""One-time YouTube login: OAuth (Desktop app client, loopback + PKCE) -> refresh token in .env.

1. Google Cloud project with "YouTube Data API v3" + "YouTube Analytics API" enabled, OAuth consent screen
   published (In production, so the refresh token doesn't expire after 7 days), OAuth client "Desktop app"
   downloaded as client_secret.json next to this file (gitignored).
2. python yt_token.py      (a browser opens: pick the AI Playbooks channel and allow)

Writes YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN, YT_CHANNEL_ID into .env. Never prints token values.
Run it again if the token stops working (password change, access removed in the Google account).
"""
import sys, json, base64, hashlib, secrets, pathlib, threading, webbrowser, urllib.parse, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = pathlib.Path(__file__).parent.resolve()
ENV = ROOT / ".env"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]


def read_env():
    env = {}
    if ENV.exists():
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def post(url, data):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, urllib.parse.urlencode(data).encode()), timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as ex:
        sys.exit(f"token request failed: {json.loads(ex.read() or b'{}').get('error_description', ex)}")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    f = ROOT / "client_secret.json"
    if not f.exists(): sys.exit(f"missing {f}")
    c = json.loads(f.read_text(encoding="utf-8"))["installed"]
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16); got = {}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
            if "code" not in q and "error" not in q: self.send_response(404); self.end_headers(); return
            got.update(q)
            ok = q.get("state") == state and "code" in q
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(("<h2>AI Playbooks: YouTube bağlandı. Bu sekmeyi kapatabilirsin.</h2>" if ok else
                              f"<h2>Giriş başarısız: {q.get('error', 'state mismatch')}</h2>").encode())
            threading.Thread(target=srv.shutdown, daemon=True).start()

    srv = HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    url = c["auth_uri"] + "?" + urllib.parse.urlencode({
        "client_id": c["client_id"], "redirect_uri": redirect, "response_type": "code", "scope": " ".join(SCOPES),
        "access_type": "offline", "prompt": "consent", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256"})
    print("Opening the browser for the Google login. If it doesn't open, visit:\n" + url, flush=True)
    webbrowser.open(url)
    srv.serve_forever()
    if got.get("state") != state or "code" not in got: sys.exit(f"login failed: {got.get('error', 'state mismatch')}")

    tok = post(c["token_uri"], {"code": got["code"], "client_id": c["client_id"], "client_secret": c["client_secret"],
                                "redirect_uri": redirect, "grant_type": "authorization_code", "code_verifier": verifier})
    if "refresh_token" not in tok: sys.exit("no refresh token returned (remove the app's access in the Google account and retry)")
    granted = set(tok.get("scope", "").split())
    missing = [s.rsplit("/", 1)[1] for s in SCOPES if s not in granted]

    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
                                 headers={"Authorization": f"Bearer {tok['access_token']}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read()).get("items", [])
    if not items: sys.exit("this Google login has no YouTube channel: log in again and pick the AI Playbooks channel")
    ch = items[0]

    env = read_env()
    env.update(YT_CLIENT_ID=c["client_id"], YT_CLIENT_SECRET=c["client_secret"],
               YT_REFRESH_TOKEN=tok["refresh_token"], YT_CHANNEL_ID=ch["id"])
    ENV.write_text("".join(f"{k}={v}\n" for k, v in env.items()), encoding="utf-8")
    print(f"YouTube channel : {ch['snippet']['title']} ({ch['snippet'].get('customUrl', '')}, {ch['id']})")
    print(f"Permissions     : {'all granted' if not missing else 'MISSING ' + ', '.join(missing)}")
    print(f"saved to {ENV}")


if __name__ == "__main__":
    main()
