"""One-time setup (and health check) of the Instagram comment-to-DM bot (bot/worker.js on Cloudflare Workers).

Usage:
    python dm_setup.py            deploy the Worker, upload its secrets, subscribe Meta's webhooks to it
    python dm_setup.py --check    only show the state (Worker health, Meta subscriptions), change nothing
    python dm_setup.py --register content/<post>.json WORD
                                  test the bot on an already published post: saves dm.keyword into the JSON and
                                  registers it (page + gh-pages dm.json) without touching the published caption

Needs: a (free) Cloudflare account and `npx wrangler login` done once (opens the browser); .env with META_APP_ID,
META_APP_SECRET, META_PAGE_TOKEN, FB_PAGE_ID, IG_USER_ID. Writes DM_VERIFY_TOKEN and DM_BOT_URL into .env.
Secret values are never printed. Owner-side switch that no API can flip: Instagram app → Settings → Messages and
story replies → Message controls → Connected tools → "Allow access to messages" ON.
"""
import sys, re, json, secrets, pathlib, subprocess, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).parent.resolve()
BOT = ROOT / "bot"
GRAPH = "https://graph.facebook.com/v25.0"
FIELDS = "comments,messages,messaging_postbacks"
NPX = "npx.cmd" if sys.platform == "win32" else "npx"


def env():
    out = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1); out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def set_env(key, value):
    f = ROOT / ".env"; lines = [l for l in f.read_text(encoding="utf-8").splitlines() if not l.startswith(key + "=")]
    f.write_text("\n".join(lines + [f"{key}={value}"]) + "\n", encoding="utf-8")


def api(method, path, params):
    data = urllib.parse.urlencode(params).encode() if method == "POST" else None
    url = GRAPH + path + ("" if data else "?" + urllib.parse.urlencode(params))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method), timeout=60) as r: return json.load(r)
    except urllib.error.HTTPError as ex:
        return {"error": json.load(ex).get("error", {}).get("message", str(ex))}


def wrangler(*args, stdin=None):
    return subprocess.run([NPX, "--yes", "wrangler", *args], cwd=BOT, input=stdin, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def check(e):
    url = e.get("DM_BOT_URL")
    print("Worker:", url or "not deployed yet")
    if url:
        try:
            with urllib.request.urlopen(url + "/health", timeout=20) as r: print("  health:", r.read().decode()[:200])
        except OSError as ex: print("  health: FAIL", ex)
    app = f"{e['META_APP_ID']}|{e['META_APP_SECRET']}"
    subs = api("GET", f"/{e['META_APP_ID']}/subscriptions", {"access_token": app})
    for s in subs.get("data", []):
        print(f"Meta app webhook: {s['object']} -> {s.get('callback_url')} fields {[f['name'] for f in s.get('fields', [])]} active={s.get('active')}")
    if subs.get("error"): print("Meta app webhook: ERROR", subs["error"])
    page = api("GET", f"/{e['FB_PAGE_ID']}/subscribed_apps", {"access_token": e["META_PAGE_TOKEN"]})
    print("Page subscribed apps:", [(a.get("name"), a.get("subscribed_fields")) for a in page.get("data", [])] or page.get("error"))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    e = env()
    if "--check" in sys.argv: return check(e)
    if "--register" in sys.argv:
        i = sys.argv.index("--register"); content, kw = sys.argv[i + 1], sys.argv[i + 2].upper()
        if not re.fullmatch(r"[A-Z0-9]{2,20}", kw): sys.exit("keyword: 2-20 letters/digits")
        sys.path.insert(0, str(ROOT)); import publish as P
        f = pathlib.Path(content); data = json.loads(f.read_text(encoding="utf-8"))
        data["dm"] = {**(data.get("dm") or {}), "keyword": kw}
        f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        post = P.Post(content); post.state.pop("dm", None); P.dm(post)
        return print(f"Test: comment {kw} under the post from a test account (the page may take ~1 min to go live).")
    who = wrangler("whoami")
    if "You are logged in" not in who.stdout + who.stderr:
        sys.exit("Cloudflare: not logged in. Run once:  cd bot && npx wrangler login   (opens the browser), then rerun.")
    if not e.get("DM_VERIFY_TOKEN"): set_env("DM_VERIFY_TOKEN", secrets.token_urlsafe(24)); e = env()
    d = wrangler("deploy")
    out = d.stdout + d.stderr
    if d.returncode: sys.exit("wrangler deploy failed:\n" + out[-1500:])
    m = re.search(r"https://[\w.-]+\.workers\.dev", out)
    if not m: sys.exit("deployed, but no workers.dev URL in the output:\n" + out[-800:])
    url = m.group(0); set_env("DM_BOT_URL", url); print("deployed:", url)
    for name, key in (("PAGE_TOKEN", "META_PAGE_TOKEN"), ("APP_SECRET", "META_APP_SECRET"), ("VERIFY_TOKEN", "DM_VERIFY_TOKEN")):
        r = wrangler("secret", "put", name, stdin=e[key])
        print(f"secret {name}:", "ok" if r.returncode == 0 else "FAILED " + (r.stderr or r.stdout)[-300:])
    app = f"{e['META_APP_ID']}|{e['META_APP_SECRET']}"
    r = api("POST", f"/{e['META_APP_ID']}/subscriptions", {"object": "instagram", "callback_url": url, "fields": FIELDS,
                                                          "verify_token": e["DM_VERIFY_TOKEN"], "include_values": "true", "access_token": app})
    print("Meta webhook (instagram):", r)
    r = api("POST", f"/{e['FB_PAGE_ID']}/subscribed_apps", {"subscribed_fields": "feed,messages", "access_token": e["META_PAGE_TOKEN"]})
    print("Page subscription:", r)
    check(env())


if __name__ == "__main__":
    main()
