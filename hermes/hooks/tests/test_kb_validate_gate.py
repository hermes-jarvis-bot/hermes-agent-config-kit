"""Stdlib-only smoke test for kb-validate-gate.py's wire contract.

Pipes synthetic pre_verify/on_session_end JSON directly to the script's stdin over a
subprocess and checks its stdout (pre_verify only) and stderr (on_session_end, audit-log-only
-- see the script's own docstring). No dependency on a live Hermes install or
~/.hermes/config.yaml, so this runs unmodified in CI. For verification against Hermes's actual
dispatch code path (agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml. The script's own `--self-test` mode (pure evaluate() logic,
carried over unchanged from upstream) is checked separately here too.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "kb-validate-gate.py"


def run_case(payload: dict, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop("HERMES_SKIP_KB_GATE", None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )


def main() -> int:
    failures = 0
    total = 0

    def check(label, payload, expect_stdout_substr, expect_stderr_substr, env_extra=None) -> None:
        nonlocal failures, total
        total += 1
        result = run_case(payload, env_extra)
        ok = True
        if expect_stdout_substr is None:
            ok &= result.stdout.strip() == ""
        else:
            ok &= expect_stdout_substr in result.stdout
        if expect_stderr_substr is None:
            ok &= result.stderr.strip() == ""
        else:
            ok &= expect_stderr_substr in result.stderr
        if not ok:
            failures += 1
        print(
            f"{'PASS' if ok else 'FAIL'}  {label!r:65} "
            f"stdout={result.stdout.strip()[:50]!r} stderr={result.stderr.strip()[:50]!r}"
        )

    check("wrong event", {"hook_event_name": "pre_tool_call"}, None, None)

    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        check(
            "no validator, not long-run -> silent",
            {"hook_event_name": "pre_verify", "cwd": str(cwd)},
            None,
            None,
        )

        scripts_dir = cwd / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "validate_kb.py").write_text(
            "import sys\nprint('KB validation FAILED: dead path', file=sys.stderr)\nsys.exit(1)\n",
            encoding="utf-8",
        )
        check(
            "failing validator, pre_verify -> live block on stdout",
            {"hook_event_name": "pre_verify", "cwd": str(cwd)},
            "FAILED",
            None,
        )
        check(
            "failing validator, on_session_end -> audit-log only (stderr, no stdout)",
            {"hook_event_name": "on_session_end", "cwd": str(cwd)},
            None,
            "FAILED",
        )
        check(
            "env bypass HERMES_SKIP_KB_GATE=1",
            {"hook_event_name": "pre_verify", "cwd": str(cwd)},
            None,
            None,
            env_extra={"HERMES_SKIP_KB_GATE": "1"},
        )

        (cwd / ".hermes").mkdir()
        (cwd / ".hermes" / ".skip-kb-gate").write_text("x", encoding="utf-8")
        check(
            "file bypass .hermes/.skip-kb-gate",
            {"hook_event_name": "pre_verify", "cwd": str(cwd)},
            None,
            None,
        )

    with tempfile.TemporaryDirectory() as tmp2:
        cwd2 = Path(tmp2)
        (cwd2 / "feature_list.json").write_text('{"features": []}', encoding="utf-8")
        check(
            "long-run project with no agent docs and no validator -> blocks",
            {"hook_event_name": "pre_verify", "cwd": str(cwd2)},
            "LONG-RUN",
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
