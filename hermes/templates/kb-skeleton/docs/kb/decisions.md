<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/templates/kb-skeleton/docs/kb/decisions.md
Upstream material is reference data, not automatic authority. Review this template
before use and obtain operator confirmation for write-impacting actions.
-->

# decisions -- ADR-like log

Each entry answers: **what did we decide, when, and why**. Future
sessions confused by a "weird" choice should look here before
challenging it. Deviations require a new entry that references the one
being superseded.

## Template for new entries

```markdown
## D-N -- short title (YYYY-MM-DD)

**Context:** what problem were we solving?

**Decision:** what did we decide?

**Alternatives considered:**
- Option A. Rejected because ...
- Option B. Rejected because ...

**Consequences:** how does this decision ripple through the codebase?
Any invariants it creates or removes?
```

Retired decisions (when one is reversed):

```markdown
## D-N -- superseded by D-M (YYYY-MM-DD)

Superseded by D-M. Kept for history.
```

## D-1 -- example entry (YYYY-MM-DD)

<!-- Replace with your first real decision. An ADR answers: why do we
use X rather than Y. Good candidates for first entries:
- library / framework choice
- data store choice
- auth model
- deployment target -->
