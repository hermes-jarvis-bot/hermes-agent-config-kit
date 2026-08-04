#!/usr/bin/env python3
"""Deterministic half of distill-feedback: turn a queued session backlog into review-ready input.

Reviewed-script lane (see SECURITY.md and mappings/reviewed-scripts.yaml).
Source: AnastasiyaW/claude-code-config/skills/development/distill-feedback/scripts/extract_feedback_queue.py
Ported unmodified after full manual review: stdlib-only (argparse, json, sys, datetime, pathlib,
tempfile in the self-test only), no network calls, no subprocess/os.system/eval/exec. It reads
~/.claude/feedback/queue.jsonl and the referenced session transcripts, and only ever appends to
~/.claude/feedback/processed.jsonl — it never rewrites or deletes either file. See the skill's
SKILL.md "Prerequisite" section: the queue file is populated by a separate Claude-Code Stop hook
that is not part of this adapter; if nothing populates it, this script correctly reports zero
pending items. Run it yourself and read it before trusting it.
"""
from __future__ import annotations

import argparse
import json
import sys
import datetime as _dt
from pathlib import Path

FEEDBACK_DIR = Path.home() / ".claude" / "feedback"
QUEUE_PATH = FEEDBACK_DIR / "queue.jsonl"
PROCESSED_PATH = FEEDBACK_DIR / "processed.jsonl"


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return []
    return out


def pending_sessions() -> list[dict]:
    processed = {r.get("session_id") for r in _read_jsonl(PROCESSED_PATH)}
    seen: set[str] = set()
    out = []
    for rec in _read_jsonl(QUEUE_PATH):
        sid = rec.get("session_id")
        if not sid or sid in processed or sid in seen:
            continue
        seen.add(sid)
        out.append(rec)
    return out


def extract_user_turns(transcript_path: str) -> list[str]:
    """Pull genuine human turns (skip tool_result echoes / summaries / empties)."""
    if not transcript_path:
        return []
    p = Path(transcript_path)
    if not p.exists():
        return []
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    turns = []
    for line in lines:
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (obj.get("type") or obj.get("message", {}).get("type")) == "summary":
            continue
        role = obj.get("role") or obj.get("message", {}).get("role")
        if role != "user":
            continue
        content = obj.get("content")
        if content is None:
            content = obj.get("message", {}).get("content")
        if isinstance(content, list):
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                continue
            text = " ".join(
                b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
            )
        else:
            text = content if isinstance(content, str) else ""
        text = text.strip()
        # Skip slash-command envelopes and system-reminder-only turns.
        if text and not text.startswith("<"):
            turns.append(text)
    return turns


def mark_processed(session_ids: list[str]) -> int:
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with PROCESSED_PATH.open("a", encoding="utf-8") as fh:
        for sid in session_ids:
            fh.write(json.dumps({"session_id": sid, "processed_at": stamp}, ensure_ascii=False) + "\n")
    return len(session_ids)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=0, help="max sessions to emit (0 = all)")
    ap.add_argument("--mark-processed", nargs="+", metavar="SID", help="log these sessions as distilled")
    args = ap.parse_args()

    if args.mark_processed:
        n = mark_processed(args.mark_processed)
        print(json.dumps({"marked_processed": n}, ensure_ascii=False))
        return 0

    sessions = pending_sessions()
    if args.limit > 0:
        sessions = sessions[: args.limit]
    payload = []
    for rec in sessions:
        turns = extract_user_turns(rec.get("transcript_path", ""))
        if not turns:
            continue
        payload.append(
            {
                "session_id": rec.get("session_id", ""),
                "cwd": rec.get("cwd", ""),
                "ts": rec.get("ts", ""),
                "user_turns": turns,
            }
        )
    print(json.dumps({"pending": len(sessions), "sessions": payload}, ensure_ascii=False, indent=2))
    return 0


def _self_test() -> int:
    import tempfile

    global FEEDBACK_DIR, QUEUE_PATH, PROCESSED_PATH
    tmp = Path(tempfile.mkdtemp())
    tx = tmp / "t.jsonl"
    tx.write_text(
        "\n".join(
            [
                json.dumps({"type": "user", "message": {"role": "user", "content": "do X"}}),
                json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "z"}]}}),
                json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": "no, do Y"}]}}),
            ]
        ),
        encoding="utf-8",
    )
    assert extract_user_turns(str(tx)) == ["do X", "no, do Y"], "extract human turns only"
    FEEDBACK_DIR = tmp
    QUEUE_PATH = tmp / "queue.jsonl"
    PROCESSED_PATH = tmp / "processed.jsonl"
    QUEUE_PATH.write_text(
        "\n".join([json.dumps({"session_id": "s1", "transcript_path": str(tx)}),
                   json.dumps({"session_id": "s2", "transcript_path": str(tx)})]),
        encoding="utf-8",
    )
    assert len(pending_sessions()) == 2
    mark_processed(["s1"])
    assert [s["session_id"] for s in pending_sessions()] == ["s2"], "processed excluded"
    print("self-test OK")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    sys.exit(main())
