---
name: api-utf8-posting
description: "Prepare non-ASCII API payloads deliberately and verify stored receiver-side text after an authorised external write."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: rules/api-utf8-posting.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Api Utf8 Posting

Source: `AnastasiyaW/claude-code-config/rules/api-utf8-posting.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

## Unicode payload integrity

This module provides data-integrity guidance for authorised API writes that contain non-ASCII text, including Cyrillic, CJK, Arabic, accented text, and emoji. It is guidance only: it does not send requests, configure a communications channel, activate a hook, access credentials, or retry an external action.

## When to use

Use this module when an API request will create or update text outside the local workspace and the body contains characters beyond ASCII. Typical boundaries include issue trackers, messaging gateways, webhooks, and service APIs.

Use `verify-at-consumer` for the wider receiving-side contract. Use this module for the narrower question: did the stored text retain its intended Unicode characters and UTF-8 encoding?

## Read-only preflight

Before an external write:

1. Confirm the target endpoint, resource identifier, expected response field, and the operator authorisation for the write.
2. Keep the intended text in a UTF-8 source file or a runtime value whose encoding is explicit; avoid passing non-ASCII payload text through ambiguous shell or console boundaries.
3. Ensure the request representation declares JSON UTF-8 where the interface supports a content type.
4. Keep access credentials out of payload files, command history, telemetry, generated artefacts, and reports.
5. Define the receiver-side read-back query and the exact text or character class that must survive storage.

If the endpoint, encoding contract, or read-back route is unknown, stop and retrieve it before sending. A successful transport response is not proof that stored text is intact.

## Authorised write and verification protocol

After operator confirmation for the external write:

1. Use the approved interface with an explicit UTF-8 payload boundary.
2. Record only redacted sender evidence, such as a resource identifier or delivery status.
3. Read the stored field back through the receiving API or consumer interface.
4. Compare the returned text with the intended text, or check the expected non-ASCII character ranges when a full equality check is impractical.
5. Treat replacement characters, unexpected question-mark runs, missing expected characters, or decode failures as a data-integrity fault.
6. Do not repeat the same ambiguous delivery path. Preserve the original identifier for audit, diagnose the boundary, and propose a corrected repost only with the required operator authorisation.

## Platform-neutral boundary rules

- Explicitly encode JSON bytes as UTF-8 in application code.
- Explicitly decode API response bytes as UTF-8 when the response contract requires it.
- Open payload and result files with a declared UTF-8 encoding.
- Prefer a reviewed file or application request path over embedding non-ASCII data in an ad-hoc shell command when console encoding is uncertain.
- Keep verification independent of display fonts or terminal rendering; inspect returned data from the receiving interface.

## Avoid

- Assuming an HTTP success response proves stored text is readable.
- Retrying an unchanged path after it has corrupted text.
- Replacing or deleting an affected external record without an audit-aware recovery decision.
- Logging access credentials, raw authorization headers, or sensitive external payloads to prove encoding.
- Adding an active shell hook, automatic repost routine, or communications-channel integration from this guidance.

## Reporting

Report the target class, whether the action was read-only or externally write-impacting, the payload encoding boundary, redacted sender evidence, receiver-side read-back result, and any remaining recovery or operator-confirmation point.
