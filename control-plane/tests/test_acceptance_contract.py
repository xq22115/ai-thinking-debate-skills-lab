from __future__ import annotations

import pathlib
import sys
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_acceptance_contract import validate_contract


def valid_contract() -> dict:
    return {
        "schema_version": 1,
        "task_id": "task-001",
        "task_class": "material",
        "status": "PASS",
        "criteria": [
            {
                "criterion_id": "C1",
                "statement": "Requested behavior works end-to-end",
                "hard": True,
                "observable_test": "Run the user path",
                "state": "SATISFIED",
                "evidence_ids": ["E1"],
            },
            {
                "criterion_id": "C2",
                "statement": "Existing behavior does not regress",
                "hard": True,
                "observable_test": "Run targeted regression",
                "state": "SATISFIED",
                "evidence_ids": ["E2"],
            },
        ],
        "evidence_index": {
            "E1": {"kind": "runtime", "reference": "run:user-path", "result": "PASS"},
            "E2": {"kind": "test", "reference": "test:regression", "result": "PASS"},
        },
    }


class AcceptanceContractTests(unittest.TestCase):
    def test_valid_pass_requires_each_hard_criterion_evidence(self) -> None:
        self.assertEqual(validate_contract(valid_contract()), [])

    def test_partial_completion_cannot_pass(self) -> None:
        contract = valid_contract()
        contract["criteria"][1]["state"] = "UNSATISFIED"
        contract["criteria"][1]["evidence_ids"] = []
        self.assertIn(
            "pass_with_unsatisfied_hard_criterion:C2",
            validate_contract(contract),
        )

    def test_satisfied_without_evidence_is_rejected(self) -> None:
        contract = valid_contract()
        contract["criteria"][0]["evidence_ids"] = []
        self.assertIn("satisfied_without_evidence:C1", validate_contract(contract))

    def test_satisfied_with_unresolved_evidence_is_rejected(self) -> None:
        contract = valid_contract()
        contract["criteria"][0]["evidence_ids"] = ["MISSING"]
        self.assertIn("evidence_unresolved:C1:MISSING", validate_contract(contract))

    def test_satisfied_with_failed_evidence_is_rejected(self) -> None:
        contract = valid_contract()
        contract["evidence_index"]["E1"]["result"] = "FAIL"
        self.assertIn(
            "satisfied_with_nonpass_evidence:C1:E1",
            validate_contract(contract),
        )


if __name__ == "__main__":
    unittest.main()
