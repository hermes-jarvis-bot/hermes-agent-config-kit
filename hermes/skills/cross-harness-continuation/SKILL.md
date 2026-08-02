---
name: cross-harness-continuation
description: "Continue a bounded project slice across agent sessions using a shared, evidence-backed continuity contract without overwriting accepted work or activating enforcement."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/operational/cross-harness-continuation/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Cross Harness Continuation

Source: `AnastasiyaW/claude-code-config/skills/operational/cross-harness-continuation/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Cross-Harness Continuation

Use this module when a bounded project slice moves between agent sessions or
interfaces and the next operator needs to preserve decisions that Git alone cannot
express. It governs the shared continuation contract between agents; use
`session-handoff` for one agent's concise session notes. This is guidance only: it
does not create a contract, change files, activate a guard, or authorise a replan.

## Read-only intake

1. Locate the project-approved continuity record, newest handoff, project guidance,
   and current Git status. Treat the live checkout as authoritative over stale prose.
2. Confirm the baseline branch and commit, pre-existing dirty paths, claimed scope,
   preserved decisions, rejected approaches, and recorded verification evidence.
3. If the record, baseline, scope, or required evidence is absent, report the gap
   before editing. Do not infer another agent's intent from a clean tree or prose.

## Continuation protocol

1. Preserve accepted decisions and existing changes unless focused evidence proves a
   regression or the operator explicitly authorises redesign.
2. Keep the next change within the declared file scope. A scope expansion is a new
   decision that must record its reason and affected paths before write-impacting work.
3. Use the smallest relevant verification, then an independent verifier for a
   non-trivial or cross-module change. Record commands, outcomes, and remaining risk
   in the approved continuity record or handoff.
4. Finish with one explicit next step and a clean checkpoint when the project workflow
   permits it. Parallel work needs isolated worktrees and integration verification;
   this contract does not resolve concurrent merges.

## Replan boundary

A replan is valid only when measured evidence disproves the current design, the
requirements changed, or the operator explicitly authorises a redesign. Record the
reason, intended design change, and scope before altering accepted work. An informal
flag, clean checkout, or aesthetic preference is not evidence of authority.

## Contract shape

Use `references/continuity-contract-example.md` as data-only field guidance. Keep
the record small: put long research or transcripts in the project's approved archive
and link stable evidence rather than copying credentials or raw session history.

## Output

Report the verified baseline, dirty-path classification, declared scope, preserved
decisions, verification status, any replan authority, residual risk, and the exact
next operator-confirmation point.
