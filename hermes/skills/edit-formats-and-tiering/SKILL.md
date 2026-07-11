---
name: edit-formats-and-tiering
description: "Choose a precise file-edit format, keep planning separate from mechanical application when useful, and verify the resulting diff."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/edit-formats-and-tiering.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Edit Formats And Tiering

Source: `AnastasiyaW/claude-code-config/rules/edit-formats-and-tiering.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Edit Formats and Tiering

Use this module when changing files through an agent interface. It preserves a simple reliability rule: select the smallest edit representation that makes the intended change unambiguous, then verify the result. This is guidance only; it does not select models, activate delegation, apply changes, or alter tool permissions.

## Select the edit format

Choose the format from the change, not from habit:

- **Whole file** — use for a new small file, a generated file, or a deliberate replacement where preserving untouched content is not required.
- **Targeted replacement** — use for a bounded change when the original block is exact and uniquely identifiable. Include sufficient surrounding context to prevent a match in the wrong location.
- **Unified diff** — use when a patch is the required interface or when several nearby, reviewable changes belong in one coherent diff.
- **Plan then apply** — use when the design decision is materially harder than the mechanical edit. Record the intended change first, then apply it through the appropriate file interface.

Do not rewrite an established file merely to change a few lines. Conversely, do not force a fragile partial replacement when a small complete file is clearer and safer.

## Precision protocol

Before a targeted change:

1. Read the current file and identify the exact intended location.
2. Check that the match is unique or add stable context until it is.
3. Separate the semantic decision from mechanical application when review, a second context, or a deterministic interface would reduce risk.
4. Apply the smallest coherent change.
5. Inspect the diff and run the narrowest relevant validation before declaring success.

If the expected original content is absent or ambiguous, stop and re-read the current state. Do not approximate a replacement into a file that may have changed underneath the protocol.

## Tiering without provider assumptions

Some work benefits from a planning pass followed by mechanical application, but this is a task boundary rather than a provider or price rule. Keep the planner focused on intent, constraints, and acceptance evidence; keep the applier focused on an exact, reviewable artefact.

Use a single context for small, unambiguous edits. Use independent review or a separate application step when a change is high-impact, spans several interfaces, is difficult to reverse, or needs stronger evidence. Any delegation, external model use, or billing-impacting action remains subject to the applicable access and operator-confirmation boundary.

## Avoid

- Whole-file rewrites for small local changes without a preservation reason.
- Ambiguous replacements that could affect several locations.
- Treating a plan as a completed change before an artefact and verification exist.
- Selecting an execution strategy from assumed model capability, cost, or provider behaviour rather than the verified task boundary.
- Automatically enabling hooks, scripts, workflows, or background processes to enforce an editing convention.

## Relationships

- Use `code-quality` to keep the implementation proportionate to the requirement.
- Use `proof-loop` and `independent-verification` when the resulting diff needs stronger completion evidence.
- Use `multi-agent-task-decomposition` only when a separate planning or review context materially reduces a real risk.
- Use `safe-deletion` before an edit removes or replaces retained data.

## Reporting

Report the chosen edit format, why its match or scope was safe, the paths changed, diff inspection result, validation evidence, and any approval point. A compact diff is useful only when it is also the right diff.
