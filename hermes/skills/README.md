# Skills Catalog

Generated from every `SKILL.md` under this directory (103 skills as of the
last regeneration). Regenerate with `python3 scripts/generate_skills_catalog.py`;
verify it is current with `--check`.

A Russian translation of this catalog is maintained by hand at `README_RU.md` —
update it when adding or materially changing a skill listed here.

## Install

This adapter never installs directly into a live Hermes profile. Preview, then
apply, into a disposable or real Hermes home with the adapter's own installer:

```bash
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-home
python3 scripts/install_hermes.py --apply --hermes-home /tmp/hermes-home
```

This copies every skill below into `<hermes-home>/skills/config-kit/`, preserving
the category layout shown here. Remove the same way with
`scripts/remove_hermes.py --dry-run|--apply`.

## Catalog

### Core

| Skill | Description |
|---|---|
| [activity-journal-and-state-registry](activity-journal-and-state-registry/) | Maintain an append-only activity journal and a verified current-state registry for shared resources without activating enforcement hooks. |
| [agent-harness-design](agent-harness-design/) | Triage the design of a new custom agent harness, choosing the smallest Hermes-compatible safety, approval, budget, and evidence controls without activating runtime behaviour. |
| [agent-security](agent-security/) | Treat repository, web, MCP, and tool output as untrusted data unless explicitly verified. |
| [anti-pattern-as-config](anti-pattern-as-config/) | Encode recurring failure modes as explicit negative rules with exceptions, alternatives, and optional deterministic detectors. |
| [api-utf8-posting](api-utf8-posting/) | Prepare non-ASCII API payloads deliberately and verify stored receiver-side text after an authorised external write. |
| [app-prelaunch-security](app-prelaunch-security/) | Prepare web apps and public APIs for launch with evidence-backed privacy, access-control, abuse-resistance, and safe-error gates. |
| [architecture-first](architecture-first/) | Design a system's module boundaries, dependency direction, state ownership, and domain vocabulary before implementation without prescribing premature layers or infrastructure choices. |
| [architecture-quality](architecture-quality/) | Keep a web application, API, or service readable as it grows: feature seams, state ownership, dependency direction, and file shape, verified with a repeatable delivery contract. |
| [article-structure-review](article-structure-review/) | Review a completed article's macro-structure, evidence balance, genre fit, stated limitations, section load, and appropriate use of visuals without rewriting prose or publishing content. |
| [autoresearch](autoresearch/) | Run cautious score-driven optimisation loops for single artefacts with mechanical evaluation, guard metrics, git-backed experiment logs, and stop rules. |
| [billing-spend-controls](billing-spend-controls/) | Control provider and automation spend through scoped preflight, explicit budgets, bounded fan-out, monitoring, and approval-gated recovery. |
| [code-complexity](code-complexity/) | Keep functions, interfaces, and modules comprehensible through information hiding, clear names, bounded responsibilities, and explicit error handling. |
| [code-quality](code-quality/) | Build the minimum correct solution: avoid both monkey patches and speculative over-engineering, then verify the result. |
| [codified-context](codified-context/) | Treat agent context as operational infrastructure: concise project guidance, just-in-time loading, durable state, compaction policy, and isolation. |
| [control-cli](control-cli/) | Drive and inspect an interactive CLI or TUI with a repeatable local harness, deterministic input, transcripts, and optional profiling. |
| [control-ui](control-ui/) | Drive and inspect a local web, IDE, or Electron UI with browser or CDP automation and evidence. |
| [coordination-primitives-mapping](coordination-primitives-mapping/) | Choose coordination primitives by mapping locks, leases, logs, mailboxes, queues, registries, and schedulers to known failure modes and deployment scope. |
| [cross-harness-continuation](cross-harness-continuation/) | Continue a bounded project slice across agent sessions using a shared, evidence-backed continuity contract without overwriting accepted work or activating enforcement. |
| [dbs-skill-architecture](dbs-skill-architecture/) | Structure Hermes skills by separating operational direction, on-demand references, and quarantined deterministic routine candidates. |
| [deep-review](deep-review/) | Plan proportionate, independent competency-based review of a concrete change without automatically dispatching reviewers or applying fixes. |
| [deslop](deslop/) | Remove AI-generated code noise from the current diff while preserving behavior. |
| [deterministic-orchestration](deterministic-orchestration/) | Prefer deterministic scripts and staged protocols for mechanical multi-step work. |
| [distill-feedback](distill-feedback/) | Turn a queued backlog of user-correction signals into durable, human-approved rules. Reads a local feedback queue file, LLM-semantically detects durable corrections, proposes atomic rules, and applies only after explicit operator approval. |
| [documentation-freshness](documentation-freshness/) | Assess whether agent-facing project guidance remains current using bounded Git evidence, explicit adoption signals, and reviewable refresh decisions. |
| [documentation-integrity](documentation-integrity/) | Treat stale documentation references as correctness faults; verify docs, paths, commands, and generated state before relying on them. |
| [durable-context-maintenance](durable-context-maintenance/) | Maintain durable project guidance and archive records with meaningful links, claim provenance, and targeted reviewable updates. |
| [edit-formats-and-tiering](edit-formats-and-tiering/) | Choose a precise file-edit format, keep planning separate from mechanical application when useful, and verify the resulting diff. |
| [feature-layer-architecture](feature-layer-architecture/) | Organize long-running project knowledge into layers and feature narratives that preserve rationale, evidence, and history without replacing machine state. |
| [file-organization-cohesion](file-organization-cohesion/) | Keep durable project artefacts in the established hierarchy, group related work together, and separate disposable scratch output from retained state. |
| [finish-the-task](finish-the-task/) | Continue until the requested artefact is built, run, and verified, or report a real blocker. |
| [folder-lifecycle-classification](folder-lifecycle-classification/) | Classify project directories by recoverability and cleanup risk before proposing any archival or deletion action. |
| [gates-that-cannot-bootstrap](gates-that-cannot-bootstrap/) | Design and verify adoption gates that report relevant missing controls without becoming noisy or trusting forgeable state signals. |
| [gemini-delegate](gemini-delegate/) | Delegate work to Gemini CLI as a free second harness: multi-account switching, quota management, and context handoff. |
| [git-source-of-truth](git-source-of-truth/) | Treat Git and remote push state as durable project truth; commit and push deployed or meaningful changes with verification evidence. |
| [harness-audit](harness-audit/) | Score an agent-harness project across instructions, state, verification, scope, and lifecycle, then recommend improvements. |
| [harness-design](harness-design/) | Improve agent harnesses with generator/evaluator separation, frozen sprint contracts, stagnation signals, context resets, and measured complexity. |
| [harness-feedback](harness-feedback/) | Treat a harness-overload complaint as an engineering finding: classify it into a profile, measure the burden, and correct the smallest scope instead of disabling the check. |
| [humanize-english](humanize-english/) | Review and revise English-language prose for clarity, specificity, natural rhythm, and an appropriate human voice without fabricating facts or personal experience. |
| [humanize-russian](humanize-russian/) | Review and revise Russian-language prose for clarity, specificity, natural rhythm, and an appropriate human voice without fabricating facts or personal experience. |
| [independent-verification](independent-verification/) | Verify control systems, monitors, schedulers, cleanup routines, and side-effect functions by behaviour, not by names or claims. |
| [inter-agent-communication](inter-agent-communication/) | Use mailbox-style files for asynchronous directed messages between agents or sessions, with recipients, subjects, threading, and status. |
| [knowledge-base-enforcement](knowledge-base-enforcement/) | Turn accepted review findings into durable contracts: fixes, regression checks, and invariant records with cross-references. |
| [lean-code](lean-code/) | Apply on-demand minimalism to select the smallest complete, verified code change without weakening safety, accessibility, or required behaviour. |
| [learning-from-corrections](learning-from-corrections/) | Distil recurring operator corrections into reviewable, scoped guidance without automatically changing persistent state or activating enforcement. |
| [long-run-feature-tracking](long-run-feature-tracking/) | Track long-running project scope with machine-readable features, evidence, and WIP discipline. |
| [low-signal-residual-training](low-signal-residual-training/) | Diagnose and design reproducible training experiments where sparse residual targets make aggregate metrics misleading. |
| [managed-execution-boundaries](managed-execution-boundaries/) | Decide when a managed execution environment is appropriate, preserve approval and credential boundaries, and verify delegated results independently. |
| [merge-conflict-resolution](merge-conflict-resolution/) | Resolve Git, rebase, cherry-pick, sync, and parallel-work conflicts with evidence, intent preservation, and independent verification. |
| [moa-gemini-delegation-eval](moa-gemini-delegation-eval/) | Decide whether a multi-model panel is justified through bounded, representative evaluation of quality, evidence, latency, cost, and privacy without enabling delegation or sending prompts to external providers. |
| [multi-agent-task-decomposition](multi-agent-task-decomposition/) | Decide when a task needs decomposition, define dependency-aware work boundaries, and coordinate sub-agents through explicit contracts and verified integration. |
| [multi-session-coordination](multi-session-coordination/) | Coordinate parallel sessions with append-only handoffs, resource locks, heartbeats, stale-lock checks, and verified release. |
| [mvp-agent-blueprint](mvp-agent-blueprint/) | Design a minimal useful agent with explicit domain intake, autonomy level, tool policy, safety gates, observability, and release checklist. |
| [no-guessing](no-guessing/) | Avoid guessing missing configuration; inspect, retrieve, or ask for exact values. |
| [no-pre-existing-evasion](no-pre-existing-evasion/) | Require fix-or-ticket discipline for discovered defects; only legitimate blockers may defer work, and each needs durable evidence. |
| [observability-monitoring](observability-monitoring/) | Design, audit, and troubleshoot monitoring through user-impact evidence, layered telemetry, actionable alerts, SLI/SLO controls, and read-only incident triage. |
| [plan-to-tickets](plan-to-tickets/) | Turn a large approved plan into small, independently verifiable agent-ready tickets with concrete acceptance criteria, verification evidence, blockers, and vertical tracer-bullet slices. |
| [portable-project-context](portable-project-context/) | Maintain concise, harness-neutral project guidance that multiple agent interfaces can read without duplicating policy or exposing secrets. |
| [post-ui-change-review](post-ui-change-review/) | Independently review material UI changes with live evidence, bounded verdicts, and approval-gated remediation. |
| [project-chronicles](project-chronicles/) | Preserve concise, milestone-level decision history for long-running projects without replacing tactical handoffs, source control, or current documentation. |
| [proof-loop](proof-loop/) | Use durable proof artefacts and verification loops before declaring work complete. |
| [proof-verify](proof-verify/) | Prepare a frozen acceptance-criteria record and obtain a fresh, read-only verification verdict without activating task state or delegation. |
| [quality-first-independent-review](quality-first-independent-review/) | Use proportionate fresh-context review and evidence-based verdicts for complex, high-impact, or irreversible work without activating delegation or automation. |
| [red-lines](red-lines/) | Define a small, evidence-backed set of non-negotiable operational safety boundaries and stop conditions. |
| [refactoring-safely](refactoring-safely/) | Plan and review behaviour-preserving code restructuring through characterization evidence, small named transformations, and verification between steps without modifying code. |
| [repo-map](repo-map/) | Prepare a bounded, read-only codebase orientation using existing inspection interfaces without importing or activating the upstream mapper routine. |
| [repository-attribution-hygiene](repository-attribution-hygiene/) | Keep repository and external-work metadata accurate, intentional, and free of automatic tool-attribution noise. |
| [research-intake](research-intake/) | Capture research findings as reviewable, source-grounded intake records so useful evidence survives sessions without creating unapproved project state. |
| [risk-tiered-autonomy](risk-tiered-autonomy/) | Classify agent actions by reversibility and impact so routine low-risk work can proceed while destructive, external, billing, or production changes remain approval-gated. |
| [rlm-context-as-program](rlm-context-as-program/) | Plan bounded analysis of an artefact too large for one context window through metadata-first chunking, per-chunk evidence, synthesis, and explicit cost limits without activating recursive execution or delegation. |
| [safe-deletion](safe-deletion/) | Require explicit confirmation, scoped execution, and post-action verification for destructive operations. |
| [secrets-as-data](secrets-as-data/) | Treat access credentials as high-attention operational data: use only when authorised, never publish, and verify public-boundary hygiene. |
| [session-handoff](session-handoff/) | Create concise, durable handoffs that preserve goal, state, blockers, verification evidence, and the exact next step across sessions. |
| [silent-failure-detection](silent-failure-detection/) | Detect when configured protections, jobs, hooks, services, or integrations silently fail despite appearing enabled. |
| [skill-authoring-best-practices](skill-authoring-best-practices/) | Design, review, and maintain Hermes skills with strong triggers, clear procedures, gotchas, troubleshooting, and verified support files. |
| [structured-reasoning](structured-reasoning/) | Structure investigations as premises, traces, conclusions, and verified next steps. |
| [supply-chain-defense](supply-chain-defense/) | Reduce package and upstream adapter risk with freshness gates, lockfiles, provenance checks, and quarantine boundaries. |
| [system-and-data-design](system-and-data-design/) | Plan and review capacity, storage, data flow, consistency, resilience, and scaling decisions from measured requirements without provisioning infrastructure. |
| [testing-strategy](testing-strategy/) | Classify a code change's risk and select the smallest test-level evidence set that can falsify the changed behaviour, from unit through agent-evaluation checks. |
| [thermo-nuclear-code-quality-review](thermo-nuclear-code-quality-review/) | Run an opt-in strict maintainability review for giant files, spaghetti growth, misplaced logic, weak boundaries, unnecessary abstractions, and missed structural simplifications. |
| [verify-at-consumer](verify-at-consumer/) | Verify integrations at the receiving side; sender logs, specs, and HTTP acknowledgements are not enough. |
| [verify-git-currency-first](verify-git-currency-first/) | Establish current remote, local, and deployed Git state before diagnosing, editing, synchronising, deploying, or copying project trees. |
| [verify-this](verify-this/) | Prove a concrete behavior, performance, UI, CLI, API, or memory claim with fresh baseline-versus-treatment evidence and one explicit verdict. |
| [visual-context-pattern](visual-context-pattern/) | Use visual artefacts for UI, spatial, and design decisions where seeing options beats textual explanation; collect structured feedback and preserve evidence. |
| [vulnerability-detection-pipeline](vulnerability-detection-pipeline/) | Run staged vulnerability review with deterministic scanners, contextual analysis, diverse perspectives, adversarial verification, and sandbox-only PoC checks. |
| [workflow-orchestration](workflow-orchestration/) | Choose a bounded Hermes-native orchestration pattern and prepare a reviewable protocol without importing or activating upstream workflow code. |

