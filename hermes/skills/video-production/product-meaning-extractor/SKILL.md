---
name: product-meaning-extractor
description: "Prepare an evidence-bounded product brief from approved product material without browsing, contacting customers, publishing claims, or activating production tooling."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/video-production/product-meaning-extractor/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Product Meaning Extractor

Source: `AnastasiyaW/claude-code-config/skills/video-production/product-meaning-extractor/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Product Meaning Extractor

Use this module to turn approved product material into an evidence-bounded product brief for later review, writing, or video-planning work. It is a structured analysis protocol; it does not browse a product site, take screenshots, inspect CSS, contact customers, collect reviews, invent claims, write a script, modify scenes, render media, publish content, or activate production tooling.

## Read-only preflight

1. Confirm the approved source material, audience, intended use, product owner, and boundaries for any customer, market, or competitive information.
2. Separate supplied facts, permissioned quotations, and measured results from assumptions or missing evidence. Mark every gap as `needs data`; do not fill it with plausible marketing copy.
3. Record whether a claim, testimonial, visual signal, price, comparative statement, or customer phrase may be reused and where its approval or source can be checked.

## Meaning-extraction protocol

1. List each observed feature and apply the “So what?” test until it reaches a concrete customer outcome, cost avoided, capability gained, or emotional change. Preserve the evidence chain; do not turn an inference into a fact.
2. Identify the customer's functional, emotional, and social jobs, then state the specific problem or friction the product addresses.
3. Describe the before-and-after transformation as observed or explicitly inferred: situation, actions, constraints, and outcome. Flag uncertain language rather than overstating it.
4. State the mechanism only from approved technical or operational evidence. Distinguish a product capability from a promised outcome.
5. Rank proof points by strength: measured result with context, permissioned customer evidence, documented comparison, or `needs data`. Do not manufacture statistics, customer endorsements, alternatives, or competitive advantages.
6. Draft no more than three audience segments and a short language bank. Quote customer language only when it is supplied with an approved source; otherwise label it as an inference for review.

## Product brief output

Produce a concise brief with these headings:

- `## Core insight` — the customer-world tension, separate from a product slogan.
- `## Problem and enemy` — concrete observed friction and its evidence.
- `## Transformation` — before, after, confidence level, and unresolved assumptions.
- `## Mechanism` — supportable explanation of how the product addresses the problem.
- `## Proof points` — source, approval status, and qualification for every claim.
- `## Customer language` — quoted source material or clearly labelled inferences.
- `## Audience and positioning` — ranked segments, alternatives, unique attributes, and missing competitive evidence.
- `## Brand and delivery constraints` — only approved tone, visual, offer, platform, and accessibility information.
- `## Candidate angles` — optional hypotheses for a later approved narrative protocol, not finished copy or publication instructions.

## Review gates

- A core insight must describe a customer tension rather than repeat unsupported product positioning.
- A mechanism must explain the observed approach, not merely attach an unverified “AI-powered” claim.
- At least one proof point must be traceable; otherwise record the brief as incomplete rather than persuasive.
- Keep audience scope to three segments or fewer and identify the evidence for the ranking.
- Treat JTBD, StoryBrand, positioning, and value-proposition frameworks as prompts for analysis, not evidence that a claim is true.

## Reporting and hand-off

Report the supplied material, evidence and permission boundaries, brief, assumptions, missing data, claim-review queue, residual risks, and the next approval point. Use `video-narrative-arc` only after the brief and required claims are approved; use `script-evaluator` to assess an existing draft. Any browsing, customer outreach, copywriting, scene implementation, rendering, or publication requires a separate approved protocol.
