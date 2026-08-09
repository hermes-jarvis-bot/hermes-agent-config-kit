"""Shared Hermes shell-hook utilities. Reviewed-hook lane (see SECURITY.md).

Reads a pre_tool_call/post_tool_call JSON event from stdin, exposes helpers
for logging and blocking. Adapted from claude-code-config's
hooks/safety_common.py for the Hermes Agent shell-hook wire protocol.

Hermes exit conventions (verified 2026-08-07 against the live
agent/shell_hooks.py source and
https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks):
  - exit code is NEVER used to block. A non-zero exit, malformed JSON, or a
    timeout is logged as a warning only; stdout is still parsed for a
    decision. This is the one load-bearing difference from Claude Code's
    "exit 2 = block" convention.
  - exit 0 (or any code) + empty stdout: allow (silent pass-through)
  - JSON {"action": "block", "message": "..."} on stdout: block
    (Hermes-canonical shape; the Claude-Code-style
    {"decision": "block", "reason": "..."} shape is also accepted and
    translated internally by Hermes, but this module emits the canonical
    shape directly so it needs no translation.)

This module is never invoked automatically by this adapter or its CI. It is
copied by scripts/install_hermes.py into <hermes-home>/hooks/config-kit/ and
must be wired into the operator's own ~/.hermes/config.yaml by hand — see
hermes/hooks/README.md.

See: hermes hooks --help, website/docs/user-guide/features/hooks.md
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

LOG_PATH = Path.home() / ".hermes" / "logs" / "config-kit-safety.log"


def read_event() -> dict:
    """Parse a pre_tool_call/post_tool_call event from stdin. Empty dict on failure."""
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        raw = raw.lstrip("﻿")
        return json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return {}


def log(level: str, hook: str, verdict: str, pattern: str, target: str) -> None:
    """Append an audit line. One JSONL record per event. Best-effort."""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "level": level,
            "hook": hook,
            "verdict": verdict,
            "pattern": pattern,
            "target": target[:400],
        }
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def block(reason: str) -> None:
    """Emit a Hermes-canonical block verdict and exit."""
    msg = {"action": "block", "message": reason}
    print(json.dumps(msg, ensure_ascii=False))
    sys.exit(0)


def allow() -> None:
    """Pass-through: no output, exit 0."""
    sys.exit(0)


def bypass_env(name: str) -> bool:
    """Check a HERMES_ALLOW_* override. Accepts 1/true/yes/on."""
    val = os.environ.get(name, "").strip().lower()
    return val in {"1", "true", "yes", "on"}


def bypass_marker(command_or_content: str, name: str) -> bool:
    """Check an in-command bypass marker.

    Accepted forms (case-insensitive):
        # hermes-bypass: NAME
        # hermes-bypass: other, NAME, third
        // hermes-bypass: NAME   (js/ts contexts)
        <!-- hermes-bypass: NAME -->  (html/md contexts)
    """
    if not command_or_content or not name:
        return False
    pattern = r"(?:#|//|<!--)\s*hermes-bypass\s*:\s*([a-z0-9_, \-]+)"
    for m in re.finditer(pattern, command_or_content, re.IGNORECASE):
        names = [x.strip().lower() for x in m.group(1).split(",")]
        if name.lower() in names or "all" in names:
            return True
    return False


def bypass(name: str, command_or_content: str = "", env_name: str | None = None) -> bool:
    """Unified bypass check. True if either the marker or the env override is set."""
    if env_name is None:
        env_name = f"HERMES_ALLOW_{name.upper().replace('-', '_')}"
    if bypass_env(env_name):
        return True
    if bypass_marker(command_or_content, name):
        return True
    return False


def terminal_command(tool_input: dict) -> str:
    """Extract the command string from a `terminal` tool call's input."""
    return str((tool_input or {}).get("command", ""))


def file_path(tool_input: dict) -> str:
    """Extract the file path from a `read_file`/`write_file`/`patch` tool call's input."""
    ti = tool_input or {}
    return str(ti.get("file_path") or ti.get("path") or "")


def any_match(text: str, patterns: list[str]) -> str | None:
    """Return the first matching regex (string form) or None. Case-insensitive."""
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return pat
    return None


_TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:_(\d{2})-(\d{2}))?")


def filename_timestamp(path: Path) -> float | None:
    """Parse a `YYYY-MM-DD_HH-MM` prefix from a filename into an epoch timestamp.

    Returns None if the filename has no such prefix — the caller should fall back to
    `path.stat().st_mtime` in that case. The filename is authoritative over mtime for a
    handoff file: a merge/checkout/sync rewrites mtimes for every file it touches, which
    would otherwise make a months-old restored handoff read as "just written".
    """
    m = _TS_RE.match(path.name)
    if not m:
        return None
    try:
        hh = int(m.group(2)) if m.group(2) else 0
        mm = int(m.group(3)) if m.group(3) else 0
        dt = _dt.datetime.strptime(m.group(1), "%Y-%m-%d").replace(hour=hh, minute=mm)
        return dt.timestamp()
    except ValueError:
        return None
