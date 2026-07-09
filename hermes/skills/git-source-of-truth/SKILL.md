---
name: git-source-of-truth
description: "Treat Git and remote push state as durable project truth; commit and push deployed or meaningful changes with verification evidence."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/git-source-of-truth.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Git Source Of Truth

Source: `AnastasiyaW/claude-code-config/rules/git-source-of-truth.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Git Source of Truth

Upstream source policy states that Git must be the durable source of truth for project work. Hermes adaptation keeps that operational invariant while removing project-specific anecdotes and harness-specific references.

## Principle

If a project can be held in Git, Git is the durable source of truth for its code, documentation, configuration templates, and project decisions.

Local folders, conversation context, unstaged edits, deployment directories, and memory summaries are not durable proof of project state. They are useful telemetry, not the record.

## Required protocol

Before work:

1. Inspect the repository state:
   - `git status --short --branch`
   - `git log -1 --oneline --decorate`
   - `git remote -v` when remote state matters.
2. Identify whether the task is read-only, local-editing, deployment-impacting, or release-impacting.
3. If the repo has uncommitted work, classify it before editing:
   - current task work;
   - unrelated operator work;
   - generated noise;
   - secrets or local machine state that must not be committed.

During work:

- Stage explicit paths, not blind `git add -A`, unless the repository has been inspected and the scope is intentionally all changes.
- Keep commits small and meaningful.
- Do not mix unrelated clean-up with functional changes unless the operator asked for that clean-up.
- If a change is deployed, published, or otherwise made externally visible, commit and push the exact source state promptly.

After work:

1. Run the relevant verification.
2. Commit the verified artefacts with a descriptive message.
3. Push when remote durability or CI is part of the workflow.
4. Read back the result:
   - `git status --short --branch` for local cleanliness and tracking state;
   - `git rev-parse HEAD` for the exact commit;
   - CI/check-run status for GitHub-hosted workflows;
   - release/deployment URL or version when applicable.

## What belongs in Git

Commit project truth:

- source code;
- documentation and architecture notes;
- tests and fixtures safe for publication;
- build, CI, and deployment configuration;
- templates such as `.env.example` without secrets;
- generated artefacts only when the project deliberately tracks them;
- handoffs, changelogs, release notes, and backlog updates that define project state.

## What does not belong in Git

Keep these out unless the operator explicitly approves a special storage pattern:

- access credentials, tokens, private keys, real `.env` files;
- regenerable dependency directories and build caches;
- machine-local noise;
- large binary artefacts better stored in object storage or a release system;
- private operational dumps or logs containing sensitive data.

`.gitignore` should document the boundary. It is not a bin for inconvenient project truth.

## Deployment invariant

Deployed-but-uncommitted is a fault. It means production, staging, or an external consumer may now depend on code that future sessions cannot reconstruct from Git.

If a deployment happened before the repository was committed:

1. stop further changes;
2. inspect current deployed/source state;
3. commit the source state that matches the deployment;
4. push and read back the remote commit/CI status;
5. report any uncertainty explicitly.

## Reporting format

When closing Git-backed work, report:

- changed paths;
- verification command and result;
- commit SHA;
- push/remote status;
- CI/check-run URL when available;
- remaining uncommitted changes, if any, with explanation.

If Git state is dirty at handoff, say so plainly. A charming summary is not a substitute for `git status`.
