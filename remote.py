"""Phone access to the Studio (owner, 2026-09-29): a free Cloudflare quick tunnel + a secret key.

The Studio starts `bin/cloudflared.exe tunnel --url http://localhost:<port>` at startup (no Cloudflare account, no
domain); cloudflared prints a random https://<words>.trycloudflare.com address, which changes on every restart.
The Studio then sends "<address>/?k=<STUDIO_KEY>" to the owner's Telegram (also on the Telegram command `link`).
Every request that doesn't come from this PC (Host is not localhost) needs the key: `?k=` once, then a cookie
(30 days). Without it: 401. The key lives in .env (STUDIO_KEY, created on first start) and is never logged.
If the tunnel process dies, it is restarted and the new link goes to Telegram again.
"""
import re, time, secrets, pathlib, threading, subprocess, hmac

ROOT = pathlib.Path(__file__).parent.resolve()
EXE = ROOT / "bin" / "cloudflared.exe"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
COOKIE = "studio_key"
STATE = {"url": None, "since": None, "error": None}
_on_link = None


def key():
    f = ROOT / ".env"; text = f.read_text(encoding="utf-8") if f.exists() else ""
    m = re.search(r"^STUDIO_KEY=(\S+)", text, re.M)
    if m: return m.group(1)
    k = secrets.token_urlsafe(24)
    f.write_text(text.rstrip("\n") + ("\n" if text else "") + f"STUDIO_KEY={k}\n", encoding="utf-8")
    return k


KEY = None


def is_local(host):
    return (host or "").split(":")[0] in ("localhost", "127.0.0.1", "[::1]", "")


def authorized(headers, query):
    """(ok, set_cookie): local requests always pass; remote ones need ?k= or the cookie."""
    if is_local(headers.get("Host")): return True, False
    if hmac.compare_digest(query.get("k", ""), KEY): return True, True
    cookies = dict(c.strip().split("=", 1) for c in (headers.get("Cookie") or "").split(";") if "=" in c)
    return hmac.compare_digest(cookies.get(COOKIE, ""), KEY), False


def cookie_header():
    return f"{COOKIE}={KEY}; Max-Age=2592000; Path=/; HttpOnly; Secure; SameSite=Lax"


def link():
    return f"{STATE['url']}/?k={KEY}" if STATE["url"] else None


def _run(port, log):
    while True:
        if not EXE.exists():
            STATE["error"] = "bin/cloudflared.exe yok"; log("remote: bin/cloudflared.exe missing"); return
        try:
            p = subprocess.Popen([str(EXE), "tunnel", "--no-autoupdate", "--url", f"http://localhost:{port}"],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                 text=True, encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
            for line in p.stdout:
                m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
                if m and m.group(0) != STATE["url"]:
                    STATE.update(url=m.group(0), since=time.time(), error=None)
                    log(f"remote: tunnel up {m.group(0)}")
                    if _on_link:
                        try: _on_link()
                        except Exception as ex: log(f"remote: notify failed {ex}")  # noqa: BLE001
            p.wait()
        except OSError as ex:
            STATE["error"] = str(ex)
        STATE["url"] = None
        log("remote: tunnel stopped, restarting in 30 s")
        time.sleep(30)


def start(port, log, on_link=None):
    global KEY, _on_link
    KEY = key(); _on_link = on_link
    threading.Thread(target=_run, args=(port, log), daemon=True).start()
