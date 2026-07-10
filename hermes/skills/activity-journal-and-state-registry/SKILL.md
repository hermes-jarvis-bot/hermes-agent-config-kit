---
name: activity-journal-and-state-registry
description: "Maintain an append-only activity journal and a verified current-state registry for shared resources without activating enforcement hooks."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/activity-journal-and-state-registry.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Activity Journal And State Registry

Source: `AnastasiyaW/claude-code-config/rules/activity-journal-and-state-registry.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Activity Journal and State Registry

Upstream source policy combines an activity journal, a current-state registry, and an enforcement mechanism. Hermes adaptation retains the first two as an operator-reviewed convention for shared resources. It does not install, enable, or imply an active hook, validator, daemon, or scheduled protocol.

## Principle

For multi-session work or a shared resource, make three questions answerable from durable evidence: what is running, who started it, and why.

Use two distinct artefacts:

1. an append-only activity journal for state-changing actions;
2. a compact current-state registry for verified active work.

The journal is history. The registry is a snapshot. Neither substitutes for live process, service, queue, or resource telemetry.

## When to use

Use this convention when multiple sessions share a workstation, server, GPU, database, queue, deployment target, long-running job, or another mutable resource. For a single short task, normal command evidence and `session-handoff` are usually sufficient.

Choose a repository-local or resource-local location deliberately. Do not create tracking files in a project or on a shared system without operator confirmation for that target.

## Journal record

Append one record for a state-changing action that affects the shared scope: starting or stopping a job, restart, deployment, configuration change, delete, resource claim or release, or a material recovery action.

Each record should identify:

```text
timestamp | actor/session | scope or resource | action | reason | result/evidence
```

Prefer append-safe JSONL or uniquely named entries. Do not rewrite prior records; append a correction if the history needs qualification. Read-only inspection does not normally require a journal entry.

Do not record access credentials, private payloads, or raw sensitive command output.

## Current-state registry

Keep a small human-readable snapshot of verified active work:

```text
Running now:
- resource/job: <identifier>
  owner: <actor/session>
  purpose: <bounded task>
  started: <timestamp>
  writes/uses: <paths, ports, queues, or resources>
  verification: <live telemetry command or result>

Constraints:
- <relevant capacity, maintenance, or approval boundary>
```

Update the registry after a relevant state change, then verify its claims against live telemetry where practical. A registry that has not been checked is a hypothesis, not current truth.

## Read-only design protocol

Before proposing adoption:

1. Identify the shared resource, participants, topology, and existing source of truth.
2. Decide whether an append-only journal and registry add information not already covered by service telemetry, scheduler records, Git, or `multi-session-coordination`.
3. Define the smallest location, record fields, retention expectations, and owner.
4. Specify the read-back command or telemetry that verifies each registry entry.
5. Identify what remains manual and which write-impacting actions require operator confirmation.

If the resource has a real scheduler, service manager, or control plane, prefer that system's telemetry as authoritative and link to it from the registry rather than recreating it in prose.

## Boundaries

- This module is guidance, not enforcement.
- Do not activate shell hooks, validators, background watchers, or scheduled protocols from this convention.
- A file-based journal or registry coordinates trusted participants; it is not a security boundary.
- Use `multi-session-coordination` for locks, heartbeats, and verified resource release.
- Use `session-handoff` for bounded transfer between sessions.
- Use `coordination-primitives-mapping` when topology or failure modes require a stronger primitive.

## Reporting

Report the resource scope, existing authoritative telemetry, whether the convention is justified, proposed journal and registry locations, required operator confirmation, and the live verification method. For a state-changing action, report both the appended record and the post-action telemetry read-back.

Clear state is useful. Pretending a markdown snapshot is a control plane is considerably less so.
