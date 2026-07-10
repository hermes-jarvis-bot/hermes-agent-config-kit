---
name: merge-conflict-resolution
description: "Resolve Git, rebase, cherry-pick, sync, and parallel-work conflicts with evidence, intent preservation, and independent verification."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/24-merge-conflict-resolution.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Merge Conflict Resolution

Source: `AnastasiyaW/claude-code-config/principles/24-merge-conflict-resolution.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Merge Conflict Resolution

Upstream source policy describes conflict resolution as an evidence problem rather than a taste problem. Hermes adaptation keeps the conflict protocol and removes incident-specific harness assumptions. This module does not install hooks, merge drivers, daemons, or automatic conflict resolvers.

## Principle

Do not resolve conflicts by intuition.

A conflict means two sources of project state disagree. The task is to preserve the valid intent from each side, backed by evidence, then verify the synthesized result.

Use this module for:

- Git merge conflicts;
- rebase or cherry-pick conflicts;
- auto-resolved hunks that may still be semantically wrong;
- parallel human/agent edits to the same files;
- local source diverging from deployed or generated state;
- configuration, schema, or documentation conflicts where both versions appear plausible.

For trivial mechanical conflicts, keep the protocol lightweight, but still inspect and verify. A one-line conflict can still erase a production fix with impeccable efficiency.

## Stop before editing

When conflict markers or suspicious auto-resolutions appear:

1. Stop making unrelated edits.
2. Record the conflicted files and commands that produced the conflict.
3. Inspect repository state with `git status --short --branch`.
4. Identify whether any unrelated operator work is present.
5. Gather evidence before choosing sides.

Do not immediately run broad formatters, bulk rewrites, or cleanup. They make the conflict harder to audit.

## Evidence sources

Prefer evidence in this order:

1. **Current executable checks** — build, lint, unit tests, smoke tests, targeted probes.
2. **Running/deployed state** — only when accessible and explicitly relevant.
3. **Generated artefact source of truth** — converter output, schema generator, lockfile producer.
4. **Git history** — `git log -p`, blame, related commits, branch intent.
5. **Surrounding code** — current call sites, tests, and data model.
6. **Documentation** — useful, but verify because it may be stale.

If access to a required source is missing, say so and lower confidence rather than guessing.

## Hunk protocol

For each non-trivial hunk:

1. Label each side clearly: ours/theirs, branch names, or source names.
2. Explain what each side is trying to preserve.
3. Identify tests, probes, or history supporting each intent.
4. Prefer synthesis over wholesale selection when both sides have valid intent.
5. Keep the smallest resolution that preserves both behaviours.
6. Re-read the resolved file around the hunk, not just the hunk itself.

Examples:

- If one side adds validation and the other refactors the call site, keep the refactor and preserve the validation.
- If one side renames a symbol and the other adds a new use, update the new use to the renamed symbol.
- If two error messages changed, keep the more informative message unless tests or API compatibility require exact text.

## Independent verification

For non-trivial conflicts, use a fresh-context reviewer when practical. The reviewer should receive:

- the resolved file or diff;
- the original conflict sides;
- the intended behaviours to preserve;
- the relevant tests or commands.

Ask the reviewer to answer:

1. Is the resolved file syntactically valid?
2. Does the resolution preserve side A's intent?
3. Does it preserve side B's intent?
4. Are there accidental edits outside the conflict area?
5. Which command output supports the conclusion?

If reviewer and resolver disagree, gather more evidence. Do not settle disagreement with confidence alone.

## Post-resolution checks

After resolving:

1. Check conflict markers are gone:

```bash
grep -RInE '^(<{7}|>{7}|={7}\s*$)' -- .
```

Scope this command if the repository is large or contains vendored/generated files.

2. Inspect the diff:

```bash
git diff --check
git diff -- <resolved paths>
```

3. Run the narrowest meaningful build, lint, or test command.
4. Run broader verification if the conflict touched shared contracts, schemas, or public APIs.
5. Confirm no unrelated files changed because of formatting, generation, or editor actions.

Errors are stronger evidence than agent consensus. If checks fail, reopen the resolution.

## Relationship to other modules

- Use `git-source-of-truth` to preserve resolved state in commits and remote read-back.
- Use `multi-session-coordination` when conflicts come from parallel sessions sharing resources.
- Use `inter-agent-communication` when another session needs a directed question or review request.
- Use `proof-loop` and `independent-verification` for reviewer freshness and behavioural evidence.
- Use `documentation-integrity` when documentation, generated state, or comments are part of the conflict.

## Avoid

- Taking “ours” or “theirs” because it is newer, local, or feels cleaner.
- Trusting auto-merge tools without reading the resolved hunk.
- Running formatters before understanding the conflict.
- Resolving semantic conflicts from conflict markers alone.
- Claiming success without marker checks, diff review, and at least one relevant verification command.
- Treating deployed state as authoritative without checking whether it represents an approved hotfix or accidental drift.

## Reporting format

When using this module, report:

- conflicted files;
- conflict source: merge, rebase, cherry-pick, sync, or parallel edit;
- evidence consulted;
- resolution strategy for important hunks;
- verification commands and outputs;
- independent review result if used;
- remaining uncertainty or follow-up.

A merge conflict is not Git being difficult. It is Git politely asking you not to delete someone else's work by accident.
