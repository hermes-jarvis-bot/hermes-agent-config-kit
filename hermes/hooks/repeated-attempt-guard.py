#!/usr/bin/env python3
"""pre_tool_call + post_tool_call: stop the guess-and-retry loop -- no fourth try at the same
target without reading something first.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/repeated-attempt-guard.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

The loop this exists for is only visible ACROSS calls -- attempt, fail, vary the surface,
attempt again -- and a hook that receives one tool call with no history cannot see it, however
good the always-on "do not guess" rule is under task pressure. So this one remembers attempts.
The rule it enforces is deliberately narrow and always satisfiable by the cheap correct action:

    You may not make a FOURTH attempt at a target that has failed three times unless you have
    read something since the last failure.

Reading anything -- the resolver, the spec, the error's source -- clears it.

Wire on BOTH events:
    post_tool_call -- records outcomes (reads Hermes's own derived extra.status/error_type,
                      confirmed present via model_tools.py's _emit_post_tool_call_hook; this
                      adapter never needs to re-parse a raw result blob).
    pre_tool_call   -- reads the record and decides.

post_tool_call's return value is discarded by Hermes (fire-and-forget, same as
verify-deleted-guard.py/over-engineering-advisor.py) -- fine here, since the post_tool_call side
only needs the side effect of recording, never a decision.

Adaptations from upstream:
  - Tool-name sets translated to Hermes's actual registry (toolsets.py's file_tools list):
    ACTING = {terminal, write_file, patch} (no separate MultiEdit -- patch covers it),
    CONSULTING = {read_file, search_files} (no separate Grep/Glob -- search_files covers both;
    this matches Hermes's own internal `_READ_SEARCH_TOOLS` grouping in model_tools.py).
  - `failed()` reads Hermes's already-derived `extra.status == "error"` instead of re-parsing a
    raw `tool_response` blob -- Hermes computes this once per call (model_tools.py's
    `_tool_result_observer_fields`) and hands it to every post_tool_call listener, so
    re-deriving it here would just be a second, less-informed copy of the same check.
  - State path defaults to ~/.hermes/state/attempts.jsonl (HERMES_RETRY_STATE override).
    Tunables: HERMES_RETRY_SOFT/HERMES_RETRY_HARD/HERMES_RETRY_WINDOW_SEC.
    Bypass: HERMES_ALLOW_RETRY_LOOP=1, or `# hermes-bypass: retry-loop` in the command/args.
  - Block verdict emitted via hermes_hook_common.block() (Hermes-canonical
    {"action":"block","message":...} shape) instead of upstream's Claude-Code-style
    {"decision":"block","reason":...}.

Self-test: python3 repeated-attempt-guard.py --self-test
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    block,
    bypass,
    bypass_env,
    file_path,
    read_event,
    terminal_command,
)

WARN_AFTER_FAILURES = int(os.environ.get("HERMES_RETRY_SOFT", "2"))
BLOCK_AFTER_FAILURES = int(os.environ.get("HERMES_RETRY_HARD", "3"))
WINDOW = int(os.environ.get("HERMES_RETRY_WINDOW_SEC", "3600"))

STATE = Path(os.environ.get("HERMES_RETRY_STATE", str(Path.home() / ".hermes" / "state" / "attempts.jsonl")))

ACTING = {"terminal", "write_file", "patch"}
CONSULTING = {"read_file", "search_files"}

_FLAG = re.compile(r"^-")
_PATHISH = re.compile(r"[\\/]|\.[A-Za-z0-9]{1,5}$")
MAX_KEY_TOKENS = 14


def target_key(tool: str, tool_input: dict) -> str:
    """A stable name for 'the thing being attempted'. Flags are dropped, arguments kept --
    a flag is the surface variation a guess-and-retry loop consists of, an argument is what
    the attempt is aimed at."""
    if tool in ("write_file", "patch"):
        p = file_path(tool_input)
        return f"file:{Path(p).name.lower()}" if p else ""
    cmd = terminal_command(tool_input).strip()
    if not cmd:
        return ""
    tokens = [t for t in cmd.split() if not _FLAG.match(t)][:MAX_KEY_TOKENS]
    if not tokens:
        return ""
    parts = []
    for raw in tokens:
        raw = raw.strip("\"'")
        parts.append(Path(raw).name.lower() if _PATHISH.search(raw) else raw.lower())
    return "cmd:" + ":".join(parts)


def failed(extra: dict) -> bool:
    """Did the call fail? Reads Hermes's own derived status -- never invents a failure from
    an unknown shape."""
    return (extra or {}).get("status") == "error"


def _load(now: float) -> list[dict]:
    try:
        rows = [json.loads(l) for l in STATE.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    except (OSError, ValueError):
        return []
    return [r for r in rows if now - float(r.get("ts", 0)) <= WINDOW]


def _append(row: dict) -> None:
    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        with STATE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        pass


def assess(rows: list[dict], key: str) -> tuple[int, bool]:
    """How many failures for this key, and has anything been read since the last one."""
    fails = [r for r in rows if r.get("key") == key and r.get("kind") == "fail"]
    if not fails:
        return 0, True
    last = max(float(r["ts"]) for r in fails)
    consulted = any(r.get("kind") == "read" and float(r.get("ts", 0)) > last for r in rows)
    return len(fails), consulted


def record(event: dict) -> None:
    tool = event.get("tool_name") or ""
    ti = event.get("tool_input") or {}
    extra = event.get("extra") or {}
    now = time.time()
    if tool in CONSULTING:
        _append({"ts": now, "kind": "read", "key": target_key(tool, ti) or tool})
    elif tool in ACTING and failed(extra):
        key = target_key(tool, ti)
        if key:
            _append({"ts": now, "kind": "fail", "key": key})


def decide(event: dict) -> None:
    tool = event.get("tool_name") or ""
    ti = event.get("tool_input") or {}
    if tool not in ACTING:
        allow()
    blob = json.dumps(ti, ensure_ascii=False)
    if "hermes-bypass: retry-loop" in blob:
        allow()
    key = target_key(tool, ti)
    if not key:
        allow()

    n, consulted = assess(_load(time.time()), key)
    if consulted or n < WARN_AFTER_FAILURES:
        allow()

    where = key.split(":", 1)[1]
    if n < BLOCK_AFTER_FAILURES:
        sys.stderr.write(
            f"[repeated-attempt-guard] '{where}' has failed {n} times and nothing has been "
            f"read since the last failure. The next variation is a guess at the shape of the "
            f"answer. Open the thing that defines it -- the resolver, the schema, the error's "
            f"source -- before trying again.\n"
        )
        allow()

    block(
        f"Attempt {n + 1} at '{where}'. It has failed {n} times and nothing has been read "
        f"since the last failure, so each attempt has been a guess at a shape that could be "
        f"looked up. Read the definition -- the resolver, schema, or source of the error -- "
        f"then retry; a single read clears this. Deliberate override: "
        f"HERMES_ALLOW_RETRY_LOOP=1 or '# hermes-bypass: retry-loop' in the command."
    )


def main() -> None:
    if bypass_env("HERMES_ALLOW_RETRY_LOOP"):
        allow()
    event = read_event()
    hook = event.get("hook_event_name") or ""
    if hook == "post_tool_call":
        record(event)
        return
    decide(event)


def self_test() -> int:
    import contextlib
    import io
    import tempfile

    failures = []

    def run_decide(event: dict) -> str:
        """Call decide(), capturing whether it emitted a block JSON on stdout or just
        allowed (allow()/block() both exit via sys.exit(0) -- stdout content is what
        actually distinguishes them, same signal Hermes itself reads)."""
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                decide(event)
        except SystemExit:
            pass
        return "block" if buf.getvalue().strip() else "allow"

    def check(label, got, want):
        if got != want:
            failures.append(f"{label}: got {got!r}, want {want!r}")
        print(f"  [{'ok ' if got == want else 'FAIL'}] {label}")

    check("write_file key is the filename",
          target_key("write_file", {"file_path": "C:/a/b/Resolver.py"}), "file:resolver.py")
    check("same file from another directory keys the same",
          target_key("patch", {"file_path": "/other/resolver.py"}), "file:resolver.py")
    check("command key survives a changed flag",
          target_key("terminal", {"command": "python build.py --fast"}),
          target_key("terminal", {"command": "python build.py --slow -v"}))
    check("a cd prefix does not swallow the command after it",
          target_key("terminal", {"command": 'cd "D:/work/some-project" && git checkout -q master'}),
          "cmd:cd:some-project:&&:git:checkout:master")
    check("two commands in one directory stay distinct",
          target_key("terminal", {"command": "cd /repo && git push"}) !=
          target_key("terminal", {"command": "cd /repo && git status"}), True)
    check("the same command in two projects stays distinct",
          target_key("terminal", {"command": "cd /a/proj-one && npm test"}) !=
          target_key("terminal", {"command": "cd /a/proj-two && npm test"}), True)
    check("bare navigation is still its own attempt",
          target_key("terminal", {"command": "cd /nowhere"}), "cmd:cd:nowhere")
    check("failure detected from extra.status",
          failed({"status": "error", "error_type": "tool_error"}), True)
    check("success is not invented", failed({"status": "ok"}), False)
    check("unknown shape counts as success", failed({}), False)

    now = time.time()
    key = "cmd:python:build.py"
    three = [{"ts": now - 30, "kind": "fail", "key": key}] * 3
    check("three failures, nothing read -> counted", assess(three, key), (3, False))
    with_read = three + [{"ts": now - 1, "kind": "read", "key": "file:resolver.py"}]
    check("a read after the last failure clears it", assess(with_read, key)[1], True)
    early_read = [{"ts": now - 60, "kind": "read", "key": "x"}] + three
    check("a read BEFORE the last failure does not clear it", assess(early_read, key)[1], False)
    check("unrelated key is untouched", assess(three, "cmd:other")[0], 0)

    global STATE
    with tempfile.TemporaryDirectory() as td:
        saved = STATE
        try:
            STATE = Path(td) / "attempts.jsonl"
            for _ in range(WARN_AFTER_FAILURES):
                record({"hook_event_name": "post_tool_call", "tool_name": "terminal",
                        "tool_input": {"command": "python build.py"},
                        "extra": {"status": "error"}})
            rows = _load(time.time())
            check("failures persisted", len([r for r in rows if r["kind"] == "fail"]), WARN_AFTER_FAILURES)

            check("advisory at the soft threshold, not a block",
                  run_decide({"tool_name": "terminal", "tool_input": {"command": "python build.py"}}),
                  "allow")

            record({"hook_event_name": "post_tool_call", "tool_name": "terminal",
                    "tool_input": {"command": "python build.py"},
                    "extra": {"status": "error"}})
            check("bypass marker is honoured",
                  run_decide({"tool_name": "terminal",
                              "tool_input": {"command": "# hermes-bypass: retry-loop\npython build.py"}}),
                  "allow")

            record({"hook_event_name": "post_tool_call", "tool_name": "read_file",
                    "tool_input": {"file_path": "resolver.py"}, "extra": {"status": "ok"}})
            n, consulted = assess(_load(time.time()), "cmd:python:build.py")
            check("reading the source clears the block", consulted, True)
        finally:
            STATE = saved

    print("\nSELF-TEST:", "PASS" if not failures else "FAIL")
    for f in failures:
        print("  -", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
