#!/usr/bin/env python3
"""pre_tool_call: require a closure audit before writing handoff files.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/handoff-closure-audit-guard.py, reimplemented for Hermes
Agent's shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the
upstream Claude-Code version this was read from).

Handoffs are the legitimate exception to "finish the task now". That exception is easy to
abuse: an agent can write a handoff while silently leaving related work half-open. This hook
blocks handoff writes unless the handoff contains an explicit Closure Audit section with the
required fields, and cross-checks against PROBLEMS.md tickets opened THIS project, TODAY, that
are still open and unmentioned in the handoff.

Watched paths (multi-harness, matching transfer-contract-guard.py's recognition pattern -- a
handoff written under any of these conventions is still validated):
- .hermes/handoffs/<project-slug>/*.md and .hermes/HANDOFF.md (Hermes-native default)
- .claude/handoffs/<project-slug>/*.md and .claude/HANDOFF.md
- .agent/handoffs/<project-slug>/*.md and .codex/handoffs/<project-slug>/*.md

INDEX.md and archive folders are ignored.

Ported unchanged: the Closure Audit required-fields validation, the today's-open-PROBLEMS.md-
tickets cross-check (both pure text/regex logic, harness-agnostic). Adapted: `Write`/`Edit`/
`MultiEdit` -> Hermes's `write_file`/`patch` (`mode="replace"` reconstructs the same way as
upstream's Edit; `mode="patch"` V4A multi-file bodies are NOT reconstructed -- a handoff write is
realistically always single-file, so this falls through to the same "cannot reconstruct, use a
full write_file instead" guidance upstream gives for any tool shape it can't handle either).

Bypass: HERMES_ALLOW_INCOMPLETE_HANDOFF=1 or a `<!-- hermes-bypass: incomplete-handoff -->`
marker in the handoff content.
"""
from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import allow, block, bypass, file_path, log, read_event  # noqa: E402

REQUIRED_LABELS = {
    "Primary request status": re.compile(r"^\s*[-*]?\s*\**Primary request status\**\s*:", re.I | re.M),
    "Acceptance/checklist verified": re.compile(r"^\s*[-*]?\s*\**Acceptance/checklist verified\**\s*:", re.I | re.M),
    "Related/scope-adjacent tasks checked": re.compile(r"^\s*[-*]?\s*\**Related/scope-adjacent tasks checked\**\s*:", re.I | re.M),
    "Unfinished related tasks": re.compile(r"^\s*[-*]?\s*\**Unfinished related tasks\**\s*:", re.I | re.M),
    "Why not continuing now": re.compile(r"^\s*[-*]?\s*\**Why not continuing now\**\s*:", re.I | re.M),
}

HEADING_RE = re.compile(r"^##\s+(Closure Audit|Аудит закрытия)\s*$", re.I | re.M)
NEXT_HEADING_RE = re.compile(r"^##\s+", re.M)
PRIMARY_STATUS_RE = re.compile(
    r"^\s*[-*]?\s*\**Primary request status\**\s*:\s*"
    r"(COMPLETE|BLOCKED-[A-Z0-9_-]+|HANDOFF-NEAR-CONTEXT-LIMIT|USER-REDIRECTED)\b",
    re.I | re.M,
)
UNFINISHED_RE = re.compile(
    r"^\s*[-*]?\s*\**Unfinished related tasks\**\s*:\s*(?P<value>.+)$",
    re.I | re.M,
)
TRACKER_RE = re.compile(
    r"\b(PROBLEMS\.md|feature_list\.json|issue\s*#?\d+|ticket\s*#?\d+|"
    r"backlog|task[-_ ]?inbox|DECISIONS\.md|BLOCKED-[A-Z0-9_-]+)\b",
    re.I,
)
BAD_EVASION_RE = re.compile(
    r"\b(todo later|later maybe|next session maybe|not checked|unknown|tbd|"
    r"unclear|probably done|seems done|should be fine)\b",
    re.I,
)

