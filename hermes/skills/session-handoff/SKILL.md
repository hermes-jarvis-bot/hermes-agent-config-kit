---
name: session-handoff
description: "Create concise, durable handoffs that preserve goal, state, blockers, verification evidence, and the exact next step across sessions."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/session-handoff.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Session Handoff

Source: `AnastasiyaW/claude-code-config/rules/session-handoff.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Session Handoff

Upstream source policy was written for a different harness. Hermes adaptation keeps the operational pattern and removes harness-specific storage assumptions.

## When to create a handoff

Create a concise handoff when:

- the operator asks to prepare a handoff, save context, or continue in a new session;
- the task is long-running and context compaction is likely;
- a blocker prevents immediate completion but future continuation is expected;
- control is transferring from one agent/session/environment to another.

Do not use a handoff to avoid finishing work that can still be completed safely in the current session.

## What to preserve

A valid handoff records enough state for a fresh agent to continue without guessing:

- objective and why it matters;
- repository, branch, commit, working directory, and relevant remote URLs;
- files changed or created;
- verification actually run, including command names and real outcomes;
- blockers and exact error messages;
- key decisions and safety constraints;
- current artefact state, including CI/check URLs where available;
- one concrete next action, not a vague list.

## What not to preserve

Do not include:

- access credential values, tokens, private keys, `.env` bodies, or provider auth files;
- raw tool-call transcripts when a concise result is enough;
- stale task progress that belongs in git, issues, backlog, or session history;
- speculative claims not backed by files, commands, or operator decisions.

## Storage guidance for Hermes work

Prefer durable project documents when the handoff is project state:

- `AGENTS.md` for agent operating instructions;
- `PORTING_BACKLOG.md` for migration scope, omitted artefacts, and next waves;
- `INSTALL.md` and `SECURITY.md` for install and safety protocols;
- GitHub issues, PRs, or release notes for remote project state.

Use chat/session summaries for temporary continuation context. If writing a handoff file inside a project, keep it append-only or uniquely named to avoid overwriting another session's state.

## Handoff format

Use this compact structure:

```markdown
# Session Handoff - YYYY-MM-DD HH:MM

## Objective
[What we were trying to accomplish and why.]

## Completed
- [Concrete result, file path, commit, URL, or command outcome.]

## Current State
- Repo/branch/commit:
- Working tree:
- Verification:
- CI / external state:

## Blockers / What Did Not Work
- [Exact blocker or `NONE`.]

## Key Decisions
- [Decision] — [reason/evidence].

## Safety Constraints
- [Credentials, production boundaries, approval requirements, quarantine notes.]

## Next Step
[One concrete action to start with.]
```

## Resume protocol

When resuming from a handoff:

1. Treat it as context, not as live truth.
2. Inspect the current source of truth first: files, git state, CI, running services, or external systems.
3. Reconcile any drift before acting.
4. Ask the operator if the handoff conflicts with the latest user request.

The latest operator message wins over stale handoff content.
