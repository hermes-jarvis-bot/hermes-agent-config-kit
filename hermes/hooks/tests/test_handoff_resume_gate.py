"""Stdlib-only smoke test for handoff-resume-gate.py's wire contract.

The hook's own --self-test already covers the staleness-classification logic in depth; this
covers the pre_llm_call/is_first_turn wire contract (context injection shape, event filtering)
against a real .hermes/handoffs/<project>/*.md tree in a disposable tempdir.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "handoff-resume-gate.py"


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

    self_test = subprocess.run(
        [sys.executable, str(GUARD), "--self-test"], capture_output=True, text=True, timeout=10
    )
    check("hook's own --self-test passes", self_test.returncode == 0, self_test.stdout)

    with tempfile.TemporaryDirectory() as td:
        cwd = Path(td)
        proj_dir = cwd / ".hermes" / "handoffs" / "myproj"
        proj_dir.mkdir(parents=True)
        stale_day = time.strftime("%Y-%m-%d", time.localtime(time.time() - 6 * 86400))
        (proj_dir / f"{stale_day}_10-00_aaaa.md").write_text(
            "# Handoff\n**Status:** ACTIVE\n## Current state\n- server up at 1.2.3.4\n",
            encoding="utf-8",
        )

        result = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(cwd),
            "extra": {"is_first_turn": True},
        })
        check("stale handoff -> context injected", result.stdout.strip() != "", result.stdout)
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            check("emitted as {\"context\": ...}", "context" in parsed, parsed)
            check("mentions the stale project", "myproj" in parsed.get("context", ""), parsed)

        result_not_first = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(cwd),
            "extra": {"is_first_turn": False},
        })
        check("not first turn -> silent", result_not_first.stdout.strip() == "")

        result_wrong_event = run_case({
            "hook_event_name": "pre_tool_call",
            "cwd": str(cwd),
            "extra": {"is_first_turn": True},
        })
        check("wrong event -> silent", result_wrong_event.stdout.strip() == "")

    with tempfile.TemporaryDirectory() as td2:
        empty_cwd = Path(td2)
        result_empty = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(empty_cwd),
            "extra": {"is_first_turn": True},
        })
        check("no handoffs at all -> silent", result_empty.stdout.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
