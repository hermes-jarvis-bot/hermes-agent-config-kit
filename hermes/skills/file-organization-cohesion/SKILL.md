---
name: file-organization-cohesion
description: "Keep durable project artefacts in the established hierarchy, group related work together, and separate disposable scratch output from retained state."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/file-organization-cohesion.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# File Organization Cohesion

Source: `AnastasiyaW/claude-code-config/rules/file-organization-cohesion.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# File Organization Cohesion

Use this module when creating, moving, saving, or retaining durable project artefacts. It keeps project state navigable by placing each artefact in its established home and keeping related material together. It is guidance only: it does not install file watchers, activate hooks, move files, or override project retention policy.

## Placement decision

Before writing a durable artefact, identify its owner, lifecycle, and existing project convention. Prefer a repository, project-local documentation tree, named handoff area, data directory, or other verified home over a convenient but disconnected location.

Use the narrowest existing convention that fits. Do not create a new top-level directory merely to avoid inspecting nearby structure.

## Cohesion rules

1. Keep artefacts for one task, feature, experiment, or handoff within one predictable directory branch.
2. Follow neighbouring naming, layout, and ownership conventions when they are known to be current.
3. Store durable code, documentation, configuration, data, results, and decisions in their retained project location from the outset.
4. Use a uniquely named temporary workspace only for genuinely disposable logs, probes, generated intermediates, and verification harnesses.
5. Before closing the task, review newly created artefacts and relocate or remove only with the applicable project policy and required operator confirmation.

## Read-only preflight

Before proposing a write or relocation:

1. Inspect the repository layout, project guidance, relevant manifests, and nearby artefacts.
2. Distinguish retained state from disposable output; do not infer lifecycle from a directory name alone.
3. Check whether an existing feature, run, handoff, dataset, or documentation area already owns the material.
4. For shared or remote storage, identify the owner, access boundary, backup expectation, and consumer path.
5. If no suitable home is established, report the gap and propose the smallest explicit convention rather than scattering files across convenience paths.

## Boundary and verification

Temporary verification artefacts may live under a uniquely named temporary directory and should be cleaned up after the check. Do not treat temporary storage as a durable archive, and do not move or delete retained material without the required approval.

After an authorised placement or relocation, verify that the intended path contains the expected artefact, references resolve, and no stale duplicate became an accidental source of truth.

## Relationship to other modules

- Use `feature-layer-architecture` for long-running project knowledge layout.
- Use `git-source-of-truth` for retained repository state and commit discipline.
- Use `folder-lifecycle-classification` before archival or cleanup proposals.
- Use `documentation-integrity` when paths, references, or generated lists must remain current.

## Reporting

Report the artefact category, selected retained or temporary location, convention evidence, related artefacts kept together, any lifecycle uncertainty, and the verification or confirmation point. A tidy path is useful only when future operators can find and trust it.
