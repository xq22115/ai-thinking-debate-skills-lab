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

    def test_request_id_is_bounded_path_safe_and_ref_safe(self):
        bad_ids = ["../bad", "bad.name", "bad_name", "bad..name"]
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            for request_id in bad_ids:
                path = self._write_request(root, request_id=request_id)
                _, failures = gate.validate_request(path)
                self.assertIn("request_id_invalid", failures, request_id)

    def test_five_methods_and_ten_lanes_are_hard_requirements(self):
        config = gate._json_load(gate.CONFIG)
        methods = [item["id"] for item in config["completionMethods"]]
        self.assertEqual(methods, ["M1", "M2", "M3", "M4", "M5"])
        self.assertEqual(gate.LANES, [f"A{i:02d}" for i in range(1, 11)])

    def test_pack_manifest_contains_required_files(self):
        required = gate._required_pack_files()
        missing = [path for path in required if not path.is_file()]
        self.assertEqual(missing, [])

    def test_proof_persistence_is_immutable_and_does_not_move_source_branch(self):
        config = gate._json_load(gate.CONFIG)
        relay = config["relay"]
        self.assertEqual(relay["proofPersistence"], "immutable_tag")
        self.assertEqual(relay["proofRefPrefix"], "refs/tags/ordinary-chat-proof/")
        self.assertFalse(relay["sourceBranchMutation"])
        self.assertFalse(relay["proofRefOverwriteAllowed"])
        self.assertTrue(relay["proofCommitMustHaveSourceShaAsParent"])

        workflow = gate.WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('proof_ref="refs/tags/ordinary-chat-proof/$request_id"', workflow)
        self.assertIn('git ls-remote --exit-code --tags origin "$proof_ref"', workflow)
        self.assertIn('git push origin "$proof_ref"', workflow)
        self.assertIn('test "$(git rev-parse HEAD^)" = "$GITHUB_SHA"', workflow)
        self.assertNotIn("git push origin HEAD:ordinary-chat-agent-stack-v4-immediate-use", workflow)
        self.assertNotIn("git push --force", workflow)
        self.assertNotIn("git push -f", workflow)

    def test_proof_persistence_runs_only_after_successful_aggregate(self):
        workflow = gate.WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("if: steps.aggregate.outcome == 'success' && github.event_name == 'push'", workflow)


if __name__ == "__main__":
    unittest.main()
