---
name: documentation-integrity
description: "Treat stale documentation references as correctness faults; verify docs, paths, commands, and generated state before relying on them."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/11-documentation-integrity.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Documentation Integrity

Source: `AnastasiyaW/claude-code-config/principles/11-documentation-integrity.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Documentation Integrity

Upstream source policy was written for a different harness with session-start hooks. Hermes adaptation keeps the principle and removes automatic hook wiring: stale references are correctness faults, and documentation must be verified before it is used as authority.

## Principle

Documentation drift is operational drift. A README, AGENTS file, backlog, skill, or generated artefact that points at a stale path, stale command, stale count, or stale workflow can make an agent perform the wrong action confidently.

Treat broken documentation references like failing tests, not like harmless prose.

## When to apply

Use this module when:

- changing generated skills, mappings, installers, removers, workflows, or repo layout;
- relying on documented commands, file paths, ports, endpoints, or counts;
- preparing release notes, handoffs, or migration backlog updates;
- onboarding another agent/session from project documentation;
- seeing disagreement between docs and live telemetry.

## Verification protocol

Before acting on documentation or declaring docs updated:

1. Check referenced paths exist or are intentionally illustrative.
2. Check documented commands still exist and run, or clearly mark them as examples.
3. Check counts and tables match the source of truth.
4. Check generated artefacts match converter output after regeneration.
5. Check external claims with read-back where practical: CI URLs, release tags, issue/PR links, service ports, or API endpoints.

Prefer high-precision checks over noisy broad scans. Bare filenames such as `README.md` can be examples; explicit paths such as `scripts/install_hermes.py`, `hermes/skills/foo/SKILL.md`, or `/etc/service/config.yaml` should be validated.

## Hermes adapter checks

For this kit, keep these files in sync when porting a module:

- `scripts/sync_upstream.py` — supported source path, target path, name, description, source-specific adaptation if needed;
- `mappings/compatibility.yaml` — status, type, target, risk;
- `hermes/skills/<name>/SKILL.md` — generated output and frontmatter;
- `PORTING_BACKLOG.md` — totals, ported table, not-yet-ported lane, Wave candidate lists;
- `AGENTS.md` — generated skill list and operating contract.

Run focused ad-hoc verification when no canonical suite covers the change. The verifier should copy the repo to a temp directory, regenerate outputs, compare stability, and dry-run/apply/remove against a disposable Hermes home.

## Reporting

Report documentation integrity with evidence:

- `path reference verified: <path>`;
- `command verified: <command>`;
- `count reconciled: 16 generated skills`;
- `generated artefact stable after regeneration`;
- `external URL read back successfully`.

If a reference is stale or unchecked, say so. Do not treat documentation as authority merely because it is well formatted. Elegant markdown can still be confidently wrong.

## What this module does not do

This module does not install hooks, validators, or scheduled checks automatically. Any automated documentation validator must be designed as a separate Hermes-native routine and reviewed before activation.
