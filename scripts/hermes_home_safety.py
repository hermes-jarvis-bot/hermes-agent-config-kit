"""Safety checks for disposable Hermes-home installer targets."""
from __future__ import annotations

import os
from pathlib import Path


def validate_hermes_home(path: Path, allow_production: bool) -> None:
    """Reject production and non-disposable targets unless explicitly overridden."""
    production_paths = {Path.home() / ".hermes"}
    if configured_home := os.environ.get("HERMES_HOME"):
        production_paths.add(Path(configured_home).expanduser().resolve())

    if path in production_paths:
        if not allow_production:
            raise ValueError(
                f"refusing production Hermes home {path}; pass "
                "--i-know-this-is-production only after operator confirmation"
            )
        return

    disposable = path.is_relative_to(Path("/tmp")) or path.name.endswith(("-test", "-sandbox"))
    if not disposable and not allow_production:
        raise ValueError(
            f"refusing non-disposable Hermes home {path}; use /tmp, a *-test or "
            "*-sandbox path, or pass --i-know-this-is-production after operator confirmation"
        )