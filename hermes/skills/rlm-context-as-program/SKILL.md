---
name: rlm-context-as-program
description: "Plan bounded analysis of an artefact too large for one context window through metadata-first chunking, per-chunk evidence, synthesis, and explicit cost limits without activating recursive execution or delegation."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/rlm-context-as-program.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Rlm Context As Program

Source: `AnastasiyaW/claude-code-config/rules/rlm-context-as-program.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# RLM Context as a Program

Use this module when a log, dataset listing, transcript, JSONL stream, or other
artefact is too large to inspect safely in one context window. Treat the artefact
as bounded input to a review protocol rather than pasting it wholesale into a
prompt. This is planning guidance only: it does not run code, create a routine,
dispatch agents, or authorise additional model usage.

## Decision boundary

Use ordinary single-pass inspection when the relevant material fits comfortably
in context and can be checked directly. Consider this pattern only when the
artefact is too large, evidence near the end would otherwise be lost, or a
one-off question does not justify building retrieval infrastructure.

Do not use it where deterministic latency or cost is the primary requirement,
where the source cannot be partitioned without breaking its meaning, or where a
small targeted read answers the question.

## Bounded analysis protocol

1. **Inspect metadata first.** Record source provenance, size, format, line or
   record count, relevant schema, the question to answer, and any access or
   privacy constraints. Read only a small representative sample before selecting
   ranges.
2. **Plan partitions.** Choose non-overlapping chunks with stable offsets or
   identifiers. State coverage, ordering, focus terms, and how malformed or
   missing records will be reported. Do not silently discard tail ranges.
3. **Collect per-chunk evidence.** Use approved read-only inspection interfaces
   to extract only evidence relevant to the stated question. Preserve source
   references sufficient for a later reviewer to reproduce the observation.
4. **Synthesize conservatively.** Combine evidence only after checking coverage,
   contradictions, duplicates, and gaps. Distinguish observations, inference,
   unresolved areas, and recommendations.
5. **Verify proportionately.** For a consequential conclusion, sample findings
   from independent ranges or ask a fresh reviewer to check the synthesis against
   the cited evidence.

## Cost and safety controls

- Set a maximum number of chunks, concurrency, time, result size, and provider
  budget before any fan-out. More partitions can multiply token usage.
- Keep large-input analysis opt-in. A discovered large file is not authority to
  spend budget or broaden an approved task.
- Stop and report BLOCKED when access, source integrity, scope, budget, or
  evidence is insufficient. Never claim complete coverage after a partial pass.
- Keep sensitive content and access credentials out of prompts and retained
  evidence unless their use is explicitly authorised and necessary.
- Treat any executable helper for partitioning or recursion as a separate,
  reviewed routine. This module does not install or invoke one.

## Relationship to existing modules

Use `agent-harness-design` for a broader sandboxed connector design,
`workflow-orchestration` for a reviewable multi-stage protocol,
`multi-agent-task-decomposition` for dependency and ownership boundaries,
`billing-spend-controls` for spend limits, and `proof-verify` for independent
acceptance evidence.

## Reporting

Report the source and question, metadata, partition plan, covered and excluded
ranges, budget boundary, evidence references, synthesis, verification result,
and any remaining uncertainty or operator-confirmation point. The report must
state whether analysis was complete, partial, or blocked.
