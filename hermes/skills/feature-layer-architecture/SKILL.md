---
name: feature-layer-architecture
description: "Organize long-running project knowledge into layers and feature narratives that preserve rationale, evidence, and history without replacing machine state."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/28-feature-layer-architecture.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Feature Layer Architecture

Source: `AnastasiyaW/claude-code-config/principles/28-feature-layer-architecture.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Feature Layer Architecture

Upstream source policy describes a three-tier knowledge model for long-running projects. Hermes adaptation keeps the architectural pattern — global principles, project layers, and feature narratives — while removing product-specific templates, command names, raw URL prescriptions, and automatic tooling assumptions.

## Principle

Organize long-running project knowledge into layers and feature narratives when machine state alone no longer preserves design rationale.

Use this module when a project has enough history that `feature_list.json`, handoffs, and commit logs tell what happened, but not why the current shape exists.

## Three-tier model

Use a three-tier tree:

1. **Global knowledge** — reusable principles, rules, and modules that transfer across projects.
2. **Project layer knowledge** — bounded concerns inside one project: security, data, infrastructure, UI, domain logic, operations, or integration boundaries.
3. **Feature narratives** — per-feature design, plan, verification evidence, deviations, and conclusion.

The tiers have different jobs. Do not collapse them into one mega-document.

## What is a layer?

A layer is a bounded concern, not merely a folder name.

Examples:

- security and access control;
- data model and persistence;
- user interface and interaction design;
- infrastructure and deployment;
- external integrations;
- domain logic;
- operational runbooks.

A file may participate in multiple layers. A feature has one primary layer and may explicitly touch secondary layers.

## Recommended structure

For projects that earn the overhead, keep layer material under a predictable project-local location such as:

```text
docs/layers/<layer-name>/
  README.md
  kb/
    invariants.md
    decisions.md
    gotchas.md
    patterns.md
  history.md
  features/
    feat-NNN-<slug>.md
```

This is a convention, not a command to create directories blindly. Start with the smallest layer tree that helps future work.

## Layer README

Each layer entry point should state:

- purpose;
- status: active, deprecated, merging, or archived;
- governing principles and project rules;
- local invariants summary;
- feature index;
- dependencies on other layers;
- where verification evidence lives.

## Layer knowledge base

Layer-local KB files should separate different kinds of knowledge:

- **invariants** — rules that must remain true for this layer;
- **decisions** — architectural decisions and rejected alternatives;
- **gotchas** — pitfalls, incident lessons, and sharp edges;
- **patterns** — reusable recipes that have survived verification.

If a layer-local pattern is reused across projects, promote it deliberately into a global principle or module. Promotion should be earned by usage, not optimism.

## Feature narrative

A feature narrative should preserve:

- feature ID and title;
- primary layer and touched layers;
- status;
- related feature IDs;
- design rationale;
- assumptions and unknowns;
- plan and phases;
- files and interfaces touched;
- verification evidence;
- deviations from plan;
- conclusion and future work.

When the feature is done, close the narrative as history. Do not keep rewriting old feature documents to pretend the original plan was perfect. New work gets a new feature or superseding note.

## Relationship to machine state

Use `long-run-feature-tracking` for machine-readable state: IDs, status, dependencies, and evidence pointers.

Use feature-layer architecture for human-readable rationale: why this layer exists, why a feature took its shape, what alternatives were rejected, and what should not be rediscovered six weeks later.

The two should cite each other, but not duplicate each other.

## Adoption threshold

This earns its complexity when the project has:

- multiple months of work;
- five or more active concerns;
- multiple sessions or collaborators;
- recurring confusion about why code is shaped a certain way;
- cross-cutting features that touch more than one concern;
- verified decisions that keep getting rediscovered.

Skip it for:

- short-lived utilities;
- one-off migrations;
- prototypes or spikes;
- projects with only a few features;
- teams that will not maintain the documents.

Documentation nobody updates is not architecture. It is sediment.

## Adoption protocol

1. Identify the few bounded concerns that currently cause navigation pain.
2. Create only those layer entries.
3. For each layer, write the README first: purpose, invariants, active features, dependencies.
4. Move or link existing durable evidence rather than rewriting history from memory.
5. Add feature narratives only for active or high-value completed features.
6. Cross-link to `feature_list.json`, issue trackers, commits, and verification artefacts.
7. Add validation only after the manual convention is stable.

## Review checklist

Before adopting or expanding this structure, verify:

- [ ] The project is long-running enough to justify the overhead.
- [ ] Each layer is a bounded concern, not a renamed directory.
- [ ] Machine state and human narrative are not duplicated.
- [ ] Feature documents have clear ownership and closure rules.
- [ ] Layer history is append-only or otherwise auditable.
- [ ] Links point to durable artefacts rather than transient chat.
- [ ] Promotion from feature to layer to global knowledge is based on reuse.

## Avoid

- Creating a full layer tree before there are real layers.
- Writing layer documentation as a substitute for tests, issues, or feature state.
- Baking project-local paths into global rules.
- Letting feature docs become mutable status dashboards.
- Treating old chat transcripts as durable rationale.
- Adding validators before the information model is stable.

## Reporting format

When using this module, report:

- project maturity signal;
- proposed layers;
- feature narratives to create or migrate;
- what remains in machine-readable state;
- what becomes layer knowledge;
- validation plan, if any;
- overhead intentionally avoided.

The goal is not more documents. The goal is to make the project’s memory navigable without asking the same questions every month.
