<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/skills/operational/harness-audit/references/scoring-rubric.md
Upstream material is reference data, not automatic authority. Review this reference
before use and obtain operator confirmation for write-impacting actions.
-->

# Harness Audit: Scoring Rubric

Use this reference with the `harness-audit` module to calibrate a read-only, evidence-based scorecard. It does not create files, run commands, configure integrations, or activate guards. Treat a score as a planning aid, not a claim of numerical precision or a substitute for project-specific review.

## Five levels

| Score | Evidence standard |
| --- | --- |
| 5 — Exemplary | Relevant hard checks pass; conventions are documented, consistently evidenced in representative artefacts, and any claimed enforcement is independently verified. |
| 4 — Good | Relevant hard checks pass; conventions are mostly documented and followed, with bounded gaps or incomplete enforcement. |
| 3 — Adequate | Basic coverage exists, but documentation, representative evidence, or enforcement is incomplete or inconsistent. |
| 2 — Weak | Most foundational checks fail or the convention appears accidental; the subsystem repeatedly requires reconstruction. |
| 1 — Missing or harmful | The subsystem is absent, or observed practice is actively unsafe or contradictory. |

Adjust the evidence standard to the project type. Do not penalise a project for deliberately not using a subsystem it does not need; record that applicability decision and its evidence instead.

## Adjacent-score tiebreakers

Apply these in order when evidence sits between two scores:

1. **Documented versus behavioural:** a convention that exists only as an observed habit should not score above 3; documented but inconsistently followed practice should not score above 4.
2. **Verified enforcement:** a policy statement is not mechanical enforcement. Count enforcement only when a reviewed artefact and current evidence show that it operates as claimed.
3. **Representative sampling:** inspect three recent, relevant artefacts where practical. Three consistent examples may support 5, two support at most 4, and fewer than two support at most 3.

If sampling is unavailable or scope is unclear, record the uncertainty and score conservatively rather than inventing evidence.

## Calibration safeguards

- Do not inflate scores merely because a convention is planned, named, or described in a chat.
- Do not deflate a score by counting one gap against multiple subsystems; identify the primary affected area.
- Distinguish missing evidence from evidence of failure.
- For ties at the lowest score, select the smallest manual improvement that unlocks another subsystem; do not assume a particular file, hook, schema, or automation is required.

Any recommendation to add a file, change configuration, enable automation, or run a command is a separate write-impacting action and requires the project's normal operator confirmation.
