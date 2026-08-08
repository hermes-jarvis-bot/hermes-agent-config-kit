#!/usr/bin/env python3
"""pre_tool_call: detect suspicious shell substitution in terminal commands.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/command-injection-guard.py, reimplemented
for Hermes Agent's shell-hook contract (see hermes_hook_common.py for the exact
I/O differences from the upstream Claude-Code version this was read from).

Targets the class of bugs where text meant as data becomes command:
  gh issue create --body "$(dropdb prod)"
  echo "result: $(rm -rf /tmp)" > log.txt

Here the outer command is safe (gh, echo), but $(...) executes before the
argument reaches the outer command. This class is distinct from
destructive-command-guard, which catches a naked 'dropdb'; here the target is
'dropdb' smuggled inside a string.

Strategy:
  - Trivial substitutions are allowed: $(pwd), $(date), $(whoami), $(hostname),
    $(basename ...), $(dirname ...), $(echo ...), $(uname ...)
  - Substitution containing a destructive verb -> hard block
  - Other substitutions -> advisory block (pass with confirmation)

Bypass: HERMES_ALLOW_INJECTION=1 or a `# hermes-bypass: injection` marker in
the command text.

Never invoked automatically by this adapter. Copied by
scripts/install_hermes.py into <hermes-home>/hooks/config-kit/; the operator
must add a `hooks: pre_tool_call:` entry pointing at it in their own
~/.hermes/config.yaml by hand — see hermes/hooks/README.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    block,
    bypass,
    log,
    read_event,
    terminal_command,
)

# Well-known side-effect-free utilities safe inside $(...)
TRIVIAL_CMDS = {
    "pwd", "date", "whoami", "hostname", "id", "uname", "echo", "printf",
    "basename", "dirname", "realpath", "readlink",
    "cat", "head", "tail",  # reads; add only if they take trivial args
    "which", "command", "type",
    "tr", "cut", "wc", "sort", "uniq",
    "git",  # git rev-parse etc is common and safe
    "node", "python", "python3",  # when running --version
}

SUBST_REGEX = re.compile(r"\$\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
BACKTICK_REGEX = re.compile(r"`([^`]+)`")

DESTRUCTIVE_VERBS = re.compile(
    r"\b("
    r"dropdb|dropuser|drop\s+(table|database|schema)"
    r"|truncate\s+table"
    r"|delete\s+from\s+\w+(\s*;|\s*$|\s+where\s+(1\s*=\s*1|true))"  # DELETE no real WHERE
    r"|rm\s+-[rf]+"
    r"|mkfs\.|dd\s+if=|dd\s+of=/dev/"
    r"|kubectl\s+delete"
    r"|docker\s+(rm\s+-f|system\s+prune)"
    r"|killall|pkill"
    r"|shutdown|reboot|halt|poweroff"
    r"|:\s*\(\s*\)\s*\{"  # fork bomb
    r"|curl\s+.*\|\s*(sh|bash)"  # pipe to shell
    r"|wget\s+.*\|\s*(sh|bash)"
    r")",
    re.IGNORECASE,
)


def is_trivial(subst_body: str) -> bool:
    """Check if the substitution body is a safe utility with safe args."""
    body = subst_body.strip()
    if not body:
        return True
    # Heredoc forms: $(cat <<EOF ... EOF) or $(cat <<'EOF' ... EOF) -
    # safely reads multiline literal text into a string. No execution.
    if re.match(r"^(cat|printf|echo)\s+<<", body) or re.match(r"^<<", body):
        return True
    # First word determines the utility
    first = body.split(maxsplit=1)[0]
    first = first.lstrip("\\")  # strip leading escape
    if first not in TRIVIAL_CMDS:
        return False
    # Extra check: even trivial cmd with shell metacharacters in args is suspect.
    # But <<- and << are heredoc markers, not pipes/redirects - allow.
    if re.search(r"[;&|](?!\|)", body):  # ; & | (but not ||)
        return False
    if re.search(r"[<>](?!<)", body):  # < or > but not << (heredoc)
        return False
    return True


def find_substitutions(cmd: str) -> list[tuple[str, str]]:
    """Return list of (form, body) for each substitution in cmd.

    form: '$()' or '``'
    body: inner text
    """
    found: list[tuple[str, str]] = []
    # Skip single-quoted regions since $(...) is literal inside '...'
    # Approximate: remove content between unescaped single quotes
    sanitized = re.sub(r"'[^']*'", "''", cmd)
    for m in SUBST_REGEX.finditer(sanitized):
        found.append(("$()", m.group(1)))
    for m in BACKTICK_REGEX.finditer(sanitized):
        found.append(("``", m.group(1)))
    return found


def main() -> None:
    event = read_event()
    if event.get("tool_name") != "terminal":
        allow()

    cmd = terminal_command(event.get("tool_input", {}))
    if not cmd:
        allow()

    substitutions = find_substitutions(cmd)
    if not substitutions:
        allow()

    # Check each substitution
    destructive_hits: list[str] = []
    nontrivial_hits: list[str] = []
    for form, body in substitutions:
        if DESTRUCTIVE_VERBS.search(body):
            destructive_hits.append(f"{form} -> {body[:80]}")
        elif not is_trivial(body):
            nontrivial_hits.append(f"{form} -> {body[:80]}")

    if not destructive_hits and not nontrivial_hits:
        allow()

    if bypass("injection", cmd):
        pattern = destructive_hits[0] if destructive_hits else nontrivial_hits[0]
        log("WARN", "block_command_injection", "bypass", pattern, cmd)
        allow()

    # Destructive substitution = always block
    if destructive_hits:
        log("BLOCK", "block_command_injection", "deny_destructive",
            destructive_hits[0], cmd)
        block(
            "Destructive shell substitution detected inside command:\n"
            f"  {destructive_hits[0]}\n"
            "This is the bug class where text meant as data executes as a\n"
            "command because of incorrectly escaped quoting. Real example:\n"
            "  gh issue create --body \"...$(dropdb prod)...\"\n"
            "The $() substitution runs BEFORE the argument reaches gh.\n"
            "What to do:\n"
            "  - use single quotes to make $() literal\n"
            "  - pass the text via stdin: printf '...' | gh ...\n"
            "  - use --body-file instead of an inline --body\n"
            "  - if the substitution is genuinely intended: HERMES_ALLOW_INJECTION=1"
        )

    # Non-trivial but non-destructive = advisory block
    log("BLOCK", "block_command_injection", "deny_nontrivial",
        nontrivial_hits[0], cmd)
    block(
        f"Non-trivial shell substitution: {nontrivial_hits[0]}\n"
        "A substitution with side effects. Confirm it is intentional.\n"
        "Trivial substitutions (pwd, date, whoami, basename, dirname, echo) pass.\n"
        "If this is fine: HERMES_ALLOW_INJECTION=1."
    )


if __name__ == "__main__":
    main()
