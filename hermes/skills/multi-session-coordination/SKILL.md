---
name: multi-session-coordination
description: "Coordinate parallel sessions with append-only handoffs, resource locks, heartbeats, stale-lock checks, and verified release."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/18-multi-session-coordination.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Multi Session Coordination

Source: `AnastasiyaW/claude-code-config/principles/18-multi-session-coordination.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Multi-Session Coordination

Upstream source policy describes parallel sessions sharing a workspace. Hermes adaptation keeps the distributed-systems pattern and removes harness-specific directories, hooks, and product assumptions. This module is guidance only; it does not create lock files, daemons, hooks, or scheduled protocols automatically.

## Principle

Parallel sessions are concurrent processes. Treat shared resources accordingly.

Separate two kinds of state:

1. **Append-only state** — handoffs, logs, findings, and journal entries. Each session writes its own file or appends a new line; nobody rewrites another session's record.
2. **Mutable exclusive state** — GPU ownership, ports, containers, queues, migrations, or long-running jobs. These require locks, heartbeats, stale checks, and verified release.

Do not use one shared mutable table for both. It becomes a charming little race condition factory.

## Suggested Hermes-friendly layout

Use a repo-local or workspace-local coordination directory chosen by the operator, for example:

```text
.hermes-coordination/
  handoffs/
    <timestamp>-<session-id>.md
    INDEX.md
  locks/
    <resource-id>.lock
    INDEX.md
```

Only create this structure after confirming it belongs in the project. For transient one-off work, a temp directory or explicit note may be enough.

## Append-only handoffs

Use append-only handoffs when the state is historical rather than exclusive:

- completion notes;
- findings;
- handoff summaries;
- decisions that should be visible to future sessions.

Protocol:

1. Write a new handoff file with a unique timestamp/session identifier.
2. Append one line to `handoffs/INDEX.md` if an index is useful.
3. Do not edit older handoff records to "fix" history; append a correction.

## Resource locks

Use one lock file per resource:

```yaml
---
session_id: build-release-7f3a
resource: port_8080
task: "local integration server"
started: 2026-07-10T12:00:00Z
heartbeat: 2026-07-10T12:00:00Z
expected_duration: 30m
---

Purpose, owner, command, and recovery notes.
```

Canonical resource names matter. Use `port_8080`, `gpu_host-a_3`, or `container_worker-01`; do not mix variants for the same resource.

## Take protocol

Before claiming a resource:

1. Check static rules and operator constraints.
2. Check whether the resource lock exists.
3. If no lock exists, write the lock file in a single file operation.
4. Append `TAKE` to the lock index if one exists.
5. If a lock exists and its heartbeat is fresh, stop or choose another resource.
6. If a lock exists but appears stale, verify externally before reclaiming.

External verification depends on the resource:

- ports: `ss`, `lsof`, or a real connection check;
- containers: Docker/Compose telemetry;
- GPUs: vendor tooling;
- jobs: process table, scheduler state, or service telemetry.

A stale heartbeat is evidence to investigate, not permission to delete.

## Heartbeat protocol

For long-running work, update only the heartbeat field periodically. Do not spam the history index for every heartbeat. If heartbeats are not practical, record a realistic expected duration and recovery note.

## Release protocol

To release a lock:

1. Stop or finish the underlying resource use.
2. Remove the lock file.
3. Verify the lock file is gone.
4. Verify the resource is actually free when feasible.
5. Append `RELEASE` or `STALE-RECLAIM` to the index with a short result summary.

Never report a release from intent alone. Read back the state.

## Avoid

- Shared mutable markdown tables edited by multiple sessions.
- Lock names based on task instead of resource.
- Deleting another session's stale-looking lock without external verification.
- Hook automation before the manual convention is stable.
- Treating file locks as a security boundary. They coordinate trusted agents; they do not stop a malicious writer.

## Reporting format

When using this module, report:

- coordination root path;
- session identifier;
- resource identifier;
- lock state before action;
- action taken;
- verification after action;
- remaining locks or handoffs relevant to the operator.

Use `inter-agent-communication` when the problem is a directed request to another session. Use this module when the problem is shared state, ownership, or handoff discipline.
