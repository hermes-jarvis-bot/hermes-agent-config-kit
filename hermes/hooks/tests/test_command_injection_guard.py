"""Stdlib-only smoke test for command-injection-guard.py's wire contract.

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

GUARD = Path(__file__).resolve().parents[1] / "command-injection-guard.py"
DROPDB_SUBST = 'gh issue create --body "$(' + "dropdb prod" + ')"'
RM_SUBST = 'echo "result: $(' + "rm -rf /tmp/x" + ')" > log.txt'

CASES: list[tuple[str, dict, str | None]] = [
    ("benign command, no substitution", {"tool_name": "terminal", "tool_input": {"command": "ls -la"}}, None),
    (
        "trivial substitution $(pwd)",
        {"tool_name": "terminal", "tool_input": {"command": 'echo "cwd: $(pwd)"'}},
        None,
    ),
    (
        "trivial substitution $(git rev-parse HEAD)",
        {"tool_name": "terminal", "tool_input": {"command": 'echo "$(git rev-parse HEAD)"'}},
        None,
    ),
    ("destructive substitution: dropdb smuggled via $()", {"tool_name": "terminal", "tool_input": {"command": DROPDB_SUBST}}, "block"),
    ("destructive substitution: rm -rf smuggled via $()", {"tool_name": "terminal", "tool_input": {"command": RM_SUBST}}, "block"),
    (
        "non-trivial but non-destructive substitution",
        {"tool_name": "terminal", "tool_input": {"command": 'echo "$(curl -s https://example.com)"'}},
        "block",
    ),
    (
        "literal $() inside single quotes is not a real substitution",
        {"tool_name": "terminal", "tool_input": {"command": "echo '$(dropdb prod)'"}},
        None,
    ),
    (
        "bypass marker",
        {"tool_name": "terminal", "tool_input": {"command": DROPDB_SUBST + " # hermes-bypass: injection"}},
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
