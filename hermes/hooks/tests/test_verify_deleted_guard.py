"""Stdlib-only smoke test for verify-deleted-guard.py's wire contract.

Pipes synthetic post_tool_call JSON directly to the script's stdin over a subprocess and
checks its stderr (this hook is audit-log-only per its own header comment -- it never emits
stdout JSON, since Hermes discards a post_tool_call hook's return value regardless of what it
prints). No dependency on a live Hermes install or ~/.hermes/config.yaml, so this runs
unmodified in CI. For verification against Hermes's actual dispatch code path
(agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "verify-deleted-guard.py"


def build_cases(existing: str, missing: str) -> list[tuple[str, dict, str | None]]:
    return [
        (
            "non-destructive command",
            {"tool_name": "terminal", "tool_input": {"command": "ls -la"}},
            None,
        ),
        (
            "wrong tool (write_file, not terminal)",
            {"tool_name": "write_file", "tool_input": {"path": "/tmp/x", "content": "y"}},
            None,
        ),
        (
            "rm on a target that still exists -> still-present",
            {"tool_name": "terminal", "tool_input": {"command": f"rm {existing}"}},
            "STILL PRESENT",
        ),
        (
            "rm on a target that is gone -> verified-deleted",
            {"tool_name": "terminal", "tool_input": {"command": f"rm {missing}"}},
            "verified deletion",
        ),
        (
            "blocked call is skipped entirely (Hermes analog of upstream's interrupted)",
            {
                "tool_name": "terminal",
                "tool_input": {"command": f"rm {existing}"},
                "extra": {"status": "blocked"},
            },
            None,
        ),
        (
            "recognized destructive intent with no verify strategy",
            {"tool_name": "terminal", "tool_input": {"command": "kill -9 99999"}},
            "no auto-verify strategy",
        ),
        (
            "mv source that still exists -> still-present",
            {"tool_name": "terminal", "tool_input": {"command": f"mv {existing} /tmp/dest"}},
            "STILL PRESENT",
        ),
        (
            "mv source that is gone -> verified-deleted",
            {"tool_name": "terminal", "tool_input": {"command": f"mv {missing} /tmp/dest"}},
            "verified deletion",
        ),
    ]


def run_case(payload: dict) -> str:
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stderr


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        existing = str(Path(tmp) / "still-here.txt")
        Path(existing).write_text("x")
        missing = str(Path(tmp) / "definitely-not-here.txt")
        for label, payload, expect_substr in build_cases(existing, missing):
            stderr = run_case(payload)
            if expect_substr is None:
                ok = stderr.strip() == ""
                got = stderr.strip() or "(empty)"
            else:
                ok = expect_substr in stderr
                got = stderr.strip() or "(empty)"
            if not ok:
                failures += 1
            print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} expect={expect_substr!r} got={got!r}")
    total = len(build_cases("x", "y"))
    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
