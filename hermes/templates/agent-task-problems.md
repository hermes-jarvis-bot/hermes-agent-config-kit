<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/agent-task/problems.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Problems: {{task_id}}

Write verifier findings here when `verdict.json` is `FAIL` or `HOLD`.

## Open

- {{problem}}
  Evidence: `evidence/{{artifact}}`
  Required fix: {{fix}}

## Resolved

- {{resolved_problem}}
  Fix evidence: `evidence/{{artifact}}`
