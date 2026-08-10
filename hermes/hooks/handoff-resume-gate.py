#!/usr/bin/env python3
"""pre_llm_call (is_first_turn only): flag STALE handoffs as a "verify before trusting" nudge.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/handoff-resume-gate.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

session-handoff-check.py *shows* recent handoffs. This complements it by flagging STALE ones: a
handoff older than STALE_DAYS that is still ACTIVE is a trap -- a resuming session trusts
assumptions ("VM up", "branch X is canon") that may have rotted since. It does not re-show
content; it emits a short "verify before trusting" nudge listing the exact claim-bearing lines
(Current state / What did NOT work / Next step), same intent as no-guessing.md.

Read-only, never modifies files. Reuses hermes_hook_common.local_handoffs_dir() -- the same
`.hermes/handoffs/<project-slug>/*.md` convention session-handoff-check.py already established,
so the two hooks agree on where handoffs live without either hardcoding the other's path.

Adaptations from upstream: same is_first_turn substitution as session-handoff-check.py (Hermes
has no SessionStart-equivalent whose output reaches the model). Global store
(~/.hermes/handoffs/) is scanned too, matching session-handoff-check.py's dual-store behavior.

Self-test: python3 handoff-resume-gate.py --self-test
"""
from __future__ import annotations

import re
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import emit_context, local_handoffs_dir, read_event  # noqa: E402

STALE_DAYS = 3
TS_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:_(\d{2})-(\d{2}))?")
DEAD_STATES = ("CLOSED", "ABANDONED", "RESOLVED", "SUPERSEDE")
CLAIM_HEADINGS = ("current state", "what did not", "what didn't", "next step", "blocked", "verification")


def file_ts(path: Path) -> float:
    m = TS_RE.match(path.name)
    if m:
        try:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            hh = int(m.group(4)) if m.group(4) else 0
            mm = int(m.group(5)) if m.group(5) else 0
            return time.mktime((y, mo, d, hh, mm, 0, 0, 0, -1))
        except (ValueError, OverflowError):
            pass
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def latest_per_project(handoffs_dir: Path) -> dict:
    """{project_slug: latest .md Path} from <handoffs_dir>/<slug>/*.md."""
    out: dict = {}
    if not handoffs_dir.is_dir():
        return out
    for sub in handoffs_dir.iterdir():
        if not sub.is_dir() or sub.name in ("archive", "_graph"):
            continue
        mds = [p for p in sub.glob("*.md") if p.name.upper() != "INDEX.MD"]
        if not mds:
            continue
        out[sub.name] = max(mds, key=file_ts)
    return out


def is_dead(text: str) -> bool:
    head = text[:1200].upper()
    m = re.search(r"STATUS[:*\s]+([A-Z\-]+)", head)
    return bool(m and any(m.group(1).startswith(s) for s in DEAD_STATES))


def claim_lines(text: str, limit: int = 6) -> list[str]:
    lines = text.split("\n")
    picked: list[str] = []
    grab = False
    for ln in lines:
        low = ln.strip().lower()
        if low.startswith("#"):
            grab = any(h in low for h in CLAIM_HEADINGS)
            continue
        if grab and ln.strip() and not ln.strip().startswith("#"):
            picked.append(ln.strip())
            if len(picked) >= limit:
                break
    return picked


def assess(handoffs_dir: Path, now: float) -> list[str]:
    msgs: list[str] = []
    for slug, path in sorted(latest_per_project(handoffs_dir).items()):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        age_days = (now - file_ts(path)) / 86400.0
        if age_days < STALE_DAYS or is_dead(text):
            continue
        claims = claim_lines(text)
        block = [
            "[handoff-resume-gate] STALE handoff for '%s' (%.0fd old, still ACTIVE): %s"
            % (slug, age_days, path.name),
            "  Verify these claims against CURRENT reality before trusting (no-guessing):",
        ]
        for c in claims[:5]:
            block.append("   - " + c[:140])
        if not claims:
            block.append("   - (no Current-state/Next-step section found; read the file fully)")
        msgs.append("\n".join(block))
    return msgs


def _self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        now = time.time()
        stale_day = time.strftime("%Y-%m-%d", time.localtime(now - 6 * 86400))
        fresh_day = time.strftime("%Y-%m-%d", time.localtime(now - 1 * 86400))
        (root / "projA").mkdir(parents=True)
        (root / "projA" / f"{stale_day}_10-00_aaaa.md").write_text(
            "# Handoff\n**Status:** ACTIVE\n## Current state\n- VM up at 1.2.3.4\n- branch X is canon\n",
            encoding="utf-8")
        (root / "projB").mkdir(parents=True)
        (root / "projB" / f"{fresh_day}_10-00_bbbb.md").write_text(
            "# Handoff\n**Status:** ACTIVE\n## Current state\n- fresh, do not flag\n",
            encoding="utf-8")
        (root / "projC").mkdir(parents=True)
        (root / "projC" / f"{stale_day}_09-00_cccc.md").write_text(
            "# Handoff\n**Status:** CLOSED\n## Current state\n- old but closed, skip\n",
            encoding="utf-8")
        msgs = assess(root, now)
        flagged = " ".join(msgs)
        ok = ("projA" in flagged) and ("projB" not in flagged) and ("projC" not in flagged)
        print(f"SCANNED: handoffs_assessed=3 flagged={len(msgs)}")
        if not ok:
            print(f"[ERR] self-test FAILED: {msgs!r}")
            return 1
        print("[OK] handoff-resume-gate self-test passed (stale flagged, fresh+closed skipped)")
        return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()

    event = read_event()
    if event.get("hook_event_name") != "pre_llm_call":
        return 0
    extra = event.get("extra", {}) or {}
    if not extra.get("is_first_turn"):
        return 0

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    now = time.time()
    msgs: list[str] = []
    local_store = local_handoffs_dir(cwd)
    msgs.extend(assess(local_store, now))
    global_store = (Path.home() / ".hermes" / "handoffs").resolve()
    if global_store != local_store:
        msgs.extend(assess(global_store, now))

    if msgs:
        emit_context("\n\n".join(msgs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
