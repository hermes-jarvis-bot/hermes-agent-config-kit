"""Stdlib-only smoke test for docs-staleness-guard.py's wire contract.

Pipes synthetic pre_llm_call JSON directly to the script's stdin over a subprocess and checks
its stdout ({"context": ...} JSON -- same genuinely-reaches-the-model event as
session-handoff-check.py). No dependency on a live Hermes install or ~/.hermes/config.yaml, so
this runs unmodified in CI. For verification against Hermes's actual dispatch code path
(agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml. The script's own `--self-test` mode (pure git/filesystem logic,
carried over unchanged from upstream, no wire-protocol dependency) is checked separately here
too since it is a real, independent verification surface this hook ships with.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "docs-staleness-guard.py"


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


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def main() -> int:
    failures = 0
    total = 0

    def check(label: str, payload: dict, expect_context_substr) -> None:
        nonlocal failures, total
        total += 1
        parsed = run_case(payload)
        got_context = parsed.get("context") if parsed else None
        if expect_context_substr is None:
            ok = parsed is None
        else:
            ok = bool(got_context) and expect_context_substr in got_context
        if not ok:
            failures += 1
        preview = (got_context[:60] + "...") if got_context else None
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} expect_substr={expect_context_substr!r} got={preview!r}")

    check("wrong event", {"hook_event_name": "pre_tool_call", "extra": {"is_first_turn": True}}, None)
    check(
        "pre_llm_call but not first turn",
        {"hook_event_name": "pre_llm_call", "extra": {"is_first_turn": False}},
        None,
    )
    check(
        "first turn, no repo (not even git) -> silent",
        {"hook_event_name": "pre_llm_call", "cwd": "/", "extra": {"is_first_turn": True}},
        None,
    )

    total += 1
    self_test = subprocess.run([sys.executable, str(GUARD), "--self-test"], capture_output=True, text=True, timeout=30)
    ok = self_test.returncode == 0 and "SELF-TEST: PASS" in self_test.stdout
    if not ok:
        failures += 1
    print(f"{'PASS' if ok else 'FAIL'}  {'--self-test mode (upstream pure-logic checks)':65} rc={self_test.returncode} out={self_test.stdout.strip()[-60:]!r}")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
