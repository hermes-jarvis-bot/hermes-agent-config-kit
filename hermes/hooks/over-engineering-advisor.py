#!/usr/bin/env python3
"""post_tool_call(write_file|patch): advisory nudge on large / dependency-adding code changes.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's hooks/over-engineering-advisor.py
(see mappings/reviewed-hooks.yaml). Makes the quality-code / anti-over-engineering (YAGNI)
principle a mechanical layer, not just an always-on rule that decays under context pressure.

Audit-log-only, by design and by necessity (verified 2026-08-08 against the live
model_tools.py/agent/shell_hooks.py source, same finding as verify-deleted-guard.py): Hermes's
post_tool_call is a fire-and-forget observer hook whose return value is discarded by its only
caller (`_emit_post_tool_call_hook()` in model_tools.py), so upstream's `additionalContext`
mechanism (Claude Code's PostToolUse -> same-turn model feedback) has no working equivalent
here. This script logs a durable, operator-inspectable advisory instead of trying to nudge the
live agent turn — a real capability gap versus upstream, not a reimplementation shortcut.

Design (unchanged from upstream):
  * NON-BLOCKING by construction — an advisory only, never a block.
  * Checks ONLY reliable mechanical signals: a large net addition to a code file, or a new
    dependency in a manifest. Fuzzy "abstraction smells" are deliberately NOT auto-classified
    here — left to the model + the /lean-code (or /simplify) review skill.
  * Scoped to code files + dependency manifests. Docs/markdown/data are skipped.

Tool-shape adaptation (Hermes has no MultiEdit; `patch` covers both cases):
  * `write_file` -> upstream's `Write` (args: path, content).
  * `patch` mode="replace" (default) -> upstream's `Edit` (args: path, old_string, new_string).
  * `patch` mode="patch" (V4A, can span multiple files in one call) -> upstream's `MultiEdit`
    equivalent, in a structurally different format. File paths are extracted from the same
    `*** Update/Add/Delete/Move File:` header regex Hermes's own
    agent/tool_dispatch_helpers.py:_extract_file_mutation_targets() uses internally (reused
    for consistency, not reinvented). Net lines are counted as (+lines - -lines) across the
    whole patch body.
    # simplification: V4A net-line counting is aggregate across the whole multi-file patch,
    # not per-file, and does not distinguish a rename's line churn from real additions. This
    # is an advisory nudge, not a gate, so an approximate signal is an acceptable ceiling;
    # upgrade path is a real V4A parser (tools/patch_parser.py already has one) if this ever
    # needs per-file precision.

Tunables: HERMES_BLOAT_EDIT_LINES (default 150), HERMES_BLOAT_NEWFILE_LINES (default 300).
Bypass: HERMES_ALLOW_BLOAT=1 or a `# hermes-bypass: bloat` marker in the changed content.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import bypass, log, read_event  # noqa: E402

CODE_EXT = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".c", ".h",
    ".hpp", ".cpp", ".cc", ".cs", ".rb", ".php", ".swift", ".kt", ".scala",
    ".m", ".mm", ".lua", ".sh", ".ps1", ".vue", ".svelte",
}
DEP_MANIFESTS = {
    "package.json", "requirements.txt", "pyproject.toml", "go.mod", "cargo.toml",
    "gemfile", "build.gradle", "pom.xml", "pubspec.yaml", "composer.json",
}

EDIT_LIMIT = int(os.environ.get("HERMES_BLOAT_EDIT_LINES", "150"))
NEWFILE_LIMIT = int(os.environ.get("HERMES_BLOAT_NEWFILE_LINES", "300"))

# Same regexes as agent/tool_dispatch_helpers.py:_extract_file_mutation_targets() — reused so
# this hook's file-path extraction from a V4A patch body never drifts from Hermes's own.
_V4A_HEADER_RE = re.compile(r'^\*\*\*\s*(?:Update|Add|Delete)\s+File:\s*(.+)$', re.MULTILINE)
_V4A_MOVE_RE = re.compile(r'^\*\*\*\s*Move\s+File:\s*(.+?)\s*->\s*(.+)$', re.MULTILINE)


def _advise(text: str, fp: str) -> None:
    log("ADVISE", "over_engineering", "advise", "advisory", fp)
    sys.stderr.write(f"[over_engineering] {text}\n")
    sys.exit(0)


def _lines(s: str) -> int:
    return str(s).count("\n") + (1 if s else 0)


def _v4a_paths(body: str) -> list[str]:
    paths = [m.group(1).strip() for m in _V4A_HEADER_RE.finditer(body) if m.group(1).strip()]
    for m in _V4A_MOVE_RE.finditer(body):
        src, dst = m.group(1).strip(), m.group(2).strip()
        if src:
            paths.append(src)
        if dst:
            paths.append(dst)
    return paths


def _v4a_net_lines(body: str) -> int:
    added = removed = 0
    for line in body.splitlines():
        if line.startswith("+++") or line.startswith("---") or line.startswith("*** "):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1
    return added - removed


def main() -> None:
    event = read_event()
    tool = event.get("tool_name", "")
    if tool not in ("write_file", "patch"):
        sys.exit(0)

    args = event.get("tool_input", {}) or {}
    mode = args.get("mode") or "replace"

    if tool == "patch" and mode == "patch":
        body = str(args.get("patch", ""))
        paths = _v4a_paths(body)
        blob = body
        added_text = body  # V4A has no single "new content" field; the whole body is the signal
        net = _v4a_net_lines(body)
        threshold, signal = EDIT_LIMIT, "large_v4a_patch"
        primary_path = paths[0] if paths else ""
    else:
        primary_path = str(args.get("path", ""))
        paths = [primary_path] if primary_path else []
        if tool == "write_file":
            content = str(args.get("content", ""))
            blob = added_text = content
            net = _lines(content)
            threshold, signal = NEWFILE_LIMIT, "large_file"
        else:  # patch mode=replace
            old_string = str(args.get("old_string", ""))
            new_string = str(args.get("new_string", ""))
            blob = old_string + new_string
            added_text = new_string  # only the added side counts as "adding a dependency"
            net = _lines(new_string) - _lines(old_string)
            threshold, signal = EDIT_LIMIT, "large_addition"

    if bypass("bloat", blob):
        sys.exit(0)

    # 1. New dependency in a manifest — any touched path matching a manifest name.
    for p in paths:
        name = Path(p).name.lower()
        if name in DEP_MANIFESTS and added_text.strip():
            _advise(
                f"[minimalism] {name} changed - adding a dependency? Per quality-code: prefer "
                "stdlib / a native platform feature / an already-installed dependency before "
                "adding a new one for what a few lines can do. If the dependency is genuinely "
                "the minimal correct choice, proceed.",
                p,
            )

    # Only advise on code files past this point.
    if not any(Path(p).suffix.lower() in CODE_EXT for p in paths):
        sys.exit(0)

    if net < threshold:
        sys.exit(0)

    _advise(
        f"[minimalism] ~{net} lines into {primary_path or '(multi-file patch)'}. Per "
        "quality-code (YAGNI ladder): is this the SMALLEST solution that FULLY does the task? "
        "Could stdlib / a native feature / an existing dependency / fewer lines cover it, or is "
        "any of it unrequested abstraction? This targets OVER-building only - never under-"
        f"deliver or cut a required branch. If the task genuinely needs this size, proceed. "
        f"[{signal}]",
        primary_path,
    )


if __name__ == "__main__":
    main()
