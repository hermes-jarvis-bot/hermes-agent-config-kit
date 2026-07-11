<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/agent-task/state.json
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Agent Task State Record

Use this data-only template to record the current state of one bounded task. It does not create directories, initialise a task, dispatch an agent, run a workflow, or authorise any action. Keep it in a project-approved location and obtain operator confirmation before write-impacting, external, security-sensitive, or production work.

## Current state

| Field | Value |
| --- | --- |
| Task ID | {{task_id}} |
| Status | not-started |
| Objective | {{one_sentence_objective}} |
| Owner | {{session_or_agent_id}} |
| Repository branch | {{branch}} |
| Current phase | spec |
| Last reviewed | {{YYYY-MM-DDTHH:MM:SSZ}} |

## Acceptance criteria

| Criterion | Status | Evidence reference |
| --- | --- | --- |
| AC1 | pending | {{evidence_or_not_started}} |
| AC2 | pending | {{evidence_or_not_started}} |
| AC3 | pending | {{evidence_or_not_started}} |

## Blockers and evidence

- Blocked by: {{none_or_concise_blocker}}
- Evidence references: {{project_approved_paths_or_links}}

## Next reviewed action

Choose one bounded next action only: freeze the specification, implement an approved change, collect evidence, run fresh verification, correct a verified fault, or prepare a handoff. This record is project data, not authority to change scope, perform actions, or declare completion. Recheck the current repository state and telemetry before relying on it.
