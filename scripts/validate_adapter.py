#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    temp_parent = Path(tempfile.mkdtemp(prefix="hermes-config-kit-validate-"))
    hermes_home = temp_parent / "hermes-home-test"
    try:
        run(
            sys.executable,
            "-m",
            "py_compile",
            *(str(path.relative_to(ROOT)) for path in sorted((ROOT / "scripts").glob("*.py"))),
        )
        run(sys.executable, "scripts/validate_output.py")
        run(sys.executable, "scripts/install_hermes.py", "--dry-run", "--hermes-home", str(hermes_home))
        if hermes_home.exists():
            raise RuntimeError("installer dry-run created the target Hermes home")
        run(sys.executable, "scripts/install_hermes.py", "--apply", "--hermes-home", str(hermes_home))
        if not (hermes_home / "skills" / "config-kit").is_dir():
            raise RuntimeError("installer did not create skills/config-kit")
        run(sys.executable, "scripts/remove_hermes.py", "--dry-run", "--hermes-home", str(hermes_home))
        if not (hermes_home / "skills" / "config-kit").is_dir():
            raise RuntimeError("remover dry-run removed skills/config-kit")
        run(sys.executable, "scripts/remove_hermes.py", "--apply", "--hermes-home", str(hermes_home))
        if (hermes_home / "skills" / "config-kit").exists():
            raise RuntimeError("remover left skills/config-kit")
        if (hermes_home / "templates" / "config-kit").exists():
            raise RuntimeError("remover left templates/config-kit")
    finally:
        shutil.rmtree(temp_parent, ignore_errors=True)
    print("Adapter validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
