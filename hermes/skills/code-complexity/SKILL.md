---
name: code-complexity
description: "Keep functions, interfaces, and modules comprehensible through information hiding, clear names, bounded responsibilities, and explicit error handling."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/code-complexity/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Code Complexity

Source: `AnastasiyaW/claude-code-config/skills/development/code-complexity/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Code Complexity

Use this module when writing or reviewing an existing function, class, or module that
is hard to understand or expensive to change. It is a read-only analysis protocol: it
does not modify code, add dependencies, or authorise a refactor.

## Scope and exclusions

This module improves the comprehensibility of an existing unit: function shape, names,
interfaces, local responsibilities, information hiding, comments, errors, and tests.
Use `architecture-first` for system boundaries and code placement; `refactoring-safely`
for a named, verified transformation of an oversized unit; `system-and-data-design` for
capacity, storage, scaling, or distributed-system choices; and `lean-code` to remove
unjustified scope. It complements `code-quality`; it does not replace project-specific
correctness, security, or review requirements.

## Read-only complexity review

1. State the observed change cost and inspect the smallest relevant call sites, tests,
   public contract, and error paths. Record behaviour that must remain stable before
   proposing a simplification.
2. Identify change amplification and leaked knowledge: a decision belongs to one owner;
   callers should not need unstated locks, formats, ordering rules, or configuration.
3. Assess interface depth. Prefer a small, clear interface that hides useful behaviour;
   do not split a coherent unit into shallow wrappers merely to reduce line count.
4. Check names, responsibilities, parameters, comments, and error handling. A name
   should reveal intent; a function should operate at one abstraction level; comments
   preserve why and constraints; failure must be explicit rather than quietly treated
   as success.
5. Distinguish duplicated knowledge from coincidental text. Reduce coupling only where
   two sites must change together, and preserve independently changing behaviour.
6. Propose the smallest safe change, its behavioural verification, residual risk, and
   the operator-confirmation point before any write-impacting refactor.

## Output

Report the affected unit, concrete complexity symptoms, knowledge owner, interface and
error-path evidence, minimal proposed change, verification needed, and any scope that
belongs to a sibling module.
