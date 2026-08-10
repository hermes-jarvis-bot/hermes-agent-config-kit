"""Stdlib-only smoke test for session-handoff-reminder.py's wire contract.

Pipes synthetic pre_verify/on_session_end JSON directly to the script's stdin over a
subprocess and checks its stdout (pre_verify only -- Hermes genuinely consumes
{"action":"continue",...} there) and stderr (on_session_end -- audit-log-only, see the
script's own docstring for why). No dependency on a live Hermes install or
~/.hermes/config.yaml, so this runs unmodified in CI. For verification against Hermes's actual
dispatch code path (agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "session-handoff-reminder.py"


def run_case(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )


def backdate(path: Path, minutes_ago: float) -> None:
    ts = time.time() - minutes_ago * 60
    os.utime(path, (ts, ts))


def main() -> int:
    failures = 0
    total = 0

    def check(label: str, payload: dict, expect_stdout_substr, expect_stderr_substr) -> subprocess.CompletedProcess:
        nonlocal failures, total
        total += 1
        result = run_case(payload)
        ok = True
        if expect_stdout_substr is None:
            ok &= result.stdout.strip() == ""
        else:
            ok &= expect_stdout_substr in result.stdout
        if expect_stderr_substr is None:
            ok &= result.stderr.strip() == ""
        else:
            ok &= expect_stderr_substr in result.stderr
        if not ok:
            failures += 1
        print(
            f"{'PASS' if ok else 'FAIL'}  {label!r:65} "
            f"stdout={result.stdout.strip()[:50]!r} stderr={result.stderr.strip()[:50]!r}"
        )
        return result

    check("wrong event", {"hook_event_name": "pre_tool_call"}, None, None)

    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        sid = "sess-x"
        check(
            "no .hermes dir at all -> not a Hermes project",
            {"hook_event_name": "on_session_end", "cwd": str(cwd), "session_id": sid},
            None,
            None,
        )

        hermes_dir = cwd / ".hermes"
        hermes_dir.mkdir()
        check(
            "no session marker yet -> touches it, no reminder",
            {"hook_event_name": "on_session_end", "cwd": str(cwd), "session_id": sid},
            None,
            None,
        )
        session_marker = hermes_dir / "sessions" / sid / "session-start"
        assert session_marker.exists(), "session-scoped marker should have been created"
        assert (hermes_dir / "sessions" / sid / "heartbeat").exists(), "heartbeat should be touched"

        check(
            "session too young (<15 min)",
            {"hook_event_name": "on_session_end", "cwd": str(cwd), "session_id": sid},
            None,
            None,
        )

        backdate(session_marker, 20)
        check(
            "old enough, no fresh handoff, pre_verify -> live nudge on stdout",
            {"hook_event_name": "pre_verify", "cwd": str(cwd), "session_id": sid},
            "continue",
            None,
        )
        reminder_marker = hermes_dir / "sessions" / sid / "handoff-reminded"
        assert reminder_marker.exists(), "reminder marker should be set after nudging"

        check(
            "already reminded this session -> silent even though still eligible",
            {"hook_event_name": "pre_verify", "cwd": str(cwd), "session_id": sid},
            None,
            None,
        )
        reminder_marker.unlink()

        check(
            "old enough, no fresh handoff, on_session_end -> audit-log only (stderr, no stdout)",
            {"hook_event_name": "on_session_end", "cwd": str(cwd), "session_id": sid},
            None,
            "handoff",
        )
        reminder_marker.unlink()

        handoffs = hermes_dir / "handoffs" / "myproj"
        handoffs.mkdir(parents=True)
        fresh_name = datetime.now().strftime("%Y-%m-%d_%H-%M") + "_abcd1234.md"
        (handoffs / fresh_name).write_text("fresh handoff")
        check(
            "fresh handoff exists -> silent despite old session",
            {"hook_event_name": "pre_verify", "cwd": str(cwd), "session_id": sid},
            None,
            None,
        )

    # Session-scoping (2026-08-10 fix): a second, brand-new session in the same project must
    # get its own fresh baseline -- not silenced by session sid's already-old marker, and not
    # able to clear sid's reminded marker either.
    with tempfile.TemporaryDirectory() as tmp2:
        cwd2 = Path(tmp2)
        (cwd2 / ".hermes").mkdir()
        sid_a, sid_b = "sess-a", "sess-b"
        run_case({"hook_event_name": "on_session_end", "cwd": str(cwd2), "session_id": sid_a})
        a_marker = cwd2 / ".hermes" / "sessions" / sid_a / "session-start"
        backdate(a_marker, 20)
        run_case({"hook_event_name": "pre_verify", "cwd": str(cwd2), "session_id": sid_a})
        a_reminded = cwd2 / ".hermes" / "sessions" / sid_a / "handoff-reminded"
        assert a_reminded.exists(), "session A should have been reminded"

        check(
            "brand-new session B in the same project -> not silenced by A's state, no reminder yet",
            {"hook_event_name": "on_session_end", "cwd": str(cwd2), "session_id": sid_b},
            None,
            None,
        )
        total += 1
        ok = a_reminded.exists()
        if not ok:
            failures += 1
        label = "session B's first call does not clear session A's reminded marker"
        print(f"{'PASS' if ok else 'FAIL'}  {label:65}")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