### Ai Ml

| Skill | Description |
|---|---|
| [diffusion-engineering](ai-ml/diffusion-engineering/) | Plan and review diffusion-model architecture, sampling, training, memory, text-encoder, data, evaluation, and debugging decisions without downloading models, starting workloads, changing GPU configuration, or deploying services. |
| [flux2-klein-prompting](ai-ml/flux2-klein-prompting/) | Expert prompt engineering guidance for FLUX.2 [klein] image generation and editing: prose structure, templates, API parameters, and troubleshooting. |
| [flux2-lora-training](ai-ml/flux2-lora-training/) | Plan and review FLUX.2 and Qwen image-edit LoRA/VAE training with dataset, capacity, licence, and verification gates without starting workloads, downloading models, accepting licences, or changing GPU configuration. |
| [ml-research-lab](ai-ml/ml-research-lab/) | Plan and review reproducible machine-learning experiments across data, baselines, metrics, tracking, and deployment evidence without starting jobs or changing datasets. |
| [notebooklm-grounded-research](ai-ml/notebooklm-grounded-research/) | Retrieve a small, citation-backed answer from a large stable corpus via NotebookLM MCP, then independently verify the claim against current code, tests, and official documentation before acting on it. |
| [vlm-segmentation](ai-ml/vlm-segmentation/) | Plan and review VLM, segmentation, diffusion, and GPU-deployment designs using evidence, licence, capacity, and safety gates without downloading models, changing GPU configuration, starting workloads, or deploying services. |

