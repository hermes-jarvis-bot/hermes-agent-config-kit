---
name: supply-chain-defense
description: "Reduce package and upstream adapter risk with freshness gates, lockfiles, provenance checks, and quarantine boundaries."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/09-supply-chain-defense.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Supply Chain Defense

Source: `AnastasiyaW/claude-code-config/principles/09-supply-chain-defense.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Supply Chain Defense

Upstream source policy focuses on package freshness. Hermes adaptation applies the same principle to package managers, CI, generated adapter output, and upstream snapshot ingestion.

## Principle

Treat dependencies and upstream artefacts as supply-chain inputs, not trusted configuration. Prefer delayed adoption, pinned inputs, reproducible installs, and explicit review of executable material.

## Package freshness

When installing public packages, prefer a seven-day freshness gate where the ecosystem supports it:

- npm: use `min-release-age=7` in project or runner configuration;
- uv: use `exclude-newer = "7 days"` where appropriate;
- pip-only environments: pin exact versions and review update diffs manually;
- cargo/go: rely on lockfiles, audit tools, checksum verification, and reviewed diffs.

Do not write global package-manager configuration without operator approval. Prefer project-local configuration or disposable CI/test environments first.

## Defense in depth

- Commit and review lockfiles: `package-lock.json`, `uv.lock`, `Cargo.lock`, `go.sum`.
- Prefer exact versions for operational tooling.
- Run audit/provenance checks where available.
- Minimise dependency count; every dependency is operational attack surface.
- Inspect package names, scopes, publishers, and typosquatting risk before adding new packages.
- Treat install scripts and postinstall hooks as executable code.

## Runtime enforcement posture

Treat a dependency-manifest edit and an install/download command as boundaries worth checking mechanically, not just documenting:

- On a manifest edit, check candidate names against a typosquat/slopsquat profile, reject releases younger than the freshness gate, and flag stale exact pins that could be updated.
- Before an install/download runs, require the canonical registry — not a direct wheel/archive/Git URL, an extra index, or a find-links source — unless that source has been reviewed and recorded independently. Require an artifact digest for pinned versions, and prefer hash-locked installs (`pip install --require-hashes`, `uv sync --locked`, `npm ci` with install scripts disabled) over unlocked ones.
- **Registry silence is a block, not a warning.** If the canonical registry cannot be reached, do not assume the package is fine — use a previously verified record only if one exists and is recent, and stop the install otherwise. A lockfile hash is independent offline proof for an already-reviewed lock; it is not permission to add a new, unreviewed package.
- Do not infer safety from a URL or publisher string alone. A private mirror, a direct artifact, or a Git revision needs the same independent review as a fresh package name.

When a requested package name looks mistyped or fails to resolve, search the official registry surface for close matches rather than guessing a substitute. A candidate is only worth considering if its stable release clears the same freshness gate and has a verifiable artifact digest — it still needs the project's normal compatibility testing before adoption.

## Version selection policy

For a new dependency, prefer the newest stable version the canonical registry offers, tested against the actual project. Treat a deliberately older pin as an exception that needs a stated reason — a supported runtime version, an ABI/CUDA boundary, a failing test — not a default choice made out of familiarity.

If an upgrade breaks something, record the failing test and roll back to the last known-good pin rather than silently keeping the old version. The goal is not an automatic, unverified upgrade or rollback — that just trades one supply-chain risk for an untested compatibility change; a human or a tested CI run should confirm the new pin.

## Hermes adapter boundary

For adapter repositories such as this kit:

1. Pin upstream snapshots by commit SHA.
2. Auto-convert only allowlisted markdown artefacts.
3. Keep hooks, scripts, plugin descriptors, and CI workflows in review/quarantine lanes.
4. Never copy upstream executable workflow files into active project automation without review.
5. Validate generated output with path-safety, secret-scan, and install/remove smoke checks.
6. Read back CI/check-run status after publishing changes.

## Exceptions

A same-day package release may be justified for an urgent security fix, but treat that as an explicit exception:

- identify the exact package and version;
- verify publisher, changelog, provenance, and advisory context;
- install in a disposable environment first;
- record why the freshness gate was bypassed.

## Reporting

Report supply-chain decisions as evidence, not reassurance:

- `lockfile diff reviewed`;
- `package age gate applied`;
- `upstream snapshot pinned to <sha>`;
- `executable artefact left in quarantine lane`;
- `CI validation read back as success`.

If a dependency, package release, or upstream artefact has not been reviewed, say so before using it in a write-impacting protocol.
