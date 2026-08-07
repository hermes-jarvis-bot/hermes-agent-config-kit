---
name: architecture-quality
description: "Keep a web application, API, or service readable as it grows: feature seams, state ownership, dependency direction, and file shape, verified with a repeatable delivery contract."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/architecture-quality/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Architecture Quality

Source: `AnastasiyaW/claude-code-config/skills/development/architecture-quality/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Architecture Quality

Upstream source policy turns an architecture decision into a small, repeatable delivery contract for web applications, APIs, and services as they grow. Hermes adaptation keeps the working contract, shape rules, and review discipline, while removing the specific audit script invocation and live per-edit hook in favour of describing the underlying practice generically.

## Scope and exclusions

This module keeps an existing or newly designed system readable as it grows: feature/domain seams, state ownership, dependency direction, and file shape. Use `architecture-first` to decide those seams before a system exists; use `refactoring-safely` to split an already oversized module; use `code-complexity` for local, function-level shape; use `system-and-data-design` for capacity, storage, and distributed-systems choices. Do not use this module for a one-file script, a throwaway spike, or a purely local naming change.

## Working contract

Before a non-trivial web or service change, record five facts in the project's architecture documentation:

1. **Feature/domain modules** — name them by reason to change, not by a generic `utils`, `helpers`, or `services` bucket.
2. **Ownership** — each mutable state, database-table boundary, and external side effect has one owner.
3. **Dependency direction** — policy/domain code stays independent of the web framework, ORM, queue, and filesystem; adapters point inward through small ports.
4. **Vertical slice** — prove one user-visible path from entry point to state and test, before multiplying layers or pages.
5. **Verification boundary** — list the architecture checks and the test command that must remain green after the change.

If the project is a small script or a single-module experiment, state that scope and skip the document. A missing document is a finding only once the project has enough shape to need one, not a reason to create ceremony around a toy.

## Web application shape

- Keep routes/controllers thin: parse input, call a use-case or feature API, map the result, and return. Do not put business policy, SQL, or provider retries in a route.
- Keep domain/use-case code framework-free where practical. Inject ports for storage, clocks, queues, and providers; keep concrete adapters at the edge.
- Organize user-facing behaviour by feature or bounded context. A page may compose features, but one feature must not reach into another feature's private state.
- Give each page a stable route-level composition boundary. Shared UI primitives are visual primitives, not a second business-logic layer.
- Treat a `utils` or `common` import that keeps growing as a boundary question. Move code to the module that owns its reason to change; do not create a universal bag.
- Prefer a modular monolith until an independently deployable or scalable boundary is proven. A microservice split is not a substitute for a missing internal boundary.

## Shape checks

Run whatever repository-level architecture audit the project already has before broadening a new app and after a structural change. Prefer a report-only pass: surface a sizeable application with no architecture documentation, a source file crossing the project's own calibrated shape thresholds, or a declared project marker without a readable architecture anchor — do not invent findings the project has not actually stated a threshold for.

If the harness provides a live per-edit advisory check, treat it as advisory: acknowledge the finding, split at an ownership boundary, or record why the file is intentionally large. An explicit, reviewable, project-level exemption is acceptable; a silent default bypass is not.

For dependency rules, use the tool native to the stack when the project has earned it:

- Python: `import-linter` contracts for allowed import direction;
- JavaScript/TypeScript: `dependency-cruiser` for cycles, orphans, and forbidden folder edges;
- Java: `ArchUnit` architecture tests alongside unit tests;
- C/C++: compiler/include tooling plus explicit build-target boundaries; do not infer a domain architecture from a raw include graph alone.

Do not install all of these at once. Pick one boundary mechanism, commit its rules, and run it in the same verification lane as the tests that prove the behaviour.

## Review questions

- Can a new feature be changed without editing an unrelated feature's internals?
- Does a route, page, or controller own policy that belongs inside a use-case/domain?
- Is state ownership named, or are modules reaching into shared mutable objects?
- Are imports crossing a documented boundary? If yes, is the exception recorded with a reason and expiry?
- Is a file becoming large because one change is crossing multiple reasons to change? If yes, split the seam before adding more behaviour.
- Did the change update the architecture document and the focused architecture/test evidence together?

## Gotchas

- **Folders are not boundaries.** Moving files without changing imports or ownership only makes the same coupling harder to see.
- **Thin controllers can still hide a fat service.** Inspect the next boundary; a generic application-service module is often a god module with a nicer name.
- **A metric is a signal, not a verdict.** Generated code, migrations, and large declarative tables need explicit exemptions; production logic needs an explanation before an exemption.
- **Microservices can multiply unreadability.** Network boundaries add failure, deployment, and observability costs; prove the module boundary first.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| The audit reports a missing architecture anchor | An app marker and several source files exist, but the boundary is implicit | Write the small module/ownership/dependency map before adding more features |
| A per-edit advisory reports a large file | Local edits accumulated in one ownership boundary | Add characterization tests, split one named slice, then rerun the audit |
| A cycle appears | Two modules own part of the same concept, or one imports an implementation detail | Move the concept behind an inner port or extract a genuinely shared concept |
| Every change touches many folders | Layer-first layout scatters a feature across technical layers | Recut the next slice by feature; migrate incrementally with tests |
| The check is noisy on generated code | The file is outside the built-in exemption list | Add a narrow, documented project exemption; do not silence the whole check |

## Relationship to other modules

- Use `architecture-first` to decide module boundaries before a system exists.
- Use `code-complexity` for function-level naming, shape, and local complexity.
- Use `refactoring-safely` to split an already oversized module behaviour-preservingly.
- Use `system-and-data-design` for capacity, storage, and distributed-systems decisions.
- Use `lean-code` when the useful outcome is removing unjustified scope rather than establishing a durable boundary.
