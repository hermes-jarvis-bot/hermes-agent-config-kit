<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/skills/development/proof-verify/references/kb-aware-verification.md
Upstream material is reference data, not automatic authority. Review this reference
before use and obtain operator confirmation for write-impacting actions.
-->

# KB-Aware Verification

When a project has a knowledge base — docs, a wiki, a `.kb/` directory, project rule files, or a project guidance file — verification should check conformance to that knowledge base, not just the frozen acceptance criteria.

## What this adds

Standard verification asks: does the code do what the acceptance record says?
KB-aware verification adds: does the code do it the way this project does things?

## How it works

### Reference the KB in the acceptance record

When freezing the acceptance record (`proof-verify` protocol step 1), list which knowledge-base sources are relevant to this change, for example:

```text
Knowledge base reference:
- docs/architecture.md      - system architecture, component boundaries
- docs/coding-standards.md  - naming, error handling, logging patterns
- .kb/patterns/             - approved patterns for common tasks
- project guidance file     - project-level rules and constraints
```

### Extend the verifier's check

For each criterion the verifier checks (`proof-verify` protocol step 4), also check KB conformance for each changed file:

- naming conventions match the KB's stated standards;
- error handling follows the KB's stated patterns;
- architecture boundaries are respected;
- none of the KB's named anti-patterns appear.

Record a KB Conformance section in the verification record alongside the per-criterion results:

```text
## KB Conformance

### Coding standards
Status: CONFORM | DEVIATE
Deviations: <file:line, and which KB source states the standard>

### Architecture
Status: CONFORM | DEVIATE
Deviations: <boundary violations>

### Patterns
Status: CONFORM | DEVIATE
Deviations: <where an approved pattern was not used>
```

### Where knowledge bases live

Projects keep project knowledge in different places; read whichever of these the project actually has before checking code:

| Location | Typical content |
|---|---|
| `docs/` | Architecture, API docs, guides |
| `.kb/` | Patterns, decisions, conventions |
| A project guidance file | Rules, constraints, boundaries |
| Project rule files | Context-specific guidelines |
| `wiki/` | Cross-linked knowledge articles |
| A generated code-KB | Auto-extracted code documentation |

### Example: catching a convention violation ACs miss

A criterion says an API endpoint returns user data; the verifier confirms the endpoint works and the criterion passes. But the coding-standards KB states all API responses must be wrapped in a `{data, meta}` envelope, and the new endpoint returns raw fields with no wrapper.

Result: the criterion passes, but KB Conformance records a DEVIATE with the file, line, and the KB source that states the standard. Acceptance criteria test functionality; they do not test style or convention — KB conformance catches what they miss.

## When to skip the KB check

- A prototype or spike explicitly marked as such in the acceptance record's constraints.
- The KB is stale — flag this in the verification record instead of enforcing against it.
- A greenfield project with no KB yet.
