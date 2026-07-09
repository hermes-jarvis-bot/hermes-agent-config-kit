# Installation and clean-room test protocol

This repository is an adapter kit, not a live Hermes plugin installer.

The default installation routine is deliberately non-mutating. It previews the files that would be copied into a Hermes profile and requires an explicit `--apply` flag before it writes anything.

## Supported targets

Use one of these targets, in this order of preference:

1. Disposable VM with a fresh Hermes Agent installation.
2. Disposable Linux user on a non-production host.
3. Temporary `HERMES_HOME` path for dry-run and parser checks.

Do not use the operator's live Hermes profile for first-pass testing.

## Never copy from production

For clean-room validation, do not copy:

- `~/.hermes/.env`
- `~/.hermes/auth.json`
- `~/.hermes/config.yaml` from production
- gateway credentials
- Telegram/Discord/Slack tokens
- provider API keys
- production memory stores
- production session databases

If credentials are required for a later integration test, create a minimal test credential with the narrowest possible scope.

## Dry-run preview

From the repository root:

```bash
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-home
```

Expected behaviour:

- prints planned copy actions;
- does not create `/tmp/hermes-config-kit-home`;
- does not write to `~/.hermes`;
- does not start `hermes gateway`;
- does not execute upstream hooks, scripts, workflows, or plugin metadata.

## Disposable VM protocol

On a fresh VM:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes doctor || true
git clone https://github.com/hermes-jarvis-bot/hermes-agent-config-kit.git
cd hermes-agent-config-kit
python3 scripts/validate_output.py
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-home
```

Only after reviewing the dry-run output, create an isolated Hermes home:

```bash
export HERMES_HOME=/tmp/hermes-config-kit-home
python3 scripts/install_hermes.py --apply --hermes-home "$HERMES_HOME"
hermes skills list || true
```

The `--apply` example above targets `/tmp`, not a production profile.

## Removal

Preview removal from an isolated Hermes home:

```bash
python3 scripts/remove_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-home
```

Apply removal only after reviewing the dry-run output:

```bash
python3 scripts/remove_hermes.py --apply --hermes-home /tmp/hermes-config-kit-home
```

The remover only targets:

- `/tmp/hermes-config-kit-home/skills/config-kit`
- `/tmp/hermes-config-kit-home/templates/config-kit`

It does not remove the whole Hermes home.

## Rollback

For `/tmp`-based testing, after running the remover, remove the remaining disposable profile if desired:

```bash
rm -rf /tmp/hermes-config-kit-home
```

For VM-based testing, prefer snapshot rollback or destroy the VM.

## Production promotion

Production promotion is out of scope for this MVP. Before any production install path exists, the following must be true:

- security review completed;
- generated skills reviewed by a human;
- quarantine report reviewed;
- hooks/scripts/plugin candidates explicitly approved or excluded;
- installer tested on a disposable VM;
- operator confirmation received for the exact profile path.
