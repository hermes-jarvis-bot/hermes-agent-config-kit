"""Stdlib-only smoke test for transfer-contract-guard.py's wire contract.

Covers all three event registrations: pre_tool_call (genuine block), post_tool_call
(audit-log-only, stderr), pre_verify/on_session_end (dual-registered, same pattern as
session-handoff-reminder.py/kb-validate-gate.py). No dependency on a live Hermes install or
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
import time as _time
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "transfer-contract-guard.py"

VALID_CONTRACT = {
    "schema_version": 1,
    "transfer_id": "2026-08-09_move-example",
    "status": "planned",
    "source": "/src/path",
    "destination": "/dest/path",
    "purpose": "test",
    "motivation": "test",
    "deadline": "2026-12-31T23:59:00+00:00",
    "operation": {"kind": "sync", "tool": "rsync", "settings": {"flags": []}},
    "verification": {"plan": ["destination exists"], "performed": False, "result": None, "evidence": []},
    "source_cleanup": {"planned": False, "performed": False, "verified": False, "reason": "keep until verified"},
    "next_action": "run the copy",
    "closure_reason": "",
}


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

    def check(label, payload, expect_stdout_substr, expect_stderr_substr) -> None:
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

    # pre_tool_call: genuine block
    check(
        "pre_tool_call: non-transfer command allowed",
        {"hook_event_name": "pre_tool_call", "tool_name": "terminal", "tool_input": {"command": "ls -la"}},
        None,
        None,
    )
    check(
        "pre_tool_call: wrong tool allowed",
        {"hook_event_name": "pre_tool_call", "tool_name": "write_file", "tool_input": {"path": "x"}},
        None,
        None,
    )
    check(
        "pre_tool_call: transfer command with no marker -> BLOCKED",
        {"hook_event_name": "pre_tool_call", "tool_name": "terminal", "tool_input": {"command": "rsync -a /a /b"}},
        "block",
        None,
    )

    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        contract_dir = cwd / ".hermes" / "transfers"
        contract_dir.mkdir(parents=True)
        contract_path = contract_dir / "test.json"
        contract_path.write_text(json.dumps(VALID_CONTRACT), encoding="utf-8")
        marker = f"# transfer-contract: .hermes/transfers/test.json"

        check(
            "pre_tool_call: transfer command with valid matching contract -> allowed",
            {
                "hook_event_name": "pre_tool_call",
                "cwd": str(cwd),
                "tool_name": "terminal",
                "tool_input": {"command": f"rsync -a /a /b {marker}"},
            },
            None,
            None,
        )

        wrong_kind = dict(VALID_CONTRACT)
        wrong_kind["operation"] = {"kind": "move", "tool": "rsync", "settings": {}}
        (contract_dir / "wrong.json").write_text(json.dumps(wrong_kind), encoding="utf-8")
        check(
            "pre_tool_call: contract operation.kind mismatch -> BLOCKED",
            {
                "hook_event_name": "pre_tool_call",
                "cwd": str(cwd),
                "tool_name": "terminal",
                "tool_input": {"command": "rsync -a /a /b # transfer-contract: .hermes/transfers/wrong.json"},
            },
            "block",
            None,
        )

        # post_tool_call: audit-log-only
        check(
            "post_tool_call: non-transfer command allowed",
            {"hook_event_name": "post_tool_call", "tool_name": "terminal", "tool_input": {"command": "ls"}},
            None,
            None,
        )
        check(
            "post_tool_call: transfer command reminds via stderr only",
            {
                "hook_event_name": "post_tool_call",
                "tool_name": "terminal",
                "tool_input": {"command": "rsync -a /a /b"},
                "extra": {"status": "ok"},
            },
            None,
            "verification_pending",
        )
        check(
            "post_tool_call: failed transfer command reminds with failed outcome",
            {
                "hook_event_name": "post_tool_call",
                "tool_name": "terminal",
                "tool_input": {"command": "rsync -a /a /b"},
                "extra": {"status": "error"},
            },
            None,
            "failed",
        )

    # pre_verify / on_session_end: dual-registered Stop-equivalent
    with tempfile.TemporaryDirectory() as empty_tmp:
        check(
            "pre_verify: no transfers dir -> silent",
            {"hook_event_name": "pre_verify", "cwd": str(empty_tmp)},
            None,
            None,
        )

    with tempfile.TemporaryDirectory() as tmp2:
        cwd2 = Path(tmp2)
        open_dir = cwd2 / ".hermes" / "transfers"
        open_dir.mkdir(parents=True)
        open_contract = dict(VALID_CONTRACT)
        open_contract["status"] = "running"
        (open_dir / "open.json").write_text(json.dumps(open_contract), encoding="utf-8")

        check(
            "pre_verify: open transfer -> live block on stdout",
            {"hook_event_name": "pre_verify", "cwd": str(cwd2)},
            "continue",
            None,
        )
        check(
            "on_session_end: open transfer -> audit-log only (stderr, no stdout)",
            {"hook_event_name": "on_session_end", "cwd": str(cwd2)},
            None,
            "transfer_contract",
        )

    # Session ownership (2026-08-10 fix): an open contract owned by a DIFFERENT, still-live
    # session is deferred (stderr note, not a block); one owned by no one, by the current
    # session, or by a stale (heartbeat-expired) session still blocks.
    with tempfile.TemporaryDirectory() as tmp3:
        cwd3 = Path(tmp3)
        hermes_dir = cwd3 / ".hermes"
        transfers = hermes_dir / "transfers"
        transfers.mkdir(parents=True)
        owned = dict(VALID_CONTRACT)
        owned["status"] = "running"
        owned["session_id"] = "other-session"
        (transfers / "owned.json").write_text(json.dumps(owned), encoding="utf-8")

        check(
            "pre_verify: open transfer owned by an UNKNOWN (never-heartbeat) session -> still blocks",
            {"hook_event_name": "pre_verify", "cwd": str(cwd3)},
            "continue",
            None,
        )

        # Give "other-session" a fresh heartbeat -> now it reads as live, and its open
        # contract should be deferred instead of blocking "my-session".
        (hermes_dir / "sessions" / "other-session").mkdir(parents=True)
        (hermes_dir / "sessions" / "other-session" / "heartbeat").touch()
        check(
            "pre_verify: open transfer owned by a LIVE foreign session -> deferred, not blocked",
            {"hook_event_name": "pre_verify", "cwd": str(cwd3), "session_id": "my-session"},
            None,
            "left to their owners",
        )
        check(
            "on_session_end: same live-foreign-owned transfer -> deferred note only",
            {"hook_event_name": "on_session_end", "cwd": str(cwd3), "session_id": "my-session"},
            None,
            "left to their owners",
        )

        # Make the owner's heartbeat stale -> its contract blocks again.
        stale_heartbeat = hermes_dir / "sessions" / "other-session" / "heartbeat"
        old = _time.time() - 1800 - 600
        os.utime(stale_heartbeat, (old, old))
        check(
            "pre_verify: same contract, owner's heartbeat now STALE -> blocks again",
            {"hook_event_name": "pre_verify", "cwd": str(cwd3), "session_id": "my-session"},
            "continue",
            None,
        )

        # The current session's OWN open contract always blocks it, regardless of liveness.
        mine = dict(VALID_CONTRACT)
        mine["status"] = "running"
        mine["session_id"] = "my-session"
        (transfers / "owned.json").unlink()
        (transfers / "mine.json").write_text(json.dumps(mine), encoding="utf-8")
        (hermes_dir / "sessions" / "my-session").mkdir(parents=True, exist_ok=True)
        (hermes_dir / "sessions" / "my-session" / "heartbeat").touch()
        check(
            "pre_verify: my own open contract blocks me even though I'm live",
            {"hook_event_name": "pre_verify", "cwd": str(cwd3), "session_id": "my-session"},
            "continue",
            None,
        )

    total += 1
    self_test_proc = subprocess.run([sys.executable, str(GUARD), "--self-test"], capture_output=True, text=True, timeout=15)
    ok = self_test_proc.returncode == 0 and "self-test: ok" in self_test_proc.stdout
    if not ok:
        failures += 1
    print(f"{'PASS' if ok else 'FAIL'}  {'--self-test mode (ownership rule on real files)':65} rc={self_test_proc.returncode} out={self_test_proc.stdout.strip()[-40:]!r}")

    total += 1
    spec_exit_check = run_case({"hook_event_name": "unknown_event"})
    ok = spec_exit_check.stdout.strip() == "" and spec_exit_check.stderr.strip() == ""
    if not ok:
        failures += 1
    print(f"{'PASS' if ok else 'FAIL'}  {'unknown event -> silent':65}")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
