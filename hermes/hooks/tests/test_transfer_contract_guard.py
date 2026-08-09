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
import subprocess
import sys
import tempfile
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
