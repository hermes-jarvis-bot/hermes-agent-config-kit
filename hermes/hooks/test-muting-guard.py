#!/usr/bin/env python3
"""pre_tool_call: flag test-muting edits before they land.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/test-muting-guard.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

Watches write_file/patch on test files. If the new content adds a skip/xfail/disable pattern
that wasn't already there, blocks with guidance to fix instead of mute.

Why: "muted failing test" is how bugs ship. Pattern from real incidents:
 - adding @pytest.mark.skip to hide a recently broken test
 - .only() left over from debugging -- silently runs 1 test of 100
 - it.skip() replacing it() after a merge conflict

Ported unchanged: the test-path matcher, the full multi-language mute-pattern list
(pytest/unittest/Jest-Mocha-Vitest/JUnit/Go/Rust/RSpec), the old-vs-new added-pattern diff
logic. Adapted: `Edit`/`Write`/`NotebookEdit` -> Hermes's `write_file`/`patch` (no separate
NotebookEdit tool exists); `patch` mode="patch" (V4A, can span multiple files) treats every
"+"-prefixed line across the whole patch body as "new" and every "-"-prefixed line as "old",
since V4A bodies don't carry separate old/new full-file strings the way `mode="replace"` does --
an approximate signal for the rarer multi-file-patch-touches-a-test-file case, not a full diff
reconstruction (same class of simplification over-engineering-advisor.py already accepts for
V4A patches).

Bypass: HERMES_ALLOW_TEST_MUTING=1.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import allow, block, bypass, log, read_event  # noqa: E402

TEST_PATH_REGEX = re.compile(
    r"(?:^|/|\\)("
    r"tests?|__tests__|spec|specs"
    r")(?:/|\\)"
    r"|"
    r"(?:^|/|\\)[^/\\]*"
    r"(?:_test|_spec|\.test|\.spec)"
    r"\.[a-z]+$",
    re.IGNORECASE,
)

MUTE_PATTERNS = [
    r"@pytest\.mark\.skip\b",
    r"@pytest\.mark\.xfail\b",
    r"pytest\.skip\s*\(",
    r"@unittest\.skip\b",
    r"@unittest\.expectedFailure\b",
    r"\b(it|test|describe|context)\.skip\s*\(",
    r"\bx(it|test|describe|context)\s*\(",
    r"\.todo\s*\(",
    r"\b(it|test|describe|context|suite)\.only\s*\(",
    r"@Ignore\b",
    r"@Disabled\b",
    r"\bt\.Skip\s*\(",
    r"\bt\.Skipf\s*\(",
    r"#\[ignore\]",
    r"\bskip\s+['\"]\w",
    r"\bxdescribe\b|\bxcontext\b|\bxit\b",
    r"^\s*return;?\s*//\s*(skip|todo|fixme|disable)",
]

_V4A_HEADER_RE = re.compile(r'^\*\*\*\s*(?:Update|Add|Delete)\s+File:\s*(.+)$', re.MULTILINE)


def is_test_file(path: str) -> bool:
    return bool(TEST_PATH_REGEX.search(path))


def find_added_mute(old: str, new: str) -> str | None:
    """Return the first mute pattern that appears in `new` but not in `old`."""
    if not new:
        return None
    for pat in MUTE_PATTERNS:
        if not re.search(pat, new, re.IGNORECASE | re.MULTILINE):
            continue
        if not re.search(pat, old or "", re.IGNORECASE | re.MULTILINE):
            return pat
    return None


def _v4a_old_new(body: str) -> tuple[str, str]:
    old_lines, new_lines = [], []
    for line in body.splitlines():
        if line.startswith("+++") or line.startswith("---") or line.startswith("*** "):
            continue
        if line.startswith("+"):
            new_lines.append(line[1:])
        elif line.startswith("-"):
            old_lines.append(line[1:])
    return "\n".join(old_lines), "\n".join(new_lines)


def main() -> None:
    event = read_event()
    tool_name = event.get("tool_name", "")
    if tool_name not in {"write_file", "patch"}:
        allow()

    tool_input = event.get("tool_input", {}) or {}
    mode = tool_input.get("mode") or "replace"

    if tool_name == "patch" and mode == "patch":
        body = str(tool_input.get("patch", ""))
        paths = [m.group(1).strip() for m in _V4A_HEADER_RE.finditer(body) if m.group(1).strip()]
        if not any(is_test_file(p) for p in paths):
            allow()
        old, new = _v4a_old_new(body)
        path = paths[0] if paths else "(multi-file patch)"
    else:
        path = str(tool_input.get("path") or tool_input.get("file_path", ""))
        if not is_test_file(path):
            allow()
        if tool_name == "write_file":
            old, new = "", str(tool_input.get("content", ""))
        else:  # patch mode=replace
            old = str(tool_input.get("old_string", ""))
            new = str(tool_input.get("new_string", ""))

    hit = find_added_mute(old, new)
    if not hit:
        allow()

    if bypass("test-muting", new, env_name="HERMES_ALLOW_TEST_MUTING"):
        log("WARN", "block_test_muting", "bypass", hit, path)
        allow()

    log("BLOCK", "block_test_muting", "deny", hit, path)
    block(
        f"Test mute pattern added in {path}: /{hit}/.\n"
        "\"Muted failing test\" is how bugs ship. Frequent real incidents:\n"
        "  - @pytest.mark.skip added to hide a recently broken test\n"
        "  - .only() left over from debugging -> suite silently runs 1 of 100 tests\n"
        "  - it.skip() replaced it() after a merge conflict\n"
        "What to do:\n"
        "  1) Fix the test or the code it exercises\n"
        "  2) If the test is genuinely obsolete (testing a deprecated feature) - delete it "
        "entirely, don't mute\n"
        "  3) If genuinely flaky and there's no time to fix now - @skip with reason='...' + a "
        "linked issue\n"
        "  4) If deliberate and everyone knows - HERMES_ALLOW_TEST_MUTING=1 + an explanatory commit"
    )


if __name__ == "__main__":
    main()
