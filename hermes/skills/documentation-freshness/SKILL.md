---
name: documentation-freshness
description: "Assess whether agent-facing project guidance remains current using bounded Git evidence, explicit adoption signals, and reviewable refresh decisions."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/agent-docs-freshness.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Documentation Freshness

Source: `AnastasiyaW/claude-code-config/rules/agent-docs-freshness.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Documentation Freshness

This module distinguishes documentation that exists from documentation that remains current. It provides a read-only review protocol for agent-facing project guidance. It does not create files, activate validators, install integrations, or schedule recurring checks.

## When to use

Use this module when a long-running repository has agent guidance, a knowledge base, layer notes, feature narratives, or generated reference material and there is reason to suspect the implementation has moved ahead of it.

Use `documentation-integrity` for path, command, link, and generated-output correctness. Use this module for the separate question: has relevant project change accumulated since the documentation was last intentionally refreshed?

## Read-only freshness protocol

1. Identify the documentation anchor and its owner. Prefer a project guidance file, a layer index, a knowledge-base entry point, or a documented generated-output manifest.
2. Verify that the anchor is intentionally part of the project; do not treat an arbitrary markdown file as required documentation.
3. Inspect the most recent commit touching the anchor and the commits since it using Git history.
4. Classify intervening changes by relevance: documentation-only, implementation change, interface/configuration change, operational change, or unrelated work.
5. Inspect a small representative sample of relevant diffs and compare their claims with the anchor.
6. Record one outcome: current, refresh recommended, insufficient evidence, or no adopted documentation surface.

Commit distance is a signal, not a verdict. A large count of unrelated commits does not prove drift; a single interface change can make an otherwise recent document stale.

## Adoption boundary

Documentation freshness checks should be opt-in through an explicit project convention: a named guidance path, a documented knowledge-base root, a maintained layer tree, or a repository-specific validation command.

Do not impose a documentation requirement on every small repository. A lightweight project may need only a concise README and current local context. A long-running project earns stronger freshness review when its complexity, collaboration, or operational risk makes stale guidance costly.

If a repository declares durable project tracking but has no stated documentation surface, report the gap and propose a small manual adoption step. Do not create a tree, run generation, or add enforcement without operator confirmation.

## Safe response to suspected drift

1. Gather evidence before editing: changed paths, interfaces, commands, generated outputs, and any affected guidance sections.
2. Propose the smallest refresh that restores accurate navigation and operational safety.
3. Keep implementation truth in source control, manifests, tests, and telemetry; documentation summarises and points to those sources.
4. Treat generated reference material as reviewable output, not authoritative truth.
5. Obtain operator confirmation before write-impacting documentation changes under the project's policy.
6. After an approved refresh, validate referenced paths, commands, counts, and consumer-facing instructions with `documentation-integrity`.

## Avoid

- Treating an age threshold as an automatic failure.
- Blocking work or session completion solely because documentation is old.
- Automatically generating documentation or spending external-provider budget to refresh it.
- Treating a document-presence check as proof that the document is correct or current.
- Adding active enforcement, background automation, or repository configuration as part of this guidance.

## Reporting

Report the documentation anchor, Git evidence reviewed, relevant change categories, freshness outcome, proposed refresh scope, and any operator-confirmation point. State clearly when the evidence is only suggestive.

Useful output is a bounded, evidence-based maintenance decision, not a ceremonial document-age score.
