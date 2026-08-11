#!/usr/bin/env python3
"""pre_llm_call (is_first_turn only): auto-DETECT a long-running project and nudge to adopt a harness.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/long-run-detector.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

A [LONG-RUN]-style harness (feature_list.json/init.sh + a documented adoption checklist) is
meant to be assigned by a human decision, not auto-applied -- but a manual gate rots: a project
quietly grows across many sessions and nobody runs the checklist. This hook makes the DETECTION
mechanical while keeping the human decision: it surfaces "this looks long-running -> consider
adopting the harness" when signals appear, and stays silent otherwise. It does NOT auto-write
any adoption marker itself.

Signals (current project = cwd):
  - strong : >=3 dated session handoffs in a handoffs/ tree (multi-session)
  - medium : >=40 git commits ; >=200 tracked files ; PROBLEMS.md present
  Fire when strong OR (>=2 medium).

Suppressed (silent) when:
  - already adopted   : feature_list.json or init.sh present in cwd
  - aggregation hub    : >5 distinct project subdirs under the handoffs tree
                         (a multi-project hub, not a single project to mark)
  - not a real project : cwd is HOME, or has no .git and no .hermes/.claude dir
  - nagged recently    : the per-project cooldown stamp is younger than 14 days

Never blocks, informational only (injected via pre_llm_call's genuine `{"context": ...}`
channel, same mechanism as session-handoff-check.py). Ported unchanged: the signal thresholds,
the aggregation-hub exemption, the hub-context-gap check, the upstream `--self-test`. Adapted:
looks for the handoffs tree under `.hermes/handoffs` first, falling back to `.claude/handoffs`
if that doesn't exist (this adapter has no established convention for merging counts across
both at once -- a project using one convention consistently is the expected case, not a
project deliberately splitting handoffs across two); cooldown stamp moved to
`.hermes/.longrun-nudged`; "is this a real project" check accepts either `.hermes` or `.claude`
present, not just Claude Code's directory.

Self-test: python3 long-run-detector.py --self-test
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import emit_context, read_event  # noqa: E402

NUDGE_COOLDOWN_DAYS = 14
HUB_SUBDIR_LIMIT = 5
MIN_HANDOFFS = 3
MIN_COMMITS = 40
MIN_TRACKED = 200


def _git(cwd: Path, *args: str, count_lines: bool = False) -> int:
    try:
        out = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=3)
        if out.returncode != 0:
            return -1
        if count_lines:
            return sum(1 for ln in out.stdout.splitlines() if ln.strip())
        return int(out.stdout.strip() or 0)
    except Exception:
        return -1


def has_agent_docs(cwd: Path) -> bool:
    return any(
        (cwd / p).exists()
        for p in ("docs/kb", "docs/layers", "kb/docs", "openwiki", "scripts/validate_kb.py")
    )


def _handoffs_dir(cwd: Path) -> Path | None:
    hermes_dir = cwd / ".hermes" / "handoffs"
    if hermes_dir.exists():
        return hermes_dir
    claude_dir = cwd / ".claude" / "handoffs"
    if claude_dir.exists():
        return claude_dir
    return None


def detect(cwd: Path) -> list[str] | None:
    """Return list of signal strings if a nudge should fire, else None."""
    home = Path.home().resolve()
    if cwd.resolve() == home:
        return None
    if not (cwd / ".git").exists() and not (cwd / ".hermes").exists() and not (cwd / ".claude").exists():
        return None
    if (cwd / "feature_list.json").exists() or (cwd / "init.sh").exists():
        return None

    signals: list[str] = []
    strong = False

    hdir = _handoffs_dir(cwd)
    if hdir is not None:
        subdir_count = sum(1 for d in hdir.iterdir() if d.is_dir() and d.name != "archive")
        if subdir_count > HUB_SUBDIR_LIMIT:
            return None
        handoffs = 0
        for p in hdir.rglob("*.md"):
            rel = p.relative_to(hdir)
            if p.name.startswith("INDEX") or "archive" in rel.parts:
                continue
            handoffs += 1
        if handoffs >= MIN_HANDOFFS:
            strong = True
            signals.append(f"{handoffs} session handoffs (multi-session work)")

    commits = _git(cwd, "rev-list", "--count", "HEAD")
    if commits >= MIN_COMMITS:
        signals.append(f"{commits} git commits")
    tracked = _git(cwd, "ls-files", count_lines=True)
    if tracked >= MIN_TRACKED:
        signals.append(f"{tracked} tracked files (large codebase)")
    if (cwd / "PROBLEMS.md").exists():
        signals.append("PROBLEMS.md present (ongoing incident log)")

    if strong or len(signals) >= 2:
        return signals
    return None


def hub_context_gap(cwd: Path) -> list[str] | None:
    """An aggregation hub is exempt from the adoption mark, not from context."""
    hdir = _handoffs_dir(cwd)
    if hdir is None:
        return None
    try:
        subdirs = sum(1 for d in hdir.iterdir() if d.is_dir() and d.name != "archive")
    except OSError:
        return None
    if subdirs <= HUB_SUBDIR_LIMIT:
        return None
    missing = [name for name in ("AGENTS.md", "CLAUDE.md", "feature_list.json") if not (cwd / name).exists()]
    if not missing:
        return None
    return [f"aggregation hub with {subdirs} project subdirs", "missing: " + ", ".join(missing)]


def _nudge_stamp(cwd: Path) -> Path:
    base = cwd / ".hermes" if (cwd / ".hermes").exists() or not (cwd / ".claude").exists() else cwd / ".claude"
    return base / ".longrun-nudged"


def _recently_nudged(cwd: Path, now: float) -> bool:
    stamp = _nudge_stamp(cwd)
    if not stamp.exists():
        return False
    try:
        return (now - stamp.stat().st_mtime) / 86400 < NUDGE_COOLDOWN_DAYS
    except OSError:
        return False


def _stamp(cwd: Path) -> None:
    try:
        stamp = _nudge_stamp(cwd)
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text(time.strftime("%Y-%m-%d %H:%M"), encoding="utf-8")
    except OSError:
        pass


def build_report(cwd: Path) -> str | None:
    signals = detect(cwd)
    if not signals:
        gap = hub_context_gap(cwd)
        if not gap:
            return None
        _stamp(cwd)
        return (
            "=" * 60 + "\n"
            "AGENT CONTEXT MISSING in this aggregation hub.\n"
            "  " + "; ".join(gap) + "\n"
            + "=" * 60 + "\n"
            "INSTRUCTION: a hub is exempt from the long-run adoption mark, not from carrying "
            "context. It needs AGENTS.md (canonical, harness-neutral), a thin CLAUDE.md "
            "importing it with @AGENTS.md, and feature_list.json holding the plan. If this repo "
            "has them on another branch they are almost certainly still there -- check before "
            "writing new ones:\n"
            "  git checkout origin/main -- AGENTS.md feature_list.json README.md"
        )

    docs_missing = not has_agent_docs(cwd)
    lines = [
        "=" * 60,
        "LONG-RUN candidate: this project shows long-running signals but is",
        "NOT tracked as long-run (no feature_list.json / init.sh).",
        "  signals: " + "; ".join(signals),
    ]
    if docs_missing:
        lines.append("  ALSO: no agent-docs tree (docs/kb, docs/layers, kb/docs all absent).")
    lines += [
        "=" * 60,
        "INSTRUCTION: Consider adopting a long-run harness: run your project's adoption "
        "checklist; if it passes, add feature_list.json + init.sh and record the decision.",
    ]
    if docs_missing:
        lines += [
            "ALSO PROPOSE to the user adopting an agent-docs KB now (kb-skeleton: docs/kb + "
            "a validator script) -- a complex project without docs is exactly the gap this "
            "signals; once adopted, a Stop-gate + CI can keep it current mechanically.",
        ]
    lines += [
        "Detection is automatic; the adoption mark and KB adoption stay a human decision by "
        "design (premature marks are an anti-pattern). Surface this to the user as an explicit "
        "proposal.",
        "=" * 60,
    ]
    _stamp(cwd)
    return "\n".join(lines)


def main() -> int:
    event = read_event()
    if event.get("hook_event_name") != "pre_llm_call":
        return 0
    extra = event.get("extra", {}) or {}
    if not extra.get("is_first_turn"):
        return 0

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    if _recently_nudged(cwd, time.time()):
        return 0
    report = build_report(cwd)
    if report:
        emit_context(report)
    return 0


def _self_test() -> int:
    import tempfile

    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        proj = root / "proj"
        hd = proj / ".hermes" / "handoffs" / "alpha"
        hd.mkdir(parents=True)
        for i in range(3):
            (hd / f"2026-06-1{i}_10-00_abc1234{i}.md").write_text("h", encoding="utf-8")
        pos = detect(proj)
        if not pos:
            print("SELF-TEST FAIL: long-run project not detected")
            ok = False
        (proj / "feature_list.json").write_text("{}", encoding="utf-8")
        if detect(proj) is not None:
            print("SELF-TEST FAIL: adopted project should be silent")
            ok = False
        hub = root / "hub"
        hubh = hub / ".hermes" / "handoffs"
        for n in range(6):
            sd = hubh / f"p{n}"
            sd.mkdir(parents=True)
            (sd / f"2026-06-10_10-00_dead000{n}.md").write_text("h", encoding="utf-8")
        if detect(hub) is not None:
            print("SELF-TEST FAIL: aggregation hub should be silent")
            ok = False
        if hub_context_gap(hub) is None:
            print("SELF-TEST FAIL: hub without AGENTS.md/CLAUDE.md/feature_list.json should report a gap")
            ok = False
        for name in ("AGENTS.md", "CLAUDE.md", "feature_list.json"):
            (hub / name).write_text("x", encoding="utf-8")
        if hub_context_gap(hub) is not None:
            print("SELF-TEST FAIL: hub with full context should be silent")
            ok = False
        triv = root / "triv"
        (triv / ".hermes").mkdir(parents=True)
        if detect(triv) is not None:
            print("SELF-TEST FAIL: trivial project should be silent")
            ok = False
    print("SELF-TEST: PASS" if ok else "SELF-TEST: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    sys.exit(main())
