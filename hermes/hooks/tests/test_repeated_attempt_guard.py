"""Stdlib-only smoke test for repeated-attempt-guard.py's wire contract.

The hook's own --self-test already covers the retry-key/failure-detection logic in depth (see
`python3 repeated-attempt-guard.py --self-test`); this covers the actual pre_tool_call/
post_tool_call dispatch shape across real subprocess calls, with HERMES_RETRY_STATE pointed at
an isolated tempfile so this never touches ~/.hermes/state/attempts.jsonl.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "repeated-attempt-guard.py"


def run_case(payload: dict, state_path: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["HERMES_RETRY_STATE"] = state_path
    env.pop("HERMES_ALLOW_RETRY_LOOP", None)
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
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

    self_test = subprocess.run(
        [sys.executable, str(GUARD), "--self-test"], capture_output=True, text=True, timeout=15
    )
    check("hook's own --self-test passes", self_test.returncode == 0, self_test.stdout[-200:])

    with tempfile.TemporaryDirectory() as td:
        state = str(Path(td) / "attempts.jsonl")
        cmd_payload_ok = {
            "hook_event_name": "pre_tool_call",
            "tool_name": "terminal",
            "tool_input": {"command": "python build.py"},
        }

        check("clean state: first attempt is allowed silently",
              run_case(cmd_payload_ok, state).stdout.strip() == "")

        def record_failure() -> None:
            run_case({
                "hook_event_name": "post_tool_call",
                "tool_name": "terminal",
                "tool_input": {"command": "python build.py"},
                "extra": {"status": "error"},
            }, state)

        record_failure()
        record_failure()
        r = run_case(cmd_payload_ok, state)
        check("2 failures: advisory on stderr, not a block",
              r.stdout.strip() == "" and "guess" in r.stderr, r.stderr)

        record_failure()
        r = run_case(cmd_payload_ok, state)
        check("3 failures, nothing read: 4th attempt is blocked", r.stdout.strip() != "")
        if r.stdout.strip():
            parsed = json.loads(r.stdout)
            check("block shape", parsed.get("action") == "block", parsed)

        run_case({
            "hook_event_name": "post_tool_call",
            "tool_name": "read_file",
            "tool_input": {"file_path": "build.py"},
            "extra": {"status": "ok"},
        }, state)
        r2 = run_case(cmd_payload_ok, state)
        check("a read since the last failure clears the block", r2.stdout.strip() == "")

        r3 = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps(cmd_payload_ok),
            capture_output=True, text=True, timeout=10,
            env={**os.environ, "HERMES_RETRY_STATE": state, "HERMES_ALLOW_RETRY_LOOP": "1"},
        )
        check("global bypass env var suppresses the guard entirely", r3.stdout.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
