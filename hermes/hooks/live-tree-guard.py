#!/usr/bin/env python3
"""pre_tool_call: opt-in guard that makes the primary checkout receive-only.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/live-tree-guard.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

The primary checkout receives finished work; it is not where work is done. A lock says
"please do not"; a separate git worktree means there is nothing to overwrite -- you cannot
clobber a file you do not have. Directly relevant to this adapter's own recorded operating
condition (memory: "a concurrent Codex main agent edits this tree live; stage explicit paths,
don't sweep its work") -- the exact hazard this hook exists to make structurally impossible
rather than merely detected.

Opt-in per repository, by a marker file (multi-harness recognition, matching
transfer-contract-guard.py's `.hermes/.claude/.agent/.codex` pattern -- ANY of them present is
enough to treat the repo as receive-only, since a marker written by one harness working the same
repo should still be honored by another). Blocking every repo on the machine would be exactly
the non-monotonic harm quality-code.md warns about -- a guard that wedges unrelated work gets
switched off rather than tuned.

Still allowed in the primary tree, on purpose:
  * anything inside a linked worktree (the sanctioned place to work);
  * append-only per-session artifacts -- handoffs, chronicles, journals (conflict-free by
    construction: one file per session, never edited by anyone else);
  * creating a file that is not tracked -- there is nothing of anyone else's to lose.

Ported unchanged: the git-worktree detection (git-dir vs common-dir comparison), the
tracked/append-only/absolute-path classification logic, the upstream `--self-test`. Adapted:
`Write`/`Edit`/`MultiEdit`/`NotebookEdit` -> Hermes's `write_file`/`patch` (no separate
NotebookEdit tool exists); marker path and APPEND_ONLY prefixes extended to recognize
`.hermes/` alongside `.claude/`/`.agent/`/`.codex/`; block verdict via
hermes_hook_common.block() (Hermes-canonical shape) instead of upstream's raw
`{"decision":"block",...}` dict.

Bypass:    HERMES_ALLOW_LIVE_TREE_EDIT=1, or remove the marker file
Self-test: python3 live-tree-guard.py --self-test
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import block, bypass_env, file_path, log, read_event  # noqa: E402

MARKERS = (
    Path(".hermes") / "live-tree",
    Path(".claude") / "live-tree",
    Path(".agent") / "live-tree",
    Path(".codex") / "live-tree",
)

APPEND_ONLY = (
    ".hermes/handoffs/", ".hermes/chronicles/", ".hermes/briefs/", ".hermes/research/",
    ".claude/handoffs/", ".claude/chronicles/", ".claude/briefs/", ".claude/research/",
    "ops/journal", "activity.jsonl",
)

EDITING = {"write_file", "patch"}


def _git(args: list[str], cwd: Path) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                             text=True, timeout=15, encoding="utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def in_linked_worktree(repo_dir: Path) -> bool:
    """True inside a `git worktree add` checkout, where working is expected.

    A linked worktree's git-dir sits under the primary repo's common dir, so the two
    differ; in the primary checkout they are the same path.
    """
    git_dir = _git(["rev-parse", "--absolute-git-dir"], repo_dir)
    common = _git(["rev-parse", "--path-format=absolute", "--git-common-dir"], repo_dir)
    if not git_dir or not common:
        return False
    return Path(git_dir).resolve() != Path(common).resolve()


def has_marker(repo_root: Path) -> bool:
    return any((repo_root / m).exists() for m in MARKERS)


def is_tracked(path: Path, repo_root: Path) -> bool:
    rel = path.relative_to(repo_root).as_posix()
    return _git(["ls-files", "--error-unmatch", "--", rel], repo_root) is not None


def append_only(path: Path, repo_root: Path) -> bool:
    rel = path.relative_to(repo_root).as_posix()
    return any(marker in rel for marker in APPEND_ONLY)


def assess(target_path: str) -> str | None:
    """None to allow; a reason string to block."""
    try:
        target = Path(target_path)
    except (TypeError, ValueError):
        return None
    search_dir = target.parent if target.parent.exists() else Path.cwd()
    root = _git(["rev-parse", "--show-toplevel"], search_dir)
    if not root:
        return None
    repo_root = Path(root)
    if not has_marker(repo_root):
        return None
    if in_linked_worktree(repo_root):
        return None
    try:
        target.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return None
    if append_only(target, repo_root):
        return None
    if not is_tracked(target, repo_root):
        return None
    rel = target.relative_to(repo_root).as_posix()
    return (
        f"`{rel}` is a tracked file in the PRIMARY checkout of {repo_root.name}, which is "
        f"declared receive-only (a live-tree marker under .hermes/.claude/.agent/.codex). "
        f"Another session may be editing it right now, and in a shared tree the loser of that "
        f"race finds out at commit time or never.\n\n"
        f"Work in your own worktree instead, then let the primary tree receive it:\n"
        f"    git -C \"{repo_root}\" worktree add .hermes/worktrees/<name> -b <branch>\n"
        f"    # edit there, commit, push; the primary tree pulls or merges\n\n"
        f"Append-only artifacts (handoffs, chronicles, journals) are exempt and need no "
        f"worktree. Deliberate override: HERMES_ALLOW_LIVE_TREE_EDIT=1."
    )


def main() -> None:
    if bypass_env("HERMES_ALLOW_LIVE_TREE_EDIT"):
        return
    event = read_event()
    if not event:
        return  # fail open: a guard bug must not be the reason work stops
    if event.get("tool_name") not in EDITING:
        return
    path = file_path(event.get("tool_input") or {})
    if not path:
        return
    reason = assess(path)
    if reason:
        log("BLOCK", "live_tree", "deny", "tracked_file_in_primary_tree", path)
        block(reason)


def self_test() -> int:
    import tempfile

    failures = []

    def check(label, got, want):
        if got != want:
            failures.append(f"{label}: got {got!r}, want {want!r}")
        print(f"  [{'ok ' if got == want else 'FAIL'}] {label}")

    def run(args, cwd):
        subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=30)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "repo"
        root.mkdir()
        run(["init", "-b", "main"], root)
        run(["config", "user.email", "t@example.invalid"], root)
        run(["config", "user.name", "t"], root)
        tracked = root / "src.py"
        tracked.write_text("x = 1\n", encoding="utf-8")
        handoff = root / ".hermes" / "handoffs" / "proj"
        handoff.mkdir(parents=True)
        (handoff / "note.md").write_text("hi\n", encoding="utf-8")
        run(["add", "-A"], root)
        run(["commit", "-m", "init"], root)

        check("no marker -> silent", assess(str(tracked)) is None, True)

        (root / ".hermes" / "live-tree").write_text("", encoding="utf-8")
        check("tracked file in the primary tree is blocked", assess(str(tracked)) is not None, True)
        check("the block names the file", "src.py" in (assess(str(tracked)) or ""), True)
        check("a handoff is exempt", assess(str(handoff / "note.md")) is None, True)
        check("an untracked new file is allowed", assess(str(root / "brand-new.py")) is None, True)

        wt = Path(td) / "wt"
        run(["worktree", "add", str(wt), "-b", "side"], root)
        if (wt / "src.py").exists():
            check("the same file inside a linked worktree is allowed",
                  assess(str(wt / "src.py")) is None, True)
            check("linked worktree is detected as linked", in_linked_worktree(wt), True)
            check("primary tree is not detected as linked", in_linked_worktree(root), False)
        else:
            failures.append("worktree add did not produce a checkout")

        outside = Path(td) / "loose.txt"
        outside.write_text("x", encoding="utf-8")
        check("a file outside any repo is silent", assess(str(outside)) is None, True)

        import json as _json
        event = _json.dumps({
            "hook_event_name": "pre_tool_call", "tool_name": "patch",
            "tool_input": {"path": str(tracked), "mode": "replace", "old_string": "x", "new_string": "y"},
        })
        for label, payload in (("plain", event.encode("utf-8")),
                               ("BOM-prefixed", b"\xef\xbb\xbf" + event.encode("utf-8"))):
            done = subprocess.run([sys.executable, str(Path(__file__).resolve())],
                                  input=payload, capture_output=True, timeout=60)
            check(f"a {label} event still blocks", b'"action": "block"' in (done.stdout or b""), True)

    print("\nSELF-TEST:", "PASS" if not failures else "FAIL")
    for f in failures:
        print("  -", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
