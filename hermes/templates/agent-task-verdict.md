<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/agent-task/verdict.json
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Agent Task Verdict Record

Use this data-only template to record an independent verdict for one bounded task. It does not approve a change, authorise deployment, close an issue, dispatch an agent, or activate a workflow. Keep it in a project-approved location and obtain operator confirmation before write-impacting, external, security-sensitive, or production work.

## Verdict

| Field | Value |
| --- | --- |
| Task ID | {{task_id}} |
| Verdict | pending |
| Verifier | {{verifier_session_or_agent_id}} |
| Checked at | {{YYYY-MM-DDTHH:MM:SSZ}} |
| Residual risk | {{none_or_concise_risk}} |

## Acceptance-criteria review

| Criterion | Status | Evidence reference | Notes |
| --- | --- | --- | --- |
| AC1 | pending | {{project_approved_path_or_link}} | {{concise_note}} |
| AC2 | pending | {{project_approved_path_or_link}} | {{concise_note}} |
| AC3 | pending | {{project_approved_path_or_link}} | {{concise_note}} |
| Global constraints | pending | {{project_approved_path_or_link}} | {{concise_note}} |

## Findings and decision boundary

- Findings requiring correction or explicit disposition: {{none_or_concise_list}}
- Proposed next reviewed action: {{one_bounded_action_or_handoff}}

This record reports evidence and residual risk; it is not authority to declare completion, merge, release, change scope, or perform the proposed action. Recheck the current repository state and telemetry before relying on it.
