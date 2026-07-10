---
name: project-chronicles
description: "Preserve concise, milestone-level decision history for long-running projects without replacing tactical handoffs, source control, or current documentation."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/16-project-chronicles.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Project Chronicles

Source: `AnastasiyaW/claude-code-config/principles/16-project-chronicles.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Project Chronicles

Use a project chronicle to preserve why a long-running project changed direction. A chronicle is a concise, milestone-level decision history. It complements source control, current documentation, and `session-handoff`; it does not replace any of them.

This module is guidance and a data-only template. It does not create files, append entries, load project state automatically, activate hooks, or grant access to a project.

## Applicability gate

Consider a chronicle only when a project spans multiple weeks or sessions and has meaningful decisions, pivots, quantitative milestones, or confirmed dead ends that a future operator would otherwise need to rediscover.

Do not create one for routine maintenance, a short task, or a project whose useful history is already clear from a compact decision log. A second history mechanism without a distinct purpose is merely decorative archaeology.

## Separation of records

Keep each record focused:

| Record | Primary question | Typical update |
| --- | --- | --- |
| Source control and release notes | What changed? | Each committed change or release |
| Current documentation | How does it work now? | When the current design changes |
| `session-handoff` | What should the next session do? | Transfer, compaction, or blocker |
| Project chronicle | Why did the project reach this state? | Significant milestone or pivot |

Do not copy command output, access credentials, full chat transcripts, private incident detail, or unverified claims into a chronicle. Link to reviewed evidence such as a commit, issue, release, test artefact, or documented decision instead.

## Read-only preflight

Before proposing a chronicle or entry:

1. Identify the project owner, authoritative project path, and existing documentation or decision-log convention.
2. Inspect whether a chronicle already exists and whether the proposed fact is already recorded elsewhere.
3. Confirm that a real milestone, decision, pivot, measured outcome, or dead end occurred.
4. Gather durable evidence and separate observed facts from interpretation.
5. Determine whether creating or updating project documentation is write-impacting under the project's own policy.

If the storage location, ownership, retention policy, or evidence is unclear, report the gap. Do not invent a directory convention or write a history file by default.

## Entry content

When an operator approves an update under an established project convention, keep each entry short and strategic:

```markdown
### YYYY-MM-DD — milestone title
Summary: one or two sentences describing the durable change.
- Decision: chosen approach and reason.
- Evidence: commit, issue, test artefact, or release reference.
- Rejected path: only when it prevents useful future rework.
- Follow-up: open decision or linked tactical handoff, if any.
```

An entry should answer what changed in direction and why. It should not become a duplicate changelog or a task diary.

## Lifecycle

- Add an entry only after an evidenced milestone, pivot, decision, measurable outcome, or confirmed dead end.
- Keep entries append-only unless the project owner approves a correction; preserve the correction rationale.
- Periodically add a concise summary or split by completed phase when the chronicle no longer loads efficiently.
- Treat historical entries as context, not live truth. Verify current source control, documentation, services, and external state before acting.
- Archive or retire the chronicle according to the documented project retention policy; do not delete project history automatically.

## Relationship to other modules

- Use `session-handoff` for the immediate continuation record.
- Use `long-run-feature-tracking` for current scope, status, dependencies, and evidence.
- Use `codified-context` to keep durable state concise and correctly separated.
- Use `documentation-integrity` to verify that linked paths, commits, and evidence still resolve.

## Reporting

Report whether a chronicle is justified, the existing storage/ownership convention, the proposed milestone and evidence, whether an operator confirmation is required for the write, and the next verification point. If no update is approved, return the concise proposed entry without creating project state.
