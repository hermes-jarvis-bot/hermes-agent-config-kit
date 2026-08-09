#!/usr/bin/env python3
"""pre_llm_call (is_first_turn only): flag when a repo's agent-facing docs have gone STALE vs code.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's hooks/docs-staleness-guard.py
(reimplemented from the upstream SessionStart hook, see mappings/reviewed-hooks.yaml).

Same event choice as session-handoff-check.py, for the same reason: Hermes's
`on_session_start` discards its return value, but `pre_llm_call` filtered to
`extra.is_first_turn` genuinely appends its `{"context": ...}` return to the model's first
message (verified in agent/turn_context.py:1059-1109).

Why a hook, not a reminder: acting on STALE repo docs = acting on wrong context
(agent-legible-environment). "Docs exist" != "docs current". A mechanical invariant beats
prompt advice. Detection is automatic; refreshing the docs stays a human/tool decision.

Anchors whose freshness is tracked (current project = cwd):
  - openwiki/      (OpenWiki output, if the project uses that tool)
  - docs/layers/   (this kit's own feature-layer-architecture skill's curated docs)
Freshness signal (git = source of truth): base = last commit that touched the anchor. Every
commit in base..HEAD by construction did NOT touch the anchor, so its count = how far the
docs have fallen behind. >= STALE_COMMITS -> STALE.
Pointer signal: openwiki/ present but neither AGENTS.md nor CLAUDE.md references it -> the
docs exist but agents are not told to read them.

Silent (opt-in) when: no anchor present; cwd is HOME / ~/.hermes; docs are fresh; nagged <
COOLDOWN_DAYS ago; or .hermes/.skip-docs-staleness present.

Tunables: HERMES_DOCS_STALE_COMMITS (default 20).
Opt-out per project: touch .hermes/.skip-docs-staleness
Self-test (unchanged logic from upstream, no Hermes wire-protocol dependency):
    python3 docs-staleness-guard.py --self-test
Related skills (adapted from the upstream rules these anchors were named for):
  hermes/skills/documentation-freshness/SKILL.md, hermes/skills/billing-spend-controls/SKILL.md
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

COOLDOWN_DAYS = 7
DEFAULT_STALE_COMMITS = 20
ANCHORS = ("openwiki", "docs/layers")
ANCHORS_FILE = ".docs-anchors"  # .hermes/.docs-anchors: extra per-project anchors, one rel path per line
STAMP_NAME = ".docs-staleness-nudged"
SKIP_NAME = ".skip-docs-staleness"


def _project_anchors(cwd: Path) -> tuple[str, ...]:
    """Default anchors + optional per-project extras from .hermes/.docs-anchors."""
    extra: list[str] = []
    f = cwd / ".hermes" / ANCHORS_FILE
    if f.exists():
        try:
            for line in f.read_text(encoding="utf-8").splitlines():
                line = line.strip().replace("\\", "/").strip("/")
                if line and not line.startswith("#"):
                    extra.append(line)
        except Exception:
            pass
    return ANCHORS + tuple(x for x in extra if x not in ANCHORS)


def _git_out(cwd: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=4
        )
        if out.returncode != 0:
            return None
        return out.stdout.strip()
    except Exception:
        return None


def _git_count(cwd: Path, *args: str) -> int:
    s = _git_out(cwd, *args)
    if s is None:
        return -1
    try:
        return int(s.strip() or 0)
    except ValueError:
        return -1


def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def detect(cwd: Path, stale_commits: int) -> list[str] | None:
    """Return list of finding strings if a nudge should fire, else None."""
    home = Path.home().resolve()
    if cwd.resolve() in (home, (home / ".hermes").resolve()):
        return None
    if (cwd / ".hermes" / SKIP_NAME).exists():
        return None

    anchor_present = False
    findings: list[str] = []

    for anchor in _project_anchors(cwd):
        if not (cwd / anchor).exists():
            continue
        anchor_present = True
        base = _git_out(cwd, "rev-list", "-1", "HEAD", "--", anchor)
        if not base:
            continue
        n = _git_count(cwd, "rev-list", "--count", f"{base}..HEAD")
        if n >= stale_commits:
            findings.append(
                f"{anchor}/ is {n} commits behind HEAD "
                f"(>= {stale_commits}) -- refresh the agent docs"
            )

    if (cwd / "openwiki").exists():
        referenced = any(
            "openwiki" in _read_text(cwd / f).lower()
            for f in ("AGENTS.md", "CLAUDE.md")
        )
        if not referenced:
            findings.append(
                "openwiki/ present but not referenced from AGENTS.md/CLAUDE.md "
                "-- add a one-line pointer so agents read it"
            )

    if not anchor_present:
        return None
    return findings or None


def _recently_nudged(hermes_dir: Path, now: float) -> bool:
    stamp = hermes_dir / STAMP_NAME
    if not stamp.exists():
        return False
    try:
        return (now - stamp.stat().st_mtime) / 86400 < COOLDOWN_DAYS
    except Exception:
        return False


def _stamp(hermes_dir: Path) -> None:
    try:
        hermes_dir.mkdir(parents=True, exist_ok=True)
        (hermes_dir / STAMP_NAME).write_text(
            time.strftime("%Y-%m-%d %H:%M"), encoding="utf-8"
        )
    except Exception:
        pass


def main() -> int:
    event = json.loads(sys.stdin.read().lstrip("﻿").strip() or "{}")
    if event.get("hook_event_name") != "pre_llm_call":
        return 0
    if not (event.get("extra", {}) or {}).get("is_first_turn"):
        return 0

    cwd = Path(str(event.get("cwd") or Path.cwd()))
    hermes_dir = cwd / ".hermes"
    now = time.time()
    if _recently_nudged(hermes_dir, now):
        return 0
    try:
        stale_commits = int(os.environ.get("HERMES_DOCS_STALE_COMMITS", "") or DEFAULT_STALE_COMMITS)
    except ValueError:
        stale_commits = DEFAULT_STALE_COMMITS

    findings = detect(cwd, stale_commits)
    if not findings:
        return 0

    lines = [
        "=" * 60,
        "AGENT DOCS FRESHNESS: repo docs the agent relies on look stale.",
        *[f"  - {f}" for f in findings],
        "=" * 60,
        "INSTRUCTION: treat these agent-facing docs as possibly out-of-date.",
        "Refresh them (OpenWiki `openwiki --update`, or update docs/layers/) and",
        "ensure AGENTS.md points to them. Generation costs tokens (opt-in, see",
        "the billing-spend-controls skill); this detection is free. Surface to the user.",
        "See the documentation-freshness skill. Opt out: touch .hermes/.skip-docs-staleness",
        "=" * 60,
        "",
    ]
    print(json.dumps({"context": "\n".join(lines)}, ensure_ascii=False))
    _stamp(hermes_dir)
    return 0


def _self_test() -> int:
    import tempfile

    def run(cwd: Path, *a: str) -> None:
        subprocess.run(["git", *a], cwd=str(cwd), capture_output=True, text=True)

    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "repo"
        root.mkdir()
        run(root, "init", "-q")
        run(root, "config", "user.email", "t@t")
        run(root, "config", "user.name", "t")
        run(root, "config", "commit.gpgsign", "false")

        (root / "openwiki").mkdir()
        (root / "openwiki" / "index.md").write_text("doc", encoding="utf-8")
        run(root, "add", "-A")
        run(root, "commit", "-q", "-m", "docs")

        f = detect(root, 20)
        if not f or not any("not referenced" in x for x in f):
            print("SELF-TEST FAIL: missing pointer not detected")
            ok = False
        if f and any("behind HEAD" in x for x in f):
            print("SELF-TEST FAIL: fresh docs wrongly flagged stale")
            ok = False

        (root / "AGENTS.md").write_text("Map lives in openwiki/", encoding="utf-8")
        run(root, "add", "-A")
        run(root, "commit", "-q", "-m", "pointer")
        f = detect(root, 20)
        if f and any("not referenced" in x for x in f):
            print("SELF-TEST FAIL: present pointer still flagged")
            ok = False

        for i in range(4):
            (root / f"src{i}.py").write_text(f"x = {i}", encoding="utf-8")
            run(root, "add", "-A")
            run(root, "commit", "-q", "-m", f"c{i}")
        f = detect(root, 3)
        if not f or not any("behind HEAD" in x for x in f):
            print("SELF-TEST FAIL: stale docs not detected")
            ok = False

        (root / ".hermes").mkdir(exist_ok=True)
        (root / ".hermes" / SKIP_NAME).write_text("x", encoding="utf-8")
        if detect(root, 3) is not None:
            print("SELF-TEST FAIL: opt-out file did not silence")
            ok = False

        bare = Path(td) / "bare"
        bare.mkdir()
        run(bare, "init", "-q")
        if detect(bare, 20) is not None:
            print("SELF-TEST FAIL: repo without anchor should be silent")
            ok = False

        cust = Path(td) / "custom"
        cust.mkdir()
        run(cust, "init", "-q")
        run(cust, "config", "user.email", "t@t")
        run(cust, "config", "user.name", "t")
        run(cust, "config", "commit.gpgsign", "false")
        (cust / "kb" / "docs").mkdir(parents=True)
        (cust / "kb" / "docs" / "index.md").write_text("kb", encoding="utf-8")
        (cust / ".hermes").mkdir()
        (cust / ".hermes" / ANCHORS_FILE).write_text("# agent-KB\nkb/docs\n", encoding="utf-8")
        run(cust, "add", "-A")
        run(cust, "commit", "-q", "-m", "kb")
        for i in range(4):
            (cust / f"s{i}.py").write_text(str(i), encoding="utf-8")
            run(cust, "add", "-A")
            run(cust, "commit", "-q", "-m", f"c{i}")
        f = detect(cust, 3)
        if not f or not any("kb/docs" in x for x in f):
            print("SELF-TEST FAIL: custom anchor kb/docs staleness not detected")
            ok = False

    print("SELF-TEST: PASS" if ok else "SELF-TEST: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    sys.exit(main())
