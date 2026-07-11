<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/agent-task/trace.jsonl
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Agent Task Trace Record

Use this data-only template to record one reviewed event in the timeline of a bounded task. It does not create a task directory, initialise state, dispatch an agent, run a workflow, or authorise an action. Keep the record in a project-approved location and obtain operator confirmation before write-impacting, external, security-sensitive, or production work.

## Trace entry

| Field | Value |
| --- | --- |
| Timestamp | {{YYYY-MM-DDTHH:MM:SSZ}} |
| Task ID | {{task_id}} |
| Phase | {{spec_or_approved_phase}} |
| Responsible session or agent | {{session_or_agent_id}} |
| Reviewed event | {{concise_event}} |
| Claim | {{evidence-backed_claim}} |
| Evidence reference | {{project_approved_path_or_link}} |
| Decision | {{continue_pause_or_handoff}} |

## Next action boundary

Record at most one proposed bounded next action, such as freezing a specification, implementing an approved change, collecting evidence, running fresh verification, correcting a verified fault, or preparing a handoff. This entry is project data, not authority to change scope, perform the action, or declare completion. Recheck the current repository state and telemetry before relying on it.
