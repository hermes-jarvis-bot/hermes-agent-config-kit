"""Stdlib-only smoke test for handoff-closure-audit-guard.py's wire contract."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "handoff-closure-audit-guard.py"

COMPLETE_HANDOFF = """# Handoff

## Closure Audit
- Primary request status: COMPLETE
- Acceptance/checklist verified: tests pass
- Related/scope-adjacent tasks checked: yes
- Unfinished related tasks: NONE
- Why not continuing now: NONE
"""

INCOMPLETE_HANDOFF = """# Handoff

Some notes but no closure audit at all.
"""


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
        handoff_dir = Path(td) / ".hermes" / "handoffs" / "myproj"
        handoff_dir.mkdir(parents=True)
        handoff_path = str(handoff_dir / "2026-08-11_10-00_aaaa.md")

        check("non-handoff path -> pass through",
              run_case({"tool_name": "write_file", "tool_input": {"path": str(Path(td) / "x.py"), "content": "x"}}).stdout.strip() == "")

        check("wrong tool -> pass through",
              run_case({"tool_name": "terminal", "tool_input": {"command": "ls"}}).stdout.strip() == "")

        r = run_case({"tool_name": "write_file", "tool_input": {"path": handoff_path, "content": INCOMPLETE_HANDOFF}})
        check("write with no Closure Audit -> blocked", r.stdout.strip() != "")
        if r.stdout.strip():
            parsed = json.loads(r.stdout)
            check("block shape", parsed.get("action") == "block")
            check("names the missing section", "Closure Audit" in parsed.get("message", ""))

        check("write with a complete Closure Audit -> allowed",
              run_case({"tool_name": "write_file", "tool_input": {"path": handoff_path, "content": COMPLETE_HANDOFF}}).stdout.strip() == "")

        bypassed = INCOMPLETE_HANDOFF + "\n<!-- hermes-bypass: incomplete-handoff -->\n"
        check("bypass marker suppresses the block",
              run_case({"tool_name": "write_file", "tool_input": {"path": handoff_path, "content": bypassed}}).stdout.strip() == "")

        index_path = str(handoff_dir / "INDEX.md")
        check("INDEX.md is exempt",
              run_case({"tool_name": "write_file", "tool_input": {"path": index_path, "content": INCOMPLETE_HANDOFF}}).stdout.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
