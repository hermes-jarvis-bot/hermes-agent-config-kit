"""Stdlib-only smoke test for git-destructive-guard.py's wire contract.

Pipes synthetic pre_tool_call JSON directly to the script's stdin over a
subprocess and checks its stdout. No dependency on a live Hermes install,
~/.hermes/config.yaml, or the shell-hooks allowlist, so this runs unmodified
in CI. For verification against Hermes's actual dispatch code path
(agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "git-destructive-guard.py"

CASES: list[tuple[str, dict, str | None]] = [
    ("benign git status", {"tool_name": "terminal", "tool_input": {"command": "git status"}}, None),
    ("reset --hard", {"tool_name": "terminal", "tool_input": {"command": "git reset --hard HEAD~1"}}, "block"),
    ("push --force", {"tool_name": "terminal", "tool_input": {"command": "git push --force origin main"}}, "block"),
    (
        "push --force-with-lease is the recommended safe alternative",
        {"tool_name": "terminal", "tool_input": {"command": "git push --force-with-lease origin main"}},
        None,
    ),
    ("branch -D", {"tool_name": "terminal", "tool_input": {"command": "git branch -D feature-x"}}, "block"),
    (
        "branch -d (lowercase, safe merged-branch delete) is not blocked",
        {"tool_name": "terminal", "tool_input": {"command": "git branch -d feature-x"}},
        None,
    ),
    ("clean -fdx", {"tool_name": "terminal", "tool_input": {"command": "git clean -fdx"}}, "block"),
    ("filter-branch", {"tool_name": "terminal", "tool_input": {"command": "git filter-branch --tree-filter true"}}, "block"),
    (
        "bypass marker",
        {"tool_name": "terminal", "tool_input": {"command": "git reset --hard HEAD~1 # hermes-bypass: git-destructive"}},
        None,
    ),
    (
        "wrong tool (read_file, not terminal)",
        {"tool_name": "read_file", "tool_input": {"file_path": "/etc/passwd"}},
        None,
    ),
]


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


def main() -> int:
    failures = 0
    for label, payload, expect in CASES:
        parsed = run_case(payload)
        got = parsed.get("action") if parsed else None
        ok = got == expect
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} expect={expect!r} got={got!r}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
