"""Turn a carousel content JSON into an animated 1080x1920 Reel (MP4, 30fps, music + optional voice-over).

Usage:
    python reel.py content/2026-09-24_claude-tradingview.json [--theme ledger] [--music path.wav]
                   [--voice am_michael] [--speed 1.05] [--no-voice]

Each theme module provides: render(data), REEL_CSS, ANIM_SEL, TYPE_SEL, DRAW_SEL, ACCENT (optional: CC_CSS).
If slides have a `voiceover` field, voice.py (Kokoro) is run in the Pinokio TTS env: slide length follows the
voice, the typewriter is sped up to finish with it, word-level captions are burned in and the music is ducked.
Output: output/<content-name>/reel.mp4
Requires ffmpeg on PATH.
"""
import sys, os, json, html, re, wave, random, pathlib, subprocess, shutil, argparse
import numpy as np
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))
from carousel import load  # noqa: E402

FPS = 30
CPS = 75       # typewriter speed (characters per second)
MAX_CPS = 180  # fastest the typewriter may go to keep up with the voice
LEAD = 0.15    # voice starts this long after the slide appears
TAIL = 0.25    # pause after the voice before the next slide
VO_MIN = {"cover": 2.4, "prompt": 2.8}  # minimum slide length with voice-over (others: 2.8)

# Voice pool (owner's picks). A new post gets the least-recently-used voice; the pick is saved into its JSON.
VOICES = ["af_sarah", "af_jessica", "am_liam", "am_fenrir", "am_puck", "am_eric", "am_adam"]

# Kokoro lives in Pinokio's Ultimate-TTS-Studio env; used read-only.
PINOKIO_TTS = pathlib.Path(r"E:\pinokio-new\api\Ultimate-TTS-Studio.git")
KOKORO_PY = os.environ.get("KOKORO_PYTHON", str(PINOKIO_TTS / "app" / "tts_env" / "python.exe"))
KOKORO_HF_HOME = os.environ.get("KOKORO_HF_HOME", str(PINOKIO_TTS / "cache" / "HF_HOME"))
KOKORO_CUDA_HOME = r"E:\pinokio-new\bin\miniforge\Library"  # deepspeed (pulled in by transformers) wants it

JS = """
<script>
const q=s=>s?[...document.querySelectorAll(s)]:[];
const anim=q(%(anim)s);
anim.forEach((el,i)=>el.dataset.d=(0.15+i*0.16).toFixed(2));
const draw=%(draw)s?document.querySelector(%(draw)s):null;
const term=%(type)s?document.querySelector(%(type)s):null; let orig=null,total=0;
if(term){orig=term.cloneNode(true); total=term.textContent.length;}
const CC=%(cc)s; const cc=document.getElementById('cc');
function cut(src,n){const dst=src.cloneNode(false);
  for(const c of src.childNodes){ if(n<=0)break;
    if(c.nodeType===3){dst.appendChild(document.createTextNode(c.textContent.slice(0,n))); n-=c.textContent.length;}
    else{const r=cut(c,n); dst.appendChild(r.node); n=r.left;} }
  return {node:dst,left:n};}
const ease=x=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
function holder(el){let p=el; while(p&&!p.dataset.d)p=p.parentElement; return p;}
window.setT=(t,dur,gp,cps,typeEnd)=>{
  for(const el of anim){const p=ease((t-el.dataset.d)/0.45);
    el.style.opacity=p; el.style.transform=`translateY(${(1-p)*44}px)`;}
  if(draw){const p=ease((t-0.9)/1.4); draw.style.clipPath=`inset(0 ${(1-p)*100}%% 0 0)`;}
  if(term){const h=holder(term); const td=(h?parseFloat(h.dataset.d):0.3)+0.45;
    if(typeEnd>0) cps=Math.min(%(maxcps)s,Math.max(cps,total/Math.max(0.5,typeEnd-td)));
    const n=Math.max(0,Math.floor((t-td)*cps));
    term.innerHTML=cut(orig,Math.min(n,total)).node.innerHTML;
    if(n<total+cps*1.5 && Math.floor(t*2.5)%%2===0){const c=document.createElement('span');c.className='caret';c.innerHTML='&nbsp;';term.appendChild(c);} }
  if(cc){const g=CC.find(g=>t>=g.s&&t<g.e);
    if(!g){cc.style.opacity=0;}
    else{let on=0; g.w.forEach((w,i)=>{if(t>=w[1])on=i;});
      cc.firstChild.innerHTML=g.w.map((w,i)=>`<span class="${i===on?'on':''}">${w[0]}</span>`).join(' ');
      const p=ease((t-g.s)/0.14); cc.style.opacity=1; cc.firstChild.style.transform=`scale(${0.9+0.1*p})`;}}
  const b=document.querySelector('.body'); const x=ease((t-(dur-0.35))/0.35);
  if(b){b.style.opacity=1-x; b.style.transform=`translateY(${-40*x}px)`;}
  document.getElementById('prog').style.width=(gp*100)+'%%';
};
</script>"""

