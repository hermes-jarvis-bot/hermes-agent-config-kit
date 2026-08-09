"""Stdlib-only smoke test for session-handoff-check.py's wire contract.

Pipes synthetic pre_llm_call JSON directly to the script's stdin over a subprocess and checks
its stdout ({"context": ...} JSON, the one Hermes event proven to actually reach the model --
see the script's own docstring). No dependency on a live Hermes install or ~/.hermes/config.yaml,
so this runs unmodified in CI. For verification against Hermes's actual dispatch code path
(agent.shell_hooks.run_once), see the functional_test evidence recorded in
mappings/reviewed-hooks.yaml.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "session-handoff-check.py"


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
    total = 0

    def check(label: str, payload: dict, expect_context_substr: str | None) -> None:
        nonlocal failures, total
        total += 1
        parsed = run_case(payload)
        got_context = parsed.get("context") if parsed else None
        if expect_context_substr is None:
            ok = parsed is None
        else:
            ok = bool(got_context) and expect_context_substr in got_context
        if not ok:
            failures += 1
        preview = (got_context[:60] + "...") if got_context else None
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} expect_substr={expect_context_substr!r} got={preview!r}")

    check("wrong event", {"hook_event_name": "pre_tool_call", "extra": {"is_first_turn": True}}, None)
    check(
        "pre_llm_call but not first turn",
        {"hook_event_name": "pre_llm_call", "extra": {"is_first_turn": False}},
        None,
    )

    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        check(
            "first turn, no handoffs yet",
            {"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": True}},
            None,
        )
        assert (cwd / ".hermes" / ".session-start").exists(), "session marker should be touched"

        handoffs = cwd / ".hermes" / "handoffs" / "myproj"
        handoffs.mkdir(parents=True)
        from datetime import datetime

        fresh_name = datetime.now().strftime("%Y-%m-%d_%H-%M") + "_abcd1234.md"
        (handoffs / fresh_name).write_text("# Handoff\n\nSome state.\n")
        reminded = cwd / ".hermes" / ".handoff-reminded"
        reminded.write_text("x")

        check(
            "first turn, one handoff present -> injected as context",
            {"hook_event_name": "pre_llm_call", "cwd": str(cwd), "extra": {"is_first_turn": True}},
            "SESSION HANDOFF(S)",
        )
        assert not reminded.exists(), "stale .handoff-reminded marker should be cleared on first turn"

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
