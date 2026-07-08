---
name: long-run-feature-tracking
description: "Track long-running project scope with machine-readable features, evidence, and WIP discipline."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: principles/27-feature-tracking.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Long Run Feature Tracking

Source: `AnastasiyaW/claude-code-config/principles/27-feature-tracking.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# 21 - Feature Tracking: Machine-Readable Scope for Long-Run Projects

**Source:** [Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/) (walkinglabs, MIT license), Lectures 06-09.

## Overview

Long-running projects accumulate features across many sessions. Free-form notes ("we did A, then B, working on C") get scattered across handoffs and chronicles. After 10 sessions, nobody — human or agent — can answer the basic question: **how many features are done, which one is in progress right now, what depends on what.**

A `feature_list.json` with a strict schema fixes this. Each feature is an object with `id`, `name`, `description`, `dependencies[]`, `status`, and `evidence`. The agent reads it at session start, picks the active feature, works on it, updates evidence with verification artifacts, and transitions to `done`. The agent **cannot** put two features in `in-progress` simultaneously (WIP=1 invariant), and **cannot** mark `done` without populated evidence (Anti-Fabrication, see principle 02 Proof Loop).

Combined with a minimal `init.sh` (canonical "is the project healthy?" check) and the existing `PROBLEMS.md` (incident log), these three artifacts form the standard harness for long-run projects.

---

## The Three-Artifact Harness

| Artifact | Answers | When updated |
|---|---|---|
| `PROBLEMS.md` | What is **broken** right now? Recovery procedures? | When an incident happens or is resolved |
| `feature_list.json` | What **features** exist? Which is active? What's done? | When status of a feature changes |
| `init.sh` | Is the project **healthy** right now? (binary check) | When dependencies, tooling, or test commands change |

These are independent. A feature can be `blocked` because of a `PROBLEMS.md` entry. `init.sh` failing is its own kind of red — fix it before adding scope.

This sits **alongside** existing per-project conventions, not in place of them:

- **AGENTS.md or project guidance / AGENTS.md** — how to work here (rules and routing)
- **`.hermes-compatible project artefacts/handoffs/`** — tactical "what to do next" between sessions
- **`.hermes-compatible project artefacts/chronicles/`** — strategic "how we got here" across months

Features and incidents and health checks were the missing layer.

---

## feature_list.json — Schema

```json
{
  "features": [
    {
      "id": "feat-001",
      "name": "User authentication",
      "description": "Email + password login with JWT session tokens",
      "dependencies": [],
      "status": "done",
      "evidence": "L1: tsc clean (commit a3f2c1); L2: pytest 12/12 passed; L3: manual login flow verified in staging"
    }
  ]
}
```

### Four states

- `not-started` — defined, not yet picked up
- `in-progress` — active work right now (WIP=1: at most **one** feature in this state)
- `blocked` — cannot proceed, blocker named in `evidence`
- `done` — all three validation layers passed with durable artifacts in `evidence`

### Transition rules

```
not-started  →  in-progress     # if all dependencies are 'done' AND no other in-progress
in-progress  →  done            # only when evidence has L1+L2+L3 artifacts
in-progress  →  blocked         # name the blocker in evidence
blocked      →  in-progress     # after unblock (and WIP=1 still holds)
done         →  anything else   # FORBIDDEN. Regression → new feat-NNN
```

The `done → ?` prohibition is important. If a previously-done feature regresses, **do not** flip it back to `in-progress`. Create a new feature `feat-NNN` named "fix regression in feat-MMM". This preserves the audit trail and forces explicit acknowledgment that something broke after being verified.

---

## WIP=1 Invariant

At most one feature in `in-progress` at any time, across the entire `feature_list.json`. This is enforced by convention; a session-finish routine concept can verify it (see "Mechanical enforcement" below).

### Why WIP=1

The natural tendency under context pressure is to start a second feature when the first hits friction. "I'll just begin on B while A's tests run." Two days later both are half-done, neither is verified, and the agent (or human) cannot tell which assumptions belong to which feature. WIP=1 forces a clean answer: either finish the current feature, formally block it, or roll it back to `not-started`. No middle states.

### What to do when context demands switching

- Current feature is **technically blocked** (external dependency, decision needed from user): mark `blocked` with reason in `evidence`, then start a new feature.
- **Priorities changed** (user redirected): roll current back to `not-started` (or `blocked` if partial work matters), note the pivot in session handoff, start new feature.
- **Never** leave two in `in-progress` simultaneously.

This pairs with principle 02 (Proof Loop) — both forbid the agent from making fuzzy claims about completion. WIP=1 prevents the related anti-pattern of fuzzy claims about *what is being worked on*.

---

## Evidence Field — What Belongs There

When transitioning to `done`, `evidence` must reference durable artifacts at three layers:

| Layer | Proves | Examples |
|---|---|---|
| **L1 — Static** | Syntax valid, types check, lint clean | `tsc --noEmit` output, `ruff check` output, commit hash where lint became clean |
| **L2 — Runtime** | Tests pass, app starts, critical paths work | Test runner output file, log capture, ./init.sh exit 0 |
| **L3 — System** | End-to-end behavior, integration verified | Screenshot, curl response log, video, user flow capture |

Example acceptable evidence:

```
L1: tsc clean (commit a3f2c1) + ruff check passed
L2: pytest tests/test_auth.py 12/12 passed (.agent/evidence/test-output-2026-05-10.txt)
L3: manual login + reset flow in staging (.agent/evidence/auth-flow.png)
```

Not acceptable as evidence:

- "Works for me" / "Tested manually, looks good"
- "I ran the tests" without a file path
- Reference to a chat or session — those disappear, artifacts persist

The three-layer requirement is the same gate as principle 02's Proof Loop. The difference: Proof Loop is per-task; feature evidence accumulates across the project lifetime, surviving every context reset and session change.

---

## init.sh — The Health Check

A single executable script in the project root with one job: exit 0 if the project is healthy enough to work on, exit non-zero otherwise.

```bash
#!/bin/bash
set -e

