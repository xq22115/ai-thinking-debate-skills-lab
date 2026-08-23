import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "capability_router_validator",
    ROOT / "scripts/validate_context_first_capability_router.py",
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

CONFIG = ROOT / "ai-system/configs/context-first-capability-routing.json"


class ContextFirstCapabilityRouterTests(unittest.TestCase):
    def load_config(self):
        return json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_repository_config_passes(self):
        result = validator.validate(self.load_config())
        self.assertEqual(result["result"], "PASS", result)

    def test_keyword_only_blocking_is_fail_closed(self):
        payload = self.load_config()
        payload["invariants"]["keyword_only_blocking"] = True
        result = validator.validate(payload)
        self.assertEqual(result["result"], "FAIL", result)
        self.assertIn("keyword_only_blocking_must_be_false", result["failures"])

    def test_partial_refusal_must_preserve_allowed_scope(self):
        payload = self.load_config()
        payload["response_policy"]["mixed_request"] = "refuse_entire_request"
        result = validator.validate(payload)
        self.assertEqual(result["result"], "FAIL", result)
        self.assertIn("mixed_request_must_preserve_allowed_scope", result["failures"])

    def test_platform_safety_cannot_be_removed_from_boundaries(self):
        payload = self.load_config()
        payload["non_override_boundaries"].remove("host_or_platform_safety_enforcement")
        result = validator.validate(payload)
        self.assertEqual(result["result"], "FAIL", result)
        self.assertTrue(any(item.startswith("missing_non_override_boundaries:") for item in result["failures"]))

    def test_benign_sensitive_contexts_are_explicitly_preserved(self):
        payload = self.load_config()
        expected = {
            "analysis", "translation", "summarization", "quotation", "fiction",
            "historical_discussion", "legal_or_policy_analysis", "research",
            "defensive_security", "harm_prevention",
        }
        self.assertTrue(expected.issubset(set(payload["benign_contexts_to_preserve"])))

    def test_filter_evasion_is_not_enabled(self):
        payload = self.load_config()
        self.assertTrue(payload["invariants"]["do_not_attempt_safety_bypass_or_filter_evasion"])
        result = validator.validate(payload)
        self.assertEqual(result["result"], "PASS", result)


if __name__ == "__main__":
    unittest.main()
