---
name: architecture-first
description: "Design a system's module boundaries, dependency direction, state ownership, and domain vocabulary before implementation without prescribing premature layers or infrastructure choices."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/architecture-first/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Architecture First

Source: `AnastasiyaW/claude-code-config/skills/development/architecture-first/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Architecture First

Use this module before creating a service, API, subsystem, or cross-module feature
whose placement is not already clear. It is a read-only design protocol: it does not
create files, select frameworks, add dependencies, or authorise implementation.

## Scope and exclusions

This module decides where code lives: module responsibilities, dependency direction,
state ownership, and domain boundaries. Use `code-complexity` for function shape,
naming, and local complexity; `refactoring-safely` for splitting an already oversized
module; and `system-and-data-design` for capacity, storage, scaling, or distributed
systems choices. Use `lean-code` when the useful outcome is to remove unjustified
scope rather than establish a durable boundary. Do not introduce layers merely to
satisfy a diagram.

## Read-only design protocol

1. State the user outcome, change boundary, existing project constraints, and smallest
   viable vertical slice. Stop early for a script, spike, one-file task, or an existing
   seam that needs no boundary change.
2. Name modules by their reason to change and assign each mutable state item one owner.
   Record what each module may know and which interfaces expose that knowledge.
3. Draw dependency arrows. Business policy must not depend on framework, transport,
   storage, queue, or other delivery details; define ports from the inner policy side
   where an outer detail is necessary.
4. Establish ubiquitous language. Where one term has different meanings, draw a bounded
   context rather than forcing a shared model. Define aggregates around consistency
   needs and name domain events as meaningful completed facts.
5. Record a concise architecture note or ADR: module map, ownership, dependency flow,
   external boundaries, alternatives, decision, consequences, and assumptions.
6. Validate one vertical slice and tests that exercise policy without requiring the
   outer framework where practical. Treat dependency cycles, shared mutable state, and
   unexplained cross-boundary imports as design faults to resolve or explicitly accept.

## Output

Report the proposed module map, ownership and dependency evidence, vocabulary/context
boundaries, deliberately deferred details, vertical-slice verification, residual risk,
and the next operator-confirmation point for any write-impacting implementation.
