# hermes-agent-config-kit hooks

A Russian translation of this file is maintained by hand at `README_RU.md` — update it when
adding or materially changing a hook listed here.

Reviewed-hook lane (see `SECURITY.md`). These are Hermes-native reimplementations of
selected upstream Claude-Code/Codex guard hooks — never a copy-paste of the upstream file,
because the I/O contract differs (tool names, block-JSON shape, and critically: **Hermes
never blocks on exit code, only on a stdout JSON decision**).

`scripts/install_hermes.py --apply` copies this directory's files into
`<hermes-home>/hooks/config-kit/`. **It does not register anything in `~/.hermes/config.yaml`
and does not activate any hook.** Wiring a copied hook into your own profile is a deliberate,
manual, operator-performed step — this adapter never auto-executes or auto-activates
executable content.

Three flavors, by event — not every Claude Code hook event has a Hermes equivalent that
actually reaches the model, so check which bucket a hook falls into before assuming it behaves
like its upstream original:

- **`pre_tool_call` guards** (`destructive-command-guard.py`, `git-destructive-guard.py`,
  `self-harm-guard.py`, `command-injection-guard.py`) can genuinely block a call — Hermes
  parses their stdout JSON and denies the tool call before it runs.
- **`post_tool_call` guards** (`verify-deleted-guard.py`, `over-engineering-advisor.py`) are
  **audit-log-only**. Hermes's `post_tool_call` is a fire-and-forget observer event —
  `_emit_post_tool_call_hook()` in `model_tools.py` discards whatever `invoke_hook()` returns,
  so nothing a post_tool_call hook prints can reach the model's context in this turn or the
  next (verified 2026-08-08 against the live source; see `mappings/reviewed-hooks.yaml` for
  detail). These two write a durable verdict to the shared safety log instead — useful as an
  operator-inspectable audit trail, but not a live in-turn nudge to the agent, unlike upstream's
  Claude Code behavior. Revisit if a future Hermes version adds a context-injection path for
  `post_tool_call`.
