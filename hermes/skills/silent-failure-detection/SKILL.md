---
name: silent-failure-detection
description: "Detect when configured protections, jobs, hooks, services, or integrations silently fail despite appearing enabled."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/silent-failure-detection.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Silent Failure Detection

Source: `AnastasiyaW/claude-code-config/rules/silent-failure-detection.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Silent Failure Detection

Upstream source policy was written for plugin prerequisite checks in a different harness. Hermes adaptation generalises the rule: configured does not mean working, and silence is not proof of protection.

## Principle

A protection, integration, scheduled protocol, background process, CI workflow, plugin, MCP server, or gateway can appear enabled while its required binary, credential, network path, permission, working directory, or delivery route is missing. Treat that state as unverified until behaviour is observed.

Examples:

- a background process was started without `notify_on_complete` and nobody polls it;
- a scheduled protocol runs locally in CLI mode and cannot deliver to the terminal;
- a GitHub workflow is queued or skipped while the push succeeded;
- an SSH command exits `0` but the expected marker or artefact is absent;
- an installer prints planned actions but dry-run unexpectedly creates files;
- a remover reports success but target artefacts still exist;
- a gateway/webhook is configured but no event reaches the consumer.

## Required evidence

Before claiming a protection or automation works, verify at least one behavioural signal:

1. The required command, credential, endpoint, or service exists.
2. The operation was triggered under realistic conditions.
3. The expected output, event, artefact, check-run, log marker, or delivery was observed.
4. The negative case is understood when silence is possible.

Configuration state such as `enabled: true`, an installed package, a running process, or a green setup command is useful context, not sufficient proof.

## Hermes-specific checks

- For background terminal processes, prefer `notify_on_complete=True` for bounded work or explicitly poll with `process`.
- For scheduled protocols created from CLI sessions, remember that default delivery is local-only and not a live terminal notification.
- For GitHub work, read back check-runs or workflow runs after push.
- For installers and removers, inspect the exact filesystem targets after dry-run/apply/remove.
- For SSH and remote commands, check exit code, stderr/stdout, and an explicit success marker or artefact.
- For gateways, verify both configuration and event delivery at the consumer side.

## Reporting

If telemetry is incomplete, say so. Use wording like:

- `configured but not behaviour-verified`;
- `started, completion not yet observed`;
- `CI queued, conclusion pending`;
- `delivery path unverified`;
- `no evidence of failure, but no success marker either`.

Do not convert missing telemetry into success. A quiet interface may be healthy; it may also be dead with excellent manners.

## Known gaps

Document what the check does not cover. If a verifier only checks missing binaries, say that it does not prove credentials, permissions, environment variables, network reachability, or runtime behaviour. This prevents a safety check from becoming a more sophisticated illusion of safety.
