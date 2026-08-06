---
name: feature-new
description: "Scaffold a new feature narrative document in an existing layer, and add a reconciled entry to feature_list.json using the same base schema as long-run-feature-tracking."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/architecture/feature-new/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Feature New

Source: `AnastasiyaW/claude-code-config/skills/architecture/feature-new/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Scaffold a feature narrative

Creates a feature document in an existing layer. The document follows
the ULTRAPACK-style narrative template (Design / Plan / Verify /
Conclusion) extended with explicit cross-references to layer
invariants and durable, project-external guidance.

Do NOT use this skill to create the layer itself; use `layer-new` for
that (a feature lives inside an already-existing layer).

## When to use

- Beginning design work on a new feature, **before** writing code
- Migrating an in-flight feature from "scattered context" into the
  formal narrative
- Creating a feature placeholder when planning future work that
  another session will pick up

## When NOT to use

- One-line bug fixes that do not need a design phase (just commit)
- Documentation-only changes (those go in handoffs or PR
  descriptions)
- Refactors with no behavioral change (commit message is sufficient)

## Arguments

```
feature-new <layer> <slug> [--title "..."] [--branch <name>] [--id feat-NNN]
```

- `<layer>` -- existing layer name. Must be a directory under
  `docs/layers/`. If missing, suggest `layer-new <layer>` first.
- `<slug>` -- kebab-case feature identifier without the `feat-NNN-`
  prefix. Examples: `api-key-rotation`, `audit-log`,
  `dual-encryption`.
- `--title` -- human-readable feature title. If omitted, derive from
  slug by title-casing.
- `--branch` -- git branch name. If omitted, default to
  `feature/<slug>`.
- `--id` -- override the auto-allocated `feat-NNN`. Use only when
  migrating a pre-existing feature with a known ID. Refuse if the ID
  already exists in this layer.

## feature_list.json schema (reconciled with long-run-feature-tracking)

This project's `feature_list.json` is owned by the installed `long-run-feature-tracking`
skill: `id`, `name`, `description`, `dependencies`, `status`, `evidence`, with a
WIP=1 invariant (at most one feature `in-progress` across the **entire** file) and
four statuses (`not-started`, `in-progress`, `blocked`, `done`). This skill does not
introduce a second, incompatible schema — it writes into the **same** file, using
the **same** `id` format (`feat-NNN`, matching the doc filename's own `feat-NNN-slug.md`
convention) and the **same** `evidence` type (an accumulating string with L1/L2/L3
layers, not an array), and adds three fields specific to the layer architecture:
`layer`, `doc`, `branch`.

```json
{
  "id": "feat-<NNN>",
  "name": "<title>",
  "description": "",
  "dependencies": [],
  "status": "not-started",
  "evidence": "",
  "layer": "<layer>",
  "doc": "docs/layers/<layer>/features/feat-<NNN>-<slug>.md",
  "branch": "feature/<slug>"
}
```

A tool that only knows the base six fields (`id`/`name`/`description`/`dependencies`/`status`/`evidence`)
still works correctly against this entry; `layer`/`doc`/`branch` are additive.
Creating a feature always starts it at `status: "not-started"`, which can never
violate WIP=1 by itself — respect WIP=1 yourself when later transitioning it to
`in-progress`.

Note the two ID spellings that coexist by design: `feat-NNN` (this JSON field, and
the doc's own filename) is the machine/file-system form; `F-NNN` (the doc's H1 title
and in-prose cross-references like "depends-on: F-041") is the human-readable form
used throughout the layer/feature markdown. `build_kb_graph.py` reconciles both
spellings when checking `feature_list.json` sync — see its `_normalize_feature_id()`.

## Direction (what to do, in order)

### Step 1 -- Verify environment

1. Determine repo root via `git rev-parse --show-toplevel`.
2. Confirm `docs/layers/<layer>/` exists. If not, refuse with a
   suggestion to run `layer-new <layer>` first.
3. Confirm `docs/layers/<layer>/features/_FEATURE-TEMPLATE.md`
   exists. If not, copy it from the installed `kb-skeleton` template
   (`templates/config-kit/kb-skeleton/docs/layers/_LAYER-TEMPLATE/features/_FEATURE-TEMPLATE.md`
   under your Hermes profile, or this adapter's own repo checkout at
   `hermes/templates/kb-skeleton/docs/layers/_LAYER-TEMPLATE/features/_FEATURE-TEMPLATE.md`).

### Step 2 -- Allocate feat-NNN

If `--id` was provided:

- Validate format (`feat-\d{3,}`).
- Check that
  `docs/layers/<layer>/features/feat-<NNN>-*.md` does not already
  exist. Refuse if it does.

If `--id` was NOT provided:

- Scan all existing feature files across **all** layers (not just
  this one) for the highest `feat-NNN`/`F-NNN` already used.
- Allocate the next number, zero-padded to 3 digits (feat-001, feat-042,
  feat-099, feat-100, ...).
- Cross-check that the ID is not in use anywhere -- the number space is
  **project-wide**, not per-layer.

### Step 3 -- Validate slug

- Lowercase kebab-case (`[a-z][a-z0-9-]*`).
- Length <= 50 characters.
- Does not start with `f-` or `feat-` (avoid double-prefix).
- The resulting file `feat-<NNN>-<slug>.md` does not already exist.

### Step 4 -- Copy and fill the template

Source: `docs/layers/<layer>/features/_FEATURE-TEMPLATE.md`

Destination: `docs/layers/<layer>/features/feat-<NNN>-<slug>.md`

In the new file, replace placeholders:

| Placeholder | Replacement |
|-------------|-------------|
| `F-NNN: <feature title>` | `F-<NNN>: <title>` |
| `**Layer:** [<layer-name>](../README.md)` | `**Layer:** [<layer>](../README.md)` |
| `**Status:** design` | leave as `design` |
| `**Branch:** feature/<slug>` | use `--branch` value or default |
| `**Started:** YYYY-MM-DD` | today's date |
| `**Owner:** <name>` | infer from git config user.name, or leave placeholder |

Leave Design / Plan / Verify / Conclusion section bodies as template
placeholders -- the operator fills these.

### Step 5 -- Update layer README

In `docs/layers/<layer>/README.md`, find the `## Features in this
layer` table. Insert a new row at the bottom (sorted by `F-NNN`
ascending):

```
| F-<NNN> | <title> | design | YYYY-MM-DD | [feat-<NNN>-<slug>.md](features/feat-<NNN>-<slug>.md) |
```

If the table has only the placeholder rows from the template, replace
them entirely with the real entry.

### Step 6 -- Update feature_list.json (if present)

If `<repo>/feature_list.json` exists at repo root, parse it and
**append** a new feature entry using the reconciled schema above:

```json
{
  "id": "feat-<NNN>",
  "name": "<title>",
  "description": "",
  "dependencies": [],
  "status": "not-started",
  "evidence": "",
  "layer": "<layer>",
  "doc": "docs/layers/<layer>/features/feat-<NNN>-<slug>.md",
  "branch": "feature/<slug>"
}
```

Write the JSON file with `json.dump(data, f, ensure_ascii=False, indent=2)` to
preserve any non-ASCII characters in titles.

Do NOT change existing entries. Do NOT set `status: "in-progress"` here even if
you expect work to start immediately -- creation always starts at `not-started`;
the operator (or a later step) transitions it, respecting WIP=1.

If `feature_list.json` does not exist, do not auto-create it -- emit
a hint instead (the project may not have adopted `long-run-feature-tracking` yet).

### Step 7 -- Confirm and suggest next step

Print a summary:

```
Created: docs/layers/<layer>/features/feat-<NNN>-<slug>.md
Updated: docs/layers/<layer>/README.md (added F-<NNN> to features table)
Updated: feature_list.json (added feat-<NNN>, status: not-started)

