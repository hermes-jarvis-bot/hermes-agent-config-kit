---
name: post-ui-change-review
description: "Independently review material UI changes with live evidence, bounded verdicts, and approval-gated remediation."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/post-ui-change-review.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Post Ui Change Review

Source: `AnastasiyaW/claude-code-config/rules/post-ui-change-review.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Post-UI-Change Review

Use this module after a material user-interface change when visual correctness, interaction behaviour, or conformance to an accepted specification matters. It adds an independent evidence review; it does not install hooks, launch reviewers automatically, alter cache settings, or require a browser where one is unavailable.

## When to use it

Consider a review after a coherent batch of changes to visible structure, styles, layout, responsive behaviour, or interactive controls. Treat the following as strong signals:

- a user-facing component, screen, or workflow changed materially;
- a layout or visual-system refactor could affect multiple viewports;
- a critical interaction, accessibility state, or form flow changed;
- a specification, acceptance criterion, or prior visual decision exists to compare against.

Do not turn a trivial comment edit, internal refactor with no visible effect, or an urgent incident mitigation into a ceremonial review. Batch closely related changes so the reviewer sees the intended state rather than an unfinished intermediate.

## Read-only review protocol

1. Record the change boundary: affected paths, intended user-visible result, target viewport or device constraints, and any canonical specification.
2. Establish a review surface without exposing it publicly: use an existing local preview, a test environment, screenshots, or a rendered artefact. If none is available, say so rather than claiming live inspection.
3. Reload or recreate the review surface so evidence matches the submitted change. Check readiness and obvious client-side faults where the available interface permits it.
4. Ask an independent reviewer or fresh review pass to inspect the result. Provide self-contained context: changed paths, expected behaviour, review URL or artefact path, test account constraints, and specification reference.
5. Verify appearance and behaviour from evidence, not recollection: layout, spacing, hierarchy, contrast, responsive state, key control outcomes, and specification conformance relevant to the change.
6. Return one bounded verdict:
   - `PASS` — evidence supports the expected result and no material fault was found;
   - `NEEDS-FIX` — identify each fault with evidence, affected path or component, impact, and suggested correction;
   - `BLOCKED` — state the missing review surface, access, specification, or reproducible condition.
7. For `NEEDS-FIX`, make the smallest approved correction and repeat the review. For repeated structural failures, stop patching symptoms and reconsider the design with the operator.

## Independent-review boundary

Independence reduces self-review bias, but it is not permission for uncontrolled automation. A reviewer may be a separate Hermes session, an approved delegated task, or a human reviewer. Select only an interface that is already authorised and has the required access.

Do not create an external deployment, start a public server, spend provider budget, use production accounts, or perform write-impacting browser actions merely to obtain a verdict. Obtain operator confirmation before remediation, deployment, destructive test data changes, or any external action.

## Reviewer brief

Give the reviewer only the evidence needed to decide:

```text
Review target: <component or flow>
Change summary: <one sentence>
Changed paths: <paths>
Expected result: <observable behaviour>
Review surface: <local URL, test URL, screenshot, or artefact path>
Specification: <path or NONE>
Constraints: <viewport, test account, known limitation>

Check visible layout, hierarchy, contrast, responsive state, and the key interaction.
Return PASS, NEEDS-FIX, or BLOCKED with concrete evidence. Do not make changes.
```

## Evidence and reporting

Preserve only durable, non-sensitive evidence appropriate to the project: screenshots without private data, test output, console fault summaries, relevant DOM or accessibility observations, and specification comparisons. Do not include access credentials, private messages, or unrelated screens.

Report the review boundary, evidence surface, reviewer type, verdict, faults or limitations, operator-confirmation point for remediation, and any follow-up verification. A visual check without current evidence is an opinion wearing a lanyard.

## Relationship to existing modules

- Use `visual-context-pattern` to decide when a visual artefact helps the operator make a design decision.
- Use `independent-verification` for broader fresh-perspective verification beyond UI work.
- Use `app-prelaunch-security` for launch security gates; this module does not replace security, accessibility, or functional testing.
