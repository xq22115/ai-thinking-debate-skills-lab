import importlib.util
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts/validate_agent_control_plane.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

EXPECTED_AGENT_NAMES = {
    "A01": "編排代理",
    "A02": "主張代理",
    "A03": "原始來源研究代理",
    "A04": "根因分析代理",
    "A05": "反方代理",
    "A06": "交叉詰問代理",
    "A07": "實作代理",
    "A08": "驗證代理",
    "A09": "風險代理",
    "A10": "裁決代理",
}


class AgentControlPlaneTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS", receipt)
        self.assertIn("two_phase_write_plan_contract", receipt["checks"])
        self.assertIn("isolated_ref_plan_collection", receipt["checks"])
        self.assertIn("write_scope_enforcement_contract", receipt["checks"])
        self.assertIn("preflight_and_scope_enforced_parallelism", receipt["checks"])
        self.assertIn("no_shared_mutable_plan_ledger", receipt["checks"])
        self.assertIn("exact_10_named_agent_roles", receipt["checks"])

    def test_exact_ten_agent_names_match_user_contract(self):
        registry = json.loads(
            (ROOT / "ai-system/control-plane/registry.json").read_text(encoding="utf-8")
        )
        actual = {agent["id"]: agent["name_zh"] for agent in registry["agents"]}
        self.assertEqual(actual, EXPECTED_AGENT_NAMES)

    def test_all_ten_lanes_pass_static_contract(self):
        for i in range(1, 11):
            receipt = validator.validate(ROOT, f"{i:02d}")
            self.assertEqual(receipt["result"], "PASS", receipt)
            self.assertIn(f"lane_{i:02d}_contract", receipt["checks"])

    def test_python_test_artifacts_are_ignored(self):
        probes = [
            "scripts/__pycache__/probe.cpython-314.pyc",
            "tests/__pycache__/probe.pyc",
            ".pytest_cache/v/cache/nodeids",
            ".mypy_cache/3.14/meta.json",
            ".ruff_cache/cache.db",
            "control-contract-receipt.json",
            "control-plane-receipt-01.json",
            "workflow-registry-receipt.json",
            "agent-adjudication.json",
        ]
        for relative in probes:
            cp = subprocess.run(
                ["git", "-C", str(ROOT), "check-ignore", "-q", relative],
                check=False,
            )
            self.assertEqual(cp.returncode, 0, relative)

    def test_registry_is_single_writer(self):
        reg = json.loads((ROOT / "ai-system/control-plane/registry.json").read_text())
        concurrency = reg["concurrency"]
        self.assertFalse(concurrency["same_branch_multiple_writers"])
        self.assertFalse(concurrency["shared_mutable_run_files"])
        self.assertFalse(concurrency["shared_mutable_plan_ledger"])
        self.assertTrue(concurrency["plan_collection_read_only_across_refs"])
        self.assertTrue(concurrency["update_requires_current_blob_sha"])
        self.assertTrue(concurrency["base_sha_pinned"])
        self.assertTrue(concurrency["write_plan_required_before_mutation"])
        self.assertTrue(concurrency["write_set_overlap_requires_dependency"])
        self.assertTrue(concurrency["actual_diff_scope_verification_required_before_fanin"])
        self.assertTrue(concurrency["integration_via_pull_request_only"])

    def test_gate_is_zero_veto_all_pass(self):
        gates = json.loads((ROOT / "ai-system/control-plane/gates.json").read_text())
        self.assertEqual(len(gates["gates"]), 10)
        self.assertEqual(gates["aggregate"]["required_pass_count"], 10)
        self.assertEqual(gates["aggregate"]["veto_tolerance"], 0)
        self.assertEqual(gates["aggregate"]["missing_receipt_tolerance"], 0)

    def test_negative_shared_writer_is_rejected_for_the_intended_reason(self):
        with tempfile.TemporaryDirectory() as td:
            target = pathlib.Path(td)
            shutil.copytree(ROOT / "ai-system", target / "ai-system")
            shutil.copy2(ROOT / ".gitignore", target / ".gitignore")
            (target / "scripts").mkdir()
            (target / "tests").mkdir()
            for source in [
                ROOT / "scripts/collect_write_plans_from_refs.py",
                ROOT / "scripts/check_write_plan_conflicts.py",
                ROOT / "scripts/verify_write_plan_scope.py",
                ROOT / "scripts/verify_snapshot_bound_execution.py",
                ROOT / "scripts/verify_run_freshness.py",
                ROOT / "scripts/adjudicate_agent_receipts.py",
                ROOT / "scripts/local_agent_executor.py",
                ROOT / "scripts/finalize_local_agent_execution.py",
                ROOT / "scripts/prepare_local_agent_run.py",
                ROOT / "scripts/run_local_agent_workflow.py",
                ROOT / "scripts/manage_local_agent_run.py",
            ]:
                shutil.copy2(source, target / "scripts" / source.name)
            for source in [
                ROOT / "tests/test_collect_write_plans_from_refs.py",
                ROOT / "tests/test_write_plan_conflicts.py",
                ROOT / "tests/test_write_plan_scope.py",
                ROOT / "tests/test_snapshot_bound_execution.py",
                ROOT / "tests/test_run_freshness.py",
                ROOT / "tests/test_actor_claims.py",
                ROOT / "tests/test_snapshot_governance_registration.py",
                ROOT / "tests/test_adjudicate_agent_receipts.py",
                ROOT / "tests/test_local_agent_executor.py",
                ROOT / "tests/test_local_executor_registration.py",
                ROOT / "tests/test_finalize_local_agent_execution.py",
                ROOT / "tests/test_prepare_local_agent_run.py",
                ROOT / "tests/test_run_local_agent_workflow.py",
                ROOT / "tests/test_manage_local_agent_run.py",
            ]:
                shutil.copy2(source, target / "tests" / source.name)
            reg_path = target / "ai-system/control-plane/registry.json"
            reg = json.loads(reg_path.read_text(encoding="utf-8"))
            reg["concurrency"]["same_branch_multiple_writers"] = True
            reg_path.write_text(json.dumps(reg), encoding="utf-8")
            receipt = validator.validate(target)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertIn(
                "concurrency_invariant:same_branch_multiple_writers",
                receipt["failures"],
            )
            self.assertFalse(
                any(item.startswith("missing_or_empty:") for item in receipt["failures"]),
                receipt,
            )


if __name__ == "__main__":
    unittest.main()
