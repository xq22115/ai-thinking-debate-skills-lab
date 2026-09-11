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

import validate_chatgpt_github_plugin_bridge as bridge


class ChatGPTGitHubPluginBridgeTests(unittest.TestCase):
    def _mutate_json(self, attr: str, mutate) -> list[str]:
        source = getattr(bridge, attr)
        payload = json.loads(source.read_text(encoding="utf-8"))
        candidate = copy.deepcopy(payload)
        mutate(candidate)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / source.name
            path.write_text(json.dumps(candidate), encoding="utf-8")
            with mock.patch.object(bridge, attr, path):
                return bridge.validate()

    def _mutate_text(self, attr: str, transform) -> list[str]:
        source = getattr(bridge, attr)
        text = source.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / source.name
            path.write_text(transform(text), encoding="utf-8")
            with mock.patch.object(bridge, attr, path):
                return bridge.validate()

    def test_current_bridge_contract_passes(self) -> None:
        self.assertEqual(bridge.validate(), [])

    def test_missing_author_is_fail_closed(self) -> None:
        failures = self._mutate_json("PLUGIN_MANIFEST", lambda payload: payload.pop("author"))
        self.assertIn("plugin_author_name_missing", failures)

    def test_missing_app_binding_is_fail_closed(self) -> None:
        failures = self._mutate_json("PLUGIN_MANIFEST", lambda payload: payload.pop("apps"))
        self.assertIn("plugin_apps_path_invalid", failures)

    def test_wrong_github_connector_is_fail_closed(self) -> None:
        failures = self._mutate_json(
            "APP_MANIFEST",
            lambda payload: payload["apps"]["github"].__setitem__("id", "connector_wrong"),
        )
        self.assertIn("github_connector_id_mismatch", failures)

    def test_nonportable_app_field_is_rejected(self) -> None:
        failures = self._mutate_json(
            "APP_MANIFEST",
            lambda payload: payload["apps"]["github"].__setitem__("required", False),
        )
        self.assertIn("github_app_manifest_nonportable_fields", failures)

    def test_marketplace_authentication_cannot_disappear(self) -> None:
        def mutate(payload: dict) -> None:
            payload["plugins"][0]["policy"].pop("authentication")

        failures = self._mutate_json("MARKETPLACE", mutate)
        self.assertIn("marketplace_authentication_policy_missing", failures)

    def test_ten_way_cannot_reintroduce_duplicate_version_constant(self) -> None:
        def mutate(payload: dict) -> None:
            payload["chatgpt_host_live"]["plugin_version"] = "0.0.0"

        failures = self._mutate_json("TEN_WAY_CONFIG", mutate)
        self.assertIn("ten_way_duplicate_version_constant_present", failures)

    def test_bridge_schema_v2_is_required(self) -> None:
        failures = self._mutate_json(
            "BRIDGE_PROFILE",
            lambda payload: payload.__setitem__("schema_version", 1),
        )
        self.assertIn("bridge_schema_version_invalid", failures)

    def test_bridge_operation_state_cannot_disappear(self) -> None:
        def mutate(payload: dict) -> None:
            payload["operation_state_machine"]["states"].remove("TOOL_SCHEMA_READY")

        failures = self._mutate_json("BRIDGE_PROFILE", mutate)
        self.assertIn("bridge_operation_state_missing:TOOL_SCHEMA_READY", failures)

    def test_bridge_operation_envelope_requires_evidence_delta(self) -> None:
        def mutate(payload: dict) -> None:
            payload["operation_envelope"]["required_fields"].remove("evidence_delta")

        failures = self._mutate_json("BRIDGE_PROFILE", mutate)
        self.assertIn("bridge_operation_envelope_field_missing:evidence_delta", failures)

    def test_bridge_transport_success_cannot_be_task_success(self) -> None:
        failures = self._mutate_json(
            "BRIDGE_PROFILE",
            lambda payload: payload["response_contract"].__setitem__("transport_success_is_not_task_success", False),
        )
        self.assertIn("bridge_response_contract_missing:transport_success_is_not_task_success", failures)

    def test_bridge_readback_cannot_be_disabled(self) -> None:
        failures = self._mutate_json(
            "BRIDGE_PROFILE",
            lambda payload: payload["write_contract"].__setitem__("readback_after_material_write", False),
        )
        self.assertIn("bridge_write_contract_missing:readback_after_material_write", failures)

    def test_live_schema_requirement_cannot_be_disabled(self) -> None:
        failures = self._mutate_json(
            "BRIDGE_PROFILE",
            lambda payload: payload["tool_surface_contract"].__setitem__("invented_or_remembered_unknown_parameters_forbidden", False),
        )
        self.assertIn("bridge_tool_surface_contract_missing:invented_or_remembered_unknown_parameters_forbidden", failures)

    def test_execution_cannot_be_inferred_from_repository_state(self) -> None:
        failures = self._mutate_json(
            "BRIDGE_PROFILE",
            lambda payload: payload["execution_contract"].__setitem__("repository_state_is_not_runtime_execution", False),
        )
        self.assertIn("bridge_execution_contract_missing:repository_state_is_not_runtime_execution", failures)

    def test_recovery_route_for_schema_mismatch_cannot_disappear(self) -> None:
        def mutate(payload: dict) -> None:
            payload["recovery_contract"]["routes"].pop("schema_mismatch")

        failures = self._mutate_json("BRIDGE_PROFILE", mutate)
        self.assertIn("bridge_recovery_route_missing:schema_mismatch", failures)

    def test_completion_gate_requires_observed_execution(self) -> None:
        failures = self._mutate_json(
            "BRIDGE_PROFILE",
            lambda payload: payload["completion_gate"].__setitem__("requested_execution_observed_at_correct_layer", False),
        )
        self.assertIn("bridge_completion_gate_missing:requested_execution_observed_at_correct_layer", failures)

    def test_operation_loop_no_progress_detector_cannot_disappear(self) -> None:
        failures = self._mutate_text(
            "OPERATION_LOOP",
            lambda text: text.replace("## 13. No-progress detector", "## 13. Retry notes"),
        )
        self.assertIn("marker_missing:GITHUB_OPERATION_LOOP.md:No-progress detector", failures)

    def test_host_adapter_registration_cannot_disappear(self) -> None:
        def mutate(payload: dict) -> None:
            payload["adapters"] = [item for item in payload["adapters"] if item.get("name") != "github-pull-runtime"]

        failures = self._mutate_json("HOST_ADAPTERS", mutate)
        self.assertIn("github_host_adapter_registration_invalid", failures)

    def test_runtime_probe_cannot_reintroduce_stale_plugin_version(self) -> None:
        failures = self._mutate_text("RUNTIME_PROBE", lambda text: text + "\nExpected package: `1.2.0`\n")
        self.assertIn("stale_plugin_version_literal:RUNTIME_PROBE.md", failures)


if __name__ == "__main__":
    unittest.main()
