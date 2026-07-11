---
name: durable-context-maintenance
description: "Maintain durable project guidance and archive records with meaningful links, claim provenance, and targeted reviewable updates."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/memory-maintenance.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Durable Context Maintenance

Source: `AnastasiyaW/claude-code-config/rules/memory-maintenance.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Durable Context Maintenance

Use this module to keep long-lived project guidance, decision records, and archive entries navigable and trustworthy. It adapts three safe practices: meaningful cross-links, explicit provenance for load-bearing claims, and small reviewable updates. It is guidance only; it does not write to the archive, rewrite project files, activate a hook, or create a scheduled protocol.

## Scope and boundary

Apply this to retained project guidance, decision logs, handoffs, knowledge-base entries, and stable operator preferences. Do not use it to preserve access credentials, raw private transcripts, transient tool output, or unreviewed claims.

Before any persistent update, inspect the current target, identify its owner and source-of-truth role, and check for existing equivalent guidance. Writing or deleting durable context remains a write-impacting action and requires the applicable operator confirmation unless the exact change is already authorised.

## Meaningful links

Link related retained records only when following the link would help a future operator understand the active entry or verify a decision. Prefer stable repository-relative paths, issue identifiers, commit references, or clearly named local records over a dense web of vague links.

When creating or updating an entry:

1. Identify the few records that supply context, evidence, or a dependent decision.
2. Confirm each reference resolves and still describes the intended relationship.
3. Add only links that make navigation or verification materially easier.
4. Remove or correct stale links only with the required approval and read-back verification.

Links improve discovery; they do not make a claim true.

## Claim provenance

Mark a claim when a future action would depend on how well it is established. Use concise language such as:

- **verified** — directly supported by a dated command result, repository source, documentation, or operator statement;
- **inferred** — a reasoned conclusion that should be rechecked before a consequential action;
- **uncertain** — incomplete, conflicting, or time-sensitive evidence requiring further inspection.

State the source or verification command where practical. Do not decorate every sentence with provenance labels; reserve them for facts that affect safety, configuration, capacity, ownership, or operational decisions.

## Targeted update protocol

Prefer an explicit, minimal change over a wholesale rewrite of a mature context file:

1. Capture the proposed addition, correction, or removal with its evidence and exact target section.
2. Check for duplication, conflict, stale references, and loss of relevant nuance.
3. Review the proposed diff independently when the record governs high-impact, multi-session, or safety-sensitive work.
4. Apply only the approved targeted change.
5. Re-read the updated record and its affected references to confirm the intended state.

Writing a new record may appropriately start from a complete document. The targeted-update discipline applies when an established record already carries accumulated operational context.

## Avoid

- Rewriting an entire durable record merely to add one lesson.
- Treating a model summary as verified evidence without its source.
- Adding duplicate guidance to the archive, project instructions, and reusable modules without an authoritative home.
- Replacing an old decision silently instead of recording a correction or superseding decision.
- Turning a documentation convention into an active validator, hook, plugin, or scheduled protocol without separate review and approval.

## Relationship to other modules

- Use `codified-context` to choose the appropriate context artefact and loading boundary.
- Use `learning-from-corrections` to decide whether a correction merits durable guidance.
- Use `documentation-integrity` to verify paths, commands, counts, and generated state.
- Use `session-handoff` for temporary cross-session transfer rather than permanent archive content.
- Use `no-guessing` when a fact must be retrieved or verified before acting.

## Reporting

Report the target record, proposed scope, provenance of load-bearing claims, duplicate/conflict checks, references inspected, exact diff or approval point, and post-update read-back. Durable context should become more useful through maintenance, not merely more voluminous.
