# Porting backlog and handoff

This document records what the `v0.1.0` Hermes Agent Config Kit deliberately did **not** port from `AnastasiyaW/claude-code-config`, why it stayed out, and how future work should approach it.

It is the planning and handoff companion to:

- `README.md` — project overview;
- `SECURITY.md` — trust and quarantine policy;
- `INSTALL.md` — clean-room install/remove protocol;
- `AGENTS.md` — agent operating guide;
- `mappings/compatibility.yaml` — machine-readable conversion policy.

## Snapshot baseline

Current baseline is the upstream snapshot pinned in `upstream.lock.json`.

Inventory from the current `upstream/claude-code-config/snapshot/`. Counts are
rechecked against the pinned snapshot when this table changes.

| Area | Files in snapshot | Auto-ported in MVP | Left out |
| --- | ---: | ---: | ---: |
| Root docs/config | 10 | 0 | 10 |
| `.claude-plugin/` | 1 | 0 | 1 |
| `.github/` | 1 | 0 | 1 |
| `agents/` | 6 | 0 | 6 |
| `alternatives/` | 19 | 0 | 19 |
| `docs/` | 4 | 0 | 4 |
| `evals/` | 2 | 0 | 2 |
| `hooks/` | 44 | 0 | 44 |
| `principles/` | 30 | 30 | 0 |
| `references/` | 1 | 0 | 1 |
| `rules/` | 30 | 28 | 2 |
| `scripts/` | 35 | 0 | 35 |
| `skills/` | 159 | 98 | 61 |
| `templates/` | 47 | 13 | 34 |
| `workflows/` | 5 | 0 | 5 |
| **Total** | **394** | **178** | **216** |

## Ported so far

The adapter intentionally auto-converts only selected markdown-only material into Hermes skills:

| Upstream source | Hermes target |
| --- | --- |
| `skills/ai-ml/ml-research-lab/SKILL.md` | `hermes/skills/ai-ml/ml-research-lab/SKILL.md` |
| `skills/ai-ml/flux2-lora-training/SKILL.md` | `hermes/skills/ai-ml/flux2-lora-training/SKILL.md` |
| `skills/ai-ml/diffusion-engineering/SKILL.md` | `hermes/skills/ai-ml/diffusion-engineering/SKILL.md` |
| `skills/ai-ml/diffusion-engineering/references/architectures.md` | `hermes/skills/ai-ml/diffusion-engineering/references/architectures.md` |
| `skills/ai-ml/diffusion-engineering/references/encoders-data.md` | `hermes/skills/ai-ml/diffusion-engineering/references/encoders-data.md` |
| `skills/ai-ml/diffusion-engineering/references/eval-debug.md` | `hermes/skills/ai-ml/diffusion-engineering/references/eval-debug.md` |
| `skills/ai-ml/diffusion-engineering/references/memory.md` | `hermes/skills/ai-ml/diffusion-engineering/references/memory.md` |
| `skills/ai-ml/diffusion-engineering/references/samplers.md` | `hermes/skills/ai-ml/diffusion-engineering/references/samplers.md` |
| `skills/ai-ml/diffusion-engineering/references/training.md` | `hermes/skills/ai-ml/diffusion-engineering/references/training.md` |
| `skills/video-production/remotion-production-guide/SKILL.md` | `hermes/skills/video-production/remotion-production-guide/SKILL.md` |
| `skills/video-production/video-post-production/SKILL.md` | `hermes/skills/video-production/video-post-production/SKILL.md` |
| `skills/video-production/script-evaluator/SKILL.md` | `hermes/skills/video-production/script-evaluator/SKILL.md` |
| `skills/video-production/video-narrative-arc/SKILL.md` | `hermes/skills/video-production/video-narrative-arc/SKILL.md` |
| `skills/video-production/product-meaning-extractor/SKILL.md` | `hermes/skills/video-production/product-meaning-extractor/SKILL.md` |
| `skills/ai-ml/vlm-segmentation/SKILL.md` | `hermes/skills/ai-ml/vlm-segmentation/SKILL.md` |
| `skills/ai-ml/vlm-segmentation/references/diffusion-engineering.md` | `hermes/skills/ai-ml/vlm-segmentation/references/diffusion-engineering.md` |
| `skills/ai-ml/vlm-segmentation/references/gpu-deployment.md` | `hermes/skills/ai-ml/vlm-segmentation/references/gpu-deployment.md` |
| `skills/ai-ml/vlm-segmentation/references/vlm-segmentation.md` | `hermes/skills/ai-ml/vlm-segmentation/references/vlm-segmentation.md` |
| `skills/ios/ios-development/SKILL.md` | `hermes/skills/ios/ios-development/SKILL.md` |
| `skills/ios/ios-development/references/architecture.md` | `hermes/skills/ios/ios-development/references/architecture.md` |
| `skills/ios/ios-development/references/data.md` | `hermes/skills/ios/ios-development/references/data.md` |
| `skills/ios/ios-development/references/metal-graphics.md` | `hermes/skills/ios/ios-development/references/metal-graphics.md` |
| `skills/ios/ios-development/references/navigation.md` | `hermes/skills/ios/ios-development/references/navigation.md` |
| `skills/ios/ios-development/references/networking.md` | `hermes/skills/ios/ios-development/references/networking.md` |
| `skills/ios/ios-development/references/performance.md` | `hermes/skills/ios/ios-development/references/performance.md` |
| `skills/ios/ios-development/references/swiftui.md` | `hermes/skills/ios/ios-development/references/swiftui.md` |
| `skills/ios/ios-development/references/uikit.md` | `hermes/skills/ios/ios-development/references/uikit.md` |
| `skills/development/deep-review/SKILL.md` | `hermes/skills/deep-review/SKILL.md` |
| `skills/development/repo-map/SKILL.md` | `hermes/skills/repo-map/SKILL.md` |
| `skills/development/workflow-orchestration/SKILL.md` | `hermes/skills/workflow-orchestration/SKILL.md` |
| `skills/writing/humanize-russian/SKILL.md` | `hermes/skills/humanize-russian/SKILL.md` |
| `skills/writing/article-structure-review/SKILL.md` | `hermes/skills/article-structure-review/SKILL.md` |
| `skills/lean-code/SKILL.md` | `hermes/skills/lean-code/SKILL.md` |
| `skills/plan-to-tickets/SKILL.md` | `hermes/skills/plan-to-tickets/SKILL.md` |
| `skills/agent-harness-design/SKILL.md` | `hermes/skills/agent-harness-design/SKILL.md` |
| `skills/frontend/frontend-design/SKILL.md` | `hermes/skills/frontend/frontend-design/SKILL.md` |
| `skills/frontend/frontend-design/references/components-frameworks.md` | `hermes/skills/frontend/frontend-design/references/components-frameworks.md` |
| `skills/frontend/frontend-design/references/layout-css.md` | `hermes/skills/frontend/frontend-design/references/layout-css.md` |
| `skills/frontend/frontend-design/references/performance-a11y.md` | `hermes/skills/frontend/frontend-design/references/performance-a11y.md` |
| `skills/frontend/frontend-design/references/visual-styles.md` | `hermes/skills/frontend/frontend-design/references/visual-styles.md` |
| `skills/development/proof-verify/SKILL.md` | `hermes/skills/proof-verify/SKILL.md` |
| `skills/operational/harness-audit/SKILL.md` | `hermes/skills/harness-audit/SKILL.md` |
| `skills/operational/harness-audit/references/checklist-per-subsystem.md` | `hermes/skills/harness-audit/references/checklist-per-subsystem.md` |
| `skills/operational/harness-audit/references/scoring-rubric.md` | `hermes/skills/harness-audit/references/scoring-rubric.md` |
| `skills/operational/cross-harness-continuation/SKILL.md` | `hermes/skills/cross-harness-continuation/SKILL.md` |
| `skills/operational/cross-harness-continuation/references/CONTINUITY.example.json` | `hermes/skills/cross-harness-continuation/references/continuity-contract-example.md` |
| `skills/operational/observability-monitoring/SKILL.md` | `hermes/skills/observability-monitoring/SKILL.md` |
| `skills/operational/observability-monitoring/references/source-notes.md` | `hermes/skills/observability-monitoring/references/source-notes.md` |
| `skills/development/architecture-first/` (13 reviewed markdown files) | `hermes/skills/architecture-first/` (flat package with Clean Architecture and domain-driven design references) |
| `skills/development/code-complexity/` (22 reviewed markdown files) | `hermes/skills/code-complexity/` (flat package with Clean Code, Pragmatic Programmer, and Software Design Philosophy references) |
| `skills/development/refactoring-safely/` (8 reviewed markdown files) | `hermes/skills/refactoring-safely/` (flat package with behaviour-preserving transformation references) |
| `skills/development/system-and-data-design/` (16 reviewed markdown files) | `hermes/skills/system-and-data-design/` (flat package with DDIA and System Design references) |
| `templates/proof-plan.md` | `hermes/templates/proof-plan.md` |
| `templates/agent-task/handoff.md` | `hermes/templates/agent-task-handoff.md` |
| `templates/agent-task/fix-log.md` | `hermes/templates/agent-task-fix-log.md` |
| `templates/agent-task/problems.md` | `hermes/templates/agent-task-problems.md` |
| `templates/agent-task/scratchpad.md` | `hermes/templates/agent-task-scratchpad.md` |
| `templates/agent-task/README.md` | `hermes/templates/agent-task-overview.md` |
| `templates/agent-task/evidence/README.md` | `hermes/templates/agent-task-evidence.md` |
| `templates/agent-task/state.json` | `hermes/templates/agent-task-state.md` |
| `templates/agent-task/trace.jsonl` | `hermes/templates/agent-task-trace.md` |
| `templates/agent-task/verdict.json` | `hermes/templates/agent-task-verdict.md` |
| `templates/long-run-project/PRD-BOOTSTRAP.md` | `hermes/templates/long-run-project-prd-bootstrap.md` |
| `templates/long-run-project/README.md` | `hermes/templates/long-run-project-overview.md` |
| `principles/01-harness-design.md` | `hermes/skills/harness-design/SKILL.md` |
| `principles/02-proof-loop.md` | `hermes/skills/proof-loop/SKILL.md` |
| `principles/03-autoresearch.md` | `hermes/skills/autoresearch/SKILL.md` |
| `principles/04-deterministic-orchestration.md` | `hermes/skills/deterministic-orchestration/SKILL.md` |
| `principles/05-structured-reasoning.md` | `hermes/skills/structured-reasoning/SKILL.md` |
| `principles/06-multi-agent-decomposition.md` | `hermes/skills/multi-agent-task-decomposition/SKILL.md` |
| `principles/07-codified-context.md` | `hermes/skills/codified-context/SKILL.md` |
| `principles/08-skills-best-practices.md` | `hermes/skills/skill-authoring-best-practices/SKILL.md` |
| `principles/09-supply-chain-defense.md` | `hermes/skills/supply-chain-defense/SKILL.md` |
| `principles/10-agent-security.md` | `hermes/skills/agent-security/SKILL.md` |
| `principles/11-documentation-integrity.md` | `hermes/skills/documentation-integrity/SKILL.md` |
| `principles/12-low-signal-residual-training.md` | `hermes/skills/low-signal-residual-training/SKILL.md` |
| `principles/13-research-pipeline.md` | `hermes/skills/research-intake/SKILL.md` |
| `principles/14-managed-agents.md` | `hermes/skills/managed-execution-boundaries/SKILL.md` |
| `principles/15-red-lines.md` | `hermes/skills/red-lines/SKILL.md` |
| `principles/16-project-chronicles.md` | `hermes/skills/project-chronicles/SKILL.md` |
| `principles/17-dbs-skill-creation.md` | `hermes/skills/dbs-skill-architecture/SKILL.md` |
| `principles/18-multi-session-coordination.md` | `hermes/skills/multi-session-coordination/SKILL.md` |
| `principles/19-inter-agent-communication.md` | `hermes/skills/inter-agent-communication/SKILL.md` |
| `principles/20-vulnerability-detection-pipeline.md` | `hermes/skills/vulnerability-detection-pipeline/SKILL.md` |
| `principles/21-knowledge-base-enforcement.md` | `hermes/skills/knowledge-base-enforcement/SKILL.md` |
| `principles/22-visual-context-pattern.md` | `hermes/skills/visual-context-pattern/SKILL.md` |
| `principles/23-anti-pattern-as-config.md` | `hermes/skills/anti-pattern-as-config/SKILL.md` |
| `principles/24-merge-conflict-resolution.md` | `hermes/skills/merge-conflict-resolution/SKILL.md` |
| `principles/25-coordination-primitives-mapping.md` | `hermes/skills/coordination-primitives-mapping/SKILL.md` |
| `principles/26-no-pre-existing-evasion.md` | `hermes/skills/no-pre-existing-evasion/SKILL.md` |
| `principles/27-feature-tracking.md` | `hermes/skills/long-run-feature-tracking/SKILL.md` |
| `principles/28-feature-layer-architecture.md` | `hermes/skills/feature-layer-architecture/SKILL.md` |
| `principles/29-mvp-agent-blueprint.md` | `hermes/skills/mvp-agent-blueprint/SKILL.md` |
| `principles/30-gates-that-cannot-bootstrap.md` | `hermes/skills/gates-that-cannot-bootstrap/SKILL.md` |
| `rules/activity-journal-and-state-registry.md` | `hermes/skills/activity-journal-and-state-registry/SKILL.md` |
| `rules/folder-lifecycle-labels.md` | `hermes/skills/folder-lifecycle-classification/SKILL.md` |
| `rules/file-organization-cohesion.md` | `hermes/skills/file-organization-cohesion/SKILL.md` |
| `rules/memory-maintenance.md` | `hermes/skills/durable-context-maintenance/SKILL.md` |
| `rules/edit-formats-and-tiering.md` | `hermes/skills/edit-formats-and-tiering/SKILL.md` |
| `rules/app-prelaunch-security-checklist.md` | `hermes/skills/app-prelaunch-security/SKILL.md` |
| `rules/autonomy-risk-tiers.md` | `hermes/skills/risk-tiered-autonomy/SKILL.md` |
| `rules/safety-billing.md` | `hermes/skills/billing-spend-controls/SKILL.md` |
| `rules/cross-harness-agents-md.md` | `hermes/skills/portable-project-context/SKILL.md` |
| `rules/agent-docs-freshness.md` | `hermes/skills/documentation-freshness/SKILL.md` |
| `rules/no-guessing.md` | `hermes/skills/no-guessing/SKILL.md` |
| `rules/verify-git-currency-first.md` | `hermes/skills/verify-git-currency-first/SKILL.md` |
| `rules/moa-gemini-delegation-eval.md` | `hermes/skills/moa-gemini-delegation-eval/SKILL.md` |
| `rules/finish-the-task.md` | `hermes/skills/finish-the-task/SKILL.md` |
| `rules/git-source-of-truth.md` | `hermes/skills/git-source-of-truth/SKILL.md` |
| `rules/quality-code.md` | `hermes/skills/code-quality/SKILL.md` |
| `rules/deletion-confirm-and-verify.md` | `hermes/skills/safe-deletion/SKILL.md` |
| `rules/secrets-as-data.md` | `hermes/skills/secrets-as-data/SKILL.md` |
| `rules/session-handoff.md` | `hermes/skills/session-handoff/SKILL.md` |
| `rules/silent-failure-detection.md` | `hermes/skills/silent-failure-detection/SKILL.md` |
| `rules/learn-from-corrections.md` | `hermes/skills/learning-from-corrections/SKILL.md` |
| `rules/system-verification-independent.md` | `hermes/skills/independent-verification/SKILL.md` |
| `rules/verify-at-consumer.md` | `hermes/skills/verify-at-consumer/SKILL.md` |
| `rules/api-utf8-posting.md` | `hermes/skills/api-utf8-posting/SKILL.md` |
| `rules/no-claude-attribution.md` | `hermes/skills/repository-attribution-hygiene/SKILL.md` |
| `rules/post-ui-change-review.md` | `hermes/skills/post-ui-change-review/SKILL.md` |
| `rules/quality-over-tokens-independent-verify.md` | `hermes/skills/quality-first-independent-review/SKILL.md` |
| `skills/ai-ml/notebooklm-grounded-research/SKILL.md` | `hermes/skills/ai-ml/notebooklm-grounded-research/SKILL.md` |
| `skills/ai-ml/notebooklm-grounded-research/references/workflow.md` | `hermes/skills/ai-ml/notebooklm-grounded-research/references/workflow.md` |
| `skills/development/distill-feedback/SKILL.md` | `hermes/skills/distill-feedback/SKILL.md` |
| `skills/operational/gemini-delegate/SKILL.md` | `hermes/skills/gemini-delegate/SKILL.md` |
| `skills/architecture/plan-swarm-review/SKILL.md` | `hermes/skills/architecture/plan-swarm-review/SKILL.md` |
| `skills/architecture/plan-swarm-review/references/vulnerability-kb.md` | `hermes/skills/architecture/plan-swarm-review/references/vulnerability-kb.md` |
| `skills/creative/pixel-art-studio/SKILL.md` | `hermes/skills/creative/pixel-art-studio/SKILL.md` |
| `skills/creative/pixel-art-studio/references/01-techniques.md` | `hermes/skills/creative/pixel-art-studio/references/01-techniques.md` |
| `skills/creative/pixel-art-studio/references/02-palette-theory.md` | `hermes/skills/creative/pixel-art-studio/references/02-palette-theory.md` |
| `skills/creative/pixel-art-studio/references/03-shading-materials.md` | `hermes/skills/creative/pixel-art-studio/references/03-shading-materials.md` |
| `skills/creative/pixel-art-studio/references/04-animation.md` | `hermes/skills/creative/pixel-art-studio/references/04-animation.md` |
| `skills/creative/pixel-art-studio/references/05-quality-rubric.md` | `hermes/skills/creative/pixel-art-studio/references/05-quality-rubric.md` |
| `skills/creative/pixel-art-studio/references/06-tools-and-libraries.md` | `hermes/skills/creative/pixel-art-studio/references/06-tools-and-libraries.md` |
| `skills/creative/pixel-art-studio/references/07-cultural-styles.md` | `hermes/skills/creative/pixel-art-studio/references/07-cultural-styles.md` |
| `skills/creative/pixel-art-studio/references/08-json-schema.md` | `hermes/skills/creative/pixel-art-studio/references/08-json-schema.md` |
| `skills/creative/pixel-art-storyboard/SKILL.md` | `hermes/skills/creative/pixel-art-storyboard/SKILL.md` |
| `skills/creative/pixel-art-storyboard/references/scene-description-framework.md` | `hermes/skills/creative/pixel-art-storyboard/references/scene-description-framework.md` |
| `skills/creative/pixel-art-storyboard/references/looped-animation-techniques.md` | `hermes/skills/creative/pixel-art-storyboard/references/looped-animation-techniques.md` |
| `skills/creative/pixel-art-storyboard/references/three-registers.md` | `hermes/skills/creative/pixel-art-storyboard/references/three-registers.md` |
| `skills/creative/pixel-art-storyboard/references/easing-curves.md` | `hermes/skills/creative/pixel-art-storyboard/references/easing-curves.md` |
| `skills/creative/pixel-art-storyboard/references/retouch-style-guide.md` | `hermes/skills/creative/pixel-art-storyboard/references/retouch-style-guide.md` |
| `skills/creative/pixel-art-storyboard/references/smoother-animation-baking.md` | `hermes/skills/creative/pixel-art-storyboard/references/smoother-animation-baking.md` |
| `skills/creative/pixel-art-storyboard/references/dataset-to-library-actionable.md` | `hermes/skills/creative/pixel-art-storyboard/references/dataset-to-library-actionable.md` |
| `skills/creative/pixel-art-storyboard/references/element-library-scaling-architecture.md` | `hermes/skills/creative/pixel-art-storyboard/references/element-library-scaling-architecture.md` |
| `skills/creative/pixel-art-storyboard/references/high-detail-pipeline.md` | `hermes/skills/creative/pixel-art-storyboard/references/high-detail-pipeline.md` |
| `skills/creative/pixel-art-storyboard/references/pinterest-to-library-pipeline.md` | `hermes/skills/creative/pixel-art-storyboard/references/pinterest-to-library-pipeline.md` |

