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
| `principles/` | 30 | 29 | 1 |
| `references/` | 1 | 0 | 1 |
| `rules/` | 30 | 25 | 5 |
| `scripts/` | 35 | 0 | 35 |
| `skills/` | 159 | 28 | 131 |
| `templates/` | 47 | 13 | 34 |
| `workflows/` | 5 | 0 | 5 |
| **Total** | **394** | **95** | **299** |

## Ported so far

The adapter intentionally auto-converts only selected markdown-only material into Hermes skills:

| Upstream source | Hermes target |
| --- | --- |
| `skills/ai-ml/ml-research-lab/SKILL.md` | `hermes/skills/ai-ml/ml-research-lab/SKILL.md` |
| `skills/video-production/script-evaluator/SKILL.md` | `hermes/skills/video-production/script-evaluator/SKILL.md` |
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

These were chosen because they are broadly useful, markdown-centric, and can be adapted without executing upstream code or assuming Claude Code hook APIs.

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
- `rules/moa-gemini-delegation-eval.md`
- `rules/no-pre-existing-evasion.md`
- `rules/rlm-context-as-program.md`
- `rules/safety-hooks.md`

No remaining rule is a clear low-risk auto-conversion candidate. `rules/long-run-harness.md` overlaps `long-run-feature-tracking`; `rules/moa-gemini-delegation-eval.md` and `rules/rlm-context-as-program.md` require provider or orchestration review; `rules/safety-hooks.md` remains executable-adjacent and quarantined.

## Skill packages not yet ported

Upstream contains 145 skill-package files left out of MVP. Some are complete skills, some are support files, examples, scripts, templates, images, palettes, and references.

Top-level skill packages left out:

- `skills/agent-harness-design/`
- `skills/ai-ml/diffusion-engineering/`
- `skills/ai-ml/flux2-klein-prompting/`
- `skills/ai-ml/flux2-lora-training/`
- `skills/ai-ml/forensic-prompt-compiler/`
- `skills/ai-ml/vlm-segmentation/`
- `skills/architecture/feature-new/`
- `skills/architecture/harness-design/`
- `skills/architecture/layer-new/`
- `skills/architecture/plan-swarm-review/`
- `skills/creative/pixel-art-storyboard/`
- `skills/creative/pixel-art-studio/`
- `skills/development/distill-feedback/`
- `skills/development/proof-verify/references/kb-aware-verification.md` (reference remains separately reviewed and unported)
- `skills/development/repo-map/`
- `skills/development/workflow-orchestration/` (the markdown `SKILL.md` is ported; references, JavaScript template, and validation script remain unported and quarantined)

- `skills/operational/desktop-sessions-discovery/`
- `skills/operational/gemini-delegate/`
- `skills/video-production/product-meaning-extractor/`
- `skills/video-production/remotion-production-guide/`

- `skills/video-production/video-narrative-arc/`
- `skills/video-production/video-post-production/`
- `skills/writing/humanize-english/`
- `skills/writing/humanize-russian/`

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
- The approved domain queue is exhausted. Do not select another domain skill automatically;
  an operator must designate the next candidate.
- **Vetted-and-pending domain candidates (2026-07-13; mechanically clean and leak-clean,
  awaiting an operator scope/priority pick):** video-production — `video-narrative-arc`,
  `product-meaning-extractor`, `remotion-production-guide`, `video-post-production`; ai-ml —
  `vlm-segmentation` (4-file), `diffusion-engineering` (7-file), `flux2-lora-training`.
- **Manual-review-only (policy), NOT auto-port:** `skills/ai-ml/forensic-prompt-compiler/`
  — a high-fidelity image→prompt reconstructor (risk of replicating third-party images or a
  specific identity; it carries an "identity-safe" mitigation but the capability is
  dual-use), and `skills/ai-ml/flux2-klein-prompting/` (`api_key` policy flag). Both need a
  product/policy decision before any port.
- `skills/development/distill-feedback/`,
  `skills/operational/desktop-sessions-discovery/` — carry `.py` scripts; quarantined,
  manual-review-only.

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
| Latest released tag | `v0.3.23` |
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
