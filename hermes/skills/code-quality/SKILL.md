---
name: code-quality
description: "Build the minimum correct solution: avoid both monkey patches and speculative over-engineering, then verify the result."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/quality-code.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Code Quality

Source: `AnastasiyaW/claude-code-config/rules/quality-code.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Code Quality

Upstream source policy frames code quality as the midpoint between two faults: speculative over-engineering and fragile monkey patches. Hermes adaptation keeps that practical standard and removes harness-specific hook machinery.

## Principle

Build the minimum correct solution.

Minimum does not mean incomplete. Correct does not mean ornate. The target is the smallest design that fully solves the requested behaviour, handles real edge cases, and can be verified.

## Avoid monkey patches

Do not use a hack, monkey patch, global override, or unexplained shim merely because it is fast.

A shortcut is acceptable only when:

- there is a real emergency or production-impacting fault;
- the operator accepts the trade-off;
- the patch is scoped and documented;
- a follow-up path to the clean solution is recorded.

If the choice is between a brittle patch and a clean small rewrite, prefer the clean rewrite and verify it.

## Avoid over-engineering

Do not add speculative architecture for needs that do not exist yet. Before adding code, ask:

1. Is this requirement real and in scope?
2. Can the standard library or native platform feature solve it?
3. Can existing project code or dependencies solve it?
4. Can this be a simple function, data structure, or configuration change?
5. Only then add the smallest new code that handles the requirement.

Avoid:

- abstractions with one implementation;
- factories for one product;
- configuration for values that are not actually variable;
- new dependencies for a few lines of stable logic;
- boilerplate that exists only for imagined future work.

## Mark intentional simplifications

A deliberate simplification with a known ceiling should say so near the code:

```text
simplification: global lock is acceptable while throughput is low; use per-account locks if contention appears.
simplification: linear scan is acceptable below 10k records; add an index if this becomes a hot path.
```

The comment should name both the ceiling and the upgrade path. Without that, future maintainers cannot tell judgement from accident.

## Do not simplify away safety

Never remove or underbuild:

- validation at trust boundaries;
- error handling that prevents data loss;
- security controls;
- availability and retry behaviour that users depend on;
- calibration for real hardware or external systems;
- explicitly requested functionality.

Minimalism is not permission to skip branches, tests, or verification.

## Verification requirement

Non-trivial logic needs at least one runnable check that would fail if the logic broke. Prefer the smallest useful verification:

- a unit test;
- a focused integration check;
- a small self-check routine;
- a real command run with captured output.

For trivial one-line changes, use judgement, but still inspect the diff.

## Reporting format

When applying this module, report:

- what complexity was avoided;
- what shortcuts, if any, were intentionally accepted;
- why the solution is complete rather than merely small;
- what verification ran;
- any remaining follow-up required.

The goal is not fewer lines. The goal is less unnecessary surface area and fewer charming little future incidents.
