"""Stdlib-only smoke test for backup-retention-cleanup.py's wire contract.

Real disposable git repo, real branches/stashes with backdated timestamps baked into their
names (matching git-auto-backup.py's own naming: hermes-backup-<unix_ts>,
hermes-pre-clean-<unix_ts>) -- proves the retention window is actually enforced, not just that
the regex compiles.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "backup-retention-cleanup.py"


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


def run_hook(cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"hook_event_name": "on_session_end", "cwd": cwd}),
        capture_output=True,
        text=True,
        timeout=15,
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
        now = int(time.time())
        old_ts = now - 20 * 86400   # 20 days old -> past 14-day retention
        fresh_ts = now - 1 * 86400  # 1 day old -> kept

        git("branch", f"hermes-backup-{old_ts}", cwd=str(repo))
        git("branch", f"hermes-backup-{fresh_ts}", cwd=str(repo))

        result = run_hook(str(repo))
        check("hook never blocks (no stdout JSON)", result.stdout.strip() == "")

        branches = git("branch", "--list", "hermes-backup-*", cwd=str(repo)).stdout
        check("old backup branch removed", f"hermes-backup-{old_ts}" not in branches, branches)
        check("fresh backup branch kept", f"hermes-backup-{fresh_ts}" in branches, branches)
        check("cleanup mentioned on stderr", "Retention" in result.stderr, result.stderr)

        # Idempotent: running again with nothing left to clean is silent.
        result2 = run_hook(str(repo))
        check("second run is silent (idempotent)",
              result2.stdout.strip() == "" and result2.stderr.strip() == "")

        # Non-git cwd is a silent no-op.
        non_git = tmp / "not-a-repo"
        non_git.mkdir()
        result3 = run_hook(str(non_git))
        check("non-git cwd: silent no-op",
              result3.stdout.strip() == "" and result3.stderr.strip() == "")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
