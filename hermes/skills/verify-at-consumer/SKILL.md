---
name: verify-at-consumer
description: "Verify integrations at the receiving side; sender logs, specs, and HTTP acknowledgements are not enough."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/verify-at-consumer.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Verify At Consumer

Source: `AnastasiyaW/claude-code-config/rules/verify-at-consumer.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Verify At Consumer

Upstream source policy was written for webhook/API/queue integration failures. Hermes adaptation keeps the rule: verify an integration where the receiving side consumes the event, not where the sender claims it was sent.

## Principle

For integrations, the receiving side is the source of truth. Sender logs, OpenAPI documents, schemas, queue acknowledgements, and HTTP `200` responses prove at most that something was emitted or accepted. They do not prove that the consumer parsed it, applied it, rendered it, stored it, or acted on it.

Use this rule for:

- webhooks and callback URLs;
- API request bodies where sender and receiver evolve separately;
- queues, pub/sub, workers, and event buses;
- RPC or JSON-RPC payloads;
- gateway integrations and cross-service contracts.

## Protocol

1. Identify the consumer code, worker, handler, database write, UI state, or downstream side effect that matters.
2. Read the exact fields, paths, types, and wrappers the consumer actually uses.
3. Compare the proposed sender payload to those consumer expectations.
4. Trigger an end-to-end test or replay through the real boundary when safe.
5. Verify the receiver-side outcome: row written, queue job processed, UI rendered, state changed, callback handled, or consumer log marker observed.

## What is not enough

- `HTTP 200` from the receiver.
- `webhook delivered` in sender telemetry.
- A schema that permits the payload shape.
- A retry of the same malformed event.
- The author's memory of how the integration usually works.

## Hermes examples

- For a gateway webhook, confirm both the platform send result and the Hermes-side received event or resulting session/job.
- For a GitHub Actions trigger, confirm the workflow run/check-run, not only the `git push`.
- For a queue producer, confirm the worker consumed the job and produced the expected artefact.
- For an API integration, confirm the downstream state, not merely request success.

## Fresh verification prompt

For important integrations, ask a fresh verifier to inspect the consumer:

```text
Read the consumer code at <path:line>. List the exact payload fields, nesting, types, and required side effects it uses. Compare that to this sender payload: <payload>. Verdict: MATCH / MISMATCH / AMBIGUOUS with evidence.
```

## Reporting

Report both sides separately:

- sender evidence: request id, delivery status, queue id, or emitted event;
- consumer evidence: parsed field path, database row, UI state, worker log, callback effect, or downstream artefact.

If only sender-side evidence exists, say `sent but not consumer-verified`.
