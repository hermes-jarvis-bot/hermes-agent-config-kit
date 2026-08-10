#!/usr/bin/env python3
"""on_session_end: delete old auto-backup branches/stashes that git-auto-backup.py created.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/backup-retention-cleanup.py, reimplemented for Hermes
Agent's shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the
upstream Claude-Code version this was read from).

Companion to git-auto-backup.py: matches the exact `hermes-backup-<ts>` branch prefix and
`hermes-pre-clean-<ts>` stash-message prefix that hook creates. Fires on every turn
(on_session_end has no `is_first_turn` filter, unlike pre_llm_call) -- cheap and idempotent, so
running it more often than strictly needed is harmless. Hermes discards this event's return
value (same as post_tool_call), which is fine here: the hook is pure side effect, no decision to
surface. Default retention: 14 days. Silent no-op outside a git repo, and silent when nothing is
old enough to remove.
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import log, read_event  # noqa: E402

RETENTION_DAYS = 14
RETENTION_SECONDS = RETENTION_DAYS * 86400

BACKUP_BRANCH_RE = re.compile(r"^\s*(?:\*\s+)?(hermes-backup-(\d+))\s*$", re.MULTILINE)
BACKUP_STASH_RE = re.compile(r"^(stash@\{\d+\}):.*hermes-pre-clean-(\d+)", re.MULTILINE)


def in_git_repo(cwd: str) -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, cwd=cwd, timeout=5,
        )
        return r.returncode == 0 and r.stdout.strip() == "true"
    except (subprocess.SubprocessError, OSError):
        return False


def list_local_branches(cwd: str) -> list[tuple[str, int]]:
    try:
        r = subprocess.run(
            ["git", "branch", "--list", "hermes-backup-*"],
            capture_output=True, text=True, cwd=cwd, timeout=5,
        )
        if r.returncode != 0:
            return []
        out: list[tuple[str, int]] = []
        for m in BACKUP_BRANCH_RE.finditer(r.stdout):
            try:
                out.append((m.group(1), int(m.group(2))))
            except ValueError:
                continue
        return out
    except (subprocess.SubprocessError, OSError):
        return []


def list_stashes(cwd: str) -> list[tuple[str, int]]:
    try:
        r = subprocess.run(["git", "stash", "list"], capture_output=True, text=True, cwd=cwd, timeout=5)
        if r.returncode != 0:
            return []
        out: list[tuple[str, int]] = []
        for m in BACKUP_STASH_RE.finditer(r.stdout):
            try:
                out.append((m.group(1), int(m.group(2))))
            except ValueError:
                continue
        return out
    except (subprocess.SubprocessError, OSError):
        return []


def delete_branch(cwd: str, name: str) -> bool:
    try:
        r = subprocess.run(["git", "branch", "-D", name], capture_output=True, text=True, cwd=cwd, timeout=5)
        return r.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False


def drop_stash(cwd: str, ref: str) -> bool:
    try:
        r = subprocess.run(["git", "stash", "drop", ref], capture_output=True, text=True, cwd=cwd, timeout=5)
        return r.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False


def main() -> None:
    event = read_event()
    cwd = event.get("cwd") or "."
    if not in_git_repo(cwd):
        return

    now = int(time.time())
    deleted_branches: list[str] = []
    dropped_stashes: list[str] = []

    for name, ts in list_local_branches(cwd):
        if now - ts > RETENTION_SECONDS and delete_branch(cwd, name):
            deleted_branches.append(name)
            log("INFO", "backup_retention_cleanup", "branch_deleted", name, cwd)

    # Descending ref order: dropping stash@{0} shifts stash@{1} to {0}.
    for ref, ts in sorted(list_stashes(cwd), key=lambda x: x[0], reverse=True):
        if now - ts > RETENTION_SECONDS and drop_stash(cwd, ref):
            dropped_stashes.append(ref)
            log("INFO", "backup_retention_cleanup", "stash_dropped", ref, cwd)

    if deleted_branches or dropped_stashes:
        msg = []
        if deleted_branches:
            msg.append(f"{len(deleted_branches)} old hermes-backup branch(es)")
        if dropped_stashes:
            msg.append(f"{len(dropped_stashes)} old hermes-pre-clean stash(es)")
        sys.stderr.write(
            "[backup-retention-cleanup] Retention: removed " + ", ".join(msg)
            + f" (older than {RETENTION_DAYS} days)\n"
        )


if __name__ == "__main__":
    main()
