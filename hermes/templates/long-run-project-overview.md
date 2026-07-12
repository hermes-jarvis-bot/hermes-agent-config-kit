<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/long-run-project/README.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Long-Run Project Tracking Overview

Use this data-only template to assess whether a project that spans several sessions needs a reviewed feature record and health evidence. It does not create project files, initialise machine-readable state, run checks, install a routine, or activate automation. Keep any completed record in a project-approved location and obtain operator confirmation before write-impacting, external, security-sensitive, or production work.

## Applicability review

| Question | Evidence | Decision |
| --- | --- | --- |
| Does the work span multiple sessions or independently reviewable deliverables? | {{evidence}} | {{yes_no_or_uncertain}} |
| Would a stable feature record reduce scope, handoff, or dependency ambiguity? | {{evidence}} | {{yes_no_or_uncertain}} |
| Is there a documented, project-appropriate health check or verification entry point? | {{evidence}} | {{yes_no_or_uncertain}} |
| Is a lightweight handoff sufficient instead? | {{evidence}} | {{yes_no_or_uncertain}} |

Do not add tracking structure merely because it is available. Short-lived, exploratory, or one-off work may need only concise handoff notes and current verification evidence.

## Proposed record boundary

If the project adopts a feature record after review, define it before creating any state:

| Field | Proposed value |
| --- | --- |
| Record owner | {{operator_or_project_owner}} |
| Approved location | {{project_approved_path}} |
| Feature identifier format | {{stable_identifier_format}} |
| Allowed statuses | not-started, in-progress, blocked, done |
| Work-in-progress boundary | {{project_specific_limit_or_not_applicable}} |
| Completion evidence | {{approved_static_runtime_system_evidence}} |
| Health evidence source | {{documented_check_or_not_applicable}} |

## Review rules

- Keep identifiers stable and describe user-facing outcomes rather than implementation chores.
- Treat a status change as a reviewed project decision; do not infer completion from a chat claim.
- Record only evidence that exists and is safe to reference. Exclude access credentials, private dumps, and unreviewed instructions.
- If a completed deliverable later regresses, record the corrective work as a new bounded item with its own evidence rather than rewriting history.
- Use the smallest appropriate evidence set: static, runtime, and system-level proof are examples, not mandatory layers for every project.
- A documented health check is not authority to run it. Execute checks only under the project's normal approval and environment policy.

## Decision boundary

This overview is planning data, not authority to create a register, add a script, run a validator, change project state, dispatch work, or declare completion. Recheck current repository state and telemetry before relying on an earlier assessment.