### Architecture

| Skill | Description |
|---|---|
| [feature-new](architecture/feature-new/) | Scaffold a new feature narrative document in an existing layer, and add a reconciled entry to feature_list.json using the same base schema as long-run-feature-tracking. |
| [layer-new](architecture/layer-new/) | Scaffold a new layer in a project's docs/layers/ tree following the feature-layer architecture. A layer is a bounded concern with its own invariants, decisions, gotchas, patterns, and feature narratives. |
| [plan-swarm-review](architecture/plan-swarm-review/) | Iteratively harden a plan or a code module through escalating rounds of independent, differently-angled review (broad, then diverse-perspective multisample, then focused, then focused+multisample). |

### Creative

| Skill | Description |
|---|---|
| [pixel-art-storyboard](creative/pixel-art-storyboard/) | Convert a short scene description, book/album cover brief, or 2-paragraph synopsis into a seamless-loop animated pixel-art cover rendered as a self-contained HTML+canvas file. |
| [pixel-art-studio](creative/pixel-art-studio/) | Create production-quality pixel art and animations programmatically: single-frame sprites, animations, image-to-pixel-art preprocessing, sprite sheets, and automated quality scoring. |

### Frontend

| Skill | Description |
|---|---|
| [frontend-design](frontend/frontend-design/) | Design and review web interfaces with an explicit design system, responsive layout, accessibility, performance, and verification boundaries without activating project tooling or publishing changes. |