# 1. Dependencies
npm install

# 2. L1 — Static checks
npm run check  # tsc --noEmit

# 3. L2 — Tests
npm test

# 4. Build (if applicable)
npm run build

echo "=== Initialization Complete ==="
```

### Constraints

- **Idempotent** — running twice in a row must not break anything
- **Non-interactive** — no prompts; if credentials are needed, they come from env vars
- **Fast** — target <3 minutes from fresh clone to green. If your setup is slower, split into `init.sh` (essentials) and `init-full.sh` (everything).
- **Free** — no paid API calls. The script should be runnable in CI on every PR.
- **Local** — no deploys. `init.sh` proves the code works on this machine; deploy is separate.

### What this replaces

Before `init.sh` convention: every new session spends 10-15 minutes piecing together commands from README + handoff + chronicle. With `init.sh`: 3 minutes from `git clone` to working state. The Learn Harness Engineering course measures this as a 5x speedup, consistent with our experience.

### Bootstrap rule

If `init.sh` fails on a fresh checkout, **fix the baseline first**. Do not add new features on top of a broken baseline. The first task in any session should be "is `./init.sh` green?" — if not, the only acceptable next task is making it green.

---

## When to Apply

**Good fit** for `feature_list.json` + `init.sh`:

- Projects with >5 distinct features
- Projects spanning >5 sessions of work
- Multi-developer or multi-agent collaboration
- Anything you'd describe as "long-running" or "ongoing"

**Skip** for:

- Short-term projects (1-2 sessions total)
- Projects with <5 features
- Pure research / exploration where scope is intentionally fluid
- Utility scripts and one-offs

For skipped projects, free-form notes in handoffs are fine. The overhead of maintaining `feature_list.json` is only worth it when there are enough features and sessions for the structure to pay back.

---

## Mechanical Enforcement (Optional)

A session-finish routine concept can verify the invariants automatically:

```python
# scripts/stop-feature-list-check.py (pseudocode)
def check_feature_list(repo_root):
    fl_path = repo_root / "feature_list.json"
    if not fl_path.exists():
        return  # project doesn't use this convention
    data = json.loads(fl_path.read_text())
    in_progress = [f for f in data["features"] if f["status"] == "in-progress"]
    if len(in_progress) > 1:
        raise BlockedSession(f"WIP=1 violated: {len(in_progress)} features in progress")
    # If this session edited the file to set status=done, evidence must be populated
    if session_set_done() and not session_done_features_have_evidence():
        raise BlockedSession("done without evidence")
```

This is a defence-in-depth layer. The primary enforcement is culture: the agent reads `feature_list.json` at session start, picks up the in-progress feature, and updates it correctly. The hook catches drift.

---

## Bootstrapping an Existing Project

For projects that already have handoffs and a chronicle but no `feature_list.json`:

1. Read the last 5-10 handoff files plus the project chronicle
2. Extract completed work → list of features → mark all `status: "done"` with evidence pointing to commit hashes
3. Identify the **single** currently-active thread → one feature `in-progress`
4. Identify planned work → features `not-started` with declared dependencies
5. Identify blocked work → features `blocked` with reason in evidence
6. Commit both `feature_list.json` and `init.sh` in one changeset: `harness: bootstrap feature_list + init.sh`

This takes 30-60 minutes for a typical 3-month-old project. The payoff is that every subsequent session starts from a clean machine-readable state instead of reading paragraph-form handoffs.

---

## Anti-Patterns

- **50+ entries** in feature_list.json — this is a backlog, not a working list. Move non-active items to `BACKLOG.md`.
- **`init.sh` that downloads multi-GB models or trains** — exceeds 3-minute target. Split: `init.sh` for quick health, `setup.sh` for one-time heavy lifting.
- **`done` with vague evidence** — "tests pass" is not evidence. The file path of the test output is.
- **Two in-progress** to avoid blocking — name the actual blocker, set `blocked` honestly.
- **Editing `feature_list.json` to silently roll back `done` → `in-progress`** — this hides regressions. Create a new fix feature instead.

---

## Relationship to Other Principles

- **02 Proof Loop** — Anti-Fabrication and evidence requirements apply to every feature transition. Evidence field references the same kind of durable artifacts.
- **04 Deterministic Orchestration** — `feature_list.json` is the state file the relay pattern reads. WIP=1 is a deterministic constraint a hook can verify mechanically.
- **07 Codified Context** — `feature_list.json` is the canonical structured handoff between sessions; it survives compaction.
- **16 Project Chronicles** — chronicles capture **why** decisions were made. feature_list captures **what** is currently done. Both are needed for long-run projects.

---

## Source

Templates and conceptual framework adapted from [walkinglabs/learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering), MIT-licensed, specifically:

- Lectures 06, 07, 08, 09 in the course documentation
- `skills/harness-creator/templates/feature-list.json` (schema)
- `skills/harness-creator/templates/feature-list.schema.json` (JSON schema)
- `skills/harness-creator/templates/init.sh` (bootstrap script)

Our adaptation:

- Added explicit 3-layer evidence requirement (L1/L2/L3) — integrated with our existing Proof Loop principle (02)
- Added WIP=1 invariant as a hard rule with `blocked` escape valve
- Added relationship to existing PROBLEMS.md / handoffs / chronicles layers (not in the original course)
- Drop-in templates available in `templates/long-run-project/`
