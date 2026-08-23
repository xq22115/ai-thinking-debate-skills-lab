import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
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
        self.assertEqual(validator.validate(self.load_config())["result"], "PASS")

    def test_global_policy_is_context_first(self):
        text = (REPO_ROOT / "docs/CAPABILITY_ACCESS_AND_FLEXIBILITY_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("Context over keywords", text)
        self.assertIn("Goal-preserving transformation", text)
        self.assertIn("Machine-enforced routing contract", text)

    def test_keyword_only_blocking_is_fail_closed(self):
        payload = self.load_config()
        payload["invariants"]["keyword_only_blocking"] = True
        result = validator.validate(payload)
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("keyword_only_blocking_must_be_false", result["failures"])

    def test_partial_refusal_must_preserve_allowed_scope(self):
        payload = self.load_config()
        payload["response_policy"]["mixed_request"] = "refuse_entire_request"
        result = validator.validate(payload)
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("mixed_request_must_preserve_allowed_scope", result["failures"])

    def test_platform_boundary_cannot_be_removed(self):
        payload = self.load_config()
        payload["non_override_boundaries"].remove("host_or_platform_safety_enforcement")
        result = validator.validate(payload)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any(item.startswith("missing_non_override_boundaries:") for item in result["failures"]))

    def test_legitimate_sensitive_contexts_are_preserved(self):
        contexts = set(self.load_config()["benign_contexts_to_preserve"])
        expected = {
            "analysis", "translation", "summarization", "quotation", "fiction",
            "historical_discussion", "legal_or_policy_analysis", "research",
            "defensive_security", "harm_prevention",
        }
        self.assertTrue(expected.issubset(contexts))

    def test_evasion_mode_is_not_enabled(self):
        payload = self.load_config()
        self.assertTrue(payload["invariants"]["do_not_attempt_safety_bypass_or_filter_evasion"])
        self.assertEqual(validator.validate(payload)["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
