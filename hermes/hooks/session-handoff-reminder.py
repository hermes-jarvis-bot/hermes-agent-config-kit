#!/usr/bin/env python3
"""pre_verify + on_session_end: remind to write a handoff when closing a long session.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's
hooks/session-handoff-reminder.py (reimplemented from the upstream Stop hook, see
mappings/reviewed-hooks.yaml).

Hermes has no Stop-equivalent that fires on every turn-end attempt regardless of what happened
that turn. The two closest events, verified against the live agent/conversation_loop.py and
agent/turn_finalizer.py source, have complementary and incomplete coverage on their own:

  - `pre_verify`: a genuine live nudge (its `{"action": "continue", "message": "..."}` reaches
    the model via get_pre_verify_continue_message() -> agent/conversation_loop.py:7116-7147,
    same mechanism that produced this exact "Stop hook feedback" text live in this operator's
    own session). BUT it is only checked when `if _edited and has_hook("pre_verify") and
    _attempt < max_verify_nudges()` (conversation_loop.py:7109) -- `_edited` means the agent
    mutated a file THIS turn, and `max_verify_nudges()` defaults to 3 nudges for the WHOLE
    session, shared with any other pre_verify consumer. A read-only/analysis session never
    triggers it at all, no matter how long it runs.
  - `on_session_end`: fires "at the very end of every run_conversation call" -- i.e. every
    turn, matching upstream's actual trigger frequency far better -- but its return value is
    discarded by its only caller (turn_finalizer.py, same fire-and-forget pattern as
    post_tool_call), so it can only log, never nudge.

Operator-approved design (2026-08-09): register on BOTH. `on_session_end` is the reliable
audit-log fallback that covers every long session, coding or not. `pre_verify` is a bonus live
nudge that actually reaches the model on the turns where the narrow gate holds. Both share the
same underlying age/freshness check and the same `.hermes/.handoff-reminded` marker, so whichever
fires first in a given turn suppresses the other for the rest of the session.

Other adaptations:
  - No `.claude/HANDOFF.md` legacy single-file format -- this is a fresh Hermes-native
    adaptation with no legacy baggage to carry. # simplification: only the
    `.hermes/handoffs/*.md` format is checked.
  - Tunables (SESSION_MIN_MINUTES, HANDOFF_STALE_MINUTES) carried over unchanged from upstream.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import filename_timestamp, log, read_event  # noqa: E402

SESSION_MIN_MINUTES = 15
HANDOFF_STALE_MINUTES = 30
HANDOFF_DIR_ENV = "HERMES_HANDOFF_DIR"


def handoffs_dir(cwd: Path) -> Path:
    import os

    override = os.environ.get(HANDOFF_DIR_ENV, "").strip()
    if override:
        return (cwd / override).resolve()
    return (cwd / ".hermes" / "handoffs").resolve()


def reminder_text(age_minutes: int) -> str:
    return (
        f"This session has been active for ~{age_minutes} minutes and no fresh "
        f"handoff exists. Before ending, please write a handoff file in "
        f".hermes/handoffs/<project-slug>/ (or the directory named by "
        f"{HANDOFF_DIR_ENV} if set), following the format in the session-handoff skill/rule. "
        f"<project-slug> = kebab-case name of the project worked on (reuse an existing "
        f"subdirectory name if one fits; create it if not). File name: "
        f"YYYY-MM-DD_HH-MM_<session-short-id>.md. Keep it under 1500 tokens. Must include: "
        f"goal, what was done, what did NOT work (with reasons), current state, key "
        f"decisions, single next step, and a Closure Audit (primary request status; "
        f"acceptance/checklist verified; related/scope-adjacent tasks checked; unfinished "
        f"related tasks; why not continuing now). Append one line to the handoffs INDEX.md "
        f"(format: date time | session-id | project | summary | status). After writing, you "
        f"may end the session normally."
    )


def main() -> None:
    event = read_event()
    hook_event = event.get("hook_event_name")
    if hook_event not in ("pre_verify", "on_session_end"):
        sys.exit(0)

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    hermes_dir = cwd / ".hermes"
    if not hermes_dir.exists():
        sys.exit(0)  # not a Hermes-managed project

    reminder_marker = hermes_dir / ".handoff-reminded"
    session_marker = hermes_dir / ".session-start"

    if reminder_marker.exists():
        sys.exit(0)  # already reminded this session

    if not session_marker.exists():
        session_marker.touch()
        sys.exit(0)  # no baseline yet -- age is ~0, same as upstream's first-Stop behavior

    age = (time.time() - session_marker.stat().st_mtime) / 60
    if age < SESSION_MIN_MINUTES:
        sys.exit(0)

    fresh = False
    hdir = handoffs_dir(cwd)
    if hdir.exists():
        for p in hdir.rglob("*.md"):
            if p.name.startswith("INDEX"):
                continue
            ts = filename_timestamp(p)
            if ts is None:
                ts = p.stat().st_mtime
            if (time.time() - ts) / 60 < HANDOFF_STALE_MINUTES:
                fresh = True
                break
    if fresh:
        sys.exit(0)

    reminder_marker.touch()
    text = reminder_text(int(age))
    log("WARN", "session_handoff_reminder", "reminded", hook_event, f"age={int(age)}min")

    if hook_event == "pre_verify":
        print(json.dumps({"action": "continue", "message": text}, ensure_ascii=False))
    else:
        # on_session_end: return value is discarded by Hermes (see module docstring) --
        # audit-log-only. stderr kept for potential visibility via Hermes's own logger.
        sys.stderr.write(f"[session_handoff_reminder] {text}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
