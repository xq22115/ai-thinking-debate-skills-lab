import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "planner", ROOT / "scripts/check_write_plan_conflicts.py"
)
planner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(planner)

BASE = "a" * 40


def plan(actor, write_set, *, branch=None, depends_on=None, base_sha=BASE):
    return {
        "schema_version": 1,
        "issue_number": 27,
        "run_id": "run-1",
        "actor_id": actor,
        "branch": branch or f"chat/27/{actor}",
        "base_sha": base_sha,
        "read_set": [],
        "write_set": write_set,
        "depends_on": depends_on or [],
        "status": "PROPOSED",
    }


class WritePlanConflictTests(unittest.TestCase):
    def test_write_planning_is_registered_as_a_hard_contract(self):
        registry = json.loads(
            (ROOT / "ai-system/control-plane/registry.json").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(registry["schema_version"], 4)
        self.assertEqual(
            registry["contracts"]["write_plan_schema"],
            "ai-system/control-plane/write-plan.schema.json",
        )
        self.assertEqual(
            registry["contracts"]["write_conflict_checker"],
            "scripts/check_write_plan_conflicts.py",
        )
        self.assertEqual(registry["planning"]["mode"], "two-phase-fanout")
        self.assertTrue(registry["concurrency"]["write_plan_required_before_mutation"])
        self.assertTrue(registry["concurrency"]["write_set_overlap_requires_dependency"])
        self.assertTrue((ROOT / registry["contracts"]["write_plan_schema"]).is_file())
        self.assertTrue((ROOT / registry["contracts"]["write_conflict_checker"]).is_file())

    def test_write_plan_schema_allows_empty_write_set_for_readonly_actor(self):
        schema = json.loads(
            (ROOT / "ai-system/control-plane/write-plan.schema.json").read_text()
        )
        write_set = schema["properties"]["write_set"]
        self.assertLessEqual(write_set.get("minItems", 0), 0)

    def test_empty_write_set_is_parallel_safe_with_writer(self):
        result = planner.evaluate_plans([
            plan("A08", []),
            plan("A07", ["work/A07/**"]),
        ])
        self.assertEqual(result["result"], "PASS", result)
        self.assertTrue(result["parallel_safe"])
        self.assertEqual(result["unresolved_conflicts"], [])

    def test_disjoint_write_sets_are_parallel_safe(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/api/**"]),
            plan("chat-b", ["docs/**"]),
        ])
        self.assertEqual(result["result"], "PASS", result)
        self.assertTrue(result["parallel_safe"])
        self.assertEqual(result["unresolved_conflicts"], [])

    def test_exact_same_path_without_dependency_is_veto(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/app.py"]),
            plan("chat-b", ["src/app.py"]),
        ])
        self.assertEqual(result["result"], "VETO", result)
        self.assertFalse(result["parallel_safe"])
        self.assertEqual(len(result["unresolved_conflicts"]), 1)

    def test_glob_and_literal_overlap_is_veto(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/api/**"]),
            plan("chat-b", ["src/api/routes.py"]),
        ])
        self.assertEqual(result["result"], "VETO", result)
        self.assertEqual(
            result["unresolved_conflicts"][0]["reason"], "write_set_overlap"
        )

    def test_dependency_serializes_an_overlap(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/app.py"]),
            plan("chat-b", ["src/app.py"], depends_on=["chat-a"]),
        ])
        self.assertEqual(result["result"], "PASS", result)
        self.assertFalse(result["parallel_safe"])
        self.assertEqual(len(result["serialized_conflicts"]), 1)
        self.assertEqual(result["unresolved_conflicts"], [])

    def test_dependency_cycle_is_veto(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/a.py"], depends_on=["chat-b"]),
            plan("chat-b", ["src/b.py"], depends_on=["chat-a"]),
        ])
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("dependency_cycle", result["failures"])

    def test_base_sha_mismatch_is_veto(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/a.py"]),
            plan("chat-b", ["src/b.py"], base_sha="b" * 40),
        ])
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("base_sha_mismatch", result["failures"])

    def test_duplicate_branch_is_veto(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["src/a.py"], branch="chat/27/shared"),
            plan("chat-b", ["src/b.py"], branch="chat/27/shared"),
        ])
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("duplicate_branch", result["failures"])

    def test_parent_traversal_path_is_rejected(self):
        result = planner.evaluate_plans([
            plan("chat-a", ["../secrets.txt"]),
            plan("chat-b", ["docs/**"]),
        ])
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(
            any(
                item.startswith("invalid_write_pattern:")
                for item in result["failures"]
            )
        )


if __name__ == "__main__":
    unittest.main()
