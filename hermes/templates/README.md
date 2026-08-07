# Templates Catalog

Data-only Hermes-adapted templates. None of these create files, initialise state, dispatch
an agent, or activate automation on their own — each is a starting point an operator copies
into a project-approved location and fills in, with operator confirmation before any
write-impacting, external, or production action.

This file is hand-maintained (there are few enough templates that a generator script would
be more machinery than it's worth) — update it when adding, removing, or retiring a template.
A Russian translation is maintained by hand at `README_RU.md`.

## Install

Preview, then apply, into a disposable or real Hermes home with the adapter's own installer:

```bash
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-home
python3 scripts/install_hermes.py --apply --hermes-home /tmp/hermes-home
```

This copies every template below into `<hermes-home>/templates/config-kit/`. Remove the same
way with `scripts/remove_hermes.py --dry-run|--apply`.

## Agent task record

A per-task set of records for a bounded, long-running, multi-session, or high-risk task.
Adopt only the records a project actually needs.

| Template | Description |
|---|---|
| [agent-task-overview.md](agent-task-overview.md) | Data-only index explaining what the agent-task record set is and when to adopt it. |
| [agent-task-spec.md](agent-task-spec.md) | Frozen objective and acceptance criteria for one bounded task, agreed before building starts. |
| [agent-task-state.md](agent-task-state.md) | Current machine-readable state of one bounded task. |
| [agent-task-evidence.md](agent-task-evidence.md) | Index of project-approved evidence (test output, logs, artefacts) for a bounded task. |
| [agent-task-trace.md](agent-task-trace.md) | One reviewed event in a bounded task's timeline. |
| [agent-task-verdict.md](agent-task-verdict.md) | An independent PASS/FAIL/BLOCKED verdict record for a bounded task. |
| [agent-task-fix-log.md](agent-task-fix-log.md) | Log of fix passes applied against a verdict's findings. |
| [agent-task-problems.md](agent-task-problems.md) | Verifier findings to address, written when a verdict is FAIL or HOLD. |
| [agent-task-handoff.md](agent-task-handoff.md) | Structured handoff for one bounded task between sessions. |
| [agent-task-scratchpad.md](agent-task-scratchpad.md) | Short-lived working memory for resuming a task — not a transcript. |

## Long-run project tracking

For a project spanning many sessions, deciding whether it needs a reviewed feature record
and health evidence, and proposing that plan from an approved brief.

| Template | Description |
|---|---|
| [long-run-project-overview.md](long-run-project-overview.md) | Assess whether a multi-session project needs a reviewed feature record and health evidence. |
| [long-run-project-prd-bootstrap.md](long-run-project-prd-bootstrap.md) | Prepare a proposed feature plan from an approved project brief, specification, or design record. |

## Verification

| Template | Description |
|---|---|
| [proof-plan.md](proof-plan.md) | Frozen acceptance criteria, exact verification commands, expected outcomes, scope, and constraints for one verification pass. |

## Knowledge-base skeleton

| Template | Description |
|---|---|
| [kb-skeleton/](kb-skeleton/) | Drop-in knowledge-base directory tree (global KB, per-project layers, feature narratives) for the feature-layer-architecture skill's `/layer-new` and `/feature-new` scaffolding. See its own `kb-skeleton/README.md`. |
