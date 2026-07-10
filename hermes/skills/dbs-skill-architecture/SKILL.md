---
name: dbs-skill-architecture
description: "Structure Hermes skills by separating operational direction, on-demand references, and quarantined deterministic routine candidates."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/17-dbs-skill-creation.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Dbs Skill Architecture

Source: `AnastasiyaW/claude-code-config/principles/17-dbs-skill-creation.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# DBS Skill Architecture

This adaptation provides a small information-architecture review for Hermes modules. It separates guidance that belongs in a skill from on-demand reference material and deterministic work that must stay in review until separately approved. It does not create support files, install routines, or activate any automation.

## Principle

Classify each candidate component before adding it to a Hermes module:

| Class | Purpose | Safe default target |
| --- | --- | --- |
| Direction | Decision logic, procedures, boundaries, recovery paths | `SKILL.md` |
| Blueprints | Stable examples, templates, taxonomies, lookup material | reviewed `references/` or `templates/` support file |
| Solutions | Deterministic operations such as API calls, calculations, validation, or file mutation | review/quarantine lane; no activation by default |

The classification is an architecture aid, not a permission grant. A component's content, provenance, scope, and side effects still determine whether it can be added.

## Review protocol

1. Define the module's operator-facing outcome and trigger conditions.
2. Keep only reusable decision logic and safety boundaries in `SKILL.md`.
3. Move lengthy but stable material to a reviewed support file only when on-demand loading improves clarity.
4. Treat any deterministic routine as executable design work: document its inputs, outputs, permissions, failure modes, test plan, and removal path.
5. Keep executable candidates quarantined until an operator approves the exact implementation and activation scope.
6. Verify all links and support-file paths, then run focused validation appropriate to the changed artefact.

## Direction

Direction should tell an operator or agent when to use the module, what prerequisites apply, the ordered protocol, decision points, expected evidence, and when to stop for operator confirmation. Keep it concise enough to load routinely. Do not bury safety constraints under large examples or copied research notes.

## Blueprints

Use blueprints for stable material that is useful only for particular invocations, for example a report outline, taxonomy, configuration skeleton, or worked example. Each support file must stay inside a Hermes-allowed directory, be source-reviewed, and have a clear link from the parent module.

Do not add a support file merely to make a module look comprehensive. If the main procedure is short and self-contained, keep it that way.

## Solution candidates

Deterministic work can reduce reasoning errors, but it changes the risk profile. Before proposing a routine, establish:

- exact inputs, outputs, paths, network use, and required access credentials;
- read-only, write-impacting, external, billing, and production effects;
- dry-run behaviour, test fixtures or disposable environment, and rollback/removal method;
- an owner and operator-confirmation point for implementation or activation.

Do not convert examples of deterministic work into active code automatically. A documented candidate remains documentation until separately reviewed.

## Relationship to other modules

- Use `skill-authoring-best-practices` for triggers, lifecycle, and support-file conventions.
- Use `documentation-integrity` to verify generated paths, links, and module lists.
- Use `deterministic-orchestration` to design a reviewed routine after its safety boundary is approved.
- Use `supply-chain-defense` when the source material or dependencies are external.

## Reporting

Report the selected direction, any blueprint retained with its path, every solution candidate kept in review/quarantine, verification performed, and any approval still required. Clear separation prevents a helpful reference from quietly becoming an unreviewed capability.
