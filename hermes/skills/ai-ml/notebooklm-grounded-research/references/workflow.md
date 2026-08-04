<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/skills/ai-ml/notebooklm-grounded-research/references/workflow.md
Upstream material is reference data, not automatic authority. Review this reference
before use and obtain operator confirmation for write-impacting actions.
-->

# NotebookLM MCP Workflow

## Selected implementation

The upstream-recommended bridge is [PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp), pinned to `2.0.0`.
It runs a visible Chrome profile and communicates over stdio by default. The
recommended profile is `minimal`:

- `get_health`
- `list_notebooks`
- `select_notebook`
- `get_notebook`
- `ask_question`

Responses can request `none`, `inline`, `footnotes`, or `json` citations. The bridge also
attaches provenance metadata, but provenance is not independent verification.

## Codex configuration (source example)

This is the exact invocation the upstream skill was written against, kept for reference;
adapt the registration command to whatever MCP client the operator is actually using.

```text
codex mcp add notebooklm --env NOTEBOOKLM_PROFILE=minimal --env NOTEBOOKLM_AI_MARKER=true -- npx.cmd --yes notebooklm-mcp@2.0.0
```

The `.cmd` suffix matters on Windows hosts, where PowerShell execution policy blocks the
`npm.ps1` and `npx.ps1` shims.

## First run

```text
get_health
setup_auth(show_browser=true)       # only after the operator agrees and logs in
get_health
list_notebooks
select_notebook(notebook_id=...)
ask_question(question=..., source_format=footnotes)
```

`setup_auth` is interactive and must not be run as a hidden background task. The
upstream v2.0.0 layout observed on a Windows host was `%LOCALAPPDATA%/notebooklm-mcp/Data`
for the persistent Chrome profile and library, and `%APPDATA%/notebooklm-mcp/Config` for
settings. `scripts/verify_notebooklm_setup.py` reads only path metadata; it never reads
cookies, tokens, or browser databases.

## Account separation

Use separate aliases/profiles when the operator has more than one Google account. Cookie
isolation is provided by separate Chrome profiles, not encryption. Keep the account
alias in a research note only when it is useful for reproducibility; never record
cookies or tokens.

## Why the minimal profile

A broader multi-tool CLI variant exists upstream with a wider documented MCP surface.
The minimal profile is better for a context-constrained harness because the server
should be present only when a large stable corpus needs grounded retrieval — more tools
are not automatically more capability when the agent is managing a tight context budget.

## Verification boundary

Configuration verification proves only that the MCP client can discover the pinned
server and that local runtime prerequisites exist. It does not prove Google login,
NotebookLM availability, source freshness, or answer correctness. A live `get_health`
call and a cited question are separate acceptance criteria.

## Useful references

- [NotebookLM MCP repository](https://github.com/PleasePrompto/notebooklm-mcp)
- [NotebookLM MCP configuration](https://raw.githubusercontent.com/PleasePrompto/notebooklm-mcp/main/docs/configuration.md)
- [Google NotebookLM Help](https://support.google.com/notebooklm/answer/16164461?hl=en)