These were chosen because they are broadly useful, markdown-centric, and can be adapted without executing upstream code or assuming Claude Code hook APIs.

`notebooklm-grounded-research` additionally ships one **reviewed-script-lane** artefact —
`skills/ai-ml/notebooklm-grounded-research/scripts/verify_notebooklm_setup.py`, ported to
`hermes/skills/ai-ml/notebooklm-grounded-research/scripts/verify_notebooklm_setup.py` under the
allowlist in `mappings/reviewed-scripts.yaml` (see `SECURITY.md` "Reviewed-script lane" and
`AGENTS.md`'s quarantine-policy section). This is the pilot for a new lane, not the markdown fast
lane: the script is stdlib-only, read-only, performs no network call, and was fully read by hand
before being added. It is deliberately absent from the `SUPPORTED` table above — it is governed
solely by the reviewed-script manifest and `validate_reviewed_scripts()`, never auto-converted.

## Why most upstream material stayed out

The omitted material falls into four broad buckets.

1. **Quarantine lane** — executable or runtime-affecting artefacts. These must never be copied into live Hermes behaviour automatically.
2. **Review lane** — useful markdown concepts that need Hermes-native adaptation, deduplication against existing Hermes skills, and human review.
3. **Domain-specific skill backlog** — complete upstream skill packages that may be valuable, but require packaging, support-file policy, and possible dependency review.
4. **Template/workflow backlog** — reusable project structures and JS workflows that need deliberate Hermes template/script/scheduled-protocol design.

## Quarantine lane: not ported

These artefacts are explicitly review-only. They are present in the upstream snapshot as data, not as executable authority.

### Claude plugin descriptor

- `.claude-plugin/plugin.json`

Reason: Claude Code plugin descriptors do not map directly to Hermes plugin loading. Future work requires a Hermes plugin design review, not a direct copy.

### GitHub workflow

- `.github/workflows/skills-lock-check.yml`

Reason: upstream CI can execute arbitrary commands. Adapter workflows must be authored locally and reviewed in this repository.

### Hooks

All upstream hooks remain unported:

- `hooks/activity-journal-guard.py`
- `hooks/api-key-leak-detector.py`
- `hooks/ask-question-guard.py`
- `hooks/backup-retention-cleanup.py`
- `hooks/claude-attribution-guard.py`
- `hooks/command-injection-guard.py`
- `hooks/conversation-history-capture.py`
- `hooks/coord-claim-guard.py`
- `hooks/cyrillic-bash-guard.py`
- `hooks/db-snapshot-guard.py`
- `hooks/destructive-command-guard.py`
- `hooks/directory-creation-guard.py`
- `hooks/docs-staleness-guard.py`
- `hooks/feature-list-validator.py`
- `hooks/feedback-pending-show.py`
- `hooks/file-cohesion-guard.py`
- `hooks/git-auto-backup.py`
- `hooks/git-destructive-guard.py`
- `hooks/handoff-closure-audit-guard.py`
- `hooks/handoff-resume-gate.py`
- `hooks/human-confirmation-guard.py`
- `hooks/kb-validate-gate.py`
- `hooks/keyword-skill-router.py`
- `hooks/long-run-detector.py`
- `hooks/over-engineering-advisor.py`
- `hooks/plan-gate.py`
- `hooks/pre-push-claude-attribution.py`
- `hooks/precompact-handoff-guard.py`
- `hooks/problems-md-validator.py`
- `hooks/safety_common.py`
- `hooks/secret-leak-guard.py`
- `hooks/self-harm-guard.py`
- `hooks/session-drift-validator.py`
- `hooks/session-feedback-capture.py`
- `hooks/session-handoff-check.py`
- `hooks/session-handoff-reminder.py`
- `hooks/stop-phrase-guard.py`
- `hooks/task-inbox-show.py`
- `hooks/test-gate-stop-hook.py`
- `hooks/test-muting-guard.py`
- `hooks/verify-deleted-guard.py`
- `hooks/README.md`

Reason: these are Python programs designed for Claude Code hook events. Hermes has different tool, approval, skill, cron, gateway, and plugin surfaces. Porting requires threat modelling and Hermes-native interfaces.

Recommended future treatment:

- Start with read-only catalogue generation.
- Classify each hook as one of:
  - already covered by Hermes core/approval layer;
  - skill guidance only;
  - candidate Hermes plugin/tool;
  - candidate validator script;
  - reject/no-port.
- Never install a hook as executable code from upstream without rewriting it under Hermes conventions.

### Scripts and evals

All upstream scripts and evals remain unported:

- `scripts/ace_context_merge.workflow.js`
- `scripts/build_hook_catalog.py`
- `scripts/cleanup_handoffs.py`
- `scripts/context_degradation.py`
- `scripts/cross_reference_check.py`
- `scripts/folder_lifecycle_audit.py`
- `scripts/gemini-switch.sh`
- `scripts/generate_skills_lock.py`
- `scripts/install_hooks.py`
- `scripts/kvcache_stats.py`
- `scripts/openscience_skill_inventory.py`
- `scripts/reasoning_metrics.py`
- `scripts/review_handoff_memory_loop.py`
- `scripts/skill_lint.py`
- `scripts/sync_public_config.py`
- `scripts/test_app_security_checklist.py`
- `scripts/test_conversation_history_capture.py`
- `scripts/test_directory_creation_guard.py`
- `scripts/test_openscience_skill_inventory.py`
- `scripts/test_review_handoff_memory_loop.py`
- `scripts/test_task_completion_hooks.py`
- `scripts/test_validate_agent_tickets.py`
- `scripts/validate_agent_tickets.py`
- `scripts/validate_config.py`
- `scripts/validate_kb_links.py`
- `scripts/verify_plugin_prerequisites.py`
- `evals/hooks/cases.json`
- `evals/hooks/run_hook_evals.py`

Reason: executable upstream code must remain data until reviewed. Some scripts may become useful validator routines, but should be rewritten or vendored deliberately with tests.

## Review lane: principles not yet ported

All upstream principles in the pinned snapshot have now been reviewed and ported as low- or medium-risk Hermes-native guidance. Further principle work should arrive through a deliberate upstream sync and fresh overlap review.

## Review lane: rules not yet ported

The following rules stayed out of MVP:


- `rules/long-run-harness.md`
- `rules/no-pre-existing-evasion.md`
- `rules/safety-hooks.md`

The remaining rules require separate review. `rules/long-run-harness.md` overlaps `long-run-feature-tracking`; `rules/no-pre-existing-evasion.md` needs a target-name and hook-link adaptation decision; `rules/safety-hooks.md` remains executable-adjacent and quarantined.

## Skill packages not yet ported

Upstream contains 123 skill-package files left out of MVP. Some are complete skills, some are support files, examples, scripts, templates, images, palettes, and references.

Top-level skill packages left out (this is a historical snapshot from early in the project and
has not been kept in sync with later domain-queue ports — `agent-harness-design`,
`diffusion-engineering`, `vlm-segmentation`, `distill-feedback`, `repo-map`, and
`humanize-russian` are confirmed already ported per the "Ported so far" table above and are
removed from this list; the remaining entries have not been re-checked this session):

- `skills/ai-ml/flux2-klein-prompting/`
- `skills/ai-ml/forensic-prompt-compiler/`
- `skills/architecture/feature-new/`
- `skills/architecture/harness-design/`
- `skills/architecture/layer-new/`
- `skills/development/proof-verify/references/kb-aware-verification.md` (reference remains separately reviewed and unported)
- `skills/development/workflow-orchestration/` (the markdown `SKILL.md` is ported; references, JavaScript template, and validation script remain unported and quarantined)
- `skills/writing/humanize-english/`

Special note: `skills/operational/harness-audit/SKILL.md`, its per-subsystem
evidence checklist, and its scoring rubric are ported as reviewed, data-only
guidance. They do not create files, run commands, configure integrations, or activate
guards. The rubric calibrates observed evidence without treating a named policy as
active enforcement.

Recommended future treatment:

- Do not bulk-copy upstream skill directories.
- For each candidate, decide whether it should be:
  - a Hermes local skill;
  - a support file under `references/`, `templates/`, `scripts/`, or `assets/`;
  - split across existing Hermes skills;
  - rejected as duplicate or out-of-scope.
- Pay special attention to support scripts and binary/media assets inside skill packages.

Next-candidate selection is governed by the **operator matrix in the autopilot run
prompt**, not by this list — do not designate a fast-lane "next" here that the matrix
has not blessed (doing so contradicts the matrix and blocks the autopilot). As of
2026-07-13 `skills/lean-code/`, `skills/plan-to-tickets/SKILL.md`, and the complete
five-file `skills/frontend/frontend-design/` package are ported. No remaining candidate
below is eligible for automatic porting without a new operator matrix decision.

- `skills/lean-code/SKILL.md` → `hermes/skills/lean-code/SKILL.md` — ported as the
  operator-approved Wave 3 markdown-only module. The Hermes adaptation retains the
  on-demand, complete-and-verified minimalism boundary and directs routine quality work
  to `code-quality`; no upstream tooling or runtime policy is carried over.
- `skills/writing/humanize-english/` — **manual-review-only**: detector-evasion
  framing, volatile word-ban lists, and overlap with the installed builtin
  `humanizer`. Product/policy decision required; not auto-port. (Mechanically it is a
  clean single-md conversion, but the framing is the blocker.)
- `skills/plan-to-tickets/SKILL.md` → `hermes/skills/plan-to-tickets/SKILL.md` —
  ported as the operator-approved Wave 3 markdown-only module. The Hermes adaptation
  retains project-relative ticket output and ticket-contract guidance, replaces the
  harness-specific validation command with project-applicable checks or an explicit
  manual-review gate, and positions the module as complementary to builtin `plan` /
  local `writing-plans`, not a duplicate.
- `skills/architecture/feature-new/`, `skills/architecture/layer-new/` — **not
  portable to Hermes (review-lane, not auto-port)**. Their substance depends on
  upstream-specific KB infrastructure Hermes does not have and cannot reproduce by
  adaptation: `docs/layers/<layer>/features/`, `feature_list.json`,
  `templates/kb-skeleton/`, `build_kb_graph.py`/`validate_kb_links.py`, ULTRAPACK, and
  `<claude-code-skills>` checkout paths (a pure conversion also fails the validator on
  the `claude-code-skills` reference). **General rule (2026-07-13):** any skill whose
  mechanics depend on concrete upstream artefacts/paths/tooling (kb-skeleton,
  docs/layers, feature_list.json, claude-code-skills/config checkout, kb-graph scripts)
  is not portable to Hermes-specifics — classify review-lane, do not auto-port.
- **Domain-skill scope applied (operator, 2026-07-13):** the agent-harness pool is
  exhausted; the approved five-file **`skills/frontend/frontend-design/`** package is
  ported to `hermes/skills/frontend/frontend-design/`, retaining the domain directory.
  `validate_output.py` now recursively validates nested `SKILL.md` and `references/*.md`
  paths, including frontmatter and harness-leak sweeps, so this package cannot bypass
  the validation boundary.
- `skills/architecture/harness-design/` — **not a candidate (duplicate)**: same
  Anthropic source, same core (Generator-Evaluator / Sprint-Contract / Context /
  Assumption / Quality) and the same `name: harness-design` as the already-ported
  `harness-design` (principle 01). Its unique operational bits are a manual merge
  decision, not an auto-port.
- **Domain queue (operator-approved 2026-07-13, all vetted clean on 4 axes; port in
  order, one per run, keep the `hermes/skills/<domain>/<skill>/` folder):**
  1. `skills/ai-ml/ml-research-lab/SKILL.md` → `hermes/skills/ai-ml/ml-research-lab/SKILL.md`
     — ported as a single-file, data-only ML experiment planning and review module; CUDA/ML
     content remains domain guidance, not tooling policy.
  2. `skills/video-production/script-evaluator/SKILL.md` →
     `hermes/skills/video-production/script-evaluator/SKILL.md` — ported as a single-file,
     data-only script review module; Remotion remains domain content and no production,
     rendering, or publication action is activated.
  3. `skills/ios/ios-development/` → `hermes/skills/ios/ios-development/` — ported as the
     complete 9-file markdown package (`SKILL.md` + 8 reviewed references); Swift/Xcode,
     Metal, and keychain constants remain domain reference material, and no signing,
     distribution, project-tooling, or runtime action is activated.
- **Domain queue #2 (operator-approved 2026-07-13, all vetted clean on 4 axes + leak
  sweep; port in order, one per run, keep the `hermes/skills/<domain>/<skill>/` folder):**
  1. `skills/video-production/video-narrative-arc/SKILL.md` →
     `hermes/skills/video-production/video-narrative-arc/SKILL.md` — ported as a single,
     data-only beat-planning module. Narrative templates remain adaptable guidance; no
     rendering, publication, customer contact, or production tooling is activated.
  2. `skills/video-production/product-meaning-extractor/SKILL.md` →
     `hermes/skills/video-production/product-meaning-extractor/SKILL.md` — ported as a
     single, data-only product-brief analysis module. Frameworks guide analysis only;
     browsing, customer contact, claims, and production actions remain separate approved work.
  3. `skills/ai-ml/vlm-segmentation/` → `hermes/skills/ai-ml/vlm-segmentation/` — ported as
     the complete four-file markdown package (`SKILL.md` + `references/` for diffusion
     engineering, GPU deployment, and VLM segmentation). The module is data-only design
     guidance: model acquisition, remote-code acceptance, GPU partitioning, workload launch,
     deployment, and spend remain separate approved protocols.
