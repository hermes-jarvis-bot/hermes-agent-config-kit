"""Stdlib-only smoke test for session-drift-validator.py's wire contract.

Real disposable project dir with a CLAUDE.md containing one resolvable path reference and one
stale one, checked against pre_llm_call/is_first_turn's context-injection shape.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "session-drift-validator.py"


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
        (cwd / "real_file.py").write_text("# real\n", encoding="utf-8")
        (cwd / "CLAUDE.md").write_text(
            "See ./real_file.py for the real thing.\n"
            "See ./ghost/module/missing.py for the missing thing.\n",
            encoding="utf-8",
        )

        result = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(cwd),
            "extra": {"is_first_turn": True},
        })
        check("drift found -> context injected", result.stdout.strip() != "", result.stdout)
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            check("mentions the stale path", "missing.py" in parsed.get("context", ""), parsed)
            check("does not flag the real path",
                  "real_file.py" not in parsed.get("context", "").split("Found stale")[-1]
                  if "Found stale" in parsed.get("context", "") else True)

        result_not_first = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(cwd),
            "extra": {"is_first_turn": False},
        })
        check("not first turn -> silent", result_not_first.stdout.strip() == "")

    with tempfile.TemporaryDirectory() as td2:
        clean_cwd = Path(td2)
        (clean_cwd / "real_file.py").write_text("# real\n", encoding="utf-8")
        (clean_cwd / "CLAUDE.md").write_text("See ./real_file.py for the real thing.\n", encoding="utf-8")
        result_clean = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(clean_cwd),
            "extra": {"is_first_turn": True},
        })
        check("no drift -> silent (no noise on a clean project)", result_clean.stdout.strip() == "")

    with tempfile.TemporaryDirectory() as td3:
        no_config_cwd = Path(td3)
        result_none = run_case({
            "hook_event_name": "pre_llm_call",
            "cwd": str(no_config_cwd),
            "extra": {"is_first_turn": True},
        })
        check("no CLAUDE.md/AGENTS.md/rules at all -> silent", result_none.stdout.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
