# Hermes Agent Config Kit

Adapter repository for selectively porting proven Claude/Codex agent-harness patterns from [`AnastasiyaW/claude-code-config`](https://github.com/AnastasiyaW/claude-code-config) into Hermes Agent-compatible skills, templates, and future plugin modules.

This repository is intentionally **not** a fork. It is a controlled adapter:

- tracks upstream by commit range;
- batches upstream changes into review PRs;
- converts only supported low-risk artefacts automatically;
- quarantines hooks/scripts/plugin descriptors for manual review;
- never installs into a live Hermes profile by default.

## Current MVP scope

Supported in the first adapter stage:

- selected markdown skills/principles/rules/templates;
- Hermes `SKILL.md` generation;
- upstream snapshot and lockfile tracking;
- batch upstream-watch GitHub workflow;
- dry-run-only installer by default;
- CI validation against temporary directories only.

Explicitly deferred:

- live Hermes installation;
- automatic hook/plugin execution;
- conversion of Claude Code hook APIs into Hermes plugins;
- auto-merge of upstream changes.

## Safety model

The adapter treats upstream content as data, not as executable authority.

- Upstream is pinned by commit SHA in `upstream.lock.json`.
- Sync PRs show the full commit range and changed-file classification.
- Hooks, scripts, workflows, and plugin metadata are manual-review only.
- `scripts/install_hermes.py` defaults to `--dry-run` and requires `--apply` to write.
- CI uses a temporary `HERMES_HOME`; it does not write to `~/.hermes`.

See also:

- `SECURITY.md` for the trust model and quarantine policy.
- `INSTALL.md` for the disposable-VM clean-room test protocol.

## Repository layout

```text
upstream.lock.json                         # source-of-truth upstream checkpoint
upstream/claude-code-config/snapshot/      # current upstream snapshot
mappings/compatibility.yaml                # source -> target conversion policy
hermes/skills/                             # generated/adapted Hermes skills
hermes/templates/                          # adapted templates
reports/upstream-sync/                     # generated upstream sync reports
scripts/                                   # sync, conversion, validation, installer routines
.github/workflows/                         # upstream watch and validation workflows
```

## Local usage

Inspect upstream without touching Hermes:

```bash
python3 scripts/sync_upstream.py --check
```

Synchronise the local snapshot and generate adapted artefacts:

```bash
python3 scripts/sync_upstream.py --sync
python3 scripts/validate_output.py
```

Preview installation into a temporary Hermes home:

```bash
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-home
```

Real installation is intentionally explicit:

```bash
python3 scripts/install_hermes.py --apply --hermes-home ~/.hermes
```

Do not run real installation on production profiles without operator confirmation.

## Upstream batching protocol

The upstream watcher compares:

```text
upstream.lock.json:last_synced_sha .. AnastasiyaW/claude-code-config:main
```

If changes exist, it updates the adapter branch and opens or updates one PR. Multiple upstream commits are batched into a single review unit. Existing open sync PRs are updated rather than duplicated.

Large or risky batches are marked draft/manual-review by report content.
