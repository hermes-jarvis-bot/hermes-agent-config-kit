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
| `principles/` | 29 | 29 | 0 |
| `references/` | 1 | 0 | 1 |
| `rules/` | 30 | 25 | 5 |
| `scripts/` | 26 | 0 | 26 |
| `skills/` | 159 | 1 | 158 |
| `templates/` | 47 | 2 | 45 |
| `workflows/` | 5 | 0 | 5 |
| **Total** | **382** | **57** | **325** |

## Ported so far

The adapter intentionally auto-converts only selected markdown-only material into Hermes skills:

| Upstream source | Hermes target |
| --- | --- |
| `skills/operational/harness-audit/SKILL.md` | `hermes/skills/harness-audit/SKILL.md` |
| `templates/proof-plan.md` | `hermes/templates/proof-plan.md` |
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

One low-risk upstream template has been adapted with Hermes-native provenance and
operator-confirmation wording: `templates/proof-plan.md` ->
`hermes/templates/proof-plan.md`. The installer copies it only into the isolated
`<hermes-home>/templates/config-kit/` namespace and the remover deletes only that
namespace. The remaining template categories stay out of MVP:

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
  - remaining `templates/agent-task/*` artefacts after separate review
- Knowledge-base skeleton:
  - `templates/kb-skeleton/*`
- Long-run project skeleton:
  - `templates/long-run-project/*`

Reason: template installation raises path, naming, lifecycle, and overwrite questions. It needs a Hermes-native template target and removal contract.

High-value next candidates:

1. `templates/agent-task/` — useful for multi-agent/delegation task handoff.
2. `templates/long-run-project/` — useful for feature tracking.
3. `templates/kb-skeleton/` — useful, but includes workflow/script files and must remain reviewed.

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
| Active Wave | Wave 2 — support files and templates |
| Active release line | `0.2` |
| Latest released tag | `v0.2.0` (created for this accepted artefact) |
| `upstream.lock.json` `adapter.version` | `0.2.0` (Wave 2 baseline, not a patch-release counter) |
| Historical classification of `templates/proof-plan.md` | Wave 1 close-out; its `v0.1.40` release did not start Wave 2 |
| Exact Wave 2 trigger | First accepted and verified `templates/agent-task/*` artefact |
| First Wave 2 version | `v0.2.0`, with `adapter.version` updated to `0.2.0` in that same commit |

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

Status: active. The exact Wave 2 trigger was satisfied by the first accepted,
verified `templates/agent-task/*` artefact: `templates/agent-task/spec.md` ->
`hermes/templates/agent-task-spec.md`. It remains a markdown-only, data-only
template in the existing scoped installer/remover namespace; no task state,
hooks, scripts, or automation were activated.

Candidates:

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

## External review findings (as of commit `f10d655`, verify before trusting)

