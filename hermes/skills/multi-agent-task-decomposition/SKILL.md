---
name: multi-agent-task-decomposition
description: "Decide when a task needs decomposition, define dependency-aware work boundaries, and coordinate sub-agents through explicit contracts and verified integration."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/06-multi-agent-decomposition.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Multi Agent Task Decomposition

Source: `AnastasiyaW/claude-code-config/principles/06-multi-agent-decomposition.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Multi-Agent Task Decomposition

This adaptation keeps a narrow planning discipline: use more than one agent only when decomposition improves the outcome, derive boundaries from dependencies rather than filenames, and integrate against explicit contracts. It is guidance only. It does not create agents, start background processes, activate a workflow, or grant additional access.

## Decision gate

Start with one agent when the task is local, the relevant context fits in one session, and focused verification has a clear owner. Decomposition is justified when distinct work domains have real dependency boundaries, independent review adds value, or one session cannot safely retain the necessary context.

Do not decompose merely because a task touches several files. More agents add coordination cost, access surface, and integration risk.

## Read-only decomposition protocol

Before dispatching work:

1. Map the control flow, data flow, shared state, and external side effects that cross proposed boundaries.
2. Identify contracts: inputs, outputs, ownership, ordering, invariants, and verification evidence.
3. Check for overlapping write targets, shared access credentials, production interfaces, and resource conflicts.
4. Choose the smallest coordination pattern that fits: sequential handoff, independent read-only review, or isolated implementation tasks.
5. Define one integration owner and a completion rule before any implementation begins.

If a dependency or contract is unclear, keep the work single-agent until it is clarified. Parallel ambiguity is not a productivity feature.

## Task contract

Give every worker a self-contained contract:

```text
Objective: one bounded outcome
Context: only the verified facts and files needed
Allowed scope: exact paths and permitted interfaces
Excluded scope: paths, systems, and decisions the worker must not touch
Inputs and outputs: formats, ownership, and acceptance conditions
Risk policy: read-only or write-impacting; access and approval requirements
Evidence: exact checks or artefacts required for acceptance
```

Do not ask a worker to infer unresolved architecture from a previous worker's raw notes. The coordinator must synthesize verified findings into the next contract.

## Boundary rules

- Divide work by a stable capability or contract, not by file extension or arbitrary directory slices.
- Give one worker ownership of each mutable interface, schema, migration, release, or shared configuration surface.
- Keep untrusted input and generated code in isolated, least-privilege environments.
- Restrict workers to the minimum interfaces and access credentials needed for their contract.
- Use `multi-session-coordination` for resource ownership and durable handoffs; use `inter-agent-communication` for directed messages.
- Use `coordination-primitives-mapping` when selecting locks, queues, schedules, or a cross-machine coordinator.

## Integration protocol

The integration owner must:

1. Read each delivered artefact and its verification evidence.
2. Check contract compatibility at the consuming boundary, not only in worker output.
3. Resolve overlaps deliberately; do not silently pick the last writer.
4. Run focused integration checks and record remaining uncertainty.
5. Obtain operator confirmation before any production, external, destructive, security-sensitive, or billing-impacting action.

A worker status message is progress telemetry, not proof of completion.

## Avoid

- Recursive or unbounded delegation.
- Shared mutable scratch files without ownership rules.
- Dispatching implementation before mapping dependencies.
- Passing full conversation history where a concise contract will do.
- Treating a file-based coordination convention as a security boundary.
- Automatically activating hooks, scripts, plugins, or scheduled protocols because a decomposition exists.

## Reporting

Report the decision to stay single-agent or decompose, the dependency map, worker contracts, mutable ownership boundaries, integration evidence, and any blocked approval point. If decomposition did not reduce a real risk or bottleneck, do not use it.
