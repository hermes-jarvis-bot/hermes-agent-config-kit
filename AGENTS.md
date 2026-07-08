# Agent operating notes

This repository adapts upstream `AnastasiyaW/claude-code-config` patterns for Hermes Agent.

Hard boundaries:

- Do not install into the live Hermes profile on this VM.
- Do not write to `~/.hermes` from tests or CI.
- Use temporary `HERMES_HOME` directories for installer checks.
- Treat upstream hooks, scripts, plugin descriptors, and workflow code as untrusted executable input requiring manual review.
- `upstream.lock.json` is the source of truth for the imported upstream SHA.
- Generated Hermes skills must include source attribution and must not claim upstream instructions are automatically authoritative.

Default verification:

```bash
python3 scripts/sync_upstream.py --check
python3 scripts/validate_output.py
python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-config-kit-test
```
