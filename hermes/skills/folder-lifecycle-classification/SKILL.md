---
name: folder-lifecycle-classification
description: "Classify project directories by recoverability and cleanup risk before proposing any archival or deletion action."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/folder-lifecycle-labels.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Folder Lifecycle Classification

Source: `AnastasiyaW/claude-code-config/rules/folder-lifecycle-labels.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Folder Lifecycle Classification

This module provides a small, review-first vocabulary for describing directory recoverability. It is planning guidance only: it does not create marker files, run cleanup routines, delete directories, or override the operator's retention policy.

## When to use

Use it before proposing archival, cleanup, relocation, or deletion of a non-obvious project directory, especially when its name alone does not establish whether it is reproducible or contains manual work.

For the actual destructive-action protocol, use `safe-deletion`. Classification is evidence for a decision, not permission to carry it out.

## Classification vocabulary

Assign the narrowest supported classification after inspection:

| Classification | Meaning | Default treatment |
| --- | --- | --- |
| project root | Deliberate repository or worktree root | Never bulk-delete. |
| git-backed | Reconstructible clone with a verified clean state and reachable remote | Preserve until repository state and remote are verified. |
| reproducible temporary | Scratch, probe, or test output with a known producer | Eligible only for a scoped cleanup proposal after checking no process uses it. |
| rebuildable dataset | Downloaded or generated data backed by verified manifests, source, hashes, and rebuild instructions | Preserve source-of-truth material; require verification before any cleanup proposal. |
| generated cache | Rebuildable cache, build, model, or download output | Confirm the producer and any active consumer first. |
| regenerable artefact | Report, preview, or derived output with preserved source and generation method | Preserve the source and regeneration evidence first. |
| manual or irreplaceable | Operator-created, unique, or otherwise non-reconstructible material | Do not propose bulk deletion without explicit operator confirmation. |
| needs review | Recoverability is uncertain | Stop classification and inspect further. |

Use project-local metadata only when the project already has an approved convention. Do not introduce a marker schema merely to make a one-off cleanup look official.

## Read-only assessment protocol

1. Identify the directory's owner, purpose, and whether it is a project root, disposable workspace, cache, or data store.
2. Inspect source control, manifests, generation commands, provenance, and retention documentation.
3. Check for active processes, mounts, containers, locks, or consumers before treating a path as idle.
4. Verify the claimed source of truth: a clean remote repository, readable manifest, reproducible command, or retained original data.
5. Record uncertainty as `needs review`; names such as `tmp`, `cache`, or `old` are clues, not proof.

## Decision boundary

Classification does not change the write-impacting policy:

- Never delete or move a project root, manual material, or uncertain directory automatically.
- For a reproducible path, propose the exact scope, recovery evidence, and verification check before requesting the required operator confirmation.
- Before removing a copy after transfer, verify the destination content and integrity first.
- After an authorised action, verify the intended path state and report any remaining recovery route.

## Reporting

Report the path, classification, evidence for recoverability, active-consumer check, retention or recovery route, uncertainty, and any confirmation point. If evidence is incomplete, retain the directory and report the classification gap.
