"""Stdlib-only smoke test for destructive-command-guard.py's wire contract.

Pipes synthetic pre_tool_call JSON directly to the script's stdin over a
subprocess and checks its stdout — the same shape Hermes's shell-hook engine
uses (see agent/shell_hooks.py's _serialize_payload). No dependency on a
live Hermes install, ~/.hermes/config.yaml, or the shell-hooks allowlist, so
this runs unmodified in CI.

For verification against Hermes's actual dispatch code path
(agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "destructive-command-guard.py"

CASES: list[tuple[str, dict, str | None]] = [
    ("benign command", {"tool_name": "terminal", "tool_input": {"command": "ls -la"}}, None),
    ("rm -rf /", {"tool_name": "terminal", "tool_input": {"command": "rm -rf /"}}, "block"),
    ("rm -rf ~", {"tool_name": "terminal", "tool_input": {"command": "rm -rf ~"}}, "block"),
    (
        "DROP TABLE",
        {"tool_name": "terminal", "tool_input": {"command": "psql -c 'DROP TABLE users;'"}},
        "block",
    ),
    (
        "kubectl delete --all",
        {"tool_name": "terminal", "tool_input": {"command": "kubectl delete pods --all"}},
        "block",
    ),
    (
        "bypass marker",
        {"tool_name": "terminal", "tool_input": {"command": "rm -rf / # hermes-bypass: destructive"}},
        None,
    ),
    (
        "wrong tool (read_file, not terminal)",
        {"tool_name": "read_file", "tool_input": {"file_path": "/etc/passwd"}},
        None,
    ),
    (
        "rm -rf on a normal project dir (not a protected path)",
        {"tool_name": "terminal", "tool_input": {"command": "rm -rf ./build"}},
        None,
    ),
]


def run_case(payload: dict) -> dict | None:
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    out = result.stdout.strip()
    if not out:
        return None
    return json.loads(out)


def main() -> int:
    failures = 0
    for label, payload, expect in CASES:
        parsed = run_case(payload)
        got = parsed.get("action") if parsed else None
        ok = got == expect
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:55} expect={expect!r} got={got!r}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
