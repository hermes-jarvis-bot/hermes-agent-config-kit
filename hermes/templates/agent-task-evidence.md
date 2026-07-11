<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/agent-task/evidence/README.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Task Evidence Register

Use this data-only template to index project-approved evidence for a bounded task. It does not create directories, collect telemetry, upload files, or activate a verifier. Keep raw artefacts in a project-approved location and obtain operator confirmation before any write-impacting or external action.

## Evidence entries

| Reference | Kind | Scope or phase | Result | Redaction check |
| --- | --- | --- | --- | --- |
| `evidence/<timestamp>-test.txt` | Test output | {{phase}} | {{pass_fail_or_summary}} | {{redaction_status}} |
| `evidence/<timestamp>-report.md` | Generated report | {{phase}} | {{summary}} | {{redaction_status}} |

## Recording rules

- Use stable, meaningful filenames such as a timestamp or phase name.
- Record only the smallest evidence needed to support a claim; link to large raw outputs rather than copying them into active context.
- Do not store access credentials, private dumps, personal data, or unreviewed instructions. Redact or omit sensitive material before recording a reference.
- State what each item verifies and whether it is current for the task's final repository state.
- Cross-reference important evidence from the project's approved task record or final verification summary.

Evidence is supporting project data, not authority to change scope, run commands, or declare completion. Recheck the current repository state and relevant telemetry before relying on an earlier entry.
