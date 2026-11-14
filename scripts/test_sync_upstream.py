#!/usr/bin/env python3
"""Regression tests for upstream-to-Hermes text adaptation."""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import sync_upstream  # noqa: E402


class RelocationPathAdaptationTests(unittest.TestCase):
    SOURCE = "rules/deletion-confirm-and-verify.md"

    def adapt(self, source: str) -> str:
        return sync_upstream.adapt_source_text(self.SOURCE, source)

    def test_relocation_command_does_not_emit_upstream_runtime_path(self) -> None:
        source = (
            "Run `python ~/.claude/claude-code-config/scripts/relocate_from_list.py "
            "relocations.txt --show`, then run `... relocate_from_list.py relocations.txt "
            "--sha abc123`."
        )

        adapted = self.adapt(source)

        self.assertNotIn("claude-code-config/scripts/", adapted)
        self.assertNotIn("~/.claude/", adapted)
        self.assertIn("the Hermes-approved relocation safety tool relocations.txt --show", adapted)
        self.assertIn("the Hermes-approved relocation safety tool relocations.txt --sha abc123", adapted)

    def test_relocation_regression_test_reference_is_neutralised(self) -> None:
        source = "Regression test: `hooks/tests/test_relocate_list.py`."

        adapted = self.adapt(source)

        self.assertNotIn("test_relocate_list.py", adapted)
        self.assertIn("the corresponding Hermes relocation regression test", adapted)


if __name__ == "__main__":
    unittest.main()
