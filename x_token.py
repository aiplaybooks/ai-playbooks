"""One-time X (Twitter) login for posting: OAuth 2.0 (confidential client, PKCE, loopback) -> refresh token in .env.

The developer console's own "Generate" button makes tokens for the account that owns the developer app, not for our
page's X account, so the page's account authorizes the app here instead.
1. X developer console -> the app "AI Playbooks Publisher" -> User authentication settings -> Callback URI:
   add  http://127.0.0.1:8766/x  (exactly this).
2. In the default browser, be logged in to X with the AI PLAYBOOKS account (log out of any other account first).
3. python x_token.py      (the browser opens: "Authorize app")

Needs X_CLIENT_ID + X_CLIENT_SECRET in .env. Writes X_REFRESH_TOKEN, X_USER_ID, X_USERNAME. Never prints token values.
X rotates the refresh token on every use (valid 6 months unused): `refresh()` saves the new one each time.
"""
import sys, json, base64, hashlib, secrets, pathlib, threading, webbrowser, urllib.parse, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = pathlib.Path(__file__).parent.resolve()
ENV = ROOT / ".env"
PORT, PATH = 8766, "/x"
REDIRECT = f"http://127.0.0.1:{PORT}{PATH}"
SCOPES = ["tweet.read", "tweet.write", "users.read", "media.write", "offline.access"]


def read_env():
    env = {}
    if ENV.exists():
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def save_env(**kv):
    env = read_env(); env.update(kv)
    ENV.write_text("".join(f"{k}={v}\n" for k, v in env.items()), encoding="utf-8")


def token_request(data, env=None):
    env = env or read_env()
    basic = base64.b64encode(f"{env['X_CLIENT_ID']}:{env['X_CLIENT_SECRET']}".encode()).decode()
    req = urllib.request.Request("https://api.x.com/2/oauth2/token", urllib.parse.urlencode(data).encode(),
                                 headers={"Authorization": f"Basic {basic}",
                                          "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())
    except urllib.error.HTTPError as ex:
        body = json.loads(ex.read() or b"{}")
        raise RuntimeError(f"X token request failed ({ex.code}): {body.get('error_description') or body.get('error') or body}")


def refresh():
    """-> a fresh access token (2 h). Saves the rotated refresh token right away (the old one is dead after this)."""
    env = read_env()
    if not env.get("X_REFRESH_TOKEN"): raise RuntimeError("no X login yet: run `python x_token.py` once")
    tok = token_request({"grant_type": "refresh_token", "refresh_token": env["X_REFRESH_TOKEN"]}, env)
    if tok.get("refresh_token"): save_env(X_REFRESH_TOKEN=tok["refresh_token"])
    return tok["access_token"]


def me(access):
    req = urllib.request.Request("https://api.x.com/2/users/me", headers={"Authorization": f"Bearer {access}"})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())["data"]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    env = read_env()
    if not env.get("X_CLIENT_ID") or not env.get("X_CLIENT_SECRET"): sys.exit("X_CLIENT_ID / X_CLIENT_SECRET missing in .env")
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16); got = {}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query))
            if u.path != PATH or ("code" not in q and "error" not in q): self.send_response(404); self.end_headers(); return
            got.update(q)
            ok = q.get("state") == state and "code" in q
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(("<h2>AI Playbooks: X bağlandı. Bu sekmeyi kapatabilirsin.</h2>" if ok else
                              f"<h2>Giriş başarısız: {q.get('error', 'state mismatch')}</h2>").encode())
            threading.Thread(target=srv.shutdown, daemon=True).start()

    srv = HTTPServer(("127.0.0.1", PORT), H)
    url = "https://x.com/i/oauth2/authorize?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": env["X_CLIENT_ID"], "redirect_uri": REDIRECT, "scope": " ".join(SCOPES),
        "state": state, "code_challenge": challenge, "code_challenge_method": "S256"})
    print("Opening the browser for the X login (use the AI Playbooks account). If it doesn't open, visit:\n" + url, flush=True)
    webbrowser.open(url)
    srv.serve_forever()
    if got.get("state") != state or "code" not in got: sys.exit(f"login failed: {got.get('error', 'state mismatch')}")

    try:
        tok = token_request({"grant_type": "authorization_code", "code": got["code"], "redirect_uri": REDIRECT,
                             "code_verifier": verifier, "client_id": env["X_CLIENT_ID"]}, env)
    except RuntimeError as ex: sys.exit(str(ex))
    if "refresh_token" not in tok: sys.exit("no refresh token returned (offline.access missing?)")
    user = me(tok["access_token"])
    granted = set(tok.get("scope", "").split()); missing = [s for s in SCOPES if s not in granted]
    save_env(X_REFRESH_TOKEN=tok["refresh_token"], X_USER_ID=user["id"], X_USERNAME=user["username"])
    print(f"X account   : {user['name']} (@{user['username']}, {user['id']})")
    print(f"Permissions : {'all granted' if not missing else 'MISSING ' + ', '.join(missing)}")
    print(f"saved to {ENV}")


if __name__ == "__main__":
    main()
