---
name: deslop
description: "Remove AI-generated code noise from the current diff while preserving behavior."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/deslop/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Deslop

Source: `AnastasiyaW/claude-code-config/skills/development/deslop/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Deslop

Review only the branch diff against its intended base and remove noise that does not belong in the local code style. Keep the behavior and public contract unchanged unless a clear, separately verified bug is fixed.

This module is a narrower, lighter tier than `lean-code`: it cleans up noise already present in a diff (typically agent-generated) rather than deciding, before writing code, whether a piece of work should exist at all.

## Review targets

- comments that narrate obvious code or contradict local conventions;
- defensive checks or catch blocks abnormal for a trusted path;
- `any`, unsafe casts, or optionality used only to silence a type checker;
- deep nesting that can be made clearer with early returns or a named helper;
- one-off wrappers, flags, and branches inconsistent with the surrounding module;
- C++ ownership or error-handling scaffolding that is redundant with the established RAII/contract boundary.

## Workflow

1. Inspect the base, diff, local style, tests, and ownership boundaries.
2. Classify each candidate as noise, a clear bug, or an intentional contract.
3. Remove only confirmed noise in a focused edit.
4. Run the narrow relevant checks and inspect the final diff.
5. If the structure needs a real redesign, stop deslop and use `refactoring-safely`, `architecture-first`, or `thermo-nuclear-code-quality-review` instead.

Do not delete comments that explain a non-obvious invariant, security boundary, ABI constraint, workaround with an owner, or externally required behavior.

## Gotchas

- Shorter code is not automatically clearer; preserve names and boundaries that carry domain meaning.
- A broad formatter run can hide behavior changes and is not deslop proof.
- Removing a defensive check without proving the trusted-path invariant can turn cleanup into a regression.
- In C++, exception and ownership code may look repetitive while protecting an ABI or lifetime boundary; inspect callers before removing it.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Cleanup changes a test result | Candidate was behavior, not noise | Revert that candidate and isolate the real contract |
| Diff is too broad | Tool ran over the whole tree | Restrict review to the branch diff and restore unrelated files |
| Comment seems redundant but explains a constraint | Context is outside the file | Read the owning docs/tests before changing it |
| Code remains structurally tangled | Deslop is the wrong scope | Escalate to a planned refactor with characterization tests |

## Provenance

Adapted from Cursor Team Kit's MIT-licensed `deslop` workflow: `github.com/cursor/plugins/tree/main/cursor-team-kit/skills/deslop`. Upstream's cross-reference to `architecture-quality` was retargeted to `architecture-first`, the closest module this adapter actually ports.
