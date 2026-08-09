#!/usr/bin/env python3
"""post_tool_call(terminal): verify destructive operations actually completed.

Reviewed-hook lane (see SECURITY.md). Source: claude-code-config's hooks/verify-deleted-guard.py
(see mappings/reviewed-hooks.yaml). "Command exit 0" != "thing is gone" — this hook performs an
after-the-fact existence check based on the command shape (rm, docker rm, kubectl delete, curl
-X DELETE) and logs a verdict.

Audit-log-only, by design and by necessity (verified 2026-08-08 against the live
model_tools.py/agent/shell_hooks.py source): unlike Claude Code's PostToolUse, whose stderr is
surfaced back into the *same* agent turn, Hermes's post_tool_call is a fire-and-forget observer
hook — `_emit_post_tool_call_hook()` in model_tools.py calls `invoke_hook("post_tool_call", ...)`
and discards its return value entirely, so nothing this script prints can reach the model's
context in this turn or the next. This is a real capability gap versus upstream, not a
reimplementation shortcut — recorded in mappings/reviewed-hooks.yaml and revisit-worthy if a
future Hermes version adds a context-injection path for post_tool_call. What still works: a
durable, operator-inspectable verdict in the shared safety log (same mechanism the other 4
reviewed hooks use), matching this operator's own `deletion-confirm-and-verify.md` rule
("after a delete/copy, re-verify it actually happened").

Verdict values logged
======================
  verified-deleted   - target confirmed gone
  still-present      - target still exists (WARN)
  could-not-verify    - recognized destructive intent but no verify strategy
  (non-destructive commands are not logged at all)
"""
from __future__ import annotations

import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import log, read_event, terminal_command  # noqa: E402


def warn(msg: str) -> None:
    sys.stderr.write(f"[verify_deleted] {msg}\n")


def info(msg: str) -> None:
    sys.stderr.write(f"[verify_deleted] {msg}\n")


# =============================================================================
# Per-command verify strategies (unchanged from upstream — harness-agnostic).
# Each takes the command string and returns (verdict, details).
# =============================================================================

def verify_rm(cmd: str) -> tuple[str, str]:
    """For rm/rmdir: each target should not exist anymore."""
    cmd_no_comments = re.sub(r"#[^\n]*", "", cmd)
    try:
        tokens = shlex.split(cmd_no_comments, posix=True)
    except ValueError:
        return "could-not-verify", "shlex parse failed"

    targets: list[str] = []
    rm_seen = False
    for tok in tokens:
        if tok in ("rm", "rmdir") or tok.endswith("/rm") or tok.endswith("/rmdir"):
            rm_seen = True
            continue
        if not rm_seen:
            continue
        if tok.startswith("-"):
            continue
        if tok in (";", "&&", "||", "|", "&"):
            rm_seen = False
            continue
        targets.append(tok)

    if not targets:
        return "could-not-verify", "no targets extracted"

    still_present = []
    for t in targets:
        if any(c in t for c in "*?["):
            continue
        if "$" in t:
            continue
        p = Path(t).expanduser()
        if p.exists():
            still_present.append(str(p))

    if still_present:
        sample = ", ".join(still_present[:3])
        more = f" (+{len(still_present) - 3} more)" if len(still_present) > 3 else ""
        return "still-present", f"{sample}{more}"
    return "verified-deleted", f"{len(targets)} target(s) gone"


def verify_docker_rm(cmd: str) -> tuple[str, str]:
    """docker rm <container> - check `docker ps -a` doesn't list it."""
    if not shutil.which("docker"):
        return "could-not-verify", "docker not in PATH"
    m = re.search(r"\bdocker\s+(?:rm|rmi|volume\s+rm|network\s+rm)\s+(?:-[a-zA-Z]+\s+)*(.+?)(?:$|\|)", cmd)
    if not m:
        return "could-not-verify", "could not extract container name"
    raw = m.group(1).strip()
    names = [n for n in raw.split() if not n.startswith("-")]
    if not names:
        return "could-not-verify", "no container names extracted"

    list_cmd = ["docker", "ps", "-a", "--format", "{{.Names}}"]
    if "rmi" in cmd:
        list_cmd = ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"]
    elif "volume rm" in cmd:
        list_cmd = ["docker", "volume", "ls", "--format", "{{.Name}}"]
    elif "network rm" in cmd:
        list_cmd = ["docker", "network", "ls", "--format", "{{.Name}}"]

    try:
        # argv-list form (no shell=True) -- every branch above is a hardcoded arg list, not
        # built from `cmd`'s content, so this changes nothing about behavior, only removes an
        # unnecessary shell layer (this repo's own reviewed-hook policy bans shell=True).
        proc = subprocess.run(list_cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode != 0:
            return "could-not-verify", f"docker list exit {proc.returncode}: {proc.stderr.strip()[:120]}"
        listed = set(line for line in proc.stdout.strip().split("\n") if line)
    except (subprocess.TimeoutExpired, OSError) as e:
        return "could-not-verify", f"list failed: {e}"

    still_present = [n for n in names if n in listed]
    if still_present:
        return "still-present", f"docker resources still listed: {', '.join(still_present)}"
    return "verified-deleted", f"all {len(names)} resource(s) absent from docker"


def verify_kubectl_delete(cmd: str) -> tuple[str, str]:
    """kubectl delete <type> <name> - kubectl get should NotFound."""
    if not shutil.which("kubectl"):
        return "could-not-verify", "kubectl not in PATH"
    m = re.search(r"\bkubectl\s+delete\s+(\w+)\s+(\S+)", cmd)
    if not m:
        return "could-not-verify", "could not parse kubectl delete syntax"
    rtype, rname = m.group(1), m.group(2)
    try:
        proc = subprocess.run(
            ["kubectl", "get", rtype, rname],
            capture_output=True, text=True, timeout=10,
        )
        if proc.returncode != 0 and "NotFound" in (proc.stderr + proc.stdout):
            return "verified-deleted", f"kubectl get {rtype}/{rname} -> NotFound"
        if proc.returncode == 0:
            return "still-present", f"kubectl get {rtype}/{rname} still returns the resource"
        return "could-not-verify", f"kubectl get exit {proc.returncode}"
    except (subprocess.TimeoutExpired, OSError) as e:
        return "could-not-verify", f"kubectl get failed: {e}"


def verify_curl_delete(cmd: str) -> tuple[str, str]:
    """curl -X DELETE <url> - GET <url> should be 404 or similar."""
    if not shutil.which("curl"):
        return "could-not-verify", "curl not in PATH"
    m = re.search(r"https?://[^\s\"';|]+", cmd)
    if not m:
        return "could-not-verify", "no URL extracted"
    url = m.group(0)
    if not url.startswith("https://"):
        return "could-not-verify", "non-HTTPS URL - skipping verify"
    try:
        proc = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", "10", url],
            capture_output=True, text=True, timeout=15,
        )
        code = proc.stdout.strip()
        if code in ("404", "410", "204"):
            return "verified-deleted", f"GET {url} -> HTTP {code}"
        if code == "200":
            return "still-present", f"GET {url} -> HTTP 200 (resource still served)"
        return "could-not-verify", f"GET {url} -> HTTP {code} (ambiguous)"
    except (subprocess.TimeoutExpired, OSError) as e:
        return "could-not-verify", f"curl GET failed: {e}"


