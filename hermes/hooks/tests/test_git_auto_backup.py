"""Stdlib-only smoke test for git-auto-backup.py's wire contract.

Uses a real disposable git repo (via subprocess `git init`) rather than mocking git, since this
hook's whole job is running real git commands as a side effect -- verifying it against a real
repo is the only way to actually prove a backup branch/stash gets created. Never touches any
repo outside its own tempdir.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "git-auto-backup.py"


def git(*args: str, cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10)


def make_repo(tmp: Path) -> Path:
    repo = tmp / "repo"
    repo.mkdir()
    git("init", "-q", cwd=str(repo))
    git("config", "user.email", "test@example.com", cwd=str(repo))
    git("config", "user.name", "Test", cwd=str(repo))
    (repo / "a.txt").write_text("hello\n", encoding="utf-8")
    git("add", "a.txt", cwd=str(repo))
    git("commit", "-q", "-m", "init", cwd=str(repo))
    return repo


def run_case(payload: dict, env: dict | None = None) -> subprocess.CompletedProcess:
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=15,
        env=full_env,
    )


def main() -> int:
    failures = 0
    total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        if not ok:
            failures += 1
        print(f"{'PASS' if ok else 'FAIL'}  {label!r:65} {detail}")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        repo = make_repo(tmp)

        # No bypass set -> hook is a no-op safety net, nothing created.
        result = run_case(
            {"tool_name": "terminal", "tool_input": {"command": "git reset --hard HEAD~1"}, "cwd": str(repo)},
        )
        branches = git("branch", "--list", "hermes-backup-*", cwd=str(repo)).stdout
        check("without bypass: no backup branch created (main guard would have blocked)",
              "hermes-backup-" not in branches, f"stdout={result.stdout!r}")

        # Bypass set -> backup branch created before the (simulated) destructive op.
        result = run_case(
            {"tool_name": "terminal", "tool_input": {"command": "git reset --hard HEAD~1"}, "cwd": str(repo)},
            env={"HERMES_ALLOW_GIT_DESTRUCTIVE": "1"},
        )
        branches = git("branch", "--list", "hermes-backup-*", cwd=str(repo)).stdout
        check("with bypass: a hermes-backup-<ts> branch is created",
              "hermes-backup-" in branches, f"branches={branches!r}")
        check("hook never blocks (no stdout JSON)", result.stdout.strip() == "")

        # clean -fdx with an untracked file present -> stash created.
        (repo / "untracked.txt").write_text("scratch\n", encoding="utf-8")
        result = run_case(
            {"tool_name": "terminal", "tool_input": {"command": "git clean -fdx"}, "cwd": str(repo)},
            env={"HERMES_ALLOW_GIT_DESTRUCTIVE": "1"},
        )
        stashes = git("stash", "list", cwd=str(repo)).stdout
        check("clean -fdx with bypass: a hermes-pre-clean stash is created",
              "hermes-pre-clean-" in stashes, f"stashes={stashes!r}")

        # Benign command -> no git side effects, no output.
        result = run_case({"tool_name": "terminal", "tool_input": {"command": "git status"}, "cwd": str(repo)})
        check("benign command: no output", result.stdout.strip() == "" and result.stderr.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
