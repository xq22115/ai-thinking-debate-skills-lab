from __future__ import annotations

import pathlib
import sys
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evaluate_execution_integrity_receipt as runtime

BASE = "1" * 40
HEAD = "2" * 40


def scenario(family: str) -> dict:
    common = {
        "family": family,
        "executed": True,
        "precondition": f"{family} precondition",
        "action": f"execute {family}",
        "expected_result": "handled",
        "actual_result": "handled",
        "evidence": [f"evidence://{family}"],
        "invariant_violations": [],
        "observations": {},
    }
    obs = common["observations"]
    if family == "normal_valid_input":
        common["expected_result"] = "success"
        common["actual_result"] = "success"
        obs["behavior_matches_expected"] = True
    elif family in {"invalid_input", "empty_or_missing_input"}:
        obs.update(rejected=True, failure_detected=True, state_changed=False)
    elif family == "idempotent_repeat":
        obs.update(
            duplicate_side_effects=False,
            state_after_first={"revision": HEAD},
            state_after_second={"revision": HEAD},
        )
    elif family == "rapid_consecutive_operations":
        obs.update(operations_observed=3, lost_update=False, final_state_consistent=True)
    elif family == "reordered_operations":
        obs.update(out_of_order_detected=True, state_corrupted=False)
    elif family == "permission_loss_or_scope_reduction":
        obs.update(permission_loss_detected=True, unauthorized_write=False)
    elif family == "network_interruption_timeout_retry":
        obs.update(
            interruption_detected=True,
            recovered=True,
            retry_performed=True,
            final_readback_matches=True,
        )
    elif family == "dependency_unavailable_or_version_mismatch":
        obs.update(
            dependency_problem_detected=True,
            recovered_with_verified_compatible_dependency=False,
            operation_blocked=True,
            reported_success=False,
        )
    elif family == "stale_cache_state_or_old_installation_residue":
        obs.update(stale_state_detected=True, stale_state_accepted=False)
    elif family == "partial_success_then_failure":
        obs.update(partial_failure_detected=True, reported_success=False)
    elif family == "stale_search_index_vs_direct_lookup":
        obs.update(
            search_miss_observed=True,
            fallback_mechanism="exact_repository_lookup",
            fallback_outcome="found",
        )
    elif family == "exact_revision_mismatch":
        obs.update(revision_mismatch_detected=True, mismatched_state_accepted=False)
    elif family == "rollback_and_recovery":
        obs.update(
            rollback_target_recorded=True,
            rollback_performed=True,
            recovery_readback_matches=True,
        )
    else:
        raise AssertionError(f"unhandled scenario {family}")
    return common


def good_receipt(extra_family: str = "rollback_and_recovery") -> dict:
    families = ["normal_valid_input"]
    if extra_family != "normal_valid_input":
        families.append(extra_family)
    else:
        families.append("rollback_and_recovery")
    return {
        "schema_version": 1,
        "operation_id": "github-integrity-test",
        "material_change": True,
        "target_identity": {
            "repository": "owner/repo",
            "branch": "fix/integrity",
            "path": "control-plane",
        },
        "base_revision": BASE,
        "reported_revision": HEAD,
        "protected_capabilities": {
            "before": ["pull", "push", "runtime-readback"],
            "after": ["pull", "push", "runtime-readback"],
        },
        "permissions": {
            "before": ["pull", "push"],
            "after": ["pull", "push"],
            "verified": True,
        },
        "io_contract": {
            "before": "github-execution-integrity-v1",
            "after": "github-execution-integrity-v1",
            "migration_accepted": False,
        },
        "source_resolution": {
            "resolved": True,
            "attempts": [
                {"mechanism": "exact_repository_lookup", "result": "found"},
            ],
        },
        "operation": {
            "attempted": True,
            "result": "success",
            "failure_detected": False,
            "partial_success": False,
        },
        "readback": {
            "performed": True,
            "revision": HEAD,
            "matches_intended": True,
        },
        "adjacent_regression": {"performed": True, "passed": True},
        "rollback": {"target_revision": BASE, "available": True},
        "task_outcome_verified": True,
        "evidence_families": [
            "target_runtime_or_owning_installation_readback",
            "exact_github_object_and_revision_metadata",
            "high_signal_third_party_practitioner_or_tooling_evidence",
        ],
        "lifecycle": {"applicable": False},
        "required_scenarios": families,
        "scenario_results": [scenario(family) for family in families],
    }


