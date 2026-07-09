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
