---
name: system-and-data-design
description: "Plan and review capacity, storage, data flow, consistency, resilience, and scaling decisions from measured requirements without provisioning infrastructure."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/system-and-data-design/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# System And Data Design

Source: `AnastasiyaW/claude-code-config/skills/development/system-and-data-design/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# System and Data Design

Use this module to plan or review whether a system can meet a stated workload and
where its data should live. It covers capacity estimates, data access patterns,
storage, replication, partitioning, consistency, queues, and resilience. It is a
read-only design protocol: it does not provision infrastructure, change a cloud
account, create data stores, run migrations, deploy, or authorise spending.

## Scope and exclusions

Begin with the smallest credible deployment. Use `architecture-first` for module
boundaries, dependency direction, and domain ownership; `code-complexity` for local
function, interface, and readability concerns; `refactoring-safely` for a
behaviour-preserving code transformation; and `lean-code` when the primary answer is
to remove unjustified scope. This module does not turn a low-traffic internal tool
into a distributed system merely because the diagram can accommodate one.

## Read-only design protocol

1. Establish functional behaviour, peak and expected load, payload and retention,
   read/write mix, latency and staleness tolerance, failure tolerance, budget,
   compliance, existing constraints, and what evidence is unavailable. Treat absent
   requirements as a design blocker rather than inventing scale.
2. Make order-of-magnitude estimates for requests, bandwidth, storage growth, working
   set, recovery window, and limiting resource. Record assumptions and ranges; the
   purpose is to choose an appropriate scale, not to manufacture false precision.
3. Draw the smallest end-to-end data flow. Add a cache, queue, replica, partition, CDN,
   or secondary store only against an observed or estimated bottleneck, and record the
   new operational cost: invalidation, lag, ordering, duplicate delivery, conflicts,
   recovery, or cross-partition complexity.
4. Select data model, indexes, storage behaviour, replication, partitioning key, and
   transaction or consistency guarantee from the access patterns and invariants. State
   which reads may be stale, which operations require atomicity, how side effects are
   made idempotent, and where data can be lost or replayed.
5. Review the first failure at 10x expected load, dependency degradation behaviour,
   observability needs, backup and restore evidence, rollback boundary, and the
   operator-confirmation point before any infrastructure, data, billing, or deployment
   action. Load individual references as reviewed data for the decision in question.

## Output

Report requirements and assumptions, estimates and limiting resource, proposed data
flow, each component's explicit reason and cost, storage and consistency decisions,
capacity and failure boundaries, verification evidence still needed, residual risk,
and the next operator-confirmation point.
