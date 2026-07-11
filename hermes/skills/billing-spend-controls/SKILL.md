---
name: billing-spend-controls
description: "Control provider and automation spend through scoped preflight, explicit budgets, bounded fan-out, monitoring, and approval-gated recovery."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/safety-billing.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Billing Spend Controls

Source: `AnastasiyaW/claude-code-config/rules/safety-billing.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Billing Spend Controls

This adaptation retains a provider-neutral spend-control protocol and deliberately excludes upstream provider-specific incident claims, product behaviour, environment-variable names, history-rewrite instructions, and hook proposals. It is guidance only: it does not inspect access credentials, change provider settings, launch agents, or activate spending controls.

## When to use

Use this module before an action can create metered provider usage, cloud consumption, paid API requests, large fan-out, auto-recharge exposure, or another material billing effect. Routine local inspection remains read-only; any cost-bearing execution follows the applicable operator-authorisation boundary.

Use `risk-tiered-autonomy` to classify the action and approval requirement. Use `secrets-as-data` when access credentials or environment configuration are relevant, without displaying their values. Use `quality-first-independent-review` when the proposed spend or blast radius warrants independent review.

## Read-only preflight

Before a potentially chargeable run:

1. Identify the provider, account or project boundary, action, pricing unit where available, and the maximum plausible fan-out.
2. Confirm whether an explicit budget, quota, spend limit, alert threshold, or cost owner exists. Do not infer one from a prior run.
3. Inspect the intended configuration through approved redacted interfaces; distinguish subscription, prepaid, and metered paths where the provider documents them.
4. Estimate a conservative upper bound from the requested scope, concurrency, retries, and duration. Label an estimate as an estimate.
5. Check whether credentials, inherited environment, defaults, or automation could select a different billed account or higher-cost route. Do not print values or modify configuration during preflight.
6. Record a stop condition: budget cap, maximum requests, maximum workers, deadline, anomaly threshold, or an operator cancellation point.

If the billed account, effective route, budget, or stop control cannot be established, stop before execution and report the missing evidence.

## Bounded execution protocol

1. Obtain operator confirmation for the exact cost-bearing scope when standing authority does not already cover it.
2. Start with the smallest representative, bounded run that can validate the intended outcome.
3. Set explicit concurrency, request, retry, duration, and worker limits; do not rely on an implicit provider ceiling as a budget.
4. Monitor provider telemetry or another approved usage signal during the run when the scale makes delayed discovery material.
5. Pause or stop on a breached cap, unexpected routing, anomalous consumption, missing telemetry, or a result that no longer justifies further spend.
6. Verify the consumer-side result and report actual usage evidence where available, separately from estimates.

## Guardrails

- Do not activate hooks, scripts, workflows, plugins, scheduled protocols, or background agents from this guidance.
- Do not use a different provider, model, account, credential, or payment route to bypass a quota, budget, or approval blocker.
- Do not broaden a small trial into a batch, fan-out, or recurring run without rechecking scope and authority.
- Do not alter billing settings, auto-recharge, spend caps, payment methods, or credentials without exact operator approval for that interface.
- Do not claim that a run was free, capped, or safely stopped without telemetry or provider evidence.

## Incident response

If unexpected charges or usage appear, stop further cost-bearing work where authorised, preserve redacted telemetry and timestamps, identify the suspected route without exposing credentials, and report the account boundary, observed impact, uncertainty, and required operator decision. Recovery actions such as changing billing settings, requesting refunds, or rewriting configuration remain separate approval-gated operations.

## Reporting

Report the provider and account boundary at an appropriate redaction level, planned scope, estimate and assumptions, configured limits, authority basis, telemetry observed, stop condition, actual result, and any unresolved billing risk. Cost control is a verification discipline, not a promise made by a configuration file.
