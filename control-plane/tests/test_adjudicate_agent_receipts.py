import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "adjudicator", ROOT / "scripts/adjudicate_agent_receipts.py"
)
adjudicator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adjudicator)

ROLES = adjudicator.EXPECTED
RUN_ID = "20260817T064358Z-test"
ISSUE = 27


def reasoning_quality(agent_id: str) -> dict:
    return {
        "task_class": "material",
        "objective_model": f"Validate the declared outcome for {agent_id}",
        "causal_model": f"Observed repository evidence determines whether {agent_id} may pass",
        "high_impact_unknowns": [],
        "evidence_delta": f"Direct evidence for {agent_id} changes the verdict from unknown to supported",
        "stagnation_state": "CLEAR",
        "verification_level": "readback" if agent_id in {"A08", "A10"} else "static",
        "adversarial_check": "Tried a relevant counterexample and found no contradiction in the recorded evidence",
        "research_stop_reason": "decision_saturated",
        "remaining_risks": [],
    }


def make_receipt(agent_id: str, result: str = "PASS") -> dict:
    index = int(agent_id[1:])
    receipt = {
        "schema_version": 3,
        "issue_number": ISSUE,
        "run_id": RUN_ID,
        "agent_id": agent_id,
        "role": ROLES[agent_id],
        "branch": f"agent/{ISSUE}/{agent_id}/{RUN_ID}",
        "claim_id": f"claim-{agent_id}-0001",
        "plan_head_sha": f"{1000 + index:040x}"[-40:],
        "head_sha": f"{index:040x}"[-40:],
        "result": result,
        "independent_agent_execution": result != "NOT_RUN",
        "executor_id": f"executor-{agent_id}",
        "execution_id": f"execution-{agent_id}",
        "evidence_partition": f"partition-{agent_id}",
        "reasoning_quality": reasoning_quality(agent_id),
        "runtime_attestation": {
            "provider": "claude-code",
            "observer": "scripts/local_agent_executor.py",
            "process_instance_id": f"process-instance-{agent_id}",
            "process_id": 5000 + index,
            "spawn_monotonic_ns": 1000000000 + index,
            "backend_session_sha256": f"{2000 + index:064x}"[-64:],
            "stdout_sha256": f"{3000 + index:064x}"[-64:],
            "stderr_sha256": f"{4000 + index:064x}"[-64:],
        },
        "evidence": [
            {
                "kind": "test",
                "reference": f"test-evidence-{agent_id}",
                "result": "PASS",
                "sha": f"{index:040x}"[-40:]
            }
        ]
    }
    if result == "VETO":
        receipt["veto_reason"] = "reproducible counterexample"
    if result == "NOT_RUN":
        receipt["schema_version"] = 1
        for key in [
            "claim_id", "plan_head_sha", "executor_id", "execution_id",
            "evidence_partition", "head_sha", "evidence", "reasoning_quality",
            "runtime_attestation",
        ]:
            receipt.pop(key, None)
    return receipt


def write_receipts(directory: pathlib.Path, overrides=None, omit=None):
    overrides = overrides or {}
    omit = set(omit or [])
    for agent_id in ROLES:
        if agent_id in omit:
            continue
        receipt = make_receipt(agent_id)
        receipt.update(overrides.get(agent_id, {}))
        (directory / f"{agent_id}.json").write_text(
            json.dumps(receipt, ensure_ascii=False), encoding="utf-8"
        )


