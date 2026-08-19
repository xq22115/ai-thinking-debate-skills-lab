import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_agent_core_admin.py"

spec = importlib.util.spec_from_file_location("agent_core_admin", SCRIPT)
admin = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(admin)


class AgentCoreAdminConvergenceTests(unittest.TestCase):
    def test_repository_settings_contract(self):
        self.assertEqual(
            admin.DESIRED_REPOSITORY_SETTINGS,
            {
                "allow_auto_merge": True,
                "allow_merge_commit": False,
                "allow_squash_merge": True,
                "allow_rebase_merge": True,
                "allow_update_branch": True,
            },
        )

    def test_new_ruleset_contract_has_single_merge_readiness_check(self):
        payload = admin.build_ruleset_payload(None)
        self.assertEqual(payload["name"], "protect-main")
        self.assertEqual(payload["target"], "branch")
        self.assertEqual(payload["enforcement"], "active")
        self.assertEqual(payload["conditions"]["ref_name"]["include"], ["~DEFAULT_BRANCH"])
        rule_types = [rule["type"] for rule in payload["rules"]]
        for required in ["deletion", "non_fast_forward", "required_linear_history", "pull_request", "required_status_checks"]:
            self.assertIn(required, rule_types)
        status = next(rule for rule in payload["rules"] if rule["type"] == "required_status_checks")
        self.assertEqual(
            status["parameters"]["required_status_checks"],
            [{"context": "Merge Readiness", "integration_id": 15368}],
        )
        self.assertFalse(status["parameters"]["strict_required_status_checks_policy"])
        self.assertTrue(status["parameters"]["do_not_enforce_on_create"])

    def test_existing_ruleset_preserves_non_status_rules_and_bypass(self):
        current = {
            "name": "protect-main",
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "bypass_actors": [{"actor_id": None, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}],
            "rules": [
                {"type": "deletion"},
                {"type": "non_fast_forward"},
                {"type": "required_linear_history"},
                {"type": "pull_request", "parameters": {"required_approving_review_count": 0, "required_review_thread_resolution": True, "dismiss_stale_reviews_on_push": False, "require_code_owner_review": False, "require_last_push_approval": False, "allowed_merge_methods": ["squash", "rebase"]}},
                {"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": False, "do_not_enforce_on_create": True, "required_status_checks": [{"context": "old-check", "integration_id": 15368}]}},
            ],
        }
        payload = admin.build_ruleset_payload(current)
        self.assertEqual(payload["bypass_actors"], current["bypass_actors"])
        before = [r for r in current["rules"] if r["type"] != "required_status_checks"]
        after = [r for r in payload["rules"] if r["type"] != "required_status_checks"]
        self.assertEqual(after, before)
        self.assertTrue(admin.verify_ruleset(payload)[0])

    def test_repository_verifier_rejects_demo_current_state(self):
        ok, diff = admin.verify_repository_settings({
            "allow_auto_merge": False,
            "allow_merge_commit": True,
            "allow_squash_merge": True,
            "allow_rebase_merge": True,
            "allow_update_branch": False,
        })
        self.assertFalse(ok)
        self.assertEqual(set(diff), {"allow_auto_merge", "allow_merge_commit", "allow_update_branch"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
