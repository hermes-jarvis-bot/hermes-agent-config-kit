---
name: layer-new
description: "Scaffold a new layer in a project's docs/layers/ tree following the feature-layer architecture. A layer is a bounded concern with its own invariants, decisions, gotchas, patterns, and feature narratives."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/architecture/layer-new/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Layer New

Source: `AnastasiyaW/claude-code-config/skills/architecture/layer-new/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Scaffold a project layer

Creates `docs/layers/<layer-name>/` with the full template structure from the
installed `kb-skeleton` template. See the `feature-layer-architecture` skill for the
architecture this scaffolds and its adoption threshold — do not create a layer tree
before the project has earned the overhead.

## When to use

- Starting to track a new bounded concern in a long-running project
- Refactoring sprawling cross-cutting code into a documented layer
- Onboarding a new team member who needs the layer map

## When NOT to use

- One-off scripts or pet projects with <5 features (overhead not
  justified)
- Layer name describes a directory (`src` is not a layer)
- The "layer" is actually one feature in disguise -- use `feature-new`
  inside an existing layer instead

## Arguments

```
layer-new <layer-name> [--purpose "..."] [--principles <ref1>,<ref2>]
```

- `<layer-name>` -- kebab-case, single word preferred. Examples:
  `security`, `data`, `image-processing`, `observability`.
- `--purpose` -- one-sentence purpose. If omitted, prompt the operator.
- `--principles` -- comma-separated references to durable, project-external
  guidance (installed Hermes skills, or your own org's standards) that govern this
  layer. If omitted, leave placeholder in README.

## Direction (what to do, in order)

### Step 1 -- Verify environment

Check the current working directory:

1. Is it a git repository? Run `git rev-parse --show-toplevel`. If
   not, ask the operator whether to initialise one.
2. Does `docs/` exist? If not, create it.
3. Does `docs/layers/README.md` exist? If not, copy it from this adapter's
   installed `kb-skeleton` template (`templates/config-kit/kb-skeleton/docs/layers/README.md`
   under your Hermes profile, sibling to `skills/config-kit/`; or from this adapter's
   own repo checkout at `hermes/templates/kb-skeleton/docs/layers/README.md` if you
   are working inside `hermes-agent-config-kit` itself).
4. Check if `docs/layers/<layer-name>/` already exists. If yes,
   **stop** with a message -- do not overwrite. Suggest
   `feature-new <layer> <slug>` instead.

### Step 2 -- Validate layer name

- Must be lowercase kebab-case (`[a-z][a-z0-9-]*`).
- Must not start with `_` (reserved for templates).
- Must not be a generic file-system name (`src`, `tests`, `docs`,
  `build`).
- If invalid, refuse with a clear message and a suggested fix.

### Step 3 -- Copy the template

Source: the installed `kb-skeleton` template's
`docs/layers/_LAYER-TEMPLATE/` (same location resolved in Step 1).

Destination: `<repo>/docs/layers/<layer-name>/`

Copy the entire directory tree. Preserve subdirectory structure (`kb/`
and `features/`). Result:

```
docs/layers/<layer-name>/
├── README.md
├── history.md
├── kb/
│   ├── invariants.md
│   ├── patterns.md
│   ├── decisions.md
│   └── gotchas.md
└── features/
    └── _FEATURE-TEMPLATE.md
```

### Step 4 -- Fill placeholders

In every file under the new layer, replace:

- `<layer-name>` -> the actual layer name
- `<Layer name>` -> Title Case of the layer name (e.g. "Security",
  "Image Processing")

In `README.md` specifically:

- `**Purpose:** <one sentence...>` -> the `--purpose` argument value,
  or prompt the operator
- `## Governing principles` list -> populate from `--principles` arg,
  or leave the placeholder bullets in place for the operator to fill

In `history.md`:

- Insert a "Layer created" entry at the top with today's date
  (YYYY-MM-DD) and the originating reason. Prompt the operator for the
  reason if not provided.

### Step 5 -- Register the layer

Update `docs/layers/README.md`:

- Add a row to the `## Layer index` table:
  `| <layer-name> | <purpose> | active |`
- If a cross-layer Mermaid graph exists, add a node for the new layer
  with no edges (operator will add edges as dependencies form).

### Step 6 -- Wire to project state

If the project has `feature_list.json` at repo root, leave it alone --
features get added by `feature-new`. Do not edit `feature_list.json`
from this skill.

If the project has `AGENTS.md`, suggest (but do not auto-edit) adding
the new layer to its source-of-truth-docs table if multiple layers
exist.

### Step 7 -- Confirm and suggest next step

Print a summary:

```
Layer created: docs/layers/<layer-name>/
Files: 1 README, 1 history, 4 kb/, 1 feature template

Suggested next steps:
1. Fill governing principles in docs/layers/<layer-name>/README.md
2. Write the first feature: feature-new <layer-name> <slug>
3. Add the first invariant when it earns its place
```

## Blueprints (files this skill writes from)

- the installed `kb-skeleton` template's `docs/layers/_LAYER-TEMPLATE/` -- the
  source tree to copy
- the installed `kb-skeleton` template's `docs/layers/README.md` -- the layers
  index template (used only if missing)

## Gotchas

- **Renaming a layer is not idempotent.** If the operator runs
  `layer-new wrong-name` then realises they wanted `right-name`,
  manually rename the directory and update references. This skill
  does NOT detect or fix duplicates.
- **Layer name collision with existing directories.** If
  `docs/<layer-name>/` exists at the `docs/` root (not under
  `docs/layers/`), refuse and ask the operator which they want -- there
  is no automatic merge.
- **Template location varies by install.** If the `kb-skeleton` template cannot be
  found under either the Hermes-installed `templates/config-kit/` path or this
  adapter's own repo checkout, stop and report the missing location rather than
  inventing a directory tree from memory.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Layer already exists" | Directory `docs/layers/<name>/` present | Use `feature-new` to add to it, or pick a different name |
| Template files missing | `kb-skeleton` not installed or repo checkout unavailable | Locate `hermes-agent-config-kit`'s `hermes/templates/kb-skeleton/` and copy from there |
| Layers README not updated | `docs/layers/README.md` had no `## Layer index` table | Open file manually, add table per the `kb-skeleton` template |
| Validator warns about layer | `validate_kb.py`/`build_kb_graph.py` flagged something | Layer is fine; the flagged item is in a feature doc inside it. Run the project's own copy of the graph-builder script (from the `kb-skeleton` template) for the full health report. |

## Implementation note

The bulk of the work is file copy + placeholder replacement. No
dynamic logic is needed; the template files do all the structural
heavy lifting. Keep this skill **deterministic and idempotent** -- it
must be safe to invoke twice on the same layer (second call should be
a no-op with a clear message).
