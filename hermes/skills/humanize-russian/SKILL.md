---
name: humanize-russian
description: "Review and revise Russian-language prose for clarity, specificity, natural rhythm, and an appropriate human voice without fabricating facts or personal experience."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/writing/humanize-russian/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Humanize Russian

Source: `AnastasiyaW/claude-code-config/skills/writing/humanize-russian/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Russian prose revision

Use this module to revise a Russian-language draft that sounds generic, over-formal,
translated, repetitive, or mechanically produced. It is an editorial protocol, not a
tool for concealing authorship or evading a publisher's disclosure, moderation, or
academic-integrity rules. Preserve the author's intended meaning, required facts, and
appropriate professional tone.

## Boundary and overlap

Use the installed `humanizer` module for its general cross-language scan of generic
AI-writing patterns. Use this module when Russian grammar, word order, register, and
Russian-language phrasing need focused attention. Do not combine their checklists
mechanically: a phrase is a revision candidate only when it weakens this particular
draft's clarity, accuracy, or voice.

This guidance does not publish text, modify a repository, create a false provenance
record, insert fabricated experience, or bypass an operator's review process.

## Read-only editorial pass

1. **Establish the brief.** Identify audience, publication context, intended register,
   facts that must remain exact, quotations, terminology, and any disclosure or style
   requirements. If the draft is a file, inspect it before proposing edits.
2. **Mark rather than ban.** Look for abstractions that hide the actor or result,
   chained verbal nouns, formulaic introductions and conclusions, vague attribution,
   repetitive sentence rhythm, and translated word order. These are prompts to review,
   not forbidden words: `является`, `позволяет`, and formal connectors can be correct
   when they improve precision.
3. **Prefer concrete Russian.** Name the actor, action, constraint, date, version, or
   observable result when the source supports it. Replace bureaucratic constructions
   with direct verbs where meaning and register allow. Preserve technical terminology
   when a casual synonym would reduce accuracy.
4. **Repair flow.** Vary sentence and paragraph length naturally, remove duplicated
   claims, and make the reasoning between paragraphs explicit. Do not add slang,
   deliberate grammar mistakes, humour, or an informal first-person voice merely to
   simulate a person.
5. **Protect evidence.** Keep quotations, measurements, error messages, references,
   and uncertainty intact. Never invent a personal incident, a failed experiment,
   a number, a source, or an opinion to make prose feel authentic.
6. **Read back in context.** Check the revised Russian aloud or sentence by sentence
   for natural cadence, factual preservation, and fit for the intended audience. For a
   file change, present the proposed diff and obtain the required approval before
   writing it.

## Useful review prompts

- Does each paragraph add a distinct, supported claim?
- Is an abstract noun concealing a clearer action and actor?
- Does a connector explain a real relationship, or merely delay the point?
- Does the word order sound native for the intended register?
- Are specificity, humour, informality, and first person supplied by the source and
  audience rather than manufactured by the editor?
- Could a reader distinguish verified facts, the author's view, and unresolved
  uncertainty?

## Output shape

Return a revised draft or a compact set of proposed edits, followed by: retained facts
and quotations, material stylistic changes, unresolved ambiguities, and any required
operator confirmation for a file or publication write. A natural voice is useful only
when it remains truthful.
