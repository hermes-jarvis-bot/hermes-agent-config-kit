#!/usr/bin/env python3
"""pre_tool_call: auto-snapshot a DB before an already-bypassed destructive SQL command, then
verify the dump is real before saying so.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/db-snapshot-guard.py, reimplemented for Hermes Agent's
shell-hook contract (see hermes_hook_common.py for the exact I/O differences from the upstream
Claude-Code version this was read from).

Never blocks — this is a safety net alongside a blocking guard (e.g. destructive-command-guard.py
covers DROP/TRUNCATE patterns), not a replacement for one. It only activates once a destructive
SQL command is about to run anyway (bypass already granted), takes a best-effort dump, verifies
the dump is non-empty/non-truncated per engine (PostgreSQL/MySQL/MongoDB), and prints the result
to stderr — then always allows. Missing dump tooling (no pg_dump/mysqldump/mongodump on PATH) is
reported the same way: a loud warning, never a block, so a machine without backup tooling
installed cannot be locked out of legitimate destructive work.

Bypass: HERMES_ALLOW_DB_SNAPSHOT=1 or a `# hermes-bypass: db-snapshot` marker in the command text
(use only on testing/throwaway DBs — this suppresses the safety net entirely, not just the
snapshot).

Never invoked automatically by this adapter. Copied by scripts/install_hermes.py into
<hermes-home>/hooks/config-kit/; the operator must add a `hooks: pre_tool_call:` entry pointing
at it in their own ~/.hermes/config.yaml by hand — see hermes/hooks/README.md.
"""
from __future__ import annotations

import datetime as _dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    any_match,
    bypass,
    log,
    read_event,
    terminal_command,
)

SQL_DESTRUCTIVE_PATTERNS = [
    r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b",
    r"\bTRUNCATE\s+TABLE\b",
    r"\bdropdb\b",
    r"\bmongo\s+.*\bdropDatabase\b",
    r"\bredis-cli\s+.*\bflushall\b",
    r"\bDELETE\s+FROM\s+\w+\s*(;|$)",
]

MIN_PG_SIZE = 200      # empty PG schema dump baseline
MIN_MYSQL_SIZE = 200
MIN_BSON_SIZE = 1       # any non-empty bson

SNAPSHOT_DIR = Path("/tmp")


def now_ts() -> str:
    return _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def find_pg_url(cmd: str) -> str | None:
    m = re.search(r"postgres(?:ql)?://[^\s\"';]+", cmd)
    return m.group(0) if m else None


def find_mysql_dsn(cmd: str) -> dict | None:
    if not re.search(r"\bmysql\b|\bmysqldump\b", cmd):
        return None
    h = re.search(r"-h\s*(\S+)", cmd)
    u = re.search(r"-u\s*(\S+)", cmd)
    db = re.search(r"\b(?:mysql|mysqldump)\s+(?:[-\w\s]+\s+)?(\S+)\s*$", cmd)
    return {
        "host": h.group(1) if h else "localhost",
        "user": u.group(1) if u else None,
        "db": db.group(1) if db else None,
    }


def find_mongo_url(cmd: str) -> str | None:
    m = re.search(r"mongodb(?:\+srv)?://[^\s\"';]+", cmd)
    return m.group(0) if m else None


def try_pg_snapshot(url: str, out_path: Path) -> tuple[bool, str]:
    if not shutil.which("pg_dump"):
        return False, "pg_dump not in PATH"
    try:
        proc = subprocess.run(
            ["pg_dump", "--no-owner", "--no-acl", "-f", str(out_path), url],
            capture_output=True, text=True, timeout=180,
        )
        if proc.returncode == 0:
            return True, "pg_dump exit 0"
        return False, f"pg_dump exit {proc.returncode}: {proc.stderr.strip()[:200]}"
    except subprocess.TimeoutExpired:
        return False, "pg_dump timed out (180s)"
    except OSError as e:
        return False, f"pg_dump OSError: {e}"


