<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/kb-skeleton/docs/index.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# {PROJECT} — Knowledge Base

Per-project knowledge, co-located with the code (feature-layer architecture).

## Map
- **[kb/](kb/)** — cross-cutting project knowledge: invariants, decisions (ADR), gotchas, patterns, conventions.
- **[layers/](layers/)** — bounded concerns (security / data / ui / infra / domain), each with its own KB + feature narratives.

## Conventions
- IDs: `IV-N` invariant · `D-N` decision · `G-N` gotcha · `PT-N` pattern · `F-NNN` feature.
- Decisions are append-only ADRs; an invariant changes only via a new decision.
- Keep entries dense and runnable — code/configs/gotchas, not tutorials.

## Rendering

Upstream renders this tree with a shared MkDocs Material container specific to that
project's own infrastructure. This adapter does not ship or assume any renderer —
these are plain markdown files, readable as-is; wire your own docs pipeline if you
want rendered output.
