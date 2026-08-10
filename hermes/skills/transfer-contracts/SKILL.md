---
name: transfer-contracts
description: "Record a durable JSON contract for every clone/copy/move/sync operation -- source, destination, verification plan, and source-cleanup intent -- so a later agent can resume without reconstructing intent from shell history."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/transfer-contracts.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Transfer Contracts

Source: `AnastasiyaW/claude-code-config/rules/transfer-contracts.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Transfer Contracts

File movement is shared mutable state. A later agent must be able to answer, without reading
shell history: what moved, from where, to where, with which settings, why, by when, what was
verified, and whether the source was removed.

## Required workflow

1. Create one JSON record under `.hermes/transfers/` before running the command. Use
   [transfer-contract.md](../templates/transfer-contract.md) as the starting shape. Keep
   records in the project repository or its private operational state; never put credentials
   in a public repository.
2. Add the marker to the command:

   ```text
   git clone https://example.invalid/repo D:/work/repo # transfer-contract: .hermes/transfers/2026-08-09_clone-repo.json
   ```

3. The reviewed transfer-contract guard hook (see `mappings/reviewed-hooks.yaml`) blocks
   the command unless the record is complete and its operation matches the command
   (`git clone`, `gh repo clone`, `robocopy`, `rclone`, `rsync`, `scp`, `sftp`, `xcopy`, `cp`,
   `copy`, `Copy-Item`, or `Move-Item`).
4. After the command, update `status` to `verification_pending` (or `failed`). Run the checks
   named in `verification.plan`, put the result and durable evidence paths/commands in
   `verification`, and only then use `verified`.
5. Source cleanup is a separate decision. Set `source_cleanup.planned` and explain it. If it is
   planned, the record cannot be `verified` until `performed=true` and `verified=true`.
   Deletion still requires the existing human-confirmation and post-delete verification gates
   (see the `safe-deletion` skill).
6. The session-end gate blocks while any record is open or invalid. A genuinely blocked,
   failed, or cancelled transfer may close only with a non-empty `closure_reason` and a useful
   `next_action`, so another agent can resume it. An open record owned by a different, still-
   live Hermes session is deferred instead of blocked -- see the hook's own docstring.

## Contract fields

| Field | Meaning |
| --- | --- |
| `source`, `destination` | Exact local path, repository URL, host path, or remote endpoint. |
| `operation.kind/tool/settings` | Copy, move, clone, or sync; tool used; flags and relevant settings. |
| `purpose`, `motivation`, `deadline` | Why the transfer exists and when it should be complete. |
| `verification.plan` | The checks that prove destination integrity before cleanup. |
| `verification.performed/result/evidence` | What was actually checked, the verdict, and where proof lives. |
| `source_cleanup` | Whether source deletion was planned, performed, and independently verified. |
| `session_id` | Which session opened the record; stamped automatically, used to scope the session-end gate to its actual owner. |
| `next_action`, `closure_reason` | The handoff for the next agent and why a non-success state is closed. |

The hook does not claim that an external/remote check happened. For remote paths, record the
command, log, checksum, manifest, or other durable evidence in `verification.evidence`. For
local verified destinations, the hook also checks that the destination exists; when cleanup is
claimed, it checks that the local source is gone.

## Mechanical wiring (Hermes-native)

The reviewed transfer-contract guard hook is registered on four Hermes events, not the three
Claude-Code events (`PreToolUse`/`PostToolUse`/`Stop`) this rule was originally written for:
`pre_tool_call` is the hard start gate (genuinely blocks); `post_tool_call` leaves an explicit
reminder (audit-log-only -- Hermes discards this event's return value); `pre_verify` and
`on_session_end` together are the orphan-transfer gate (`pre_verify` nudges the live agent on
file-edit turns, `on_session_end` is the reliable audit-log fallback for every turn). See the
hook's own docstring under `hermes/hooks/` for the exact mapping and the session-ownership
mechanism.
