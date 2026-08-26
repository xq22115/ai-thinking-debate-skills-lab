import importlib.util
import json
import pathlib
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "ordinary_chat_completion_gate.py"
spec = importlib.util.spec_from_file_location("ordinary_chat_completion_gate", MODULE_PATH)
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class OrdinaryChatCompletionGateTests(unittest.TestCase):
    def _write_request(self, root: pathlib.Path, **overrides):
        payload = {
            "schemaVersion": 1,
            "request_id": "prove-ready-test",
            "goal": "Prove that the ordinary-chat GitHub relay is immediately usable.",
            "intent": "ordinary_chat_immediate_use",
            "mode": "prove-ready",
            "requested_completion_methods": ["M1", "M2", "M3", "M4", "M5"],
        }
        payload.update(overrides)
        path = root / "request.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_valid_request_passes_contract_validation(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_request(pathlib.Path(temp))
            request, failures = gate.validate_request(path)
            self.assertEqual(failures, [])
            self.assertEqual(request["intent"], "ordinary_chat_immediate_use")

    def test_arbitrary_command_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_request(pathlib.Path(temp), command="echo nope")
            _, failures = gate.validate_request(path)
            self.assertTrue(any(item.startswith("request_unknown_fields:") for item in failures))

    def test_completion_method_set_must_be_exact(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_request(pathlib.Path(temp), requested_completion_methods=["M1"])
            _, failures = gate.validate_request(path)
            self.assertIn("completion_method_set_invalid", failures)

    def test_request_id_is_bounded_and_path_safe(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_request(pathlib.Path(temp), request_id="../bad")
            _, failures = gate.validate_request(path)
            self.assertIn("request_id_invalid", failures)

    def test_five_methods_and_ten_lanes_are_hard_requirements(self):
        config = gate._json_load(gate.CONFIG)
        methods = [item["id"] for item in config["completionMethods"]]
        self.assertEqual(methods, ["M1", "M2", "M3", "M4", "M5"])
        self.assertEqual(gate.LANES, [f"A{i:02d}" for i in range(1, 11)])

    def test_pack_manifest_contains_required_files(self):
        required = gate._required_pack_files()
        missing = [path for path in required if not path.is_file()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
