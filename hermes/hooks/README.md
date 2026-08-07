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

## Available hooks

### `destructive-command-guard.py`

Blocks catastrophically destructive shell commands run through the `terminal` tool:
`rm -rf` on root/home/wildcards, `DROP`/`TRUNCATE` without a `WHERE`, `kubectl delete --all`,
`docker system prune --volumes`, `mkfs`/`dd` on a block device, a fork bomb.

To activate, add this to your own `~/.hermes/config.yaml`:

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "python3 ~/.hermes/hooks/config-kit/destructive-command-guard.py"
      timeout: 10
```

Then approve it at the first-use consent prompt (or set `hooks_auto_accept: true` /
`HERMES_ACCEPT_HOOKS=1` if you already trust it). Verify with:

```bash
hermes hooks list
hermes hooks test pre_tool_call --for-tool terminal
hermes hooks doctor
```

Bypass a single call with `HERMES_ALLOW_DESTRUCTIVE=1` in the session, or a
`# hermes-bypass: destructive` marker in the command text itself (useful when the env var
isn't visible to the hook's subprocess).

Log: `~/.hermes/logs/config-kit-safety.log` (JSONL, one line per evaluated event).

## Testing without touching your live profile

`tests/test_destructive_command_guard.py` pipes synthetic JSON directly to the script's
stdin and checks its stdout — the same wire format Hermes uses, with zero dependency on a
live Hermes install or `~/.hermes/config.yaml`:

```bash
python3 hermes/hooks/tests/test_destructive_command_guard.py
```

For deeper verification against Hermes's actual dispatch code path
(`agent.shell_hooks.run_once`), see the review evidence recorded in
`mappings/reviewed-hooks.yaml` — that test was run against an isolated `ShellHookSpec`
object, which never reads or writes `~/.hermes/config.yaml` or the shell-hooks allowlist.
