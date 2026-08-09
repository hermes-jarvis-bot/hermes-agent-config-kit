#!/usr/bin/env python3
"""pre_llm_call (is_first_turn only): check for handoffs from previous sessions.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's hooks/session-handoff-check.py
(reimplemented from the upstream SessionStart hook, see mappings/reviewed-hooks.yaml).

Hermes has no SessionStart-equivalent whose output reaches the model: `on_session_start`'s
return value is discarded by its only caller, same pattern as `post_tool_call` (see
verify-deleted-guard.py/over-engineering-advisor.py). The correct working substitute, verified
against the live agent/turn_context.py source, is `pre_llm_call` filtered to
`extra.is_first_turn` — its `{"context": "..."}` return IS appended to the first user message
(turn_context.py:1059-1109), so this genuinely reaches the model, unlike the two previous
post_tool_call ports.

Adaptations from upstream:
  - No `source` field (startup/resume/clear/compact) exists on `pre_llm_call` — Hermes has no
    exposed compaction-boundary hook/flag at all (verified: not in hermes_cli/plugins.py's
    VALID_HOOKS). # simplification: every is_first_turn=True is treated as a fresh start; the
    upstream after-compact branch (show 1 project instead of 3, different instruction wording)
    is dropped rather than guessed at. If Hermes ever exposes a compaction signal, revisit.
  - No fixed handoff-directory convention exists in this adapter (the already-ported
    `session-handoff` skill deliberately "removes harness-specific storage assumptions" rather
    than prescribing one) — this hook defines a Hermes-native default (`.hermes/handoffs/` in
    the project, `~/.hermes/handoffs/` globally), overridable via HERMES_HANDOFF_DIR.
  - Dropped the upstream PreCompact-marker surfacing and other-hook marker resets
    (`.stop-phrase-guard-fired`, `.stop-budget-*`) — those reference sibling upstream hooks this
    adapter does not port. Still resets `.hermes/.handoff-reminded` and touches
    `.hermes/.session-start` — session-handoff-reminder.py's own state, needed for it to work at
    all (same feature, split across two files, matching upstream's own design).
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import filename_timestamp, read_event  # noqa: E402

MAX_PROJECTS = 3
MAX_AGE_HOURS = 168  # 7 days
HANDOFF_DIR_ENV = "HERMES_HANDOFF_DIR"


def local_handoffs_dir(cwd: Path) -> Path:
    import os

    override = os.environ.get(HANDOFF_DIR_ENV, "").strip()
    if override:
        return (cwd / override).resolve()
    return (cwd / ".hermes" / "handoffs").resolve()


def scan_store(root: Path, store_label: str, now: float) -> list[dict]:
    found: list[dict] = []
    if not root.exists():
        return found
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if p.name.startswith("INDEX") or "archive" in rel.parts:
            continue
        ts = filename_timestamp(p)
        if ts is None:
            ts = p.stat().st_mtime
        if (now - ts) / 3600 > MAX_AGE_HOURS:
            continue
        project = rel.parts[0] if len(rel.parts) > 1 else "(no-project)"
        found.append({"ts": ts, "path": p, "project": project, "store": store_label})
    return found


def emit_context(text: str) -> None:
    print(json.dumps({"context": text}, ensure_ascii=False))
    sys.exit(0)


def main() -> None:
    event = read_event()
    if event.get("hook_event_name") != "pre_llm_call":
        sys.exit(0)
    extra = event.get("extra", {}) or {}
    if not extra.get("is_first_turn"):
        sys.exit(0)

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    hermes_dir = cwd / ".hermes"
    if hermes_dir.exists():
        reminded = hermes_dir / ".handoff-reminded"
        if reminded.exists():
            try:
                reminded.unlink()
            except OSError:
                pass
    else:
        hermes_dir.mkdir(parents=True, exist_ok=True)
    (hermes_dir / ".session-start").touch()

    now = time.time()
    found: list[dict] = []
    local_store = local_handoffs_dir(cwd)
    found.extend(scan_store(local_store, "project", now))
    global_store = (Path.home() / ".hermes" / "handoffs").resolve()
    if global_store != local_store:
        found.extend(scan_store(global_store, "global", now))

    if not found:
        sys.exit(0)

    groups: dict[str, list[dict]] = {}
    for h in found:
        groups.setdefault(h["project"], []).append(h)
    for items in groups.values():
        items.sort(key=lambda h: h["ts"], reverse=True)
    ordered = sorted(groups.items(), key=lambda kv: kv[1][0]["ts"], reverse=True)
    shown = ordered[:MAX_PROJECTS]
    rest = ordered[MAX_PROJECTS:]

    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(
        f"SESSION HANDOFF(S) - {len(found)} found across "
        f"{len(groups)} project(s), showing latest per project"
    )
    lines.append("=" * 60)

    for project, items in shown:
        top = items[0]
        ts_str = datetime.fromtimestamp(top["ts"]).strftime("%Y-%m-%d %H:%M")
        extra_older = f", {len(items) - 1} older" if len(items) > 1 else ""
        lines.append(
            f"\n--- [{project}] {ts_str} - {top['path'].name} "
            f"({top['store']} store{extra_older}) ---"
        )
        lines.append(top["path"].read_text(encoding="utf-8", errors="replace"))

    if rest:
        lines.append("")
        lines.append("Other projects with recent handoffs (see INDEX.md):")
        for project, items in rest:
            ts_str = datetime.fromtimestamp(items[0]["ts"]).strftime("%Y-%m-%d %H:%M")
            lines.append(f"  - {project}: {len(items)} handoff(s), latest {ts_str}")

    lines.append("=" * 60)
    lines.append("")
    lines.append(
        "INSTRUCTION: List the handoff(s) briefly to the user (project, timestamp, session "
        "ID, topic). Ask if they want to continue one of them or start fresh."
    )
    lines.append("")

    emit_context("\n".join(lines))


if __name__ == "__main__":
    main()
