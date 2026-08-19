import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts/validate_agent_control_plane.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

NEW_CONTROL_PATHS = [
    "ai-system/control-plane/claim.schema.json",
    "scripts/verify_snapshot_bound_execution.py",
    "tests/test_snapshot_bound_execution.py",
    "scripts/verify_run_freshness.py",
    "tests/test_run_freshness.py",
    "tests/test_actor_claims.py",
]


class SnapshotGovernanceRegistrationTests(unittest.TestCase):
    def test_static_validator_exposes_all_new_hard_gates(self):
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS", receipt)
        for check in [
            "actor_ownership_claim_contract",
            "immutable_plan_snapshot_contract",
            "snapshot_bound_execution_contract",
            "per_run_integration_branch",
            "run_base_freshness_contract",
        ]:
            self.assertIn(check, receipt["checks"], receipt)

    def test_receipt_claim_binding_is_a_registered_hard_contract(self):
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS", receipt)
        self.assertIn("receipt_claim_binding_contract", receipt["checks"], receipt)
        policy = (ROOT / ".github/agent-core-policy.yml").read_text()
        self.assertIn("receipt_claim_binding: required", policy)
        self.assertIn("receipt_work_head_semantics: pre-receipt-task-head", policy)
        self.assertIn("receipt_commit_directly_follows_work_head: true", policy)
        runbook = (ROOT / "ai-system/control-plane/RUNBOOK.md").read_text()
        self.assertIn("receipt-only evidence commit", runbook)
        self.assertIn("`head_sha` = work head", runbook)


    def test_required_check_manifest_covers_new_control_paths(self):
        text = (ROOT / ".github/required-checks.yml").read_text()
        for path in NEW_CONTROL_PATHS:
            self.assertIn(path, text, path)

    def test_agent_core_policy_covers_new_control_paths_and_contracts(self):
        text = (ROOT / ".github/agent-core-policy.yml").read_text()
        for path in NEW_CONTROL_PATHS:
            self.assertIn(path, text, path)
        for marker in [
            "claim_schema: ai-system/control-plane/claim.schema.json",
            "snapshot_execution_verifier: scripts/verify_snapshot_bound_execution.py",
            "run_freshness_verifier: scripts/verify_run_freshness.py",
            "integration_branch_scope: per-run",
        ]:
            self.assertIn(marker, text, marker)

    def test_codeowners_protects_new_executable_controls(self):
        text = (ROOT / ".github/CODEOWNERS").read_text()
        for path in NEW_CONTROL_PATHS[1:]:
            self.assertIn(f"/{path} @xq22115-pixel", text, path)

    def test_ten_gate_workflow_triggers_and_executes_new_tests(self):
        text = (ROOT / ".github/workflows/agent-control-plane-10-gate.yml").read_text()
        for path in NEW_CONTROL_PATHS[1:]:
            self.assertIn(path, text, path)
        for module in [
            "tests.test_actor_claims",
            "tests.test_snapshot_bound_execution",
            "tests.test_run_freshness",
        ]:
            self.assertIn(module, text, module)

    def test_runbook_documents_claim_snapshot_and_freshness_sequence(self):
        text = (ROOT / "ai-system/control-plane/RUNBOOK.md").read_text()
        for marker in [
            "claim.schema.json",
            "plan_head_sha",
            "verify_snapshot_bound_execution.py",
            "verify_run_freshness.py",
            "task/<issue>/<run_id>/integration",
        ]:
            self.assertIn(marker, text, marker)

    def test_root_contract_documents_snapshot_bound_execution(self):
        text = (ROOT / "AGENTS.md").read_text()
        self.assertIn("ownership claim", text.lower())
        self.assertIn("snapshot-bound", text.lower())
        self.assertIn("new `run_id`", text)


if __name__ == "__main__":
    unittest.main()
