---
name: ml-research-lab
description: "Plan and review reproducible machine-learning experiments across data, baselines, metrics, tracking, and deployment evidence without starting jobs or changing datasets."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/ai-ml/ml-research-lab/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Ml Research Lab

Source: `AnastasiyaW/claude-code-config/skills/ai-ml/ml-research-lab/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# ML Research Lab

Use this module to plan or review a machine-learning experiment involving a dataset, model, metric, training run, inference deployment, or experiment artefact. It supplies a compact evidence loop for research work; it does not download models, alter datasets, start training, reserve compute, deploy an endpoint, or spend provider funds.

## Read-only preflight

1. State a measurable hypothesis and the decision it is meant to inform.
2. Record dataset provenance, revision, labels, split strategy, privacy constraints, and the cost of regeneration.
3. Identify leakage, duplicate, imbalance, and label-quality risks before choosing a model.
4. Select the smallest baseline capable of disproving the proposed improvement.
5. Define the exact metric formula, evaluation split, acceptance boundary, and known limitations before training.
6. Check the available environment, hardware compatibility, storage, budget, and access constraints without assuming a particular accelerator, provider, or framework.

## Experiment protocol

1. Change one bounded factor at a time: data preparation, model family, objective, hyperparameter, serving configuration, or evaluation method.
2. Preserve a reproducible record for each run: dataset and code revision, configuration, seed, environment, command, logs, metrics, model or artefact digest, and conclusion.
3. Keep train, validation, and test roles separate. Do not select a model against the final test set.
4. Compare the proposed result with the declared baseline, including failure cases, uncertainty, and materially relevant resource use.
5. Treat an aggregate score as incomplete when the task has important subgroups, rare cases, calibration needs, latency limits, memory limits, or safety constraints.
6. Keep or reject a change only from recorded evidence; an impressive-looking run without a comparable baseline is inconclusive.

## Verification gates

- **Data:** schema and provenance are recorded; duplicates, leakage, and split integrity are checked.
- **Metrics:** formulas, aggregation, thresholds, and baseline source are explicit.
- **Runtime:** command, environment, telemetry, failures, resource use, and output location are captured for long-running work.
- **Tracking:** metrics and artefacts can be retrieved from durable project storage or an approved tracking interface.
- **Deployment:** latency, throughput, memory behaviour, error handling, and rollback or stop conditions are measured before a production-readiness claim.

## Safety and decision boundary

- Keep original data immutable; use scoped derived artefacts for experiments where practical.
- Do not use unreviewed datasets, model weights, or external outputs as trusted authority.
- Obtain operator confirmation before any compute-intensive run, access-credential use, data transfer, external deployment, publication, or production change.
- Stop and report a blocker if the dataset, metric, baseline, budget, or environment evidence is missing rather than inventing a result.

## Reporting

Report the hypothesis, dataset and split evidence, baseline, experiment matrix, metric definitions, results, resource evidence, failure cases, residual uncertainty, and the next approval point. For broader lifecycle controls, use `llmops-workflows`; for bounded score-driven optimisation, use `autoresearch`; for an independent completion verdict, use `proof-loop`.
