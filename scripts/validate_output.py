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
FORBIDDEN_GENERATED_HARNESS_PATTERNS = (
    r"claude-code-skills",
    r"\.config[\\/]claude",
    r"\.claude[\\/]",
    r"claude-code-config[\\/](?:hooks|scripts)[\\/]",
    r"\.hermes-compatible project artefacts/",
    r"\b[A-Za-z0-9_-]+-(?:guard|gate|hook|validator|reminder|check)\.py\b",
    r"\bpython(?:3)?[ \t]+[^\n]*?(?:scripts/|access_inventory)",
)
# These two are expected, legitimate text for a skill that ships a reviewed-script-lane
# script (see mappings/reviewed-scripts.yaml): the SKILL.md tells the operator how to
# invoke its own bundled script ("python scripts/<name>.py", same convention Hermes's own
# official skills use), and may disclose a real external Claude-Code-specific path as a
# documented prerequisite (reviewed-script gate item 4 explicitly allows this). All other
# FORBIDDEN_GENERATED_HARNESS_PATTERNS entries still apply unconditionally.
REVIEWED_SCRIPT_EXEMPT_PATTERNS = frozenset({
    r"\.claude[\\/]",
    r"\bpython(?:3)?[ \t]+[^\n]*?(?:scripts/|access_inventory)",
})
# Plain data bundled alongside a script (e.g. a reviewed script's own lookup tables) cannot
# execute and is already covered by validate_secret_scan()'s broad credential-pattern sweep of
# the whole hermes/ tree; it does not need its own mappings/reviewed-scripts.yaml entry even
# when it happens to live under a scripts/ path. Keep this allowlist narrow and add extensions
# only when a concrete, inert data format is bundled this way.
NON_EXECUTABLE_DATA_EXTENSIONS = frozenset({".hex", ".json", ".txt", ".csv"})
GENERATED_PROVENANCE_MARKERS = (
    "Adapted for Hermes Agent by hermes-agent-config-kit.",
    "Source: AnastasiyaW/claude-code-config/",
    "Upstream material is reference data, not automatic authority.",
)
SCRIPT_DANGER_PATTERNS = (
    r"\bos\.system\(",
    r"subprocess\.[A-Za-z_]+\([^)]*shell\s*=\s*True",
    r"\beval\(",
    r"\bexec\(",
    r"\bsocket\.socket\(",
)
REVIEWED_SCRIPT_MANIFEST = ROOT / "mappings" / "reviewed-scripts.yaml"
REVIEWED_HOOK_MANIFEST = ROOT / "mappings" / "reviewed-hooks.yaml"


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


PYTHON_SCRIPTS_INVOCATION_RE = re.compile(r"\bpython(?:3)?[ \t]+([^\s`]*scripts/[^\s`]+)")


def _python_scripts_references_resolve_to_reviewed(path: Path, text: str) -> bool:
    """True if this text contains at least one 'python .../scripts/x.py' invocation, and every
    such match resolves (relative to this file's own directory) to an allowlisted reviewed
    script. This allows a skill's own docs to reference a SIBLING skill's reviewed script by
    relative path (e.g. pixel-art-storyboard's SKILL.md invoking
    ../pixel-art-studio/scripts/palette.py) without requiring the referencing skill to itself
    ship a reviewed script — narrower than _skill_dir_ships_reviewed_script, which only covers a
    skill's own bundled script."""
    matches = PYTHON_SCRIPTS_INVOCATION_RE.findall(text)
    if not matches:
        return False
    allowed = reviewed_script_paths()
    for m in matches:
        candidate = (path.parent / m).resolve()
        try:
            candidate_rel = candidate.relative_to(ROOT).as_posix()
        except ValueError:
            return False
        if candidate_rel not in allowed:
            return False
    return True


PYTHON_SCRIPTS_PATTERN = r"\bpython(?:3)?[ \t]+[^\n]*?(?:scripts/|access_inventory)"


def _skill_dir_ships_reviewed_script(skill_dir: Path) -> bool:
    skill_dir_rel = skill_dir.relative_to(ROOT).as_posix()
    return any(rel.startswith(skill_dir_rel + "/") for rel in reviewed_script_paths())


