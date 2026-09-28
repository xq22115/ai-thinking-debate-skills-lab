from __future__ import annotations

import pathlib
import sys
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evaluate_root_cause_falsification_receipt as runtime


def good_receipt() -> dict:
    return {
        "schema_version": 1,
        "claim_scope": "universal_zero_failure",
        "change_class": "ROOT_FIX",
        "goal_preserved": True,
        "root_mechanism_identified": True,
        "root_mechanism_changed": True,
        "protected_capability_regressed": False,
        "research": {
            "material_external_advice_used": True,
            "scope_version_lineage_qualified": True,
            "discriminating_target_test_before_mutation": True,
            "one_search_hit_direct_to_patch": False,
        },
        "verification": {
            "matrix_predeclared": True,
            "all_in_scope_trials_counted": True,
            "original_failure_replayed": True,
            "original_failure_reproduces_after_fix": False,
            "negative_check_passed": True,
            "regression_check_passed": True,
            "failures": [],
        },
        "readback": {"owning_runtime_observed": True},
    }


class RootCauseFalsificationRuntimeTests(unittest.TestCase):
    def assertStatus(self, receipt: dict, status: str) -> dict:
        result = runtime.evaluate_receipt(receipt)
        self.assertEqual(result["status"], status, result)
        return result

    def test_clean_root_fix_passes(self) -> None:
        self.assertStatus(good_receipt(), "ROOT_FIX_VERIFIED")

    def test_one_reproducible_in_scope_failure_vetoes_universal_pass(self) -> None:
        receipt = good_receipt()
        receipt["verification"]["failures"] = [
            {"case_id": "original-lag", "in_scope": True, "reproducible": True}
        ]
        result = self.assertStatus(receipt, "FAIL")
        self.assertIn("universal_claim_falsified:original-lag", result["reasons"])

    def test_nonreproducible_or_out_of_scope_failure_does_not_fake_counterexample(self) -> None:
        receipt = good_receipt()
        receipt["verification"]["failures"] = [
            {"case_id": "out", "in_scope": False, "reproducible": True},
            {"case_id": "fluke", "in_scope": True, "reproducible": False},
        ]
        self.assertStatus(receipt, "ROOT_FIX_VERIFIED")

    def test_limit_or_guardrail_cannot_be_root_fix(self) -> None:
        for change_class in ("MITIGATION", "GUARDRAIL", "WORKAROUND", "DEGRADATION"):
            with self.subTest(change_class=change_class):
                receipt = good_receipt()
                receipt["change_class"] = change_class
                self.assertStatus(receipt, "MITIGATION_ONLY")

    def test_goal_drift_blocks_even_otherwise_green_receipt(self) -> None:
        receipt = good_receipt()
        receipt["goal_preserved"] = False
        self.assertStatus(receipt, "FAIL")

    def test_one_search_hit_direct_to_patch_fails(self) -> None:
        receipt = good_receipt()
        receipt["research"]["one_search_hit_direct_to_patch"] = True
        self.assertStatus(receipt, "FAIL")

    def test_external_advice_requires_qualification_and_target_test(self) -> None:
        receipt = good_receipt()
        receipt["research"]["scope_version_lineage_qualified"] = False
        self.assertStatus(receipt, "FAIL")
        receipt = good_receipt()
        receipt["research"]["discriminating_target_test_before_mutation"] = False
        self.assertStatus(receipt, "FAIL")

    def test_root_cause_can_be_proven_before_fix(self) -> None:
        receipt = good_receipt()
        receipt["root_mechanism_changed"] = False
        self.assertStatus(receipt, "ROOT_CAUSE_PROVEN")

    def test_missing_closure_proof_is_partial_not_verified(self) -> None:
        for key in (
            "matrix_predeclared",
            "all_in_scope_trials_counted",
            "original_failure_replayed",
            "negative_check_passed",
            "regression_check_passed",
        ):
            with self.subTest(key=key):
                receipt = good_receipt()
                receipt["verification"][key] = False
                self.assertStatus(receipt, "PARTIAL")

    def test_original_failure_still_reproducing_is_partial(self) -> None:
        receipt = good_receipt()
        receipt["verification"]["original_failure_reproduces_after_fix"] = True
        self.assertStatus(receipt, "PARTIAL")

    def test_missing_owning_runtime_readback_is_partial(self) -> None:
        receipt = good_receipt()
        receipt["readback"]["owning_runtime_observed"] = False
        self.assertStatus(receipt, "PARTIAL")

    def test_protected_capability_regression_is_partial(self) -> None:
        receipt = good_receipt()
        receipt["protected_capability_regressed"] = True
        self.assertStatus(receipt, "PARTIAL")

    def test_probabilistic_slo_uses_declared_error_budget(self) -> None:
        receipt = good_receipt()
        receipt["claim_scope"] = "probabilistic_slo"
        receipt["slo"] = {
            "error_budget_rate": 0.001,
            "total_trials": 10000,
            "observed_failures": 1,
        }
        self.assertStatus(receipt, "ROOT_FIX_VERIFIED")

        receipt["slo"]["observed_failures"] = 11
        result = self.assertStatus(receipt, "FAIL")
        self.assertTrue(any(x.startswith("slo_exceeded:") for x in result["reasons"]))

    def test_bounded_behavior_counterexample_remains_partial(self) -> None:
        receipt = good_receipt()
        receipt["claim_scope"] = "bounded_behavior"
        receipt["verification"]["failures"] = [
            {"case_id": "bounded-edge", "in_scope": True, "reproducible": True}
        ]
        self.assertStatus(receipt, "PARTIAL")


if __name__ == "__main__":
    unittest.main()
