<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/transfer-contract.json
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# Transfer Contract Record

Use this data-only template to record a durable contract for one clone/copy/move/sync operation before running it. It does not create directories, run the transfer, verify a destination, delete a source, or activate a workflow. Keep it in a project-approved location (for example `.hermes/transfers/<id>.json`) and obtain operator confirmation before write-impacting, external, security-sensitive, or production work. See the `transfer-contracts` skill for the full workflow this record supports.

## Identity and status

| Field | Value |
| --- | --- |
| Transfer ID | {{transfer_id}} |
| Status | planned |
| Source | {{exact_local_path_or_repository_url_or_remote_endpoint}} |
| Destination | {{exact_local_path_or_repository_url_or_remote_endpoint}} |
| Purpose | {{why_the_transfer_exists}} |
| Motivation | {{why_now}} |
| Deadline | {{ISO-8601_date_or_time}} |
| Owner | {{session_or_agent_id}} |

Status is one of: `planned`, `running`, `verification_pending`, `verified`, `failed`, `blocked`, `cancelled`.

## Operation

| Field | Value |
| --- | --- |
| Kind | {{copy_move_clone_or_sync}} |
| Tool | {{tool_used}} |
| Settings | {{flags_or_relevant_settings}} |

## Verification

| Field | Value |
| --- | --- |
| Plan | {{list_of_checks_that_prove_destination_integrity}} |
| Performed | false |
| Result | {{pass_or_fail_once_run}} |
| Evidence | {{durable_evidence_paths_commands_or_checksums}} |

Do not claim `verified` without `performed=true`, a `pass` result, and non-empty evidence. For
remote destinations, record the command, log, checksum, or manifest that proves integrity; a
local destination additionally needs the path confirmed to exist.

## Source cleanup

| Field | Value |
| --- | --- |
| Planned | {{true_or_false}} |
| Performed | false |
| Verified | false |
| Reason | {{why_cleanup_is_or_is_not_planned}} |

Source deletion is a separate decision from the transfer itself, and still requires this
adapter's own deletion-confirmation and post-delete-verification gates (see `safe-deletion`).
A `verified` record with `source_cleanup.planned=true` requires both `performed=true` and
`verified=true`.

## Next action and closure

| Field | Value |
| --- | --- |
| Next action | {{one_concrete_step_for_the_next_agent}} |
| Closure reason | {{required_if_status_is_failed_blocked_or_cancelled}} |
