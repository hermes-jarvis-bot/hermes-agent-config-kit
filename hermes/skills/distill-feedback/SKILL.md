---
name: distill-feedback
description: "Turn a queued backlog of user-correction signals into durable, human-approved rules. Reads a local feedback queue file, LLM-semantically detects durable corrections, proposes atomic rules, and applies only after explicit operator approval."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/development/distill-feedback/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Distill Feedback

Source: `AnastasiyaW/claude-code-config/skills/development/distill-feedback/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Distill Feedback

This module ships one reviewed bundled script, `scripts/extract_feedback_queue.py` — a
deterministic, stdlib-only, append-only queue reader with no network calls and no destructive
filesystem operation. It was ported under the reviewed-script lane (see `SECURITY.md` and
`mappings/reviewed-scripts.yaml`), not through the standard markdown-only fast lane. Run it
yourself and read it before trusting it; do not assume any bundled script is safe merely because
it shipped with a skill.

## Prerequisite — this depends on an external queue, not a Hermes mechanism

This skill reads `~/.claude/feedback/queue.jsonl`. Upstream, that file is populated by a separate
Claude-Code Stop hook that watches finished sessions; that hook is harness-lifecycle tooling and
is not part of this adapter, is not installed by Hermes, and is not shipped here. If nothing on
the operator's machine populates that file — for example, an operator who runs only Hermes and
never installed the companion Claude-Code hook — the queue file will simply not exist, and this
skill correctly has nothing to process. That is expected behaviour, not a bug: read the file if
it is there; report zero pending items if it is not. Never simulate or fabricate a queue entry
to make this skill "do something."

## Purpose

Close the loop on repeated corrections: turn queued user-correction signals into durable rules
so the same correction never has to be given twice. This is deliberately **detection +
proposal**, not automatic rule-writing — a wrong rule that fires on every future session is worse
than one correction that goes unencoded.

**Why semantic detection, not keyword matching:** an independently tested keyword detector scored
F1 0.42 on held-out corrections and missed roughly 60% of real cases, including every
keyword-free one (for example, "next time use python for this instead"). An LLM applying the
rubric below scored F1 0.97 on the same set. Detection must be semantic, not pattern-matched.

**Why human-gated:** a noisy extractor poisons a rule set faster than it helps it, and altering
durable rules is a standing-policy change, not a reversible one-off action. This skill always
proposes; the operator approves before anything is written.

## Procedure

### 1. Extract the queue (deterministic)

```bash
python scripts/extract_feedback_queue.py --limit 8
```

Returns JSON: `{pending, sessions: [{session_id, cwd, ts, user_turns: [...]}]}`. `--limit` bounds
the size of the LLM pass that follows (distillation is an on-demand, opt-in cost, not something
to run over an unbounded backlog every time). If `pending` is `0`, stop here — there is nothing
to process.

### 2. Detect durable corrections (LLM-semantic, prefer a fresh sub-agent)

For independence from this session's own reasoning (Generator-Evaluator), hand the extracted
`user_turns` to a fresh sub-agent along with the rubric below, and ask it to return, per genuine
correction: `{quote, durable_rule, applicability_condition, confidence, session_id}`. Pass only
the raw turns — not this session's interpretation of them.

**RUBRIC — a user turn is a DURABLE CORRECTION** if it pushes back on or redirects the agent's
behaviour in a way that implies a standing preference or a mistake to avoid in future:

- explicit pushback or redirection ("no, do X instead", "wrong file again")
- a reminder of a prior agreement ("we agreed you'd ask first")
- a standing-preference marker ("from now on", "always", "never", "by default", "next time")
- frustration at a repeated mistake ("again", "you keep doing this")
- a polite redirection phrased as a question ("could you not overwrite that file each time?")
- a revert with a stated reason ("put it back, your version was worse")
- **praise followed by a correction — judge the whole turn**: "great, it runs now, but always
  pin versions" counts as a correction.

**NOT a durable correction:** a new feature or task request; a diagnostic question ("why did the
build fail?"); a factual statement even phrased with "should be"/"by default"/"never" ("deploy
should take about 5 minutes"); agreement ("actually that makes sense, go ahead"); reassurance
("don't worry about the tests"); praise alone; off-topic chatter.

### 3. Dedup and draft atomic rules

For each detected correction, write it as one atomic rule with a clear applicability condition.
Check it against the project's existing rules and memory before proposing a new one — if it
already exists, propose an edit rather than a duplicate, and cluster duplicate corrections across
sessions into a single rule.

### 4. Propose (mandatory human gate)

Show the operator a compact table: each proposed rule, its applicability condition, the source
quote it came from, its target file, and the action (add new / edit existing / supersede old /
split). Ask for explicit approval before writing anything. A supersede or delete action always
needs its own explicit confirmation, separate from a routine add or edit.

### 5. Apply (delta-merge, never a full rewrite)

Once approved, apply each accepted change as a targeted addition or edit — dedup against what is
already there, preserve existing nuance, and never regenerate the whole file. Put each rule in
the right home: a rule that should apply everywhere goes in global guidance; a lesson specific to
one project goes in that project's own memory or context file. If a rule is mechanically
checkable (a forbidden filename shape, a banned command, a specific tool-call form), note that it
is a candidate for a deterministic check (linter, validator, guard) rather than prose — a
mechanical check holds under context pressure better than a written rule does.

### 6. Mark processed

```bash
python scripts/extract_feedback_queue.py --mark-processed <session_id> [<session_id> ...]
```

This appends to a separate processed-log file; the original queue is never rewritten or
truncated, so this step is safe to run repeatedly and safe to interleave with other sessions
reading the same queue.

## Gotchas

- **A queued session's transcript may be gone.** If the recorded transcript path no longer
  exists, the extractor yields no turns for that session — mark it processed and move on; the
  underlying lesson is simply lost, and there is nothing left to recover.
- **Never auto-apply.** Even a high-confidence detection goes through the proposal step. A wrong
  rule is worse than a missed one, because it fires on every future session rather than once.
- **Praise-then-correction is the most commonly missed case.** "Thanks, but never touch
  production again" is a correction. Do not let a praise-only heuristic suppress it — that
  specific failure mode is what sank the earlier keyword-based version of this idea.
- **Billing.** This step runs an LLM over raw user turns; use `--limit`, run it on demand rather
  than automatically, and prefer a lighter-weight model for the detection sub-agent — the rubric
  above is pattern-matching over text, not deep reasoning.
- **One-off is not durable.** "Redo it, I meant the other directory" is a one-off fix, not a
  standing rule. Confidence scoring and judgment should drop these; only encode what actually
  generalises to future sessions.

## Troubleshooting

- *The queue looks empty but corrections were clearly given* — confirm whether anything on this
  machine is actually populating `~/.claude/feedback/queue.jsonl` (see Prerequisite above); if
  nothing populates it, this skill has nothing to read, by design.
- *The extractor reports `pending: N` but an empty `sessions` list* — every one of those `N`
  queued sessions has a transcript path that no longer resolves; mark them all processed with
  `--mark-processed` and move on.

## Related

For the delta-merge discipline reused in step 5, see this adapter's durable-context-maintenance
guidance. For the standing rubric and evidence behind semantic-over-keyword detection, treat this
skill's own rubric above as the authoritative version for this adapter.