CC_CSS = """
#cc{position:fixed;left:60px;right:60px;bottom:345px;height:170px;display:flex;align-items:center;justify-content:center;z-index:8;opacity:0}
#cc div{max-width:900px;text-align:center;font-family:Inter,sans-serif;font-weight:800;font-size:60px;line-height:1.16;letter-spacing:-.5px;
  color:#fff;background:rgba(10,10,14,.84);padding:16px 30px 20px;border-radius:24px;transform-origin:50%% 100%%}
#cc .on{color:%s}
body .wrap{bottom:540px !important}
"""


def phrases(words, offset, end):
    """Group Kokoro word timings into short caption phrases (<= 4 words / ~22 chars, break at punctuation)."""
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or sum(len(x[0]) + 1 for x in cur) > 22 or re.search(r"[.,!?:;]$", w[0]):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    for i in range(len(groups) - 1, 0, -1):  # no one-word orphans: fold them into the previous phrase
        if len(groups[i]) == 1 and len(groups[i - 1]) < 5 and not re.search(r"[.!?]$", groups[i - 1][-1][0]):
            groups[i - 1] += groups.pop(i)
    out = []
    for i, g in enumerate(groups):
        s = offset + g[0][1] - 0.05
        e = offset + groups[i + 1][0][1] - 0.05 if i + 1 < len(groups) else min(offset + g[-1][2] + 0.5, end - 0.3)
        out.append({"s": round(s, 3), "e": round(e, 3), "w": [[html.escape(x[0]), round(offset + x[1], 3)] for x in g]})
    return out


def duration(s, vo=None):
    t = s["type"]
    if vo:
        d = max(VO_MIN.get(t, 2.8), LEAD + vo["dur"] + TAIL)
        if t == "prompt": d = max(d, 0.9 + len(s["prompt"]) / MAX_CPS + 0.7)
        return round(d, 2)
    if t == "cover": return 3.6
    if t == "prompt": return round(1.3 + len(s["prompt"]) / CPS + 2.4, 2)
    if t in ("facts", "limits", "cta"): return 5.2
    return 4.8


def pick_voice(content, data):
    """Voice for this post: its own `voice` field, else the least-recently-used pool voice (saved back to the JSON)."""
    if data.get("voice") in VOICES: return data["voice"]
    content = pathlib.Path(content).resolve(); history = []
    for f in sorted(content.parent.glob("*.json")):  # file names start with the date, so this is posting order
        if f != content: history.append(json.loads(f.read_text(encoding="utf-8")).get("voice"))
    last = {v: max([i for i, h in enumerate(history) if h == v], default=-1) for v in VOICES}
    oldest = min(last.values())
    voice = random.Random(content.stem).choice([v for v in VOICES if last[v] == oldest])
    raw = json.loads(content.read_text(encoding="utf-8"))
    raw = {**{k: v for k, v in raw.items() if k not in ("slides", "voice")}, "voice": voice, "slides": raw["slides"]}
    content.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("voice:", voice, "(saved to content JSON)")
    return voice


def synth_voice(content, out, voice, speed):
    vdir = out / "voice"; shutil.rmtree(vdir, ignore_errors=True)
    env = dict(os.environ, HF_HOME=KOKORO_HF_HOME, HF_HUB_OFFLINE="1", PYTHONIOENCODING="utf-8")
    if not env.get("CUDA_HOME") and os.path.isdir(KOKORO_CUDA_HOME): env["CUDA_HOME"] = KOKORO_CUDA_HOME
    cmd = [KOKORO_PY, str(ROOT / "voice.py"), str(content), str(vdir)]
    if voice: cmd += ["--voice", voice]
    if speed: cmd += ["--speed", str(speed)]
    subprocess.run(cmd, check=True, env=env)
    man = json.loads((vdir / "voice.json").read_text(encoding="utf-8"))
    return vdir, man


