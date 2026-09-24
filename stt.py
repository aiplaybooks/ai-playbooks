"""Speech to text for the Telegram bot (and the Studio mic later): faster-whisper, run with the Pinokio TTS env's
Python (it has faster_whisper + CUDA torch; used read-only, the model is cached in this project's .cache/).

Usage:
    <pinokio python> stt.py <audio file>        prints the transcript (UTF-8) on stdout
The owner speaks Turkish (commands) but may say English words; language is auto-detected with a Turkish hint.
"""
import sys, os, pathlib

ROOT = pathlib.Path(__file__).parent.resolve()
os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "hf"))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    from faster_whisper import WhisperModel
    try:
        model = WhisperModel("medium", device="cuda", compute_type="float16")
    except Exception:  # noqa: BLE001 - no GPU memory free (Flux running ...): smaller model on the CPU
        model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, info = model.transcribe(sys.argv[1], beam_size=5, vad_filter=True,
                                  language="tr" if len(sys.argv) < 3 else sys.argv[2],
                                  initial_prompt="AI Playbooks Studio: tara, adaylar, seç, yayınla, revize et, reddet, durum.")
    print(" ".join(s.text.strip() for s in segs).strip())


if __name__ == "__main__":
    main()
