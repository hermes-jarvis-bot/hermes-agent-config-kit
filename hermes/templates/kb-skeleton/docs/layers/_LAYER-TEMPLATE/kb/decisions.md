<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/kb-skeleton/docs/layers/_LAYER-TEMPLATE/kb/decisions.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# <Layer name> -- Architectural Decisions

Layer-scoped ADR log. Decisions affecting this layer only.
Project-wide decisions remain in `docs/kb/decisions.md`.

Each decision has: a unique ID (`D-N`), context, decision, consequences,
and references to the invariants or features it produces.

## Identity and format

- IDs are stable per layer (`D-1`, `D-2`, ...). Never reuse retired IDs.
- Format follows lightweight ADR: Context / Decision / Consequences.
- Each ADR cites the feature(s) or invariant(s) it produces or retires.

## D-1 -- <short decision name> (YYYY-MM-DD)

**Context:** <what we were trying to do, what alternatives existed, what
constraint forced a choice>.

**Decision:** <what we chose, stated as a positive assertion>.

**Consequences:**

- <good consequence>
- <good consequence>
- <bad consequence or trade-off>

**Implements / produces:** [IV-N](invariants.md#iv-n), F-NNN.

**Supersedes:** <prior decision if any, else "none">.

**Related principle:** <reference to a durable, project-external guidance
source, if any>.

<!-- Copy the block above per new decision. Order is chronological
top-down within this file. Keep the ID sequence monotonic. -->
