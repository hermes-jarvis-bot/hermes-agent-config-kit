---
name: low-signal-residual-training
description: "Diagnose and design reproducible training experiments where sparse residual targets make aggregate metrics misleading."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/12-low-signal-residual-training.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Low Signal Residual Training

Source: `AnastasiyaW/claude-code-config/principles/12-low-signal-residual-training.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Low-Signal Residual Training

This module adapts a narrow training diagnostic for datasets whose useful target is a small deviation around a baseline. It keeps the reproducible experiment discipline while omitting project-specific model choices, personal case studies, hardware claims, and executable data-processing instructions.

## Scope and safety boundary

Use this guidance for supervised image, audio, sensor, or numerical tasks where a near-constant target can score well while missing the important structure. It is planning and review guidance only: it does not download models, modify datasets, start training, delete files, or grant access to compute or data.

Before a training run, record the dataset revision, target representation, baseline distribution, loss, metrics, preprocessing, seed, environment, and intended output location. Confirm access, compute cost, data handling, and any long-running job with the operator where required.

## Failure signature

A low-signal target has a narrow distribution around a neutral baseline, with sparse or subtle deviations that matter to the result. Aggregate loss can improve when a model predicts the baseline everywhere. Treat that outcome as a diagnostic hypothesis, not success.

Check both:

1. **Global metrics** — loss, error, calibration, and stability on a held-out split.
2. **Signal-sensitive evidence** — stratified error on active regions, residual histograms, signed-error breakdowns, and blinded sample inspection at an agreed amplification or contrast scale.

A metric that hides the active region is not a sufficient acceptance criterion.

## Read-only preflight

Before changing a training configuration:

1. Measure target mean, spread, quantiles, sign balance, and the fraction of active samples or pixels.
2. Verify that target storage and preprocessing preserve the required precision; quantify compression or conversion error against the expected signal scale.
3. Compare a constant-baseline predictor with the current model using both global and active-region metrics.
4. Check whether metrics are computed in the same scale as the reported output; record every normalization or amplification factor.
5. Sample the train and validation splits for background dominance, leakage, mismatched crops, or empty regions.
6. Inspect output constraints for gradient saturation near values that the task needs to learn.

Stop and correct the measurement design if the baseline already looks competitive only because the metric ignores the meaningful residual.

## Controlled experiment protocol

Change one bounded factor per experiment in an isolated, reproducible run:

- target scaling or normalization, applied consistently in data preparation and metric inversion;
- loss family, with signed or active-region reporting where appropriate;
- target precision or preprocessing validation;
- sampling/cropping strategy that increases signal density without corrupting split boundaries;
- output constraint and gradient behaviour;
- warmup, learning-rate schedule, or delayed averaging policy.

For each run, keep the baseline, configuration diff, seed, commands, metrics, representative outputs, guard results, and decision to keep or reject. Do not compare runs that differ in unrecorded scaling or evaluation definitions.

## Guardrails

- Preserve original data and use disposable derived artefacts for format or preprocessing trials.
- Do not rely on one aggregate metric across differently scaled configurations.
- Check positive and negative residuals separately when the target is signed or asymmetric.
- Treat numerical improvement without signal-sensitive evidence as inconclusive.
- Start with a small bounded sweep; stop on instability, repeated collapse, budget exhaustion, or ambiguous evaluation.
- Do not promote a model, publish results, or spend unapproved compute based on this module alone.

## Reporting

Report the target distribution, baseline comparison, metric scale, active-region definition, experiment matrix, guard outcomes, selected configuration, remaining uncertainty, and the approval point for any costly or external next action.

Use `llmops-workflows` for broader model lifecycle controls, `autoresearch` for score-driven optimisation with guard metrics, and `proof-loop` for independent completion evidence.
