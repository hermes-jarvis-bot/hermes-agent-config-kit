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

Inventory from `upstream/claude-code-config/snapshot/` at the `v0.1.0` release:

| Area | Files in snapshot | Auto-ported in MVP | Left out |
| --- | ---: | ---: | ---: |
| Root docs/config | 10 | 0 | 10 |
| `.claude-plugin/` | 1 | 0 | 1 |
| `.github/` | 1 | 0 | 1 |
| `agents/` | 6 | 0 | 6 |
| `alternatives/` | 19 | 0 | 19 |
| `docs/` | 3 | 0 | 3 |
| `evals/` | 2 | 0 | 2 |
| `hooks/` | 42 | 0 | 42 |
| `principles/` | 30 | 12 | 18 |
| `references/` | 1 | 0 | 1 |
| `rules/` | 30 | 10 | 20 |
| `scripts/` | 26 | 0 | 26 |
| `skills/` | 159 | 1 | 158 |
| `templates/` | 47 | 0 | 47 |
| `workflows/` | 5 | 0 | 5 |
| **Total** | **382** | **23** | **359** |

## Ported so far

The adapter intentionally auto-converts only selected markdown-only material into Hermes skills:

| Upstream source | Hermes target |
| --- | --- |
| `skills/operational/harness-audit/SKILL.md` | `hermes/skills/harness-audit/SKILL.md` |
| `principles/02-proof-loop.md` | `hermes/skills/proof-loop/SKILL.md` |
| `principles/04-deterministic-orchestration.md` | `hermes/skills/deterministic-orchestration/SKILL.md` |
| `principles/05-structured-reasoning.md` | `hermes/skills/structured-reasoning/SKILL.md` |
| `principles/08-skills-best-practices.md` | `hermes/skills/skill-authoring-best-practices/SKILL.md` |
| `principles/09-supply-chain-defense.md` | `hermes/skills/supply-chain-defense/SKILL.md` |
| `principles/10-agent-security.md` | `hermes/skills/agent-security/SKILL.md` |
| `principles/11-documentation-integrity.md` | `hermes/skills/documentation-integrity/SKILL.md` |
| `principles/18-multi-session-coordination.md` | `hermes/skills/multi-session-coordination/SKILL.md` |
| `principles/19-inter-agent-communication.md` | `hermes/skills/inter-agent-communication/SKILL.md` |
| `principles/20-vulnerability-detection-pipeline.md` | `hermes/skills/vulnerability-detection-pipeline/SKILL.md` |
| `principles/21-knowledge-base-enforcement.md` | `hermes/skills/knowledge-base-enforcement/SKILL.md` |
| `principles/27-feature-tracking.md` | `hermes/skills/long-run-feature-tracking/SKILL.md` |
| `rules/no-guessing.md` | `hermes/skills/no-guessing/SKILL.md` |
| `rules/finish-the-task.md` | `hermes/skills/finish-the-task/SKILL.md` |
| `rules/git-source-of-truth.md` | `hermes/skills/git-source-of-truth/SKILL.md` |
| `rules/quality-code.md` | `hermes/skills/code-quality/SKILL.md` |
| `rules/deletion-confirm-and-verify.md` | `hermes/skills/safe-deletion/SKILL.md` |
| `rules/secrets-as-data.md` | `hermes/skills/secrets-as-data/SKILL.md` |
| `rules/session-handoff.md` | `hermes/skills/session-handoff/SKILL.md` |
| `rules/silent-failure-detection.md` | `hermes/skills/silent-failure-detection/SKILL.md` |
| `rules/system-verification-independent.md` | `hermes/skills/independent-verification/SKILL.md` |
| `rules/verify-at-consumer.md` | `hermes/skills/verify-at-consumer/SKILL.md` |

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

The following principles are markdown candidates. They were not included in MVP because they need deduplication against Hermes built-ins, scope decisions, or stronger product framing.

- `principles/01-harness-design.md`
- `principles/03-autoresearch.md`
- `principles/06-multi-agent-decomposition.md`
- `principles/07-codified-context.md`
- `principles/12-low-signal-residual-training.md`
- `principles/13-research-pipeline.md`
- `principles/14-managed-agents.md`
- `principles/15-red-lines.md`
- `principles/16-project-chronicles.md`
- `principles/17-dbs-skill-creation.md`
- `principles/22-visual-context-pattern.md`
- `principles/23-anti-pattern-as-config.md`
- `principles/24-merge-conflict-resolution.md`
- `principles/25-coordination-primitives-mapping.md`
- `principles/26-no-pre-existing-evasion.md`
- `principles/28-feature-layer-architecture.md`
- `principles/29-mvp-agent-blueprint.md`
- `principles/README.md`

High-value next candidates:

No principle candidates are currently singled out. Inspect the remaining principles one by one and deduplicate against existing Hermes skills before porting.

## Review lane: rules not yet ported

The following rules stayed out of MVP:

- `rules/activity-journal-and-state-registry.md`
- `rules/agent-docs-freshness.md`
- `rules/api-utf8-posting.md`
- `rules/app-prelaunch-security-checklist.md`
- `rules/autonomy-risk-tiers.md`
- `rules/cross-harness-agents-md.md`
- `rules/edit-formats-and-tiering.md`
- `rules/file-organization-cohesion.md`
- `rules/folder-lifecycle-labels.md`
- `rules/learn-from-corrections.md`
- `rules/long-run-harness.md`
- `rules/memory-maintenance.md`
- `rules/moa-gemini-delegation-eval.md`
- `rules/no-claude-attribution.md`
- `rules/no-pre-existing-evasion.md`
- `rules/post-ui-change-review.md`
- `rules/quality-over-tokens-independent-verify.md`
- `rules/rlm-context-as-program.md`
- `rules/safety-billing.md`
- `rules/safety-hooks.md`

