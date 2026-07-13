---
name: plan-to-tickets
description: "Turn a large approved plan into small, independently verifiable agent-ready tickets with concrete acceptance criteria, verification evidence, blockers, and vertical tracer-bullet slices."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/plan-to-tickets/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Plan To Tickets

Source: `AnastasiyaW/claude-code-config/skills/plan-to-tickets/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Plan To Tickets

Use this module when a large approved plan, PRD, feature, refactor, research plan, or multi-step coding task must be decomposed into small agent-ready tickets. Each ticket should have concrete acceptance criteria, verification evidence, explicit blockers, and a narrow vertical tracer-bullet slice. Do not use it for a small task that should be implemented directly, a single bug fix, or a chat-only summary.

This module complements the builtin `plan` and `writing-plans` modules. Those establish an implementation plan; this module turns an already understood plan into independently executable ticket contracts. It does not create tickets, publish tracker issues, run a validator, dispatch agents, or authorise implementation.

## Output location

When the operator or project has not selected an issue tracker, propose local ticket files under the project-relative path:

`<project>/.agent/tickets/<YYYY-MM-DD>-<slug>/`

Use one Markdown file per ticket, for example:

`TICKET-001-short-slug.md`

Creating ticket files or publishing external issues remains subject to the project’s normal write and operator-confirmation policy.

## Required ticket shape

Each ticket contains these headings:

- `## Status`
- `## Parent`
- `## What To Build`
- `## Acceptance Criteria`
- `## Verification`
- `## Blocked By`
- `## Notes`

Mark a ticket `ready-for-agent` only when every acceptance criterion and verification step is concrete. Acceptance criteria use observable checklist items. Verification names at least one relevant test, command, artefact inspection, or explicit manual-review gate.

## Slicing rules

- Prefer vertical tracer bullets: a narrow, complete path through the necessary layers rather than separate broad backend, UI, and test tickets.
- Make every ticket independently verifiable.
- Put preparatory refactoring first only when it makes a later slice materially smaller or safer.
- Record dependencies in `## Blocked By`; use `None` only when work can start immediately.
- Avoid stale-prone paths unless current codebase evidence establishes them as a stable contract.
- Do not publish external tracker issues unless the operator selected that tracker.

## Planning protocol

1. Read the approved plan and the smallest current project context needed to avoid invented tickets.
2. Identify the independently testable outcome and dependency boundary for each vertical slice.
3. Draft tickets in dependency order with concrete acceptance criteria, evidence-producing verification, scope exclusions, and blockers.
4. Review the set for overlap, hidden ordering, horizontal-only work, and tickets that cannot be verified alone.
5. Before declaring the split ready, run the project’s applicable checks or perform the stated manual-review gate. If no suitable check exists, report that evidence gap rather than claiming validation.
6. Report the proposed ticket directory, ready-ticket count, blocked tickets, verification evidence, and any operator decision still required.

## Avoid

- Horizontal tickets that leave integration or verification to an unspecified later agent.
- "Implement feature" as an acceptance criterion.
- "Run tests" without naming the relevant check or observable artefact.
- Ticketization used to postpone a task small enough to complete directly.
- Treating ticket status as proof that implementation or verification has occurred.
