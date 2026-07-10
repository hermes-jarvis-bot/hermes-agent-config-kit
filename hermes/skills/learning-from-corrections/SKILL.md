---
name: learning-from-corrections
description: "Distil recurring operator corrections into reviewable, scoped guidance without automatically changing persistent state or activating enforcement."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/learn-from-corrections.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Learning From Corrections

Source: `AnastasiyaW/claude-code-config/rules/learn-from-corrections.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Learning From Corrections

Upstream source policy describes a feedback loop tied to another harness's session capture and enforcement mechanisms. Hermes adaptation retains the useful discipline: a meaningful operator correction can reveal a recurring preference, safety boundary, or process defect. It does not automatically capture conversations, write persistent state, alter project guidance, create a validator, or activate a hook, plugin, or scheduled protocol.

## Principle

Treat a correction as evidence to examine, not as an instruction to create a permanent rule immediately.

The goal is to prevent costly repetition without converting one-off context, frustration, or an ambiguous request into a standing constraint. Persistent guidance has a broad effect; it requires a narrower and better-evidenced decision than a local task correction.

## When to consider distillation

Consider a reviewable lesson when the operator states a lasting preference, corrects the same failure pattern more than once, identifies a safety/privacy/cost/approval boundary, explains why an approach is unsuitable, or explicitly asks to remember, document, or enforce a lesson.

Do not treat a new feature request, a local path correction, ordinary task context, praise without a constraint, or an unexplained reversal as durable guidance.

## Read-only distillation protocol

Before proposing any persistent change:

1. Preserve the exact correction and surrounding task context without exposing access credentials or private data.
2. State the inferred lesson in one conditional sentence: trigger, desired behaviour, and scope.
3. Check existing project guidance, installed Hermes modules, and current operator preferences for an equivalent or conflicting rule.
4. Classify the lesson as a task-local note, project guidance, reusable module improvement, or candidate deterministic control.
5. Identify the smallest durable target and the evidence needed to verify it later.

If the correction is ambiguous, keep it task-local and ask for clarification only when a persistent change is requested. Do not manufacture a preference from a single uncertain exchange.

## Approval boundary

Writing to a project file, a Hermes archive, a reusable module, a configuration surface, or an enforcement routine is write-impacting. Propose the exact target, wording, scope, and rollback path, then obtain operator confirmation unless that exact write was already authorised.

A candidate deterministic control needs separate threat modelling and review. Guidance alone must not be represented as an active guard. Do not enable hooks, validators, integrations, or scheduled protocols merely because a lesson appears mechanically testable.

## Choosing the durable form

Use the lightest form that preserves the proven lesson:

- **Task-local note** for context that expires with the current objective.
- **Project guidance** for repository-specific conventions, ownership, or safety boundaries.
- **Reusable module update** for a broadly applicable, stable procedure.
- **Candidate control record** for a repeatable condition that might later merit a reviewed validator or interface.

Avoid duplicating the same guidance across chat memory, project instructions, and modules. Keep one authoritative statement and reference it from dependent material.

## Quality checks for a proposed lesson

A proposed durable lesson should be specific, conditional when applicability is limited, grounded in an operator correction or verified evidence, compatible with current approval/security/access boundaries, free of private data and access credentials, and paired with a review or verification point when it affects recurring work.

Discard or revise a proposal that cannot name its trigger, scope, or owner. A vague memory is simply a future disagreement wearing a filing label.

## Relationship to other modules

- Use `session-handoff` for temporary cross-session context.
- Use `knowledge-base-enforcement` for accepted project invariants with fixes and regression checks.
- Use `documentation-integrity` to keep persistent guidance accurate.
- Use `red-lines` and `safe-deletion` when the correction identifies a high-impact safety boundary.
- Use `skill-authoring-best-practices` before turning a stable lesson into a reusable module.

## Reporting

Report the original correction in concise form, the proposed lesson and scope, duplicate/conflict checks performed, the recommended durable target, whether operator confirmation is required, and the later verification point. If no durable change is justified, record only the immediate task correction and continue safely.
