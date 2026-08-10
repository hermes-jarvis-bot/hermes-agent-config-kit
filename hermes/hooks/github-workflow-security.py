#!/usr/bin/env python3
"""pre_tool_call: GitHub Actions workflow-file security reminder.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/github-workflow-security.py, reimplemented for Hermes
Agent's shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the
upstream Claude-Code version this was read from).

Triggers on write_file/patch of files under .github/workflows/*.yml(.yaml) and prints a security
checklist about command injection from untrusted GitHub event inputs (issue titles, PR bodies,
head_ref, commit messages, etc). Extracted from anthropics/claude-plugins-official
security-guidance plugin's `github_actions_workflow` rule (per upstream's own docstring); the
rest of that plugin's patterns are deliberately not included, same reasoning upstream gives:
this adapter's other guards already cover secrets/destructive/injection, and a generic
exec-call pattern would false-positive on JS/TS regex objects' own exec method.

Behavior:
- Blocks the first matching edit per (file, session) so the reminder is forced into context.
- Subsequent edits of the same file in the same session are advisory only (stderr) -- do not
  block. Disable with HERMES_ALLOW_GH_WORKFLOW_SECURITY=1 (upstream's env-var-as-toggle became a
  bypass name to match this adapter's other guards' convention, rather than a bespoke
  ENABLE_*=0 flag).

Adaptations from upstream: `Write`/`Edit`/`MultiEdit` -> Hermes's `write_file`/`patch` (there is
no separate MultiEdit tool). Per-session "already shown" state moves from a flat
`~/.claude/logs/github_workflow_warnings_<session>.json` file to
`.hermes/sessions/<session_id>/github-workflow-warnings.json`, matching this adapter's
established session-scoped-state convention (see transfer-contract-guard.py's docstring for why
project-scoped-not-session-scoped state is a real bug class this adapter fixes on sight).
"""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    block,
    bypass_env,
    event_session_id,
    file_path,
    read_event,
)

REMINDER = """GitHub Actions workflow security checklist

You are editing a GitHub Actions workflow file. Untrusted GitHub event
inputs can lead to command injection when interpolated directly into
run: blocks. Before merging this edit, verify:

1. NO direct ${{ ... }} interpolation of attacker-controllable inputs
   inside `run:` blocks. Examples of attacker-controllable inputs:
     - github.event.issue.title / .body
     - github.event.pull_request.title / .body
     - github.event.comment.body
     - github.event.review.body / .review_comment.body
     - github.event.pages.*.page_name
     - github.event.commits.*.message
     - github.event.head_commit.message
     - github.event.head_commit.author.name / .author.email
     - github.event.commits.*.author.name / .author.email
     - github.event.pull_request.head.ref / .head.label
     - github.event.pull_request.head.repo.default_branch
     - github.head_ref

2. Pass through env: with proper quoting instead:
     env:
       TITLE: ${{ github.event.issue.title }}
     run: echo "$TITLE"

3. Background:
   https://github.blog/security/vulnerability-research/how-to-catch-github-actions-workflow-injections-before-attackers-do/

This is the first edit of this workflow file in the current session -- the
hook is blocking once so you read the checklist. Retry the same write/patch
call and it will proceed. Further edits of this file in this session will
print this reminder as advisory only.
"""


def state_file(hermes_dir: Path, session_id: str) -> Path:
    base = hermes_dir / "sessions" / session_id if session_id else hermes_dir
    return base / "github-workflow-warnings.json"


def load_shown(path: Path) -> set:
    if not path.exists():
        return set()
    try:
        with path.open("r", encoding="utf-8") as f:
            return set(json.load(f))
    except (OSError, json.JSONDecodeError):
        return set()


def save_shown(path: Path, shown: set) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(sorted(shown), f)
    except OSError:
        pass


def is_workflow_path(path: str) -> bool:
    if not path:
        return False
    norm = path.replace("\\", "/").lstrip("/")
    if ".github/workflows/" not in norm:
        return False
    lower = norm.lower()
    return lower.endswith(".yml") or lower.endswith(".yaml")


def cleanup_old_state(hermes_dir: Path) -> None:
    """Remove session state files older than 30 days."""
    try:
        sessions_dir = hermes_dir / "sessions"
        if not sessions_dir.is_dir():
            return
        cutoff = datetime.now(timezone.utc).timestamp() - 30 * 24 * 3600
        for session_dir in sessions_dir.iterdir():
            candidate = session_dir / "github-workflow-warnings.json"
            if candidate.exists() and candidate.stat().st_mtime < cutoff:
                candidate.unlink(missing_ok=True)
    except OSError:
        pass


def main() -> None:
    if bypass_env("HERMES_ALLOW_GH_WORKFLOW_SECURITY"):
        allow()

    event = read_event()
    tool_name = event.get("tool_name", "")
    if tool_name not in ("write_file", "patch"):
        allow()

    path = file_path(event.get("tool_input", {}))
    if not is_workflow_path(path):
        allow()

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    hermes_dir = cwd / ".hermes"
    session_id = event_session_id(event)

    # 10% chance to clean up stale state files -- cheap, opportunistic, no separate cron needed.
    if random.random() < 0.1:
        cleanup_old_state(hermes_dir)

    state_path = state_file(hermes_dir, session_id)
    key = path.replace("\\", "/").lower()
    shown = load_shown(state_path)

    if key in shown:
        sys.stderr.write(REMINDER)
        allow()

    shown.add(key)
    save_shown(state_path, shown)
    block(REMINDER)


if __name__ == "__main__":
    main()
