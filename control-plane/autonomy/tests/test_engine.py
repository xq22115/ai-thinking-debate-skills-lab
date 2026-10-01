import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from control_plane_autonomy_import_shim import engine  # type: ignore


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "control-plane/autonomy/config.json").read_text())

    def candidate(self):
        return {
            "id": "L-001",
            "title": "Cache key mismatch causes stale artifact",
            "fingerprint": "abc123",
            "component": "ci-cache",
            "root_cause": "restore and save keys are not derived from the same dependency set",
            "diagnostic": "compare resolved cache key with lockfile hash",
            "repair": "derive both keys from the lockfile hash",
            "verification": "cold and warm CI runs both pass with expected cache hit behavior",
            "reuse_conditions": ["same cache action and dependency lockfile"],
            "invalidation_conditions": ["cache action semantics change"],
            "evidence": [
                {"source": "run-1", "independent_group": "ci-run-a", "verified": True, "verdict": "support"},
                {"source": "run-2", "independent_group": "ci-run-b", "verified": True, "verdict": "support"},
                {"source": "run-3", "independent_group": "ci-run-c", "verified": True, "verdict": "support"},
            ],
        }

    def test_fingerprint_ignores_volatile_ids_and_numbers(self):
        a = "2026-09-20T10:11:12Z worker 123 failed at 0xABCDEF request 550"
        b = "2026-09-21T20:22:33Z worker 999 failed at 0x123456 request 881"
        self.assertEqual(engine.failure_fingerprint(a), engine.failure_fingerprint(b))

    def test_promotion_requires_independent_verified_evidence(self):
        c = self.candidate()
        c["evidence"] = [
            {"source": "a", "independent_group": "same", "verified": True, "verdict": "support"},
            {"source": "b", "independent_group": "same", "verified": True, "verdict": "support"},
        ]
        result = engine.score_candidate(c, self.config)
        self.assertFalse(result["promotable"])
        self.assertIn("insufficient_independent_groups", result["reasons"])

    def test_candidate_promotes_with_three_clean_independent_supports(self):
        result = engine.score_candidate(self.candidate(), self.config)
        self.assertTrue(result["promotable"])
        self.assertGreaterEqual(result["confidence"], 0.75)

    def test_direct_contradiction_blocks_promotion(self):
        c = self.candidate()
        c["evidence"].append(
            {"source": "counter", "independent_group": "counter-env", "verified": True, "verdict": "contradict"}
        )
        result = engine.score_candidate(c, self.config)
        self.assertFalse(result["promotable"])
        self.assertIn("contradiction_ratio_too_high", result["reasons"])

    def test_exact_fingerprint_ranks_first(self):
        lessons = [
            dict(self.candidate(), status="active", confidence=0.8),
            dict(self.candidate(), id="L-002", fingerprint="other", status="active", confidence=0.95),
        ]
        ranked = engine.query_lessons(lessons, fingerprint="abc123")
        self.assertEqual(ranked[0]["id"], "L-001")

    def test_two_strike_rule_requires_pivot(self):
        state = {
            "attempts": [
                {"mechanism": "retry-network", "outcome": "fail"},
                {"mechanism": "retry-network", "outcome": "fail"},
            ]
        }
        result = engine.next_strategy(state, self.config)
        self.assertTrue(result["pivot_required"])
        self.assertEqual(result["reason"], "two_strike_rule")


if __name__ == "__main__":
    unittest.main()
