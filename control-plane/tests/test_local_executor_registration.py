import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts/validate_agent_control_plane.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class LocalExecutorRegistrationTests(unittest.TestCase):
    def test_static_validator_registers_local_executor_contract(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["result"], "PASS", result)
        self.assertIn("local_independent_executor_contract", result["checks"])

    def test_static_validator_registers_dependency_aware_orchestrator(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["result"], "PASS", result)
        self.assertIn("local_dependency_orchestrator_contract", result["checks"])

    def test_static_validator_registers_local_run_preparer_contract(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["result"], "PASS", result)
        self.assertIn("local_run_preparer_contract", result["checks"])
        self.assertIn("readonly_empty_write_set_contract", result["checks"])

    def test_static_validator_registers_trusted_finalizer_contract(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["result"], "PASS", result)
        self.assertIn("trusted_local_finalizer_contract", result["checks"])

    def test_static_validator_registers_durable_runtime_attestation_contract(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["result"], "PASS", result)
        self.assertIn("durable_runtime_attestation_contract", result["checks"])

    def test_static_validator_registers_run_lifecycle_manager_contract(self):
        result = validator.validate(ROOT)
        self.assertEqual(result["result"], "PASS", result)
        self.assertIn("run_lifecycle_manager_contract", result["checks"])

    def test_registry_declares_fail_closed_executor_invariants(self):
        reg = json.loads((ROOT / "ai-system/control-plane/registry.json").read_text())
        local = reg["local_executor"]
        expected = {
            "driver": "scripts/local_agent_executor.py",
            "required_actor_count": 10,
            "authentication_required_before_launch": True,
            "unauthenticated_action": "BLOCKED_ZERO_PROCESSES",
            "process_ids_recorded": True,
            "distinct_process_instances_required": True,
            "pid_reuse_does_not_invalidate_sequential_independence": True,
            "dependency_aware_orchestrator_required": True,
            "direct_full_run_completion_eligible": False,
            "distinct_execution_ids_required": True,
            "distinct_backend_session_ids_required": True,
            "distinct_workspaces_required": True,
            "model_self_asserted_independence_accepted": False,
            "bash_allowed_by_default": False,
            "readonly_allowed_tools": ["Read", "Glob", "Grep"],
            "write_role_allowed_tools": ["Read", "Glob", "Grep", "Edit", "Write"],
            "claim_bound_assignment_required": True,
            "predeclared_execution_id_required": True,
            "finalizer": "scripts/finalize_local_agent_execution.py",
            "receipt_materialization": "claim-bound-v2",
        }
        preparer = reg["local_run_preparer"]
        self.assertEqual(preparer["driver"], "scripts/prepare_local_agent_run.py")
        self.assertEqual(preparer["required_actor_count"], 10)
        self.assertTrue(preparer["claim_before_plan"])
        self.assertTrue(preparer["readonly_empty_write_set_required"])
        self.assertFalse(preparer["remote_push_performed"])
        self.assertEqual(preparer["write_role"], "A07")
        self.assertEqual(preparer["dependencies"]["A08"], ["A01", "A07"])
        self.assertEqual(preparer["dependencies"]["A10"], ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09"])
        attestation = reg["runtime_attestation"]
        self.assertTrue(attestation["durable_receipt_attestation_required"])
        self.assertFalse(attestation["raw_backend_session_persisted"])
        self.assertTrue(attestation["distinct_process_instances_required"])
        self.assertTrue(attestation["distinct_backend_session_hashes_required"])
        self.assertEqual(attestation["backend_session_storage"], "sha256-only")
        lifecycle = reg["run_lifecycle_manager"]
        self.assertEqual(lifecycle["driver"], "scripts/manage_local_agent_run.py")
        self.assertEqual(lifecycle["commands"], ["status", "publish", "integrate", "publish-integration", "recover", "rehydrate", "resume", "cleanup"])
        self.assertTrue(lifecycle["status_supported"])
        self.assertTrue(lifecycle["actor_publish_fast_forward_only"])
        self.assertTrue(lifecycle["actor_publish_atomic_multi_ref"])
        self.assertTrue(lifecycle["actor_publish_preflight_all_refs_before_push"])
        self.assertTrue(lifecycle["integration_requires_workflow_pass"])
        self.assertTrue(lifecycle["integration_re_adjudication_required"])
        self.assertTrue(lifecycle["integration_task_diff_must_equal_verified_A07_diff"])
        self.assertTrue(lifecycle["cleanup_dirty_worktree_veto_without_force"])
        self.assertFalse(lifecycle["remote_force_push_allowed"])
        self.assertTrue(lifecycle["integration_publish_fast_forward_only"])
        self.assertTrue(lifecycle["integration_publish_idempotent"])
        self.assertTrue(lifecycle["rehydrate_supported"])
        self.assertFalse(lifecycle["rehydrate_remote_mutation_performed"])
        self.assertTrue(lifecycle["resume_supported"])
        self.assertTrue(lifecycle["resume_only_missing_actors"])
        self.assertTrue(lifecycle["resume_revalidates_snapshot_and_attestation"])
        self.assertTrue(lifecycle["resume_existing_veto_terminal"])
        self.assertTrue(lifecycle["resume_provider_required_only_for_missing_actors"])
        self.assertTrue(lifecycle["git_only_recovery_supported"])
        self.assertFalse(lifecycle["recovery_requires_coordination_files"])
        self.assertTrue(lifecycle["recovery_requires_ten_actor_branches"])
        self.assertTrue(lifecycle["recovery_reconstructs_plan_head_from_git_history"])
        self.assertTrue(lifecycle["recovery_recomputes_snapshot_hashes"])
        self.assertTrue(lifecycle["recovery_rechecks_plan_preflight"])
        self.assertTrue(lifecycle["recovery_requires_fresh_base"])
        self.assertFalse(lifecycle["recovery_remote_mutation_performed"])
        self.assertTrue(lifecycle["recovery_requires_single_claim_path_commit"])
        self.assertTrue(lifecycle["recovery_requires_single_plan_path_commit"])
        self.assertTrue(lifecycle["recovery_claim_commit_must_precede_plan_commit"])
        self.assertTrue(lifecycle["status_receipts_read_from_git_head"])
        self.assertTrue(lifecycle["status_revalidates_snapshots_without_workflow"])
        self.assertTrue(lifecycle["status_runs_adjudication_without_workflow"])
        self.assertTrue(lifecycle["status_requires_fresh_base_for_finalized_pass"])
        orchestrator = reg["local_workflow_orchestrator"]
        self.assertEqual(orchestrator["driver"], "scripts/run_local_agent_workflow.py")
        self.assertTrue(orchestrator["dependency_aware"])
        self.assertTrue(orchestrator["stop_downstream_on_nonpass"])
        self.assertTrue(orchestrator["readonly_dependency_workspaces_via_add_dir"])
        self.assertTrue(orchestrator["A07_external_dependency_dirs_forbidden"])
        self.assertTrue(orchestrator["trusted_finalizer_required_per_actor"])
        self.assertTrue(orchestrator["deterministic_adjudication_required"])
        self.assertTrue(orchestrator["base_freshness_required"])
        self.assertTrue(orchestrator["resume_existing_receipts_supported"])
        self.assertTrue(orchestrator["resume_only_missing_actors"])
        self.assertTrue(orchestrator["resume_revalidation_required"])
        self.assertTrue(orchestrator["existing_veto_receipt_terminal"])
        for key, value in expected.items():
            self.assertEqual(local.get(key), value, key)

    def test_workflow_and_manifest_cover_executor(self):
        workflow = (ROOT / ".github/workflows/agent-control-plane-10-gate.yml").read_text()
        manifest = (ROOT / ".github/required-checks.yml").read_text()
        for path in [
            ".gitignore",
            "scripts/local_agent_executor.py",
            "tests/test_local_agent_executor.py",
            "tests/test_local_executor_registration.py",
            "scripts/finalize_local_agent_execution.py",
            "tests/test_finalize_local_agent_execution.py",
            "scripts/prepare_local_agent_run.py",
            "tests/test_prepare_local_agent_run.py",
            "scripts/run_local_agent_workflow.py",
            "tests/test_run_local_agent_workflow.py",
            "scripts/manage_local_agent_run.py",
            "tests/test_manage_local_agent_run.py",
        ]:
            self.assertIn(path, workflow, path)
            self.assertIn(path, manifest, path)
        self.assertIn("tests.test_local_agent_executor", workflow)
        self.assertIn("tests.test_local_executor_registration", workflow)
        self.assertIn("tests.test_finalize_local_agent_execution", workflow)
        self.assertIn("tests.test_prepare_local_agent_run", workflow)
        self.assertIn("tests.test_run_local_agent_workflow", workflow)
        self.assertIn("tests.test_manage_local_agent_run", workflow)

    def test_policy_required_files_cover_full_local_runtime_supply_chain(self):
        policy = (ROOT / ".github/agent-core-policy.yml").read_text()
        required_section = policy.split("required_files:", 1)[1]
        for path in [
            "scripts/local_agent_executor.py",
            "tests/test_local_agent_executor.py",
            "scripts/finalize_local_agent_execution.py",
            "tests/test_finalize_local_agent_execution.py",
            "scripts/prepare_local_agent_run.py",
            "tests/test_prepare_local_agent_run.py",
            "scripts/run_local_agent_workflow.py",
            "tests/test_run_local_agent_workflow.py",
            "scripts/manage_local_agent_run.py",
            "tests/test_manage_local_agent_run.py",
            "tests/test_local_executor_registration.py",
        ]:
            self.assertIn(f"- {path}", required_section, path)

    def test_policy_codeowners_and_docs_register_executor(self):
        policy = (ROOT / ".github/agent-core-policy.yml").read_text()
        owners = (ROOT / ".github/CODEOWNERS").read_text()
        readme = (ROOT / "ai-system/control-plane/README.md").read_text()
        runbook = (ROOT / "ai-system/control-plane/RUNBOOK.md").read_text()
        agents = (ROOT / "AGENTS.md").read_text()
        self.assertIn(".gitignore", policy)
        self.assertIn("/.gitignore @xq22115-pixel", owners)
        self.assertIn("scripts/local_agent_executor.py", policy)
        self.assertIn("scripts/finalize_local_agent_execution.py", policy)
        self.assertIn("scripts/prepare_local_agent_run.py", policy)
        self.assertIn("scripts/run_local_agent_workflow.py", policy)
        self.assertIn("scripts/manage_local_agent_run.py", policy)
        for marker in [
            "lifecycle_status_receipts_read_from_git_head: true",
            "lifecycle_status_revalidates_snapshots_without_workflow: true",
            "lifecycle_resume_provider_required_only_for_missing_actors: true",
            "lifecycle_recovery_requires_single_claim_path_commit: true",
            "lifecycle_recovery_requires_single_plan_path_commit: true",
            "receipt_commit_directly_follows_work_head: true",
        ]:
            self.assertIn(marker, policy, marker)
        self.assertIn("/scripts/local_agent_executor.py @xq22115-pixel", owners)
        self.assertIn("/scripts/finalize_local_agent_execution.py @xq22115-pixel", owners)
        self.assertIn("/scripts/prepare_local_agent_run.py @xq22115-pixel", owners)
        self.assertIn("/scripts/run_local_agent_workflow.py @xq22115-pixel", owners)
        self.assertIn("/scripts/manage_local_agent_run.py @xq22115-pixel", owners)
        for marker in [
            "local_agent_executor.py",
            "process instance",
            "session",
            "BLOCKED",
        ]:
            self.assertIn(marker.lower(), readme.lower())
            self.assertIn(marker.lower(), runbook.lower())
        self.assertIn("local_agent_executor.py", agents)
        self.assertIn("finalize_local_agent_execution.py", agents)
        self.assertIn("prepare_local_agent_run.py", agents)
        self.assertIn("run_local_agent_workflow.py", agents)
        self.assertIn("manage_local_agent_run.py", agents)
        self.assertIn("positive allowlist", readme.lower())
        self.assertIn("bash", readme.lower())
        self.assertIn("positive allowlist", runbook.lower())
        self.assertIn("runtime attestation", readme.lower())
        self.assertIn("runtime attestation", runbook.lower())
        self.assertIn("status / publish / integrate / publish-integration / recover / rehydrate / resume / cleanup", readme.lower())
        self.assertIn("status / publish / integrate / publish-integration / recover / rehydrate / resume / cleanup", runbook.lower())


if __name__ == "__main__":
    unittest.main()
