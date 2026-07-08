#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def validate_lock() -> None:
    data = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
    upstream = data.get("upstream", {})
    if upstream.get("repo") != "AnastasiyaW/claude-code-config":
        fail("upstream.lock.json repo mismatch")
    sha = upstream.get("last_synced_sha")
    if sha is not None and not re.fullmatch(r"[0-9a-f]{40}", sha):
        fail("last_synced_sha must be null or a 40-char SHA")


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path} missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path} frontmatter not closed")
    fm = text[4:end]
    result = {}
    for line in fm.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip().strip('"')
    return result


def validate_skills() -> None:
    skills = sorted((ROOT / "hermes" / "skills").glob("*/SKILL.md"))
    if not skills:
        fail("no Hermes skills generated")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text, path)
        for field in ["name", "description"]:
            if not fm.get(field):
                fail(f"{path} missing {field}")
        if "~/.hermes" in text and "--apply" in text:
            fail(f"{path} appears to encourage live Hermes writes")


def validate_no_live_writes_default() -> None:
    risky = []
    for path in (ROOT / "scripts").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"Path\(['\"]~/.hermes|expanduser\(['\"]~/.hermes", text):
            risky.append(str(path.relative_to(ROOT)))
    if risky:
        fail("scripts contain direct ~/.hermes path writes: " + ", ".join(risky))


def validate_snapshot() -> None:
    snap = ROOT / "upstream" / "claude-code-config" / "snapshot"
    if not snap.exists():
        fail("upstream snapshot missing; run scripts/sync_upstream.py --sync")
    if not (snap / "README.md").exists():
        fail("upstream snapshot README.md missing")


def main() -> int:
    validate_lock()
    validate_snapshot()
    validate_skills()
    validate_no_live_writes_default()
    print("Validation OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
