---
name: verify-this
description: "Prove a concrete behavior, performance, UI, CLI, API, or memory claim with fresh baseline-versus-treatment evidence and one explicit verdict."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/verify-this/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Verify This

Source: `AnastasiyaW/claude-code-config/skills/development/verify-this/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Verify This

Verification is a falsifiable comparison, not a recap of what the agent believes it changed. Turn one claim into a measurable check and preserve enough evidence for another agent to repeat it.

## Workflow

1. Restate the claim as a condition, metric, and threshold. If the claim cannot be measured, ask for a measurable form or classify it as `INCONCLUSIVE`.
2. Select the smallest local surface that can disprove it.
3. Capture a baseline from the parent commit, merge base, current failing reproducer, or unchanged fixture.
4. Capture treatment with the same command, data, warmup, environment, and measurement method.
5. Compare raw artifacts: test output, timings, screenshots, HTTP responses, traces, profiles, or heap snapshots. Do not compare summaries alone.
6. Return exactly one verdict: `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`.

## Evidence contract

Record:

- claim and threshold;
- revision or baseline identity for both runs;
- exact commands and input fixture;
- environment differences and skipped checks;
- artifact paths or hashes, with sensitive payloads kept outside public Git and outside any shared Hermes profile;
- the verdict and one short explanation of confounders.

For durable project work, use whatever proof-artifact location the project already has (do not invent a new hidden directory or task-state schema for this). Temporary or sensitive evidence may stay outside the repository; retain only safe metadata and hashes in the project. Never put credentials, private prompts, customer data, or heap contents in a public checkout.

## Verdict rules

- `VERIFIED`: baseline and treatment move in the predicted direction, meet the stated threshold, and have no material confound.
- `NOT VERIFIED`: behavior is unchanged, moves the wrong way, or misses the threshold.
- `INCONCLUSIVE`: there is no valid baseline, the signal is too noisy, the command failed, or the environments are not comparable.

Use this output shape:

```text
VERIFIED | NOT VERIFIED | INCONCLUSIVE
Claim: <falsifiable claim>
Evidence:
<artifact or metric>: baseline=<...>, treatment=<...>, delta=<...>, threshold=<...>
Reasoning:
<one tight paragraph naming evidence and confounders>
```

## Boundaries

- Use `proof-verify` when the work has frozen multi-criterion acceptance criteria and needs a fresh-context verifier; this module is for one falsifiable claim at a time, not a full acceptance pass.
- A single green test is not enough for a performance, release, UI, or memory claim unless it is the stated evidence surface.

## Gotchas

- A different fixture, warm cache, compiler, or machine can invalidate a baseline comparison; report it instead of smoothing it away.
- A missing baseline is not a passing baseline. Use `INCONCLUSIVE`.
- A test can pass while user-visible behavior remains wrong; use the real CLI, browser, API, or artifact boundary when that is the claim.
- Do not turn a failed comparison green with retries, wider tolerances, or a changed workload unless the claim itself was explicitly re-scoped.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| No comparable baseline | Parent state or repro is unavailable | Report `INCONCLUSIVE`; capture a new baseline before changing the claim |
| Results vary between runs | Warmup, shared state, timing noise, or nondeterminism | Fix isolation and repeat with a fixed workload; record variance |
| Treatment passes but claim is still doubtful | Wrong evidence surface | Move to the real boundary or add one focused integration/UI/CLI check |
| Evidence contains sensitive data | Raw artifact is not suitable for Git | Keep it private and record only safe metadata or a hash |

## Provenance

Upstream adapted this from Cursor Team Kit's MIT-licensed `verify-this` workflow (`github.com/cursor/plugins/tree/main/cursor-team-kit/skills/verify-this`). Two upstream cross-references were dropped rather than adapted: `bug-reproducer` and `testing-strategy` are not modules this adapter ports, so pointing at them would be a dangling reference.
