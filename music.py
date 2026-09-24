"""Procedural lo-fi background track (original, royalty-free). Usage: music.py out.wav seconds"""
import sys, wave, numpy as np

out, secs = sys.argv[1], float(sys.argv[2])
SR = 44100; N = int(SR * secs); t = np.arange(N) / SR
BPM = 88; beat = 60 / BPM; bar = beat * 4
mix = np.zeros(N)

def note(f): return 440 * 2 ** ((f - 69) / 12)
# Am9 - Fmaj7 - Cmaj7 - G6 voicings (midi)
chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 59, 64, 67], [55, 59, 62, 64, 69]]
bass = [45, 41, 48, 43]

def env(n, a, r):
    e = np.ones(n); a = min(int(a * SR), n); r = min(int(r * SR), n)  # last bar can be shorter than the envelope
    e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r); return e

i = 0; start = 0.0
while start < secs:
    s0 = int(start * SR); n = min(int(bar * SR), N - s0)
    if n <= 0: break
    tt = np.arange(n) / SR; ch = chords[i % 4]
    pad = sum(np.sin(2*np.pi*note(m)*tt) + .3*np.sin(2*np.pi*note(m)*2.003*tt) for m in ch) / len(ch)
    pad *= env(n, .5, .6) * (1 + .15*np.sin(2*np.pi*.5*tt))
    b = np.sin(2*np.pi*note(bass[i % 4] - 12)*tt) * env(n, .02, .4) * np.exp(-tt*.6)
    mix[s0:s0+n] += .22*pad + .35*b
    # soft keys arpeggio on 8th notes
    for k in range(8):
        a0 = s0 + int(k * beat/2 * SR); m = ch[(k*2) % len(ch)] + 12
        ln = min(int(beat*SR), N - a0)
        if ln <= 0: continue
        at = np.arange(ln)/SR
        mix[a0:a0+ln] += .07*np.sin(2*np.pi*note(m)*at)*np.exp(-at*5)
    i += 1; start += bar

rng = np.random.default_rng(3)
nb = int(secs / beat)
for k in range(nb):
    s0 = int(k*beat*SR); ln = min(int(.25*SR), N-s0)
    if ln <= 0: continue
    kt = np.arange(ln)/SR
    if k % 2 == 0:  # kick
        mix[s0:s0+ln] += .5*np.sin(2*np.pi*(50+80*np.exp(-kt*30))*kt)*np.exp(-kt*12)
    else:  # soft snare/rim
        mix[s0:s0+ln] += .12*rng.standard_normal(ln)*np.exp(-kt*25)
    h0 = s0 + int(beat/2*SR); hl = min(int(.05*SR), N-h0)
    if hl > 0: mix[h0:h0+hl] += .05*rng.standard_normal(hl)*np.exp(-np.arange(hl)/SR*80)

# gentle lowpass + fades
k = 12; mix = np.convolve(mix, np.ones(k)/k, mode="same")
fi, fo = int(1.0*SR), int(2.5*SR)
mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
mix = mix / np.max(np.abs(mix)) * 0.5
st = np.stack([mix, np.roll(mix, 220)], 1)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype(np.int16).tobytes())
print("music", out, secs)
