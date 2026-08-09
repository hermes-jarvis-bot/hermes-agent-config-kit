"""Stdlib-only smoke test for over-engineering-advisor.py's wire contract.

Pipes synthetic post_tool_call JSON directly to the script's stdin over a subprocess and
checks its stderr (audit-log-only, same reasoning as test_verify_deleted_guard.py -- Hermes
discards a post_tool_call hook's return value, so this never emits stdout JSON). No dependency
on a live Hermes install or ~/.hermes/config.yaml, so this runs unmodified in CI. For
verification against Hermes's actual dispatch code path (agent.shell_hooks.run_once), see the
functional_test evidence recorded in mappings/reviewed-hooks.yaml.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "over-engineering-advisor.py"

_SMALL_CONTENT = "\n".join(f"line {i}" for i in range(10))
_LARGE_NEW_FILE = "\n".join(f"line {i}" for i in range(350))  # > NEWFILE_LIMIT (300)
_LARGE_EDIT_ADDITION = "\n".join(f"added line {i}" for i in range(200))  # > EDIT_LIMIT (150)

_V4A_LARGE_PATCH = "\n".join(
    ["*** Update File: src/big.py"] + [f"+added line {i}" for i in range(200)]
)

CASES: list[tuple[str, dict, str | None]] = [
    (
        "wrong tool (terminal, not write_file/patch)",
        {"tool_name": "terminal", "tool_input": {"command": "ls"}},
        None,
    ),
    (
        "small write_file",
        {"tool_name": "write_file", "tool_input": {"path": "src/small.py", "content": _SMALL_CONTENT}},
        None,
    ),
    (
        "large write_file over NEWFILE_LIMIT",
        {"tool_name": "write_file", "tool_input": {"path": "src/big.py", "content": _LARGE_NEW_FILE}},
        "[minimalism]",
    ),
    (
        "large write_file to a non-code extension is skipped",
        {"tool_name": "write_file", "tool_input": {"path": "docs/big.md", "content": _LARGE_NEW_FILE}},
        None,
    ),
    (
        "small patch mode=replace",
        {
            "tool_name": "patch",
            "tool_input": {"path": "src/small.py", "old_string": "a", "new_string": "b"},
        },
        None,
    ),
    (
        "large patch mode=replace over EDIT_LIMIT",
        {
            "tool_name": "patch",
            "tool_input": {"path": "src/edit.py", "old_string": "a", "new_string": _LARGE_EDIT_ADDITION},
        },
        "[minimalism]",
    ),
    (
        "pure-deletion patch (new_string empty) is not flagged as adding a dependency",
        {
            "tool_name": "patch",
            "tool_input": {"path": "package.json", "old_string": '"left-pad": "1.0.0",\n', "new_string": ""},
        },
        None,
    ),
    (
        "dependency manifest touched with new content",
        {
            "tool_name": "patch",
            "tool_input": {"path": "requirements.txt", "old_string": "", "new_string": "left-pad==1.0.0\n"},
        },
        "adding a dependency",
    ),
    (
        "large V4A multi-file patch over EDIT_LIMIT",
        {"tool_name": "patch", "tool_input": {"mode": "patch", "patch": _V4A_LARGE_PATCH}},
        "large_v4a_patch",
    ),
    (
        "bypass marker suppresses an otherwise-large advisory",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "src/big.py",
                "content": _LARGE_NEW_FILE + "\n# hermes-bypass: bloat",
            },
        },
        None,
    ),
]


def run_case(payload: dict) -> str:
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stderr


def main() -> int:
    failures = 0
    for label, payload, expect_substr in CASES:
        stderr = run_case(payload)
        if expect_substr is None:
            ok = stderr.strip() == ""
        else:
            ok = expect_substr in stderr
        got = stderr.strip() or "(empty)"
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} expect={expect_substr!r} got={got!r}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