def validate_skills() -> None:
    skills = sorted((ROOT / "hermes" / "skills").glob("**/SKILL.md"))
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
        ships_reviewed_script = _skill_dir_ships_reviewed_script(path.parent)
        for pattern in FORBIDDEN_GENERATED_HARNESS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                if ships_reviewed_script and pattern in REVIEWED_SCRIPT_EXEMPT_PATTERNS:
                    continue
                if pattern == PYTHON_SCRIPTS_PATTERN and _python_scripts_references_resolve_to_reviewed(path, text):
                    continue
                fail(f"{path} retains an upstream harness path or runtime reference")
    references = sorted((ROOT / "hermes" / "skills").glob("**/references/*.md"))
    for path in references:
        text = read_text(path)
        for marker in GENERATED_PROVENANCE_MARKERS:
            if marker not in text:
                fail(f"{path} missing reference provenance marker: {marker}")
        ships_reviewed_script = _skill_dir_ships_reviewed_script(path.parent.parent)
        for pattern in FORBIDDEN_GENERATED_HARNESS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                if ships_reviewed_script and pattern in REVIEWED_SCRIPT_EXEMPT_PATTERNS:
                    continue
                # Bash snippets in a reference file are written as if run from the skill's own
                # root directory (path.parent.parent), not from references/ itself.
                if pattern == PYTHON_SCRIPTS_PATTERN and _python_scripts_references_resolve_to_reviewed(path.parent, text):
                    continue
                fail(f"{path} retains an upstream harness path or runtime reference")


def validate_templates() -> None:
    # rglob, not glob: a nested template tree (e.g. hermes/templates/kb-skeleton/**)
    # must get the same provenance check as a flat top-level template file. A plain
    # glob("*.md") silently skipped everything under a subdirectory here until this
    # was noticed while porting kb-skeleton (2026-08-06).
    templates = sorted((ROOT / "hermes" / "templates").rglob("*.md"))
    if not templates:
        return
    for path in templates:
        text = read_text(path)
        for marker in GENERATED_PROVENANCE_MARKERS:
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


