---
name: red-lines
description: "Define a small, evidence-backed set of non-negotiable operational safety boundaries and stop conditions."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/15-red-lines.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Red Lines

Source: `AnastasiyaW/claude-code-config/principles/15-red-lines.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Red Lines

This module defines a small set of non-negotiable operational safety boundaries. It is guidance only: it does not change approval settings, create files, activate routines, or grant access.

## Principle

A red line is a specific prohibition for a high-impact failure mode. It overrides convenience, urgency, and ordinary task preferences. When a proposed action crosses one, stop and report the blocked action, scope, reason, and required operator confirmation or review.

Use red lines only for failures with material blast radius: data loss, credential exposure, security-control weakening, uncontrolled external actions, production disruption, or unapproved cost.

## Keep the set small

Maintain roughly five to fifteen boundaries. A long catalogue of ordinary preferences obscures the few conditions that must reliably stop work.

Each boundary should include:

```text
ID: stable short identifier
Risk: concrete harm prevented
Trigger: observable action or condition
Required response: stop, evidence, and confirmation or review path
Evidence: incident, threat model, policy, or verified operational rationale
Owner and review date: who maintains it and when it is reconsidered
```

Do not invent incident history. A verified risk assessment or explicit policy is sufficient when no incident record exists.

## Baseline boundaries

Adapt these to the established project policy rather than treating them as a universal configuration:

1. Do not delete or irreversibly alter production data without exact scope, rollback information where possible, and operator confirmation.
2. Do not expose access credentials in source control, telemetry, generated artefacts, or external communications channels.
3. Do not overwrite uncommitted work, replace shared state, or force a history rewrite without inspecting the affected scope and receiving confirmation.
4. Do not weaken security controls, change identity or network boundaries, or broaden privileges without a reviewed change protocol and confirmation.
5. Do not send, publish, purchase, create public resources, or otherwise act through an external interface without the required operator confirmation.
6. Do not substitute an unapproved provider, model, paid service, access credential, or execution environment to bypass a blocker.

## Read-only preflight

Before proposing a boundary or deciding that one applies:

1. Identify the authoritative project policy, environment, owner, and affected interface.
2. Inspect the proposed action, target scope, reversibility, current state, and available rollback.
3. Distinguish a red-line trigger from an ordinary caution or recoverable defect.
4. Gather durable evidence for the risk and the required approval path.
5. Check whether existing modules already cover the action-specific procedure.

If policy or scope is unclear, do not infer an exception. Report the ambiguity as a blocker.

## Response protocol

When a red line triggers:

1. Stop before the action.
2. State the boundary ID, proposed action, affected scope, and concrete risk.
3. Preserve safe read-only evidence only; do not perform a workaround that changes the same state by another route.
4. Specify the narrowest safe next step, such as an operator confirmation, a scoped change plan, or independent security review.
5. After authorised work, verify the stated safety condition and record only the necessary evidence under the project convention.

An approval for one scoped action is not a standing exception.

## Relationship to other modules

- Use `safe-deletion` for destructive-operation confirmation and post-action verification.
- Use `secrets-as-data` for access-credential handling and public-boundary hygiene.
- Use `agent-security` and `supply-chain-defense` for untrusted input and dependency risk.
- Use `no-guessing` when configuration, ownership, or scope is missing.
- Use `independent-verification` to test whether a safety control actually works.

## Review and reporting

Review boundaries after a material incident, policy change, or scheduled review. Retire duplicates and vague statements; retain the smallest set that prevents known high-impact failures.

Report the applicable boundary, evidence, action scope, whether work stopped, the exact confirmation or review needed, and the verification point. Do not claim that this guidance is mechanically enforced unless a separately reviewed implementation has been activated.
