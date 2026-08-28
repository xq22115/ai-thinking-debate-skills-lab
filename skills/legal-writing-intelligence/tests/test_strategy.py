import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STRATEGY_PATH = ROOT / "src" / "strategy.py"
SPEC = importlib.util.spec_from_file_location("legal_writing_strategy", STRATEGY_PATH)
strategy = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(strategy)


class StrategyPreflightTests(unittest.TestCase):
    def base_payload(self):
        return {
            "matter": "Project Falcon — executive decision",
            "purpose": "Obtain written confirmation of the agreed recovery action.",
            "mode": "executive-counsel",
            "facts": ["The steering committee deferred the decision on August 27, 2026."],
            "asks": ["Confirm the accountable executive and approved recovery action."],
            "deadline": "August 29, 2026 at 5:00 p.m.",
            "timezone": "New York time",
        }

    def codes(self, result):
        return {item["code"] for item in result["risk_flags"]}

    def test_clean_executive_payload_is_ready(self):
        result = strategy.analyze(self.base_payload())
        self.assertEqual("READY", result["status"])
        self.assertEqual(1, result["firmness_level"])
        self.assertEqual(1, result["architecture"]["record_items"])
        self.assertIn("confirm-by", {x["id"] for x in result["signal_recommendations"]})

    def test_reservation_requires_scope(self):
        payload = self.base_payload()
        payload["reserve_rights"] = True
        result = strategy.analyze(payload)
        self.assertEqual("REVISE", result["status"])
        self.assertIn("UNSCOPED_RESERVATION", self.codes(result))

    def test_event_does_not_prove_causation(self):
        payload = self.base_payload()
        payload["mode"] = "project-escalation"
        payload["project_claim"] = {
            "event": "Late IFC drawing issued August 20.",
            "mechanism": "Drawing release/interface dependency under the governing contract.",
            "notice_record": "Notice N-104 and daily records.",
            "schedule_effect": "Activity E-410 is said to affect the critical path.",
            "mitigation": "Resequencing options were reviewed.",
            "instruction_requested": "Confirm revised release sequence.",
        }
        result = strategy.analyze(payload)
        codes = self.codes(result)
        self.assertEqual("REVISE", result["status"])
        self.assertIn("EVENT_IS_NOT_CAUSATION", codes)
        self.assertIn("SCHEDULE_EFFECT_WITHOUT_CAUSATION", codes)
        self.assertIn("PROJECT_CAUSATION_MISSING", codes)

    def test_complete_project_chain_can_be_ready(self):
        payload = self.base_payload()
        payload["mode"] = "project-escalation"
        payload["project_claim"] = {
            "event": "Late IFC drawing issued August 20.",
            "mechanism": "Drawing release/interface dependency under the governing contract.",
            "notice_record": "Notice N-104 and contemporaneous daily records.",
            "causation": "The drawing prevented release of fabrication package FP-12, whose successor installation activity had no available float in the current accepted schedule.",
            "schedule_effect": "The current schedule analysis identifies a five-day effect to milestone M4, subject to ongoing update.",
            "mitigation": "The team resequenced unaffected fabrication and added a second review shift.",
            "instruction_requested": "Confirm the revised IFC release sequence and responsible owner.",
        }
        result = strategy.analyze(payload)
        self.assertEqual("READY", result["status"])
        self.assertNotIn("EVENT_IS_NOT_CAUSATION", self.codes(result))

    def test_money_claim_requires_quantum_bridge(self):
        payload = self.base_payload()
        payload["mode"] = "project-escalation"
        payload["project_claim"] = {
            "event": "Late access to Area C.",
            "mechanism": "Access dependency under the project plan.",
            "notice_record": "Daily reports and Notice N-88.",
            "causation": "The unavailable area prevented planned civil works during the stated period.",
            "schedule_effect": "The current analysis identifies impact to activity C-220.",
            "mitigation": "Crews were reassigned where practical.",
            "instruction_requested": "Confirm access date.",
            "seeks_money": True,
        }
        result = strategy.analyze(payload)
        self.assertIn("PROJECT_QUANTUM_GAP", self.codes(result))
        self.assertEqual("REVISE", result["status"])

    def test_privilege_label_is_not_magic(self):
        payload = self.base_payload()
        payload["privilege"] = {
            "label_privileged": True,
            "legal_advice_purpose": False,
            "third_party_recipients": ["commercial consultant"],
        }
        result = strategy.analyze(payload)
        codes = self.codes(result)
        self.assertIn("PRIVILEGE_LABEL_WITHOUT_LEGAL_PURPOSE", codes)
        self.assertIn("PRIVILEGE_DISTRIBUTION_RISK", codes)
        self.assertIn("PRIVILEGE_JURISDICTION_CHECK", codes)

    def test_settlement_label_requires_real_context(self):
        payload = self.base_payload()
        payload["settlement"] = {
            "rule_408_label": True,
            "disputed_claim": False,
            "compromise_purpose": False,
        }
        result = strategy.analyze(payload)
        codes = self.codes(result)
        self.assertIn("SETTLEMENT_LABEL_WITHOUT_DISPUTED_CLAIM", codes)
        self.assertIn("SETTLEMENT_CONTEXT_UNCLEAR", codes)
        self.assertIn("SETTLEMENT_EFFECT_NOT_GUARANTEED", codes)

    def test_package_deal_requires_dependency(self):
        payload = self.base_payload()
        payload["mode"] = "deal-negotiation"
        payload["trade_space"] = ["Price", "indemnity cap"]
        payload["deal"] = {
            "agreed": ["Governing law"],
            "open": ["Price", "indemnity cap"],
            "risk_allocation": "The remaining issue is allocation of uncapped third-party exposure.",
            "trade_space": ["Price", "indemnity cap"],
            "package_proposal": True,
        }
        result = strategy.analyze(payload)
        self.assertIn("PACKAGE_DEPENDENCY_UNSTATED", self.codes(result))
        self.assertEqual("REVISE", result["status"])

    def test_signal_library_has_unique_machine_readable_contract(self):
        data = json.loads((ROOT / "resources" / "signals.json").read_text(encoding="utf-8"))
        signals = data["signals"]
        ids = [item["id"] for item in signals]
        self.assertGreaterEqual(len(signals), 12)
        self.assertEqual(len(ids), len(set(ids)))
        for item in signals:
            self.assertTrue(item["template"])
            self.assertTrue(item["function"])
            self.assertTrue(item["preconditions"])
            self.assertTrue(item["misuse"])


if __name__ == "__main__":
    unittest.main()