def read_wav(path):
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content"); ap.add_argument("--theme"); ap.add_argument("--music")
    ap.add_argument("--voice", help="Kokoro voice override for this render (default: the post's voice, else rotate through VOICES)")
    ap.add_argument("--speed", type=float); ap.add_argument("--no-voice", action="store_true")
    a = ap.parse_args()
    data, theme = load(a.content, a.theme)
    out = ROOT / "output" / pathlib.Path(a.content).stem
    frames = out / "frames"; shutil.rmtree(frames, ignore_errors=True); frames.mkdir(parents=True)

    vos = [None] * len(data["slides"])
    if not a.no_voice and any(s.get("voiceover") for s in data["slides"]):
        vdir, man = synth_voice(a.content, out, a.voice or pick_voice(a.content, data), a.speed); vos = man["slides"]

    css = ("<style>body{height:1920px !important}"
           f"#prog{{position:fixed;left:0;top:0;height:8px;background:{theme.ACCENT};z-index:9;width:0}}"
           ".caret{display:inline-block;width:.55em;margin-left:2px}" + theme.REEL_CSS)
    if any(vos): css += CC_CSS % getattr(theme, "CC_ACTIVE", theme.ACCENT) + getattr(theme, "CC_CSS", "")
    css += "</style>"

    pages = theme.render(data)
    durs = [duration(s, v) for s, v in zip(data["slides"], vos)]
    total = sum(durs); print("slide durations:", durs, "total:", round(total, 1), "s")

    fi = 0; elapsed = 0.0
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for n, (h, d, vo) in enumerate(zip(pages, durs, vos), 1):
            cc = phrases(vo["words"], LEAD, d) if vo else []
            type_end = LEAD + vo["dur"] - 0.1 if vo else 0
            js = JS % {"anim": json.dumps(theme.ANIM_SEL), "type": json.dumps(theme.TYPE_SEL),
                       "draw": json.dumps(theme.DRAW_SEL), "cc": json.dumps(cc), "maxcps": MAX_CPS}
            extra = '<div id="cc"><div></div></div>' if vo else ""
            h = h.replace("</head>", css + "</head>").replace("</body>", '<div id="prog"></div>' + extra + js + "</body>")
            h = h.replace("Swipe →", "")
            f = out / f"reel_{n:02d}.html"; f.write_text(h, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(300)
            for k in range(int(round(d * FPS))):
                t = k / FPS
                pg.evaluate(f"setT({t},{d},{(elapsed + t) / total},{CPS},{type_end})")
                pg.screenshot(path=str(frames / f"{fi:05d}.jpg"), type="jpeg", quality=92); fi += 1
            elapsed += d
        br.close()
    print("frames:", fi)

    music = a.music
    if not music:
        music = str(out / "music.wav")
        subprocess.run([sys.executable, str(ROOT / "music.py"), music, str(total + 0.5)], check=True)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%05d.jpg"), "-i", music]
    if any(vos):
        sr = man["sr"]; track = np.zeros(int((total + 0.5) * sr), np.float32); start = 0.0
        for d, vo in zip(durs, vos):
            if vo:
                clip = read_wav(vdir / vo["file"]); i = int((start + LEAD) * sr)
                track[i:i + len(clip)] += clip[:len(track) - i]
            start += d
        with wave.open(str(out / "voice.wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(track, -1, 1) * 32767).astype(np.int16).tobytes())
        # music sits under the voice and ducks further while it speaks; then normalise to IG loudness
        cmd += ["-i", str(out / "voice.wav"), "-filter_complex",
                "[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[vo][sc];"
                "[1:a]aresample=48000,volume=0.45[mu];"
                "[mu][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[duck];"
                "[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
                "-map", "0:v", "-map", "[a]"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-r", str(FPS), "-c:a", "aac", "-ar", "48000", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", str(out / "reel.mp4")]
    subprocess.run(cmd, check=True)
    shutil.rmtree(frames, ignore_errors=True)
    print("saved", out / "reel.mp4")


if __name__ == "__main__":
    main()
