<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/agent-task/handoff.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Handoff: {{task_id}}

## Goal

{{one_sentence_objective}}

## Current State

{{current_state}}

## Done

- {{done_item}} -- evidence: `evidence/{{artifact}}`

## Not Done

- {{not_done_item}}

## Decisions

- {{decision}} -- rationale: {{rationale}}

## Next Step

{{next_step}}

## Must Read First

- `spec.md`
- `state.json`
- `verdict.json`
- `problems.md` if verdict is not `PASS`
