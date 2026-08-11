"""Stdlib-only smoke test for task-inbox-show.py's wire contract."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "task-inbox-show.py"


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
        cwd = Path(td)
        inbox = cwd / ".hermes" / "task-inbox"
        inbox.mkdir(parents=True)
        (inbox / "1.json").write_text(
            json.dumps({"task_id": 42, "title": "Fix auth race", "priority": 3, "labels": ["ai-ready"]}),
            encoding="utf-8",
        )
        (inbox / "2.json").write_text(
            json.dumps({"task_id": 7, "title": "Low priority cleanup", "priority": 0}),
            encoding="utf-8",
        )

        result = run_case({"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": True}})
        check("inbox present -> context injected", result.stdout.strip() != "", result.stdout)
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            check("mentions the high-priority task", "Fix auth race" in parsed.get("context", ""))
            check("high priority sorted first",
                  parsed["context"].index("Fix auth race") < parsed["context"].index("Low priority cleanup"))

        result_not_first = run_case({"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": False}})
        check("not first turn -> silent", result_not_first.stdout.strip() == "")

    with tempfile.TemporaryDirectory() as td2:
        empty_cwd = Path(td2)
        result_empty = run_case({"hook_event_name": "pre_llm_call", "cwd": str(empty_cwd), "extra": {"is_first_turn": True}})
        check("no inbox at all -> silent", result_empty.stdout.strip() == "")

    with tempfile.TemporaryDirectory() as td3:
        claude_cwd = Path(td3)
        claude_inbox = claude_cwd / ".claude" / "linear-inbox"
        claude_inbox.mkdir(parents=True)
        (claude_inbox / "1.json").write_text(json.dumps({"task_id": 5, "title": "Legacy convention task"}), encoding="utf-8")
        result_legacy = run_case({"hook_event_name": "pre_llm_call", "cwd": str(claude_cwd), "extra": {"is_first_turn": True}})
        check("cross-harness .claude/ inbox is also recognized",
              result_legacy.stdout.strip() != "" and "Legacy convention task" in result_legacy.stdout)

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
