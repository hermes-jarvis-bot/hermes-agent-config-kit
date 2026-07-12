---
name: proof-verify
description: "Prepare a frozen acceptance-criteria record and obtain a fresh, read-only verification verdict without activating task state or delegation."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/proof-verify/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Proof Verify

Source: `AnastasiyaW/claude-code-config/skills/development/proof-verify/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Proof Verify

Use this module for a bounded, planned change where an independent verification verdict is more useful than a builder's self-certification. It is guidance only: it does not create task files, dispatch agents, invoke a routine, alter a project, or approve a change.

## Applicability

Use when acceptance criteria can be frozen before implementation and checked afterwards with observable evidence. Prefer a lighter focused check for exploratory work, tiny reversible edits, or work whose requirements are still changing.

## Protocol

1. **Freeze the acceptance record.** Before implementation, record three to eight specific, testable criteria, their verification commands or inspection methods, expected outcomes, exclusions, and relevant constraints in a project-approved location. Do not silently revise criteria during the build; record a changed requirement as a new approved decision.
2. **Build within scope.** The builder makes the smallest change that addresses the frozen criteria and records factual evidence such as command output, diffs, telemetry, or consumer-side results. Evidence is not a verdict.
3. **Separate the verifier.** Request a fresh-context reviewer or independently scoped session where the risk warrants it. Give that verifier the frozen criteria and repository access, but do not rely on the builder's conclusions as proof. The verifier remains read-only unless separately authorised.
4. **Check each criterion.** The verifier runs or inspects the stated checks safely, records PASS, FAIL, or BLOCKED with concrete evidence, and distinguishes incomplete evidence from a passing result.
5. **Resolve failures narrowly.** A builder may apply the smallest authorised fix for a failed criterion, then obtain a new independent verification result. Do not convert a qualified concern into a pass.

## Evidence boundaries

- Treat test names, status messages, and self-reported completion as claims until the expected effect is observed.
- For integrations, include receiving-side evidence where practical rather than only sender telemetry.
- Keep verification records in a project-approved location; this module does not prescribe a hidden directory, a file schema, or a task lifecycle.
- Never write a verdict or modify project state without the normal operator confirmation required by that project.

## Verdict format

Record the frozen criteria reference, verifier identity or separation boundary, date, evidence for each criterion, residual risk, and an overall PASS, FAIL, or BLOCKED result. PASS requires positive evidence for every criterion; uncertainty is BLOCKED or FAIL according to the stated acceptance boundary.

## Relationship to existing modules

Use `proof-loop` for the broader durable proof cycle, `independent-verification` for behavioural checks of controls and side effects, and `verify-at-consumer` when the outcome crosses an integration boundary. This module supplies the narrow plan-to-fresh-verdict protocol that joins those practices without activating automation.
