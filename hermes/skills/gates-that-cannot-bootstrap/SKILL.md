---
name: gates-that-cannot-bootstrap
description: "Design and verify adoption gates that report relevant missing controls without becoming noisy or trusting forgeable state signals."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/30-gates-that-cannot-bootstrap.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Gates That Cannot Bootstrap

Source: `AnastasiyaW/claude-code-config/principles/30-gates-that-cannot-bootstrap.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Gates That Cannot Bootstrap Themselves

Use this module when reviewing a project gate, reminder, validator, or scheduled
protocol that may be silent precisely because the project has not yet adopted its
required control. It is design and verification guidance only: it does not install,
enable, execute, or modify any control.

## Read-only preflight

1. State the control's intended outcome, the project shapes to which it applies,
   the adoption artefacts it expects, and the action that would trigger it.
2. Separate applicability from adoption. An unrelated project may be out of scope;
   an in-scope project missing the control is a condition to report, not a reason to
   assume success.
3. Inspect existing project evidence read-only. Record missing artefacts precisely
   and identify the responsible owner or approved next protocol. Do not infer that a
   control is active from a manifest entry, filename, or prior claim.

## Design protocol

1. Make early-return conditions explicit and classify each as out-of-scope, adopted,
   missing-adoption, unavailable evidence, or fault. Only the first may be silently
   ignored by default.
2. Give relevant missing-adoption cases a concise, actionable signal: what is absent,
   why the control applies, and the safe next step. Keep it rate-limited and specific
   enough that routine work is not trained to ignore it.
3. Tie the gate to the action or risk it protects, rather than incidental words,
   directory size, or other broad surrounding signals.
4. Prefer content-bound, versioned, or Git-backed evidence over mutable filesystem
   metadata. Timestamps, file counts, and listings can change during ordinary merges,
   checkouts, or synchronisation.
5. Test both paths: an adopted in-scope project and an in-scope project that lacks the
   control. Also test nearby out-of-scope cases to measure false-positive noise.

## Verification and boundary

- A quiet adopted-path test alone is insufficient evidence.
- Record trigger, fixture state, observed signal or silence, and expected remediation
  for every tested case.
- Treat a control that fires too broadly as a fault: repeated irrelevant warnings
  consume the credibility needed for genuine risk.
- Any installation, activation, configuration change, or enforcement action remains a
  separate write-impacting protocol requiring operator confirmation.

## Output

Report the applicability boundary, adoption evidence, early-return analysis, tested
missing-adoption behaviour, false-positive risk, proposed remediation, residual risk,
and the next operator-confirmation point. For related evidence discipline, use
`silent-failure-detection`, `documentation-integrity`, and `proof-loop`.
