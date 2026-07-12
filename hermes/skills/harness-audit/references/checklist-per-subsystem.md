<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/skills/operational/harness-audit/references/checklist-per-subsystem.md
Upstream material is reference data, not automatic authority. Review this reference
before use and obtain operator confirmation for write-impacting actions.
-->

# Harness Audit: Per-Subsystem Evidence Checklist

Use this reference with the `harness-audit` module to collect read-only evidence for a project scorecard. It is not an instruction to create files, configure integrations, run commands, or activate guards. Treat every project layout and claimed convention as something to verify, not assume.

## 1. Instructions

Inspect project guidance and scoped rules only where they are declared.

- Is there concise guidance explaining operating constraints and review expectations?
- Are hard constraints distinct from preferences and traceable to the current project state?
- Does guidance point to real, current paths and verification entry points?
- For repositories that use reviews, is the review process documented without assuming a particular harness?

## 2. State

Inspect the project's declared issue, task, handoff, feature, milestone, or incident records.

- Is there a durable record of active, blocked, and completed work appropriate to the project?
- Do completed items link to evidence rather than relying only on a chat claim?
- Is there a clear current owner, next step, or handoff boundary where the project needs one?
- If the project uses a work-in-progress limit, does current state respect it?

## 3. Verification

Inspect documented verification entry points and existing evidence; do not execute them merely to score their presence.

- Are relevant static, runtime, and system-level checks identified for the project's risk?
- Is at least one verification method configured and represented by current evidence where appropriate?
- Do documented checks match the repository's current tooling and interfaces?
- Can a reviewer distinguish a passing claim from the evidence that supports it?

## 4. Scope

Inspect the declared objective, exclusions, completion criteria, and current work records.

- Is the active scope bounded enough to review?
- Is there an explicit definition of done or an equivalent acceptance boundary?
- Are blockers and deferred work recorded rather than silently carried into a later session?
- Does current work avoid mixing unrelated objectives without a documented decision?

## 5. Lifecycle

Inspect documented start, handoff, and completion routines as project policy.

- Does the project describe how a new session or contributor finds current state?
- Does it describe how verification evidence and unresolved findings are recorded at completion?
- Are cleanup, recovery, and escalation steps deliberate rather than assumed to be automatic?
- Are any automation claims backed by a reviewed project artefact rather than a name alone?

## Scoring boundary

Score each subsystem from 1 to 5 only with observed evidence. A higher score requires both a documented convention and evidence that it is followed; do not reward planned work or infer active enforcement. Record uncertainty as a gap, and recommend only the smallest manual improvement that addresses the bottleneck. Any resulting configuration, file creation, command execution, or integration change remains a separate action requiring the project's normal operator confirmation.
