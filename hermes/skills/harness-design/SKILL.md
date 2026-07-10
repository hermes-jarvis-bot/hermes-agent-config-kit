---
name: harness-design
description: "Improve agent harnesses with generator/evaluator separation, frozen sprint contracts, stagnation signals, context resets, and measured complexity."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/01-harness-design.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Harness Design

Source: `AnastasiyaW/claude-code-config/principles/01-harness-design.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Harness Design

Upstream source policy describes how to improve an existing agent harness once a simple agent or MVP already works. Hermes adaptation keeps the durable architecture pattern — independent generation and evaluation, explicit success contracts, context reset discipline, stagnation detection, and measured complexity — while removing vendor anecdotes, paper-specific formulas, and fixed multi-agent machinery.

## Principle

Separate creation from judgment when quality matters.

A harness is the orchestration around an agent: instructions, state, tools, verification, context management, and lifecycle controls. Its job is not to make every task multi-agent. Its job is to add the smallest structure that measurably improves outcomes.

Use `mvp-agent-blueprint` when designing a brand-new agent. Use this module when the first agent exists and needs a better work/evaluation loop.

## Generator/evaluator split

For work where quality is hard to self-certify, separate roles:

- **Generator** — creates the candidate output: code, prose, plan, design, analysis, or configuration.
- **Evaluator** — judges the candidate against explicit criteria from an independent context.

The evaluator should have:

- independent context, not the generator's reasoning transcript;
- independent instructions, not a paraphrase of the generator prompt;
- calibrated skepticism focused on known failure modes;
- a concrete rubric rather than `is this good?`;
- permission to reject plausible-looking work.

Self-review is useful as a quick pass. It is not independent verification.

## Sprint contract

Before generation starts, define what success means.

A sprint contract should be:

- specific;
- testable or reviewable;
- frozen during the attempt;
- visible to both generator and evaluator;
- small enough to complete in one focused cycle.

Bad:

```text
Build a dashboard.
```

Better:

```text
Dashboard loads within the agreed budget, shows the required metrics, handles empty state, exposes failure telemetry, and passes the named accessibility checks.
```

If the target changes mid-cycle, stop and write a new contract. Do not quietly mutate the finish line.

## Evaluation calibration

Calibrate the evaluator with examples or explicit criteria:

- what good output looks like;
- what bad output looks like;
- what superficially good but flawed output looks like;
- which faults are blockers;
- which faults are polish;
- what evidence is required for a pass.

For subjective work, use dimensions such as coherence, originality, craft, functionality, and operator fit. For testable work, prefer `proof-loop` and durable evidence.

## Stagnation signals

Do not retry the same generator/evaluator loop forever.

Escalate when repeated attempts produce the same failure shape:

- identical test failures;
- equivalent runtime traces;
- repeated review objections;
- no meaningful diff in approach;
- growing cost without new evidence.

Escalation options, cheapest first:

1. Give the generator the concrete failure evidence and ask for one targeted correction.
2. Reset context and retry from the sprint contract plus evidence only.
3. Ask for independent alternative approaches.
4. Split the problem or reduce the contract.
5. Stop and report the blocker.

More agents are not an apology for unclear acceptance criteria.

## Context management

For long-running harness work, prefer structured reset over blind compaction.

Carry state through durable artefacts:

```text
PLAN.md      — current plan, completed items, next step
STATE.json   — machine-readable counters, IDs, flags, budgets
FINDINGS.md  — decisions, gotchas, rejected paths, evidence links
```

Context compaction preserves continuity but can preserve stale assumptions. A reset plus handoff gives the next agent less emotional baggage, which is more than can be said for many meetings.

## Context anxiety

Large contexts cause agents to wrap up early, skip checks, and declare completion before evidence exists.

Mitigations:

- break work into smaller contracts;
- store state outside the prompt;
- require verification artefacts;
- avoid making the model track counters mentally;
- hand off before the context window becomes operationally cramped.

## Assumption testing

Every harness component encodes an assumption:

```text
The model cannot do X reliably without this support.
```

Assumptions expire as models, tools, and project structure change. Periodically test whether the component still earns its cost:

1. Identify the assumption.
2. Run the same task with and without the component.
3. Compare quality, cost, latency, and risk.
4. Keep, simplify, or remove the component based on evidence.

Do not preserve harness machinery as a monument to last quarter's model limitations.

## Cost and quality decision

Use a richer harness when:

- solo execution repeatedly fails or regresses;
- output quality is subjective and high-stakes;
- verification requires independent judgment;
- the task spans multiple files, systems, or sessions;
- mistakes have real operational, security, billing, or user-visible cost.

Prefer a solo or lightly structured agent when:

- the task is routine;
- acceptance criteria are simple;
- tests provide clear feedback;
- added roles would mostly create coordination overhead;
- the operator needs speed more than polish.

The correct harness is the cheapest one that reliably meets the contract.

## Relationship to other modules

- Use `mvp-agent-blueprint` before the first implementation exists.
- Use `harness-audit` to score an existing project harness and choose improvements.
- Use `proof-loop` for testable outcomes requiring durable evidence.
- Use `deterministic-orchestration` for mechanical checks and stateful routines.
- Use `multi-session-coordination` and `inter-agent-communication` when parallel sessions need explicit coordination.
- Use `agent-security` whenever tools, external data, access credentials, or autonomy are involved.

## Review checklist

Before adding harness complexity, verify:

- [ ] The current failure is real and evidenced.
- [ ] The sprint contract is explicit and stable.
- [ ] The evaluator has independent context and criteria.
- [ ] Mechanical checks run outside the reasoning loop where possible.
- [ ] State survives context reset.
- [ ] Escalation has a stop rule.
- [ ] The added component has a measurable success signal.
- [ ] There is a plan to retire the component if it stops paying rent.

## Reporting format

When using this module, report:

- current harness problem;
- sprint contract;
- generator/evaluator roles;
- evaluator rubric;
- evidence and stagnation signals;
- context/state artefacts;
- complexity added;
- complexity intentionally avoided;
- next measurement.

A harness should make the agent system more reliable, not merely more ornate.