def try_mysql_snapshot(dsn: dict, out_path: Path) -> tuple[bool, str]:
    if not shutil.which("mysqldump"):
        return False, "mysqldump not in PATH"
    if not dsn.get("db"):
        return False, "no db name extracted"
    args = ["mysqldump", "-h", dsn["host"]]
    if dsn.get("user"):
        args += ["-u", dsn["user"]]
    args += [dsn["db"]]
    try:
        with out_path.open("wb") as fh:
            proc = subprocess.run(args, stdout=fh, stderr=subprocess.PIPE, timeout=180)
        if proc.returncode == 0:
            return True, "mysqldump exit 0"
        return False, f"mysqldump exit {proc.returncode}: {proc.stderr.decode()[:200]}"
    except subprocess.TimeoutExpired:
        return False, "mysqldump timed out (180s)"
    except OSError as e:
        return False, f"mysqldump OSError: {e}"


def try_mongo_snapshot(url: str, out_dir: Path) -> tuple[bool, str]:
    if not shutil.which("mongodump"):
        return False, "mongodump not in PATH"
    try:
        proc = subprocess.run(
            ["mongodump", f"--uri={url}", f"--out={out_dir}"],
            capture_output=True, text=True, timeout=180,
        )
        if proc.returncode == 0:
            return True, "mongodump exit 0"
        return False, f"mongodump exit {proc.returncode}: {proc.stderr.strip()[:200]}"
    except subprocess.TimeoutExpired:
        return False, "mongodump timed out (180s)"
    except OSError as e:
        return False, f"mongodump OSError: {e}"


def verify_pg_snapshot(out_path: Path) -> tuple[bool, str]:
    if not out_path.exists():
        return False, "file does not exist"
    size = out_path.stat().st_size
    if size < MIN_PG_SIZE:
        return False, f"too small ({size} bytes < {MIN_PG_SIZE} threshold)"
    try:
        text = out_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"unreadable: {e}"
    if "PostgreSQL database dump complete" not in text:
        return False, "missing footer (likely truncated mid-dump)"
    has_create = bool(re.search(r"^CREATE\s+(TABLE|SCHEMA|TYPE|INDEX)", text, re.MULTILINE))
    has_data = bool(re.search(r"^COPY\s+\w+|^INSERT\s+INTO\s+", text, re.MULTILINE))
    if not (has_create or has_data):
        return False, "no CREATE or COPY/INSERT statements found"
    n_stmts = text.count("\nCOPY ") + text.count("\nINSERT INTO ") + text.count("\nCREATE ")
    return True, f"size={size}B, statements~{n_stmts}, footer OK"


def verify_mysql_snapshot(out_path: Path) -> tuple[bool, str]:
    if not out_path.exists():
        return False, "file does not exist"
    size = out_path.stat().st_size
    if size < MIN_MYSQL_SIZE:
        return False, f"too small ({size} bytes < {MIN_MYSQL_SIZE})"
    try:
        text = out_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"unreadable: {e}"
    if "Dump completed" not in text:
        return False, "missing 'Dump completed' footer"
    has_create = "CREATE TABLE" in text
    has_data = bool(re.search(r"^INSERT\s+INTO\s+", text, re.MULTILINE))
    if not (has_create or has_data):
        return False, "no CREATE TABLE or INSERT statements"
    n_stmts = text.count("CREATE TABLE") + text.count("INSERT INTO ")
    return True, f"size={size}B, statements~{n_stmts}, footer OK"


def verify_mongo_snapshot(out_dir: Path) -> tuple[bool, str]:
    if not out_dir.exists() or not out_dir.is_dir():
        return False, "output dir missing"
    bson_files = list(out_dir.rglob("*.bson"))
    if not bson_files:
        return False, "no .bson files produced"
    non_empty = [f for f in bson_files if f.stat().st_size >= MIN_BSON_SIZE]
    if not non_empty:
        return False, f"all {len(bson_files)} .bson files are empty"
    missing_meta = [
        f for f in non_empty
        if not f.with_suffix(".metadata.json").exists()
        and not (f.parent / (f.stem + ".metadata.json")).exists()
    ]
    total_bytes = sum(f.stat().st_size for f in non_empty)
    note = f", {len(missing_meta)} without metadata" if missing_meta else ""
    return True, f"collections={len(non_empty)}, total={total_bytes}B{note}"


def warn(msg: str) -> None:
    sys.stderr.write(f"[db-snapshot-guard] {msg}\n")


