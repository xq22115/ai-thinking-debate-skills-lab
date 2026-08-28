import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "resources" / "strategy-engine.json"


class StrategyEngineContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_entrypoints_exist(self):
        for key in ("entrypoint", "writer_entrypoint", "research_entrypoint"):
            self.assertTrue((ROOT / self.data[key]).is_file(), key)

    def test_fail_closed_release_rule_is_explicit(self):
        self.assertEqual(["READY", "REVISE"], self.data["statuses"])
        self.assertIn("high-severity", self.data["release_rule"])
        self.assertIn("REVISE", self.data["release_rule"])

    def test_project_and_deal_chains_are_not_collapsed(self):
        self.assertIn("causation", self.data["major_project_chain"])
        self.assertIn("schedule_effect", self.data["major_project_chain"])
        self.assertIn("cost_quantum_if_claimed", self.data["major_project_chain"])
        self.assertIn("risk_allocation", self.data["deal_chain"])
        self.assertIn("package_dependency_if_claimed", self.data["deal_chain"])

    def test_strategy_dependencies_exist(self):
        self.assertTrue((ROOT / self.data["signal_library"]).is_file())
        self.assertTrue((ROOT / self.data["authority_ledger"]).is_file())


if __name__ == "__main__":
    unittest.main()
