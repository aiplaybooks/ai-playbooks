"""Turn a picked video clip into our Reel (1080x1920): the clip ITSELF, full screen, nothing drawn on it.

Owner, 2026-10-06: the old hook-framed look (black frame, brand line + hook on top, "Source: @creator" under the clip)
is gone. The clip is published as it is; hook, description and credit live in the CAPTION (prompts/caption.md).

Usage:
    python clip.py <video file or post URL> [--name my-clip] [--fit auto|contain|fill] [--crop-pos 0.5]
    python clip.py content/clips/<name>.json      (Studio: layout options from the JSON; the clip is
                                                  output/clips/<name>/source.mp4 if already fetched)
A URL (X / Reddit / ...) is fetched with yt-dlp: only for a single post the owner picked (see CLAUDE.md, viral Reels).
Layout (CLI or JSON): fit "auto" (default: a clip that is already about 9:16 fills the screen, any other shape is shown
whole on a blurred copy of itself) | "fill" (always crop to full screen) | "contain" (never crop); crop_pos 0..1 = which
part a crop keeps (0 top, 0.5 middle, 1 bottom). Black bars baked into the source are detected and cut first.
Output: output/clips/<name>/reel.mp4 (+ cover.jpg = first frame, check_1..5.jpg, meta.json)
Keeps the clip's own audio (loudness-normalised); max 90 s. Needs ffmpeg + ffprobe on PATH.
"""
import sys, json, re, pathlib, argparse, subprocess

ROOT = pathlib.Path(__file__).parent.resolve()
W, H = 1080, 1920
MAX_SECS = 90
NEAR = 0.08          # a clip within 8% of 9:16 is treated as vertical: crop it to full screen
VIDEO = (".mp4", ".webm", ".mkv", ".mov")


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe(f):
    d = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(f)]).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    rot = int((v.get("tags") or {}).get("rotate", 0) or 0)
    for sd in v.get("side_data_list") or []:
        if "rotation" in sd: rot = int(sd["rotation"])
    w, h = int(v["width"]), int(v["height"])
    if abs(rot) in (90, 270): w, h = h, w
    return w, h, float(d["format"]["duration"]), any(s["codec_type"] == "audio" for s in d["streams"])


def fetch(url, out):
    run([sys.executable, "-m", "yt_dlp", "-q", "--no-playlist", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
         "-o", str(out / "source.%(ext)s"), url])
    return next(f for f in out.glob("source.*") if f.suffix in VIDEO)


def debar(src, vw, vh, dur):
    """Black bars baked into the source (a 2.39:1 film inside a 16:9 frame) would become bars inside our frame:
    find them with cropdetect and cut them away first. Returns (w, h, filter prefix)."""
    best = {}
    for t0 in (dur * 0.2, dur * 0.5, dur * 0.8):
        try:
            r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{t0:.2f}", "-i", str(src), "-frames:v", "14",
                                "-vf", "cropdetect=limit=16:round=2:reset=0", "-f", "null", "-"],
                               capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.SubprocessError): return vw, vh, ""
        for m in re.finditer(r"crop=(\d+):(\d+):(\d+):(\d+)", r.stderr or ""):
            best[tuple(int(x) for x in m.groups())] = best.get(tuple(int(x) for x in m.groups()), 0) + 1
    if not best: return vw, vh, ""
    cw, ch, cx, cy = max(best, key=lambda k: (k[0] * k[1], best[k]))
    cw, ch = cw // 2 * 2, ch // 2 * 2
    if cw < 16 or ch < 16 or cw > vw or ch > vh: return vw, vh, ""
    if cw * ch >= vw * vh * 0.985: return vw, vh, ""          # nothing worth cutting
    if cw * ch < vw * vh * 0.25: return vw, vh, ""            # suspicious (a dark scene, not bars)
    # only act on a real band: a dark-styled clip whose edges merely read as black must stay untouched
    if (vw - cw) / vw < 0.06 and (vh - ch) / vh < 0.06: return vw, vh, ""
    return cw, ch, f"crop={cw}:{ch}:{cx}:{cy},"


