---
name: harness-audit
description: "Score an agent-harness project across instructions, state, verification, scope, and lifecycle, then recommend improvements."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/operational/harness-audit/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Harness Audit

Source: `AnastasiyaW/claude-code-config/skills/operational/harness-audit/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Harness Audit

Use this module for a read-only scorecard of a project's agent-working conventions. It identifies the most constraining gap across instructions, state, verification, scope, and lifecycle. It does not create files, install automation, or enable runtime behaviour.

## Read-only audit protocol

1. Identify the project's adopted guidance, task state, verification, and handoff locations; do not assume a directory layout.
2. Inspect only declared project artefacts and representative verification entry points. Do not run commands merely to score their existence.
3. Score each subsystem from 1 to 5 with concrete evidence for strengths and gaps.
4. Select the lowest-scoring subsystem as the bottleneck; break ties by the improvement that unblocks another subsystem.
5. Recommend at most three independent manual next steps, pointing only to templates or references already reviewed and adopted by the project.

If a recommendation would create files, change configuration, enable an integration, or run commands, identify it as a separate write-impacting action requiring the normal operator confirmation.

| Subsystem | Evidence to inspect |
| --- | --- |
| Instructions | Project guidance, scoped rules, review expectations |
| State | Issue/task record, handoffs, feature or milestone state |
| Verification | Documented checks, test entry points, acceptance evidence |
| Scope | Explicit exclusions, WIP limits, definition of done |
| Lifecycle | Deliberate start/finish routines and manual cleanup conventions |

## Output

```text
=== Harness Audit: <project-name> ===
Instructions  <n>/5  <evidence>
State         <n>/5  <evidence>
Verification  <n>/5  <evidence>
Scope         <n>/5  <evidence>
Lifecycle     <n>/5  <evidence>

Bottleneck: <subsystem> (<n>/5)
1. <smallest manual improvement> — <effort and expected effect>
2. <independent improvement> — <effort and expected effect>
3. <independent improvement> — <effort and expected effect>
```

Keep the result concise and distinguish observed facts from recommendations. The score is a planning aid, not a claim of numerical precision.
