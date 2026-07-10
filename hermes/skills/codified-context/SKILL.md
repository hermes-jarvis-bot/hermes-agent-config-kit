---
name: codified-context
description: "Treat agent context as operational infrastructure: concise project guidance, just-in-time loading, durable state, compaction policy, and isolation."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/07-codified-context.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Codified Context

Source: `AnastasiyaW/claude-code-config/principles/07-codified-context.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Codified Context

Upstream source policy describes context as infrastructure rather than ordinary documentation. Hermes adaptation keeps the useful pattern — concise project guidance, just-in-time retrieval, durable state, compaction policy, and isolation — while removing platform-specific file names, vendor references, research-number claims, and automatic rule-injection assumptions.

## Principle

Treat context as operational infrastructure.

Project guidance, memory, plans, decisions, and task state are not decorative notes. They shape what an agent sees, what it can safely infer, and what survives context reset. Poor context is a configuration fault: it increases cost, dilutes important facts, and encourages confident repetition of stale assumptions.

## What belongs in always-loaded guidance

Always-loaded project guidance, such as `AGENTS.md`, should contain only facts that affect most tasks and are difficult to infer by reading nearby files:

- safety boundaries and approval requirements;
- non-obvious build, test, install, or deployment commands;
- repository-specific generated-output contracts;
- live versus disposable environment boundaries;
- known operational gotchas from real failures;
- canonical source-of-truth files for project state.

Do not fill always-loaded guidance with history, generic framework facts, task logs, or material the agent can discover cheaply from manifests and neighbouring code.

## Context file roles

Use different artefacts for different jobs:

| Artefact | Role | Good content | Avoid |
| --- | --- | --- | --- |
| `AGENTS.md` or project guidance | Runtime operating contract | safety rules, repo conventions, verification commands | broad tutorials, stale narratives |
| Backlog or issue tracker | Planned work and deferred scope | candidate lists, blockers, next owner/action | private mental notes, vague wishes |
| Plan or task file | Current work state | done/remaining items, exact paths, acceptance checks | raw transcripts, speculation |
| Decision log | Cached reasoning | chosen option, rejected alternatives, evidence | re-litigating settled questions |
| Memory/archive | Cross-session facts | stable operator preferences and environment facts | secrets, transient command output |

If one file tries to do all of these jobs, it becomes either too large to load or too vague to trust.

## Just-in-time context loading

Load context in layers:

1. Start with the operator objective, project guidance, and the smallest relevant file set.
2. Search for symbols, manifests, tests, docs, or generated artefacts only when the next step requires them.
3. Write durable conclusions to project state when they must survive compaction or handoff.
4. Drop or summarise obsolete exploration rather than carrying it forward.
5. Re-read source-of-truth files after long pauses, syncs, branch changes, or context compression.

The aim is not minimal context for its own sake. The aim is high-signal context: enough to act correctly, not enough to drown the task.

## State over transcript

For multi-step work, preserve conclusions in durable state instead of relying on conversation history:

```text
objective       — what outcome is being pursued
current state   — what has actually changed, with paths and commits
evidence        — commands run, outputs observed, URLs read back
blockers        — exact missing data, access, or failing command
next step       — one concrete action, not a menu of guesses
```

Use `session-handoff` for transfer between sessions, `documentation-integrity` for checking documented claims, and `git-source-of-truth` when state belongs in commits.

## Compaction policy

Before a long session is likely to compact or hand off, decide what survives:

- keep: objective, constraints, decisions, changed paths, verification evidence, unresolved blockers, exact next step;
- discard or compress: raw file dumps, failed exploratory paths after their conclusion is recorded, verbose logs, duplicate explanations;
- re-read later: source files, manifests, generated artefacts, CI state, release metadata.

If a fact is important but stale-prone, store a pointer and verification command rather than trusting the old value forever.

## Context isolation

Different tasks and subagents should receive only the context they need:

- research workers can be read-only and receive scope plus source pointers;
- implementers need exact contracts, paths, and constraints, not the full research transcript;
- reviewers need the diff, acceptance criteria, and verification evidence, not the author's private reasoning;
- risky or untrusted work should run in disposable workspaces or containers where practical.

Do not delegate understanding. A coordinator must synthesize findings into a self-contained prompt or task record before assigning work.

## Quality checks for context

Review context artefacts with the same scepticism as configuration:

- Does each always-loaded line affect many tasks?
- Is the fact non-inferable or expensive to rediscover?
- Is the command/path still valid?
- Is task state separated from durable policy?
- Are stale facts dated or linked to a verification command?
- Are secrets and access credentials excluded?
- Can a fresh session continue from the preserved state without guessing?

## Hermes adapter use

For this kit, apply codified context when updating:

- `AGENTS.md` generated module lists and operating boundaries;
- `PORTING_BACKLOG.md` counts, candidates, and handoff guidance;
- generated skills and source attribution;
- release notes and verification summaries;
- temporary ad-hoc verifier evidence.

Keep generated module guidance concise and positive. Do not carry upstream harness mechanics into generated output unless they have been deliberately translated into Hermes-native policy.

## Avoid

- Treating project guidance as a wiki for everything ever learned.
- Letting generated or stale context outrank live files, Git, CI, or release telemetry.
- Copying task transcripts into durable state when a short conclusion would do.
- Putting access credentials, private dumps, or provider auth state into context artefacts.
- Asking workers to infer missing decisions from another session's conversation.
- Loading entire repositories when a symbol trace or manifest read would answer the question.

## Reporting format

When using this module, report:

- context artefacts consulted;
- facts accepted as current and how they were verified;
- stale or noisy context removed or ignored;
- durable state updated;
- compaction or handoff policy applied;
- remaining context gaps.

Good context is quiet infrastructure: unglamorous, load-bearing, and missed only when it fails.
