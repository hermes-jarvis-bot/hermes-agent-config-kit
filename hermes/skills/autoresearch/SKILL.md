---
name: autoresearch
description: "Run cautious score-driven optimisation loops for single artefacts with mechanical evaluation, guard metrics, git-backed experiment logs, and stop rules."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/03-autoresearch.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Autoresearch

Source: `AnastasiyaW/claude-code-config/principles/03-autoresearch.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Autoresearch

Upstream source policy describes iterative optimisation for artefacts with measurable outcomes. Hermes adaptation keeps the useful protocol — one mutation, mechanical score, guard checks, git-backed experiment log, plateau detection, and stop rules — while removing paper-specific benchmark claims, vendor plugin assumptions, infrastructure prescriptions, cost anecdotes, and broad self-improvement promises.

## Principle

Optimise only what you can measure mechanically.

Autoresearch is a cautious experiment loop for improving one artefact against a numerical score. It is not a licence to run unbounded self-modification, rewrite several files at once, or let a model invent its own success criteria.

The safe loop is simple:

```text
read baseline -> change one thing -> run evaluation -> compare score + guard -> keep or revert -> record result
```

## Applicability gate

Use this module only when all conditions hold:

1. **Numerical scoring** — the target has a score expressed as a number, percentage, count, latency, size, error rate, coverage, pass rate, or similar metric.
2. **Automated evaluation** — the evaluation can run without human judgment and returns deterministic, reproducible output.
3. **Single target artefact** — each iteration changes exactly one file or one tightly bounded parameter.
4. **Guard metric** — there is at least one check that catches collateral damage.
5. **Rollback path** — failed experiments can be reverted cleanly.

If any condition is missing, do not run autoresearch. Use `harness-design`, `proof-loop`, or ordinary manual tuning instead.

## Good fits

Autoresearch can be appropriate for:

- prompt or skill tuning against a fixed eval set;
- configuration tuning with measurable latency, accuracy, or error rate;
- code optimisation against tests plus performance metrics;
- template changes where examples can be scored mechanically;
- benchmarkable extraction, classification, or routing tasks.

It is a poor fit for:

- visual taste, prose voice, UX polish, or other subjective criteria;
- contested scoring rubrics;
- one-off tasks;
- tiny search spaces where manual inspection is faster;
- systems already at metric saturation;
- high-risk production behaviour without sandboxing and operator confirmation.

## Scoring design

Prefer 3-6 binary assertions plus one headline score.

Too few assertions create loopholes. Too many encourage checklist gaming. The target is a compact score that represents the real goal without becoming a toy objective.

Example:

```text
score = passed_assertions / total_assertions

guards:
- existing baseline tests pass
- no new forbidden strings
- latency does not exceed threshold
- generated output remains valid
```

Do not ask an LLM to rate output on a 1-10 scale and call that measurement. That is an opinion wearing a number costume.

## Iteration protocol

For each iteration:

1. Record the baseline score and guard status.
2. Choose exactly one mutation.
3. Apply the mutation in an isolated branch or disposable workspace when possible.
4. Run the evaluation command exactly as documented.
5. Run guard checks.
6. Compare baseline versus candidate.
7. Keep the mutation only if the primary score improves and guards pass.
8. Revert otherwise.
9. Record the experiment result.

Use deterministic scripts for evaluation and comparison. The model may propose the mutation; it should not mentally execute the benchmark.

## Git-backed experiment log

Record experiments in git or an equivalent durable log:

```text
experiment: shorten retrieval prompt (score 0.62 -> 0.69) [kept]
experiment: add negative examples (score 0.69 -> 0.66) [reverted]
experiment: lower threshold to 0.35 (score 0.69 -> 0.72, guard pass) [kept]
```

For repository work, prefer one experiment per commit on a temporary branch. Squash or summarise only after the useful result is understood. Failed experiments should remain discoverable in notes, branch history, or a results table.

## Guard checks

Every run needs both:

- **verify** — did the target score improve?
- **guard** — did anything important break?

Examples of guard checks:

- existing test suite still passes;
- output schema still validates;
- safety strings or secrets did not appear;
- latency, cost, or bundle size stayed within budget;
- baseline examples did not regress;
- install/remove or dry-run behaviour still works.

An improvement that breaks a guard is a failed experiment.

## Stop rules

Stop rather than grind when:

- three consecutive iterations produce no improvement;
- the same failure shape repeats;
- guard failures dominate improvements;
- the score is already near the expected ceiling;
- the metric stops representing the real objective;
- the experiment budget is exhausted;
- the next mutation would require broader architectural changes.

When stopped, report the best result, failed directions, remaining hypothesis, and whether the bottleneck is metric quality, search space, model capability, or evaluation cost.

## Optional upgrade path

Only after the simple loop proves useful:

1. **Linear loop** — one branch, keep or revert.
2. **Branching search** — explore multiple mutation families in separate branches.
3. **Strategy review** — periodically analyse which mutation types improved scores.
4. **Cross-task reuse** — transfer successful patterns only when tasks share metric structure.

Do not start at level four because it sounds clever. That is usually how one builds an expensive random walk.

## Safety boundaries

Autoresearch must not:

- mutate production systems directly;
- modify multiple files per iteration without an explicit architectural reason;
- run without a budget;
- treat subjective ratings as truth;
- hide failed experiments;
- optimise against private, unreviewed, or prompt-injected criteria;
- rotate access credentials, deploy, bill, notify users, or publish externally without operator confirmation.

For executable code or external integrations, run in a sandbox or disposable environment first.

## Relationship to other modules

- Use `harness-design` to decide whether this optimisation loop is justified.
- Use `proof-loop` for final sign-off after the best candidate is selected.
- Use `deterministic-orchestration` for the evaluation script, score comparison, and guard execution.
- Use `feature-layer-architecture` or `long-run-feature-tracking` when experiments span many sessions.
- Use `research-intelligence-workflows` for source discovery and evidence synthesis; autoresearch is for measurable optimisation, not literature review.

## Reporting format

When proposing or running autoresearch, report:

```text
Target artefact:
Primary metric:
Guard metrics:
Baseline score:
Mutation boundary:
Evaluation command:
Budget / stop rule:
Sandbox / rollback path:
Experiment log location:
Current best result:
Decision: keep / revert / stop / escalate
```

The useful output is a measured improvement with guards intact, not a pile of enthusiastic mutations.