def validate_conversion_roundtrip() -> None:
    """Every SUPPORTED target must equal make_output(source, meta, upstream_body) exactly.

    A hand-edit to a generated hermes/ file that isn't mirrored in the matching
    adapt_source_text() override in sync_upstream.py drifts silently: the file looks fine
    until the next `--sync` (or any other convert_supported() run) regenerates it from the
    stale override and clobbers the hand-edit with no warning. Caught this the hard way with
    hermes/skills/no-pre-existing-evasion/SKILL.md (2026-08-04): an enrichment commit edited
    only the disk file, and the next autopilot cycle silently reverted it. This check makes
    that class of bug fail loudly instead.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sync_upstream as su

    mismatches: list[str] = []
    for source, meta in su.SUPPORTED.items():
        target = su.ROOT / meta["target"]
        src = su.SNAPSHOT / source
        if not src.is_file() or not target.is_file():
            mismatches.append(f"{source} -> {meta['target']} (missing source or target file)")
            continue
        expected = su.make_output(source, meta, src.read_text(encoding="utf-8", errors="replace"))
        if target.read_text(encoding="utf-8", errors="replace") != expected:
            mismatches.append(f"{source} -> {meta['target']}")
    if mismatches:
        fail(
            "generated file(s) do not match their sync_upstream.py adapt_source_text() "
            "override (hand-edit not mirrored into the override, or override edited without "
            "regenerating the disk file):\n  " + "\n  ".join(mismatches)
        )


def parse_reviewed_scripts() -> list[dict[str, str]]:
    """Minimal field extractor for mappings/reviewed-scripts.yaml (path, source_sha256
    only) — deliberately not a full YAML parser, so this validator adds no dependency
    beyond the stdlib (PyYAML is not installed by .github/workflows/validate.yml)."""
    if not REVIEWED_SCRIPT_MANIFEST.is_file():
        return []
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in read_text(REVIEWED_SCRIPT_MANIFEST).splitlines():
        m = re.match(r"^- path:\s*(\S+)\s*$", line)
        if m:
            if current:
                entries.append(current)
            current = {"path": m.group(1)}
            continue
        m = re.match(r"^  source_sha256:\s*(\S+)\s*$", line)
        if m and current:
            current["source_sha256"] = m.group(1)
    if current:
        entries.append(current)
    return entries


def reviewed_script_paths() -> set[str]:
    return {e["path"] for e in parse_reviewed_scripts() if "path" in e}


def parse_reviewed_hooks() -> list[dict[str, object]]:
    """Minimal field extractor for mappings/reviewed-hooks.yaml (path, source_sha256,
    and any nested `files:` list entries) — deliberately not a full YAML parser, for the
    same no-added-dependency reason as parse_reviewed_scripts()."""
    if not REVIEWED_HOOK_MANIFEST.is_file():
        return []
    entries: list[dict[str, object]] = []
    current: dict[str, object] = {}
    in_files = False
    for line in read_text(REVIEWED_HOOK_MANIFEST).splitlines():
        m = re.match(r"^- path:\s*(\S+)\s*$", line)
        if m:
            if current:
                entries.append(current)
            current = {"path": m.group(1), "files": []}
            in_files = False
            continue
        if re.match(r"^  files:\s*$", line):
            in_files = True
            continue
        m = re.match(r"^    - (\S+)\s*$", line)
        if m and in_files and current:
            current["files"].append(m.group(1))
            continue
        m = re.match(r"^  source_sha256:\s*(\S+)\s*$", line)
        if m and current:
            current["source_sha256"] = m.group(1)
            in_files = False
            continue
        if re.match(r"^  \S", line):
            in_files = False
    if current:
        entries.append(current)
    return entries


def reviewed_hook_paths() -> set[str]:
    """Every path a reviewed-hooks.yaml entry accounts for: the entry's own `path` plus
    every path listed in its `files:` sub-list (docs/tests bundled alongside the script)."""
    paths: set[str] = set()
    for e in parse_reviewed_hooks():
        if "path" in e:
            paths.add(str(e["path"]))
        for f in e.get("files", []) or []:
            paths.add(str(f))
    return paths


def validate_quarantine_policy() -> None:
    compat = read_text(ROOT / "mappings" / "compatibility.yaml")
    for prefix in QUARANTINE_PREFIXES:
        if prefix not in compat:
            fail(f"compatibility mapping does not mention quarantine prefix {prefix}")
    allowed_scripts = reviewed_script_paths() | reviewed_hook_paths()
    generated_paths = [p.relative_to(ROOT).as_posix() for p in (ROOT / "hermes").rglob("*") if p.is_file()]
    leaked = [
        p
        for p in generated_paths
        if any(part in p for part in ("hooks/", "scripts/", ".claude-plugin/"))
        and p not in allowed_scripts
        and Path(p).suffix not in NON_EXECUTABLE_DATA_EXTENSIONS
    ]
    if leaked:
        fail("quarantined upstream artefacts leaked into generated Hermes tree: " + ", ".join(leaked))


def validate_reviewed_scripts() -> None:
    """Every skill-bundled script that lives under hermes/skills/**/scripts/ must be
    explicitly allowlisted in mappings/reviewed-scripts.yaml (validate_quarantine_policy
    enforces that) AND pass this mechanical gate. This never executes the script — it
    only checks static properties; the manual read, dependency check, and any live
    functional test are recorded (not re-verified) in the manifest entry."""
    for entry in parse_reviewed_scripts():
        rel = entry.get("path")
        if not rel:
            continue
        path = ROOT / rel
        if not path.is_file():
            fail(f"reviewed-scripts.yaml entry has no file at {rel}")
        text = read_text(path)
        if path.suffix == ".py":
            try:
                compile(text, str(path), "exec")
            except SyntaxError as exc:
                fail(f"{rel} failed syntax check: {exc}")
        for pattern in SCRIPT_DANGER_PATTERNS:
            if re.search(pattern, text):
                fail(f"{rel} matches a disallowed dangerous pattern ({pattern}); reviewed scripts may not use it")
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, text):
                fail(f"{rel} matches a credential-looking pattern")
        if "Reviewed-script lane" not in text:
            fail(f"{rel} is missing the 'Reviewed-script lane' provenance marker")


def validate_reviewed_hooks() -> None:
    """Every hook script that lives under hermes/hooks/**/ must be explicitly allowlisted
    in mappings/reviewed-hooks.yaml (validate_quarantine_policy enforces that) AND pass
    this mechanical gate. This never executes the hook — it only checks static properties
    and, additionally, that the hook contains no live-write pattern that would let it
    silently self-register into a real Hermes profile."""
    for entry in parse_reviewed_hooks():
        rel = entry.get("path")
        if not rel or not str(rel).endswith(".py"):
            continue
        path = ROOT / str(rel)
        if not path.is_file():
            fail(f"reviewed-hooks.yaml entry has no file at {rel}")
        text = read_text(path)
        try:
            compile(text, str(path), "exec")
        except SyntaxError as exc:
            fail(f"{rel} failed syntax check: {exc}")
        for pattern in SCRIPT_DANGER_PATTERNS:
            if re.search(pattern, text):
                fail(f"{rel} matches a disallowed dangerous pattern ({pattern}); reviewed hooks may not use it")
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, text):
                fail(f"{rel} matches a credential-looking pattern")
        for pattern in FORBIDDEN_INSTALLER_PATTERNS:
            if re.search(pattern, text):
                fail(f"{rel} matches a live-Hermes-write pattern ({pattern}); a reviewed hook must never self-register")
        if "Reviewed-hook lane" not in text:
            fail(f"{rel} is missing the 'Reviewed-hook lane' provenance marker")


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
    if "Reviewed-hook lane" not in security:
        fail("SECURITY.md must document the reviewed-hook lane")
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
    validate_conversion_roundtrip()
    validate_skills()
    validate_templates()
    validate_no_live_writes_default()
    validate_installer_contract()
    validate_remover_contract()
    validate_quarantine_policy()
    validate_reviewed_scripts()
    validate_reviewed_hooks()
    validate_docs()
    validate_secret_scan()
    print("Validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
