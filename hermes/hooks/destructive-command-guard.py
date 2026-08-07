#!/usr/bin/env python3
"""pre_tool_call: block catastrophically destructive shell commands.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/destructive-command-guard.py, reimplemented
for Hermes Agent's shell-hook contract (see hermes_hook_common.py for the exact
I/O differences from the upstream Claude-Code version this was read from).

Covers: rm -rf on root/home/*, database DROP/TRUNCATE, docker/k8s mass delete,
mkfs/dd on block devices, fork bomb. Bypass: HERMES_ALLOW_DESTRUCTIVE=1 or a
`# hermes-bypass: destructive` marker in the command text.

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
    # Filesystem catastrophes - only truly dangerous paths
    r"\brm\s+-[a-z]*r[a-z]*f?\s+/\s*($|;|&|\|)",
    r"\brm\s+-[a-z]*r[a-z]*f?\s+/\*",
    r"\brm\s+-[a-z]*r[a-z]*f?\s+\*\s*($|;|&|\|)",
    r"\brm\s+-[a-z]*r[a-z]*f?\s+~\s*($|;|&|\|/)",
    r"\brm\s+-[a-z]*r[a-z]*f?\s+\$HOME(\s|$|/)",
    r"\brm\s+-[a-z]*r[a-z]*f?\s+~/\s*($|;|&|\|)",
    r"\brm\s+-[a-z]*r[a-z]*f?\s+/(etc|usr|var|boot|sys|proc|lib|lib64|sbin|bin|root|home)(/\s*)?($|;|&|\|)",
    r"\bfind\s+/\s+.*-delete\b",
    r"\bmkfs\.[a-z0-9]+\s+/dev/",
    r"\bdd\s+if=\S+\s+of=/dev/[sh]d[a-z]",
    r"\b:\s*\(\s*\)\s*\{\s*:\s*\|\s*:",  # fork bomb
    # Database destruction
    r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b",
    r"\bTRUNCATE\s+TABLE\b",
    r"\bdropdb\b",
    r"\bmongo\s+.*\bdropDatabase\b",
    r"\bredis-cli\s+.*\bflushall\b",
    r"\bDELETE\s+FROM\s+\w+\s*(;|$)",  # DELETE without WHERE
    # Container/orchestration mass delete
    r"\bdocker\s+rm\s+-f\s+\$\(docker\s+ps",
    r"\bdocker\s+system\s+prune\s+.*-a.*--volumes",
    r"\bdocker-compose\s+down\s+.*-v",
    r"\bkubectl\s+delete\s+(ns|namespace|all)\b",
    r"\bkubectl\s+delete\s+.*--all\b",
    r"\bhelm\s+uninstall\b.*-n\s+(prod|production)",
]


def main() -> None:
    event = read_event()
    tool_name = event.get("tool_name", "")
    if tool_name != "terminal":
        allow()

    cmd = terminal_command(event.get("tool_input", {}))
    if not cmd:
        allow()

    hit = any_match(cmd, PATTERNS)
    if not hit:
        allow()

    if bypass("destructive", cmd):
        log("WARN", "block_destructive", "bypass", hit, cmd)
        allow()

    log("BLOCK", "block_destructive", "deny", hit, cmd)
    block(
        f"Destructive pattern detected: /{hit}/. "
        "This hook blocks catastrophic operations.\n"
        "If the action is intentional and reversibility is understood:\n"
        "  1) confirm the goal and backup with the user first\n"
        "  2) run with HERMES_ALLOW_DESTRUCTIVE=1 in the same session\n"
        "Categories: rm -rf root/home, DROP/TRUNCATE, kubectl delete all, "
        "docker prune --volumes, dd/mkfs, fork bomb."
    )


if __name__ == "__main__":
    main()