An external reviewer (not this repo's own autonomous porting run) audited
`scripts/sync_upstream.py` at commit `f10d655`. This is *review input to verify
independently*, in the same spirit as this adapter's own stance on upstream content:
data to check, not automatic authority. Line numbers below drift every time
`SUPPORTED` grows (the file has grown from ~3100 to ~4200 lines across recent porting
commits) — re-grep the function names rather than trusting the numbers.

**Priority — breaks the adapter's core provenance guarantee:**

1. `main()` (grep `if base == head and SNAPSHOT.exists()`, near end of file): `--sync`
   short-circuits whenever the upstream SHA hasn't moved, **without checking whether
   `SUPPORTED` or `mappings/compatibility.yaml` changed**. Evidence this already bit
   the repo: most recently-ported skills have no matching `reports/upstream-sync/`
   entry or lockfile advance — they were hand-authored directly into `hermes/skills/`
   in the same commits that edited `SUPPORTED`, because an actual `--sync` run at the
   same upstream SHA would have silently no-op'd. This undermines the "every generated
   skill traces to a recorded, reviewed sync" property the whole adapter exists to
   provide. Verify independently: `ls reports/upstream-sync/ | wc -l` vs. `git log
   --oneline -- hermes/skills | wc -l`.

**Secondary — real but lower blast radius:**

2. `write_report()`: under-reports if `--sync` is forced at an unchanged SHA (e.g. by
   deleting the snapshot to work around #1) — GitHub's compare API returns empty
   commits/files, and the empty-fallback branch (`if not files and not base`) doesn't
   fire because `base` is non-empty, so the report claims 0 changed files despite a
   full conversion having run.

Status (2026-07-11): **confirmed and closed**. Current-code inspection reproduced
the empty compare-data path after a forced snapshot refresh at an unchanged SHA. The
report now receives an explicit refresh signal and enumerates the refreshed snapshot
when compare data is empty. Focused ad-hoc verification asserts a non-zero snapshot
file count and classification for that path (`Fixes #9`).
3. `download_snapshot()`: `rmtree` + `copytree` with no atomic swap/completion marker
   — a killed run can leave a truncated snapshot that `SNAPSHOT.exists()` still treats
   as complete, compounding #1's short-circuit.
4. `save_lock()`: writes `upstream.lock.json` directly via `write_text`, no
   temp-file+rename — a kill mid-write can corrupt the lockfile and break every
   subsequent invocation, including `--check`.
5. `gh_api()`: runs `gh` with `stderr=subprocess.STDOUT`, so a stderr warning can
   corrupt the JSON it parses; currently masked by a broad `except Exception` fallback
   to the unauthenticated, 60-req/hr GitHub REST API path.

Status (2026-07-11): **confirmed and closed**. Current-code inspection reproduced
`run(..., stderr=subprocess.STDOUT)` and the broad fallback. The transport now captures
stdout and stderr separately, parses stdout only, falls back only after a missing or
failed `gh` invocation, and raises a labelled fault for malformed `gh` JSON. Focused
ad-hoc verification covers stderr isolation, valid authenticated JSON, failed-command
fallback, and malformed-JSON non-fallback (`Fixes #8`).
6. `convert_supported()`: silently skips (`if not src.exists(): continue`) a
   `SUPPORTED` entry whose upstream source file no longer exists — no warning in the
   report or exit code, so a generated skill can go stale with zero signal.

Cross-file consistency was re-checked at commit `f10d655` and currently holds: the
`SUPPORTED` dict, `mappings/compatibility.yaml`'s `status: supported` count,
`hermes/skills/*` directories, and `AGENTS.md`'s skill list all agree (50 as of this
commit). This agreement is accidental/hand-maintained, not enforced by any script —
don't treat it as a guarantee for future commits (see finding 1).

No fix is applied here. Recommended: pick finding 1 as the next single-artefact
task (fix the short-circuit to also diff `SUPPORTED`/`mappings/compatibility.yaml`
against what's already reflected in `hermes/skills/`), log it as a real fix rather
than silently working around it, per this repo's own no-pre-existing-evasion stance.

Status (2026-07-11): **confirmed and closed**. Current-code inspection reproduced
the SHA-only short-circuit. The condition now also requires every supported source to
match its generated target byte-for-byte under the current conversion policy; a
missing or stale target forces a complete sync/report path. Focused ad-hoc verification
exercises the stale-output branch before this status is recorded.

## Review findings 2026-07-11 (second pass — verify before trusting)

Independent second review. Same stance as everything inbound here: review input to
verify, not authority. Findings 1/4/6 below re-confirm the earlier "External review
findings" block against current code; 2/3/5 are new. Re-grep function names — line
numbers drift as SUPPORTED grows.

**Priority 1 — provenance (still open, evidence re-confirmed):**
1. `main()` `if base == head and SNAPSHOT.exists()` (~line 4201): `--sync` no-ops on an
   unchanged upstream SHA even when SUPPORTED/compatibility.yaml changed, so new skills
   never get a sync report or lockfile advance. Re-verified 2026-07-11:
   `ls reports/upstream-sync/*.md | grep -v latest | wc -l` = 2, but
   `ls hermes/skills | wc -l` = 50 — 48 skills have no recorded sync. Fix: gate the
   short-circuit on "converted output already matches SUPPORTED", not SHA equality.

Status (2026-07-11): **confirmed and closed**. Reproduced against the current
SHA-equality branch, then closed by the generated-output invariant and focused
ad-hoc stale-output sync verification described above.

**Priority 2 — installer/remover safety is convention-only, not enforced (NEW):**
2. `install_hermes.py` / `remove_hermes.py` accept any `--hermes-home` — including
   `~/.hermes`, `/root/.hermes`, or any live profile — and will `--apply` there. The
   repo's top red line ("never write to a production Hermes profile") has no code guard;
   `validate_output.py` only forbids the literal string as a *default*, not the runtime
   target. Fix: refuse known production paths (`~/.hermes`, `/root/.hermes`,
   `$HERMES_HOME`) unless an explicit `--i-know-this-is-production` override is passed;
   otherwise require the path to look disposable (`/tmp/…`, `*-test`, `*-sandbox`).
3. `--dry-run` is decorative in both scripts — defined, never read. `apply` derives only
   from `--apply`, so `--apply --dry-run` writes. Fix: make the two mutually exclusive
   (error out), or let `--dry-run` force dry-run regardless of `--apply`.

Status (2026-07-11): **confirmed and closed**. Independent pre-change probes accepted
`/root/.hermes` and showed that `--apply --dry-run` wrote into a disposable target.
Both installer interfaces now reject production and non-disposable targets unless the
explicit production override is supplied, and make `--apply` and `--dry-run` mutually
exclusive. Focused ad-hoc verification covers refusal, conflict rejection, disposable
dry-run/apply/remove, and the unchanged generated-output contract.

**Priority 3 — lower blast radius:**
4. `save_lock()` `write_text` (no temp+rename) → a killed run corrupts
   `upstream.lock.json`, breaking even `--check`. `download_snapshot()` `rmtree`+
   `copytree` with no completion marker → truncated snapshot still passes
   `SNAPSHOT.exists()`, compounding #1. Fix: temp-file+`os.replace`; write a
   `.sync-complete` marker and check it in the short-circuit.

Status (2026-07-11): **confirmed and closed**. Current-code inspection reproduced
both direct-write/replace sequences. `atomic_write_text()` now fsyncs a sibling
staging file before `os.replace`; snapshot refresh stages a complete copy, swaps it
with rollback to the previous snapshot on in-process failure, and writes a
SHA-matching `.sync-complete` marker. The unchanged-SHA short-circuit requires that
marker. Focused ad-hoc verification exercised marker mismatch, atomic snapshot
replacement, lock JSON readability, conversion stability, and disposable
install/remove.
5. `validate_output.py:validate_skills()` checks only `name`+`description`, not the
   documented `version`/`license`/`metadata.hermes_config_kit.*` frontmatter contract.
   A regressed skill passes CI. Fix: assert the full documented frontmatter shape.

Status (2026-07-11): **confirmed and closed**. A disposable current-code probe removed
`version` from a generated skill and the validator still returned success. The validator
now requires non-empty `name`, `description`, `version`, and `license`, plus the
`metadata.hermes_config_kit` mapping and its `source_repo`, `source_path`, `adapter`,
and `conversion` entries. Focused ad-hoc verification exercises each required-field and
metadata-mapping rejection path, then validates the unchanged generated set.

6. `convert_supported()` silently `continue`s past a SUPPORTED entry whose source file
   is gone — no report line, no exit code. Fix: collect missing sources, surface them
   in the report, and exit non-zero.

Status (2026-07-11): **confirmed and closed**. Current-code inspection reproduced
the silent skip. Conversion now preflights every supported source before writing any
generated target; a missing source is listed in the sync report and makes `--sync`
return non-zero without advancing the lockfile. Focused ad-hoc verification injects
a missing source in a disposable copy and checks the non-zero result, report entry,
unchanged lockfile, and unchanged generated output.

Recommended order for Codex: #1 (core guarantee) → #2/#3 (safety, small diffs) →
#4/#5/#6. One artefact per PR per this repo's commit-narrowness rule. Don't work
around #1 by deleting the snapshot — fix it and log it (no-pre-existing-evasion).

## Follow-up review finding: generated harness leakage (GitHub issue #16)

GitHub review finding **#16** reported upstream-specific paths and active-runtime
language in generated `harness-audit` and `agent-security` modules. It was
independently confirmed on 2026-07-11: regeneration from the current snapshot
produced `claude-code-skills/...` and an invalid transformed configuration path.
The source-specific adapters now emit Hermes-native read-only guidance, while
`validate_output.py` rejects the identified upstream harness-path/runtime
patterns across generated skills. Closure requires focused ad-hoc regeneration,
leakage, installer, and validator verification for the fixing commit.

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
