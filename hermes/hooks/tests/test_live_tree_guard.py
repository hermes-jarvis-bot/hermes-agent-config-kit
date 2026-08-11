"""Stdlib-only smoke test for live-tree-guard.py's wire contract.

The hook's own --self-test already covers the git-worktree/tracked/append-only classification
logic in depth (real disposable git repo, real worktree); this covers the actual
pre_tool_call dispatch shape via subprocess.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "live-tree-guard.py"


def main() -> int:
    failures = 0
    total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} {detail}")

    self_test = subprocess.run(
        [sys.executable, str(GUARD), "--self-test"], capture_output=True, text=True, timeout=60
    )
    check("hook's own --self-test passes", self_test.returncode == 0, self_test.stdout[-300:])

    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps({"tool_name": "terminal", "tool_input": {"command": "ls"}}),
        capture_output=True, text=True, timeout=10,
    )
    check("wrong tool -> silent", result.stdout.strip() == "" and result.returncode == 0)

    result2 = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps({}),
        capture_output=True, text=True, timeout=10,
    )
    check("empty event -> fail open, no crash", result2.returncode == 0 and result2.stdout.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
