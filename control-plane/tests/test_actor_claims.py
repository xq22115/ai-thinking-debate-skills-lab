import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts/validate_agent_control_plane.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ActorClaimTests(unittest.TestCase):
    def test_claim_contract_is_registered_as_hard_gate(self):
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS", receipt)
        self.assertIn("actor_ownership_claim_contract", receipt["checks"])

    def test_claim_schema_binds_actor_and_execution_identity(self):
        schema = json.loads(
            (ROOT / "ai-system/control-plane/claim.schema.json").read_text()
        )
        required = set(schema["required"])
        expected = {
            "schema_version", "issue_number", "run_id", "actor_id", "branch",
            "base_sha", "claim_id", "executor_id", "execution_id", "status",
        }
        self.assertTrue(expected.issubset(required), required)
        self.assertEqual(schema["properties"]["status"], {"const": "CLAIMED"})

    def test_claim_policy_forbids_takeover_and_force_push(self):
        reg = json.loads(
            (ROOT / "ai-system/control-plane/registry.json").read_text()
        )
        ownership = reg["ownership"]
        self.assertEqual(ownership["claim_mode"], "create-only")
        self.assertFalse(ownership["automatic_takeover"])
        self.assertFalse(ownership["force_push_allowed"])
        self.assertEqual(ownership["recovery"], "new-run-id")

    def test_negative_claim_takeover_policy_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            target = pathlib.Path(td)
            shutil.copytree(ROOT / "ai-system", target / "ai-system")
            shutil.copy2(ROOT / ".gitignore", target / ".gitignore")
            shutil.copytree(ROOT / "scripts", target / "scripts")
            shutil.copytree(ROOT / "tests", target / "tests")
            reg_path = target / "ai-system/control-plane/registry.json"
            reg = json.loads(reg_path.read_text(encoding="utf-8"))
            reg["ownership"]["automatic_takeover"] = True
            reg_path.write_text(json.dumps(reg), encoding="utf-8")
            receipt = validator.validate(target)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertIn("ownership_contract:automatic_takeover", receipt["failures"])
            self.assertFalse(
                any(item.startswith("missing_or_empty:") for item in receipt["failures"]),
                receipt,
            )


if __name__ == "__main__":
    unittest.main()
