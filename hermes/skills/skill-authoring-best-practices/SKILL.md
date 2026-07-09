---
name: skill-authoring-best-practices
description: "Design, review, and maintain Hermes skills with strong triggers, clear procedures, gotchas, troubleshooting, and verified support files."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/08-skills-best-practices.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Skill Authoring Best Practices

Source: `AnastasiyaW/claude-code-config/principles/08-skills-best-practices.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Skill Authoring Best Practices

Upstream source policy was written for a different skill system. Hermes adaptation keeps the durable lessons: a useful module is discoverable, procedural, maintained, and verified.

## Principle

A skill is operational memory. It should make future work safer and faster, not merely archive prose. Good skills have:

- a trigger-rich description so the model selects them at the right time;
- concise procedural instructions for the common path;
- gotchas learned from real failures;
- troubleshooting organised by symptom, cause, and fix;
- support files only when they are reviewed and useful;
- verification evidence from at least one realistic use.

## Description as trigger

The description is not decoration. It is the model-selection trigger.

Use this shape:

```text
[What the skill does] + [when to use it / user phrases] + [key capabilities]
```

Prefer user-visible symptoms and nouns:

- `Use when GitHub Actions are failing, PR checks are queued, or a workflow did not publish a release`;
- `Use when Hermes skills, mappings, generated artefacts, or install/remove smoke tests need verification`.

Avoid vague descriptions such as `helps with development`.

## Required content

A Hermes skill should normally include:

- when to use it;
- prerequisites and required access;
- step-by-step protocol;
- verification checklist;
- gotchas / pitfalls;
- what not to do;
- reporting format or expected evidence.

Keep `SKILL.md` self-contained for common cases. Move bulky detail into linked support files when the platform supports them.

## Hermes support-file policy

For Hermes-managed skills, support files belong under reviewed subdirectories such as:

- `references/` for detailed documentation;
- `templates/` for reusable text/config templates;
- `scripts/` for reviewed helper scripts;
- `assets/` for static assets.

Do not create arbitrary files beside `SKILL.md`. Do not add executable scripts to a generated or ported skill unless they are separately reviewed, tested, and intentionally installed.

## Deterministic checks

When a step is mechanical and repeated, prefer a deterministic routine over a vague instruction. Examples:

- validator scripts for generated artefacts;
- dry-run/apply/remove smoke tests against disposable homes;
- link/path/count checks for documentation;
- CI read-back commands.

If a routine is too risky to run automatically, document it as a manual verification step and require operator confirmation before write-impacting actions.

## Lifecycle

Create a skill when a workflow has repeated value or a hard-won lesson. Update it when:

- the skill failed or missed a gotcha;
- a command, path, API, or permission changed;
- the description did not trigger when it should have;
- verification evidence shows the procedure is incomplete.

Retire or merge skills that become stale, redundant, or misleading.

## Review checklist

Before publishing or trusting a skill, check:

- description has specific trigger phrases;
- instructions are procedural rather than motivational;
- paths and commands are current;
- gotchas/troubleshooting reflect known failure modes;
- deterministic checks are scripted or otherwise explicit;
- support files stay inside approved subdirectories;
- no access credentials or environment-specific secrets are embedded;
- the skill was exercised or reviewed against a realistic task.

A stale skill is worse than no skill: it gives the agent confidence with a map from last year's terrain.