- **`pre_llm_call`/`pre_verify`/`on_session_end` hooks** (`session-handoff-check.py`,
  `session-handoff-reminder.py`, `docs-staleness-guard.py`, `kb-validate-gate.py`) — a mixed
  bucket, verified individually rather than assumed: `pre_llm_call` (filtered to
  `extra.is_first_turn`) genuinely injects context into the model's first message, same as a
  working `pre_tool_call` block; `pre_verify` genuinely nudges the live agent but only on turns
  where the agent edited a file, capped at 3 nudges *per session, shared across every hook
  registered on it* (`session-handoff-reminder.py`, `kb-validate-gate.py`, and
  `transfer-contract-guard.py`'s Stop-equivalent portion all use it — see
  `kb-validate-gate.py`'s own section for the tradeoff that creates); `on_session_end` is
  audit-log-only like `post_tool_call`. See each hook's own section below.
- **`transfer-contract-guard.py` spans all three buckets at once** — one hook, registered on
  `pre_tool_call` (genuine block), `post_tool_call` (audit-log-only), and both `pre_verify`/
  `on_session_end` (dual-registered). See its own section below.

**Multi-session note (added 2026-08-10):** `session-handoff-check.py`, `session-handoff-reminder.py`,
and `transfer-contract-guard.py` all share a heartbeat mechanism
(`hermes_hook_common.touch_session_heartbeat()`/`session_is_live()`,
`.hermes/sessions/<session_id>/heartbeat`, 30-minute TTL, `HERMES_SESSION_HEARTBEAT_TTL`
override). This is what lets `transfer-contract-guard.py` tell a foreign-but-still-active
session's open transfer apart from an abandoned one, and it's also why
`session-handoff-check.py`/`session-handoff-reminder.py` scope their own markers per session
(`.hermes/sessions/<session_id>/{session-start,handoff-reminded}`) instead of per project — two
concurrent Hermes sessions in the same project no longer stomp on each other's state. Ported
from an upstream fix to `transfer-contract-guard.py` specifically; the equivalent fix for the
other two hooks was this adapter's own addition (upstream has not fixed that pair yet).

## Available hooks

### `destructive-command-guard.py`

Blocks catastrophically destructive shell commands run through the `terminal` tool:
`rm -rf` on root/home/wildcards, `DROP`/`TRUNCATE` without a `WHERE`, `kubectl delete --all`,
`docker system prune --volumes`, `mkfs`/`dd` on a block device, a fork bomb.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/destructive-command-guard.py"
      timeout: 10
```

Bypass: `HERMES_ALLOW_DESTRUCTIVE=1` or a `# hermes-bypass: destructive` marker in the command.

### `git-destructive-guard.py`

Blocks destructive git operations: `reset --hard`, `push --force`, `branch -D` (case-sensitive
— `-d` is allowed), `clean -fdx`, `checkout -- .`, `filter-branch`/`filter-repo`, deleting a
main/master/production ref, interactive rebase of HEAD, aggressive reflog/gc expiry.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/git-destructive-guard.py"
      timeout: 10
```

Bypass: `HERMES_ALLOW_GIT_DESTRUCTIVE=1` or a `# hermes-bypass: git-destructive` marker.

### `self-harm-guard.py`

Blocks commands that could cut the agent off from its own host: sshd config edits/restart/kill,
killing its own runtime process (`hermes`/`hermes_cli`/`node`/`bun`/`python` via
`killall`/`pkill -f`), iptables/ufw rules that drop its own connectivity, reboot without a
handoff.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/self-harm-guard.py"
      timeout: 10
```

Bypass: `HERMES_ALLOW_SELF_HARM=1` or a `# hermes-bypass: self-harm` marker.

### `command-injection-guard.py`

Detects shell-substitution injection: text meant as data that executes as a command via
`$(...)`/backticks before the outer command sees it (e.g. a `dropdb` smuggled into a
`gh issue create --body "$(...)"` call). Trivial, side-effect-free substitutions (`pwd`,
`date`, `git rev-parse`, etc.) pass; anything else with a destructive verb hard-blocks;
everything in between advisory-blocks pending confirmation.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/command-injection-guard.py"
      timeout: 10
```

Bypass: `HERMES_ALLOW_INJECTION=1` or a `# hermes-bypass: injection` marker.

### `verify-deleted-guard.py` (audit-log-only — see the note above)

After a destructive command runs (`rm`/`rmdir`, `docker rm`/`rmi`/`volume rm`/`network rm`,
`kubectl delete`, `curl -X DELETE`), checks whether the target is actually gone and logs
`verified-deleted` / `still-present` / `could-not-verify`. "Command exit 0" != "thing is gone."

```yaml
hooks:
  post_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/verify-deleted-guard.py"
      timeout: 15
```

No bypass — it never blocks, only logs.

### `over-engineering-advisor.py` (audit-log-only — see the note above)

After a `write_file` or `patch` call, logs an advisory when the change is large (net lines over
a tunable threshold) or touches a dependency manifest (`package.json`, `requirements.txt`,
etc.) — mechanically enforcing the quality-code / YAGNI ladder without ever blocking.

```yaml
hooks:
  post_tool_call:
    - matcher: "write_file|patch"
      command: "python3 ~/.hermes/hooks/config-kit/over-engineering-advisor.py"
      timeout: 15
```

Tunables: `HERMES_BLOAT_EDIT_LINES` (default 150), `HERMES_BLOAT_NEWFILE_LINES` (default 300).
Bypass: `HERMES_ALLOW_BLOAT=1` or a `# hermes-bypass: bloat` marker in the changed content.

### `session-handoff-check.py`

On the first LLM call of a new session, scans `.hermes/handoffs/` (project) and
`~/.hermes/handoffs/` (global) for recent handoffs and injects a listing into the model's
context so it can offer to continue. Unlike the two `post_tool_call` guards above, this one's
context genuinely reaches the model — `pre_llm_call`'s `{"context": ...}` return is appended
to the first user message (verified against the live source, not assumed).

```yaml
hooks:
  pre_llm_call:
    - command: "python3 ~/.hermes/hooks/config-kit/session-handoff-check.py"
      timeout: 10
```

Handoff directory override: `HERMES_HANDOFF_DIR` (default `.hermes/handoffs/` under the
project). No bypass — it never blocks, only injects context or stays silent.

### `session-handoff-reminder.py` (dual-registered — see note below)

Reminds to write a handoff when a session has run long (`SESSION_MIN_MINUTES`, default 15)
with no fresh handoff on disk (`HANDOFF_STALE_MINUTES`, default 30). Register on **both**
events — each covers a gap the other has:

```yaml
hooks:
  pre_verify:
    - command: "python3 ~/.hermes/hooks/config-kit/session-handoff-reminder.py"
      timeout: 10
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/session-handoff-reminder.py"
      timeout: 10
```

- `pre_verify` genuinely nudges the live agent to write a handoff before ending its turn, but
  Hermes only checks it when the agent edited a file *this turn*, and only up to 3 times per
  session total (shared with any other `pre_verify` consumer).
- `on_session_end` fires on every turn regardless of edits — the broad, reliable fallback —
  but is audit-log-only (see the note at the top of this file).

Both share the same `.hermes/.handoff-reminded`/`.hermes/.session-start` marker files, so
whichever fires first in a turn suppresses the other for the rest of the session. Handoff
directory override: same `HERMES_HANDOFF_DIR` as above. No bypass — it never blocks.

### `docs-staleness-guard.py`

On the first LLM call of a session, flags when `openwiki/` or `docs/layers/` has fallen more
than `HERMES_DOCS_STALE_COMMITS` (default 20) commits behind `HEAD`, or when `openwiki/`
exists but neither `AGENTS.md` nor `CLAUDE.md` points to it. Git-based, cooldown of 7 days
between nudges for the same project.

```yaml
hooks:
  pre_llm_call:
    - command: "python3 ~/.hermes/hooks/config-kit/docs-staleness-guard.py"
      timeout: 10
```

Extra anchors: list repo-relative paths in `.hermes/.docs-anchors` (one per line, `#` for
comments). Opt out per project: touch `.hermes/.skip-docs-staleness`. Ships its own
`--self-test` (pure git/filesystem logic — run it directly, no Hermes install needed):
`python3 hermes/hooks/docs-staleness-guard.py --self-test`.

### `kb-validate-gate.py` (dual-registered — see note above)

Blocks/logs while the repo's own `scripts/validate_kb.py` (see the `kb-skeleton` template)
reports the knowledge base out of sync with the code, or while a `[LONG-RUN]` project
(`feature_list.json` present) has no agent docs at all.

```yaml
hooks:
  pre_verify:
    - command: "python3 ~/.hermes/hooks/config-kit/kb-validate-gate.py"
      timeout: 30
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/kb-validate-gate.py"
      timeout: 30
```

Unlike `session-handoff-reminder.py`, this hook is willing to block on *every* eligible turn
while the KB stays broken — it does not self-suppress after one nudge. That means it competes
harder for the shared `pre_verify` 3-nudge/session budget: in the rare case where the KB is
genuinely broken *and* the session is also long with no fresh handoff, this hook could consume
the whole budget and leave `session-handoff-reminder.py` with no live nudge for the rest of
that session (its `on_session_end` audit-log entry still fires regardless — nothing is ever
silently lost, just possibly not surfaced live). If you'd rather cap this hook to one nudge per
session, add your own marker-file check before registering it, or register only
`on_session_end` and skip `pre_verify` entirely.

Bypass: `HERMES_SKIP_KB_GATE=1` or `.hermes/.skip-kb-gate`. Ships its own `--self-test`:
`python3 hermes/hooks/kb-validate-gate.py --self-test`.

### `transfer-contract-guard.py` (spans all three flavors — see note above)

Guards clone/copy/move/sync commands (`git clone`, `robocopy`, `rclone`, `rsync`, `scp`,
`sftp`, `xcopy`, `cp`/`copy`/`Copy-Item`, `mv`/`move`/`Move-Item`) with a durable JSON contract
under `.hermes/transfers/<id>.json` (see `templates/transfer-contract.json`'s shape). Register
on all three events:

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
  post_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
  pre_verify:
    - command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/transfer-contract-guard.py"
      timeout: 10
```

- `pre_tool_call` genuinely blocks a transfer command that has no
  `# transfer-contract: .hermes/transfers/<id>.json` marker, or whose contract is missing,
  incomplete, or describes a different operation than the command actually runs.
- `post_tool_call` reminds (stderr + safety log, audit-log-only) to update the contract and
  verify the destination before touching the source.
- `pre_verify`/`on_session_end` block/log while any contract stays open (`planned`/`running`/
  `verification_pending`) or closed-but-invalid — the orphan-transfer gate. This is a **third**
  consumer of the shared 3-nudge `pre_verify` budget, alongside `session-handoff-reminder.py`
  and `kb-validate-gate.py` — see `kb-validate-gate.py`'s section above for the tradeoff.

Recognizes `.hermes/transfers/`, `.claude/transfers/`, `.agent/transfers/`, and
`.codex/transfers/` (cross-harness: a contract written by another harness working the same
repo is still enforced). No bypass — this hook only ever blocks on a genuinely missing or
invalid contract; write the contract instead of looking for an escape hatch.

### `db-snapshot-guard.py` and `git-auto-backup.py` (never block — safety nets)

Once a destructive DB command or git op has already cleared its own blocking guard's bypass,
these take a best-effort backup right before allowing the op through, then warn on stderr if the
backup looks incomplete. Neither ever blocks — a machine without `pg_dump`/`mysqldump`/
`mongodump`/git available for the backup step must not be locked out of legitimate destructive
work.

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/db-snapshot-guard.py"
      timeout: 180
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/git-auto-backup.py"
      timeout: 10
```

`db-snapshot-guard.py` bypass: `HERMES_ALLOW_DB_SNAPSHOT=1` or `# hermes-bypass: db-snapshot`
(suppresses the whole safety net, use only on throwaway DBs). `git-auto-backup.py` only acts once
`HERMES_ALLOW_GIT_DESTRUCTIVE=1` is already set (the same bypass `git-destructive-guard.py`
uses) — if it isn't, that guard already blocked the command and this one never sees it act.
Creates `hermes-backup-<ts>` branches / `hermes-pre-clean-<ts>` stashes.

### `backup-retention-cleanup.py` (on_session_end — companion to `git-auto-backup.py`)

Deletes `hermes-backup-<ts>` branches and `hermes-pre-clean-<ts>` stashes older than 14 days.
Pure side effect (Hermes discards this event's return value, same as the audit-log-only guards
above) — idempotent, silent when nothing is old enough to remove.

```yaml
hooks:
  on_session_end:
    - command: "python3 ~/.hermes/hooks/config-kit/backup-retention-cleanup.py"
      timeout: 10
```

### `handoff-resume-gate.py` and `session-drift-validator.py`

Both `pre_llm_call`+`is_first_turn`, read-only, genuinely inject context (same mechanism as
`session-handoff-check.py` above). The first flags STALE-but-still-ACTIVE handoffs — a resuming
session should re-verify their claims, not trust them (shares `session-handoff-check.py`'s
`.hermes/handoffs/`/`HERMES_HANDOFF_DIR` convention). The second scans `CLAUDE.md`, `AGENTS.md`,
and `.claude/rules/*.md` for file-path references that no longer resolve on disk, staying silent
when everything checks out.

```yaml
hooks:
  pre_llm_call:
    - command: "python3 ~/.hermes/hooks/config-kit/handoff-resume-gate.py"
      timeout: 10
    - command: "python3 ~/.hermes/hooks/config-kit/session-drift-validator.py"
      timeout: 10
```

No bypass on either — they never block, only inject context or stay silent.

### `github-workflow-security.py`

Blocks the first edit of any `.github/workflows/*.yml(.yaml)` file per session to force a
GitHub-Actions command-injection checklist into context; later edits of the same file in the
same session are advisory-only (stderr).

```yaml
hooks:
  pre_tool_call:
    - matcher: "write_file|patch"
      command: "python3 ~/.hermes/hooks/config-kit/github-workflow-security.py"
      timeout: 10
```

Disable entirely: `HERMES_ALLOW_GH_WORKFLOW_SECURITY=1`.

### `repeated-attempt-guard.py` (dual-registered)

Stops the guess-and-retry loop: blocks a 4th attempt at the same command/file target after 3
failures with nothing read since the last one. A single read (of anything) clears it.

```yaml
hooks:
  post_tool_call:
    - command: "python3 ~/.hermes/hooks/config-kit/repeated-attempt-guard.py"
      timeout: 10
  pre_tool_call:
    - command: "python3 ~/.hermes/hooks/config-kit/repeated-attempt-guard.py"
      timeout: 10
```

Tunables: `HERMES_RETRY_SOFT` (default 2, advisory threshold), `HERMES_RETRY_HARD` (default 3,
block threshold), `HERMES_RETRY_WINDOW_SEC` (default 3600), `HERMES_RETRY_STATE` (state file
path). Bypass: `HERMES_ALLOW_RETRY_LOOP=1` or `# hermes-bypass: retry-loop` in the command.
Self-test: `python3 repeated-attempt-guard.py --self-test`.

## Activating any hook

Add the relevant block above to your own `~/.hermes/config.yaml`, then approve it at the
first-use consent prompt (or set `hooks_auto_accept: true` / `HERMES_ACCEPT_HOOKS=1` if you
already trust it). Verify with:

```bash
hermes hooks list
hermes hooks test pre_tool_call --for-tool terminal
hermes hooks doctor
```

Log: `~/.hermes/logs/config-kit-safety.log` (JSONL, one line per evaluated event, shared by all
hooks above).

## Testing without touching your live profile

Each hook has a stdlib-only test under `tests/` that pipes synthetic JSON directly to the
script's stdin and checks its stdout/stderr — the same wire format Hermes uses, with zero
dependency on a live Hermes install or `~/.hermes/config.yaml`:

```bash
python3 hermes/hooks/tests/test_destructive_command_guard.py
python3 hermes/hooks/tests/test_git_destructive_guard.py
python3 hermes/hooks/tests/test_self_harm_guard.py
python3 hermes/hooks/tests/test_command_injection_guard.py
python3 hermes/hooks/tests/test_verify_deleted_guard.py
python3 hermes/hooks/tests/test_over_engineering_advisor.py
python3 hermes/hooks/tests/test_session_handoff_check.py
python3 hermes/hooks/tests/test_session_handoff_reminder.py
python3 hermes/hooks/tests/test_docs_staleness_guard.py
python3 hermes/hooks/tests/test_kb_validate_gate.py
python3 hermes/hooks/tests/test_transfer_contract_guard.py
```

For deeper verification against Hermes's actual dispatch code path
(`agent.shell_hooks.run_once`), see the `functional_test` evidence recorded in
`mappings/reviewed-hooks.yaml` for each hook — those tests were run against an isolated
`ShellHookSpec` object, which never reads or writes `~/.hermes/config.yaml` or the shell-hooks
allowlist.
