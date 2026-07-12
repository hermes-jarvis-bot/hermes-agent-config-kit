<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/long-run-project/PRD-BOOTSTRAP.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Long-Run Project Feature-Plan Proposal

Use this data-only template to prepare a proposed feature plan from an approved project brief, specification, or design record. It does not create project files, initialise machine-readable state, invoke a model, run a validator, or activate a workflow. Keep the completed record in a project-approved location and obtain operator confirmation before any write-impacting, external, security-sensitive, or production action.

## Input boundary

| Field | Value |
| --- | --- |
| Project or initiative | {{project_name}} |
| Approved brief reference | {{project_approved_path_or_link}} |
| Brief reviewed at | {{YYYY-MM-DDTHH:MM:SSZ}} |
| Planner | {{operator_or_session_id}} |
| Scope exclusions | {{explicit_exclusions}} |

Do not infer requirements not supported by the approved brief. If the input is incomplete, record the missing decision or evidence rather than inventing scope.

## Proposed features

| ID | User-facing deliverable | Dependencies | Initial status | Evidence boundary |
| --- | --- | --- | --- | --- |
| feat-001 | {{one_sentence_capability}} | none or {{feat_ids}} | not-started | Empty until verified work exists |
| feat-002 | {{one_sentence_capability}} | {{feat_ids}} | not-started | Empty until verified work exists |

## Review rules

- Keep the proposal small enough for deliberate review; split an oversized initiative into separately approved plans.
- Describe user-facing deliverables, not implementation chores.
- Use stable `feat-NNN` identifiers and list only dependencies that must be complete first.
- Seed every feature as `not-started`; selecting active work is a separate, approved decision.
- Keep at most one feature `in-progress` once a project adopts this convention.
- Record durable verification references only when a feature is reviewed complete or blocked; never pre-fill evidence with predictions.
- Check that dependencies are acyclic with a project-approved review method before relying on the plan.

## Decision boundary

This proposal is planning data, not authority to create a feature register, change project state, dispatch work, approve scope, or declare completion. Recheck the current repository state and telemetry before using it as the basis for a later action.
