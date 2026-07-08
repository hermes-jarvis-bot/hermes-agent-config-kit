#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def copy_tree(src: Path, dst: Path, apply: bool) -> list[str]:
    actions: list[str] = []
    for path in sorted(src.rglob("*")):
        if path.is_file():
            rel = path.relative_to(src)
            target = dst / rel
            actions.append(f"copy {path.relative_to(ROOT)} -> {target}")
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
    return actions


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hermes-home", required=True, help="Target Hermes home/profile directory. Use a temp dir for tests.")
    ap.add_argument("--apply", action="store_true", help="Actually write files. Without this, dry-run only.")
    ap.add_argument("--dry-run", action="store_true", help="Explicit dry-run flag for readability.")
    args = ap.parse_args()
    hermes_home = Path(args.hermes_home).expanduser().resolve()
    apply = bool(args.apply)
    print(("APPLY" if apply else "DRY RUN") + f": target {hermes_home}")
    actions: list[str] = []
    skills_src = ROOT / "hermes" / "skills"
    if skills_src.exists():
        actions.extend(copy_tree(skills_src, hermes_home / "skills" / "config-kit", apply))
    templates_src = ROOT / "hermes" / "templates"
    if templates_src.exists():
        actions.extend(copy_tree(templates_src, hermes_home / "templates" / "config-kit", apply))
    for action in actions:
        print(action)
    print(f"Actions: {len(actions)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
