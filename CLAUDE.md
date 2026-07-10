# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read AGENTS.md first

`AGENTS.md` is the primary, authoritative agent operating guide for this repository — it is more detailed and more operational than this file. Read it in full before editing anything here. This file only summarizes what's needed to get moving quickly; where the two disagree, `AGENTS.md` wins.

## What this repository is

An **adapter**, not a fork. It selectively ports proven agent-harness patterns (principles, rules, one skill) from the upstream repo `AnastasiyaW/claude-code-config` into Hermes Agent-compatible `SKILL.md` files under `hermes/skills/`. Upstream content is treated as data to review and convert, never as executable authority. Hooks, scripts, plugin descriptors, and workflows from upstream are quarantined — they are never auto-converted or auto-executed.

Core pipeline:

```text
upstream claude-code-config
  -> pinned snapshot + range-based sync report   (scripts/sync_upstream.py)
  -> compatibility mapping + risk classification  (mappings/compatibility.yaml)
  -> selected markdown-only Hermes skills          (hermes/skills/*/SKILL.md)
  -> dry-run-first installer                       (scripts/install_hermes.py)
```

## Non-negotiable boundaries

These require explicit operator confirmation before being violated for any specific action/path:

- Never write to `~/.hermes` or any production Hermes profile (from code, tests, or CI).
- Never copy production credentials, `.env`, `auth.json`, gateway tokens, or session/memory stores into a sandbox.
- Never auto-execute upstream hooks, scripts, workflows, or plugin descriptors.
- Only convert artefacts explicitly listed in `scripts/sync_upstream.py:SUPPORTED` and marked `status: supported` in `mappings/compatibility.yaml`.
- Never auto-merge upstream sync changes, and only advance `upstream.lock.json:last_synced_sha` as part of a deliberate, reported sync.
- Never run `--apply` (installer/remover) against a real Hermes home — only against disposable/temp paths.

If in doubt, stop at dry-run and ask the operator.

## Commands

```bash
# Compile check
python3 -m py_compile scripts/*.py

# Canonical local validator (safety policy, frontmatter, quarantine leakage, secret scan)
python3 scripts/validate_output.py

# Inspect upstream without touching anything (non-mutating)
python3 scripts/sync_upstream.py --check

# Sync snapshot + convert supported artefacts + write report + advance lockfile
python3 scripts/sync_upstream.py --sync

# Installer: dry-run must NOT create the target path
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-test

# Installer: real write, temp path only
python3 scripts/install_hermes.py --apply --hermes-home /tmp/hermes-config-kit-test

# Remover: mirrors installer's dry-run/--apply contract
python3 scripts/remove_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-test
python3 scripts/remove_hermes.py --apply --hermes-home /tmp/hermes-config-kit-test
```

Standard post-change verification sequence (matches CI in `.github/workflows/validate.yml`):

```bash
python3 -m py_compile scripts/*.py
python3 scripts/validate_output.py
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-test
test ! -e /tmp/hermes-config-kit-test   # dry-run must not create the path
```

There is no other test suite in this repo — `validate_output.py` plus the installer/remover dry-run/apply/verify cycle *is* the test suite.

## Architecture notes

- **`upstream.lock.json`** is the single source of truth for sync state (`last_synced_sha`, `latest_seen_sha`). Don't rely on memory of what's synced — read this file.
- **`mappings/compatibility.yaml`** maps each upstream source path to a `status` (`supported` / `review` / `unsupported` / `planned`), a `target` Hermes path, and a `risk` level. Only `supported` entries feed the fast (auto-convert) lane.
- **`scripts/sync_upstream.py`** (~3100 lines) is the biggest and most important script: it resolves the latest upstream SHA, diffs against `last_synced_sha`, downloads/extracts the upstream tarball (`filter="data"` required), classifies every changed file into review buckets, converts only `SUPPORTED` entries, and writes `reports/upstream-sync/<timestamp>-<sha>.md` (+ `latest.md`). `--check` must stay non-mutating; `--sync` performs the full pipeline including advancing the lockfile.
- **`scripts/validate_output.py`** is the canonical local safety/correctness gate — it checks lockfile shape, snapshot presence, generated-skill frontmatter, that no generated skill/script encourages live Hermes writes, that quarantined prefixes didn't leak into `hermes/`, and scans for credential-looking patterns.
- **`scripts/install_hermes.py`** / **`scripts/remove_hermes.py`** are small, symmetric, dry-run-first copiers/removers scoped only to `<hermes-home>/skills/config-kit/` and `<hermes-home>/templates/config-kit/`. Neither ever defaults to `~/.hermes`, and neither touches the Hermes gateway.
- **`hermes/skills/*/SKILL.md`** are the generated output artefacts. Each has Hermes-style frontmatter (`name`, `description`, `version`, `license`, `metadata.hermes_config_kit.{source_repo,source_path,adapter,conversion}`) and a body that explicitly states upstream instructions are reference material, not automatic authority.
- **Quarantine lane** (never auto-converted): `hooks/**`, `scripts/**` (upstream's, not this repo's), `.claude-plugin/**`, `.github/workflows/**` from the upstream snapshot, plus anything handling credentials/shell exec/deletion/network/process control.
- **`.github/workflows/`**: `validate.yml` runs the compile+validate+install/remove dry-run/apply cycle on push/PR; `upstream-watch.yml` is the scheduled/manual range-based sync checker that batches multiple upstream commits into a single review PR (never one PR per commit); `manual-sync.yml` is a manual sync entry point.
- **`PORTING_BACKLOG.md`** tracks what was deliberately left unported from upstream (currently 33 of 382 upstream files) and why — check it before adding new conversions to avoid redoing prior review decisions.

## Commit style

Concise conventional commits (`feat:`, `fix:`, `chore:`, `docs:`), kept narrow — don't mix upstream sync, installer behavior, and broad doc rewrites in one commit unless the operator asked for a project-wide update.
