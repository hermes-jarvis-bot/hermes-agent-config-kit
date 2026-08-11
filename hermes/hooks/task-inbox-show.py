#!/usr/bin/env python3
"""pre_llm_call (is_first_turn only): surface pending tasks from any tracker inbox.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/task-inbox-show.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

Some teams run a small script on the operator's machine that polls their task tracker (Vikunja,
Linear, Jira, GitHub Projects, ...) for tasks assigned to the agent-identity and writes
snapshots into `.hermes/task-inbox/<id>.json` (or a sibling name below). This hook reads that
directory at the start of a session and injects a compact summary via `pre_llm_call`'s genuine
`{"context": ...}` channel (same mechanism as session-handoff-check.py) so the agent can pick a
task up without the human pasting one.

The hook is provider-agnostic. It does not know or care which tracker wrote the snapshots; it
only needs each file to be JSON with the fields shown in `INBOX_DIR_NAMES`'s sibling docstring
below. Files older than any you want to keep can be deleted by the poller -- this hook does not
delete or modify anything.

Ported unchanged: the inbox-discovery walk, the snapshot schema, the priority-sort/formatting
logic. Adapted: looks under BOTH `.hermes/<name>/` (Hermes-native default) and `.claude/<name>/`
(cross-harness -- a poller that already writes under Claude Code's convention needs no
migration) in cwd and up to 3 parent directories; same is_first_turn substitution as
session-handoff-check.py for Hermes's lack of a SessionStart-equivalent whose output reaches the
model.

Expected snapshot format (any extra fields are ignored):

    {
      "task_id": 1247,            // int or string
      "title": "Fix auth race",   // short human title
      "priority": 3,              // 0-5, higher = more urgent
      "labels": ["ai-ready"],     // optional list
      "link": "https://..."       // optional URL
    }
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import emit_context, read_event  # noqa: E402

INBOX_DIR_NAMES = ("task-inbox", "vikunja-inbox", "linear-inbox", "jira-inbox", "gh-inbox", "inbox")
HARNESS_DIRS = (".hermes", ".claude")


def _find_inbox(cwd: Path) -> Path | None:
    """Look for `.hermes/<inbox>/` or `.claude/<inbox>/` in cwd and up to 3 parents."""
    for candidate in (cwd, *list(cwd.parents)[:3]):
        for harness_dir in HARNESS_DIRS:
            base = candidate / harness_dir
            if not base.is_dir():
                continue
            for name in INBOX_DIR_NAMES:
                p = base / name
                if p.is_dir() and any(p.glob("*.json")):
                    return p
    return None


def _priority_label(p: int) -> str:
    if p <= 0:
        return "P0"
    return f"P{min(p, 5)}"


def build_report(cwd: Path) -> str | None:
    inbox = _find_inbox(cwd)
    if inbox is None:
        return None

    files = sorted(inbox.glob("*.json"))
    if not files:
        return None

    entries = []
    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        tid = data.get("task_id", "?")
        title = (data.get("title") or "")[:70]
        labels = data.get("labels") or []
        try:
            priority = int(data.get("priority") or 0)
        except (TypeError, ValueError):
            priority = 0
        entries.append((priority, tid, title, labels))

    if not entries:
        return None

    entries.sort(key=lambda e: (-e[0], str(e[1])))

    kind = inbox.name
    lines = [f"[{kind}] {len(entries)} task(s) pending:"]
    for priority, tid, title, labels in entries[:10]:
        label_part = f" [{' '.join(labels)}]" if labels else ""
        lines.append(f"  #{tid} {_priority_label(priority)}{label_part} {title}")
    if len(entries) > 10:
        lines.append(f"  ... and {len(entries) - 10} more")
    lines.append("")
    lines.append("  Your poller script populates this inbox; claim a task in the tracker UI "
                  "or via your team's bridge before starting work.")
    return "\n".join(lines)


def main() -> int:
    event = read_event()
    if event.get("hook_event_name") != "pre_llm_call":
        return 0
    extra = event.get("extra", {}) or {}
    if not extra.get("is_first_turn"):
        return 0

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    report = build_report(cwd)
    if report:
        emit_context(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