- **Domain queue #3 (operator-approved 2026-07-14; all vetted clean on 4 axes + leak
  sweep, md-only, no policy/infra/duplicate; port in order, one per run, keep the folder):**
  1. `skills/ai-ml/flux2-lora-training/SKILL.md` →
     `hermes/skills/ai-ml/flux2-lora-training/SKILL.md` — ported as a single-file,
     data-only LoRA/VAE training reference; ComfyUI/CUDA examples remain domain guidance
     and model acquisition, training, GPU changes, and spend require separate approval.
  2. `skills/video-production/remotion-production-guide/SKILL.md` →
     `hermes/skills/video-production/remotion-production-guide/SKILL.md` — ported as a
     single-file, data-only scene-planning and render-review module; Remotion/npm commands
     remain reference material, and dependency installation, project configuration, rendering,
     and publication require a separately approved protocol.
  3. `skills/video-production/video-post-production/SKILL.md` →
     `hermes/skills/video-production/video-post-production/SKILL.md` — single file; ffmpeg/npx how-to.
  4. `skills/ai-ml/diffusion-engineering/` → `hermes/skills/ai-ml/diffusion-engineering/` — 7-file
     package is ported as data-only design guidance (`SKILL.md` + 6 `references/`: architectures,
     encoders-data, eval-debug, memory, samplers, training). Model downloads, workload launch,
     GPU changes, deployment, and spend remain separate approved protocols.
