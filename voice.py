"""Per-slide voice-over with Kokoro-82M (local, Apache-2.0).

Runs inside the Pinokio Ultimate-TTS-Studio env (it already has kokoro + CUDA torch); reel.py calls it
as a subprocess, so nothing needs to be installed into the system Python.

Usage:
    <kokoro python> voice.py content.json outdir [--voice af_sarah] [--speed 1.1]

Reads `voiceover` from each slide (slides without one stay silent).
Writes outdir/vo_NN.wav (24 kHz mono) and outdir/voice.json:
    {"sr": 24000, "voice": "...", "slides": [{"file": "vo_01.wav", "dur": 3.2,
                                               "words": [["Seven", 0.12, 0.41], ...]} | null, ...]}
Word times come from Kokoro's own token timestamps (seconds from the start of that slide's clip).
"""
import sys, json, re, pathlib, argparse
import numpy as np, soundfile as sf
from kokoro import KPipeline

SR = 24000
PUNCT = re.compile(r"^[^\w]+$")


def synth(pipe, text, voice, speed):
    chunks, words, off = [], [], 0.0
    for r in pipe(text, voice=voice, speed=speed):
        if r.audio is None: continue
        for tk in r.tokens or []:
            if PUNCT.match(tk.text):  # glue punctuation onto the previous word
                if words: words[-1][0] += tk.text
                continue
            if tk.start_ts is None or tk.end_ts is None:
                if words: words[-1][0] += " " + tk.text
                continue
            words.append([tk.text, round(off + tk.start_ts, 3), round(off + tk.end_ts, 3)])
        a = r.audio.numpy(); chunks.append(a); off += len(a) / SR
    audio = np.concatenate(chunks)
    if words:  # Kokoro pads ~0.3s of silence at the start and ~0.25s at the end; reel.py adds its own timing
        s0 = max(0.0, words[0][1] - 0.05); s1 = min(len(audio) / SR, words[-1][2] + 0.15)
        audio = audio[int(s0 * SR):int(s1 * SR)]
        words = [[w, round(a - s0, 3), round(b - s0, 3)] for w, a, b in words]
    return audio, words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content"); ap.add_argument("outdir")
    ap.add_argument("--voice"); ap.add_argument("--speed", type=float)
    a = ap.parse_args()
    data = json.loads(pathlib.Path(a.content).read_text(encoding="utf-8"))
    voice = a.voice or data.get("voice", "af_sarah")
    speed = a.speed or data.get("voice_speed", 1.1)
    out = pathlib.Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    pipe = KPipeline(lang_code=voice[0], repo_id="hexgrad/Kokoro-82M")
    res = []
    for n, s in enumerate(data["slides"], 1):
        text = s.get("voiceover", "").strip()
        if not text:
            res.append(None); continue
        audio, words = synth(pipe, text, voice, speed)
        f = f"vo_{n:02d}.wav"; sf.write(out / f, audio, SR)
        res.append({"file": f, "dur": round(len(audio) / SR, 3), "words": words})
        print(f"slide {n}: {len(audio) / SR:.2f}s  {text}")
    (out / "voice.json").write_text(json.dumps({"sr": SR, "voice": voice, "slides": res}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
