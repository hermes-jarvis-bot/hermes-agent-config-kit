---
name: anti-pattern-as-config
description: "Encode recurring failure modes as explicit negative rules with exceptions, alternatives, and optional deterministic detectors."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/23-anti-pattern-as-config.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Anti Pattern As Config

Source: `AnastasiyaW/claude-code-config/principles/23-anti-pattern-as-config.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Anti-Pattern as Config

Upstream source policy describes preventing repeated model defaults by making negative patterns explicit. Hermes adaptation keeps the anti-attractor protocol and rule structure, but does not install command wrappers, detectors, CI, browser automation, or third-party design tooling. Any detector is a separate reviewed implementation.

## Principle

When a task has a recurring bad default, positive guidance is not enough. Encode the failure mode as an explicit negative rule with exceptions and alternatives.

Use this module when:

- an agent repeatedly chooses the same generic design, naming, architecture, copy, or implementation pattern;
- a project has known foot-guns that are easy to detect;
- review findings keep rediscovering the same avoidable default;
- a domain needs a small negative checklist before generation or review.

Do not use it for subjective taste preferences, one-off disagreements, or broad rules that cannot be checked or explained.

## Anti-attractor protocol

Before committing to a visible or structural choice:

1. **Name the reflex default.** State the first obvious choice the model is likely to make.
2. **Check it against the negative rules.** If the default matches a rule, reject it and cite the rule ID.
3. **Enumerate alternatives.** List at least three viable alternatives when the choice matters.
4. **Pick with context.** Choose one alternative and explain why it fits this project, not just why it is different.
5. **Verify when possible.** If the rule has a deterministic check, run it and preserve the output.

This prevents the common failure where the first default is rejected and the second default quietly replaces it.

## Rule shape

A useful anti-pattern rule has four parts:

```markdown
### AP-NAME-001: Avoid vague helper names

**Pattern:** New symbols named `Utils`, `Helper`, `Manager`, `Thing`, `getData`, or `handleClick` without domain-specific context.

**Why:** Generic names hide responsibility and make future maintenance harder.

**Exceptions:** Temporary spike code; framework-mandated handler names; existing public API compatibility.

**Alternatives:** Name the domain action or owned resource, for example `loadInvoiceRows`, `syncDevicePeers`, or `renderStatusCard`.
```

Required properties:

- stable rule ID;
- concrete pattern that a human or script can recognise;
- short reason;
- explicit exceptions;
- suggested alternatives.

Without exceptions, the rule becomes dogma. Without alternatives, it becomes a complaint.

## Enforcement layers

Prefer the lightest useful layer:

1. **Generation-time reference.** Keep the negative rules in a repo-local markdown file and load them before relevant work.
2. **Review checklist.** Use the rules during code/design/copy review and report rule IDs for findings.
3. **Optional deterministic detector.** Add a grep, linter, static check, visual check, or test only when the pattern is concrete enough and false positives are manageable.

Do not add automation merely because a rule exists. Automation that reports noise trains everyone to ignore the protocol.

## Good candidate domains

- UI/design defaults: generic typefaces, low-contrast text, decorative gradients, nested-card layouts.
- Copywriting: stock phrases, inflated claims, vague calls to action.
- Code naming: vague helpers, generic managers, misleading abstractions.
- Architecture: premature microservices, unnecessary queues, databases for tiny static state.
- Security: known unsafe patterns with clear markers.
- Data access: `SELECT *`, N+1 queries, missing transaction boundaries.
- Dockerfiles and CI: floating tags, root containers, cache-busting copy order, unpinned remote scripts.
- Tests: no assertions, skipped checks without reason, mocks that replace the behaviour under test.

## Relationship to other modules

- Use `code-quality` to choose the minimum correct implementation.
- Use this module to prevent recurring bad defaults while making that choice.
- Use `knowledge-base-enforcement` when an accepted anti-pattern should become a durable project invariant.
- Use `documentation-integrity` to ensure rule files, detectors, and referenced commands stay true.
- Use `visual-context-pattern` when design anti-patterns need side-by-side visual evidence.

## Detector discipline

If adding a detector later:

- run it locally before adding it to CI;
- document what it checks and what it deliberately ignores;
- include rule IDs in output;
- classify severity so low-value findings do not drown important ones;
- tune false positives aggressively;
- provide an explicit exception mechanism;
- keep the detector read-only unless the operator approves autofix behaviour.

A detector is evidence, not authority. If it disagrees with project context, update the rule or exception instead of blindly obeying it.

## Gotchas

- Negative lists drift stale faster than positive guides. Keep the reason and retirement condition visible.
- Stable IDs matter. Treat rule IDs like public API once referenced by docs, tests, or reports.
- Rules must be concrete enough to check. “Be tasteful” is not a rule; “avoid new `Manager` suffixes unless matching an existing public API” is.
- Too many low-value rules create compliance theatre. Start with five to ten recurring failures.
- Do not encode personal taste as project policy unless the operator explicitly wants that style constraint.

## Reporting format

When using this module, report:

- anti-pattern rule file or rule IDs consulted;
- reflex default identified;
- rejected anti-patterns;
- alternatives considered;
- chosen option and rationale;
- detector command/output, if any;
- exceptions accepted and why.

The point is not to make the agent more negative. It is to stop it walking into the same tastefully labelled hole.
