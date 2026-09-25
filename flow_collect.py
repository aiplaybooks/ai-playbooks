"""Collect images/videos made with the "Flow Automation" Chrome extension (semi-automatic Flow: we write the prompt
file, the owner imports it in the extension's side panel on the test profile and presses Start).

The extension saves into Downloads/veo-folder-N/ (one folder per Flow project). This copies every file we have not
collected yet into output/flow/<date>/ and appends it to output/flow/collected.json.

Usage:
    python flow_collect.py            copy new files once
    python flow_collect.py --watch    keep watching (every 15 s) until Ctrl+C
    python flow_collect.py --list     show what was collected

Prompt files for the extension: plain .txt, one prompt per paragraph (a blank line between prompts). Keep them in
Downloads/flow-prompts/ so the file dialog finds them quickly.
"""
import sys, json, time, shutil, hashlib, pathlib, argparse
from datetime import datetime

ROOT = pathlib.Path(__file__).parent.resolve()
DOWNLOADS = pathlib.Path.home() / "Downloads"
OUT = ROOT / "output" / "flow"
STATE = OUT / "collected.json"
MEDIA = {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".mov"}


def load():
    try: return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError): return []


def digest(f):
    h = hashlib.sha1()
    with f.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()


def collect():
    done = load(); seen = {d["sha1"] for d in done}; new = []
    for f in sorted(DOWNLOADS.glob("veo-folder*/**/*")):
        if not f.is_file() or f.suffix.lower() not in MEDIA: continue
        if time.time() - f.stat().st_mtime < 5: continue  # still being written by Chrome
        sha = digest(f)
        if sha in seen: continue
        day = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
        dest = OUT / day / f"{f.parent.name}_{f.name}"
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, dest)
        entry = {"sha1": sha, "source": str(f), "file": dest.relative_to(ROOT).as_posix(),
                 "kind": "video" if f.suffix.lower() in {".mp4", ".webm", ".mov"} else "image",
                 "collected": datetime.now().astimezone().isoformat(timespec="seconds")}
        done.append(entry); seen.add(sha); new.append(entry)
    if new:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(done, indent=1, ensure_ascii=False), encoding="utf-8")
    return new


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(); ap.add_argument("--watch", action="store_true"); ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for d in load(): print(d["collected"][:16], d["kind"], d["file"])
        return
    while True:
        for e in collect(): print(f"{e['kind']}: {e['file']}", flush=True)
        if not a.watch: break
        time.sleep(15)


if __name__ == "__main__":
    main()
