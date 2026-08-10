"""Stdlib-only smoke test for db-snapshot-guard.py's wire contract.

This hook never emits a block JSON (side-effect-only safety net) -- correctness is checked via
stdout being empty (never blocks) plus expected diagnostic substrings on stderr. No dependency
on a live Hermes install, ~/.hermes/config.yaml, or actual pg_dump/mysqldump/mongodump binaries
(their absence is itself a tested path -- "not in PATH" is a normal, non-fatal outcome).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "db-snapshot-guard.py"


def run_case(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )


def main() -> int:
    failures = 0
    total = 0

    def check(label, payload, expect_stderr_substr) -> None:
        nonlocal failures, total
        total += 1
        result = run_case(payload)
        stdout_ok = result.stdout.strip() == ""  # never blocks
        stderr_ok = (expect_stderr_substr is None) or (expect_stderr_substr in result.stderr)
        ok = stdout_ok and stderr_ok
        if not ok:
            failures += 1
        print(
            f"{'PASS' if ok else 'FAIL'}  {label!r:65} "
            f"stdout_empty={stdout_ok} stderr_has={expect_stderr_substr!r}: {stderr_ok}"
        )
        if not ok:
            print(f"      stdout={result.stdout!r}")
            print(f"      stderr={result.stderr!r}")

    check("benign command, no output at all",
          {"tool_name": "terminal", "tool_input": {"command": "ls -la"}}, None)

    check("wrong tool (write_file, not terminal)",
          {"tool_name": "write_file", "tool_input": {"file_path": "x.sql"}}, None)

    check("DROP TABLE with no connection string -> skip-with-warning, never blocks",
          {"tool_name": "terminal", "tool_input": {"command": "DROP TABLE users;"}},
          "no recognizable connection string")

    check("DROP TABLE with a postgres URL, pg_dump likely absent -> FAILED not blocked",
          {"tool_name": "terminal",
           "tool_input": {"command": "psql postgres://u:p@localhost/db -c 'DROP TABLE users;'"}},
          "[db-snapshot-guard]")

    check("bypass marker suppresses the whole safety net silently",
          {"tool_name": "terminal",
           "tool_input": {"command": "DROP TABLE users; # hermes-bypass: db-snapshot"}},
          None)

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
