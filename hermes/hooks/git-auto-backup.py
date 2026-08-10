#!/usr/bin/env python3
"""pre_tool_call: auto-create a backup branch/stash before an already-bypassed destructive git op.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/git-auto-backup.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

Unlike git-destructive-guard.py (which denies), this one wraps: it creates a safety net right
before allowing the op, and only runs once the main guard's bypass has already been granted
(HERMES_ALLOW_GIT_DESTRUCTIVE=1) -- if the bypass isn't set, git-destructive-guard.py already
blocked the command and this hook never sees it act on anything.

Triggers on:
  git reset --hard / git checkout -- .  -> branch hermes-backup-<unix_ts>
  git clean -fdx(X)                     -> git stash push -u -m 'hermes-pre-clean-<ts>'

Always allows -- this hook never blocks; a failed backup is a loud stderr warning, not a denial
(a machine without git available for the backup step must not be locked out of legitimate work).
Silent (and a no-op) outside a git repo.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    bypass,
    log,
    read_event,
    terminal_command,
)

RESET_HARD_RE = re.compile(r"\bgit\s+reset\s+--hard\b", re.IGNORECASE)
CLEAN_FDX_RE = re.compile(r"\bgit\s+clean\s+-[fdxX]{2,}", re.IGNORECASE)
CHECKOUT_DOT_RE = re.compile(r"\bgit\s+checkout\s+--\s+\.", re.IGNORECASE)


def in_git_repo(cwd: str | None) -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, cwd=cwd, timeout=5,
        )
        return r.returncode == 0 and r.stdout.strip() == "true"
    except (subprocess.SubprocessError, OSError):
        return False


def make_branch_backup(cwd: str | None, ts: int) -> str | None:
    name = f"hermes-backup-{ts}"
    try:
        r = subprocess.run(["git", "branch", name], capture_output=True, text=True, cwd=cwd, timeout=5)
        if r.returncode == 0:
            return name
    except (subprocess.SubprocessError, OSError):
        pass
    return None


def make_stash_backup(cwd: str | None, ts: int) -> str | None:
    msg = f"hermes-pre-clean-{ts}"
    try:
        r = subprocess.run(
            ["git", "stash", "push", "-u", "-m", msg],
            capture_output=True, text=True, cwd=cwd, timeout=10,
        )
        if r.returncode == 0 and "No local changes" not in r.stdout:
            return msg
    except (subprocess.SubprocessError, OSError):
        pass
    return None


def main() -> None:
    event = read_event()
    if event.get("tool_name") != "terminal":
        allow()

    cmd = terminal_command(event.get("tool_input", {}))
    if not cmd:
        allow()

    needs_branch = bool(RESET_HARD_RE.search(cmd) or CHECKOUT_DOT_RE.search(cmd))
    needs_stash = bool(CLEAN_FDX_RE.search(cmd))
    if not (needs_branch or needs_stash):
        allow()

    # Safety net only -- if the main gate's bypass isn't set, it already blocked this command.
    if not bypass("git-destructive", cmd, env_name="HERMES_ALLOW_GIT_DESTRUCTIVE"):
        allow()

    cwd = event.get("cwd") or os.getcwd()
    if not in_git_repo(cwd):
        allow()

    ts = int(time.time())

    if needs_branch:
        branch = make_branch_backup(cwd, ts)
        if branch:
            log("INFO", "git_auto_backup", "branch_created", branch, cmd)
            sys.stderr.write(
                f"[git-auto-backup] Created safety branch {branch} before destructive op.\n"
                f"Recover: git checkout {branch}\n"
            )
        else:
            log("WARN", "git_auto_backup", "branch_failed", "", cmd)
            sys.stderr.write(
                "[git-auto-backup] WARNING: failed to create safety branch. "
                "Consider aborting and backing up manually.\n"
            )

    if needs_stash:
        stash = make_stash_backup(cwd, ts)
        if stash:
            log("INFO", "git_auto_backup", "stash_created", stash, cmd)
            sys.stderr.write(
                f"[git-auto-backup] Stashed working tree as '{stash}' before clean.\n"
                "Recover: git stash list && git stash pop stash@{N}\n"
            )
        else:
            log("WARN", "git_auto_backup", "stash_failed_or_empty", "", cmd)

    allow()


if __name__ == "__main__":
    main()
