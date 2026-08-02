---
name: verify-git-currency-first
description: "Establish current remote, local, and deployed Git state before diagnosing, editing, synchronising, deploying, or copying project trees."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/verify-git-currency-first.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Verify Git Currency First

Source: `AnastasiyaW/claude-code-config/rules/verify-git-currency-first.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Verify Git Currency First

Use this module before diagnosing, editing, synchronising, deploying, or bulk-copying
a Git-backed project. It specialises `no-guessing`: current Git and deployment
evidence outrank local assumptions and session memory. This is read-only guidance;
it does not fetch, stash, reset, pull, deploy, or modify a repository.

## Read-only preflight

1. Inspect the local checkout: `git status --short --branch`, `git log -1 --oneline
   --decorate`, and the configured remote when remote state matters.
2. Establish remote currency with an approved read-only query such as `git fetch
   --all --prune` only when that network update is within the current protocol, then
   inspect `git rev-list --left-right --count HEAD...origin/<main-line>`.
3. If the work concerns a deployed service, identify the commit actually running by
   using approved, read-only deployment telemetry. Compare it with the verified
   remote main line; do not assume the checkout is deployed.
4. Record branch, exact local and remote commits, ahead/behind state, deployed commit
   when applicable, and any unavailable evidence. Treat absent access or telemetry as
   a blocker, not as proof that the local tree is current.

## Decision boundary

- Local behind remote: stop before editing, deployment, or bulk copy. Review newer
  commits for an existing resolution. Synchronisation or preservation of local work is
  a separate write-impacting protocol requiring operator confirmation.
- Deployed state behind remote: treat this as a deployment gap, not a reason to rewrite
  code. Report the exact commit difference and the responsible deployment path.
- Dirty tree: classify changes before any action. Never overwrite or hide unrelated
  operator work.
- Diverged histories, unknown main line, or conflicting deployment evidence: report the
  ambiguity with the observed refs and request the missing authority or access.

## Bulk-copy and release safeguard

Before a tool copies one tree over another, confirm the local tree is not behind and
review its dry-run output. A large unexpected deletion, remote mismatch, or unknown
target is a stop condition. Before publication or deployment, verify the exact commit,
the intended target, and the relevant approval boundary.

## Output

Report local, remote, and deployed commit evidence; branch and ahead/behind state;
dirty-tree classification; the decision (proceed or block); and the next required
operator-confirmation point. Use `git-source-of-truth` for durable commit/push and
release evidence, and `no-guessing` for missing configuration or access.
