"""Stdlib-only smoke test for self-harm-guard.py's wire contract.

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

GUARD = Path(__file__).resolve().parents[1] / "self-harm-guard.py"

CASES: list[tuple[str, dict, str | None]] = [
    ("benign command", {"tool_name": "terminal", "tool_input": {"command": "ls -la"}}, None),
    (
        "restart sshd",
        {"tool_name": "terminal", "tool_input": {"command": "systemctl restart sshd"}},
        "block",
    ),
    (
        "pkill sshd",
        {"tool_name": "terminal", "tool_input": {"command": "pkill -f sshd"}},
        "block",
    ),
    (
        "killall python (own runtime)",
        {"tool_name": "terminal", "tool_input": {"command": "killall python"}},
        "block",
    ),
    (
        "pkill -f hermes_cli",
        {"tool_name": "terminal", "tool_input": {"command": "pkill -f hermes_cli"}},
        "block",
    ),
    (
        "ufw default deny incoming",
        {"tool_name": "terminal", "tool_input": {"command": "ufw default deny incoming"}},
        "block",
    ),
    ("bare reboot", {"tool_name": "terminal", "tool_input": {"command": "reboot"}}, "block"),
    (
        "reboot mentioned in a grep, not run",
        {"tool_name": "terminal", "tool_input": {"command": "grep reboot /var/log/syslog"}},
        None,
    ),
    (
        "write_file to sshd_config",
        {"tool_name": "write_file", "tool_input": {"file_path": "/etc/ssh/sshd_config"}},
        "block",
    ),
    (
        "patch on authorized_keys",
        {"tool_name": "patch", "tool_input": {"file_path": "/root/.ssh/authorized_keys"}},
        "block",
    ),
    (
        "bypass marker",
        {"tool_name": "terminal", "tool_input": {"command": "reboot # hermes-bypass: self-harm"}},
        None,
    ),
    (
        "wrong tool (read_file, not terminal/write_file/patch)",
        {"tool_name": "read_file", "tool_input": {"file_path": "/etc/ssh/sshd_config"}},
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
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:60} expect={expect!r} got={got!r}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
