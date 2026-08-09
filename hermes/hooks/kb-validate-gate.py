#!/usr/bin/env python3
"""pre_verify + on_session_end: block session close while the knowledge base is out of sync.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's hooks/kb-validate-gate.py
(reimplemented from the upstream Stop hook, see mappings/reviewed-hooks.yaml).

Same dual-registration design as session-handoff-reminder.py, for the same underlying reason:
Hermes has no Stop-equivalent firing on every turn-end attempt regardless of what happened.
`pre_verify` gives a genuine live block (its {"action":"continue","message":...} return
reaches the model), gated on `if _edited and has_hook("pre_verify") and _attempt <
max_verify_nudges()` (conversation_loop.py:7109) -- file-edit turns only, capped at 3 nudges
for the WHOLE session, a budget shared with session-handoff-reminder.py and any other
pre_verify consumer. `on_session_end` fires every turn but discards its return
(audit-log-only).

OPERATOR-APPROVED DESIGN (2026-08-09): register on both, accepting the shared pre_verify
budget as-is -- unlike session-handoff-reminder.py (fires once per session, then stays
silent), this hook is willing to fire on EVERY eligible turn while the KB stays broken
(matching upstream, which relies on its own per-hook-name budget for that -- dropped here,
see below), so in the rare worst case (KB genuinely broken AND a long session with no fresh
handoff, both true on overlapping turns) it could consume the whole shared budget and starve
session-handoff-reminder.py's live nudge for the rest of that session. Both are still
dual-registered with on_session_end, so nothing is ever silently lost -- worst case is one
loses its LIVE nudge for a session, not its audit-log entry.

Dropped from upstream: `stop_hook_active`/`stop_budget_consume`/`stop_budget_exhausted`
(safety_common's own per-hook-name anti-loop budget) -- redundant here. Hermes's own
session-wide `attempt`/`max_verify_nudges()` cap at the engine level already serves the exact
same anti-loop purpose (same reasoning already applied when porting the shared
hermes_hook_common.py module: "Hermes's pre_verify event does not have the same
re-invocation-loop shape, so the mechanism it exists to guard against does not apply here").
Kept `untrusted_block()` (now in hermes_hook_common.py) -- an orthogonal, still-relevant
safety practice: the repo's own validate_kb.py output lands in the model's context as a block
message, so it is framed as data, not instructions, before being surfaced.

## Behaviour (stdin = pre_verify/on_session_end event JSON)
- Tier 2b (force docs to EXIST): a [LONG-RUN] project (feature_list.json present) with NO
  agent docs at all (docs/kb/ and docs/layers/ both absent) and no validator -> block/log; a
  long-run project must maintain a KB.
- Tier 2 (force docs to stay CURRENT): scripts/validate_kb.py exits 1 -> block/log with its
  output as the reason.
- No scripts/validate_kb.py + not [LONG-RUN] -> silent pass (opt-in).
- validate_kb.py exits 0 (clean), or exits 2/crashes/times out (infra issue, not a KB-drift
  signal) -> silent pass, fail-open.

## Bypass
- env  HERMES_SKIP_KB_GATE=1
- file .hermes/.skip-kb-gate  (project-level)

## Self-test (unchanged logic from upstream, no Hermes wire-protocol dependency)
    python3 kb-validate-gate.py --self-test
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import untrusted_block  # noqa: E402

VALIDATOR_REL = ("scripts", "validate_kb.py")
TIMEOUT_SEC = 25
MAX_REASON_CHARS = 1500


def _validator_path(cwd: Path) -> Path:
    return cwd.joinpath(*VALIDATOR_REL)


def _run_validator(cwd: Path):
    """Return (returncode, output). returncode None on infra failure."""
    script = _validator_path(cwd)
    try:
        out = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
        )
        return out.returncode, (out.stderr or out.stdout or "")
    except Exception as e:  # noqa: BLE001 -- any failure = fail-open infra path
        return None, str(e)


def _is_longrun(cwd: Path) -> bool:
    """A project that explicitly opted into the long-run harness."""
    return (cwd / "feature_list.json").exists() or (
        cwd / ".hermes" / "feature_list.json"
    ).exists()


def _has_agent_docs(cwd: Path) -> bool:
    return (cwd / "docs" / "kb").is_dir() or (cwd / "docs" / "layers").is_dir()


def evaluate(cwd: Path) -> str | None:
    """Pure decision: return a full block-reason string, or None to allow."""
    validator = _validator_path(cwd)

    if _is_longrun(cwd) and not _has_agent_docs(cwd) and not validator.exists():
        return (
            "This project is [LONG-RUN] (feature_list.json) but carries NO agent "
            "docs: docs/kb/ and docs/layers/ are both absent. A long-run project "
            "must maintain a knowledge base. Scaffold the kb-skeleton (docs/kb/ + "
            "scripts/validate_kb.py) or start a docs/layers/ tree before ending."
        )

    if not validator.exists():
        return None
    rc, output = _run_validator(cwd)
    if rc != 1:
        return None
    body = (output or "").strip() or "validate_kb.py reported the KB is out of sync."
    if len(body) > MAX_REASON_CHARS:
        body = body[:MAX_REASON_CHARS] + "\n  ... (truncated)"
    body = untrusted_block(body, "repository scripts/validate_kb.py stdout")
    return (
        "Knowledge base is out of sync with the code -- scripts/validate_kb.py "
        "failed. Fix the kb doc or the code reference before ending the session "
        "(local mirror of the CI gate).\n\n" + body
    )


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()

    try:
        raw = sys.stdin.read().lstrip("﻿").strip()
        event = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, OSError):
        return 0

    hook_event = event.get("hook_event_name")
    if hook_event not in ("pre_verify", "on_session_end"):
        return 0
    if os.environ.get("HERMES_SKIP_KB_GATE"):
        return 0

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    if (cwd / ".hermes" / ".skip-kb-gate").exists():
        return 0

    reason_body = evaluate(cwd)
    if reason_body is None:
        return 0

    reason = reason_body + (
        "\n\nBypass: HERMES_SKIP_KB_GATE=1  or  touch .hermes/.skip-kb-gate"
    )

    if hook_event == "pre_verify":
        print(json.dumps({"action": "continue", "message": reason}, ensure_ascii=False))
    else:
        # on_session_end: return value is discarded by Hermes -- audit-log-only. stderr kept
        # for potential visibility via Hermes's own logger.
        from hermes_hook_common import log

        log("WARN", "kb_validate_gate", "blocked", hook_event, reason[:200])
        sys.stderr.write(f"[kb_validate_gate] {reason}\n")
    return 0


def _self_test() -> int:
    import tempfile

    ok = True
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad"
        (bad / "scripts").mkdir(parents=True)
        _validator_path(bad).write_text(
            "import sys\n"
            "print('KB validation FAILED: references missing path `gone.py`', file=sys.stderr)\n"
            "sys.exit(1)\n",
            encoding="utf-8",
        )
        r = evaluate(bad)
        if not r or "FAILED" not in r:
            print("SELF-TEST FAIL: failing KB validator did not block")
            ok = False

        good = Path(td) / "good"
        (good / "scripts").mkdir(parents=True)
        _validator_path(good).write_text(
            "import sys\nprint('[OK] KB consistent.')\nsys.exit(0)\n", encoding="utf-8"
        )
        if evaluate(good) is not None:
            print("SELF-TEST FAIL: passing KB validator wrongly blocked")
            ok = False

        none = Path(td) / "none"
        none.mkdir()
        if evaluate(none) is not None:
            print("SELF-TEST FAIL: repo without validator should pass")
            ok = False

        infra = Path(td) / "infra"
        (infra / "scripts").mkdir(parents=True)
        _validator_path(infra).write_text(
            "import sys\nprint('missing docs/kb/', file=sys.stderr)\nsys.exit(2)\n",
            encoding="utf-8",
        )
        if evaluate(infra) is not None:
            print("SELF-TEST FAIL: exit-2 infra error should fail-open")
            ok = False

        lr = Path(td) / "longrun_nodocs"
        lr.mkdir()
        (lr / "feature_list.json").write_text('{"features": []}', encoding="utf-8")
        r2b = evaluate(lr)
        if not r2b or "LONG-RUN" not in r2b:
            print("SELF-TEST FAIL: long-run project without docs not blocked")
            ok = False

        lrok = Path(td) / "longrun_withdocs"
        (lrok / "docs" / "kb").mkdir(parents=True)
        (lrok / "feature_list.json").write_text('{"features": []}', encoding="utf-8")
        if evaluate(lrok) is not None:
            print("SELF-TEST FAIL: long-run project WITH docs wrongly blocked")
            ok = False

        plain = Path(td) / "plain_nodocs"
        plain.mkdir()
        if evaluate(plain) is not None:
            print("SELF-TEST FAIL: non-long-run repo without docs should pass")
            ok = False

    print("SELF-TEST: PASS" if ok else "SELF-TEST: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
