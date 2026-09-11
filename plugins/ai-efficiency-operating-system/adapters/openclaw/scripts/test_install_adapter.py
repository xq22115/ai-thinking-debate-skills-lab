#!/usr/bin/env python3
"""Behavioral unit tests for additive/non-regressive OpenClaw config mutation helpers."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().with_name("install_adapter.py")
spec = importlib.util.spec_from_file_location("openclaw_install_adapter", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import install_adapter.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerAdditivityTests(unittest.TestCase):
    def test_inventory_includes_lobster_without_forcing_swarm_in_production(self) -> None:
        self.assertEqual(len(installer.ADAPTER_SKILLS), 5)
        self.assertIn("openclaw-lobster-workflows", installer.ADAPTER_SKILLS)
        self.assertIn("lobster", installer.PRODUCTION_TOOLS)
        self.assertNotIn("agents_wait", installer.PRODUCTION_TOOLS)
        self.assertIn("agents_wait", installer.LAB_TOOLS)

    def test_append_unique_preserves_existing_order_and_only_adds_missing(self) -> None:
        with patch.object(installer, "get_json", return_value=(True, ["existing-a", "existing-b"])), patch.object(
            installer, "set_value", return_value="SET"
        ) as setter:
            installer.append_unique("tools.alsoAllow", ["existing-b", "lobster"], dry_run=False)
            setter.assert_called_once_with(
                "tools.alsoAllow", ["existing-a", "existing-b", "lobster"], dry_run=False
            )

    def test_append_unique_initializes_absent_array_without_deleting_requested_values(self) -> None:
        with patch.object(installer, "get_json", return_value=(False, None)), patch.object(
            installer, "set_value", return_value="SET"
        ) as setter:
            installer.append_unique("skills.load.extraDirs", ["/adapter/skills"], dry_run=False)
            setter.assert_called_once_with(
                "skills.load.extraDirs", ["/adapter/skills"], dry_run=False
            )

    def test_absolute_tool_allowlist_is_extended_in_place(self) -> None:
        with patch.object(installer, "get_json", return_value=(True, ["read", "write"])), patch.object(
            installer, "append_unique", return_value="SET"
        ) as append:
            installer.ensure_tools_allowed("tools", ["lobster", "subagents"], dry_run=False)
            append.assert_called_once_with(
                "tools.allow", ["lobster", "subagents"], dry_run=False
            )

    def test_profile_scope_without_absolute_allowlist_uses_also_allow(self) -> None:
        with patch.object(installer, "get_json", return_value=(False, None)), patch.object(
            installer, "append_unique", return_value="SET"
        ) as append:
            installer.ensure_tools_allowed(
                "agents.entries.main.tools", ["lobster", "subagents"], dry_run=False
            )
            append.assert_called_once_with(
                "agents.entries.main.tools.alsoAllow", ["lobster", "subagents"], dry_run=False
            )

    def test_numeric_floor_never_lowers_higher_existing_value(self) -> None:
        with patch.object(installer, "get_json", return_value=(True, 32)), patch.object(
            installer, "set_value", return_value="SET"
        ) as setter:
            installer.numeric_floor("agents.defaults.subagents.maxConcurrent", 8, dry_run=False)
            setter.assert_called_once_with(
                "agents.defaults.subagents.maxConcurrent", 32, dry_run=False
            )

    def test_numeric_floor_raises_lower_existing_value(self) -> None:
        with patch.object(installer, "get_json", return_value=(True, 2)), patch.object(
            installer, "set_value", return_value="SET"
        ) as setter:
            installer.numeric_floor("agents.defaults.subagents.maxConcurrent", 8, dry_run=False)
            setter.assert_called_once_with(
                "agents.defaults.subagents.maxConcurrent", 8, dry_run=False
            )

    def test_set_value_existing_path_uses_conditional_current_value(self) -> None:
        with patch.object(installer, "get_json", return_value=(True, {"old": 1})), patch.object(
            installer, "openclaw"
        ) as cli:
            installer.set_value("example.path", {"new": 2}, dry_run=False)
            args = cli.call_args.args
            self.assertEqual(args[:3], ("config", "set", "example.path"))
            self.assertIn("--strict-json", args)
            self.assertIn("--expect-current-json", args)
            self.assertNotIn("--expect-current-absent", args)

    def test_set_value_absent_path_uses_absence_guard(self) -> None:
        with patch.object(installer, "get_json", return_value=(False, None)), patch.object(
            installer, "openclaw"
        ) as cli:
            installer.set_value("example.path", True, dry_run=False)
            args = cli.call_args.args
            self.assertIn("--expect-current-absent", args)
            self.assertNotIn("--expect-current-json", args)

    def test_dry_run_never_uses_write_expectation_flags(self) -> None:
        with patch.object(installer, "get_json", return_value=(True, 1)), patch.object(
            installer, "openclaw"
        ) as cli:
            installer.set_value("example.path", 2, dry_run=True)
            args = cli.call_args.args
            self.assertIn("--dry-run", args)
            self.assertNotIn("--expect-current-json", args)
            self.assertNotIn("--expect-current-absent", args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
