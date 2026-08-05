---
name: humanize-english
description: "Review and revise English-language prose for clarity, specificity, natural rhythm, and an appropriate human voice without fabricating facts or personal experience."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/writing/humanize-english/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Humanize English

Source: `AnastasiyaW/claude-code-config/skills/writing/humanize-english/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# English prose revision

Use this module to revise an English-language draft that sounds generic, over-formal,
formulaic, repetitive, or mechanically produced. It is an editorial protocol, not a
tool for concealing authorship or evading a publisher's disclosure, moderation, or
academic-integrity rules. Preserve the author's intended meaning, required facts, and
appropriate professional tone.

## Boundary and overlap

Use the installed `humanizer` module for its general cross-language scan of generic
AI-writing patterns. Use this module when English-specific idiom, register, and
sentence-level phrasing need focused attention. Do not combine their checklists
mechanically: a phrase is a revision candidate only when it weakens this particular
draft's clarity, accuracy, or voice.

This guidance does not publish text, modify a repository, create a false provenance
record, insert fabricated experience, or bypass an operator's review process.

## Read-only editorial pass

1. **Establish the brief.** Identify audience, publication context, intended register,
   facts that must remain exact, quotations, terminology, and any disclosure or style
   requirements. If the draft is a file, inspect it before proposing edits.
2. **Mark rather than ban.** Look for flat, uniform sentence rhythm (a run of
   similarly-timed sentences), maximally safe or hedge-heavy word choices, formulaic
   transitions and stock openings, symmetrical paragraphs or list items, and a missing
   personal stance or admitted uncertainty. These are prompts to review, not forbidden
   words — a transition or a measured claim can be correct when it improves precision.
3. **Prefer concrete English.** Name the actor, action, constraint, date, version, or
   observable result when the source supports it. Replace a vague quantifier with a
   specific number when the source has one. Preserve technical terminology when a
   casual synonym would reduce accuracy.
4. **Repair flow.** Vary sentence and paragraph length naturally, remove duplicated
   claims, and make the reasoning between paragraphs explicit. Do not add slang,
   deliberate errors, humour, or an informal first-person voice merely to simulate a
   person.
5. **Protect evidence.** Keep quotations, measurements, error messages, references,
   and uncertainty intact. Never invent a personal incident, a failed experiment, a
   number, a source, or an opinion to make prose feel authentic.
6. **Read back in context.** Check the revised English aloud or sentence by sentence
   for natural cadence, factual preservation, and fit for the intended audience. For a
   file change, present the proposed diff and obtain the required approval before
   writing it.

## Useful review prompts

- Does each paragraph add a distinct, supported claim?
- Is a hedge or a maximally safe phrase concealing a clearer, more specific point?
- Does a transition explain a real relationship, or merely delay the point?
- Does the sentence rhythm and word choice sound natural for the intended register?
- Are specificity, humour, informality, and first person supplied by the source and
  audience rather than manufactured by the editor?
- Could a reader distinguish verified facts, the author's view, and unresolved
  uncertainty?

## Output shape

Return a revised draft or a compact set of proposed edits, followed by: retained facts
and quotations, material stylistic changes, unresolved ambiguities, and any required
operator confirmation for a file or publication write. A natural voice is useful only
when it remains truthful.