def layout(vw, vh, fit, crop_pos, pre=""):
    """How the clip is placed on the 1080x1920 canvas -> (mode, filter chain, shown size, share cropped away)."""
    target, ratio = W / H, vw / vh
    fill = fit == "fill" or (fit == "auto" and abs(ratio - target) / target <= NEAR)
    if fill:  # scale up to cover the canvas, cut the overflow (crop_pos picks which part stays)
        sw = max(W, round(H * ratio / 2) * 2); sh = max(H, round(W / ratio / 2) * 2)
        x = round((sw - W) * (crop_pos if sw > W else 0.5)); y = round((sh - H) * (crop_pos if sh > H else 0.5))
        lost = round(1 - (W * H) / (sw * sh), 3)
        fc = (f"[0:v]{pre}scale={sw}:{sh}:flags=lanczos,crop={W}:{H}:{x}:{y},setsar=1,fps=30,format=yuv420p[out]")
        return "fill", fc, [W, H], lost
    # any other shape: the whole clip, centered on a blurred, darkened copy of itself (the platform-native look)
    if ratio > target: sw = W; sh = round(W / ratio / 2) * 2
    else: sh = H; sw = round(H * ratio / 2) * 2
    fc = (f"[0:v]{pre}split=2[a][b];"
          f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=42,eq=brightness=-0.14[bg];"
          f"[b]scale={sw}:{sh}:flags=lanczos,setsar=1[v];"
          f"[bg][v]overlay=(W-w)/2:(H-h)/2:format=auto,fps=30,format=yuv420p[out]")
    return "contain", fc, [sw, sh], 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--name")
    ap.add_argument("--fit", choices=["auto", "contain", "fill"], default="auto")
    ap.add_argument("--crop-pos", type=float, default=0.5)
    ap.add_argument("--hook"); ap.add_argument("--title"); ap.add_argument("--credit")  # kept for meta.json / old calls
    a = ap.parse_args()
    if a.src.endswith(".json"):
        d = json.loads(pathlib.Path(a.src).read_text(encoding="utf-8"))
        a.name = pathlib.Path(a.src).stem; a.hook = d.get("hook"); a.credit = d.get("credit")
        a.fit = d.get("fit") if d.get("fit") in ("auto", "contain", "fill") else "auto"
        a.crop_pos = min(1.0, max(0.0, float(d.get("crop_pos", 0.5))))
        got = [f for f in sorted((ROOT / "output" / "clips" / a.name).glob("source.*")) if f.suffix in VIDEO]
        a.src = str(got[0]) if got else d["source"]
    name = a.name or re.sub(r"[^a-z0-9]+", "-", (a.hook or pathlib.Path(a.src).stem).lower()).strip("-")[:50]
    out = ROOT / "output" / "clips" / name; out.mkdir(parents=True, exist_ok=True)
    src = fetch(a.src, out) if re.match(r"https?://", a.src) else pathlib.Path(a.src)
    vw, vh, dur, audio = probe(src)
    dur = min(dur, MAX_SECS)
    # a clip that is already about 9:16 is our target shape: never shrink it looking for bars
    cw, ch, pre = (vw, vh, "") if abs(vw / vh - W / H) / (W / H) <= NEAR else debar(src, vw, vh, dur)
    mode, fc, shown, lost = layout(cw, ch, a.fit, a.crop_pos, pre)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter_complex", fc, "-map", "[out]"]
    if audio: cmd += ["-map", "0:a:0", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high",
            "-movflags", "+faststart", str(out / "reel.mp4")]
    run(cmd)
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.3", "-i", str(out / "reel.mp4"), "-frames:v", "1", "-q:v", "2", str(out / "cover.jpg")])
    for i in range(5):  # check frames for the QA step (and for humans)
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{dur * (i + 0.5) / 5:.2f}", "-i", str(out / "reel.mp4"),
             "-frames:v", "1", "-vf", "scale=540:-2", str(out / f"check_{i + 1}.jpg")])
    for old in ("header.png", "header.html", "credit.png", "credit.html"):  # leftovers of the old framed look
        (out / old).unlink(missing_ok=True)
    (out / "meta.json").write_text(json.dumps({"src": a.src, "hook": a.hook, "credit": a.credit, "secs": round(dur, 2),
                                               "clip": [vw, vh], "bars_cut": None if (cw, ch) == (vw, vh) else [cw, ch],
                                               "fit": a.fit, "mode": mode, "crop_pos": a.crop_pos,
                                               "cropped": lost, "shown": shown}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    bars = "" if (cw, ch) == (vw, vh) else f" bars cut -> {cw}x{ch},"
    print(f"saved {out / 'reel.mp4'} ({mode}, clip {vw}x{vh},{bars} shown {shown[0]}x{shown[1]}, {dur:.1f}s)")


if __name__ == "__main__":
    main()
