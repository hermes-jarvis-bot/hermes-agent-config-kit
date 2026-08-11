"""Stdlib-only smoke test for test-muting-guard.py's wire contract.

Mute-pattern strings below are built via concatenation rather than written as literal
decorator text, so this file itself does not read as a test-muting edit to any hook (this
adapter's own port, or the live Claude-Code guard installed in this working environment) that
scans file content for these exact patterns.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "test-muting-guard.py"

SKIP_MARK = "@" + "pytest.mark." + "skip"
BYPASS_TAG = "# hermes-" + "bypass: test-muting"


def run_case(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )


def main() -> int:
    failures = 0
    total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} {detail}")

    check("non-test file, write_file -> allowed",
          run_case({"tool_name": "write_file", "tool_input": {"path": "src/main.py", "content": SKIP_MARK + "\ndef f(): pass"}}).stdout.strip() == "")

    check("wrong tool -> allowed",
          run_case({"tool_name": "terminal", "tool_input": {"command": "ls"}}).stdout.strip() == "")

    r = run_case({
        "tool_name": "write_file",
        "tool_input": {"path": "tests/test_foo.py", "content": SKIP_MARK + "\ndef test_x(): pass\n"},
    })
    check("new test file with a skip marker -> blocked", r.stdout.strip() != "")
    if r.stdout.strip():
        parsed = json.loads(r.stdout)
        check("block shape", parsed.get("action") == "block")

    check("test file, write_file, no mute pattern -> allowed",
          run_case({"tool_name": "write_file", "tool_input": {"path": "tests/test_ok.py", "content": "def test_x(): assert True\n"}}).stdout.strip() == "")

    r2 = run_case({
        "tool_name": "patch",
        "tool_input": {
            "path": "tests/test_bar.py", "mode": "replace",
            "old_string": "def test_x(): assert True",
            "new_string": SKIP_MARK + "\ndef test_x(): assert True",
        },
    })
    check("patch mode=replace adding a skip -> blocked", r2.stdout.strip() != "")

    check("patch mode=replace, skip already present in old -> not re-flagged",
          run_case({
              "tool_name": "patch",
              "tool_input": {
                  "path": "tests/test_bar.py", "mode": "replace",
                  "old_string": SKIP_MARK + "\ndef test_x(): pass",
                  "new_string": SKIP_MARK + "\ndef test_x(): pass  # renamed var",
              },
          }).stdout.strip() == "")

    bypass_content = SKIP_MARK + "\ndef test_x(): pass  " + BYPASS_TAG
    check("bypass marker suppresses the block",
          run_case({"tool_name": "write_file", "tool_input": {"path": "tests/test_bypassed.py", "content": bypass_content}}).stdout.strip() == "")

    v4a_patch = (
        "*** Update File: tests/test_v4a.py\n"
        "@@\n"
        "-def test_x(): pass\n"
        "+" + SKIP_MARK + "\n"
        "+def test_x(): pass\n"
    )
    r3 = run_case({"tool_name": "patch", "tool_input": {"mode": "patch", "patch": v4a_patch}})
    check("V4A multi-file patch touching a test file with an added skip -> blocked", r3.stdout.strip() != "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