- **Upstream sync before queue #4:** completed at `b293615` (2026-08-02); the snapshot and
  report are current. The report identifies 13 `manual-reapproval` sources with upstream
  changes; they remain separate operator re-review work and are not auto-accepted or ported.
- **Domain queue #4 (operator-approved 2026-08-02; all vetted clean on 4 axes + leak sweep +
  full-text read; port in order, one per run):**
  1. `principles/30-gates-that-cannot-bootstrap.md` → `hermes/skills/gates-that-cannot-bootstrap/SKILL.md`
     — ported as a single-file, Hermes-native design and verification module for opt-in gates
     that would otherwise stay silent where adoption is missing; it does not activate controls.
  2. `rules/verify-git-currency-first.md` → `hermes/skills/verify-git-currency-first/SKILL.md`
     — ported as a single-file, read-only Git-currency preflight module; it is an explicit
     specialization of the already-ported `no-guessing` (complementary, not a duplicate) and
     does not fetch, stash, reset, pull, deploy, or copy project trees automatically.
  3. `skills/operational/cross-harness-continuation/` → `hermes/skills/cross-harness-continuation/`
     — ported as a FLAT two-file package (`SKILL.md` + converted data-only
     `references/continuity-contract-example.md`); it governs the evidence-backed contract
     between agents and remains complementary to `session-handoff`, which covers session notes.
  4. `skills/operational/observability-monitoring/` → `hermes/skills/observability-monitoring/`
     — FLAT (same reason). Port `SKILL.md` + `references/source-notes.md` only;
     `agents/openai.yaml` is Codex-plugin manifest metadata (same class as
     `.claude-plugin/plugin.json`) and stays unported.
  5. `skills/development/architecture-first/` → `hermes/skills/architecture-first/` — ported as
     a FLAT 13-file markdown package (`SKILL.md` + 12 data-only Clean Architecture and
     domain-driven-design references). It decides code placement and dependency/domain boundaries;
     it explicitly excludes code-complexity, refactoring-safely, and system-and-data-design scope.
  6. `skills/development/code-complexity/` → `hermes/skills/code-complexity/` — ported as a
     FLAT 22-file markdown package (`SKILL.md` + 21 data-only Clean Code, Pragmatic Programmer,
     and Software Design Philosophy references). It decides local comprehensibility and explicitly
     excludes architecture-first, refactoring-safely, system-and-data-design, and lean-code scope.
  7. `skills/development/refactoring-safely/` → `hermes/skills/refactoring-safely/` — ported as
     a FLAT 8-file package (`SKILL.md` plus seven data-only refactoring-pattern references).
     It confines work to behaviour-preserving transformations with characterization evidence,
     one verified step at a time, and explicit exclusions for architecture, local complexity,
     system design, and scope reduction.
  8. `skills/development/system-and-data-design/` → `hermes/skills/system-and-data-design/`
     — ported as a FLAT 16-file markdown package (`SKILL.md` + 15 data-only DDIA and
     System Design references). It reviews capacity, storage, data flow, consistency,
     resilience, and scaling from stated requirements without provisioning infrastructure;
     its scope explicitly excludes architecture-first, code-complexity, refactoring-safely,
     and lean-code concerns.

  Items 5-8 (the architecture cluster) are mutually exclusive by scope — each explicitly
  excludes its siblings' territory in its own frontmatter — and none duplicates our ported
  `code-quality`/`lean-code`/`feature-layer-architecture` (upstream itself defers to
  `lean-code` for YAGNI-stripping requests).
- Queue #4 is complete.
- **Track A — re-review 13 existing hand-adapted ports (operator-approved 2026-08-03),
  surfaced by the sync report's `manual-reapproval` bucket**: complete, 13/13 reviewed.
  Each assessment diffs the upstream source against the current hand-adaptation and decides
  whether the change is material; this is a drift assessment, not a mechanical conversion
  or auto-acceptance.

  Re-review ledger:
  - `rules/agent-docs-freshness.md` → `hermes/skills/documentation-freshness/SKILL.md`:
    reviewed, no change needed. Upstream delta is path-scoping metadata plus a renamed
    reference to an upstream safety rule; both are harness-specific wiring or naming and
    do not alter the existing Hermes data-only, read-only freshness protocol.
  - `rules/autonomy-risk-tiers.md` → `hermes/skills/risk-tiered-autonomy/SKILL.md`:
    reviewed, no change needed. The upstream delta enumerates reversible action examples
    and adds upstream hook-based deferral enforcement; the Hermes adaptation already
    preserves tiering, standing-authority checks, rollback evidence, and high-impact
    approval gates without importing harness hooks or broadening permissions.
  - `rules/cross-harness-agents-md.md` → `hermes/skills/portable-project-context/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM; the Hermes
    adaptation already preserves concise shared guidance, durable task handoffs, external
    interface distrust, and access-credential boundaries without upstream-specific wiring.
  - `rules/edit-formats-and-tiering.md` → `hermes/skills/edit-formats-and-tiering/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM; the Hermes
    adaptation already preserves exact-match safety, proportionate edit selection,
    provider-neutral planning/application separation, and verification without importing
    model-selection, external delegation, or harness-wiring mechanics.
  - `rules/file-organization-cohesion.md` → `hermes/skills/file-organization-cohesion/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM; the Hermes
    adaptation already preserves durable-versus-disposable placement, hierarchy and
    cohesion checks, read-only preflight, and approval-gated relocation without importing
    the upstream advisory hook, `docs/layers/` convention, or other harness wiring.
  - `rules/folder-lifecycle-labels.md` → `hermes/skills/folder-lifecycle-classification/SKILL.md`:
    reviewed, no change needed. The upstream delta changes only the illustrative marker
    field `project` from `retouch-app` to `example-app`; the Hermes adaptation deliberately
    does not prescribe or create the upstream marker schema and already preserves the
    recoverability taxonomy, read-only inspection, active-consumer checks, and confirmation-gated cleanup boundary.
  - `rules/git-source-of-truth.md` → `hermes/skills/git-source-of-truth/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM and retargets
    two upstream `safety-billing.md` references to `safety.md`; the Hermes adaptation already
    preserves Git preflight, explicit staging, post-push read-back, and access-credential
    exclusions without importing either upstream safety-rule dependency or harness-specific wiring.
  - `rules/memory-maintenance.md` → `hermes/skills/durable-context-maintenance/SKILL.md`:
    reviewed, no change needed. The upstream delta adds only harness path-scoping metadata;
    the Hermes adaptation already preserves meaningful links, load-bearing claim provenance,
    targeted delta updates, duplicate/conflict checks, independent review, and approval-gated
    durable writes without importing upstream path conventions or executable merge tooling.
  - `rules/no-claude-attribution.md` → `hermes/skills/repository-attribution-hygiene/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM; the Hermes
    adaptation already preserves policy-aware, accurate shared metadata, required-disclosure
    exceptions, read-only preflight, and prohibition on automatic hooks or history rewriting
    without importing vendor-specific attribution controls or harness wiring.
  - `rules/safety-billing.md` → `hermes/skills/billing-spend-controls/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM; the Hermes
    adaptation already preserves provider-neutral preflight, bounded spend controls,
    approval-gated billing changes, redacted telemetry, and incident response without
    importing provider-specific claims, credential names, history rewriting, or hook wiring.
  - `rules/silent-failure-detection.md` → `hermes/skills/silent-failure-detection/SKILL.md`:
    reviewed, no change needed. The upstream delta only retargets the related upstream
    safety-rule link from `safety-hooks.md` to `safety.md`; the Hermes adaptation already
    generalises the prerequisite-verification principle into observable behavioural evidence
    and explicit telemetry gaps without importing either upstream safety-rule dependency,
    plugin paths, or hook wiring.
  - `skills/development/proof-verify/SKILL.md` → `hermes/skills/proof-verify/SKILL.md`:
    reviewed, no change needed. The upstream delta removes only a UTF-8 BOM; the Hermes
    adaptation already preserves frozen, testable criteria, builder/verifier separation,
    fresh-context read-only verification, PASS/FAIL/BLOCKED evidence, and narrow authorised
    fixes without prescribing an upstream hidden directory, task-state schema, or agent API.
  - `skills/development/workflow-orchestration/SKILL.md` →
    `hermes/skills/workflow-orchestration/SKILL.md`: reviewed, no change needed. The upstream
    delta removes only a UTF-8 BOM; the Hermes adaptation already preserves bounded protocol
    selection, stage contracts, visible failure/recovery, cost and concurrency limits,
    operator-confirmation gates, and independent evidence without importing executable
    orchestration code, upstream paths, agent APIs, or automatic dispatch.
