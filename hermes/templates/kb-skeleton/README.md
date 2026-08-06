<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/kb-skeleton/README.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# templates/kb-skeleton -- drop-in knowledge base

A minimal, project-agnostic starter for the pattern described in the installed
`knowledge-base-enforcement` skill (project-wide KB) and `feature-layer-architecture`
skill (the `docs/layers/` tier). The `layer-new` and `feature-new` skills scaffold
from this tree mechanically; `scripts/build_kb_graph.py` and `scripts/validate_kb.py`
check consistency once adopted.

## What is in the box

```
kb-skeleton/
├── AGENTS.md                       # AAIF-standard entry, fill in
├── docs/
│   ├── index.md                    # Map of docs/kb vs docs/layers
│   ├── kb/
│   │   ├── README.md               # Meta-rules (keep as-is or tweak)
│   │   ├── INVARIANTS.md           # Empty table, add I-1, I-2 ...
│   │   ├── conventions.md          # Empty sections, fill per stack
│   │   ├── patterns.md             # Empty sections, add recipes
│   │   ├── gotchas.md              # Empty, grow organically
│   │   ├── decisions.md            # Empty ADR log
│   │   └── modules/
│   │       └── example.md          # One skeleton file, copy per module
│   └── layers/
│       ├── README.md               # Layer index; see feature-layer-architecture
│       └── _LAYER-TEMPLATE/        # Copied by the layer-new skill
│           ├── README.md
│           ├── history.md
│           ├── kb/
│           │   ├── invariants.md
│           │   ├── decisions.md
│           │   ├── gotchas.md
│           │   └── patterns.md
│           └── features/
│               └── _FEATURE-TEMPLATE.md
└── scripts/
    ├── validate_kb.py               # Reviewed script; stdlib-only, read-only
    └── build_kb_graph.py            # Reviewed script; stdlib-only, read-only
```

Upstream also ships `.github/workflows/kb.yml`, a GitHub Actions workflow that runs
`validate_kb.py` on push/PR. This adapter never auto-converts anything under
`.github/workflows/**` regardless of content, so it is not included here. The workflow
itself is harmless (it only runs the read-only validator); copy it into your own
project's `.github/workflows/` by hand if you want CI enforcement — see upstream's
`templates/kb-skeleton/.github/workflows/kb.yml`.

## Adoption in 15 minutes

1. **Copy the tree into your repo root** (paths below assume this template was
   installed to `templates/config-kit/kb-skeleton/` under your Hermes profile,
   sibling to `skills/config-kit/`; adjust if you copied it from this adapter's own
   checkout instead):

   ```bash
   cp <kb-skeleton>/AGENTS.md          <your-repo>/AGENTS.md
   cp -r <kb-skeleton>/docs            <your-repo>/docs
   cp <kb-skeleton>/scripts/validate_kb.py     <your-repo>/scripts/
   cp <kb-skeleton>/scripts/build_kb_graph.py  <your-repo>/scripts/
   ```

2. **Fill `AGENTS.md`:** project one-liner, quick commands, source-of-truth docs.

3. **Configure `validate_kb.py`:** update the constants at the top
   (`REPO_ROOT`, source-area list) to match your project layout.

4. **Grow `INVARIANTS.md`** as your next review or first bug finds a
   rule worth codifying. Skeleton starts empty with a single example.

5. **Wire CI (optional):** copy `.github/workflows/kb.yml` from upstream if you want
   it; nothing here depends on it.

6. **Start referencing.** Every test that locks a rule gets a
   docstring like `"regression: <rule name>"`. Every entry in
   `INVARIANTS.md` points at the test.

7. **Adopt layers when they earn it.** Use the `layer-new` skill to scaffold a
   bounded concern, `feature-new` to scaffold a feature narrative inside it. See the
   adoption threshold in `feature-layer-architecture` before creating layer trees you
   do not need yet.

## feature_list.json

If your project also uses the `long-run-feature-tracking` skill's `feature_list.json`
convention, `feature-new` writes into the **same file and base schema** — it does not
create a second, incompatible one. See `feature-new`'s own notes for the exact
reconciled fields.

## What is NOT here

- Project-specific invariants (obviously).
- Opinionated per-module docs (you write one per area of your
  codebase).
- Language-specific conventions (the `conventions.md` skeleton just
  lists the *section titles* you should cover).

## Why this shape

See the installed `knowledge-base-enforcement` skill for the project-wide `docs/kb/`
rationale, and `feature-layer-architecture` for the `docs/layers/` tier. Short version:
review findings have three durable forms -- fix, test, invariant -- and without all
three, the expensive review artifact evaporates into commit history within weeks.

The kb-skeleton forces the third form to exist from day one.
