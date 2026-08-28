from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "control-plane/scripts/validate_cross_runtime_research_contract.py"
PROFILE_PATH = REPO_ROOT / "control-plane/ai-system/configs/continuous-thinking-global.json"
CODEX_INSTALLER = REPO_ROOT / "control-plane/scripts/install_codex_global_quality.py"
SETTINGS_PATH = REPO_ROOT / ".claude/settings.json"
STOP_HOOK = REPO_ROOT / ".claude/hooks/enforce-a03-research-cycle.py"
WORKFLOW = REPO_ROOT / "control-plane/scripts/run_quality_bound_workflow.py"
A03_ROLE = REPO_ROOT / "control-plane/ai-system/control-plane/agents/A03-source-research.md"

spec = importlib.util.spec_from_file_location("cross_runtime_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def _real_values():
    return (
        json.loads(PROFILE_PATH.read_text(encoding="utf-8")),
        CODEX_INSTALLER.read_text(encoding="utf-8"),
        json.loads(SETTINGS_PATH.read_text(encoding="utf-8")),
        STOP_HOOK.read_text(encoding="utf-8"),
        WORKFLOW.read_text(encoding="utf-8"),
        A03_ROLE.read_text(encoding="utf-8"),
    )


class CrossRuntimeResearchContractTests(unittest.TestCase):
    def test_real_cross_runtime_contract_passes(self) -> None:
        self.assertEqual(validator.validate(), [])

    def test_missing_canonical_adaptive_saturation_fails_closed(self) -> None:
        profile, codex, settings, stop, workflow, role = _real_values()
        profile = copy.deepcopy(profile)
        profile["research_and_experience"].pop("adaptive_saturation", None)
        failures = validator.validate_values(profile, codex, settings, stop, workflow, role)
        self.assertIn("canonical_adaptive_saturation_not_required", failures)
        self.assertIn("canonical_falsification_structure_not_four_stage", failures)

    def test_codex_one_pass_research_policy_is_rejected(self) -> None:
        profile, _, settings, stop, workflow, role = _real_values()
        old_codex_policy = '''POLICY_VERSION = "old"\nperform research when useful\nNever simulate deep thinking with sleep.'''
        failures = validator.validate_values(
            profile, old_codex_policy, settings, stop, workflow, role
        )
        self.assertTrue(any(item.startswith("codex_contract_missing:") for item in failures))

    def test_codex_policy_must_remain_runtime_neutral(self) -> None:
        profile, codex, settings, stop, workflow, role = _real_values()
        failures = validator.validate_values(
            profile, codex + "\nUse WebSearch and WebFetch.\n", settings, stop, workflow, role
        )
        self.assertIn("codex_runtime_neutral_policy_leaks_claude_tool_names", failures)

    def test_detached_claude_stop_hook_fails_closed(self) -> None:
        profile, codex, settings, stop, workflow, role = _real_values()
        settings = copy.deepcopy(settings)
        settings["hooks"].pop("Stop", None)
        failures = validator.validate_values(profile, codex, settings, stop, workflow, role)
        self.assertIn("claude_stop_hook_not_registered", failures)

    def test_release_revalidation_cannot_be_removed(self) -> None:
        profile, codex, settings, stop, workflow, role = _real_values()
        workflow = workflow.replace("_research_cycle_state", "_removed_cycle_state")
        failures = validator.validate_values(profile, codex, settings, stop, workflow, role)
        self.assertIn("release_cycle_revalidation_function_missing", failures)


if __name__ == "__main__":
    unittest.main()
