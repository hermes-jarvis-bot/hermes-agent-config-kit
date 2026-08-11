"""Stdlib-only smoke test for long-run-detector.py's wire contract.

The hook's own --self-test already covers the signal-detection/hub-exemption logic in depth;
this covers the pre_llm_call/is_first_turn wire contract and the cooldown stamp.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "long-run-detector.py"


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
        hdir = cwd / ".hermes" / "handoffs" / "alpha"
        hdir.mkdir(parents=True)
        for i in range(3):
            (hdir / f"2026-06-1{i}_10-00_abc1234{i}.md").write_text("h", encoding="utf-8")

        result = run_case({"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": True}})
        check("long-run signals -> context injected", result.stdout.strip() != "", result.stdout)
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            check("mentions LONG-RUN candidate", "LONG-RUN" in parsed.get("context", ""))

        check("cooldown stamp file was written", (cwd / ".hermes" / ".longrun-nudged").exists())

        result_again = run_case({"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": True}})
        check("second call within cooldown -> silent", result_again.stdout.strip() == "")

        result_not_first = run_case({"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": False}})
        check("not first turn -> silent", result_not_first.stdout.strip() == "")

    with tempfile.TemporaryDirectory() as td2:
        adopted = Path(td2)
        (adopted / ".hermes").mkdir()
        (adopted / "feature_list.json").write_text("{}", encoding="utf-8")
        result_adopted = run_case({"hook_event_name": "pre_llm_call", "cwd": str(adopted), "extra": {"is_first_turn": True}})
        check("already-adopted project -> silent", result_adopted.stdout.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