class ExecutionIntegrityRuntimeFaultTests(unittest.TestCase):
    def assertPass(self, receipt: dict) -> dict:
        result = runtime.evaluate_receipt(receipt)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["failures"], [], result)
        self.assertEqual(result["invariant_violations"], [], result)
        return result

    def assertFail(self, receipt: dict, invariant: str | None = None) -> dict:
        result = runtime.evaluate_receipt(receipt)
        self.assertEqual(result["result"], "FAIL", result)
        if invariant is not None:
            self.assertIn(invariant, result["invariant_violations"], result)
        return result

    def test_clean_material_receipt_passes(self) -> None:
        self.assertPass(good_receipt())

    def test_every_scenario_family_executes_and_passes_when_handled(self) -> None:
        for family in sorted(runtime.SUPPORTED_SCENARIOS):
            with self.subTest(family=family):
                self.assertPass(good_receipt(family))

    def test_every_scenario_family_fails_closed_when_its_observation_is_broken(self) -> None:
        breakers = {
            "normal_valid_input": lambda obs: obs.__setitem__("behavior_matches_expected", False),
            "invalid_input": lambda obs: obs.__setitem__("failure_detected", False),
            "empty_or_missing_input": lambda obs: obs.__setitem__("rejected", False),
            "idempotent_repeat": lambda obs: obs.__setitem__(
                "state_after_second", {"revision": "changed"}
            ),
            "rapid_consecutive_operations": lambda obs: obs.__setitem__("lost_update", True),
            "reordered_operations": lambda obs: obs.__setitem__("state_corrupted", True),
            "permission_loss_or_scope_reduction": lambda obs: obs.__setitem__(
                "unauthorized_write", True
            ),
            "network_interruption_timeout_retry": lambda obs: obs.__setitem__(
                "final_readback_matches", False
            ),
            "dependency_unavailable_or_version_mismatch": lambda obs: obs.__setitem__(
                "reported_success", True
            ),
            "stale_cache_state_or_old_installation_residue": lambda obs: obs.__setitem__(
                "stale_state_accepted", True
            ),
            "partial_success_then_failure": lambda obs: obs.__setitem__(
                "reported_success", True
            ),
            "stale_search_index_vs_direct_lookup": lambda obs: obs.__setitem__(
                "fallback_mechanism", "ranked_repository_search"
            ),
            "exact_revision_mismatch": lambda obs: obs.__setitem__(
                "mismatched_state_accepted", True
            ),
            "rollback_and_recovery": lambda obs: obs.__setitem__(
                "recovery_readback_matches", False
            ),
        }
        for family, break_observation in breakers.items():
            with self.subTest(family=family):
                receipt = good_receipt(family)
                target = next(
                    item for item in receipt["scenario_results"] if item["family"] == family
                )
                break_observation(target["observations"])
                result = self.assertFail(receipt, runtime.SCENARIO_GI_MAP[family])
                self.assertIn(family, result["scenario_failures"])

    def test_scenario_name_without_execution_is_not_evidence(self) -> None:
        receipt = good_receipt("network_interruption_timeout_retry")
        target = next(
            item
            for item in receipt["scenario_results"]
            if item["family"] == "network_interruption_timeout_retry"
        )
        target["executed"] = False
        result = self.assertFail(receipt, "GI-04")
        self.assertIn("not_executed", result["scenario_failures"]["network_interruption_timeout_retry"])

    def test_scenario_without_evidence_is_not_pass(self) -> None:
        receipt = good_receipt("permission_loss_or_scope_reduction")
        target = next(
            item
            for item in receipt["scenario_results"]
            if item["family"] == "permission_loss_or_scope_reduction"
        )
        target["evidence"] = []
        self.assertFail(receipt, "GI-02")

    def test_missing_required_scenario_record_is_not_pass(self) -> None:
        receipt = good_receipt("exact_revision_mismatch")
        receipt["scenario_results"] = [
            item for item in receipt["scenario_results"] if item["family"] != "exact_revision_mismatch"
        ]
        self.assertFail(receipt, "GI-08")

    def test_capability_regression_blocks_pass(self) -> None:
        receipt = good_receipt()
        receipt["protected_capabilities"]["after"].remove("push")
        self.assertFail(receipt, "GI-01")

    def test_permission_downgrade_blocks_pass(self) -> None:
        receipt = good_receipt()
        receipt["permissions"]["after"].remove("push")
        self.assertFail(receipt, "GI-02")

    def test_io_contract_drift_blocks_pass_without_accepted_migration(self) -> None:
        receipt = good_receipt()
        receipt["io_contract"]["after"] = "changed-contract"
        self.assertFail(receipt, "GI-03")

    def test_partial_success_must_be_detected(self) -> None:
        receipt = good_receipt()
        receipt["operation"]["partial_success"] = True
        receipt["operation"]["failure_detected"] = False
        self.assertFail(receipt, "GI-04")

    def test_success_without_readback_blocks_pass(self) -> None:
        receipt = good_receipt()
        receipt["readback"]["performed"] = False
        self.assertFail(receipt, "GI-05")

    def test_adjacent_regression_failure_blocks_pass(self) -> None:
        receipt = good_receipt()
        receipt["adjacent_regression"]["passed"] = False
        self.assertFail(receipt, "GI-06")

    def test_rollback_must_bind_exact_base_revision(self) -> None:
        receipt = good_receipt()
        receipt["rollback"]["target_revision"] = "3" * 40
        self.assertFail(receipt, "GI-07")

    def test_readback_must_bind_reported_revision(self) -> None:
        receipt = good_receipt()
        receipt["readback"]["revision"] = "3" * 40
        self.assertFail(receipt, "GI-08")

    def test_search_miss_requires_causally_distinct_fallback(self) -> None:
        receipt = good_receipt()
        receipt["source_resolution"] = {
            "resolved": False,
            "attempts": [
                {"mechanism": "ranked_repository_search", "result": "miss"},
                {"mechanism": "code_search", "result": "miss"},
            ],
        }
        self.assertFail(receipt, "GI-09")

    def test_search_miss_can_recover_via_exact_lookup(self) -> None:
        receipt = good_receipt()
        receipt["source_resolution"] = {
            "resolved": True,
            "attempts": [
                {"mechanism": "ranked_repository_search", "result": "miss"},
                {"mechanism": "exact_repository_lookup", "result": "found"},
            ],
        }
        self.assertPass(receipt)

    def test_repository_search_miss_can_recover_via_code_search(self) -> None:
        receipt = good_receipt()
        receipt["source_resolution"] = {
            "resolved": True,
            "attempts": [
                {"mechanism": "ranked_repository_search", "result": "miss"},
                {"mechanism": "code_search", "result": "found"},
            ],
        }
        self.assertPass(receipt)

    def test_repeating_same_failed_search_mechanism_is_not_distinct_fallback(self) -> None:
        receipt = good_receipt()
        receipt["source_resolution"] = {
            "resolved": True,
            "attempts": [
                {"mechanism": "code_search", "result": "miss"},
                {"mechanism": "code_search", "result": "found"},
            ],
        }
        self.assertFail(receipt, "GI-09")

    def test_lifecycle_cannot_promote_higher_layer_over_missing_lower_layer(self) -> None:
        receipt = good_receipt()
        receipt["lifecycle"] = {
            "applicable": True,
            "ordered_stages": [
                "configured",
                "registered",
                "loaded",
                "executed",
                "observable_effect",
            ],
            "target_stage": "observable_effect",
            "statuses": {
                "configured": "PASS",
                "registered": "NOT_RUN",
                "loaded": "PASS",
                "executed": "PASS",
                "observable_effect": "PASS",
            },
        }
        self.assertFail(receipt, "GI-10")

    def test_write_success_without_verified_outcome_blocks_pass(self) -> None:
        receipt = good_receipt()
        receipt["task_outcome_verified"] = False
        self.assertFail(receipt, "GI-11")

    def test_single_source_family_cannot_prove_material_pass(self) -> None:
        receipt = good_receipt()
        receipt["evidence_families"] = ["official_documentation"]
        self.assertFail(receipt, "GI-12")

    def test_not_run_is_not_pass(self) -> None:
        receipt = good_receipt()
        receipt["operation"]["result"] = "not_run"
        result = runtime.evaluate_receipt(receipt)
        self.assertEqual(result["result"], "NOT_RUN", result)

    def test_blocked_is_not_pass(self) -> None:
        receipt = good_receipt()
        receipt["operation"].update(result="blocked", failure_detected=True)
        result = runtime.evaluate_receipt(receipt)
        self.assertNotEqual(result["result"], "PASS", result)


if __name__ == "__main__":
    unittest.main()
