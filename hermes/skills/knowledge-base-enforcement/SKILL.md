---
name: knowledge-base-enforcement
description: "Turn accepted review findings into durable contracts: fixes, regression checks, and invariant records with cross-references."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/21-knowledge-base-enforcement.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Knowledge Base Enforcement

Source: `AnastasiyaW/claude-code-config/principles/21-knowledge-base-enforcement.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Knowledge Base Enforcement

Upstream source policy turns expensive review output into durable project contracts. Hermes adaptation keeps the contract pattern and removes harness-specific assumptions: no validator, CI workflow, template tree, or agent review machinery is installed automatically.

## Principle

Accepted review findings should not survive only as chat history, commit messages, or memory summaries.

For important findings, preserve three durable forms:

1. **Fix** — the code or configuration change that resolves the finding.
2. **Regression check** — a runnable test or focused verification that fails if the finding returns.
3. **Invariant record** — a concise knowledge-base entry explaining the rule, the reason, and the enforcement locations.

Missing the fix leaves the bug. Missing the check loses behavioural proof. Missing the invariant loses the reason future sessions need.

## When to use

Use this module when:

- a code review produces accepted findings that should not be rediscovered later;
- multiple sessions, agents, or humans will touch the same project;
- the project has non-obvious invariants around security, concurrency, data integrity, billing, migrations, or external integrations;
- a future operator would not infer the rule merely by reading the final code.

Skip or keep it lightweight when the project is a throwaway script, the codebase is tiny, or the invariant is already obvious from ordinary tests and naming.

## Suggested repo-local shape

A minimal Hermes-friendly knowledge base can be plain markdown:

```text
AGENTS.md                 # entry point and operating boundaries
docs/kb/README.md         # how the project KB is used
docs/kb/INVARIANTS.md    # durable rules, I-1, I-2, ...
docs/kb/conventions.md   # local idioms and style decisions
docs/kb/gotchas.md       # known foot-guns and workarounds
docs/kb/decisions.md     # decision log when ADR weight is justified
docs/kb/modules/*.md     # per-area contracts for large projects
```

Do not add this structure mechanically. Create the smallest shape that future sessions will actually read.

## Invariant entry shape

Use compact entries with evidence links:

```markdown
### I-2 -- Audit rows write independently

**Statement:** `audit.record()` accepts a session factory. Handler transactions and audit writes remain independent.

**Reason:** Review L3 F3 found that sharing the handler session could commit a partial side effect with a misleading success audit row.

**Enforced in:** `bot/services/audit.py`.

**Regression check:** `tests/test_observability.py::test_audit_record_takes_factory_not_session`.
```

Prefer stable paths and test names. If line numbers are useful, treat them as convenience, not the only reference.

## Review-to-contract protocol

For each accepted finding:

1. Decide whether it is worth preserving as an invariant.
2. Apply the fix in code.
3. Add or update the smallest runnable regression check.
4. Add an invariant entry with the statement, reason, enforcement location, and check.
5. Verify that the check fails when the old behaviour is present, when feasible.
6. Verify that documented paths and test names resolve.
7. Include the invariant ID in handoff or PR notes when the finding matters to future work.

Do not create an invariant for every typo. Durable contracts should capture rules that future maintainers are likely to miss.

## Optional validation

A repository may later add a reviewed validator that checks knowledge-base references, for example:

- documented paths exist;
- referenced tests exist;
- `AGENTS.md` links to present KB files;
- module docs exist for selected load-bearing areas.

That validator is a separate implementation task. This module does not install scripts, hooks, CI workflows, or scheduled protocols automatically.

## Relationship to other modules

- Use `documentation-integrity` to check that KB links, paths, commands, and counts are still true.
- Use `proof-loop` for the regression-check discipline.
- Use `git-source-of-truth` so KB updates, fixes, and checks become committed project state.
- Use `code-wiki` for broad reference documentation; use this module for durable invariants and review findings.
- Use Obsidian for personal or cross-project notes; keep project invariants in the repo when they govern code behaviour.

## Reporting format

When applying this module, report:

- finding or invariant ID;
- code/config fix path;
- regression check path and command;
- KB entry path;
- validation performed;
- any accepted gap, such as missing negative test or unresolved reference.

A review finding without a durable contract is often just an expensive way to have the same conversation twice.
