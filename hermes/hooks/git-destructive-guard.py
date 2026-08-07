#!/usr/bin/env python3
"""pre_tool_call: block destructive git operations.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/git-destructive-guard.py, reimplemented for
Hermes Agent's shell-hook contract (see hermes_hook_common.py for the exact I/O
differences from the upstream Claude-Code version this was read from).

Covers: reset --hard, push --force, branch -D, clean -fdx, checkout -- .,
filter-branch/filter-repo, deleting main/master/production refs, interactive
rebase of HEAD, and other commands that rewrite history or lose uncommitted
work. Bypass: HERMES_ALLOW_GIT_DESTRUCTIVE=1 or a
`# hermes-bypass: git-destructive` marker in the command text.

Never invoked automatically by this adapter. Copied by
scripts/install_hermes.py into <hermes-home>/hooks/config-kit/; the operator
must add a `hooks: pre_tool_call:` entry pointing at it in their own
~/.hermes/config.yaml by hand — see hermes/hooks/README.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    any_match,
    block,
    bypass,
    log,
    read_event,
    terminal_command,
)

# Patterns are regexes. Case-insensitive match via hermes_hook_common.any_match.
PATTERNS = [
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+(push\s+)?(-f|--force(?!-with-lease))\b",
    r"\bgit\s+push\s+.*--force(?!-with-lease)",
    # any_match() runs every pattern with re.IGNORECASE, so a bare -D also
    # matched the *safe* lowercase -d, which refuses to delete unmerged
    # branches and is exactly what we recommend instead. Pin the case locally
    # with (?-i:...) rather than dropping IGNORECASE globally — other guards
    # rely on it for things like DROP TABLE.
    r"\bgit\s+branch\s+(?-i:-D)\b",
    # --delete --force is the same operation spelled out, in either order.
    r"\bgit\s+branch\s+.*--delete\b.*--force\b",
    r"\bgit\s+branch\s+.*--force\b.*--delete\b",
    r"\bgit\s+clean\s+-[fdxX]{2,}",
    r"\bgit\s+clean\s+-[fdx]\s+-[fdx]",
    r"\bgit\s+checkout\s+--\s+\.",
    r"\bgit\s+restore\s+--source",
    r"\bgit\s+restore\s+--staged\s+--worktree\s+\.",
    r"\bgit\s+filter-(branch|repo)\b",
    r"\bgit\s+update-ref\s+-d\s+refs/heads/(main|master|prod(uction)?)",
    r"\bgit\s+rebase\s+.*-i.*\s+HEAD",  # interactive rebase - often destructive
    r"\bgit\s+reflog\s+expire\s+--expire=now",
    r"\bgit\s+gc\s+--prune=now\s+--aggressive",
]


def main() -> None:
    event = read_event()
    if event.get("tool_name") != "terminal":
        allow()

    cmd = terminal_command(event.get("tool_input", {}))
    if not cmd:
        allow()

    hit = any_match(cmd, PATTERNS)
    if not hit:
        allow()

    if bypass("git-destructive", cmd, env_name="HERMES_ALLOW_GIT_DESTRUCTIVE"):
        log("WARN", "block_git_destructive", "bypass", hit, cmd)
        allow()

    log("BLOCK", "block_git_destructive", "deny", hit, cmd)
    block(
        f"Destructive git operation: /{hit}/.\n"
        "These commands rewrite history or lose uncommitted work.\n"
        "Before running it:\n"
        "  1) confirm the goal with the user\n"
        "  2) make a fresh backup branch: git branch backup-$(date +%s)\n"
        "  3) run with HERMES_ALLOW_GIT_DESTRUCTIVE=1\n"
        "Safer alternatives:\n"
        "  reset --hard -> reset --keep, or stash && reset\n"
        "  push --force -> push --force-with-lease\n"
        "  branch -D -> merge/rebase, then delete the merged branch\n"
        "  clean -fdx -> check git status, then a targeted rm"
    )


if __name__ == "__main__":
    main()
