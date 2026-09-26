// AI Playbooks · Instagram comment-to-DM bot with a follow gate (Cloudflare Worker, free tier).
//
// Flow (owner, 2026-09-26):
//   1. Someone comments the post's keyword (e.g. "AGENT") under one of our Instagram posts.
//   2. We send ONE private reply (Instagram allows exactly one, within 7 days of the comment): "follow us, then tap
//      ✅" with a quick-reply button, and a short public reply under the comment ("Sent you a DM 📩").
//   3. They tap the button (this opens a 24 h messaging window) -> we check is_user_follow_business:
//      following -> the link (the post's page, from dm.json); not yet -> "follow first" + the button again.
//   Typing the keyword (or "done") in a DM works too.
// Which post has which keyword and link: DM_MAP_URL (gh-pages dm.json, written by publish.py's `dm` step).
// Secrets (wrangler secret put): PAGE_TOKEN, APP_SECRET, VERIFY_TOKEN. Vars in wrangler.toml.

const GRAPH = "https://graph.facebook.com/v25.0";

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    if (req.method === "GET" && url.searchParams.get("hub.mode") === "subscribe") {  // Meta's webhook verification
      return url.searchParams.get("hub.verify_token") === env.VERIFY_TOKEN
        ? new Response(url.searchParams.get("hub.challenge")) : new Response("forbidden", { status: 403 });
    }
    if (req.method === "GET" && url.pathname === "/health") {
      const map = await dmMap(env);
      return Response.json({ ok: true, posts: Object.keys(map).length });
    }
    if (req.method !== "POST") return new Response("AI Playbooks DM bot");
    const raw = await req.text();
    if (!(await validSignature(raw, req.headers.get("x-hub-signature-256"), env.APP_SECRET)))
      return new Response("bad signature", { status: 401 });
    let body; try { body = JSON.parse(raw); } catch { return new Response("bad json", { status: 400 }); }
    ctx.waitUntil(handle(body, env).catch(e => console.log("handle error", e.stack || e)));
    return new Response("ok");  // Meta wants a 200 within seconds; the work continues in waitUntil
  },
};

// ---------------------------------------------------------------- webhook events

async function handle(body, env) {
  if (body.object !== "instagram") return;
  for (const entry of body.entry || []) {
    for (const ch of entry.changes || []) if (ch.field === "comments") await onComment(ch.value, env);
    for (const m of entry.messaging || []) await onMessage(m, env);
  }
}

async function onComment(v, env) {
  const from = v.from || {}, mediaId = (v.media || {}).id, text = v.text || "";
  if (!v.id || !mediaId || from.id === env.IG_USER_ID) return;       // our own comments / replies
  const post = (await dmMap(env))[mediaId];
  if (!post || !hasWord(text, post.keyword)) return;
  if (await seen(`c-${v.id}`)) return;                                 // Meta sometimes delivers twice
  const r = await send(env, { comment_id: v.id }, gateMessage(post, mediaId, from.username));
  console.log("private reply", v.id, from.username, r.error ? JSON.stringify(r.error) : "ok");
  if (!r.error) await graph(env, "POST", `/${v.id}/replies`, { message: pick(PUBLIC_REPLIES) });
}

async function onMessage(m, env) {
  const msg = m.message || {}, pb = m.postback || {};
  if (msg.is_echo || !m.sender || m.sender.id === env.IG_USER_ID) return;
  const payload = (msg.quick_reply || {}).payload || pb.payload || "";
  const text = (msg.text || "").trim();
  const map = await dmMap(env);
  let mediaId = null;
  if (payload.startsWith("FOLLOWED|")) mediaId = payload.split("|")[1];
  else if (text) {  // typed the keyword in a DM: the newest post with that keyword
    const hit = Object.entries(map).filter(([, p]) => hasWord(text, p.keyword))
      .sort((a, b) => (b[1].added || "").localeCompare(a[1].added || ""))[0];
    if (hit) mediaId = hit[0];
    else if (/^(done|followed|i followed|ok|takip ettim)\b/i.test(text)) mediaId = await lastGate(m.sender.id);
  }
  const post = mediaId && map[mediaId];
  if (!post) return;
  const who = { id: m.sender.id };
  const prof = await graph(env, "GET", `/${m.sender.id}`, { fields: "username,is_user_follow_business" });
  if (prof.error) console.log("profile error", JSON.stringify(prof.error));
  if (prof.is_user_follow_business) {
    await send(env, who, linkMessage(post));
    console.log("link sent", prof.username, mediaId);
  } else {
    await rememberGate(m.sender.id, mediaId);
    await send(env, who, notYetMessage(post, mediaId, prof.username));
    console.log("not following yet", prof.username || m.sender.id, mediaId);
  }
}

// ---------------------------------------------------------------- messages (varied so they never feel canned)

