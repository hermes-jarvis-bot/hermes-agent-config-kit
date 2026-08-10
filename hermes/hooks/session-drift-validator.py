#!/usr/bin/env python3
"""pre_llm_call (is_first_turn only): flag stale file-path references in project config docs.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/session-drift-validator.py, reimplemented for Hermes
Agent's shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the
upstream Claude-Code version this was read from).

Scans CLAUDE.md, AGENTS.md, and `.claude/rules/*.md` for things that look like file-path
references, then checks whether each one still exists on disk. A stale reference means the doc
tells the agent (or a human) to look at something that moved or was deleted -- worth surfacing
once, at the start of a session, rather than discovering it mid-task.

Adaptation from upstream: the original only scanned CLAUDE.md + .claude/rules/*.md (Claude-Code
specific). This port also scans AGENTS.md -- the harness-neutral canonical-context file this
adapter's own cross-harness-agents-md.md convention (and this very repo) uses -- so the check
has value for AGENTS.md-only projects too, not just Claude-Code ones. Same is_first_turn
substitution as session-handoff-check.py (Hermes has no SessionStart-equivalent whose output
reaches the model); this hook's output is read-only and diagnostic, so it is emitted via
pre_llm_call's `{"context": ...}` channel same as the sibling hooks, rather than silently
dropped.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import emit_context, read_event  # noqa: E402

PATH_PATTERN = re.compile(
    r'(?:'
    r'[A-Za-z]:[/\\][^\s`"\')>]+'
    r'|~/[^\s`"\')>]+'
    r'|(?:\./|\.\./)[\w./-]+'
    r'|[\w.-]+(?:/[\w.-]+){2,}'
    r')'
)

SKIP_PATTERNS = [
    r'\{\{',
    r'://',
    r'example\.com',
    r'<[^>]+>',
    r'\$\{',
]

EXT_RE = re.compile(r'\.[A-Za-z0-9]{1,5}$')
DOMAIN_RE = re.compile(r'^[\w-]+(\.[\w-]+)*\.(com|org|net|io|dev|app|ai|ru|club|space|work|md)$', re.I)


def find_config_files(root: str) -> list[str]:
    files = []
    for name in ("CLAUDE.md", "AGENTS.md"):
        candidate = os.path.join(root, name)
        if os.path.isfile(candidate):
            files.append(candidate)
    rules_dir = os.path.join(root, ".claude", "rules")
    if os.path.isdir(rules_dir):
        for f in sorted(os.listdir(rules_dir)):
            if f.endswith(".md"):
                files.append(os.path.join(rules_dir, f))
    return files


def extract_paths(text: str) -> list[str]:
    paths = []
    for match in PATH_PATTERN.finditer(text):
        path = match.group(0).rstrip('.,;:)')
        if any(re.search(skip, path) for skip in SKIP_PATTERNS):
            continue
        if not path.isascii():
            continue
        anchored = path.startswith(('./', '../', '~')) or re.match(r'^[A-Za-z]:[/\\]', path)
        if not anchored:
            first_seg = path.split('/')[0]
            if DOMAIN_RE.match(first_seg):
                continue
            if not EXT_RE.search(path):
                continue
        paths.append(path)
    return paths


def resolve_path(path: str, source_file: str, cwd: str) -> str | None:
    expanded = os.path.expanduser(path)
    if os.path.isabs(expanded) and os.path.exists(expanded):
        return expanded
    source_dir = os.path.dirname(source_file)
    candidate = os.path.join(source_dir, path)
    if os.path.exists(candidate):
        return os.path.abspath(candidate)
    candidate = os.path.join(cwd, path)
    if os.path.exists(candidate):
        return os.path.abspath(candidate)
    return None


def _display_path(config_file: str, cwd: str) -> str:
    try:
        return os.path.relpath(config_file, cwd)
    except ValueError:
        return config_file


def assess(cwd: str) -> str | None:
    """Return a report string only when drift was found. Silent (None) when clean --
    matching session-handoff-check.py's convention of not injecting confirmation-only
    context into every first turn, unlike upstream which always prints something."""
    config_files = find_config_files(cwd)
    if not config_files:
        return None

    drift_found: list[str] = []
    for config_file in config_files:
        try:
            text = Path(config_file).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for path in extract_paths(text):
            if resolve_path(path, config_file, cwd) is None:
                drift_found.append(f"  {_display_path(config_file, cwd)}: {path}")

    if not drift_found:
        return None

    lines = ["[config-drift] Found stale references:"]
    lines.extend(drift_found[:20])
    if len(drift_found) > 20:
        lines.append(f"  ... and {len(drift_found) - 20} more")
    return "\n".join(lines)


def main() -> int:
    event = read_event()
    if event.get("hook_event_name") != "pre_llm_call":
        return 0
    extra = event.get("extra", {}) or {}
    if not extra.get("is_first_turn"):
        return 0

    cwd = str(event.get("cwd") or os.getcwd())
    report = assess(cwd)
    if report:
        emit_context(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
