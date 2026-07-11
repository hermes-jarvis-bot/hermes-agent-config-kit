#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from hermes_home_safety import validate_hermes_home

TARGETS = (
    Path("skills") / "config-kit",
    Path("templates") / "config-kit",
)


def planned_actions(hermes_home: Path) -> list[tuple[str, Path]]:
    actions: list[tuple[str, Path]] = []
    for rel in TARGETS:
        target = hermes_home / rel
        if target.exists():
            actions.append(("remove", target))
        else:
            actions.append(("absent", target))
    return actions


def remove_target(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hermes-home", required=True, help="Target Hermes home/profile directory. Use a sandbox path for tests.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Actually remove config-kit artefacts. Without this, dry-run only.")
    mode.add_argument("--dry-run", action="store_true", help="Explicit dry-run flag for readability.")
    ap.add_argument("--i-know-this-is-production", action="store_true", help="Override target safety checks after operator confirmation.")
    args = ap.parse_args()

    hermes_home = Path(args.hermes_home).expanduser().resolve()
    try:
        validate_hermes_home(hermes_home, args.i_know_this_is_production)
    except ValueError as exc:
        ap.error(str(exc))
    apply = bool(args.apply)
    print(("APPLY" if apply else "DRY RUN") + f": target {hermes_home}")

    actions = planned_actions(hermes_home)
    for action, target in actions:
        print(f"{action} {target}")
        if apply and action == "remove":
            remove_target(target)

    print(f"Actions: {sum(1 for action, _ in actions if action == 'remove')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
