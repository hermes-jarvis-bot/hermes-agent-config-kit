"""Stdlib-only smoke test for github-workflow-security.py's wire contract.

Covers: first edit of a workflow file blocks (forces the checklist into context), a second edit
of the SAME file in the SAME session is advisory-only (stderr, no block), a different session
sees the block again (session-scoped state, not global), and non-workflow paths / wrong tools
pass through untouched.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "github-workflow-security.py"


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

    with tempfile.TemporaryDirectory() as td:
        cwd = str(Path(td))

        check("wrong tool (terminal, not write_file/patch) -> pass through",
              run_case({"tool_name": "terminal", "tool_input": {"command": "ls"}, "cwd": cwd}).stdout.strip() == "")

        check("non-workflow path -> pass through",
              run_case({
                  "tool_name": "write_file",
                  "tool_input": {"file_path": "src/main.py"},
                  "session_id": "s1", "cwd": cwd,
              }).stdout.strip() == "")

        first = run_case({
            "tool_name": "write_file",
            "tool_input": {"file_path": ".github/workflows/ci.yml"},
            "session_id": "s1", "cwd": cwd,
        })
        check("first edit of a workflow file in session s1 -> blocks", first.stdout.strip() != "")
        if first.stdout.strip():
            parsed = json.loads(first.stdout)
            check("block action shape", parsed.get("action") == "block", parsed)
            check("message names the injection checklist", "injection" in parsed.get("message", "").lower())

        second = run_case({
            "tool_name": "patch",
            "tool_input": {"file_path": ".github/workflows/ci.yml"},
            "session_id": "s1", "cwd": cwd,
        })
        check("second edit, same file, same session -> advisory only, no block",
              second.stdout.strip() == "" and "checklist" in second.stderr.lower())

        third = run_case({
            "tool_name": "write_file",
            "tool_input": {"file_path": ".github/workflows/ci.yml"},
            "session_id": "s2", "cwd": cwd,
        })
        check("a DIFFERENT session sees the block again (session-scoped state)",
              third.stdout.strip() != "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
