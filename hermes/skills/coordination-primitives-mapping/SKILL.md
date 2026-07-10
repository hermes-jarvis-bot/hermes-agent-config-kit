---
name: coordination-primitives-mapping
description: "Choose coordination primitives by mapping locks, leases, logs, mailboxes, queues, registries, and schedulers to known failure modes and deployment scope."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/25-coordination-primitives-mapping.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Coordination Primitives Mapping

Source: `AnastasiyaW/claude-code-config/principles/25-coordination-primitives-mapping.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Coordination Primitives Mapping

Upstream source policy describes coordination design as a mapping problem: before inventing a coordination layer, name the primitive, identify the closest known analogue, and check whether the deployment topology fits its failure model. Hermes adaptation keeps that design-review protocol and removes project-specific examples, automatic enforcement machinery, and bibliography-driven authority.

## Principle

Choose coordination primitives by scope and failure mode, not by aesthetic preference.

Before designing or approving a coordination mechanism, answer three questions:

1. What primitive is this: lock, lease, log, mailbox, queue, registry, schedule, or transaction?
2. What known analogue does it resemble?
3. Does the operator's deployment topology fit the analogue's safe operating scope?

If the answer to the third question is no, do not stretch the primitive. Pick a different interface.

## Primitive map

Use this map as a design checklist, not as a promise that any implementation is automatically correct.

| Need | Candidate primitive | Safe scope | Common failure mode | Hermes relationship |
| --- | --- | --- | --- | --- |
| Exclusive ownership of a shared local resource | Lock with heartbeat or lease | Trusted writers on one reliable filesystem or one coordinator | stale locks, split brain, cache incoherence | `multi-session-coordination` |
| Durable history of what happened | Append-only log or journal | Single writer or append-safe convention with review | rewritten history, missing entries, unbounded growth | handoffs, task logs, review notes |
| Targeted asynchronous request | Mailbox/message envelope | Trusted participants, delayed delivery acceptable | unread mail, spoofed sender, command confused with permission | `inter-agent-communication` |
| Current running state | Registry/status table | Derived from logs or verified live telemetry | stale snapshot mistaken for truth | process/service telemetry |
| Work distribution | Queue | One clear consumer policy and retry semantics | duplicate work, lost work, poison messages | task runners, issue queues, schedulers |
| Periodic or delayed work | Scheduled protocol | Idempotent operation with clear delivery target | duplicate firing, missed run, silent failure | Hermes scheduled protocols |
| Cross-machine consensus | Network coordinator or database transaction | Managed service with real consistency guarantees | pretending file locks are consensus | Redis, Postgres, etcd, cloud queue, or equivalent |
| Conflict between versions | Evidence-backed synthesis | Git history plus executable checks | losing one side's intent | `merge-conflict-resolution` |

## Design protocol

When a task asks for coordination:

1. **Name the state being coordinated.** Is it ownership, history, intent, status, work, time, or version conflict?
2. **Name the primitive.** Avoid vague labels such as “agent memory” or “sync layer”.
3. **State the topology.** Same process, same workstation, one shared filesystem, SSH host, Git-only async transport, local network, WAN, or managed cloud service.
4. **State the trust model.** File-based conventions coordinate trusted collaborators; they are not security boundaries.
5. **List failure modes.** Stale lock, duplicate delivery, lost message, split brain, stale registry, replay, clock drift, or partial write.
6. **Choose the smallest primitive that covers the topology.** Do not choose consensus when a lock is enough; do not choose a file lock when consensus is required.
7. **Define verification.** How will the operator know the primitive worked: read-back, process telemetry, queue depth, delivery receipt, test, or consumer-side check?

## Scope rules

Use file-based coordination only when:

- all participants can see the same filesystem semantics;
- writers are trusted;
- latency is acceptable;
- stale detection is backed by external verification;
- losing real-time delivery is acceptable or recoverable.

Do not use file-based coordination when:

- participants write through NFS, SMB, object storage, sync folders, or opaque caching layers without tested semantics;
- untrusted writers can modify coordination files;
- cross-region or real-time correctness is required;
- duplicate work is dangerous and no idempotency exists;
- the state is security-critical.

For those cases, move to a real coordinator: database transaction, message broker, queue service, distributed lock service, or platform scheduler. A folder with optimistic naming is not a consensus system, however neatly indented.

## Choosing between Hermes coordination modules

- Use `multi-session-coordination` when the problem is shared state, resource ownership, handoffs, locks, or stale recovery.
- Use `inter-agent-communication` when the problem is a directed request, reply, broadcast, or mailbox-style audit trail.
- Use `merge-conflict-resolution` when competing versions must be synthesized without losing intent.
- Use `git-source-of-truth` when the durable record should be Git commit history.
- Use a scheduled protocol only when time is the coordinating primitive and the action is idempotent or safely repeatable.

If more than one module seems applicable, identify the primary failure mode first. Ownership problems need locks. Request problems need messages. Version conflicts need evidence. Time-based problems need schedules.

## Review checklist

Before approving a new coordination design, verify:

- [ ] The coordinated state is explicitly named.
- [ ] The primitive is named without marketing language.
- [ ] The topology and trust model are documented.
- [ ] Known failure modes are listed.
- [ ] Out-of-scope deployments are rejected or routed to a stronger interface.
- [ ] Verification/read-back is defined.
- [ ] The design does not treat advisory files as security controls.
- [ ] The design does not claim real-time cross-machine correctness from local-file semantics.

## Avoid

- Calling a lock a queue because both are files in a folder.
- Calling a status file truth without verifying the underlying process.
- Treating mailbox delivery as proof of action.
- Treating a heartbeat as permission to delete without external telemetry.
- Adding automation, daemons, or scheduled protocols before the manual convention is stable.
- Writing “works everywhere” when only one topology was tested.

## Reporting format

When using this module, report:

- coordination need;
- selected primitive;
- topology and trust assumptions;
- rejected alternatives;
- failure modes considered;
- verification/read-back plan;
- related Hermes module to apply next.

The boring name for your coordination primitive is usually the useful one. Novel names tend to arrive shortly before novel outages.
