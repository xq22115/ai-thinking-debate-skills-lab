from __future__ import annotations

import copy
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_execution_integrity_global as integrity


class ExecutionIntegrityGlobalProfileTests(unittest.TestCase):
    def _mutated_config_failures(self, mutate) -> list[str]:
        config = json.loads(integrity.CONFIG_PATH.read_text(encoding="utf-8"))
        candidate = copy.deepcopy(config)
        mutate(candidate)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "execution-integrity-global.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            with mock.patch.object(integrity, "CONFIG_PATH", path):
                return integrity.validate()

    def _mutated_text_failures(self, attr: str, transform) -> list[str]:
        source = getattr(integrity, attr)
        text = source.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / source.name
            path.write_text(transform(text), encoding="utf-8")
            with mock.patch.object(integrity, attr, path):
                return integrity.validate()

    def _mutated_manifest_failures(self, mutate) -> list[str]:
        manifest = json.loads(integrity.MANIFEST_PATH.read_text(encoding="utf-8"))
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "global-policy-manifest.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            with mock.patch.object(integrity, "MANIFEST_PATH", path):
                return integrity.validate()

    def test_current_repository_state_passes(self) -> None:
        self.assertEqual(integrity.validate(), [])

    def test_every_system_invariant_is_fail_closed(self) -> None:
        for invariant_id in sorted(integrity.REQUIRED_INVARIANTS):
            with self.subTest(invariant=invariant_id):
                failures = self._mutated_config_failures(
                    lambda config, key=invariant_id: config["system_invariants"].pop(key)
                )
                self.assertIn("system_invariants_incomplete", failures)

    def test_readback_requirement_cannot_be_disabled(self) -> None:
        failures = self._mutated_config_failures(
            lambda config: config["github_write_integrity"].__setitem__("readback_after_each_material_write", False)
        )
        self.assertIn("github_write_readback_after_each_material_write_missing_or_false", failures)

    def test_every_fallback_route_is_required(self) -> None:
        for route in sorted(integrity.REQUIRED_FALLBACKS):
            with self.subTest(route=route):
                failures = self._mutated_config_failures(
                    lambda config, value=route: config["github_source_resolution"]["fallback_routes"].remove(value)
                )
                self.assertIn("github_fallback_routes_incomplete", failures)

    def test_every_version_dimension_is_required(self) -> None:
        for dimension in sorted(integrity.REQUIRED_VERSION_DIMENSIONS):
            with self.subTest(dimension=dimension):
                failures = self._mutated_config_failures(
                    lambda config, value=dimension: config["github_source_resolution"]["required_version_dimensions"].remove(value)
                )
                self.assertIn("github_version_dimensions_incomplete", failures)

    def test_every_skill_activation_layer_is_required(self) -> None:
        for layer in sorted(integrity.REQUIRED_SKILL_LAYERS):
            with self.subTest(layer=layer):
                failures = self._mutated_config_failures(
                    lambda config, value=layer: config["skill_plugin_integrity"]["layers"].remove(value)
                )
                self.assertIn("skill_plugin_layers_incomplete", failures)

    def test_every_adversarial_scenario_family_is_required(self) -> None:
        for scenario in sorted(integrity.REQUIRED_SCENARIOS):
            with self.subTest(scenario=scenario):
                failures = self._mutated_config_failures(
                    lambda config, value=scenario: config["adversarial_scenarios"]["families"].remove(value)
                )
                self.assertIn("adversarial_scenarios_incomplete", failures)

    def test_not_run_cannot_be_silently_promoted_to_pass(self) -> None:
        failures = self._mutated_config_failures(
            lambda config: config["release"].__setitem__("not_run_cannot_be_pass", False)
        )
        self.assertIn("release_not_run_cannot_be_pass_missing_or_false", failures)

    def test_official_docs_cannot_become_execution_proof(self) -> None:
        failures = self._mutated_config_failures(
            lambda config: config["source_triangulation"].__setitem__("official_documentation_alone_is_not_execution_proof", False)
        )
        self.assertIn(
            "source_triangulation_official_documentation_alone_is_not_execution_proof_missing_or_false",
            failures,
        )

    def test_invalid_json_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "execution-integrity-global.json"
            path.write_text("{not-json", encoding="utf-8")
            with mock.patch.object(integrity, "CONFIG_PATH", path):
                failures = integrity.validate()
        self.assertTrue(any(item.startswith("json_invalid:") for item in failures))

    def test_policy_cannot_drop_an_invariant_marker(self) -> None:
        failures = self._mutated_text_failures("POLICY_PATH", lambda text: text.replace("GI-06", "GI-X6"))
        self.assertIn("policy_missing:GI-06", failures)

    def test_workflow_cannot_stop_running_the_validator(self) -> None:
        failures = self._mutated_text_failures(
            "WORKFLOW_PATH",
            lambda text: text.replace("validate_execution_integrity_global.py", "removed_execution_integrity_validator.py"),
        )
        self.assertIn("workflow_missing:validate_execution_integrity_global.py", failures)

    def test_manifest_cannot_drop_the_execution_integrity_policy(self) -> None:
        def mutate(manifest: dict) -> None:
            manifest["canonical_policies"] = [
                item for item in manifest["canonical_policies"] if item.get("id") != "github-execution-integrity"
            ]

        failures = self._mutated_manifest_failures(mutate)
        self.assertIn("manifest_github_execution_policy_missing", failures)

    def test_manifest_cannot_drop_the_machine_validator(self) -> None:
        def mutate(manifest: dict) -> None:
            manifest["entrypoints"] = [
                item for item in manifest["entrypoints"] if item.get("role") != "execution_integrity_machine_validator"
            ]

        failures = self._mutated_manifest_failures(mutate)
        self.assertIn("manifest_execution_integrity_validator_missing", failures)


if __name__ == "__main__":
    unittest.main()
