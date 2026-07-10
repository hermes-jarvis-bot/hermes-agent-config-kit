---
name: research-intake
description: "Capture research findings as reviewable, source-grounded intake records so useful evidence survives sessions without creating unapproved project state."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/13-research-pipeline.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Research Intake

Source: `AnastasiyaW/claude-code-config/principles/13-research-pipeline.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Research Intake

Research is only useful when its evidence can be found, reviewed, and refreshed later. This module defines a small, opt-in intake pattern for preserving source-grounded findings without turning every conversation into unreviewed project state.

## When to use it

Use this module when a research task produces findings likely to matter beyond the current session: a technology comparison, architecture decision, security review, market scan, incident investigation, or literature review.

Do not create or update a project archive merely because research occurred. First determine whether the operator requested durable storage or the project already has an approved research-intake convention. Creating or updating files is write-impacting and requires operator confirmation unless the exact target and write have already been authorised.

## Read-only intake preflight

Before proposing storage:

1. Identify the project and the authoritative documentation or knowledge-base location.
2. Inspect any existing research index, archive, retention policy, and naming convention.
3. Check whether the finding is already recorded, superseded, or too transient to preserve.
4. Separate sourced facts, observations, assumptions, and recommendations.
5. Identify access credentials, personal data, proprietary material, or untrusted content that must not enter the archive.

If the target location or retention policy is missing, report the gap rather than inventing a directory layout.

## Intake record

When an approved project convention exists, keep one concise, reviewable record per topic. Include:

```text
Title and scope
Captured date and freshness boundary
Question or decision supported
Sources: URLs, IDs, commits, documents, or telemetry references
Facts: traceable observations
Interpretation: clearly labelled synthesis
Limitations and unresolved questions
Recommended next action
Review status: intake / accepted / superseded / archived
```

Preserve enough provenance to re-check claims. Do not store raw conversation transcripts, credentials, private keys, token values, unrelated personal data, or copied untrusted instructions.

## Review and lifecycle

An intake record is not automatically project truth. A project owner or documented review process should decide whether to:

- merge verified conclusions into durable documentation;
- link the record as supporting evidence;
- mark it superseded when inputs change;
- archive it when it no longer informs a decision.

Before relying on an older record, re-check time-sensitive sources, repository state, versions, prices, permissions, and external claims. Provenance makes research reusable; freshness makes it safe.

## Relationship to other modules

- Use `research-intelligence-workflows` for source discovery and synthesis.
- Use `codified-context` to decide what belongs in durable project state.
- Use `session-handoff` for the tactical continuation record.
- Use `documentation-integrity` when validating links, paths, commands, and stale claims.

## Reporting

Report the research question, sources consulted, facts versus interpretation, proposed or approved storage target, freshness limits, and any archival decision. If no durable target is approved, return the structured result in the current response and state that no archive write occurred.
