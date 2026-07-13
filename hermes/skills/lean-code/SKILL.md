---
name: lean-code
description: "Apply on-demand minimalism to select the smallest complete, verified code change without weakening safety, accessibility, or required behaviour."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/lean-code/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Lean Code

Source: `AnastasiyaW/claude-code-config/skills/lean-code/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Lean Code

Use this module on demand when an implementation risks unnecessary abstraction,
boilerplate, dependencies, or speculative scope. It complements the always-on
`code-quality` baseline: `code-quality` defines the normal correctness and safety
standard, while this module intensifies the search for the smallest complete solution.
It is not a general defect-finding or merge-approval procedure.

## Minimalism protocol

1. **Confirm the required behaviour.** Read the task, surrounding code, public
   contract, and relevant constraints before removing anything. Minimal means less
   unnecessary surface area, not fewer required branches or outcomes.
2. **Choose the smallest adequate building block.** Prefer an existing project
   capability, standard library feature, native platform feature, or established
   dependency before adding a new abstraction or package. Stop when one option fully
   satisfies the actual requirement.
3. **Remove speculative structure.** Avoid a framework, configuration layer, factory,
   wrapper, or extension point that has no current use. Keep names and control flow
   direct enough that the next maintainer can verify the intent.
4. **Protect load-bearing work.** Do not simplify away input validation at trust
   boundaries, error handling that prevents data loss, security controls,
   accessibility, required compatibility, calibration for real systems, or behaviour
   the operator explicitly requested. Lean is not incomplete.
5. **Mark a deliberate ceiling.** Where a small solution has a known future limit,
   record a nearby `simplification:` note with the observed ceiling and a concrete
   upgrade path. Do not invent a threshold as runtime policy.
6. **Verify the result.** Non-trivial logic needs the smallest runnable check that
   could expose a regression. Inspect the diff and use the normal project verification
   path; minimalism never authorises skipped testing or unreviewed shortcuts.

## Intensity

- **Lite:** implement the requested solution and briefly identify a simpler viable
  alternative for the operator to consider.
- **Full (default):** apply the protocol and prefer the shortest maintainable complete
  diff.
- **Ultra:** challenge optional scope explicitly, but still implement every accepted
  requirement and preserve all load-bearing safeguards.

## Output

Present the code or proposed diff first. Then state the complexity avoided, any
intentional simplification and its upgrade path, why required behaviour remains
complete, and the verification evidence. For routine quality or broader review, use
the Hermes-native `code-quality` module.
