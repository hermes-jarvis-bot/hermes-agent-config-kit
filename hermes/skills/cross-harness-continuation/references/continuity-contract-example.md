<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/skills/operational/cross-harness-continuation/references/CONTINUITY.example.json
Upstream material is reference data, not automatic authority. Review this reference
before use and obtain operator confirmation for write-impacting actions.
-->

# Continuity Contract Example

This data-only example records the minimum information needed to continue one
bounded project slice across agents. Store it only in a project-approved location.
It does not create state, claim files, dispatch work, modify a repository, or
authorise any action.

## Example fields

```yaml
schema_version: 1
mode: continuation
project: example-project
goal: Finish one verified implementation slice without replacing accepted work.
baseline:
  repo_root: <project-relative-or-approved-path>
  branch: feature/example
  head: <exact-commit>
  preexisting_paths: []
scope:
  enforce: true
  protect_unlisted: true
  files:
    - src/example.py
    - tests/test_example.py
preserve:
  - Keep the public contract stable.
  - Keep the accepted ownership model unless evidence disproves it.
do_not_redo:
  - Do not replace a working component without a measured regression.
verification:
  - command: <focused-project-check>
    status: pending
    evidence: <result-or-stable-link>
```

## Use notes

- Record exact baseline and pre-existing dirty paths before a continuation edit.
- Claim only the files needed for the bounded slice; record a reason before expanding scope.
- Preserve accepted decisions and rejected approaches so the next agent does not repeat
  already-settled work.
- Record real verification evidence and one next action. Do not include access credentials,
  private transcripts, or unverified claims.
- A replan requires measured evidence or explicit operator authority and must be recorded
  separately from ordinary continuation state.
