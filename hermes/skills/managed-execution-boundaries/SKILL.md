---
name: managed-execution-boundaries
description: "Decide when a managed execution environment is appropriate, preserve approval and credential boundaries, and verify delegated results independently."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/14-managed-agents.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Managed Execution Boundaries

Source: `AnastasiyaW/claude-code-config/principles/14-managed-agents.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Managed Execution Boundaries

This adaptation turns a provider-specific infrastructure pattern into a Hermes decision protocol. A managed execution environment can supply isolated tools, a temporary workspace, and a bounded task lifetime. It does not inherit authority to act, approve risk, retain access credentials, or certify its own output.

## When to use

Consider a managed execution boundary when a bounded task needs standard tools, disposable filesystem state, isolation from the operator's workstation or core environment, and a clear result contract. Typical examples are untrusted-code inspection, a reproducible build, a narrow repository review, or a tool-assisted research task.

Do not introduce one merely to make a routine task look architectural. Keep work in the current controlled environment when its scope is small, verification is straightforward, and isolation adds no meaningful risk reduction.

## Decision gate

Before selecting a managed environment, establish:

1. The exact task, expected output, and completion evidence.
2. Whether input data may leave the current trust boundary.
3. Whether the task needs custom interfaces, persistent state, or a controlled local network.
4. The minimum tools, filesystem paths, network access, and lifetime required.
5. The approval policy for external, production, destructive, financial, identity, or communications actions.

If the task requires privileged credentials, tenant-specific permissions, regulated data handling, or a production control plane, do not pass those capabilities to a generic managed worker. Keep authorisation and sensitive operations with the approved Hermes-controlled interface, or stop for operator confirmation.

## Roles and boundaries

Separate three responsibilities:

- **Coordinator** — owns task definition, trust decisions, approval gates, and final reporting.
- **Execution environment** — performs only the scoped tool work within its granted interfaces and lifetime.
- **Durable state** — holds reviewed artefacts and evidence outside a worker's transient conversation context.

Give the execution environment a concise contract: permitted paths and interfaces, excluded scope, allowed data, prohibited side effects, expected evidence, timeout/budget, and cleanup rule. Its result is untrusted telemetry until the coordinator verifies it at the consuming boundary.

## Safe operating protocol

1. Start with a read-only or dry-run task where practical.
2. Use a disposable workspace or isolated worktree for generated code and untrusted input.
3. Grant least-privilege access; do not copy the operator's profile, archive, or access credentials into the environment.
4. Keep business authorisation, messages, billing, identity changes, deployments, and production writes outside the worker unless the operator explicitly approves the exact action.
5. Collect commands, outputs, changed paths, and verification evidence as durable artefacts.
6. Verify claims independently after the worker exits: inspect outputs, run focused checks, and confirm external state where relevant.
7. Remove temporary state according to the declared cleanup rule and verify the boundary was released.

## State and reuse

Execution-session filesystem state may be useful for a bounded sequence, but it is not a substitute for durable project state or an approval record. Reuse a warm environment only when the task, trust level, owner, and granted access remain compatible. Otherwise create a fresh boundary.

Never assume that a worker remembers prior decisions. Pass the minimum verified context in its contract, and record conclusions in the project state or handoff before the environment is discarded.

## Relationship to other modules

- Use `multi-agent-task-decomposition` to decide whether delegation is justified and to define work boundaries.
- Use `agent-security` for untrusted-input, access-credential, and tool-risk analysis.
- Use `mvp-agent-blueprint` when designing a new agent's autonomy and interface policy.
- Use `proof-loop` and `independent-verification` to validate delivered results.
- Use `subagent-driven-development` when an implementation plan needs a controlled implementer/reviewer sequence.

## Avoid

- Treating environment isolation as permission to perform risky actions.
- Passing production access credentials or private archive data to convenience workers.
- Giving a worker an unrestricted shell, network, or filesystem when a narrow interface will do.
- Letting a worker's completion message replace inspection and verification.
- Creating persistent workers without an owner, expiry, budget, and cleanup rule.
- Automatically activating hooks, plugins, scripts, or scheduled protocols from this guidance.

## Reporting

Report the task boundary, selected environment, granted interfaces, excluded data and actions, approval points, evidence returned, independent verification, and cleanup result. If the trust boundary cannot be made explicit, do not delegate the task.
