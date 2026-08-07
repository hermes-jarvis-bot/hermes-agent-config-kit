---
name: testing-strategy
description: "Classify a code change's risk and select the smallest test-level evidence set that can falsify the changed behaviour, from unit through agent-evaluation checks."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/testing-strategy/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Testing Strategy

Source: `AnastasiyaW/claude-code-config/skills/development/testing-strategy/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Testing Strategy

Upstream source policy treats test-level selection as an evidence-selection problem, not a contest to run the largest suite. Hermes adaptation keeps the risk-based test-level matrix, the test-kind taxonomy, and the evidence contract, while describing the session-close gate and its configuration generically instead of naming a specific hook and hidden path, and dropping a cross-reference to a module this adapter does not carry.

## Principle

Choose the smallest test set that can falsify the changed behaviour, then add one higher-level check only when it covers a boundary the lower level cannot. Keep execution environments reusable, but separate their evidence profiles: `staging-smoke`, `security-proof`, `release-attestation`, and `nightly-stress` (see `harness-feedback` for that taxonomy). Use `harness-feedback` when a gate is reported as overloaded or misplaced.

## Workflow

1. Freeze the acceptance criteria as observable outcomes.
2. Inspect the changed files and classify the risk.
3. Select the lowest useful test level from the matrix below and name the profile.
4. Run the fast gate first. If it fails, fix the cause before adding more tests.
5. Add a focused regression test for a confirmed bug or a changed invariant: reproduce the failure first, then fix, then rerun the same test.
6. Test real boundaries only when the change crosses them.
7. Keep `security-proof` and `release-attestation` checks out of `staging-smoke` unless the acceptance criteria explicitly require that evidence.
8. For high-risk or long-horizon work, use a fresh-context verifier (see `proof-verify`) and store the command, revision, result, and skipped checks in a durable artefact.

## Compact matrix

| Change | Required evidence | Usually deferred |
|---|---|---|
| Docs, comments, formatting only | Link/lint check when relevant | Runtime suite |
| Pure function, local refactor | Fast checks + focused unit/regression tests | Full E2E, mutation |
| Parser, serializer, file, DB, API adapter | Fast + focused + one real boundary/integration check | Browser E2E unless user flow changes |
| Auth, permissions, migrations, concurrency, public API, deployment | Fast + focused + integration/contract + targeted smoke; independent review for non-trivial changes | Full load test unless performance is in scope |
| UI or user journey | Fast + component/focused checks + one stable E2E smoke | Large browser matrix |
| Release or performance claim | All applicable lower levels + fixed benchmark/security/release evidence | Nothing that is part of the claim |

If the harness runs the project's fast/default suite automatically at session close, scope that gate to when the working tree actually contains code or test changes. For a project with a complex suite, declare a project-level test-policy record naming the fast, integration, and release commands separately, for example:

```json
{
  "fast": ["python", "-m", "pytest", "-q", "tests/unit"],
  "integration": ["python", "-m", "pytest", "-q", "tests/integration"],
  "release": ["python", "-m", "pytest", "-q"]
}
```

`fast` is the automatic session-close gate. `integration` is additionally selected for high-risk changes when present. `release` is explicit or CI-only; do not make every edit pay the release-suite cost. Keep the separation explicit — a staging profile must not contain release-signing requirements.

## Test kinds

- **Unit:** isolated behaviour and invariants; fast and numerous.
- **Focused regression:** a minimal test that was red before a fix and green after it. Keep it when it protects a real contract.
- **Integration:** one real boundary such as a database, filesystem, queue, or external adapter. Use a local/test dependency, never production.
- **Contract:** provider/consumer schema and serialization expectations.
- **Smoke/E2E:** a small number of real user or release paths; keep them stable.
- **Property/fuzz:** invariants over generated inputs; use for parsers, normalizers, state machines, and edge-heavy algorithms.
- **Performance/security:** only when the change or release claim needs it; preserve a fixed workload and baseline.
- **Agent eval:** test task completion, tool selection, recovery, and safety on a versioned golden set. Deterministic assertions come first; an LLM judge is an additional signal, never the sole proof of code correctness.

## Agent evidence contract

Report: revision, changed scope, commands actually run, exit status, relevant counts, environment constraints, and checks not run with a reason. "Tests passed" without command output or a durable evidence file is not proof. A generated test is a candidate until it reproduces the failure or asserts a stable contract; do not add broad snapshot tests merely to inflate coverage.

For a large or high-risk change, use `proof-verify`: a fresh context must produce the final verdict. For a safe structural refactor, use `refactoring-safely` and characterization tests before the transformation.

## Anti-duplication rules

- If a higher-level test finds a failure with no lower-level failure, add the smallest lower-level reproducer and keep the higher-level test only if it proves a distinct boundary.
- Do not run unit, integration, E2E, benchmark, and security suites by default just because they exist. Route by changed boundary and risk.
- Do not use retries, sleeps, snapshots, or a skip/expected-failure marker to make a red test look green. A flaky test needs a cause, a bounded quarantine reason, or a fix.
- Do not claim release readiness from a fast suite alone.

## Gotchas

- A green test suite proves only the exercised behaviour; it does not prove absence of defects.
- Mocks can hide serialization and wiring failures. Keep one real boundary test for each important adapter.
- End-to-end tests are valuable but expensive and flaky; they should protect journeys, not duplicate every branch already tested below.
- Mutation testing is a periodic test-quality audit, not a per-edit gate; verify a chosen tool's runtime requirements on the target platform before adding it to CI.
- Agent trajectories need task-outcome checks and tool-call checks, not only final-text similarity.
- A VM harness is an execution environment, not a release profile. Reuse it for staging and security checks, but attach signing and artifact-identity checks only to `release-attestation`.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Session-close gate runs on a docs-only change | No scope check, or a broad override | Check the actual changed-file scope; keep the default command scoped in the project's test-policy record |
| Fast suite passes, integration fails | A real boundary was changed or mocked away | Add/fix the boundary test; do not weaken the fast gate |
| E2E is flaky | Timing, shared state, browser/environment dependency | Make state isolated and waits explicit; reduce E2E to a stable smoke |
| Generated test passes without exposing the bug | Test asserts implementation details or never goes red | Reproduce the pre-fix failure and assert the user-visible invariant |
| Agent claims completion with skipped checks | Missing evidence contract or verifier | Record the skip reason and run `proof-verify` for high-risk work |
| Agent says the harness is too strict or blocks smoke | Profiles are coupled or a gate is misplaced | Invoke `harness-feedback`; capture the blocker, split profiles, and rerun the reduced smoke |

## Relationship to other modules

- Use `harness-feedback` when a specific gate is reported as overloaded, too strict, or misplaced.
- Use `proof-verify` for the frozen-acceptance-criteria, fresh-context verification cycle on high-risk or long-horizon work.
- Use `refactoring-safely` for characterization tests before a behaviour-preserving structural change.