# =============================================================================
# Dispatch - pick verifier based on command shape (unchanged from upstream).
# =============================================================================

DISPATCH = [
    (r"\b(rm|rmdir)\s+", verify_rm),
    (r"\bdocker\s+(rm|rmi|volume\s+rm|network\s+rm)\b", verify_docker_rm),
    (r"\bkubectl\s+delete\s+\w+\s+\S+", verify_kubectl_delete),
    (r"\bcurl\s+[^|]*-X\s+DELETE\b", verify_curl_delete),
]

DESTRUCTIVE_NO_STRATEGY = [
    (r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b", "DB DROP - connect and check `\\dt` manually"),
    (r"\bTRUNCATE\b", "TRUNCATE - connect and SELECT count(*) manually"),
    (r"\bDELETE\s+FROM\s+", "SQL DELETE - connect and SELECT count(*) manually"),
    (r"\baws\s+\w+\s+(delete|terminate|remove)-\w+", "AWS delete - `aws describe` to verify"),
    (r"\bgcloud\s+\w+(\s+\w+)*\s+delete\b", "GCP delete - gcloud describe to verify"),
    (r"\bcloudflared\s+tunnel\s+delete\b", "CF tunnel delete - `cloudflared tunnel list` to verify"),
    (r"\bgit\s+(reset\s+--hard|branch\s+-D|push\s+--force)", "git destructive - git log/branch/reflog"),
    (r"\bsystemctl\s+(stop|disable)\b", "systemctl - verify with systemctl status"),
    (r"\bkill\s+-9\b|\bpkill\s+-9\b|\bkillall\b", "process kill - verify with ps/pgrep"),
    (r"\b(apt|apt-get)\s+(remove|purge)\b", "apt remove - verify with dpkg -l"),
    (r"\bpip\s+uninstall\b", "pip uninstall - verify with pip show"),
    (r"\bnpm\s+(uninstall|rm)\b", "npm uninstall - verify with npm ls"),
]


def main() -> None:
    event = read_event()
    if event.get("tool_name") != "terminal":
        sys.exit(0)
    cmd = terminal_command(event.get("tool_input") or {})
    if not cmd:
        sys.exit(0)

    # Adapted from upstream's `interrupted` check (Claude-Code-specific field, no Hermes
    # equivalent). The closest Hermes analog for "this call never actually ran" is
    # extra.status == "blocked" (another hook blocked it pre-execution) — a non-zero exit
    # (extra.status == "error") deliberately does NOT skip verification, since a partial
    # failure (some targets deleted, some permission-denied) is exactly the scenario this
    # hook exists to catch, not a reason to skip it.
    extra = event.get("extra", {}) or {}
    if extra.get("status") == "blocked":
        sys.exit(0)

    for pattern, fn in DISPATCH:
        if re.search(pattern, cmd, re.IGNORECASE):
            verdict, details = fn(cmd)
            log("INFO" if verdict == "verified-deleted" else "WARN",
                "verify_deleted", verdict, pattern, f"{details} :: {cmd[:200]}")
            if verdict == "still-present":
                warn(f"STILL PRESENT after destructive op: {details}")
                warn(f"   Command: {cmd[:200]}")
                warn("   The agent should NOT report 'deleted' until this is resolved.")
            elif verdict == "verified-deleted":
                info(f"verified deletion: {details}")
            else:
                info(f"could not verify: {details}")
            sys.exit(0)

    for pattern, hint in DESTRUCTIVE_NO_STRATEGY:
        if re.search(pattern, cmd, re.IGNORECASE):
            log("INFO", "verify_deleted", "could-not-verify", pattern, f"{hint} :: {cmd[:200]}")
            info(f"destructive op detected but no auto-verify strategy. {hint}")
            sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
