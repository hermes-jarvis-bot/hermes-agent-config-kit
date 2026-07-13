---
name: article-structure-review
description: "Review a completed article's macro-structure, evidence balance, genre fit, stated limitations, section load, and appropriate use of visuals without rewriting prose or publishing content."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/writing/article-structure-review/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Article Structure Review

Source: `AnastasiyaW/claude-code-config/skills/writing/article-structure-review/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Article structure review

Use this module after a complete draft exists and before sentence-level editing or
publication. It is a read-only editorial protocol for macro-structure: the relation
between claims and their support, genre and reader expectations, declared limitations,
section load, and whether a visual would communicate structure more clearly than prose.

## Boundary and overlap

Use `humanize-russian` for Russian-language phrasing, register, cadence, and factual
preservation. Use the installed `humanizer` module for a general scan of generic
AI-writing patterns. This module does not prescribe wording, simulate a human voice,
conceal authorship, invent evidence, or bypass publication, disclosure, or editorial
review requirements.

Treat numerical ratios and paragraph-count heuristics as optional diagnostic signals,
not publication gates. A claim may be supported by a concrete example, a sourced
fact, a reproducible method, a clearly bounded case, or an explicit uncertainty; the
appropriate balance depends on the article's genre and audience.

## Read-only review protocol

1. **Set the editorial brief.** Identify the intended audience, primary genre,
   publication context, central question, factual constraints, and any required
   disclosure. If the article is stored in a file, inspect it before proposing changes.
2. **Check claim and support balance.** For each major section, mark its important
   claims and the evidence or reasoning that supports them. Flag unsupported assertions,
   evidence that arrives too late, and sections that accumulate conclusions without
   showing how the reader can assess them. Propose the smallest repair: qualify a
   claim, add available evidence, move support nearer to the claim, or narrow scope.
3. **Check genre and narrative contract.** Confirm that the title, opening, section
   sequence, and conclusion serve one primary genre such as analysis, tutorial,
   reference, opinion, or experience report. A deliberate genre shift is acceptable
   when it is signposted and has a clear purpose; an accidental one should be clarified
   or separated.
4. **Make limitations visible.** For articles that present a tool, approach, result,
   or recommendation, locate where assumptions, trade-offs, untested conditions, and
   known failure modes are stated. Recommend a bounded limitations section when their
   absence could cause readers to overgeneralise. Do not manufacture caveats or
   personal experience that the author cannot support.
5. **Review section load.** Compare the conceptual load of opening, middle, and final
   sections. Flag a dense section that introduces many new ideas without transitions,
   examples, or staging. Suggest splitting, reordering, summarising, or moving detail
   to a separately scoped article only when it improves the reader's path.
6. **Choose visual or prose deliberately.** When a section explains relationships,
   hierarchy, architecture, comparison, categories, or a timeline, ask whether a
   table, diagram, or other visual would make the structure clearer. Use prose for
   reasoning, sequence, nuance, and narrative. A visual is a proposal, not a required
   deliverable.
7. **Read back the structure.** Read the title, opening, headings, first paragraphs,
   transitions, and conclusion as a reader would. Record the supported thesis, genre,
   limitations, structural risks, and proposed edits separately from any actual write.

## Output shape

Return a compact structural review with: editorial brief; claim/support observations;
genre and reader-path assessment; limitations and uncertainty; section-load and
visual/prose recommendations; retained facts; and any operator confirmation required
before changing a file or publishing. Preserve the author's evidence and make the
scope of uncertainty visible rather than polishing it away.
