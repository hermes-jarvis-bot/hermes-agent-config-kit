---
name: plan-swarm-review
description: "Iteratively harden a plan or a code module through escalating rounds of independent, differently-angled review (broad, then diverse-perspective multisample, then focused, then focused+multisample)."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/architecture/plan-swarm-review/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Plan Swarm Review

Source: `AnastasiyaW/claude-code-config/skills/architecture/plan-swarm-review/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Plan Swarm Review

# Plan Swarm Review

Iterative plan or module hardening through independent multi-perspective review and focused
decomposition. This module is guidance only: it does not dispatch reviewers, alter a repository,
or approve a change on its own.

**Core insight:** a single reviewer misses issues because of attention-budget limits. Independent
reviewers reading the same document tend to find different problems (stochastic diversity), and
narrowing each reviewer's focus to one aspect improves depth on that aspect. Re-reviewing after a
fix round can surface issues that were previously masked by other problems.

**Evidence this rests on:** diverse prompts over identical ones measurably improve reasoning and
code-review recall in controlled studies; reasoning-tree/consensus audits recover a majority of
minority-correct findings that plain majority voting would discard; multi-perspective review has
been shown to substantially outperform a single pass on both general reasoning and targeted
vulnerability detection. Treat these as directional evidence for the pattern, not a guarantee for
any specific run.

## Modes

**Plan mode** (default): review a design document, ADR, RFC, or spec before implementation.

**Code mode**: review source files for bugs and vulnerabilities. Use when the target is code
rather than a plan, or the request is explicitly a security audit or vulnerability hunt. In code
mode the review aspects shift from plan-oriented (contracts, completeness) to code-oriented
(injection, auth bypass, race conditions, memory safety).

## Step 0: identify the target and scale the effort

Read the target document or code fully first. Note its size, the components or modules it
describes, the interfaces between them, data flows and mutations, and external dependencies and
trust boundaries.

If the target is small (a rough guide: under 100 lines with one or two simple components), a
single-pass review is more proportionate — swarming several independent reviewers over a small,
simple target is not worth the added cost.

## Round 1 — broad review (one reviewer)

Purpose: catch the obvious issues before spending effort on multi-perspective review.

Read the entire target and check for:

1. **Contracts** — are interfaces between components fully specified (types, error codes,
   required vs. optional fields, versioning)?
2. **Data flow** — is data transformation described end to end? What happens at each boundary?
   Is backward compatibility addressed?
3. **Negative scenarios** — what happens on timeout, partial failure, invalid input, or a race?
4. **Consistency** — do different sections contradict each other, or describe the same entity
   differently in two places?
5. **Completeness** — are there gaps, "TBD"/"later" placeholders, or scenarios mentioned but not
   covered?
6. **Dependencies** — is implementation order clear? Are blocking or circular dependencies
   identified?
7. **Ambiguity** — could two people reasonably implement a section differently? Watch for vague
   terms like "handle appropriately."

For each finding, record: a one-line description, the section it applies to, a severity (high /
medium / low), the evidence (a short quote), and a concrete proposed fix. If nothing is found,
say so plainly rather than padding the report with praise.

**After round 1**: if there are zero findings, the plan is clean — report that and stop. If there
are findings, present them grouped by severity and ask whether to apply the fixes and continue to
round 2. Only proceed to round 2 with explicit go-ahead, since it costs meaningfully more.

## Round 2 — diverse multi-perspective review (independent reviewers, varied angles)

Purpose: stochastic diversity catches what a single pass missed.

**Do not give every reviewer an identical prompt.** Identical prompts tend to produce correlated
errors — reviewers cluster on the same issues and share the same blind spots. Give each reviewer
a genuinely different perspective on the same target.

When the harness supports launching several independent review sessions in parallel, and the
operator has approved the added cost, run three (or five, for a higher-stakes target) reviewers
at once, each with a distinct persona below, each reading the full target with no visibility into
the others' findings.

### Plan-mode perspectives

| Reviewer | Persona | Focus |
|---|---|---|
| 1 | Skeptical implementer | "I have to build this next — what's unclear, contradictory, or impossible?" |
| 2 | Security auditor | "Where are the trust boundaries? What happens with malicious input?" |
| 3 | QA engineer | "How would I test this? What edge cases aren't covered? What breaks at scale?" |
| 4 | New team member | "What terms are undefined? What implicit knowledge does this assume?" |
| 5 | Operator/on-call | "What fails at 3am? What's the rollback plan? What's unmonitored?" |

### Code-mode perspectives

| Reviewer | Persona | Focus |
|---|---|---|
| 1 | Attacker | "How do I exploit this? Injection, auth bypass, privilege escalation?" |
| 2 | Concurrency specialist | "What races, deadlocks, or ordering issues exist?" |
| 3 | Performance engineer | "What's quadratic or worse? What allocates unbounded memory? What blocks the event loop?" |
| 4 | Error-recovery auditor | "What happens when X fails? Is cleanup correct? Are resources leaked?" |
| 5 | Integration tester | "Do contracts match? Are types compatible? What breaks at a boundary?" |

Each reviewer reads the entire target but analyzes it only through their assigned lens, using the
same finding format as round 1.

**After round 2**:

1. **Deduplicate** by section and issue type. A finding raised independently by multiple
   reviewers is high-confidence (consensus).
2. **Preserve minority findings.** A finding raised by only one reviewer is not automatically
   low-value — the evidence behind this pattern shows minority-only findings are often the ones a
   single perspective would have missed entirely. Flag these as a unique catch; do not discard
   them.
3. Synthesize a merged report separating consensus findings from unique catches, present it, and
   ask whether to continue to round 3.

**Stop criterion**: if round 2 found zero high-severity and at most two medium-severity findings,
the target is likely solid — stop here rather than continuing.

## Round 3 — focused review (decompose into aspects)

Purpose: narrowing scope deepens the analysis per aspect.

Select three to seven focus aspects based on the target's content.

### Plan-mode aspects

| Aspect | Include when |
|---|---|
| Contracts & interfaces | More than two interacting components |
| Data flow & migrations | Data transformation, schema change, or state migration involved |
| Negative scenarios | User-facing feature or distributed system |
| Consistency | Long document or multiple authors |
| Completeness | External-system references or a phased rollout |
| Security & trust | Auth, user input, or external APIs involved |
| Dependencies & order | Many implementation steps or parallel workstreams |

### Code-mode aspects (bug and vulnerability hunting)

Before this round, read `references/vulnerability-kb.md` for condensed detection heuristics per
vulnerability class, and fold the relevant heuristics into each reviewer's focus.

| Aspect | What to trace |
|---|---|
| Injection & input validation | SQL/NoSQL/command/LDAP injection, XSS, path traversal, template injection |
| Auth & access control | Auth bypass, privilege escalation, insecure direct object references, missing authorization checks |
| Concurrency & state | Race conditions, time-of-check/time-of-use, deadlocks, shared mutable state, atomicity violations |
| Memory & resources | Buffer overflows, use-after-free, resource leaks, unbounded allocation |
| Error handling & recovery | Swallowed errors, information leakage in errors, incomplete cleanup, missing rollback |
| Cryptography & secrets | Weak algorithms, hardcoded secrets, improper randomness, timing attacks |
| Business logic | State-machine violations, numeric overflow in monetary values, missing business-rule validation |

State the selected aspects to the operator before launching focused review. For each aspect, one
reviewer analyzes the whole target through that single lens only, using the same finding format
as before. When the harness supports it, run all aspect reviewers in parallel with no visibility
into each other's output.

**After round 3**: same dedup and synthesis as round 2. **Stop criterion**: zero high-severity and
at most two medium-severity findings.

## Round 4 — focused + multisample (optional, expensive)

Purpose: maximum depth, reserved for a high-stakes target where round 3 still found
high-severity issues.

Before running this round, state the cost explicitly to the operator (roughly aspect-count times
two-to-three reviewers) and get explicit confirmation — this round multiplies cost and should
never run silently. For each aspect from round 3 that had findings, run two or three reviewers
with the same focused prompt.

**After round 4**: final synthesis. If high-severity issues persist at this depth, the target
likely needs structural rework rather than further polish — say so plainly.

## Reporting

After each round, report: the round type, how many reviewers ran, how many new findings and how
many duplicates were removed, then findings grouped by severity (each with its section, evidence,
proposed fix, and confidence — high if multiple reviewers agreed, medium otherwise), followed by
a cumulative total and a recommendation to continue or stop.

After the last round, report a final summary: rounds executed, reviewers used in total, findings
by severity and how many were fixed versus deferred, and one of three verdicts:

- **Hardened** — all high-severity findings fixed, at most a few medium ones remain: safe to
  proceed.
- **Improved** — significant issues found and fixed, some medium-severity ones deliberately
  deferred.
- **Needs rework** — structural issues remain; the target needs a real revision, not polish.

## Gotchas

- **Cost.** A round-4 pass over seven aspects at three samples each is roughly twenty reviewer
  launches. Always confirm cost with the operator before an expensive round, and prefer the
  cheapest round that would settle the question.
- **The target changes between rounds.** After applying fixes, re-read the current version in the
  next round, not the original — reference the file, not pasted text, so every round reads what
  is actually there now.
- **Review depth per reviewer is bounded.** A reviewer spawned for this protocol should stay
  shallow in its own tool use (read/search the target, do not recursively spawn further
  reviewers) — this is fine for a plan or module review, which is typically a handful of files.
- **Diminishing returns.** A round-4 pass typically turns up only one to three medium findings; if
  round 3 found zero high-severity issues, skip round 4 rather than running it anyway.
- **Deduplication matters.** Multi-perspective review produces overlapping findings by design; the
  dedup step after each round is what keeps the same issue from three reviewers being counted as
  three separate issues.
- **This reviews plans and modules, not incremental diffs.** For routine pull-request review of a
  small, already-scoped change, use this adapter's `deep-review` guidance instead.

## Related

Use this adapter's `deep-review` guidance for routine or diff-scoped code review, its
`vulnerability-detection-pipeline` guidance for a staged security investigation, its
`proof-verify` guidance for frozen acceptance-criteria verification, and its
`multi-agent-task-decomposition` guidance when genuinely coordinated parallel roles are called
for beyond review. This module supplies the escalating, multi-perspective review protocol; match
review depth to the actual stakes and size of the target rather than defaulting to the deepest
round available.