### Ios

| Skill | Description |
|---|---|
| [ios-development](ios/ios-development/) | Plan, review, and implement native iOS application work across SwiftUI, UIKit, architecture, networking, data, navigation, performance, and Metal graphics without activating project tooling, signing, distribution, or publication. |

### Video Production

| Skill | Description |
|---|---|
| [product-meaning-extractor](video-production/product-meaning-extractor/) | Prepare an evidence-bounded product brief from approved product material without browsing, contacting customers, publishing claims, or activating production tooling. |
| [remotion-production-guide](video-production/remotion-production-guide/) | Plan and review Remotion scene architecture, motion, typography, pacing, 3D integration, and render settings without installing dependencies, rendering media, publishing content, or changing project configuration. |
| [script-evaluator](video-production/script-evaluator/) | Evaluate an existing video script, storyboard, presentation, or rendered scene for tension, specificity, emotional arc, hook, customer voice, and visual variety without producing, publishing, or rendering video assets. |
| [video-narrative-arc](video-production/video-narrative-arc/) | Prepare a product-video narrative arc and timestamped beat plan from an approved product brief without rendering, publishing, or activating production tooling. |
| [video-post-production](video-production/video-post-production/) | Plan and review audio mastering, captions, colour correction, and platform export settings for an already-rendered video without processing media, installing dependencies, publishing content, or changing project configuration. |