High-value next candidates:

No rule candidates are currently singled out. Inspect the remaining rules one by one and deduplicate against existing Hermes skills before porting.

## Skill packages not yet ported

Upstream contains 158 skill-package files left out of MVP. Some are complete skills, some are support files, examples, scripts, templates, images, palettes, and references.

Top-level skill packages left out:

- `skills/agent-harness-design/`
- `skills/ai-ml/diffusion-engineering/`
- `skills/ai-ml/flux2-klein-prompting/`
- `skills/ai-ml/flux2-lora-training/`
- `skills/ai-ml/forensic-prompt-compiler/`
- `skills/ai-ml/ml-research-lab/`
- `skills/ai-ml/vlm-segmentation/`
- `skills/architecture/feature-new/`
- `skills/architecture/harness-design/`
- `skills/architecture/layer-new/`
- `skills/architecture/plan-swarm-review/`
- `skills/creative/pixel-art-storyboard/`
- `skills/creative/pixel-art-studio/`
- `skills/development/deep-review/`
- `skills/development/distill-feedback/`
- `skills/development/proof-verify/`
- `skills/development/repo-map/`
- `skills/development/workflow-orchestration/`
- `skills/frontend/frontend-design/`
- `skills/ios/ios-development/`
- `skills/lean-code/`
- `skills/operational/desktop-sessions-discovery/`
- `skills/operational/gemini-delegate/`
- `skills/plan-to-tickets/`
- `skills/video-production/product-meaning-extractor/`
- `skills/video-production/remotion-production-guide/`
- `skills/video-production/script-evaluator/`
- `skills/video-production/video-narrative-arc/`
- `skills/video-production/video-post-production/`
- `skills/writing/article-structure-review/`
- `skills/writing/humanize-english/`
- `skills/writing/humanize-russian/`

Special note: `skills/operational/harness-audit/SKILL.md` was ported, but its references were not:

- `skills/operational/harness-audit/references/checklist-per-subsystem.md`
- `skills/operational/harness-audit/references/scoring-rubric.md`

Recommended future treatment:

- Do not bulk-copy upstream skill directories.
- For each candidate, decide whether it should be:
  - a Hermes local skill;
  - a support file under `references/`, `templates/`, `scripts/`, or `assets/`;
  - split across existing Hermes skills;
  - rejected as duplicate or out-of-scope.
- Pay special attention to support scripts and binary/media assets inside skill packages.

High-value next candidates:

1. `skills/development/proof-verify/` — likely complements `proof-loop`.
2. `skills/development/repo-map/` — possible Hermes codebase-inspection helper if script is reviewed.
3. `skills/development/deep-review/` — possible code-review module after dedupe.
4. `skills/development/workflow-orchestration/` — possible Hermes delegation/kanban module.
5. `skills/writing/humanize-russian/` — relevant for Russian-language output, but should be reviewed against existing `humanizer`.
6. `skills/agent-harness-design/` — broad but potentially valuable as reference material.

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

No upstream templates were ported in MVP. Left out categories:

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
  - `templates/agent-task/*`
- Knowledge-base skeleton:
  - `templates/kb-skeleton/*`
- Long-run project skeleton:
  - `templates/long-run-project/*`

Reason: template installation raises path, naming, lifecycle, and overwrite questions. It needs a Hermes-native template target and removal contract.

High-value next candidates:

1. `templates/proof-plan.md` — likely maps to the `proof-loop` skill.
2. `templates/agent-task/` — useful for multi-agent/delegation task handoff.
3. `templates/long-run-project/` — useful for feature tracking.
4. `templates/kb-skeleton/` — useful, but includes workflow/script files and must remain reviewed.

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

## Recommended next porting waves

### Wave 1 — low-risk markdown modules

Goal: expand useful Hermes guidance without executable code.

Candidates:

No specific Wave 1 rule candidate is singled out at this point; inspect remaining rules one by one before porting.

Acceptance criteria:

- each item becomes a Hermes `SKILL.md` or is merged into an existing generated skill;
- `mappings/compatibility.yaml` and `scripts/sync_upstream.py:SUPPORTED` are updated together;
- generated skills include source attribution and Hermes-native wording;
- `validate_output.py` still passes;
- disposable `HERMES_HOME` install/remove test passes.

### Wave 2 — support files and templates

Goal: add selected templates without expanding execution risk.

Candidates:

- `templates/proof-plan.md`
- `templates/agent-task/*`
- `templates/long-run-project/*`
- harness-audit reference files

Acceptance criteria:

- installer/remover handle `templates/config-kit/` predictably;
- no executable scripts are installed without review;
- overwrite behaviour is documented and dry-run visible;
- removal contract remains narrow.

### Wave 3 — skill package review

Goal: port selected upstream skill packages as Hermes skills.

Candidates:

- `skills/development/proof-verify/`
- `skills/development/repo-map/`
- `skills/development/deep-review/`
- `skills/development/workflow-orchestration/`
- `skills/writing/humanize-russian/`
- `skills/agent-harness-design/`

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
4. Should `humanize-russian` become part of this kit, or remain out because Hermes already has a `humanizer` skill?
5. Should workflow JS become Hermes scripts, scheduled protocols, or merely documented patterns?
6. Should `PORTING_BACKLOG.md` be regenerated on every upstream sync, or maintained manually as a human-curated roadmap?

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
