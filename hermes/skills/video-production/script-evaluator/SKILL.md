---
name: script-evaluator
description: "Evaluate an existing video script, storyboard, presentation, or rendered scene for tension, specificity, emotional arc, hook, customer voice, and visual variety without producing, publishing, or rendering video assets."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/video-production/script-evaluator/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Script Evaluator

Source: `AnastasiyaW/claude-code-config/skills/video-production/script-evaluator/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Script Evaluator

Use this module to review an existing video script, presentation, storyboard, rendered scene, or scene-code excerpt for flatness and audience impact. It produces an evidence-based critique; it does not generate a replacement script, change scene code, render media, publish content, contact customers, or activate production tooling.

## Read-only preflight

1. Identify the supplied artefact, intended audience, format, duration, product or message constraints, and whether the review concerns a draft, storyboard, code excerpt, or finished video.
2. Separate observed material from missing context. Do not invent customer claims, statistics, visual details, or audience reactions.
3. State the review boundary and any unavailable evidence, such as runtime pacing, sound, final editing, or customer research.

## Six-dimension review

Score each dimension from 1 to 10 and cite the specific scene, line, or visual evidence supporting the score.

1. **Tension:** Is there a concrete problem, contrast, or before-to-after stake that gives the viewer a reason to care?
2. **Specificity:** Are claims supported by a measurable detail, example, demonstration, or named limitation rather than generic superlatives?
3. **Emotional arc:** Does the sequence move through meaningful beats, including a problem or tension point and a credible resolution?
4. **Hook strength:** Do the opening seconds create relevant curiosity or urgency without relying on an unexplained logo or decorative introduction?
5. **Customer voice:** Does the language remain direct, concrete, and appropriate to the audience rather than sounding like unsupported marketing copy?
6. **Visual variety:** Do scene type, pacing, layout, and emphasis change deliberately so the key moment is legible and distinct?

## Scoring and prioritisation

Record the six scores, total out of 60, the lowest-scoring dimension, and a bounded verdict:

- **50–60:** strong; retain the observed strengths and make only targeted refinements.
- **40–49:** sound foundation; correct the concrete weak points before finalisation.
- **30–39:** revision recommended; rebuild the weakest narrative or evidence elements first.
- **Below 30:** the current artefact lacks a reliable basis for incremental polishing; request an approved brief or a separate narrative-design protocol.

A high total does not cancel a critical weakness. Prioritise the lowest dimension where it undermines comprehension, credibility, or the audience's reason to continue.

## Common review patterns

- **Feature parade:** features appear as a list with no prior problem or question. Recommend a specific audience need before the feature evidence.
- **Logo-first opening:** branding arrives before relevance. Recommend an evidence-based hook, then place identity where it supports recognition.
- **Generic superlatives:** claims such as "best" or "world-class" carry no proof. Recommend a verifiable fact, example, or qualified limitation.
- **Missing middle:** a workable opening and call to action surround an undifferentiated demonstration. Identify the single strongest proof point and make its role clear.
- **Uniform energy:** every scene uses the same pacing or treatment. Recommend contrast that matches the intended emotional beat without sacrificing clarity.

## Reporting and boundaries

Report the artefact and audience boundary, each score with cited evidence, highest-impact weaknesses, concrete revision suggestions, missing evidence, and the next approval point. Treat customer reviews and performance claims as source material to verify, not text to copy without permission. Use a separate approved writing or production protocol for any rewrite, scene implementation, render, or publication.
