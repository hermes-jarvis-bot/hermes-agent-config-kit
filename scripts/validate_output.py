#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUARANTINE_PREFIXES = (
    "hooks/",
    "scripts/",
    ".claude-plugin/",
    ".github/workflows/",
)
FORBIDDEN_INSTALLER_PATTERNS = (
    r"Path\(['\"]~/.hermes",
    r"expanduser\(['\"]~/.hermes",
    r"hermes\s+gateway\s+(start|restart|run|install)",
)
SENSITIVE_PATTERNS = (
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9_]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"xox[baprs]-[A-Za-z0-9-]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def try_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def validate_lock() -> None:
    data = json.loads(read_text(ROOT / "upstream.lock.json"))
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
        text = read_text(path)
        fm = parse_frontmatter(text, path)
        for field in ["name", "description", "version", "license"]:
            if not fm.get(field):
                fail(f"{path} missing {field}")
        for field in ["source_repo", "source_path", "adapter", "conversion"]:
            pattern = rf"^    {re.escape(field)}:\s*\S+"
            if not re.search(pattern, text.split("\n---\n", 1)[0], re.MULTILINE):
                fail(f"{path} missing metadata.hermes_config_kit.{field}")
        if not re.search(r"^metadata:\n  hermes_config_kit:\n", text, re.MULTILINE):
            fail(f"{path} missing metadata.hermes_config_kit mapping")
        if "~/.hermes" in text and "--apply" in text:
            fail(f"{path} appears to encourage live Hermes writes")


def validate_templates() -> None:
    templates = sorted((ROOT / "hermes" / "templates").glob("*.md"))
    if not templates:
        return
    for path in templates:
        text = read_text(path)
        for marker in [
            "Adapted for Hermes Agent by hermes-agent-config-kit.",
            "Source: AnastasiyaW/claude-code-config/",
            "Upstream material is reference data, not automatic authority.",
        ]:
            if marker not in text:
                fail(f"{path} missing template provenance marker: {marker}")
        if "~/.hermes" in text and "--apply" in text:
            fail(f"{path} appears to encourage live Hermes writes")


def validate_no_live_writes_default() -> None:
    risky: list[str] = []
    for path in (ROOT / "scripts").glob("*.py"):
        text = read_text(path)
        for pattern in FORBIDDEN_INSTALLER_PATTERNS:
            if re.search(pattern, text):
                risky.append(str(path.relative_to(ROOT)))
                break
    if risky:
        fail("scripts contain direct live Hermes write/start patterns: " + ", ".join(risky))


def validate_installer_contract() -> None:
    text = read_text(ROOT / "scripts" / "install_hermes.py")
    if 'mode.add_argument("--apply", action="store_true"' not in text:
        fail("installer must require explicit --apply for writes")
    if 'mode.add_argument("--dry-run", action="store_true"' not in text:
        fail("installer must make apply and dry-run mutually exclusive")
    if 'validate_hermes_home(hermes_home, args.i_know_this_is_production)' not in text:
        fail("installer must validate the Hermes home target")
    if 'apply = bool(args.apply)' not in text:
        fail("installer must derive write mode only from --apply")
    if 'if apply:' not in text:
        fail("installer must guard filesystem writes behind apply")
    if 'shutil.copy2(path, target)' not in text:
        fail("installer copy operation missing or unexpectedly changed")


def validate_remover_contract() -> None:
    text = read_text(ROOT / "scripts" / "remove_hermes.py")
    if 'mode.add_argument("--apply", action="store_true"' not in text:
        fail("remover must require explicit --apply for deletes")
    if 'mode.add_argument("--dry-run", action="store_true"' not in text:
        fail("remover must make apply and dry-run mutually exclusive")
    if 'validate_hermes_home(hermes_home, args.i_know_this_is_production)' not in text:
        fail("remover must validate the Hermes home target")
    if 'apply = bool(args.apply)' not in text:
        fail("remover must derive delete mode only from --apply")
    if 'Path("skills") / "config-kit"' not in text:
        fail("remover must target only skills/config-kit")
    if 'Path("templates") / "config-kit"' not in text:
        fail("remover must target only templates/config-kit")
    if 'shutil.rmtree(path)' not in text:
        fail("remover directory removal operation missing or unexpectedly changed")


def validate_snapshot() -> None:
    snap = ROOT / "upstream" / "claude-code-config" / "snapshot"
    if not snap.exists():
        fail("upstream snapshot missing; run scripts/sync_upstream.py --sync")
    if not (snap / "README.md").exists():
        fail("upstream snapshot README.md missing")


def validate_quarantine_policy() -> None:
    compat = read_text(ROOT / "mappings" / "compatibility.yaml")
    for prefix in QUARANTINE_PREFIXES:
        if prefix not in compat:
            fail(f"compatibility mapping does not mention quarantine prefix {prefix}")
    generated_paths = [p.relative_to(ROOT).as_posix() for p in (ROOT / "hermes").rglob("*") if p.is_file()]
    leaked = [p for p in generated_paths if any(part in p for part in ("hooks/", "scripts/", ".claude-plugin/"))]
    if leaked:
        fail("quarantined upstream artefacts leaked into generated Hermes tree: " + ", ".join(leaked))


def validate_docs() -> None:
    for rel in ["INSTALL.md", "SECURITY.md", "README.md", "PORTING_BACKLOG.md"]:
        if not (ROOT / rel).exists():
            fail(f"{rel} missing")
    install = read_text(ROOT / "INSTALL.md")
    security = read_text(ROOT / "SECURITY.md")
    backlog = read_text(ROOT / "PORTING_BACKLOG.md")
    if "Disposable VM" not in install:
        fail("INSTALL.md must document disposable VM testing")
    if "Do not use the operator's live Hermes profile" not in install:
        fail("INSTALL.md must warn against production profile testing")
    if "treated as data, not as executable authority" not in security:
        fail("SECURITY.md must document upstream trust model")
    if "Porting backlog and handoff" not in backlog:
        fail("PORTING_BACKLOG.md must document omitted artefacts and handoff")
    if "Wave 4 — hook and workflow redesign" not in backlog:
        fail("PORTING_BACKLOG.md must document hook/workflow redesign backlog")


def validate_secret_scan() -> None:
    scanned_roots = [ROOT / "hermes", ROOT / "mappings", ROOT / "scripts", ROOT / ".github", ROOT / "INSTALL.md", ROOT / "SECURITY.md", ROOT / "README.md", ROOT / "PORTING_BACKLOG.md"]
    hits: list[str] = []
    for root in scanned_roots:
        paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
        for path in paths:
            text = try_read_text(path)
            if text is None:
                continue
            for pattern in SENSITIVE_PATTERNS:
                if re.search(pattern, text):
                    hits.append(str(path.relative_to(ROOT)))
                    break
    if hits:
        fail("possible credential pattern found in adapter-controlled files: " + ", ".join(sorted(set(hits))))


def main() -> int:
    validate_lock()
    validate_snapshot()
    validate_skills()
    validate_templates()
    validate_no_live_writes_default()
    validate_installer_contract()
    validate_remover_contract()
    validate_quarantine_policy()
    validate_docs()
    validate_secret_scan()
    print("Validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
