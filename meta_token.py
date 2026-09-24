"""One-time Meta token setup: short-lived user token -> never-expiring Page token + IDs, written to .env.

1. Put these in .env (next to this file; .env is gitignored):
       META_APP_ID=...
       META_APP_SECRET=...
       META_SHORT_TOKEN=...   (Graph API Explorer user token with the publishing permissions)
2. python meta_token.py [--page "AI Playbooks"]

Writes META_PAGE_TOKEN, FB_PAGE_ID, IG_USER_ID into .env and removes META_SHORT_TOKEN.
Never prints token values. The Page token comes from a long-lived user token, so it doesn't expire
(it stops working if the password changes or the app loses its permissions: then run this again).
"""
import sys, json, pathlib, argparse, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).parent.resolve()
ENV = ROOT / ".env"
GRAPH = "https://graph.facebook.com"
NEEDED = {"instagram_basic", "instagram_content_publish", "pages_show_list", "pages_read_engagement", "pages_manage_posts"}


def read_env():
    env = {}
    if ENV.exists():
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def write_env(env):
    ENV.write_text("".join(f"{k}={v}\n" for k, v in env.items()), encoding="utf-8")


def call(path, **params):
    url = f"{GRAPH}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as ex:  # Graph errors come back as JSON; show the message, never the URL (it has tokens)
        err = json.loads(ex.read() or b"{}").get("error", {})
        sys.exit(f"Graph API error on /{path}: {err.get('message', ex)} (code {err.get('code')})")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--page", default="AI Playbooks")
    a = ap.parse_args()
    env = read_env()
    missing = [k for k in ("META_APP_ID", "META_APP_SECRET", "META_SHORT_TOKEN") if not env.get(k)]
    if missing: sys.exit(f"missing in {ENV}: {', '.join(missing)}")
    app_id, secret = env["META_APP_ID"], env["META_APP_SECRET"]

    long_user = call("oauth/access_token", grant_type="fb_exchange_token", client_id=app_id,
                     client_secret=secret, fb_exchange_token=env["META_SHORT_TOKEN"])["access_token"]
    scopes = set(call("debug_token", input_token=long_user, access_token=f"{app_id}|{secret}")["data"].get("scopes", []))
    if NEEDED - scopes: sys.exit(f"token is missing permissions: {', '.join(sorted(NEEDED - scopes))} (tick them in Graph API Explorer)")

    pages = call("me/accounts", access_token=long_user,
                 fields="id,name,access_token,instagram_business_account{id,username}")["data"]
    page = next((p for p in pages if p["name"].lower() == a.page.lower()), None)
    if not page: sys.exit(f"page '{a.page}' not found; the token can see: {', '.join(p['name'] for p in pages) or 'no pages'}")
    ig = page.get("instagram_business_account")
    if not ig: sys.exit(f"page '{page['name']}' has no linked Instagram professional account (Page settings -> Linked accounts)")

    info = call("debug_token", input_token=page["access_token"], access_token=f"{app_id}|{secret}")["data"]
    env.pop("META_SHORT_TOKEN", None)
    env.update(FB_PAGE_ID=page["id"], IG_USER_ID=ig["id"], META_PAGE_TOKEN=page["access_token"])
    write_env(env)
    exp = info.get("expires_at", 0)
    print(f"Facebook Page : {page['name']} ({page['id']})")
    print(f"Instagram     : @{ig.get('username')} ({ig['id']})")
    print(f"Page token    : {'never expires' if not exp else f'expires at unix {exp}'}; valid={info.get('is_valid')}")
    print(f"Permissions   : {', '.join(sorted(scopes))}")
    print(f"saved to {ENV} (META_SHORT_TOKEN removed)")


if __name__ == "__main__":
    main()
