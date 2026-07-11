---
name: quality-first-independent-review
description: "Use proportionate fresh-context review and evidence-based verdicts for complex, high-impact, or irreversible work without activating delegation or automation."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/quality-over-tokens-independent-verify.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Quality First Independent Review

Source: `AnastasiyaW/claude-code-config/rules/quality-over-tokens-independent-verify.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Quality-First Independent Review

This module adapts a narrow quality rule: avoid reducing verification merely to save time or model capacity when the decision is complex, high-impact, security-sensitive, externally visible, or difficult to reverse. It does not require unrestricted delegation, create agents, start a workflow, spend provider budget, or activate hooks.

## Decision boundary

Use the smallest review level that can expose the material failure modes:

| Work class | Default review |
| --- | --- |
| Read-only inspection or obvious local change | Author review plus focused evidence |
| Non-trivial implementation, integration, or migration | Fresh-context review when available and proportionate |
| Destructive, irreversible, security, production, billing, or external action | Independent review before the action, plus operator confirmation where required |

Time, token, and cost constraints are operational inputs, not reasons to fabricate confidence or omit a required safety check. If a necessary review cannot be performed because access, budget, or an interface is unavailable, report the blocker and do not substitute a claim of success.

## Read-only review protocol

Before a high-impact action:

1. Define the proposed outcome, mutable targets, acceptance criteria, and rollback or containment options.
2. Collect the smallest relevant evidence set: repository state, current telemetry, interface documentation, test output, and consumer-side observations where applicable.
3. Identify the strongest independent check available: a fresh Hermes session, an uninvolved reviewer, a deterministic validator, or a disposable-environment test.
4. Give the reviewer the final artefact and evidence needed to test the claim, not a request to endorse the author's reasoning.
5. Record a bounded verdict: `PROCEED`, `HOLD`, or `REJECT`, with evidence and the condition that would change it.

An independent reviewer should inspect alternative failure hypotheses, boundary conditions, access assumptions, and the consumer-facing result. A successful command or confident status message is evidence, not a verdict.

## Scope control

- Keep review proportional. A trivial read-only lookup does not need a separate session.
- Do not fan out work merely to create activity; add reviewers only where their independence or expertise changes the confidence level.
- Do not use a reviewer to bypass operator confirmation, access controls, change windows, or billing limits.
- Do not activate hooks, scripts, plugins, scheduled protocols, or external interfaces from this guidance.
- If reviewers disagree, resolve the factual gap with stronger evidence rather than averaging opinions.

## Relationship to existing modules

- Use `code-quality` to keep the implementation minimal but complete.
- Use `proof-loop` when frozen acceptance criteria and durable testable artefacts justify a full build/verify cycle.
- Use `independent-verification` to verify side effects at the receiving boundary.
- Use `risk-tiered-autonomy` for approval requirements and `managed-execution-boundaries` when a separate execution environment is considered.

## Reporting

Report the risk classification, evidence reviewed, independent check selected, verdict, unresolved uncertainty, and any operator-confirmation point. State explicitly when independent review was not available and why.
