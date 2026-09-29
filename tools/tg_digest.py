"""Session-start digest of the owner's Telegram messages (owner, 2026-09-29: "analyse the Telegram bot every day when
I open this session, I'm telling it things").

Claude Code runs this from the SessionStart hook in .claude/settings.json; whatever it prints lands in the session's
context. It prints every message in runs/telegram/inbox.jsonl (written by telegram_bot.py) since the last digest,
then moves the mark, so each message is shown once. `--all` shows the last 3 days again without moving the mark.
"""
import sys, json, pathlib
from datetime import datetime, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent
TG = ROOT / "runs" / "telegram"
INBOX, MARK, HISTORY = TG / "inbox.jsonl", TG / "digest_mark.txt", TG / "history.json"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    show_all = "--all" in sys.argv
    mark = "" if not MARK.exists() else MARK.read_text(encoding="utf-8").strip()
    if show_all: mark = (datetime.now().astimezone() - timedelta(days=3)).isoformat(timespec="seconds")
    rows = []
    if INBOX.exists():
        for line in INBOX.read_text(encoding="utf-8").splitlines():
            try: r = json.loads(line)
            except ValueError: continue
            if r.get("at", "") > mark: rows.append(r)
    old = []
    if not MARK.exists() and HISTORY.exists():  # first run: the undated chat history from before the inbox existed
        try: old = json.loads(HISTORY.read_text(encoding="utf-8"))
        except ValueError: old = []
    backlog = ROOT / "strategy" / "backlog.md"
    todo, cur = [], None  # open items with their indented continuation lines
    for l in (backlog.read_text(encoding="utf-8").splitlines() if backlog.exists() else []):
        if l.startswith("- ["): cur = l if l.startswith("- [ ]") else None; todo += [l] if cur else []
        elif cur and l.startswith("  "): todo[-1] += " " + l.strip()
    if todo:
        print("## Open strategy backlog (strategy/backlog.md): production changes the daily strategy director wants.")
        print("## Build them this session (autonomously), mark them done with the commit hash.")
        for l in todo: print(l)
    if not rows and not old:
        print("Telegram: no new messages from the owner since the last session."); return
    print("## Owner's Telegram messages since the last session (analyse them FIRST: instructions, wishes, complaints ->")
    print("## act on them, update memory/CLAUDE.md when they set a rule; they went to the Studio's chat bot, not to you)")
    for r in old:
        print(f"- [before inbox, undated] {r.get('who')}: {r.get('text', '')[:1500]}")
    for r in rows:
        who = "OWNER" + (" (voice)" if r.get("voice") else "") if r.get("who") == "owner" else "bot"
        print(f"- {r['at'][:16].replace('T', ' ')} {who}: {r.get('text', '')[:1500]}")
    if rows and not show_all:
        TG.mkdir(parents=True, exist_ok=True); MARK.write_text(rows[-1]["at"], encoding="utf-8")
    elif old and not show_all:
        TG.mkdir(parents=True, exist_ok=True); MARK.write_text(datetime.now().astimezone().isoformat(timespec="seconds"), encoding="utf-8")


if __name__ == "__main__":
    main()