- **Domain queue #5 (operator-approved 2026-08-03; vetted clean on 4 axes + leak sweep +
  full-text read; port in order, one per run):**
  1. `rules/rlm-context-as-program.md` → `hermes/skills/rlm-context-as-program/SKILL.md`
     — ported as a single data-only module for metadata-first partitioning, evidence-backed
     synthesis, explicit coverage, and bounded cost controls. No upstream workflow path,
     executable helper, recursive execution, or delegation mechanism is carried over.
  2. `rules/moa-gemini-delegation-eval.md` →
     `hermes/skills/moa-gemini-delegation-eval/SKILL.md` — ported as a single data-only
     evaluation gate for multi-model adoption. It requires representative, bounded evidence
     for quality, latency, cost, and privacy before any later implementation; it does not
     enable delegation, select a provider, or send prompts. It is not a duplicate of the
     operational `skills/operational/gemini-delegate/` candidate, which concerns delegation
     mechanics rather than the adoption decision.
- **One-off manual enrichment (operator-reviewed 2026-08-04), NOT a new SUPPORTED entry:**
  `rules/no-pre-existing-evasion.md` — fully diffed line-by-line against the already-ported
  `hermes/skills/no-pre-existing-evasion/SKILL.md` (source: principles/26). Verdict: ~90% of
  the content duplicates the existing skill (5-exception taxonomy, fix-or-record protocol,
  required evidence, anti-patterns — already covered); the WIP=1/VCR-Blocking section is
  infra-coupled to `feature_list.json`/`templates/long-run-project/` (same excluded class as
  `long-run-harness`/`feature-new`); the Independent-verifier section duplicates the ported
  `independent-verification`; the Opus-4.7-calibration section is a model-specific prompt tip,
  not portable; the mechanical-enforcement section names literal Claude Code hook files, not
  portable as-is. Opening a separate, similarly-named skill would mostly duplicate the
  existing one — rejected as over-engineering. Action taken instead: a targeted, hand-written
  enrichment of the EXISTING `hermes/skills/no-pre-existing-evasion/SKILL.md` (not through the
  `convert_supported`/`SUPPORTED` mechanism) adding (1) three additional forbidden-phrase
  examples ("known limitation"/"future work", "deferred for separate refactor"/"needs its own
  PR", "good stopping point"/"natural checkpoint") and (2) a generalized, Hermes-native note
  that mechanical/hook-level enforcement holds under context pressure better than prose rules
  (no literal Claude Code hook paths). One commit, a small diff to the existing file, no new
  artefact.

  **Correction (2026-08-05):** the "not through the `convert_supported`/`SUPPORTED` mechanism"
  framing above was wrong and caused a real bug. `principles/26-no-pre-existing-evasion.md` was
  already a `SUPPORTED` entry from the original port; the enrichment commit (`856ab78`) edited
  only the disk `SKILL.md`, never touching its `sync_upstream.py` `adapt_source_text()` override
  to match. That broke the round-trip invariant (`converted_output_matches_supported()`) for this
  one file. The very next autopilot cycle (2026-08-04 04:47:54-04:49:37Z, `head=856ab78`, no new
  commit) exercised the regeneration path and silently reverted the working tree back to the
  stale pre-enrichment content — confirmed by `converted_output_matches_supported()` returning
  `True` against the reverted state. Fixed by updating the override to match the enriched body,
  then regenerating the disk file directly from `make_output()` for a guaranteed byte-exact
  round-trip. One side effect: `make_skill()`'s prefix template hardcodes `version: 0.1.0` and a
  generic `Source:` line with no per-file override hook, so the custom `version: 0.1.1` and the
  enrichment-explaining `Source:` line from the original commit could not be preserved without
  extending that architecture for one file — dropped as over-engineering for a single case; the
  enriched body content itself (forbidden-phrase examples, Enforcement note) is fully intact.
  **Lesson:** hand-editing a `SUPPORTED`-lane target file always requires updating its override
  in the same commit — verify with `converted_output_matches_supported()` before committing, not
  just `validate_output.py` (which does not check override/disk consistency).
- **Not portable (infra-coupled, confirmed source):** `rules/long-run-harness.md` — the
  direct source of the `feature_list.json`/`init.sh` convention already excluded by our
  2026-07-13 general rule on upstream-KB-infrastructure-coupled content.
- After queue #5, Track A, and the `no-pre-existing-evasion` enrichment above, only
  Wave-4 script-research and policy manual-review candidates remain; do not select a
  further port automatically. An operator decision is required.
- **Manual-review-only (policy), NOT auto-port:** `skills/ai-ml/forensic-prompt-compiler/`
  — a high-fidelity image→prompt reconstructor (risk of replicating third-party images or a
  specific identity; it carries an "identity-safe" mitigation but the capability is
  dual-use), and `skills/ai-ml/flux2-klein-prompting/` (`api_key` policy flag). Both need a
  product/policy decision before any port.
- **Manual-review-only (domain blast-radius, not content), NOT auto-port:**
  `skills/operational/remote-compute-ops/` — the content itself teaches SAFE credential
  handling (explicit anti-pattern warnings), but the domain is live remote infrastructure
  (SSH, API tokens, RunPod/Massed Compute billing) with high blast radius, overlap-adjacent
  to `billing-spend-controls`. Needs a separate operator policy decision.
- **Rejected (wrong domain, not a script-safety issue), 2026-08-04:**
  `skills/operational/desktop-sessions-discovery/` — the entire skill package (SKILL.md + 4
  scripts: `sessions_registry.py`, `sessions_inventory.py`, `sessions_find.py`,
  `sessions_restore.py`) exists to discover and restore **Claude Desktop app** (Anthropic's
  separate consumer application) sessions hidden across multiple `accountId` folders — a
  workaround for an Anthropic bug (upstream cites `anthropics/claude-code#48511`). Its content
  is entirely about that other product's reverse-engineered storage layout
  (`%APPDATA%\Claude\claude-code-sessions\...`, `~/Library/Application Support/Claude/...`); it
  has nothing to do with Hermes, which is not the Claude Desktop app and has no equivalent
  multi-account session-visibility bug to work around. Not a candidate for adaptation — the
  subject matter itself is out of scope, not something a rewording could fix. (Note in passing,
  not evaluated further: `sessions_restore.py` also copies session files between account
  folders, which would need its own credential/data-safety review if this were ever revisited
  for a different reason.)
- `skills/ai-ml/notebooklm-grounded-research/` and `skills/development/distill-feedback/` —
  **ported** via the reviewed-script lane (see "Ported so far" above and `SECURITY.md`'s
  "Reviewed-script lane" section); no longer quarantined. `distill-feedback`'s bundled
  `scripts/extract_feedback_queue.py` is deterministic, stdlib-only, and only ever appends
  to a local processed-log file; the SKILL.md explicitly discloses that its queue
  (`~/.claude/feedback/queue.jsonl`) is populated by a separate Claude-Code Stop hook not
  installed by Hermes, so an operator who runs only Hermes will correctly see zero pending
  items rather than a broken feature. Porting this exposed a real gap in
  `scripts/validate_output.py`'s `FORBIDDEN_GENERATED_HARNESS_PATTERNS`: the blanket
  `.claude[\/]` and `python scripts/` checks predate the reviewed-script lane and would
  false-positive on any skill that legitimately discloses an external Claude-Code-specific
  prerequisite or instructs the operator to run its own bundled script (the same pattern
  Hermes's own official `xlsx` skill uses). Fixed narrowly: those two specific patterns are
  now skipped only for a SKILL.md whose own skill directory ships an allowlisted reviewed
  script; every other forbidden-pattern check still applies unconditionally.

## Agents not yet ported

The upstream `agents/` directory contains pixel-art review agents:

- `agents/pixel-art-animation-reviewer.md`
- `agents/pixel-art-composition-reviewer.md`
- `agents/pixel-art-interaction-reviewer.md`
- `agents/pixel-art-quality-board.md`
- `agents/pixel-art-reviewer.md`
- `agents/pixel-art-style-reviewer.md`

Reason: Hermes does not use these Claude Code agent descriptors directly. They may become Hermes skills, prompt templates, or evaluation rubrics, but not autonomous agents without a Hermes-native orchestration design.

## Alternatives and root docs not yet ported

The following markdown documents stayed as upstream reference material:

- `AGENTS.md`
- `CLAUDE.md`
- `HOW-IT-WORKS.md`
- `MAINTENANCE.md`
- `README.md`
- `UPDATES.md`
- `alternatives/README.md`
- `alternatives/agent-mailbox-system.md`
- `alternatives/agents-md-rule-loading.md`
- `alternatives/code-review.md`
- `alternatives/codebase-map-scoping.md`
- `alternatives/context-management.md`
- `alternatives/design-md-pattern.md`
- `alternatives/docker-sandbox-claude-code.md`
- `alternatives/kb-code-sync.md`
- `alternatives/managed-agents.md`
- `alternatives/memory-strategies.md`
- `alternatives/multi-agent-patterns.md`
- `alternatives/optimization.md`
- `alternatives/orchestration.md`
- `alternatives/reasoning-regression-debugging.md`
- `alternatives/session-handoff.md`
- `alternatives/skill-management-tools.md`
- `alternatives/token-economy.md`
- `alternatives/workspace-organization.md`

Reason: many are design notes or competing patterns rather than ready modules. They are useful for research and planning, but should be distilled into Hermes-native modules rather than copied wholesale.

## Templates not yet ported

Thirteen low-risk upstream templates have been adapted with Hermes-native provenance and
operator-confirmation wording, including the complete reviewed `templates/agent-task/`
record set, `templates/proof-plan.md`, and
`templates/long-run-project/PRD-BOOTSTRAP.md` ->
`hermes/templates/long-run-project-prd-bootstrap.md`. The new long-run template is
markdown-only planning data: it records a feature-plan proposal from an approved brief
without creating state, calling a validator, or activating a workflow. The installer
copies templates only into the isolated `<hermes-home>/templates/config-kit/` namespace
and the remover deletes only that namespace. The remaining template categories stay
out of MVP:

- Claude project templates:
  - `templates/CLAUDE-library.md`
  - `templates/CLAUDE-ml-project.md`
  - `templates/CLAUDE-web-app.md`
- Review/prompt templates:
  - `templates/REVIEW.md`
  - `templates/bug-fix-prompt.md`
  - `templates/proof-plan.md`
- Memory/project templates:
  - `templates/chronicle.md`
  - `templates/memory-project.md`
  - `templates/memory-reference.md`
- Agent task structure:
  - `templates/agent-task/README.md` has been ported as a data-only overview of the
    reviewed task records; `templates/agent-task/handoff.md` has been ported as a data-only task transfer
    template, `templates/agent-task/fix-log.md` as a data-only corrective-change
    record, and `templates/agent-task/problems.md` as a data-only verifier-finding
    record, `templates/agent-task/scratchpad.md` as concise resumable working
    notes, `templates/agent-task/evidence/README.md` as a redacted evidence
    register, and `templates/agent-task/state.json` as a data-only task-state record;
    `templates/agent-task/trace.jsonl` has been ported as a markdown-only,
    data-only timeline record, and `templates/agent-task/verdict.json` as a
    data-only verdict record; neither initialises a task, creates state, approves
    a change, or activates a workflow. All current `templates/agent-task/` files
    are now represented only as reviewed data-only templates.
- Knowledge-base skeleton:
  - `templates/kb-skeleton/*`
- Long-run project skeleton:
  - `templates/long-run-project/README.md` has been ported as a data-only review
    overview; JSON schema/example data and executable files remain unported.

Reason: template installation raises path, naming, lifecycle, and overwrite questions. It needs a Hermes-native template target and removal contract.

High-value next candidates:

1. `templates/kb-skeleton/` — useful, but includes workflow/script files and must remain reviewed.

## Workflows not yet ported

No upstream workflows were ported:

- `workflows/deep-review-flow.js`
- `workflows/research-cn-ru.js`
- `workflows/rlm-explore.js`
- `workflows/EFFECTIVE-AGENTS.md`
- `workflows/README.md`

Reason: JS workflows are executable orchestration artefacts. Hermes equivalents may be skills, scripts, cron jobs, kanban flows, or delegated-agent protocols. They should be redesigned, not copied.

## References and docs not yet ported

- `references/security-tooling-guide.md`
- `docs/agent-tool-evals/2026-06-26-keenable-clips-evaluation.md`
- `docs/openscience-ml-domain-eval.md`
- `docs/openscience-ml-skill-inventory.json`

Reason: these are useful reference materials but not installable Hermes modules yet.

## Release and Wave state

This ledger is the authoritative release-state input for a scheduled porting
protocol. Git tags are authoritative for the active release line and patch
number; do not infer a Wave transition from an artefact's category alone.

| Field | Current value |
| --- | --- |
| Active Wave | Wave 3 — skill package review |
| Active release line | `0.3` |
| Latest released tag | `v0.3.71` |
| `upstream.lock.json` `adapter.version` | `0.3.0` (Wave 3 baseline, not a patch-release counter) |
| Historical classification of `templates/proof-plan.md` | Wave 1 close-out; its `v0.1.40` release did not start Wave 2 |
| Exact Wave 2 trigger | First accepted and verified `templates/agent-task/*` artefact |
| First Wave 2 version | `v0.2.0`, with `adapter.version` updated to `0.2.0` in that same commit |
| Wave 3 trigger | Satisfied by the accepted and verified markdown-only `skills/development/proof-verify/SKILL.md` adaptation to `hermes/skills/proof-verify/SKILL.md`; its reference remains separately reviewed and unported. |
| Wave 3 first version | `v0.3.0`, with `adapter.version` updated to `0.3.0` in this trigger commit |
| Next Wave | Not prepared; a later transition commit must add its exact trigger and release line before any minor-version change. |

Release decision rules:

1. A review fix or a Wave 1 close-out commit stays in the active `0.1` line and
   increments only its patch tag.
2. A tag such as `v0.1.42` is compatible with `adapter.version: "0.1.0"`:
   compare only major/minor for the active line. The patch components are not
   expected to match.
3. Do not start Wave 2 merely because a template was previously ported. Only
   the exact Wave 2 trigger above authorises `v0.2.0`.
4. Before any later Wave transition, add its exact trigger and release line to
   this ledger in the transition commit. If the ledger is absent or ambiguous,
   report `BLOCKED` rather than choosing a version by inference.
5. A close-out commit that only prepares the next Wave remains on the active
   release line, increments only that line's patch tag, and does not change
   `adapter.version` or activate the prepared Wave.
6. The trigger commit activates the prepared Wave, changes `adapter.version` to
   its documented baseline, and receives that Wave's documented first version.

## Recommended next porting waves

### Wave 1 — low-risk markdown modules

Goal: expand useful Hermes guidance without executable code.

Status: close-out. `templates/proof-plan.md` was ported as a data-only Hermes
template, retaining frozen acceptance criteria, exact verification commands,
expected outcomes, scope, and constraints. It adds Hermes-native provenance and
operator-confirmation wording; the existing scoped installer/remover contract
was independently exercised against a disposable home. `rules/long-run-harness.md`
was reviewed and not selected because its useful feature-state and baseline-health
guidance is already covered by `long-run-feature-tracking`, while its active-hook
and shell conventions require a separate threat model. The next porting candidate
belongs to Wave 2 under the release ledger above.

Acceptance criteria:

- each item becomes a Hermes `SKILL.md` or is merged into an existing generated skill;
- `mappings/compatibility.yaml` and `scripts/sync_upstream.py:SUPPORTED` are updated together;
- generated skills include source attribution and Hermes-native wording;
- `validate_output.py` still passes;
- disposable `HERMES_HOME` install/remove test passes.

### Wave 2 — support files and templates

Goal: add selected templates without expanding execution risk.

Status: closed. The exact Wave 2 trigger was satisfied by the first accepted,
verified `templates/agent-task/*` artefact: `templates/agent-task/spec.md` ->
`hermes/templates/agent-task-spec.md`. It remains a markdown-only, data-only
template in the existing scoped installer/remover namespace; no task state,
hooks, scripts, or automation were activated.

Candidates: none. The remaining template material is either executable-adjacent,
schema/example data needing a separate compatibility decision, or requires a documented
next-Wave transition before further porting.

Acceptance criteria:

- installer/remover handle `templates/config-kit/` predictably;
- no executable scripts are installed without review;
- overwrite behaviour is documented and dry-run visible;
- removal contract remains narrow.

### Wave 3 — skill package review

Goal: port selected upstream skill packages as Hermes skills.

Candidates:

`skills/writing/article-structure-review/SKILL.md` is ported as a markdown-only,
read-only macro-structure review module. The adaptation retains thesis/support
balance, genre fit, stated limitations, section load, and visual-versus-prose
guidance; it deliberately leaves sentence-level style to `humanize-russian` and the
installed `humanizer` module, and treats upstream numeric heuristics as diagnostic
signals rather than runtime policy. `skills/agent-harness-design/SKILL.md` is ported
as a bounded, data-only design-triage module. Its ten upstream references remain
unported: their provider-specific implementation examples, runtime storage
conventions, and executable-looking pseudocode require separate overlap and
threat-model review before any Hermes-native reference is accepted.
`skills/frontend/frontend-design/` is ported as a complete five-file, markdown-only
domain package under `hermes/skills/frontend/frontend-design/`. Its four references
remain data-only guidance; no project tooling, service-worker registration, or external
publication action is activated by this adapter.
`skills/operational/observability-monitoring/` is ported as a flat two-file,
markdown-only module under `hermes/skills/observability-monitoring/`. It retains
read-only telemetry, SLI/SLO, alerting, and incident-evidence guidance. The upstream
`agents/openai.yaml` is Codex-specific manifest metadata and remains unported.

Acceptance criteria:

- support files are placed under Hermes-allowed skill subdirectories;
- scripts are either removed, rewritten, or explicitly reviewed;
- binary/media assets are justified;
- each skill is smoke-tested with `hermes skills list`.

### Wave 4 — hook and workflow redesign

Goal: decide which upstream guards deserve Hermes-native implementations.

Candidate groups:

- secret/credential guards;
- destructive command guards;
- handoff/session guards;
- docs freshness and KB validation;
- task inbox and feedback display;
- long-run feature validators.

Acceptance criteria:

- no direct upstream hook execution;
- each guard has a Hermes-native target: plugin, validator script, cron/scheduled protocol, skill guidance, or rejection;
- threat model is documented in `SECURITY.md`;
- disposable VM testing covers install, activation, failure mode, and removal.

## Reviewed-script lane pilot — status (2026-08-04)

The `notebooklm-grounded-research` reviewed-script-lane pilot (see the "Ported so far" entry
above and `SECURITY.md`'s "Reviewed-script lane" section) is code-complete and locally verified:
`mappings/reviewed-scripts.yaml` allowlist, `scripts/sync_upstream.py` `SUPPORTED` entries +
`adapt_source_text()` overrides for both markdown files, `mappings/compatibility.yaml` entries,
`scripts/validate_output.py`'s `validate_reviewed_scripts()` gate, and the `AGENTS.md`/
`SECURITY.md` charter language are all in place. `python3 scripts/validate_output.py` →
Validation OK; `converted_output_matches_supported()` → True; `sync_upstream.py --check` shows no
drift against the pinned lockfile SHA.

The disposable `install_hermes.py --dry-run`/`--apply`/`remove_hermes.py` cycle against a temp
`HERMES_HOME` has been run and confirms a skill's `scripts/` subfolder copies byte-identically and
removes cleanly, with no special-casing needed in either script.

Released as **v0.3.64** (commit `e675abe`, CI `Validate adapter` green:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/actions/runs/30887781264, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.64). The
`hermes-config-kit-auto-port` cron job (`aa719369167e`) remains paused per operator instruction
until explicitly resumed.

A second pilot, `distill-feedback` (see "Ported so far" above), followed immediately using the
same lane and exposed a real gap in `validate_output.py`'s harness-leak check for skills that
legitimately disclose an external prerequisite or invoke their own bundled script; fixed and
released as **v0.3.65** (commit `4cd2714`, CI green:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/actions/runs/30889699624, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.65).

`skills/operational/desktop-sessions-discovery/` — the last item this "Wave-4 script-research"
label had flagged — has been reviewed and **rejected** (wrong domain, not a script-safety issue;
see the rejection note under "Quarantine lane: not ported" above). No script-bearing candidates
remain outstanding as of 2026-08-04.

**Naming note:** "Wave-4 script-research" (this informal label, used in earlier session notes to
bucket script-bearing skill candidates) is a different thing from the formally documented
"Wave 4 — hook and workflow redesign" below, which covers a different scope: reimplementing
upstream Claude-Code **hooks** (`hooks/*.py`, e.g. secret/destructive-command/handoff guards) and
**JS workflows** (`workflows/*.js`) as Hermes-native guards, not porting skill-bundled scripts.
The reviewed-script lane and its two pilots are **Wave 3** work (skill-package review), not a
Wave 4 trigger: Wave 3's own documented acceptance criteria already anticipated this ("scripts
are either removed, rewritten, or explicitly reviewed") — the reviewed-script lane is exactly
that "explicitly reviewed" path being built out, not a new Wave.

## Wave 3 continuation (2026-08-04)

Following the two reviewed-script-lane pilots above, `skills/operational/gemini-delegate/` was
ported as a markdown-only Wave 3 skill (no `scripts/` subfolder in the upstream package itself).
Its upstream body referenced an external companion script (top-level `scripts/gemini-switch.sh`
in the claude-code-config repo, not bundled with this skill package) that copies and overwrites
live Google OAuth credential files (`oauth_creds.json`, `google_accounts.json`). That script was
**deliberately not ported**, even via the reviewed-script lane: credential-file mutation is a
higher-stakes category than the read-only/append-only scripts reviewed so far, and pulling it in
as a side effect of porting this skill's guidance would have been scope creep past what was
asked. The ported `SKILL.md` describes the account-switch pattern conceptually and states this
decision explicitly rather than silently dropping the capability. This rejection is recorded
explicitly in `mappings/rejected-scripts.yaml` (source SHA-256, full reason, and the
`revisit_condition` that would need to hold before reconsidering it), not just in this prose —
see `SECURITY.md`'s "Rejected scripts" section.

Released as **v0.3.66** (commit `0591db2`, CI `Validate adapter` green, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.66).

`skills/architecture/plan-swarm-review/` followed as the next clean Wave 3 candidate: a
markdown-only, two-file package (`SKILL.md` + `references/vulnerability-kb.md`, no scripts).
The upstream `SKILL.md` referenced three sibling skills (`/plan-eng-review`, `/plan-ceo-review`,
`/plan-design-review`) in its "when to use this vs other skills" comparison table; none of the
three exist anywhere in the pinned upstream snapshot, so those dangling references were dropped
and the comparison table rewritten against this adapter's own already-ported skills
(`deep-review`, `vulnerability-detection-pipeline`, `proof-verify`,
`multi-agent-task-decomposition`) instead. The upstream reference also pointed at a fuller
`knowledge-vault/docs/security/cwe/` example set that is not part of this adapter; the ported
reference states plainly that the condensed heuristics are the full extent of what's available
here. Upstream frontmatter fields specific to the Claude Code harness (`user-invocable`,
`model`, `allowed-tools`) were dropped, matching every other port's convention. This is the first
port from the `skills/architecture/` upstream domain, so it uses the (post-decision) nested
`hermes/skills/architecture/plan-swarm-review/` path rather than a flat one.

Released as **v0.3.67** (commit `e173207`, CI `Validate adapter` green, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.67).

`skills/creative/pixel-art-studio/` followed as a larger Wave 3 + reviewed-script-lane
combination, decomposed and partly fanned out to parallel subagents (per operator direction to
decompose the task and use subagents where safe). Package size: `SKILL.md` (398 upstream lines),
8 reference files (3093 upstream lines), 7 upstream Python scripts (2640 lines), one JS canvas
library (`elements/elements.js`, 488 lines) plus its static preview page (`catalog.html`), and 30+
bundled `.hex` palette files (136 KB) plus one small curated-index JSON.

Scope decisions made autonomously (all reversible/git-revertable, decided and reported per this
adapter's autonomy-risk-tiers discipline rather than blocked on upfront questions):

- **Companion skill `pixel-art-storyboard` deferred** to a separate round — it has its own
  dangling references (a non-existent `templates/cover-template.js`, a personal
  `Grass Field with City.html` example file not in the snapshot) and is a large enough
  companion package to deserve its own pass.
- **`bake_animation.py` excluded** from this round (of 7 upstream scripts, only 6 were ported).
  It drives a headless Chromium browser via Playwright against a fully caller-controlled URL
  (`page.goto(url)`), shells out to `ffmpeg` (safe argv-list form, not `shell=True`, but still a
  meaningfully larger external toolchain — Playwright + a Chromium install + ffmpeg, beyond the
  Pillow/numpy the other six need), and leaves un-cleaned temporary frame directories on disk.
  This is a qualitatively different risk category from the other six read/write-confined
  image-processing CLIs and was independently characterized as "needs-discussion" by a research
  subagent before this decision — same discipline as declining `gemini-switch.sh` earlier in this
  Wave: a script doesn't get pulled in by default just because it shipped alongside safer ones.
  Both rejections are recorded explicitly, with source SHA-256, full reason, and a
  `revisit_condition`, in `mappings/rejected-scripts.yaml` — see `SECURITY.md`'s "Rejected
  scripts" section.
- **`elements/elements.js` and `elements/catalog.html` ported as reference/asset data**, not
  through the reviewed-script-lane manifest: both were fully read by hand and confirmed to be
  inert, browser-sandboxed canvas-drawing code with no network calls, no `eval`, and no
  filesystem access — they only ever execute inside a browser loading the bundled catalog or a
  generated scene page, never invoked by an operator/agent directly the way the Python scripts
  are. Porting them exposed that `elements/` (unlike `scripts/`) isn't covered by the quarantine
  substring check at all — a latent gap, noted here rather than relied upon; the actual basis for
  including them is the manual safety review, not the path-naming loophole.
- **Binary example assets** (~204 KB of PNG/GIF/APNG demo images, two small JSON specs, and
  several static HTML demo pages under `examples/`) were initially excluded on the general
  heavy-binaries-exclusion reasoning in `git-source-of-truth.md`, then **included on explicit
  operator instruction** since they exist as-is in the original upstream repository (see the
  "Follow-up" note below for the full reversal and the one due-diligence finding it produced).

Mechanical/process notes:

- **Two safety-relevant validator gaps found and fixed while porting, not papered over:**
  1. `validate_quarantine_policy()`'s leak check required an individual `reviewed-scripts.yaml`
     entry for every file under a `scripts/`-named path, with no distinction between executable
     code and inert bundled data — this would have forced 30+ near-identical manifest entries for
     plain `.hex`/`.json` palette lookup tables that cannot execute and are already covered by
     `validate_secret_scan()`'s broad sweep of the whole `hermes/` tree. Fixed with a narrow
     `NON_EXECUTABLE_DATA_EXTENSIONS` allowlist (`.hex`, `.json`, `.txt`, `.csv`) — code files
     still require full manifest review; only inert data sitting alongside a reviewed script is
     exempted.
  2. The `FORBIDDEN_GENERATED_HARNESS_PATTERNS` exemption added for the `distill-feedback` pilot
     (v0.3.65) only covered `validate_skills()`'s `SKILL.md` loop, not the separate `references/*.md`
     loop — so a reference file (`02-palette-theory.md`) documenting how to invoke this skill's
     own bundled `scripts/palette.py` still false-positived. Fixed by computing the skill root
     correctly for both call sites (`path.parent` for a `SKILL.md`, `path.parent.parent` for a
     `references/*.md`) rather than assuming the check only needed to exist in one place.
- Six subagents were used in parallel to draft the 8 reference-file adaptations (one file each);
  a seventh research subagent independently characterized all 7 upstream scripts for
  network/subprocess/credential/destructive-operation risk before any were ported. Every one of
  the 6 approved scripts was then also read in full personally, matching (not merely trusting)
  the subagent's findings, before being added to `mappings/reviewed-scripts.yaml` — the manifest
  entries are a personal sign-off, not a delegated rubber stamp.
- **Live functional execution of the 6 scripts was initially not attempted**: Pillow and numpy
  were not installed in this development environment, and installing them solely for a one-off
  verification (when every script was already fully read and independently characterized) was
  judged disproportionate at the time. Superseded — see the "Follow-up" note below.

Full verification: `python3 scripts/validate_output.py` -> Validation OK;
`converted_output_matches_supported()` -> True; disposable `install_hermes.py --apply` copied all
48 files (SKILL.md + 8 references + 6 scripts + 32 palette files + elements.js + catalog.html)
byte-identically; `remove_hermes.py --apply` removed them cleanly.

Released as **v0.3.68** (commit `dfe1cde`, CI `Validate adapter` green, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.68).

**Follow-up (2026-08-04, operator-directed):** three of the decisions above were revisited on
explicit operator instruction after the v0.3.68 release:

1. **`bake_animation.py` and `gemini-switch.sh` rejections now recorded explicitly** in the new
   `mappings/rejected-scripts.yaml` (source SHA-256, full reason, and a `revisit_condition` for
   each), cross-linked from `SECURITY.md`'s new "Rejected scripts" section and from `AGENTS.md`'s
   quarantine-policy section — not just described in this backlog's prose.
2. **`examples/` (all ~204 KB of PNG/GIF/APNG demo images, two small JSON specs, and five static
   HTML demo pages) restored** into the port unmodified, per explicit operator instruction that
   they exist as-is in the upstream repository. Due diligence on the five HTML files found one
   worth flagging: `examples/twilight-covers/index-v2-static.html` uses `fetch()` plus `eval()` to
   load and re-run the canvas-drawing code from its sibling `index-v2.html` at a same-origin,
   relative path (to avoid duplicating that code across two demo pages) — it fetches no external
   URL and only functions when served locally, so this was judged safe to include as-is; noted in
   the ported `SKILL.md` rather than silently passed over.
3. **Live functional execution performed via `uv run --with Pillow --with numpy`**, per explicit
   operator instruction that this dependency-acquisition path was fine. All 6 scripts were
   exercised successfully (`palette.py --list`/`--ramp`; `render.py` on a static sprite and,
   through `animate.py`'s delegation, an animation GIF; `dither.py` with floyd-steinberg;
   `preprocess.py` downsampling with bayer4 dithering; `animate.py --template`; `quality_check.py`
   on both a static sprite and `--animation` mode) — results recorded per-script in
   `mappings/reviewed-scripts.yaml`'s `functional_test` fields. This surfaced one genuine
   **upstream bug**, disclosed rather than silently worked around: `quality_check.py`'s
   `detect_block_size()` raises `ValueError: high <= 0` when an input image's exact height or
   width matches one of its candidate block sizes with no upscale headroom (e.g. a plain,
   non-upscaled 16×16 PNG). Not fixed here — the script was ported unmodified, per this lane's own
   discipline — but recorded in both `mappings/reviewed-scripts.yaml` and the ported `SKILL.md`'s
   Gotchas section so a future user isn't the first to hit it.

Released as **v0.3.69** (commit `bf683ed`, CI `Validate adapter` green, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.69) covering these
three follow-up changes.

`skills/creative/pixel-art-storyboard/` — the `pixel-art-studio` companion deferred earlier —
followed as the next Wave 3 item: `SKILL.md` (348 upstream lines), 10 reference files (3005
upstream lines), and 2 static HTML canvas templates (`single-cover.html`, `grid-cover.html`, 255
lines), no bundled scripts of its own. Decomposed the same way as `pixel-art-studio`: 10 parallel
subagents drafted the reference-file adaptations (one file each), while the main `SKILL.md` and
final cross-file consistency were done directly.

Issues found and resolved during adaptation, all pre-existing in the upstream source (not
introduced by this port):

- **`templates/cover-template.js` does not exist upstream** — the `SKILL.md` referenced it, but
  only `templates/single-cover.html` and `templates/grid-cover.html` exist in the pinned
  snapshot. Every code example was pointed at the two templates that actually exist.
- **A personal, non-bundled `Grass Field with City.html` example** is cited throughout several
  files (the `SKILL.md`'s own frontmatter description, and `references/retouch-style-guide.md`
  most heavily, alongside two other personal files, `Elements Sheet.html` and a "Preview Grid"
  review UI) as the "authoritative"/"canonical" reference for this skill's aesthetic. None exist
  in the snapshot. Noted as illustrative/historical context in the ported files rather than
  silently kept as if bundled.
- **Three recurring "companion research" files** (`image-collection-learning-2026.md`,
  `image-to-pixelart-and-training-2026.md`, `image-to-pixel-art-tools-2026.md`) are cited across
  four different reference files as if they were sibling documents, but none exist anywhere in
  the pinned upstream snapshot. Each mention was replaced with a plain note that the file isn't
  part of this port, rather than a dangling cross-reference.
- **`bake_animation.py` is referenced throughout** (the main workflow's "Baking finished
  animations" section, and three reference files: `smoother-animation-baking.md` — almost
  entirely about this tool — plus `element-library-scaling-architecture.md` and
  `high-detail-pipeline.md`). Consistent with the `pixel-art-studio` port and the
  `mappings/rejected-scripts.yaml` record: every mention states plainly that the script was
  fully read and deliberately not ported, and — following the same precedent set for
  `gemini-switch.sh` in the `gemini-delegate` port — none of its example invocations are kept as
  literal runnable-looking `bash` commands; they were rewritten as prose or a parameter/format
  table describing what the upstream tool did.
- **A Claude-Code "agent" invocation** (`@pixel-art-quality-board`, referencing
  `agents/pixel-art-quality-board.md` — a Claude-Code autonomous-subagent descriptor with no
  Hermes-native equivalent) in `references/high-detail-pipeline.md` was rephrased as a
  description of the multi-dimensional review process itself, not a tool/agent call.
- One `references/high-detail-pipeline.md` code example invoked `scripts/quality_check.py`
  without the `../pixel-art-studio/` prefix used everywhere else in this skill (an
  inconsistency already present upstream); normalized to match every other cross-skill
  reference in this port.

Porting this exposed one further validator gap, found and fixed rather than worked around: the
`FORBIDDEN_GENERATED_HARNESS_PATTERNS` exemption added for `pixel-art-studio` (v0.3.68) only
covered a skill referencing *its own* bundled reviewed script; it did not cover a *companion*
skill's `SKILL.md`/references documenting a **sibling** skill's reviewed script via a relative
path (e.g. `pixel-art-storyboard` invoking `../pixel-art-studio/scripts/palette.py`). Fixed with
`_python_scripts_references_resolve_to_reviewed()`, which resolves each specific
`python .../scripts/x.py` match relative to the referencing file's own directory and checks it
against the reviewed-script allowlist directly — narrower and more precise than the per-skill
exemption, and it correctly continues to reject a reference to an unreviewed or rejected script
(e.g. `bake_animation.py`) even when it appears alongside legitimate ones.

Full verification: `python3 scripts/validate_output.py` -> Validation OK;
`converted_output_matches_supported()` -> True; disposable `install_hermes.py --apply` copied
all 13 files (`SKILL.md` + 10 references + 2 templates) byte-identically; `remove_hermes.py
--apply` removed them cleanly.

Released as **v0.3.70** (commit `8e93873`, CI `Validate adapter` green, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.70).

**Wave transition status:** the active Wave remains **Wave 3 — skill package review**; no Wave 4
trigger has fired (Wave 3's own candidate list — `article-structure-review`, `agent-harness-design`,
`frontend-design`, `observability-monitoring`, the reviewed-script-lane pilots, `gemini-delegate`,
`plan-swarm-review`, `pixel-art-studio`, and now `pixel-art-storyboard` — is not exhausted purely by having ported several items; per release rule 4
above, a Wave transition requires its exact trigger to be documented in the transition commit,
which has not happened here). **0.4.x is not yet authorized.** It becomes authorized only when a
future commit documents Wave 4's exact trigger (e.g., "first accepted and verified Hermes-native
reimplementation of an upstream hook/guard") and updates this ledger accordingly, per the same
discipline used for the Wave 2 and Wave 3 transitions above. Until then, all further work —
including any additional reviewed-script-lane pilots — stays on the `0.3.x` patch line.

Separately, `python3 scripts/sync_upstream.py --check` on 2026-08-04 shows upstream has advanced
3 commits past the pinned `last_synced_sha` (from `9807b2d...` to `81c543a...`). This is a
`--check`-only observation (non-mutating); a full `--sync` to review and pull those changes has
not been run and is separate work from this Wave 3 continuation.

### `bake_animation.py` reconsidered and accepted (2026-08-04)

Following the v0.3.70 release above, the operator gave an explicit 5-point directive reversing
`bake_animation.py`'s earlier rejection: (1) fix the arbitrary-URL exposure by restricting the
script to loopback addresses, (2) treat the JS-execution-in-browser concern as resolved once (1)
is fixed, no separate action needed, (3) approve the ffmpeg-via-`subprocess.run()` pattern as-is,
(4) fix the temp-directory cleanup so no garbage is left behind, (5) approve the
Playwright+Chromium+ffmpeg dependency surface.

Two narrow modifications were made to the pristine upstream script (diffed to confirm nothing
else changed): a new `_require_local_url()` check (rejects any URL whose scheme isn't http/https
or whose hostname isn't `localhost`/`127.0.0.1`/`::1`), called first thing in `main()`; and the
`bake()` body wrapped in `try/finally` with `shutil.rmtree(out_dir, ignore_errors=True)` so the
temp frame directory is always removed. The URL guard was unit-tested in isolation (7/7 cases
covering allowed and rejected hosts/schemes, case-insensitivity); the full Playwright/Chromium
capture pipeline was not exercised end-to-end (would require a large Chromium download; the
capture/encode logic itself was untouched and had already been fully read during the original
review).

This is the first entry in `mappings/reviewed-scripts.yaml` that is not byte-identical to its
upstream source — a new `modifications` field was added to the manifest schema for this case.
`mappings/rejected-scripts.yaml`'s original entry was kept verbatim (not edited or deleted) with a
new `superseded_by` field explaining the reconsideration, preserving why the script was first
turned down. `mappings/compatibility.yaml` gained a `status: review`, `risk: medium` entry (the
other six `pixel-art-studio` scripts are `risk: low`).

Propagated the "now accepted" status across every file that previously described the script as
excluded: `pixel-art-studio/SKILL.md`'s bundled-scripts disclaimer (now seven scripts, not six);
`pixel-art-storyboard/SKILL.md`'s "Baking finished animations" section and reference-index table
row; and three `pixel-art-storyboard` reference files —
`references/smoother-animation-baking.md` (reverted the "not available" framing note, restored
the literal upstream example commands with the `../pixel-art-studio/scripts/` relative path and
`localhost`-only URLs), `references/high-detail-pipeline.md` (Stage 5's `--base-image` example),
and `references/element-library-scaling-architecture.md` (Step 8's diagram note). `SECURITY.md`'s
"Reviewed-script lane" and "Rejected scripts" sections were updated to describe the current state
(one script now standing-rejected — `gemini-switch.sh` — rather than two) and to introduce the
`modifications` field convention. Every corresponding `scripts/sync_upstream.py`
`adapt_source_text()` override was regenerated to match, verified via
`converted_output_matches_supported()`.

Full verification: `python3 -m py_compile scripts/*.py` OK; `python3 scripts/validate_output.py`
-> Validation OK; `converted_output_matches_supported()` -> True; disposable
`install_hermes.py --apply` copied `bake_animation.py` byte-identically (SHA-256 verified against
the modified script's hash); `remove_hermes.py --apply` removed it cleanly.

Released as **v0.3.71** (commit `a4d8633`, CI `Validate adapter` green, release:
https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/releases/tag/v0.3.71).

## Open decisions

1. Should the adapter eventually ship templates, or only skills?
2. Should support files from upstream skill packages be copied under generated skills, or kept as references in this repository only?
3. Should any upstream hook become a Hermes plugin, or should hooks stay as design references?
4. Should workflow JS become Hermes scripts, scheduled protocols, or merely documented patterns?
5. Should `PORTING_BACKLOG.md` be regenerated on every upstream sync, or maintained manually as a human-curated roadmap?

## Review-finding tracking

Independent review findings are tracked in GitHub Issues with the
[`review-finding` label](https://github.com/hermes-jarvis-bot/hermes-agent-config-kit/issues?q=is%3Aissue%20label%3Areview-finding).

- An Issue is the canonical record for the finding, independent verification,
  triage, commit/CI evidence, and closure decision.
- Before closing a finding, add a structured Issue comment containing the
  reproduction or non-reproduction result, fixing commit, and verification
  evidence. Use `Fixes #<issue>` only when the commit actually resolves it.
- `PORTING_BACKLOG.md` records only durable roadmap decisions: Waves, release
  state, candidate scope, and a finding's lasting impact on those decisions.
  It must not duplicate per-Issue closure reports or dynamic status updates.
- Historical closure evidence formerly embedded here has been migrated to
  Issues #2–#9, #16, #18–#20. The Issues retain the original finding text and
  the migrated evidence comments.

The scheduled protocol must triage open `review-finding` Issues first. It must
not create or close an Issue merely from an upstream report; findings remain
review input until independently verified against current code.

## Upstream lockfile integrity note (`skills-lock.json`, not this repo's file)

Checked 2026-07-11 against the live installed upstream plugin checkout at
`/root/claude-code-config` (commit `71863de`, the same SHA pinned in this repo's
`upstream.lock.json`). This is a note about *upstream's own* lockfile, not a defect
in this adapter — recorded here only because it affects how much trust to place in
upstream provenance signals when reviewing future sync candidates.

Upstream ships `scripts/generate_skills_lock.py`, which hashes each `skills/*`
package (`SKILL.md` + `references/` + `scripts/`) into `skills-lock.json` and offers
a `--check` mode wired into upstream's own CI (`.github/workflows/skills-lock-check.yml`)
to catch skill edits that weren't accompanied by a lock regeneration.

Running that `--check` against the live checkout fails:

```
python3 scripts/generate_skills_lock.py --check
→ [skills-lock] DRIFT DETECTED — 30 of 33 skills changed
```

Skill inventory itself is fine — all 33 `skills-lock.json` entries match the 33
`SKILL.md` directories on disk (both in the plugin checkout and in the installed
`~/.claude/skills/`); nothing is missing or orphaned.

The hash mismatch is not recent drift from an uncommitted edit, though:

- `git log` on `skills/` after the lock's `generated_at` timestamp shows exactly one
  commit (`cc00f61`, adding `ml-research-lab`) — and that is the one skill whose
  hash *does* match.
- Recomputing the hash directly from git blobs at the commit the lock claims to have
  been generated from (`00ab6a1`), with no working-tree checkout involved, still
  shows 31 of 32 pre-existing skills mismatching what `skills-lock.json` recorded
  *in that same commit*.
- `scripts/generate_skills_lock.py` has only ever been touched once (`1e84627`, the
  commit that introduced it) — so this isn't algorithm drift either.

Conclusion: upstream's `skills-lock.json` appears to have never actually been
produced by running `generate_skills_lock.py` against the tree it was committed
with — it looks hand-patched (count/aggregate/one new entry bumped) rather than
regenerated on each change. Treat it as decorative, not as a real integrity
guarantee, when using upstream's lockfile state as input to future review decisions.
No action needed in this repo; nothing here is portable or fixable from our side.

## Handoff protocol for the next agent

Before porting anything from this backlog:

1. Read `SECURITY.md`, `INSTALL.md`, `AGENTS.md`, and this file.
2. Run:

   ```bash
   git status --short --branch
   python3 scripts/sync_upstream.py --check
   python3 scripts/validate_output.py
   ```

3. Pick one small wave item. Do not mix hooks, templates, and skills in one PR unless the operator explicitly asks.
4. Update all of these together:

   - `scripts/sync_upstream.py:SUPPORTED` for auto-converted artefacts;
   - `mappings/compatibility.yaml` for policy;
   - generated `hermes/` artefacts;
   - this backlog if scope changes.

5. Run local validation and disposable `HERMES_HOME` install/remove.
6. If executable code is introduced, add focused tests and document the threat model.
7. Never install into a production Hermes profile without explicit operator confirmation for the exact path.