const PUBLIC_REPLIES = ["Sent you a DM 📩", "Check your DMs 👀", "Just sent it to your inbox 📬", "DM sent! 🚀",
  "It's in your DMs ✨", "Sliding into your DMs now 📩"];

function button(mediaId) {
  return [{ content_type: "text", title: pick(["✅ I followed", "✅ Done, I follow", "✅ Following!"]), payload: `FOLLOWED|${mediaId}` }];
}

function gateMessage(post, mediaId, user) {
  const hi = user ? `Hey @${user}! ` : "Hey! ";
  const text = hi + pick([
    `👋 Your link is ready. One quick step: follow @aiplaybooks.daily, then tap the button below to unlock it 👇`,
    `🎁 The full ${short(post)} is waiting for you. Follow @aiplaybooks.daily and tap the button to get the link 👇`,
    `🔒 This link is for our followers. Follow @aiplaybooks.daily, then tap ✅ below and it's yours 👇`,
  ]);
  return { text, quick_replies: button(mediaId) };
}

function notYetMessage(post, mediaId, user) {
  return {
    text: pick([
      `Hmm, it looks like you're not following @aiplaybooks.daily yet 🙂 Follow us, then tap the button again to unlock the link.`,
      `Almost there! 🔒 Follow @aiplaybooks.daily first, then tap ✅ again and the link is yours.`,
      `I can't see the follow yet 👀 Follow @aiplaybooks.daily and tap the button again (it can take a few seconds to show up).`,
    ]),
    quick_replies: button(mediaId),
  };
}

function linkMessage(post) {
  return {
    attachment: { type: "template", payload: { template_type: "button",
      text: pick(["You're in! 🎉 Here it is:", "Thanks for following! 🙌 Here's your link:", "Unlocked 🔓 Enjoy:"]) + " " + post.title.slice(0, 500),
      buttons: [{ type: "web_url", url: post.link, title: pick(["Open the prompts", "Get the full guide", "Open it"]) }] } },
  };
}

// ---------------------------------------------------------------- helpers

async function send(env, recipient, message) {
  const r = await graph(env, "POST", `/${env.PAGE_ID}/messages`, { recipient, message });
  if (r.error && message.attachment) {  // a client that can't show the button still gets the link
    const b = message.attachment.payload;
    return graph(env, "POST", `/${env.PAGE_ID}/messages`, { recipient, message: { text: `${b.text}\n${b.buttons[0].url}` } });
  }
  return r;
}

async function graph(env, method, path, params) {
  const u = new URL(GRAPH + path);
  let init = { method };
  if (method === "GET") { for (const [k, v] of Object.entries(params || {})) u.searchParams.set(k, v); }
  else init = { method, headers: { "content-type": "application/json" }, body: JSON.stringify(params || {}) };
  u.searchParams.set("access_token", env.PAGE_TOKEN);
  const r = await fetch(u, init);
  try { return await r.json(); } catch { return { error: { message: `HTTP ${r.status}` } }; }
}

let MAP = null, MAP_AT = 0;
async function dmMap(env) {
  if (MAP && Date.now() - MAP_AT < 60_000) return MAP;
  try {
    const r = await fetch(env.DM_MAP_URL + "?t=" + Math.floor(Date.now() / 60_000), { cf: { cacheTtl: 60 } });
    if (r.ok) { MAP = await r.json(); MAP_AT = Date.now(); }
  } catch (e) { console.log("dm map error", e); }
  return MAP || {};
}

function hasWord(text, kw) {
  return !!kw && new RegExp(`(^|[^\\p{L}\\p{N}])${kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}($|[^\\p{L}\\p{N}])`, "iu").test(text);
}
const pick = a => a[Math.floor(Math.random() * a.length)];
const short = p => /prompt/i.test(p.title) ? "prompt pack" : "guide";

// small per-datacenter memory (Cache API; free): duplicate webhooks + which post a DM thread was about
async function seen(key) {
  const k = new Request(`https://dm-bot.local/${key}`);
  if (await caches.default.match(k)) return true;
  await caches.default.put(k, new Response("1", { headers: { "cache-control": "max-age=604800" } }));
  return false;
}
async function rememberGate(user, mediaId) {
  await caches.default.put(new Request(`https://dm-bot.local/g-${user}`), new Response(mediaId, { headers: { "cache-control": "max-age=86400" } }));
}
async function lastGate(user) {
  const r = await caches.default.match(new Request(`https://dm-bot.local/g-${user}`));
  return r ? r.text() : null;
}

async function validSignature(raw, header, secret) {
  if (!header || !secret) return false;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(raw));
  const hex = [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
  const want = header.replace(/^sha256=/, "");
  if (want.length !== hex.length) return false;
  let d = 0; for (let i = 0; i < hex.length; i++) d |= hex.charCodeAt(i) ^ want.charCodeAt(i);
  return d === 0;
}
