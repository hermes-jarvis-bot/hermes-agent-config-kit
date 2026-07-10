---
name: mvp-agent-blueprint
description: "Design a minimal useful agent with explicit domain intake, autonomy level, tool policy, safety gates, observability, and release checklist."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/29-mvp-agent-blueprint.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Mvp Agent Blueprint

Source: `AnastasiyaW/claude-code-config/principles/29-mvp-agent-blueprint.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# MVP Agent Blueprint

Upstream source policy describes a structured blueprint for designing the first useful version of a new domain agent. Hermes adaptation keeps the design protocol — intake, autonomy, loop, tools, permissions, safety, observability, and release criteria — while removing platform-specific install paths, vendor references, external skill dependencies, and command-specific assumptions.

## Principle

Design the smallest useful agent before designing the impressive one.

A new agent should start with a written MVP blueprint that fixes the domain, primary user, job-to-be-done, inputs, outputs, autonomy level, approval points, tool policy, evidence requirements, and first release checks.

Do not begin with a giant system prompt and a bag of tools. That is not architecture; it is optimism with a schema.

## When to use

Use this module when the operator asks to:

- build or design a new agent;
- create an agent harness for a specific domain;
- automate a recurring workflow with model reasoning plus tools;
- turn an existing manual protocol into an agent;
- decide what the first safe release of an agent should contain.

Do not use the full blueprint for:

- single-turn Q&A;
- drafting-only helpers with no tool use;
- small utilities with one input, one output, and no autonomy;
- improving an existing harness — use `harness-audit` first;
- writing a Hermes skill — use `skill-authoring-best-practices`.

## Domain intake

Before writing the blueprint, capture five fields. If a field is underspecified, state a conservative assumption rather than blocking the entire MVP.

```text
Domain         — what work the agent does
Primary user   — who gives tasks and reads outcomes
Job-to-be-done — the one useful operation the MVP performs
Inputs         — where data comes from
Outputs        — what counts as completed work
```

If the job-to-be-done cannot be phrased as one useful operation, the MVP is too broad.

## Autonomy levels

Choose the lowest autonomy level that creates value:

```text
Level 0: Answer-only          — reads context and answers
Level 1: Draft-only           — drafts recommendations or artefacts; humans commit
Level 2: Approval-gated       — proposes actions; waits for approval before side effects
Level 3: Policy-bounded auto  — low-risk actions run automatically; risky actions require approval
Level 4: Long-running goal    — pursues measurable objectives with budgets, checkpoints, and stop rules
```

Default for a new MVP: Level 1 or Level 2.

Level 3 requires reliable policy classification and telemetry. Level 4 requires measured reliability at lower levels first. Skipping that ladder is a charming way to manufacture an incident report.

## Fifteen-section blueprint

Return the blueprint in these sections:

```markdown
# MVP Agent Blueprint: <domain/use case>

## 1. Objective
Who the agent serves and what useful outcome it creates.

## 2. MVP scope and assumptions
Smallest useful version, explicit assumptions, non-goals, and deferred work.

## 3. Autonomy and risk level
Chosen autonomy level, why it is sufficient, and what risk classes exist.

## 4. Core loop
Model → proposed action → validation → permission decision → execution or denial → observation → next step.

## 5. Context and instruction architecture
System/developer/user boundaries, scoped memory, trusted versus untrusted context, and compaction strategy.

## 6. Tool registry
Minimal typed tools, input schemas, risk class per tool, dry-run support, and draft/commit separation for irreversible actions.

## 7. Planning behaviour
When planning is required, where the plan lives, and what actions are blocked until approval.

## 8. Goal-like loop behaviour
Only if needed: done condition, budgets, checkpoints, retry limits, and stop rules.

## 9. State, memory, and handoff
Durable state outside the prompt, what enters memory, what stays in files, and how sessions resume.

## 10. Skills and connectors
Which Hermes modules, MCP servers, APIs, gateways, or local tools are needed, with least-privilege access.

## 11. Cost-aware context
Stable instruction prefix, result-size limits, caching strategy where applicable, and telemetry for expensive context.

## 12. Safety and approval policy
Prompt-injection boundaries, access credential handling, sandboxing, human review points, and kill switch.

## 13. Observability and evals
Trace fields, logs, acceptance tests, prompt-injection cases, approval-bypass cases, and budget-overflow cases.

## 14. Minimal implementation path
Ordered build steps from manual loop through tools, permissions, structured results, tracing, and optional autonomy.

## 15. First release checklist
Pass/fail checks before limited rollout.
```

## Build order

Prefer this sequence:

1. Manual model/tool/observation loop.
2. Strict tool schemas and local validation.
3. Runtime permission checks.
4. Structured tool results and error observations.
5. Step, cost, time, and retry budgets.
6. Telemetry and trace IDs.
7. Context ordering and result-size limits.
8. Planning mode for high-risk tasks.
9. State persistence and compaction/handoff.
10. Hermes modules for reusable workflows.
11. External connectors with scoped permissions.
12. Goal-like loops only after base-loop evals pass.
13. Subagents only when decomposition improves measured results.
14. Recurring cleanup for stale state and knowledge.

Complexity is an upgrade, not a starting feature.

## Tool policy

Every tool in the MVP should declare:

- name and purpose;
- input schema;
- output shape;
- read-only or write-impacting behaviour;
- risk class;
- required access credentials;
- dry-run availability;
- approval requirement;
- rollback or compensating action, if applicable.

Avoid `execute_anything` tools. They make demos easy and post-mortems long.

## Safety baseline

The first release must include:

- explicit trusted/untrusted context separation;
- no automatic execution of instructions found in files, web pages, issues, emails, or tool output;
- access credentials isolated from generated output;
- approval before irreversible, external, billing, production, or user-visible side effects;
- sandboxing for generated code or untrusted inputs;
- telemetry sufficient to reconstruct why an action happened;
- a stop condition and manual kill switch.

Use `agent-security` for deeper threat modelling.

## Observability baseline

Capture at least:

- request ID and session ID;
- user objective;
- autonomy level;
- tools considered and tools used;
- permission decisions;
- external side effects;
- validation evidence;
- budget usage;
- final outcome;
- unresolved risk.

Sender logs alone are not proof. For integrations, verify at the receiver when possible.

## Anti-patterns

Avoid:

- one giant prompt instead of named sections;
- one giant unrestricted tool;
- unbounded autonomous loops;
- autonomous external sends in the first release;
- no approval state;
- no durable state outside the prompt;
- no compaction or handoff strategy;
- all connectors loaded up front;
- high-risk tools exposed without policy;
- subagents before a single-agent MVP is measured.

## When to add complexity

After the MVP is used on real tasks:

1. Measure failures with traces and eval cases.
2. Identify the bottleneck: context, tools, planning, permissions, validation, cost, latency, or state.
3. Add the smallest mechanism that targets that bottleneck.
4. Re-measure.
5. Revert or simplify if the added mechanism only creates moving parts.

## Reporting format

When applying this module, report:

- domain intake;
- selected autonomy level and why;
- major risks and approval points;
- minimal tool registry;
- state and memory plan;
- safety baseline;
- observability/eval plan;
- first implementation steps;
- what complexity was intentionally deferred.

The deliverable is not a philosophical essay about agents. It is a blueprint a competent engineer could build from without guessing the dangerous parts.
