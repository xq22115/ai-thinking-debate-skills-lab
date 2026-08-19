import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "scope", ROOT / "scripts/verify_write_plan_scope.py"
)
scope = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scope)


def plan(write_set):
    return {
        "schema_version": 1,
        "issue_number": 27,
        "run_id": "run-1",
        "actor_id": "chat-a",
        "branch": "chat/27/chat-a",
        "base_sha": "a" * 40,
        "write_set": write_set,
        "depends_on": [],
        "status": "APPROVED",
    }


class WritePlanScopeTests(unittest.TestCase):
    def test_actual_diff_inside_declared_glob_passes(self):
        result = scope.verify_scope(
            plan(["src/api/**"]),
            ["src/api/routes.py", "src/api/models/user.py"],
        )
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["undeclared_paths"], [])

    def test_actual_diff_outside_declared_scope_is_veto(self):
        result = scope.verify_scope(
            plan(["src/**"]), ["src/app.py", "docs/README.md"]
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertEqual(result["undeclared_paths"], ["docs/README.md"])

    def test_exact_file_declaration_is_enforced(self):
        result = scope.verify_scope(plan(["src/app.py"]), ["src/app.py"])
        self.assertEqual(result["result"], "PASS", result)
        result = scope.verify_scope(plan(["src/app.py"]), ["src/other.py"])
        self.assertEqual(result["result"], "VETO", result)

    def test_multiple_declared_scopes_are_allowed(self):
        result = scope.verify_scope(
            plan(["src/**", "tests/**"]), ["src/a.py", "tests/test_a.py"]
        )
        self.assertEqual(result["result"], "PASS", result)

    def test_path_traversal_in_actual_diff_is_veto(self):
        result = scope.verify_scope(plan(["src/**"]), ["../secrets.txt"])
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("../secrets.txt", result["invalid_changed_paths"])

    def test_empty_write_set_accepts_only_empty_actual_diff(self):
        readonly = plan([])
        self.assertEqual(scope.verify_scope(readonly, [])["result"], "PASS")
        veto = scope.verify_scope(readonly, ["docs/changed.md"])
        self.assertEqual(veto["result"], "VETO", veto)
        self.assertEqual(veto["undeclared_paths"], ["docs/changed.md"])

    def test_empty_actual_diff_is_pass(self):
        result = scope.verify_scope(plan(["src/**"]), [])
        self.assertEqual(result["result"], "PASS", result)


if __name__ == "__main__":
    unittest.main()
