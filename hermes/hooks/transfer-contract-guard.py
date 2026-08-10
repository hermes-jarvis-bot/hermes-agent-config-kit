#!/usr/bin/env python3
"""pre_tool_call + post_tool_call + pre_verify/on_session_end: guard file transfers with a
durable, handoff-friendly contract.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's
hooks/transfer-contract-guard.py (reimplemented from the upstream PreToolUse+PostToolUse+Stop
hook, see mappings/reviewed-hooks.yaml). Every clone/copy/move/sync command is shared mutable
state: a later agent must be able to answer, without reading shell history, what moved, from
where, to where, why, what was verified, and whether the source was removed. See
hermes/skills/safe-deletion/SKILL.md and the templates/transfer-contract.json shape this hook
enforces against.

The one hook spans all three Hermes-adaptation patterns already established in this repo,
verified individually rather than assumed:
  - `pre_tool_call` -- genuinely blocks, same as destructive-command-guard.py etc. A
    clone/copy/move/sync command through `terminal` without a complete
    `# transfer-contract: <path>.json` marker is denied before it runs.
  - `post_tool_call` -- audit-log-only (Hermes discards this event's return value, see
    verify-deleted-guard.py's docstring for the verified mechanism). Reminds to update the
    contract and verify the destination, in the shared safety log + stderr, not live.
  - `pre_verify` + `on_session_end`, dual-registered like session-handoff-reminder.py and
    kb-validate-gate.py -- `pre_verify` gives a genuine live block while an open or invalid
    transfer contract remains, gated on file-edit turns and the session-wide 3-nudge budget
    (now shared with THREE consumers -- session-handoff-reminder.py, kb-validate-gate.py, and
    this hook's Stop-equivalent portion); `on_session_end` is the audit-log fallback that fires
    every turn regardless.

Directory convention: recognizes `.claude/transfers/`, `.agent/transfers/`, `.codex/transfers/`
(cross-harness, unchanged from upstream -- a contract written by another harness working in
the same repo is still enforced) plus `.hermes/transfers/` as the Hermes-native default.

Session ownership (added 2026-08-10, ported from an upstream fix that landed within hours of
this hook's initial port): the first PreToolUse-equivalent (`pre_tool_call`) call that uses a
contract stamps its `session_id` onto it. At the Stop-equivalent gate, an OPEN contract owned
by a DIFFERENT, still-live session is deferred (a stderr note, not a block) -- only unowned,
own-session, or STALE (owner inactive past the TTL) contracts actually block. Without this, one
shared `transfers/` directory meant any session's in-flight transfer blocked every other
session's Stop attempt too -- collateral, and the usual fix for collateral is disabling the
gate. Liveness is checked via `hermes_hook_common.session_is_live()` (a heartbeat file this
hook and session-handoff-check.py/session-handoff-reminder.py all touch), not upstream's
per-session transcript-file mtime -- Hermes has no direct equivalent to Claude Code's
`~/.claude/projects/<slug>/<session-id>.jsonl` transcript, and `event.get("session_id")` is
already always populated on Hermes's wire payload, so no transcript-filename fallback chain is
needed either. # simplification: a contract owned by a NON-Hermes session_id (another harness
working the same repo) has no heartbeat we can check, so it is treated as not-live and can
still block -- multi-harness liveness is not solved, only same-mechanism (Hermes-to-Hermes)
liveness is.

The hook never deletes a source and never invents verification evidence. A second agent can
therefore resume from one small JSON record instead of reconstructing intent from shell
history.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    block,
    event_session_id,
    log,
    read_event,
    session_is_live,
    touch_session_heartbeat,
)

TRANSFER_MARKER = re.compile(
    r"(?:^|[\s;&])#\s*transfer-contract\s*:\s*(?P<path>[^\r\n]+)",
    re.IGNORECASE,
)
STATUS_VALUES = {"planned", "running", "verification_pending", "verified", "failed", "blocked", "cancelled"}
OPEN_STATUSES = {"planned", "running", "verification_pending"}
CLOSED_STATUSES = {"verified", "failed", "blocked", "cancelled"}
MARKER_DIRS = {".hermes", ".claude", ".agent", ".codex"}


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _event_cwd(event: dict[str, Any]) -> Path:
    raw = _text(event.get("cwd"))
    return Path(raw).expanduser() if raw else Path.cwd()


def _tool_input(event: dict[str, Any]) -> dict[str, Any]:
    value = event.get("tool_input")
    return value if isinstance(value, dict) else {}


def _repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or any((candidate / d).exists() for d in MARKER_DIRS):
            return candidate
    return current


def _contract_path(marker: str, cwd: Path) -> Path | None:
    raw = marker.strip().strip('"\'')
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = cwd / candidate
    try:
        candidate = candidate.resolve()
    except OSError:
        return None
    parent = candidate.parent
    if parent.name.lower() != "transfers" or parent.parent.name.lower() not in MARKER_DIRS:
        return None
    if candidate.suffix.lower() != ".json":
        return None
    return candidate


def _marker_path(command: str, cwd: Path) -> Path | None:
    match = TRANSFER_MARKER.search(command)
    return _contract_path(match.group("path"), cwd) if match else None


def _transfer_kind(command: str) -> tuple[str, str] | None:
    checks = (
        (r"\bgit\s+clone\b", "clone", "git"),
        (r"\bgh\s+repo\s+clone\b", "clone", "gh"),
        (r"\brobocopy\b", "move" if re.search(r"/(?:move|mov)\b", command, re.I) else "copy", "robocopy"),
        (r"\brclone\s+(?:copy|copyto)\b", "copy", "rclone"),
        (r"\brclone\s+move\b", "move", "rclone"),
        (r"\brclone\s+sync\b", "sync", "rclone"),
        (r"\brsync\b", "sync", "rsync"),
        (r"\bscp\b", "copy", "scp"),
        (r"\bsftp\b", "copy", "sftp"),
        (r"\bxcopy\b", "copy", "xcopy"),
        (r"\bcopy-item\b", "copy", "powershell"),
        (r"\bmove-item\b", "move", "powershell"),
        (r"(?:^|[;&|])\s*copy\s+", "copy", "copy"),
        (r"(?:^|[;&|])\s*move\s+", "move", "move"),
        (r"(?:^|[;&|])\s*cp\s+", "copy", "cp"),
    )
    for pattern, kind, tool in checks:
        if re.search(pattern, command, re.IGNORECASE):
            return kind, tool
    return None


def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return False


def _valid_deadline(value: Any) -> bool:
    raw = _text(value)
    if not raw:
        return False
    try:
        dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _contract_errors(contract: Any, *, pre_transfer: bool = False) -> list[str]:
    if not isinstance(contract, dict):
        return ["record must be a JSON object"]
    errors: list[str] = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not _nonempty(contract.get("transfer_id")):
        errors.append("transfer_id is required")
    status = _text(contract.get("status"))
    if status not in STATUS_VALUES:
        errors.append(f"status must be one of {sorted(STATUS_VALUES)}")
    if pre_transfer and status not in {"planned", "running"}:
        errors.append("before the command status must be planned or running")
    for name in ("source", "destination", "purpose", "motivation", "next_action"):
        if not _nonempty(contract.get(name)):
            errors.append(f"{name} is required")
    if not _valid_deadline(contract.get("deadline")):
        errors.append("deadline must be an ISO-8601 date/time")

    operation = contract.get("operation")
    if not isinstance(operation, dict):
        errors.append("operation must be an object")
    else:
        for name in ("kind", "tool", "settings"):
            if not _nonempty(operation.get(name)):
                errors.append(f"operation.{name} is required")

    verification = contract.get("verification")
    if not isinstance(verification, dict):
        errors.append("verification must be an object")
    else:
        plan = verification.get("plan")
        if not isinstance(plan, list) or not plan or not all(_nonempty(item) for item in plan):
            errors.append("verification.plan must contain at least one check")
        if not isinstance(verification.get("performed"), bool):
            errors.append("verification.performed must be boolean")

    cleanup = contract.get("source_cleanup")
    if not isinstance(cleanup, dict):
        errors.append("source_cleanup must be an object")
    else:
        for name in ("planned", "performed", "verified"):
            if not isinstance(cleanup.get(name), bool):
                errors.append(f"source_cleanup.{name} must be boolean")
        if not _nonempty(cleanup.get("reason")):
            errors.append("source_cleanup.reason is required")

    if status == "verified":
        if not isinstance(verification, dict) or verification.get("performed") is not True:
            errors.append("verified transfer requires verification.performed=true")
        if not isinstance(verification, dict) or _text(verification.get("result")).lower() not in {"pass", "passed", "ok"}:
            errors.append("verified transfer requires verification.result=pass")
        evidence = verification.get("evidence") if isinstance(verification, dict) else None
        if not isinstance(evidence, list) or not evidence or not all(_nonempty(item) for item in evidence):
            errors.append("verified transfer requires non-empty verification.evidence")
        if isinstance(cleanup, dict) and cleanup.get("planned") and not (
            cleanup.get("performed") is True and cleanup.get("verified") is True
        ):
            errors.append("verified transfer requires performed+verified source cleanup when cleanup is planned")

    if status in {"failed", "blocked", "cancelled"} and not _nonempty(contract.get("closure_reason")):
        errors.append(f"{status} transfer requires closure_reason")
    return errors


def _stamp_owner(path: Path, contract: dict[str, Any], session_id: str) -> None:
    """Record who opened this transfer, so its Stop-equivalent gate is scoped to them.

    Writes once: an existing owner is never overwritten (the first session to use a contract
    keeps it, matching upstream's own one-shot stamp semantics).
    """
    if not session_id or _text(contract.get("session_id")):
        return
    try:
        contract["session_id"] = session_id
        path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        # Ownership is an optimisation for other sessions' Stop gates. Failing to write it
        # must never turn into a blocked transfer.
        pass


def _foreign_and_live(contract: dict[str, Any], current_session: str, hermes_dir: Path) -> str:
    """Owner id when this record belongs to a different, still-live Hermes session."""
    owner = _text(contract.get("session_id"))
    if not owner or owner == current_session:
        return ""
    return owner if session_is_live(hermes_dir, owner) else ""


def _load(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"cannot read {path}: {exc}"
    errors = _contract_errors(value)
    return (value, None) if not errors else (None, "; ".join(errors))


def _tool_matches(operation: dict[str, Any], expected: str) -> bool:
    values = [_text(operation.get("tool")).lower(), _text(operation.get("command_family")).lower()]
    return any(value == expected or expected in value or value in expected for value in values if value)


def _pre(event: dict[str, Any]) -> None:
    if _text(event.get("tool_name")) != "terminal":
        allow()
    command = _text(_tool_input(event).get("command"))
    detected = _transfer_kind(command)
    if detected is None:
        allow()
    cwd = _event_cwd(event)
    marker = TRANSFER_MARKER.search(command)
    if marker is None:
        block(
            "Transfer command detected but no durable contract was provided. "
            "Create .hermes/transfers/<id>.json first, then append "
            "'# transfer-contract: .hermes/transfers/<id>.json' to the command."
        )
    path = _contract_path(marker.group("path"), cwd)
    if path is None:
        block("Transfer contract path must be a JSON file under .hermes/transfers/ (or .claude/, .agent/, .codex/transfers/).")
    if not path.is_file():
        block(f"Transfer contract does not exist: {path}. Write the contract before starting the transfer.")
    contract, error = _load(path)
    if error or contract is None:
        block(f"Invalid transfer contract {path}: {error}")
    errors = _contract_errors(contract, pre_transfer=True)
    kind, expected_tool = detected
    operation = contract.get("operation", {})
    if _text(operation.get("kind")).lower() != kind:
        errors.append(f"operation.kind={kind!r} is required for this command")
    if not _tool_matches(operation, expected_tool):
        errors.append(f"operation.tool must describe {expected_tool!r} for this command")
    if errors:
        block(f"Transfer contract is incomplete ({path}): " + "; ".join(errors))
    _stamp_owner(path, contract, event_session_id(event))
    log("INFO", "transfer_contract", "allowed", f"{kind}:{expected_tool}", str(path))
    allow()


def _post(event: dict[str, Any]) -> None:
    if _text(event.get("tool_name")) != "terminal":
        allow()
    command = _text(_tool_input(event).get("command"))
    detected = _transfer_kind(command)
    if detected is None:
        allow()
    extra = event.get("extra", {}) or {}
    failed = extra.get("status") == "error"
    outcome = "failed" if failed else "verification_pending"
    log("INFO", "transfer_contract", outcome, "post-run-reminder", command[:200])
    sys.stderr.write(
        f"[transfer_contract] {outcome}: update the marked contract, verify the destination, "
        "and record source cleanup explicitly before closing the task.\n"
    )
    allow()


def _local_path(value: Any, root: Path) -> Path | None:
    raw = _text(value)
    if not raw or re.match(r"^(?:[a-z]+://|[^\\/\s]+@[^\\/\s:]+:)", raw, re.I):
        return None
    try:
        candidate = Path(raw).expanduser()
        return (candidate if candidate.is_absolute() else root / candidate).resolve()
    except OSError:
        return None


def _verified_path_errors(contract: dict[str, Any], root: Path) -> list[str]:
    if _text(contract.get("status")) != "verified":
        return []
    errors: list[str] = []
    destination = _local_path(contract.get("destination"), root)
    if destination is not None and not destination.exists():
        errors.append(f"destination is absent: {destination}")
    cleanup = contract.get("source_cleanup") or {}
    source = _local_path(contract.get("source"), root)
    if cleanup.get("planned") and cleanup.get("performed") and source is not None and source.exists():
        errors.append(f"source still exists after claimed cleanup: {source}")
    return errors


def _transfer_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for name in MARKER_DIRS:
        directory = root / name / "transfers"
        if directory.is_dir():
            paths.extend(sorted(directory.glob("*.json")))
    return paths


def _stop_issues(root: Path, current_session: str, hermes_dir: Path) -> tuple[list[str], list[str]]:
    """Return (blocking issues for this session, notes about other live sessions')."""
    issues: list[str] = []
    deferred: list[str] = []
    for path in _transfer_files(root):
        contract, error = _load(path)
        if error or contract is None:
            # A record too broken to parse has no readable owner, so it is everyone's
            # problem until someone repairs it.
            issues.append(f"{path.name}: {error}")
            continue
        owner = _foreign_and_live(contract, current_session, hermes_dir)
        status = _text(contract.get("status"))
        if owner:
            if status in OPEN_STATUSES or _contract_errors(contract) or _verified_path_errors(contract, root):
                deferred.append(f"{path.name} (status={status}, owner session {owner} still live)")
            continue
        if status in OPEN_STATUSES:
            issues.append(
                f"{path.name}: status={status}; next_action={_text(contract.get('next_action')) or 'missing'}"
            )
        elif status in CLOSED_STATUSES:
            issues.extend(f"{path.name}: {item}" for item in _contract_errors(contract))
            issues.extend(f"{path.name}: {item}" for item in _verified_path_errors(contract, root))
    return issues, deferred


def _stop_reason(event: dict[str, Any]) -> str | None:
    """Pure decision (shared by pre_verify and on_session_end): a block-reason string, or
    None to allow. Logs (stderr) any contracts deferred to a still-live foreign session."""
    root = _repo_root(_event_cwd(event))
    hermes_dir = root / ".hermes"
    issues, deferred = _stop_issues(root, event_session_id(event), hermes_dir)
    if deferred:
        sys.stderr.write(
            "[transfer_contract] left to their owners (live sessions, not yours): "
            + " | ".join(deferred)
            + "\n"
        )
    if not issues:
        return None
    return (
        "Open or unverifiable file transfer contracts remain. Finish the transfer, "
        "record verification/source cleanup, or mark the record failed/blocked with "
        "a closure_reason. " + " | ".join(issues[:5])
    )


def _stop(event: dict[str, Any], hook_event: str) -> None:
    reason = _stop_reason(event)
    if reason is None:
        allow()
    log("WARN", "transfer_contract", "blocked", "open-or-invalid-transfer", reason[:400])
    if hook_event == "pre_verify":
        print(json.dumps({"action": "continue", "message": reason}, ensure_ascii=False))
    else:
        # on_session_end: return value is discarded by Hermes (see module docstring and
        # verify-deleted-guard.py's) -- audit-log-only. stderr kept for potential visibility
        # via Hermes's own logger.
        sys.stderr.write(f"[transfer_contract] {reason}\n")
    sys.exit(0)


def _self_test() -> int:
    """Prove the ownership rule on real files in a real temp tree."""
    import tempfile

    fails: list[str] = []
    base_contract = {
        "schema_version": 1,
        "transfer_id": "t",
        "status": "planned",
        "source": "ssh://host/src",
        "destination": "rclone://remote:dst",
        "purpose": "p",
        "motivation": "m",
        "next_action": "n",
        "deadline": "2026-12-31T00:00:00+00:00",
        "operation": {"kind": "copy", "tool": "rclone", "settings": "s"},
        "verification": {"plan": ["check"], "performed": False},
        "source_cleanup": {"planned": False, "performed": False, "verified": False, "reason": "r"},
    }

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw) / "repo"
        hermes_dir = repo / ".hermes"
        transfers = hermes_dir / "transfers"
        transfers.mkdir(parents=True)

        live, stale, mine = "live-owner", "stale-owner", "my-session"
        touch_session_heartbeat(hermes_dir, live)
        touch_session_heartbeat(hermes_dir, stale)
        stale_heartbeat = hermes_dir / "sessions" / stale / "heartbeat"
        import os
        import time

        ancient = time.time() - 1800 - 600
        os.utime(stale_heartbeat, (ancient, ancient))

        def put(name: str, **over: Any) -> Path:
            record = json.loads(json.dumps(base_contract))
            record.update(over)
            path = transfers / f"{name}.json"
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            return path

        cases = [
            ("open record owned by me", {"session_id": mine}, True),
            ("open record, owner still live", {"session_id": live}, False),
            ("open record, owner gone stale", {"session_id": stale}, True),
            ("open record with no owner at all", {}, True),
            ("closed record, owner live", {"session_id": live, "status": "cancelled", "closure_reason": "c"}, False),
        ]
        for label, over, should_block in cases:
            for leftover in transfers.glob("*.json"):
                leftover.unlink()
            put("case", **over)
            issues, deferred = _stop_issues(repo, mine, hermes_dir)
            if bool(issues) != should_block:
                fails.append(f"{label}: expected block={should_block}, issues={issues}, deferred={deferred}")

        for leftover in transfers.glob("*.json"):
            leftover.unlink()
        (transfers / "broken.json").write_text("{not json", encoding="utf-8")
        if not _stop_issues(repo, mine, hermes_dir)[0]:
            fails.append("unparseable record did not block")

        for leftover in transfers.glob("*.json"):
            leftover.unlink()
        path = put("mine-broken", session_id=mine, status="verified")
        if not _stop_issues(repo, mine, hermes_dir)[0]:
            fails.append("verified record without evidence did not block its owner")

        for leftover in transfers.glob("*.json"):
            leftover.unlink()
        path = put("stamp")
        record = json.loads(path.read_text(encoding="utf-8"))
        _stamp_owner(path, record, mine)
        if json.loads(path.read_text(encoding="utf-8")).get("session_id") != mine:
            fails.append("owner was not stamped onto an unowned record")
        _stamp_owner(path, json.loads(path.read_text(encoding="utf-8")), "someone-else")
        if json.loads(path.read_text(encoding="utf-8")).get("session_id") != mine:
            fails.append("existing owner was overwritten")

        if session_is_live(hermes_dir, "no-such-session"):
            fails.append("an unknown session was reported alive")
        if event_session_id({"session_id": "../escape"}):
            fails.append("a path-traversing session id was not rejected")

    for line in fails:
        print("FAIL:", line)
    print("transfer-contract-guard self-test:", "FAILED" if fails else "ok")
    return 1 if fails else 0


def main() -> None:
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    event = read_event()
    if not event:
        allow()
    hook_event = _text(event.get("hook_event_name"))
    touch_session_heartbeat(_event_cwd(event) / ".hermes", event_session_id(event))
    if hook_event == "pre_tool_call":
        _pre(event)
    elif hook_event == "post_tool_call":
        _post(event)
    elif hook_event in ("pre_verify", "on_session_end"):
        _stop(event, hook_event)
    else:
        allow()


if __name__ == "__main__":
    main()
