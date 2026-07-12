---
name: workflow-orchestration
description: "Choose a bounded Hermes-native orchestration pattern and prepare a reviewable protocol without importing or activating upstream workflow code."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/workflow-orchestration/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Workflow Orchestration

Source: `AnastasiyaW/claude-code-config/skills/development/workflow-orchestration/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Workflow Orchestration

Use this module to choose and prepare a repeatable, multi-stage Hermes protocol where a one-off task or ordinary delegation would be insufficient. It is planning guidance only: it does not copy or execute upstream JavaScript, activate a scheduled protocol, dispatch agents, create task state, or bypass approval boundaries.

## Applicability

Start with the smallest suitable mechanism. A single bounded investigation normally needs one session; a small independent split may use approved delegation; a repeatable sequence with explicit inputs, outputs, stop conditions, and evidence may justify a documented protocol. Do not introduce orchestration merely because a task has several steps.

Use this module when the work has a stable decomposition, a meaningful coordination or verification boundary, and enough expected reuse or risk to justify recording the protocol. Require explicit operator approval before any fan-out that adds provider cost, access, external effects, or repository writes.

## Read-only design protocol

1. **Define the boundary.** Record the objective, inputs, exclusions, expected outputs, maximum concurrency, budget or cost limit, and the action classes that require operator confirmation.
2. **Choose the simplest pattern.** Use sequential stages for real dependencies; split-and-merge only for independent, comparable work; and specialised roles only where their evidence boundary is clear. Keep headless or unattended execution out of scope unless separately designed and approved.
3. **Specify stage contracts.** For every stage, state required input, structured result, failure state, owner, and the next permitted action. Treat previous-stage summaries as claims to verify, not automatic authority.
4. **Add stop and recovery conditions.** Define success, failure, budget exhaustion, missing access credentials, uncertain evidence, and operator-confirmation checkpoints. Fail visibly rather than silently retrying or broadening scope.
5. **Plan evidence and review.** Name the smallest relevant verification for each final claim. Keep intermediate output scoped and redact access credentials or private data. A final synthesis must distinguish observations, unresolved faults, and recommendations.

## Safety boundaries

- The upstream executable template and validation script remain quarantined snapshot data; this adapter provides no executable workflow or shell routine.
- Do not use a coordination plan to pre-authorise edits, deployments, external messages, credential use, or billing spend.
- Prefer bounded batches and explicit concurrency limits. Large fan-out needs an operator-approved budget and a fresh preflight.
- Keep irreversible or production-affecting actions outside the orchestration path until an operator confirms their exact scope.
- If a claimed stage result is missing, malformed, or unverified, report it as BLOCKED rather than synthesising a plausible substitute.

## Relationship to existing modules

Use `deterministic-orchestration` for deterministic mechanical routines, `multi-agent-task-decomposition` for dependency-aware role boundaries, `billing-spend-controls` for cost controls, and `proof-verify` for independent acceptance verification. This module supplies the narrow selection and protocol-design layer without activating automation.

## Output shape

Produce a concise protocol proposal: objective, selected pattern and rationale, stage contracts, concurrency and budget boundary, approval checkpoints, stop/recovery conditions, verification evidence, residual risks, and the next operator decision. The proposal is not authority to execute it.