class ReceiptAdjudicatorTests(unittest.TestCase):
    def test_ten_distinct_pass_receipts_pass(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path)
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(len(result["found_agents"]), 10)

    def test_pass_receipts_require_durable_runtime_attestation(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path)
            a01 = json.loads((path / "A01.json").read_text(encoding="utf-8"))
            a01.pop("runtime_attestation", None)
            (path / "A01.json").write_text(json.dumps(a01), encoding="utf-8")
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(any(item.startswith("missing_runtime_attestation:") for item in result["errors"]))

    def test_legacy_v2_pass_receipts_cannot_adjudicate_pass(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            overrides = {agent_id: {"schema_version": 2} for agent_id in ROLES}
            write_receipts(path, overrides=overrides)
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(any(item.startswith("pass_veto_requires_schema_v3:") for item in result["errors"]))

    def test_receipt_schema_declares_reasoning_quality_binding(self):
        schema = json.loads(
            (ROOT / "ai-system/control-plane/receipt.schema.json").read_text()
        )
        properties = schema["properties"]
        self.assertIn("claim_id", properties)
        self.assertIn("plan_head_sha", properties)
        self.assertIn("reasoning_quality", properties)
        serialized = json.dumps(schema, sort_keys=True)
        self.assertIn('"reasoning_quality"', serialized)
        self.assertIn('"schema_version": {"const": 3}', serialized)

    def test_pass_with_unresolved_high_impact_unknown_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path)
            a04 = json.loads((path / "A04.json").read_text(encoding="utf-8"))
            a04["reasoning_quality"]["high_impact_unknowns"] = ["root cause still ambiguous"]
            (path / "A04.json").write_text(json.dumps(a04), encoding="utf-8")
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("pass_has_high_impact_unknowns:A04", result["errors"])

    def test_verifier_pass_requires_strong_verification_level(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path)
            a08 = json.loads((path / "A08.json").read_text(encoding="utf-8"))
            a08["reasoning_quality"]["verification_level"] = "inspection"
            (path / "A08.json").write_text(json.dumps(a08), encoding="utf-8")
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("pass_weak_verification_level:A08", result["errors"])

    def test_missing_receipt_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path, omit=["A10"])
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "BLOCKED", result)
            self.assertEqual(result["missing_agents"], ["A10"])

    def test_veto_overrides_other_passes(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path, overrides={"A05": {"result": "VETO", "veto_reason": "counterexample"}})
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "VETO", result)
            self.assertEqual(result["vetoes"][0]["agent_id"], "A05")

    def test_duplicate_executor_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path, overrides={"A02": {"executor_id": "executor-A01"}})
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(result["duplicate_executor_ids"])

    def test_duplicate_runtime_process_instance_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            shared = make_receipt("A01")["runtime_attestation"]["process_instance_id"]
            write_receipts(path, overrides={"A02": {"runtime_attestation": {**make_receipt("A02")["runtime_attestation"], "process_instance_id": shared}}})
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(result["duplicate_process_instances"])

    def test_duplicate_runtime_backend_session_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            shared = make_receipt("A01")["runtime_attestation"]["backend_session_sha256"]
            write_receipts(path, overrides={"A02": {"runtime_attestation": {**make_receipt("A02")["runtime_attestation"], "backend_session_sha256": shared}}})
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(result["duplicate_backend_sessions"])

    def test_duplicate_evidence_partition_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path, overrides={"A03": {"evidence_partition": "partition-A01"}})
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(result["duplicate_evidence_partitions"])

    def test_direct_failing_evidence_overrides_pass_vote(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path)
            a08 = json.loads((path / "A08.json").read_text(encoding="utf-8"))
            a08["evidence"].append({"kind": "test", "reference": "negative-test", "result": "FAIL"})
            (path / "A08.json").write_text(json.dumps(a08, ensure_ascii=False), encoding="utf-8")
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "FAIL", result)
            self.assertTrue(result["direct_failures"])

    def test_not_run_blocks_instead_of_becoming_pass(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)
            write_receipts(path)
            (path / "A04.json").write_text(
                json.dumps(make_receipt("A04", "NOT_RUN"), ensure_ascii=False), encoding="utf-8"
            )
            result = adjudicator.adjudicate(path, ISSUE, RUN_ID)
            self.assertEqual(result["result"], "BLOCKED", result)
            self.assertEqual(result["statuses"]["A04"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
