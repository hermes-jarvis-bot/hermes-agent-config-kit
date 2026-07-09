---
name: independent-verification
description: "Verify control systems, monitors, schedulers, cleanup routines, and side-effect functions by behaviour, not by names or claims."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/system-verification-independent.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Independent Verification

Source: `AnastasiyaW/claude-code-config/rules/system-verification-independent.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Independent Verification

Upstream source policy was written from a watchdog failure case in a different harness. Hermes adaptation keeps the rule: verify behaviour independently; do not trust names, comments, or self-certification.

## Principle

Any control system or side-effect routine must be verified by observed behaviour, not by what it is called or what it claims to do.

Apply this to:

- watchdogs, monitors, health checks, and alerting routines;
- kill switches, deadline enforcers, and stop/start controls;
- schedulers, cron jobs, and recurring protocols;
- cleanup, deletion, rotation, and migration routines;
- functions that mutate state, send messages, deploy, restart, bill, or revoke access.

A function named `kill_training_at_deadline`, a script named `cleanup_old_files`, or a service marked `healthy` is only a claim until the expected effect is verified.

## Verification layers

1. Read the implementation with scepticism. Follow control flow, branches, error handling, and side effects.
2. Run a safe dry-run, mock, or disposable-environment test where possible.
3. Verify the effect at the target: process gone, file absent, row written, event delivered, service restarted, schedule fired.
4. For critical systems, use a fresh-context verifier or reviewer that did not write the implementation.

## Hermes examples

- A scheduled protocol is not proven by successful creation; inspect its run history or run it once deliberately.
- A remover is not proven by `Actions: 1`; verify the target directory is absent.
- A background watchdog is not proven by a process id; verify heartbeat and trigger behaviour.
- A deployment script is not proven by exit code alone; check the running version and health endpoint.
- A safety check is not proven by its name; inspect the condition it actually enforces.

## Anti-patterns

- Trusting a function name, comment, README, or service label as behavioural proof.
- Letting the same agent that wrote the control logic provide the only verdict.
- Testing only the happy path while the danger lies in timeout, empty target, missing permission, or partial failure.
- Reporting `configured`, `installed`, or `started` as if it meant `working`.

## Reporting

State the evidence source explicitly:

- `implementation read: trigger condition confirmed at line ...`;
- `dry-run selected the expected target only`;
- `post-action read-back confirmed target absent`;
- `run history shows the scheduled protocol fired at ...`;
- `independent reviewer verdict: MATCH / MISMATCH / AMBIGUOUS`.

If the evidence is incomplete, say `not independently verified` and describe the missing behavioural check.
