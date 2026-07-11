---
name: repository-attribution-hygiene
description: "Keep repository and external-work metadata accurate, intentional, and free of automatic tool-attribution noise."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/no-claude-attribution.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Repository Attribution Hygiene

Source: `AnastasiyaW/claude-code-config/rules/no-claude-attribution.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Repository Attribution Hygiene

Use this module when preparing Git commits, pull requests, issues, release notes, or other shared project metadata. It keeps metadata accurate, intentional, and appropriate for the repository's documented authorship and disclosure policy. It is guidance only: it does not install commit hooks, rewrite history, alter Git configuration, remove existing trailers, or send messages to external services.

## Principle

Shared metadata should identify the accountable human or organisation and describe the work plainly. Do not add automatic tool-attribution trailers, badges, boilerplate, or vendor links merely because an interface offered them. Conversely, do not suppress attribution that a licence, contract, project policy, or operator explicitly requires.

This is a provenance and privacy review, not a claim that every use of an AI tool must be hidden. The repository policy and applicable obligations decide what disclosure is required.

## Read-only preflight

Before a shared metadata write:

1. Inspect repository contribution guidance, licence notices, pull-request templates, and any documented authorship or disclosure policy.
2. Identify the intended commit, PR, issue, release, or message and the party accountable for it.
3. Distinguish descriptive content (for example, a provider name required to describe an integration) from an automatic authorship claim or promotional footer.
4. Check whether the chosen interface will append a trailer, badge, hyperlink, co-author line, or generated-by wording.
5. If policy, contractual obligations, or the required disclosure wording are unclear, stop and obtain an operator decision before publishing.

## Metadata preparation protocol

1. Use a concise subject and body that state the actual change, scope, limitations, and verification evidence.
2. Include co-author, contributor, or tool-disclosure fields only when they are accurate and required by the applicable policy or operator instruction.
3. Remove optional interface-generated attribution that is neither required nor desired before the authorised write.
4. Preserve content-relevant references to providers, tools, repositories, APIs, or incidents; a factual technical reference is not an authorship claim.
5. Keep access credentials, internal prompts, private session content, and unsupported provenance claims out of public metadata.

## Existing history

Treat prior metadata as evidence, not a reason to rewrite shared history. Do not amend, filter, force-push, or bulk-edit existing commits solely for hygiene without explicit operator confirmation, impact review, a recovery plan, and coordination with affected collaborators.

For new work, apply the adopted policy prospectively. If historical content creates a concrete legal, privacy, security, or operational risk, report the exact references and propose a separately approved remediation protocol.

## Avoid

- Treating a blanket no-attribution convention as permission to evade required licence, contractual, regulatory, or operator disclosure.
- Adding active hooks, global Git settings, or automatic metadata rewriting from this guidance.
- Removing factual references to a technology when they are necessary to explain the change or reproduce a fault.
- Claiming a human author reviewed or performed work without evidence.
- Rewriting shared Git history as an incidental cleanup.

## Reporting

Report the metadata target, policy sources inspected, required versus optional attribution fields, content references deliberately retained, proposed wording, operator-confirmation point for the external write, and post-publication read-back. Accurate metadata is useful; decorative automation is not a substitute for it.
