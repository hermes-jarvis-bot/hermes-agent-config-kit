#!/usr/bin/env python3
"""pre_tool_call: block commands that can cut off the agent itself.

Reviewed-hook lane (see SECURITY.md). Source:
AnastasiyaW/claude-code-config/hooks/self-harm-guard.py, reimplemented for
Hermes Agent's shell-hook contract (see hermes_hook_common.py for the exact
I/O differences from the upstream Claude-Code version this was read from).

Covers:
 - edits to /etc/ssh/sshd_config and AuthorizedKeysFile
 - systemctl restart/stop sshd and sshd daemon kill
 - pkill/killall across Hermes's own runtime (python/node/bun) - harakiri
 - iptables/ufw rules that could drop the agent's own connectivity
 - reboot/shutdown without a handoff

Bypass: HERMES_ALLOW_SELF_HARM=1 or a `# hermes-bypass: self-harm` marker in
the command text.

Never invoked automatically by this adapter. Copied by
scripts/install_hermes.py into <hermes-home>/hooks/config-kit/; the operator
must add a `hooks: pre_tool_call:` entry pointing at it in their own
~/.hermes/config.yaml by hand — see hermes/hooks/README.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hermes_hook_common import (  # noqa: E402
    allow,
    any_match,
    block,
    bypass,
    file_path,
    log,
    read_event,
    terminal_command,
)

SSH_CONFIG_PATHS = [
    r"/etc/ssh/sshd_config",
    r"/etc/ssh/sshd_config\.d/",
    r"~/.ssh/authorized_keys$",
    r"/root/.ssh/authorized_keys$",
]

BASH_PATTERNS = [
    # SSH daemon lifecycle
    r"\bsystemctl\s+(restart|stop|disable|mask)\s+sshd?\b",
    r"\bservice\s+sshd?\s+(restart|stop)\b",
    r"\b/etc/init\.d/sshd?\s+(restart|stop)\b",
    r"\bpkill\s+.*sshd\b",
    r"\bkill(all)?\s+.*sshd\b",

    # Self-harakiri: Hermes Agent runs on a Python venv process, gateway or
    # otherwise; node/bun are kept too since the desktop/web components use
    # them.
    r"\bkillall\s+(node|bun|python|hermes)\b",
    r"\bpkill\s+-f\s+.*(\bhermes\b|hermes_cli|hermes-agent|nousresearch)",
    r"\bpkill\s+.*\b(node|bun)\b(?!.*--parent)",

    # Firewall self-block
    r"\biptables\s+.*-A\s+(INPUT|OUTPUT).*-j\s+DROP(?!.*--sport)",
    r"\bufw\s+(deny|reject)\s+(incoming|outgoing|all)",
    r"\bufw\s+default\s+deny\s+(incoming|outgoing)",

    # sshd_config edits via sed (bypasses the write_file/patch tool)
    r"\bsed\s+-i\s+.*\b(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|Port)\s+.*/etc/ssh/sshd_config",
    r">\s*/etc/ssh/sshd_config",
    r">>\s*/etc/ssh/authorized_keys",  # append alone is not always bad but worth flagging

    # Reboot without handoff. Anchored to command position (line start /
    # after ; & | / sudo) so bare "reboot" and "sudo reboot" are caught
    # while mentions like "grep reboot /var/log/syslog" stay allowed.
    r"(?:^|[;&|]\s*|\bsudo\s+)(shutdown|reboot|halt|poweroff)\b",
]


def main() -> None:
    event = read_event()
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    hit: str | None = None
    target = ""

    if tool_name == "terminal":
        target = terminal_command(tool_input)
        hit = any_match(target, BASH_PATTERNS)
    elif tool_name in {"patch", "write_file"}:
        target = file_path(tool_input)
        hit = any_match(target, SSH_CONFIG_PATHS)

    if not hit:
        allow()

    if bypass("self-harm", target, env_name="HERMES_ALLOW_SELF_HARM"):
        log("WARN", "block_self_harm", "bypass", hit, target)
        allow()

    log("BLOCK", "block_self_harm", "deny", hit, target)
    block(
        f"Self-harm pattern blocked: /{hit}/.\n"
        "These commands can:\n"
        "  - cut off SSH access (sshd edits/restart without a backup connection)\n"
        "  - kill the agent's own runtime (pkill node/bun/python/hermes)\n"
        "  - block its own network connectivity (iptables/ufw default deny)\n"
        "  - reboot the host without a ready handoff\n"
        "If this is intentional:\n"
        "  1) confirm an alternative session or backup path to the host exists\n"
        "  2) confirm the goal with the user\n"
        "  3) run with HERMES_ALLOW_SELF_HARM=1\n"
        "Known incident class: a restarted sshd with no saved key/backup session"
        " leaves nobody able to reconnect."
    )


if __name__ == "__main__":
    main()
