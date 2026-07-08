# Security policy

## Trust model

Upstream content from `AnastasiyaW/claude-code-config` is treated as data, not as executable authority.

This adapter may snapshot, classify, and transform selected markdown artefacts into Hermes-compatible skills. It must not automatically execute upstream hooks, scripts, workflows, plugin descriptors, or shell snippets.

## Safety guarantees for the MVP

- No automatic writes to `~/.hermes`.
- No automatic Hermes gateway start or restart.
- No automatic execution of upstream hooks or scripts.
- No automatic installation of upstream plugin metadata.
- No use of production credentials in CI.
- No auto-merge of upstream changes.
- Upstream sync is batched into reviewable changes rather than applied directly to a live agent.

## Quarantine lane

The following upstream artefacts are manual-review only:

- `hooks/**`
- `scripts/**`
- `.claude-plugin/**`
- `.github/workflows/**`
- files that appear to handle credentials, shell execution, deletion, network calls, or process control

Quarantined files may be included in the upstream snapshot for review, but they are not installed into Hermes by the MVP installer.

## Reporting a vulnerability

Open a private report with the maintainer, or contact the operator through the agreed operational channel. Do not include secrets in issue bodies, PR descriptions, logs, or screenshots.

If a credential appears in repository content, rotate it first and then remove it from history. Treat exposure as real until proven otherwise.

## Review checklist for upstream sync PRs

Before merging a sync PR:

- inspect the upstream commit range;
- review the generated report under `reports/upstream-sync/`;
- confirm generated Hermes skills are markdown-only and have valid frontmatter;
- confirm quarantine counts and paths make sense;
- check that no generated skill instructs live profile writes without operator confirmation;
- run `python3 scripts/validate_output.py`;
- run installer dry-run against a temp path;
- do not run `--apply` outside a disposable Hermes home.