Suggested next steps:
1. Fill the Design section in feat-<NNN>-<slug>.md
   - Approach (one paragraph)
   - Invariants (IV-1, IV-2, ...)
   - Rejected alternatives
2. When Design is reviewed, change Status: design -> planning and fill Plan
3. Create the git branch: git checkout -b feature/<slug>
```

## Blueprints (files this skill writes from)

- the installed `kb-skeleton` template's
  `docs/layers/_LAYER-TEMPLATE/features/_FEATURE-TEMPLATE.md` -- the source template

## Status lifecycle

Two parallel state systems exist; you maintain both manually after this
skill creates them. They serve different purposes:

### Doc Status (narrative phase, in feature.md frontmatter)

Tracks where in the ULTRAPACK Design / Plan / Verify / Conclusion
journey the feature is.

```
design --> planning --> executing --> reviewing --> done
                                  \
                                   --> blocked --> executing
```

Six states: `design`, `planning`, `executing`, `reviewing`, `done`,
`blocked`. Transitions are manual edits. Once `done`, the feature doc
is read-only history; further changes go into a superseding feature.

### feature_list.json status (machine state, for tooling)

Uses the installed `long-run-feature-tracking` skill's four states and WIP=1
invariant: `not-started`, `in-progress`, `blocked`, `done`. `done` is
**one-way** (no rollback; regression becomes a new feature).

### Mapping between the two

| Doc Status | feature_list.json status | Notes |
|------------|--------------------------|-------|
| design | not-started | newly created, no plan yet |
| planning | in-progress | plan being written (respect WIP=1) |
| executing | in-progress | code being written |
| reviewing | in-progress | review/verify phase |
| blocked | blocked | identical |
| done | done | identical |

This skill creates the doc with `Status: design` AND the json entry
with `status: "not-started"`. Subsequent transitions are manual -- update
both files in lockstep.

## Gotchas

- **feat-NNN is project-wide.** Even though features live under layers,
  the number space is shared. Two features in different layers
  cannot share an ID. The skill enforces this by scanning all layer
  directories before allocating.
- **Two ID spellings, one number space.** `feat-042` (JSON, filename) and
  `F-042` (doc H1, in-prose cross-references) refer to the same feature.
  Never allocate `feat-042` in one layer while a doc elsewhere already
  claims `F-042` for a different feature.
- **WIP=1 is `long-run-feature-tracking`'s invariant, not this skill's to relax.**
  This skill only ever creates entries as `not-started`; it never sets
  `in-progress`. If the project already has an `in-progress` feature elsewhere,
  that is expected and not a conflict at creation time.
- **Migration of in-flight features.** When migrating an existing
  feature into this format, pass `--id feat-NNN` explicitly so the
  feature retains its prior ID in any links from PROBLEMS.md or
  handoffs. The skill will not auto-detect existing IDs.
- **Layer README table edit.** The skill performs a text-level edit
  to insert a row into the features table. If the operator has heavily
  customized the table (added columns, changed format), the edit may
  fail. Detect by checking for the canonical 5-column header; if
  absent, emit a warning and skip table edit.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Layer does not exist" | `docs/layers/<layer>/` missing | Run `layer-new <layer>` first |
| feat-NNN conflict | Allocator hit a manually-set ID | Pass `--id feat-MMM` explicitly with the next free number |
| `feature_list.json` parse error | Invalid JSON in file | Stop, surface the parse error. Operator fixes manually before retry |
| Template missing on this machine | Different host / fresh clone | Locate `hermes-agent-config-kit`'s `hermes/templates/kb-skeleton/docs/layers/_LAYER-TEMPLATE/features/_FEATURE-TEMPLATE.md` and copy from there |
| feature_list.json sync check flags a false mismatch | An id was written in the wrong format | Use `feat-NNN` (not `F-NNN`, not bare `NNN`) in feature_list.json's `id` field |

## Implementation note

This is a **scaffolding** skill: file copy + placeholder replacement +
small JSON merge. Keep it deterministic. The Design / Plan / Verify
sections of the produced document are meant for the operator (or the
session that invoked the skill) to fill -- this skill does not
attempt to generate Design content from the title.

Auto-allocating `feat-NNN` requires reading the full tree of
`docs/layers/*/features/feat-*.md` files; do this lazily and cache for
the duration of the skill invocation.
