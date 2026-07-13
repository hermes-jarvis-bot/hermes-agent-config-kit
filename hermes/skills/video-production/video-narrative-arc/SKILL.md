---
name: video-narrative-arc
description: "Prepare a product-video narrative arc and timestamped beat plan from an approved product brief without rendering, publishing, or activating production tooling."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/video-production/video-narrative-arc/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Video Narrative Arc

Source: `AnastasiyaW/claude-code-config/skills/video-production/video-narrative-arc/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Video Narrative Arc

Use this module to prepare a structured, timestamped narrative arc for a product video, advert, launch, pitch, or short-form social asset. It converts an approved product brief into a beat plan; it does not invent unverified product claims, contact customers, modify scene code, render media, publish content, or activate production tooling.

## Read-only preflight

1. Confirm the supplied product brief, intended audience, platform, duration, call to action, and evidence available for claims, proof points, and customer language.
2. Separate confirmed facts from assumptions. If the brief, audience, proof, or approval boundary is missing, request it rather than manufacturing a story.
3. Choose the smallest suitable format: 10–15 seconds for a pattern interrupt, 15–20 seconds for problem–solution, 30 seconds for a demo, 45–60 seconds for a launch or explainer, and 60–90 seconds for a fuller story.

## Narrative protocol

1. Start with the audience's concrete problem, contrast, or relevant surprise; do not begin with a logo or decorative introduction.
2. State the tension, show the credible mechanism or demonstration, then use only verified proof such as approved metrics, customer-permissioned quotations, or documented limitations.
3. Give each beat a timestamp, audience emotion, visual intent, on-screen text, narration or dialogue, evidence source, and the intended next action.
4. Limit on-screen text to what can be read comfortably. Use plain, specific customer language rather than generic superlatives.
5. Alternate faster problem, demonstration, or proof beats with enough slower time for the key reveal or emotional transition to remain legible.
6. End with a specific, low-friction call to action that matches the approved offer and destination. Do not invent offers, prices, URLs, or availability claims.

## Template choices

- **Pattern interrupt (10–15s):** relevant surprise → possibility → concise call to action.
- **Problem–solution flash (15–20s):** customer pain → escalation → pivot → demonstrated mechanism → call to action.
- **Hook–pain–demo–proof–CTA (30s):** supportable hook → concrete pain → demonstration → evidence → call to action.
- **Launch or explainer (45–60s):** current reality → vision → gradual solution reveal → strongest proof → optional approved surprise → call to action.
- **Full story (60–90s):** a specific audience's world and breaking point → discovery and change → credible transformation and proof → the possible new world → call to action.

Treat these as adaptable patterns, not formulas. Prefer three clear, supported scenes to a longer sequence that hides the product meaning or overstates evidence.

## Output and hand-off

Report the brief boundary, selected template and rationale, timestamped beat table, claim/proof sources, unverified assumptions, accessibility and platform constraints, residual risks, and the next approval point. Use `product-meaning-extractor` to develop or revise a product brief, `script-evaluator` to assess an existing draft, and a separately approved production protocol for script rewriting, scene implementation, rendering, or publication.