def process_pg(cmd: str, ts: str) -> list[str]:
    pg = find_pg_url(cmd)
    if not pg:
        return []
    out = SNAPSHOT_DIR / f"db-snapshot-pg-{ts}.sql"
    msgs = []
    ok, info = try_pg_snapshot(pg, out)
    if not ok:
        msgs.append(f"PG SNAPSHOT FAILED: {info}")
        return msgs
    v_ok, v_info = verify_pg_snapshot(out)
    if v_ok:
        msgs.append(f"PG snapshot OK -> {out} ({v_info})")
    else:
        msgs.append(f"PG snapshot CREATED BUT VERIFY FAILED -> {out} ({v_info})")
        msgs.append("  ^ dump may be incomplete/truncated. Check it by hand before the DROP.")
    return msgs


def process_mysql(cmd: str, ts: str) -> list[str]:
    dsn = find_mysql_dsn(cmd)
    if not dsn:
        return []
    out = SNAPSHOT_DIR / f"db-snapshot-mysql-{ts}.sql"
    msgs = []
    ok, info = try_mysql_snapshot(dsn, out)
    if not ok:
        msgs.append(f"MySQL SNAPSHOT FAILED: {info}")
        return msgs
    v_ok, v_info = verify_mysql_snapshot(out)
    if v_ok:
        msgs.append(f"MySQL snapshot OK -> {out} ({v_info})")
    else:
        msgs.append(f"MySQL snapshot CREATED BUT VERIFY FAILED -> {out} ({v_info})")
        msgs.append("  ^ dump looks suspect. Check it by hand.")
    return msgs


def process_mongo(cmd: str, ts: str) -> list[str]:
    mongo = find_mongo_url(cmd)
    if not mongo:
        return []
    out_dir = SNAPSHOT_DIR / f"db-snapshot-mongo-{ts}"
    msgs = []
    ok, info = try_mongo_snapshot(mongo, out_dir)
    if not ok:
        msgs.append(f"Mongo SNAPSHOT FAILED: {info}")
        return msgs
    v_ok, v_info = verify_mongo_snapshot(out_dir)
    if v_ok:
        msgs.append(f"Mongo snapshot OK -> {out_dir} ({v_info})")
    else:
        msgs.append(f"Mongo snapshot CREATED BUT VERIFY FAILED -> {out_dir} ({v_info})")
        msgs.append("  ^ collections may be incomplete. Check by hand.")
    return msgs


def main() -> None:
    event = read_event()
    if event.get("tool_name") != "terminal":
        allow()

    cmd = terminal_command(event.get("tool_input", {}))
    if not cmd:
        allow()

    hit = any_match(cmd, SQL_DESTRUCTIVE_PATTERNS)
    if not hit:
        allow()

    if bypass("db-snapshot", cmd):
        log("INFO", "db_snapshot_guard", "skip-bypassed", hit, cmd)
        allow()

    ts = now_ts()
    all_msgs: list[str] = []
    all_msgs += process_pg(cmd, ts)
    all_msgs += process_mysql(cmd, ts)
    all_msgs += process_mongo(cmd, ts)

    if not all_msgs:
        all_msgs.append(
            "no recognizable connection string in command -- snapshot SKIPPED. "
            "If the destructive op uses env DATABASE_URL or psql with .pgpass, "
            "auto-snapshot can't see it. Make a manual backup first."
        )

    any_verified = any("snapshot OK" in m for m in all_msgs)
    any_failed_verify = any("VERIFY FAILED" in m for m in all_msgs)
    any_creation_failed = any("SNAPSHOT FAILED" in m for m in all_msgs)
    if any_verified and not any_failed_verify:
        verdict = "snapshot-verified"
    elif any_verified and any_failed_verify:
        verdict = "snapshot-partial"
    elif any_failed_verify:
        verdict = "snapshot-suspect"
    elif any_creation_failed:
        verdict = "snapshot-failed"
    else:
        verdict = "snapshot-skipped"

    log("WARN", "db_snapshot_guard", verdict, hit, cmd[:300])

    for m in all_msgs:
        warn(m)
    if any_verified:
        warn("Recovery hint: psql -f <snapshot.sql> <restore-target> (or mysql/mongorestore equivalents)")
    if any_failed_verify or any_creation_failed:
        warn("Snapshot has problems -- consider aborting the destructive op or making a manual backup first.")
    allow()


if __name__ == "__main__":
    main()
