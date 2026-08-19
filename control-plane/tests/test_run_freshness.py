import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "freshness", ROOT / "scripts/verify_run_freshness.py"
)
freshness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(freshness)

SHA_A = "a" * 40
SHA_B = "b" * 40


class RunFreshnessTests(unittest.TestCase):
    def test_integration_branch_namespace_is_per_run(self):
        reg = json.loads(
            (ROOT / "ai-system/control-plane/registry.json").read_text()
        )
        self.assertEqual(
            reg["namespace"]["integration_branch_template"],
            "task/{issue_number}/{run_id}/integration",
        )

    def test_equal_pinned_and_current_base_passes(self):
        result = freshness.verify_freshness(SHA_A, SHA_A)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["failures"], [])

    def test_stale_base_is_veto(self):
        result = freshness.verify_freshness(SHA_A, SHA_B)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("base_head_drift", result["failures"])

    def test_invalid_sha_is_veto(self):
        result = freshness.verify_freshness("not-a-sha", SHA_A)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("invalid_pinned_base_sha", result["failures"])

    def test_run_contract_requires_claims_and_plan_snapshots(self):
        schema = json.loads(
            (ROOT / "ai-system/control-plane/run-contract.schema.json").read_text()
        )
        required = set(schema["required"])
        self.assertIn("claims", required)
        self.assertIn("plan_snapshots", required)

    def test_state_machine_forbids_stale_base_and_snapshot_replay(self):
        state = json.loads(
            (ROOT / "ai-system/control-plane/state-machine.json").read_text()
        )
        forbidden = set(state["forbidden_shortcuts"])
        self.assertIn("stale_base -> merge", forbidden)
        self.assertIn("old_snapshot -> current_run_PASS", forbidden)
        self.assertIn("force_push -> ownership_transfer", forbidden)


if __name__ == "__main__":
    unittest.main()