HANDOFF_DIR_PREFIXES = (".hermes/handoffs/", ".claude/handoffs/", ".agent/handoffs/", ".codex/handoffs/")
HANDOFF_SINGLE_FILES = (".hermes/handoff.md", ".claude/handoff.md", ".agent/handoff.md", ".codex/handoff.md")


def _norm(path: str) -> str:
    return path.replace("\\", "/")


def is_handoff_path(path: str) -> bool:
    p = _norm(path).lower()
    if not p.endswith(".md"):
        return False
    if p.endswith("/index.md") or "/archive/" in p or "/handoff-history/" in p:
        return False
    if any(p == f or p.endswith("/" + f) for f in HANDOFF_SINGLE_FILES):
        return True
    return any(prefix in p for prefix in HANDOFF_DIR_PREFIXES)


def apply_edit(original: str, tool_name: str, tool_input: dict) -> str | None:
    """Best-effort reconstruction of post-edit content for `patch` mode=replace."""
    if tool_name == "write_file":
        return str(tool_input.get("content", ""))

    if tool_name != "patch" or (tool_input.get("mode") or "replace") != "replace":
        return None  # V4A multi-file patch bodies are not reconstructed -- see docstring

    old = str(tool_input.get("old_string", ""))
    new = str(tool_input.get("new_string", ""))
    if old == "" or old not in original:
        return None
    return original.replace(old, new, 1)


def closure_section(content: str) -> str | None:
    match = HEADING_RE.search(content)
    if not match:
        return None
    start = match.start()
    next_match = NEXT_HEADING_RE.search(content, match.end())
    end = next_match.start() if next_match else len(content)
    return content[start:end]


def validate_closure_audit(content: str) -> list[str]:
    errors: list[str] = []
    section = closure_section(content)
    if section is None:
        return [
            "missing required `## Closure Audit` section",
            "add the mandatory fields from rules/session-handoff.md before writing the handoff",
        ]

    for label, pattern in REQUIRED_LABELS.items():
        if not pattern.search(section):
            errors.append(f"missing Closure Audit field: {label}:")

    if not PRIMARY_STATUS_RE.search(section):
        errors.append(
            "Primary request status must be COMPLETE, BLOCKED-<reason>, "
            "HANDOFF-NEAR-CONTEXT-LIMIT, or USER-REDIRECTED"
        )

    unfinished = UNFINISHED_RE.search(section)
    if unfinished:
        value = unfinished.group("value").strip()
        if not re.search(r"\b(NONE|нет|no unfinished|nothing open)\b", value, re.I):
            if not TRACKER_RE.search(value):
                errors.append(
                    "Unfinished related tasks is not NONE and does not cite a durable tracker "
                    "(PROBLEMS.md, feature_list.json, issue/ticket, backlog, task-inbox, or BLOCKED-*)"
                )

    bad = BAD_EVASION_RE.search(section)
    if bad:
        errors.append(f"Closure Audit contains evasive/uncertain wording: {bad.group(0)!r}")

    return errors


PROBLEM_HEADING_RE = re.compile(r"^##\s+(?P<date>\d{4}-\d{2}-\d{2})[^\n]*$", re.M)
TICKET_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]{2,}(?:-[A-Z0-9]+)+\b")
STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*(?P<value>.+)$", re.M)
CLOSED_WORDS = re.compile(r"\b(RESOLVED|CLOSED|FIXED|DONE|NOT[_ ]A[_ ]BUG|WONTFIX|ОТОЗВАНО)\b", re.I)


def find_problems_file(handoff_path: Path) -> Path | None:
    """The PROBLEMS.md that governs this handoff, walking up from the handoff."""
    for parent in list(handoff_path.parents)[:6]:
        candidate = parent / "PROBLEMS.md"
        if candidate.is_file():
            return candidate
    return None


