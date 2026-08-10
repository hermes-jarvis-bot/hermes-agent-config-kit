#!/usr/bin/env python3
"""Report how this repo's `hermes/{skills,hooks,templates}` differ from a live
installed `<hermes-home>/{skills,hooks,templates}/config-kit/` copy.

Design adapted from claude-code-config's `scripts/rules_drift_report.py`:
`install_hermes.py` already performs the one-directional repo -> live copy.
This is a read-only diagnostic for the OTHER direction -- has the live copy
been hand-edited since the last install/update, in a way an operator should
review (and consider reflecting back into the repo) before running install
again? It never writes anything, in either direction.

Run:  python3 scripts/config_kit_drift_report.py --hermes-home <path> [--i-know-this-is-production]
      python3 scripts/config_kit_drift_report.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from hermes_home_safety import validate_hermes_home

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("skills", "hooks", "templates")


def _norm(path: Path) -> str:
    return hashlib.md5(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _files(root: Path) -> set[Path]:
    if not root.is_dir():
        return set()
    return {
        p.relative_to(root)
        for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    }


def classify(repo_dir: Path, live_dir: Path) -> dict[str, list[str]]:
    """Bucket every relative path by how the repo and live trees disagree."""
    buckets: dict[str, list[str]] = {
        "identical": [], "eol_only": [], "both_added": [],
        "live_superset": [], "repo_superset": [],
        "live_only": [], "repo_only": [],
    }
    repo_files, live_files = _files(repo_dir), _files(live_dir)
    for rel in sorted(repo_files | live_files, key=str):
        if rel not in live_files:
            buckets["repo_only"].append(str(rel))
            continue
        if rel not in repo_files:
            buckets["live_only"].append(str(rel))
            continue
        repo_path, live_path = repo_dir / rel, live_dir / rel
        if repo_path.read_bytes() == live_path.read_bytes():
            buckets["identical"].append(str(rel))
            continue
        if _norm(repo_path) == _norm(live_path):
            buckets["eol_only"].append(str(rel))
            continue
        try:
            repo_lines = {l for l in repo_path.read_text(encoding="utf-8", errors="strict").replace("\r\n", "\n").split("\n") if l}
            live_lines = {l for l in live_path.read_text(encoding="utf-8", errors="strict").replace("\r\n", "\n").split("\n") if l}
        except UnicodeDecodeError:
            buckets["both_added"].append(f"{rel} (binary or non-UTF-8, differs)")
            continue
        only_repo, only_live = repo_lines - live_lines, live_lines - repo_lines
        if only_repo and only_live:
            buckets["both_added"].append(f"{rel} (+{len(only_repo)} repo / +{len(only_live)} live)")
        elif only_repo:
            buckets["repo_superset"].append(f"{rel} (+{len(only_repo)} repo)")
        else:
            buckets["live_superset"].append(f"{rel} (+{len(only_live)} live)")
    return buckets


ORDER = [
    ("identical", "byte-identical, nothing to do"),
    ("eol_only", "differ only by CRLF - cosmetic"),
    ("repo_superset", "repo has content live lacks - re-run install_hermes.py to catch up"),
    ("live_superset", "live has content repo lacks - hand-edited after install; review before overwriting"),
    ("both_added", "both sides changed - merge by hand, do not blind-copy in either direction"),
    ("live_only", "only in the live install - hand-added; install/remove will not touch it"),
    ("repo_only", "only in the repo - not yet installed; run install_hermes.py to add it"),
]


def report(repo_root: Path, hermes_home: Path) -> int:
    print(f"repo: {repo_root}\nlive: {hermes_home}\n")
    for category in CATEGORIES:
        repo_dir = repo_root / "hermes" / category
        live_dir = hermes_home / category / "config-kit"
        buckets = classify(repo_dir, live_dir)
        print(f"== {category} ==")
        for key, blurb in ORDER:
            items = buckets[key]
            print(f"{key:15} {len(items):>3}  {blurb}")
            for item in items:
                print(f"                    {item}")
        print()
    print("Reminder: this is a report, not a sync. install_hermes.py/remove_hermes.py")
    print("already move content repo -> live one-directionally; this tool exists to")
    print("surface the OTHER direction (live edits the repo does not know about).")
    return 0


def _self_test() -> int:
    import tempfile

    fails: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        repo_root, hermes_home = tmp / "repo", tmp / "home"
        skills_repo = repo_root / "hermes" / "skills"
        skills_live = hermes_home / "skills" / "config-kit"
        skills_repo.mkdir(parents=True)
        skills_live.mkdir(parents=True)
        (skills_repo / "same.md").write_text("a\nb\n", encoding="utf-8")
        (skills_live / "same.md").write_text("a\nb\n", encoding="utf-8")
        (skills_repo / "eol.md").write_bytes(b"a\nb\n")
        (skills_live / "eol.md").write_bytes(b"a\r\nb\r\n")
        (skills_repo / "repo-only.md").write_text("x\n", encoding="utf-8")
        (skills_live / "live-only.md").write_text("y\n", encoding="utf-8")
        (skills_repo / "both.md").write_text("a\nonly-repo\n", encoding="utf-8")
        (skills_live / "both.md").write_text("a\nonly-live\n", encoding="utf-8")

        got = classify(skills_repo, skills_live)
        expected = {
            "identical": ["same.md"],
            "eol_only": ["eol.md"],
            "repo_only": ["repo-only.md"],
            "live_only": ["live-only.md"],
        }
        for key, want in expected.items():
            if got[key] != want:
                fails.append(f"{key}: expected {want}, got {got[key]}")
        if len(got["both_added"]) != 1 or not got["both_added"][0].startswith("both.md"):
            fails.append(f"both_added: expected one entry for both.md, got {got['both_added']}")

        # A missing live tree must degrade to a listing, not an exception.
        try:
            classify(skills_repo, tmp / "nope")
        except Exception as exc:  # noqa: BLE001
            fails.append(f"missing live tree raised {exc!r}")

        if report(repo_root, hermes_home) != 0:
            fails.append("report(): expected exit 0 (informational tool, never fails the run)")

    for line in fails:
        print("FAIL:", line)
    print("config_kit_drift_report self-test:", "FAILED" if fails else "ok")
    return 1 if fails else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hermes-home", help="Live Hermes home/profile directory to compare against.")
    parser.add_argument("--i-know-this-is-production", action="store_true", help="Override target safety checks after operator confirmation.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    if not args.hermes_home:
        parser.error("--hermes-home is required unless --self-test is passed")
    hermes_home = Path(args.hermes_home).expanduser().resolve()
    try:
        validate_hermes_home(hermes_home, args.i_know_this_is_production)
    except ValueError as exc:
        parser.error(str(exc))
    return report(ROOT, hermes_home)


if __name__ == "__main__":
    sys.exit(main())
