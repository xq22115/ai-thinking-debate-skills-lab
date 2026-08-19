#!/usr/bin/env python3
"""Dependency-free validator for the GitHub multi-chat / 10-agent control plane."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

EXPECTED_AGENT_IDS = [f"A{i:02d}" for i in range(1, 11)]
EXPECTED_GATE_IDS = [f"G{i:02d}" for i in range(1, 11)]
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


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: pathlib.Path, lane: str | None = None):
    failures: list[str] = []
    checks: list[str] = []
    cp = root / "ai-system/control-plane"
    reg_path = cp / "registry.json"
    gate_path = cp / "gates.json"
    required_files = [
        root / ".gitignore",
        reg_path,
        gate_path,
        cp / "task-contract.schema.json",
        cp / "run-contract.schema.json",
        cp / "receipt.schema.json",
        cp / "write-plan.schema.json",
        cp / "claim.schema.json",
        cp / "state-machine.json",
        cp / "README.md",
        cp / "RUNBOOK.md",
        root / "scripts/collect_write_plans_from_refs.py",
        root / "scripts/check_write_plan_conflicts.py",
        root / "scripts/verify_write_plan_scope.py",
        root / "scripts/verify_snapshot_bound_execution.py",
        root / "scripts/verify_run_freshness.py",
        root / "scripts/adjudicate_agent_receipts.py",
        root / "scripts/local_agent_executor.py",
        root / "scripts/finalize_local_agent_execution.py",
        root / "scripts/prepare_local_agent_run.py",
        root / "scripts/run_local_agent_workflow.py",
        root / "scripts/manage_local_agent_run.py",
        root / "tests/test_collect_write_plans_from_refs.py",
        root / "tests/test_write_plan_conflicts.py",
        root / "tests/test_write_plan_scope.py",
        root / "tests/test_snapshot_bound_execution.py",
        root / "tests/test_run_freshness.py",
        root / "tests/test_actor_claims.py",
        root / "tests/test_snapshot_governance_registration.py",
        root / "tests/test_adjudicate_agent_receipts.py",
        root / "tests/test_local_agent_executor.py",
        root / "tests/test_local_executor_registration.py",
        root / "tests/test_finalize_local_agent_execution.py",
        root / "tests/test_prepare_local_agent_run.py",
        root / "tests/test_run_local_agent_workflow.py",
        root / "tests/test_manage_local_agent_run.py",
    ]
    for path in required_files:
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing_or_empty:{path.relative_to(root)}")
    if failures:
        return {"result": "FAIL", "failures": failures, "checks": checks, "lane": lane}

    reg = load_json(reg_path)
    gates = load_json(gate_path)
    if reg.get("schema_version", 0) < 23:
        failures.append("registry_schema_version_lt_23")

    contracts = reg.get("contracts") or {}
    expected_contracts = {
        "task_schema": "ai-system/control-plane/task-contract.schema.json",
        "run_schema": "ai-system/control-plane/run-contract.schema.json",
        "receipt_schema": "ai-system/control-plane/receipt.schema.json",
        "write_plan_schema": "ai-system/control-plane/write-plan.schema.json",
        "claim_schema": "ai-system/control-plane/claim.schema.json",
        "state_machine": "ai-system/control-plane/state-machine.json",
        "static_validator": "scripts/validate_agent_control_plane.py",
        "write_plan_collector": "scripts/collect_write_plans_from_refs.py",
        "write_conflict_checker": "scripts/check_write_plan_conflicts.py",
        "write_scope_enforcer": "scripts/verify_write_plan_scope.py",
        "snapshot_execution_verifier": "scripts/verify_snapshot_bound_execution.py",
        "run_freshness_verifier": "scripts/verify_run_freshness.py",
        "receipt_adjudicator": "scripts/adjudicate_agent_receipts.py",
        "local_agent_executor": "scripts/local_agent_executor.py",
        "local_execution_finalizer": "scripts/finalize_local_agent_execution.py",
        "local_run_preparer": "scripts/prepare_local_agent_run.py",
        "local_workflow_orchestrator": "scripts/run_local_agent_workflow.py",
        "run_lifecycle_manager": "scripts/manage_local_agent_run.py",
    }
    for key, expected in expected_contracts.items():
        if contracts.get(key) != expected:
            failures.append(f"contract_path:{key}:{contracts.get(key)}")
    if not any(item.startswith("contract_path:") for item in failures):
        checks.append("machine_readable_contract_registry")

    ownership = reg.get("ownership") or {}
    ownership_expectations = {
        "claim_mode": "create-only",
        "claim_must_precede_plan": True,
        "claim_conflict": "VETO",
        "automatic_takeover": False,
        "force_push_allowed": False,
        "recovery": "new-run-id",
    }
    for key, expected in ownership_expectations.items():
        if ownership.get(key) != expected:
            failures.append(f"ownership_contract:{key}")
    claim_template = str(ownership.get("claim_path_template", ""))
    for marker in ["{issue_number}", "{run_id}", "{actor_id}"]:
        if marker not in claim_template:
            failures.append(f"ownership_contract:claim_path_template:{marker}")
    if not any(item.startswith("ownership_contract:") for item in failures):
        checks.append("actor_ownership_claim_contract")

    planning = reg.get("planning") or {}
    planning_expectations = {
        "mode": "two-phase-fanout",
        "phase_1": "declare-write-set-on-actor-branch-before-mutation",
        "phase_2": "execute-after-cross-ref-conflict-preflight",
        "plan_source": "isolated_actor_branch",
        "collector": "scripts/collect_write_plans_from_refs.py",
        "collector_access": "read-only-git-ref-snapshots",
        "collector_output": "ephemeral-not-committed",
        "shared_mutable_plan_ledger": False,
        "checker": "scripts/check_write_plan_conflicts.py",
        "scope_enforcer": "scripts/verify_write_plan_scope.py",
        "actual_diff_must_be_subset_of_write_set": True,
        "unresolved_overlap": "VETO",
        "undeclared_actual_path": "VETO",
        "duplicate_ref": "VETO",
        "plan_actor_or_branch_mismatch": "VETO",
        "dependency_cycle": "VETO",
        "base_sha_mismatch": "VETO",
        "duplicate_branch": "VETO",
        "path_traversal": "VETO",
        "snapshot_resolution": "resolve-ref-once-then-read-by-sha",
        "snapshot_hash_algorithm": "sha256",
        "approved_plan_snapshot_immutable": True,
        "approved_claim_snapshot_immutable": True,
        "readonly_empty_write_set_allowed": True,
        "readonly_task_writes": "VETO",
    }
    for key, expected in planning_expectations.items():
        if planning.get(key) != expected:
            failures.append(f"planning_contract:{key}")
    if not any(item.startswith("planning_contract:") for item in failures):
        checks.append("two_phase_write_plan_contract")
        checks.append("isolated_ref_plan_collection")
        checks.append("write_scope_enforcement_contract")
        checks.append("immutable_plan_snapshot_contract")

    execution_binding = reg.get("execution_binding") or {}
    execution_expectations = {
        "verifier": "scripts/verify_snapshot_bound_execution.py",
        "current_branch_head_must_equal_verified_head": True,
        "plan_head_must_be_ancestor": True,
        "plan_snapshot_hash_must_match": True,
        "claim_snapshot_hash_must_match": True,
        "own_receipt_is_only_control_plane_diff_exception": True,
        "receipt_identity_must_match_claim_snapshot": True,
        "receipt_work_head_from_head_sha": True,
        "receipt_commit_must_be_receipt_only": True,
        "receipt_commit_must_directly_follow_work_head": True,
    }
    for key, expected in execution_expectations.items():
        if execution_binding.get(key) != expected:
            failures.append(f"execution_binding:{key}")
    if not any(item.startswith("execution_binding:") for item in failures):
        checks.append("snapshot_bound_execution_contract")

    integration = reg.get("integration") or {}
    integration_expectations = {
        "branch_scope": "per-run",
        "current_base_must_match_pinned_base": True,
        "stale_base": "VETO_AND_NEW_RUN",
        "freshness_verifier": "scripts/verify_run_freshness.py",
    }
    for key, expected in integration_expectations.items():
        if integration.get(key) != expected:
            failures.append(f"integration_contract:{key}")
    if not any(item.startswith("integration_contract:") for item in failures):
        checks.append("run_base_freshness_contract")

    agents = reg.get("agents") or []
    ids = [a.get("id") for a in agents]
    if ids != EXPECTED_AGENT_IDS:
        failures.append(f"agent_ids:{ids}")
    else:
        checks.append("exactly_10_ordered_agents")
    actual_names = {str(agent.get("id")): str(agent.get("name_zh")) for agent in agents}
    if actual_names != EXPECTED_AGENT_NAMES:
        failures.append(f"agent_role_names:{actual_names}")
    else:
        checks.append("exact_10_named_agent_roles")
    if len({a.get("role_file") for a in agents}) != 10:
        failures.append("agent_role_files_not_unique")
    for agent in agents:
        role_path = root / agent.get("role_file", "")
        if not role_path.is_file():
            failures.append(f"missing_role_file:{agent.get('id')}:{role_path}")
        else:
            text = role_path.read_text(encoding="utf-8")
            for marker in ["PASS", "VETO", "Evidence contract", "Independence"]:
                if marker not in text:
                    failures.append(f"role_contract_marker:{agent.get('id')}:{marker}")
    adversarial = next((a for a in agents if a.get("id") == "A05"), None)
    if not adversarial or adversarial.get("slug") != "adversarial" or adversarial.get("name_zh") != "反方代理":
        failures.append("A05_adversarial_contract_missing")
    else:
        checks.append("adversarial_agent_present")

    namespace = reg.get("namespace") or {}
    concurrency = reg.get("concurrency") or {}
    required_templates = {
        "integration_branch_template": ["{issue_number}", "{run_id}"],
        "agent_branch_template": ["{issue_number}", "{agent_id}", "{run_id}"],
        "chat_branch_template": ["{issue_number}", "{run_id}"],
        "write_plan_path_template": ["{issue_number}", "{run_id}", "{actor_id}"],
        "claim_path_template": ["{issue_number}", "{run_id}", "{actor_id}"],
        "receipt_path_template": ["{issue_number}", "{run_id}", "{agent_id}"],
    }
    for key, markers in required_templates.items():
        value = str(namespace.get(key, ""))
        for marker in markers:
            if marker not in value:
                failures.append(f"namespace_template:{key}:{marker}")
    invariants = {
        "same_branch_multiple_writers": False,
        "shared_mutable_run_files": False,
        "shared_mutable_plan_ledger": False,
        "plan_collection_read_only_across_refs": True,
        "update_requires_current_blob_sha": True,
        "base_sha_pinned": True,
        "write_plan_required_before_mutation": True,
        "write_set_overlap_requires_dependency": True,
        "actual_diff_scope_verification_required_before_fanin": True,
        "integration_via_pull_request_only": True,
        "integration_branch_isolated_per_run": True,
    }
    for key, expected in invariants.items():
        if concurrency.get(key) is not expected:
            failures.append(f"concurrency_invariant:{key}")
    if not any(item.startswith("concurrency_invariant:") for item in failures):
        checks.append("single_writer_optimistic_concurrency")
        checks.append("preflight_and_scope_enforced_parallelism")
        checks.append("no_shared_mutable_plan_ledger")
        checks.append("per_run_integration_branch")

    receipt_binding = reg.get("runtime_adjudication") or {}
    receipt_binding_expectations = {
        "pass_veto_receipt_schema_version": 2,
        "receipt_claim_binding_required": True,
        "receipt_plan_head_binding_required": True,
        "receipt_work_head_semantics": "pre-receipt-task-head",
        "receipt_only_final_commit_required": True,
    }
    for key, expected in receipt_binding_expectations.items():
        if receipt_binding.get(key) != expected:
            failures.append(f"receipt_binding:{key}")
    if not any(item.startswith("receipt_binding:") for item in failures):
        checks.append("receipt_claim_binding_contract")

    local_executor = reg.get("local_executor") or {}
    local_executor_expectations = {
        "backend": "claude-code",
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
        "wrapper_observed_independence_required": True,
        "model_self_asserted_independence_accepted": False,
        "bash_allowed_by_default": False,
        "claim_bound_assignment_required": True,
        "predeclared_execution_id_required": True,
        "finalizer": "scripts/finalize_local_agent_execution.py",
        "receipt_materialization": "claim-bound-v2",
        "aggregate_pass_requires_all_ten_pass": True,
    }
    for key, expected in local_executor_expectations.items():
        if local_executor.get(key) != expected:
            failures.append(f"local_executor:{key}")
    readonly_roles = local_executor.get("readonly_roles") or []
    if readonly_roles != ["A01","A02","A03","A04","A05","A06","A08","A09","A10"]:
        failures.append("local_executor:readonly_roles")
    if local_executor.get("write_role") != "A07":
        failures.append("local_executor:write_role")
    if local_executor.get("readonly_allowed_tools") != ["Read", "Glob", "Grep"]:
        failures.append("local_executor:readonly_allowed_tools")
    if local_executor.get("write_role_allowed_tools") != ["Read", "Glob", "Grep", "Edit", "Write"]:
        failures.append("local_executor:write_role_allowed_tools")
    if not any(item.startswith("local_executor:") for item in failures):
        checks.append("local_independent_executor_contract")

    local_finalizer = reg.get("local_finalizer") or {}
    local_finalizer_expectations = {
        "driver": "scripts/finalize_local_agent_execution.py",
        "write_role": "A07",
        "readonly_workspace_mutation": "VETO",
        "preexisting_staged_changes": "VETO",
        "write_scope_required_before_task_commit": True,
        "trusted_wrapper_commits_task_changes": True,
        "pass_veto_receipt_schema_version": 2,
        "receipt_commit_only": True,
        "snapshot_verification_required": True,
        "remote_push_performed": False,
    }
    for key, expected in local_finalizer_expectations.items():
        if local_finalizer.get(key) != expected:
            failures.append(f"local_finalizer:{key}")
    if not any(item.startswith("local_finalizer:") for item in failures):
        checks.append("trusted_local_finalizer_contract")

    local_preparer = reg.get("local_run_preparer") or {}
    expected_dependencies = {
        "A01": [],
        "A02": ["A01"],
        "A03": ["A01"],
        "A04": ["A01"],
        "A05": ["A01", "A02", "A04"],
        "A06": ["A01", "A05"],
        "A07": ["A01", "A02", "A03", "A04", "A05", "A06"],
        "A08": ["A01", "A07"],
        "A09": ["A01", "A07", "A08"],
        "A10": ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09"],
    }
    local_preparer_expectations = {
        "driver": "scripts/prepare_local_agent_run.py",
        "required_actor_count": 10,
        "claim_before_plan": True,
        "readonly_empty_write_set_required": True,
        "write_role": "A07",
        "prospective_preflight_before_mutation": True,
        "committed_snapshot_collection_required": True,
        "committed_preflight_required": True,
        "integration_branch_created_after_preflight": True,
        "workspace_root_must_be_outside_source_repo": True,
        "source_worktree_must_be_clean": True,
        "base_ref_must_equal_pinned_base": True,
        "remote_push_performed": False,
        "dependencies": expected_dependencies,
    }
    for key, expected in local_preparer_expectations.items():
        if local_preparer.get(key) != expected:
            failures.append(f"local_preparer:{key}")
    if not any(item.startswith("local_preparer:") for item in failures):
        checks.append("local_run_preparer_contract")

    local_orchestrator = reg.get("local_workflow_orchestrator") or {}
    local_orchestrator_expectations = {
        "driver": "scripts/run_local_agent_workflow.py",
        "required_actor_count": 10,
        "dependency_aware": True,
        "stop_downstream_on_nonpass": True,
        "readonly_dependency_workspaces_via_add_dir": True,
        "A07_external_dependency_dirs_forbidden": True,
        "A07_dependency_context": "trusted-receipt-summary-in-prompt",
        "trusted_finalizer_required_per_actor": True,
        "distinct_process_instances_required": True,
        "distinct_backend_sessions_required": True,
        "deterministic_adjudication_required": True,
        "base_freshness_required": True,
        "remote_push_performed": False,
        "full_local_runtime_pass_requires": ["A01-A10_PASS", "adjudication_PASS", "base_freshness_PASS"],
        "resume_existing_receipts_supported": True,
        "resume_only_missing_actors": True,
        "resume_revalidation_required": True,
        "existing_veto_receipt_terminal": True,
    }
    for key, expected in local_orchestrator_expectations.items():
        if local_orchestrator.get(key) != expected:
            failures.append(f"local_orchestrator:{key}")
    if not any(item.startswith("local_orchestrator:") for item in failures):
        checks.append("local_dependency_orchestrator_contract")

    runtime_attestation = reg.get("runtime_attestation") or {}
    runtime_attestation_expectations = {
        "durable_receipt_attestation_required": True,
        "raw_backend_session_persisted": False,
        "backend_session_storage": "sha256-only",
        "process_instance_id_persisted": True,
        "process_id_persisted": True,
        "spawn_monotonic_ns_persisted": True,
        "stdout_stderr_hashes_persisted": True,
        "distinct_process_instances_required": True,
        "distinct_backend_session_hashes_required": True,
        "observer": "scripts/local_agent_executor.py",
        "materializer": "scripts/finalize_local_agent_execution.py",
        "adjudicator": "scripts/adjudicate_agent_receipts.py",
    }
    for key, expected in runtime_attestation_expectations.items():
        if runtime_attestation.get(key) != expected:
            failures.append(f"runtime_attestation:{key}")
    if not any(item.startswith("runtime_attestation:") for item in failures):
        checks.append("durable_runtime_attestation_contract")

    lifecycle = reg.get("run_lifecycle_manager") or {}
    lifecycle_expectations = {
        "driver": "scripts/manage_local_agent_run.py",
        "status_supported": True,
        "actor_publish_fast_forward_only": True,
        "actor_publish_atomic_multi_ref": True,
        "actor_publish_preflight_all_refs_before_push": True,
        "commands": ["status", "publish", "integrate", "publish-integration", "recover", "rehydrate", "resume", "cleanup"],
        "actor_publish_force_allowed": False,
        "actor_publish_idempotent": True,
        "integration_requires_workflow_pass": True,
        "integration_requires_adjudication_pass": True,
        "integration_requires_fresh_base": True,
        "integration_re_adjudication_required": True,
        "integration_task_diff_must_equal_verified_A07_diff": True,
        "integration_receipt_commit_only": True,
        "integration_remote_push_performed": False,
        "cleanup_dirty_worktree_veto_without_force": True,
        "cleanup_preserves_local_branches": True,
        "cleanup_deletes_remote_branches": False,
        "remote_force_push_allowed": False,
        "integration_publish_fast_forward_only": True,
        "integration_publish_idempotent": True,
        "rehydrate_supported": True,
        "rehydrate_requires_existing_local_branches": True,
        "rehydrate_remote_mutation_performed": False,
        "resume_supported": True,
        "resume_only_missing_actors": True,
        "resume_revalidates_snapshot_and_attestation": True,
        "resume_existing_veto_terminal": True,
        "resume_provider_required_only_for_missing_actors": True,
        "git_only_recovery_supported": True,
        "recovery_requires_coordination_files": False,
        "recovery_requires_ten_actor_branches": True,
        "recovery_reconstructs_plan_head_from_git_history": True,
        "recovery_recomputes_snapshot_hashes": True,
        "recovery_rechecks_plan_preflight": True,
        "recovery_requires_fresh_base": True,
        "recovery_remote_mutation_performed": False,
        "recovery_requires_single_claim_path_commit": True,
        "recovery_requires_single_plan_path_commit": True,
        "recovery_claim_commit_must_precede_plan_commit": True,
        "status_receipts_read_from_git_head": True,
        "status_revalidates_snapshots_without_workflow": True,
        "status_runs_adjudication_without_workflow": True,
        "status_requires_fresh_base_for_finalized_pass": True,
    }
    for key, expected in lifecycle_expectations.items():
        if lifecycle.get(key) != expected:
            failures.append(f"run_lifecycle:{key}")
    if not any(item.startswith("run_lifecycle:") for item in failures):
        checks.append("run_lifecycle_manager_contract")

    runtime = reg.get("runtime_adjudication") or {}
    runtime_expectations = {
        "required_agent_count": 10,
        "all_agents_must_pass": True,
        "veto_tolerance": 0,
        "missing_receipt_tolerance": 0,
        "distinct_executor_ids_required": True,
        "distinct_execution_ids_required": True,
        "distinct_evidence_partitions_required": True,
        "distinct_branches_required": True,
        "direct_failure_overrides_votes": True,
        "repository_receipts_do_not_prove_physical_independence": True,
    }
    for key, expected in runtime_expectations.items():
        if runtime.get(key) != expected:
            failures.append(f"runtime_adjudication:{key}")
    if not any(item.startswith("runtime_adjudication:") for item in failures):
        checks.append("independent_receipt_fail_closed_contract")

    gate_list = gates.get("gates") or []
    gate_ids = [g.get("id") for g in gate_list]
    gate_agents = [g.get("agent_id") for g in gate_list]
    if gate_ids != EXPECTED_GATE_IDS:
        failures.append(f"gate_ids:{gate_ids}")
    if gate_agents != EXPECTED_AGENT_IDS:
        failures.append(f"gate_agent_mapping:{gate_agents}")
    aggregate = gates.get("aggregate") or {}
    if not (
        aggregate.get("mode") == "ALL"
        and aggregate.get("required_pass_count") == 10
        and aggregate.get("veto_tolerance") == 0
        and aggregate.get("missing_receipt_tolerance") == 0
        and aggregate.get("direct_test_failure_overrides_votes") is True
    ):
        failures.append("aggregate_not_fail_closed")
    else:
        checks.append("all_10_fail_closed_gate")

    task = load_json(cp / "task-contract.schema.json")
    run = load_json(cp / "run-contract.schema.json")
    receipt = load_json(cp / "receipt.schema.json")
    write_plan = load_json(cp / "write-plan.schema.json")
    claim = load_json(cp / "claim.schema.json")
    state = load_json(cp / "state-machine.json")
    for key in ["issue_number", "title", "goal", "repository", "base_sha", "acceptance", "risk_level"]:
        if key not in task.get("required", []):
            failures.append(f"task_schema_required:{key}")
    for key in ["issue_number", "run_id", "base_sha", "integration_branch", "agent_branches", "claims", "plan_snapshots", "receipts", "status"]:
        if key not in run.get("required", []):
            failures.append(f"run_schema_required:{key}")
    for key in ["issue_number", "run_id", "actor_id", "branch", "base_sha", "write_set", "depends_on", "status"]:
        if key not in write_plan.get("required", []):
            failures.append(f"write_plan_schema_required:{key}")
    write_set_schema = ((write_plan.get("properties") or {}).get("write_set") or {})
    if write_set_schema.get("minItems", 0) > 0:
        failures.append("write_plan_schema_readonly_empty_write_set_forbidden")
    else:
        checks.append("readonly_empty_write_set_contract")
    for key in ["schema_version", "issue_number", "run_id", "actor_id", "branch", "base_sha", "claim_id", "executor_id", "execution_id", "status"]:
        if key not in claim.get("required", []):
            failures.append(f"claim_schema_required:{key}")
    if ((claim.get("properties") or {}).get("status") or {}).get("const") != "CLAIMED":
        failures.append("claim_schema_status_not_claimed")
    receipt_ids = (((receipt.get("properties") or {}).get("agent_id") or {}).get("enum") or [])
    if receipt_ids != EXPECTED_AGENT_IDS:
        failures.append(f"receipt_agent_ids:{receipt_ids}")
    receipt_props = receipt.get("properties") or {}
    if (receipt_props.get("schema_version") or {}).get("enum") != [1, 2]:
        failures.append("receipt_schema_versions_not_1_2")
    for key in ["claim_id", "plan_head_sha", "runtime_attestation"]:
        if key not in receipt_props:
            failures.append(f"receipt_schema_property:{key}")
    pass_veto_then = ((receipt.get("allOf") or [{}])[0].get("then") or {})
    pass_veto_required = set(pass_veto_then.get("required") or [])
    for key in ["claim_id", "plan_head_sha", "head_sha", "executor_id", "execution_id", "runtime_attestation"]:
        if key not in pass_veto_required:
            failures.append(f"receipt_v2_required:{key}")
    attestation_schema = receipt_props.get("runtime_attestation") or {}
    attestation_required = set(attestation_schema.get("required") or [])
    for key in ["provider", "observer", "process_instance_id", "process_id", "spawn_monotonic_ns", "backend_session_sha256", "stdout_sha256", "stderr_sha256"]:
        if key not in attestation_required:
            failures.append(f"runtime_attestation_schema_required:{key}")
    if (((pass_veto_then.get("properties") or {}).get("schema_version") or {}).get("const")) != 2:
        failures.append("receipt_pass_veto_schema_not_v2")
    for key in ["agent_id", "branch", "result", "independent_agent_execution"]:
        if key not in receipt.get("required", []):
            failures.append(f"receipt_schema_required:{key}")
    if state.get("schema_version", 0) < 8:
        failures.append("state_machine_schema_version_lt_8")
    forbidden = set(state.get("forbidden_shortcuts") or [])
    for shortcut in [
        "role_file_exists -> PASS",
        "branch_exists -> PASS",
        "agent_message_says_success -> PASS",
        "VETO -> majority_vote_override",
        "NOT_RUN -> PASS_without_new_independent_execution",
        "branch_name_resolves -> approved_snapshot_without_sha",
        "claim_exists -> takeover_allowed",
        "plan_hash_mismatch -> continue_execution",
        "claim_hash_mismatch -> continue_execution",
        "stale_base -> merge",
        "force_push -> ownership_transfer",
        "old_snapshot -> current_run_PASS",
        "own_receipt_path -> trusted_receipt_content",
        "v1_PASS_receipt -> runtime_PASS",
        "receipt_executor_mismatch -> continue_adjudication",
        "existing_VETO_receipt -> overwrite_same_run",
        "resume_existing_PASS_receipt -> trust_without_snapshot_and_attestation_revalidation",
        "remote_divergence -> force_push",
        "integration_task_diff_mismatch -> publish",
        "cleanup_dirty_worktree -> remove_without_explicit_force",
        "remote_actor_branches -> recovered_PASS_without_plan_claim_hash_and_preflight_revalidation",
        "missing_coordination_json -> unrecoverable_when_remote_actor_branches_exist",
        "actor_publish_partial_success -> accepted",
        "actor_publish_remote_divergence -> push_other_refs",
        "multiple_plan_commits -> recovered_plan_snapshot",
        "multiple_claim_commits -> recovered_claim_snapshot",
        "claim_commit_not_ancestor -> recovered_plan_snapshot",
        "removed_worktree -> receipt_missing_despite_git_head",
        "missing_workflow_json -> PREPARED_despite_verified_git_receipts",
        "multiple_receipt_commits -> trusted_final_receipt",
    ]:
        if shortcut not in forbidden:
            failures.append(f"state_machine_shortcut_missing:{shortcut}")
    if not any(item.startswith("state_machine_shortcut_missing:") for item in failures):
        checks.append("no_fake_completion_shortcuts")

    if lane:
        lane = lane.zfill(2)
        agent_id = f"A{lane}"
        gate_id = f"G{lane}"
        if agent_id not in ids or gate_id not in gate_ids:
            failures.append(f"unknown_lane:{lane}")
        else:
            checks.append(f"lane_{lane}_contract")

    secret_re = re.compile(
        r"(?i)(api[_-]?key|access[_-]?token|password|private[_-]?key)\s*[:=]\s*[\"\']?[A-Za-z0-9_./+=-]{16,}"
    )
    for path in cp.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yml", ".yaml", ".txt"}:
            if secret_re.search(path.read_text(encoding="utf-8")):
                failures.append(f"credential_shaped_value:{path.relative_to(root)}")
    if not any(item.startswith("credential_shaped_value:") for item in failures):
        checks.append("no_credential_shaped_values")

    return {
        "schemaVersion": 15,
        "lane": lane,
        "checks": checks,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--lane")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    receipt = validate(pathlib.Path(args.root), args.lane)
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