def tickets_opened_today(problems_text: str, today: str) -> list[tuple[str, str, str]]:
    """(id, status, title) for entries opened today that are still open."""
    out: list[tuple[str, str, str]] = []
    heads = list(PROBLEM_HEADING_RE.finditer(problems_text))
    for i, match in enumerate(heads):
        if match.group("date") != today:
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(problems_text)
        body = problems_text[match.start():end]
        status_match = STATUS_RE.search(body)
        status = status_match.group("value").strip() if status_match else "NO STATUS"
        if CLOSED_WORDS.search(status):
            continue
        heading = match.group(0).lstrip("# ").strip()
        found = TICKET_ID_RE.search(heading)
        if not found:
            continue
        out.append((found.group(0), status.split()[0][:40], heading[:90]))
    return out


def project_tokens(handoff_path: Path) -> set[str]:
    return {word for word in re.split(r"[-_]", handoff_path.parent.name.lower())
            if len(word) > 3}


def validate_todays_open_tickets(content: str, handoff_path: Path) -> list[str]:
    problems = find_problems_file(handoff_path)
    if problems is None:
        return []
    try:
        text = problems.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    tokens = project_tokens(handoff_path)
    if not tokens:
        return []
    today = _dt.date.today().isoformat()
    mine = [t for t in tickets_opened_today(text, today)
            if any(word in t[0].lower() for word in tokens)]
    unmentioned = [t for t in mine if t[0] not in content]
    if not unmentioned:
        return []
    listing = "\n".join(f"    {ident}  [{status}]  {title}" for ident, status, title in unmentioned)
    return [
        "these were opened in PROBLEMS.md today and are still open, and this handoff "
        "does not mention them:\n" + listing + "\n"
        "    Finish them now -- a session's own findings are not a backlog. If one genuinely "
        "cannot be finished, name its id in the Closure Audit under Unfinished related tasks "
        "with the external blocker, not a label."
    ]


def main() -> None:
    event = read_event()
    tool_name = str(event.get("tool_name", ""))
    if tool_name not in {"write_file", "patch"}:
        allow()

    tool_input = event.get("tool_input", {}) or {}
    path = file_path(tool_input)
    if not path or not is_handoff_path(path):
        allow()

    target = Path(path)
    original = ""
    if tool_name == "patch":
        try:
            original = target.read_text(encoding="utf-8", errors="replace")
        except OSError:
            log("BLOCK", "handoff_closure_audit", "cannot_read", "handoff", path)
            block(
                f"Cannot validate handoff edit because the existing file is unreadable: {path}.\n"
                "Use write_file with the full handoff content, including `## Closure Audit`."
            )

    content = apply_edit(original, tool_name, tool_input)
    if content is None:
        log("BLOCK", "handoff_closure_audit", "cannot_reconstruct", "handoff", path)
        block(
            f"Cannot validate resulting handoff content for {tool_name} on {path}.\n"
            "Use one atomic write_file with the full handoff content, including `## Closure Audit`."
        )

    if bypass("incomplete-handoff", content):
        log("WARN", "handoff_closure_audit", "bypass", "handoff", path)
        allow()

    errors = validate_closure_audit(content)
    errors += validate_todays_open_tickets(content, target)
    if not errors:
        allow()

    log("BLOCK", "handoff_closure_audit", "missing_closure_audit", "handoff", path)
    reason = (
        f"Handoff write blocked for {path}.\n\n"
        "A handoff is allowed only after a closure audit proves the current task and "
        "scope-adjacent tasks were handled honestly.\n\n"
        "Problems:\n"
        + "\n".join(f"  - {err}" for err in errors)
        + "\n\nRequired section:\n"
        "## Closure Audit\n"
        "- Primary request status: COMPLETE | BLOCKED-<external-reason> | "
        "HANDOFF-NEAR-CONTEXT-LIMIT | USER-REDIRECTED\n"
        "- Acceptance/checklist verified: <tests/checks/evidence, or explicit blocker>\n"
        "- Related/scope-adjacent tasks checked: <what adjacent work was checked>\n"
        "- Unfinished related tasks: NONE | <durable tracker + reason>\n"
        "- Why not continuing now: NONE | <external blocker/context limit/user redirect>\n"
    )
    block(reason)


if __name__ == "__main__":
    main()
