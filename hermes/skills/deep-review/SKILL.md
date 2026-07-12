---
name: deep-review
description: "Plan proportionate, independent competency-based review of a concrete change without automatically dispatching reviewers or applying fixes."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/deep-review/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Deep Review

Source: `AnastasiyaW/claude-code-config/skills/development/deep-review/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Deep Review

Use this module for a concrete, high-impact change that needs more than a routine review. It provides a proportionate, competency-based review protocol; it does not dispatch reviewers, run routines, alter a repository, create findings, or approve a merge.

## Applicability

Use after the change scope and diff are available, particularly where security, data integrity, concurrency, external interfaces, or substantial architecture changes are involved. For a small, low-risk diff, use the normal `code-review` module instead. Do not use this module merely to navigate an unfamiliar codebase.

## Protocol

1. **Establish the review boundary.** Identify the base revision, changed files, diff size, declared acceptance criteria, and any production or data-impacting surface. If there is no meaningful diff, record that there is nothing to review.
2. **Select competencies by evidence.** Choose only the relevant review lenses: security, performance, architecture, data, concurrency, error handling, interface or UI behaviour, and testing. State why each selected lens applies. Use at least two lenses only when the change genuinely spans them; do not manufacture coverage.
3. **Keep reviewers independent.** When separate review sessions are warranted and authorised, give each a narrow file set, an explicit question, and a structured finding format: location, severity, evidence, proposed correction, and confidence. Reviewers remain read-only unless a separate action authorises changes.
4. **Cross-check and triage.** Deduplicate overlapping findings, validate them against the current code and relevant tests, and classify each as fix-before-merge, deferred with a tracked owner, or accepted with evidence. A reviewer claim is not proof by itself.
5. **Close the loop.** Apply only separately authorised corrections. Re-run the relevant checks and obtain a fresh review of corrected high-risk areas before declaring the change ready.

## Competency prompts

- **Security:** trust boundaries, input handling, access control, secret exposure, unsafe paths, and external calls.
- **Performance:** unbounded work, expensive hot paths, storage access patterns, memory growth, and caching assumptions.
- **Architecture:** ownership boundaries, dependency direction, duplication, configuration, and public contracts.
- **Data and concurrency:** schema or migration safety, integrity constraints, retry and idempotency behaviour, races, locks, and partial failure.
- **Error handling and interfaces:** validation, failure visibility, cleanup, operator-facing errors, accessibility, and compatibility.
- **Testing:** changed behaviour, negative paths, isolation, regression boundaries, and whether evidence exercises the claimed outcome.

## Review boundary

- Match review depth to risk and scope; a large fan-out needs explicit operator approval for cost and access.
- Treat findings from automated or independent reviewers as input to verify, not automatic authority to change code or scope.
- Keep reports factual: distinguish observed faults, incomplete evidence, accepted trade-offs, and deferred work.
- Do not activate a workflow, schedule a protocol, or add an executable review harness through this module.

## Relationship to existing modules

Use `code-review` for routine pull-request review, `vulnerability-detection-pipeline` for a staged security investigation, `proof-verify` for frozen acceptance-criteria verification, and `multi-agent-task-decomposition` when approved work genuinely needs coordinated parallel roles. This module supplies the narrow risk-based competency selection and finding-triage layer between them.
