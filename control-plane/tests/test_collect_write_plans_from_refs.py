import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "collector", ROOT / "scripts/collect_write_plans_from_refs.py"
)
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)

ISSUE = 27
RUN_ID = "20260817T160000Z-test"
BASE_SHA = "a" * 40


def git(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_out(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


def write_claim(repo, actor, branch, *, actor_override=None, branch_override=None):
    path = (
        repo / "ai-system/control-plane/runs" / str(ISSUE) / RUN_ID
        / "claims" / f"{actor}.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1, "issue_number": ISSUE, "run_id": RUN_ID,
        "actor_id": actor_override or actor, "branch": branch_override or branch,
        "base_sha": BASE_SHA, "claim_id": f"claim-{actor}-0001",
        "executor_id": f"executor-{actor}", "execution_id": f"execution-{actor}",
        "status": "CLAIMED",
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", f"claim {actor}")


def write_plan(repo, actor, branch, *, actor_override=None, branch_override=None):
    path = (
        repo
        / "ai-system/control-plane/runs"
        / str(ISSUE)
        / RUN_ID
        / "plans"
        / f"{actor}.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "issue_number": ISSUE,
        "run_id": RUN_ID,
        "actor_id": actor_override or actor,
        "branch": branch_override or branch,
        "base_sha": BASE_SHA,
        "read_set": [],
        "write_set": [f"work/{actor}/**"],
        "depends_on": [],
        "status": "PROPOSED",
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", f"plan {actor}")


class CollectWritePlansFromRefsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.temp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test")
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-m", "base")

    def tearDown(self):
        self.temp.cleanup()

    def _branch_with_plan(
        self, actor, *, actor_override=None, branch_override=None, claim=True,
        claim_actor_override=None, claim_branch_override=None,
    ):
        branch = f"agent/{ISSUE}/{actor}/{RUN_ID}"
        git(self.repo, "switch", "main")
        git(self.repo, "switch", "-c", branch)
        if claim:
            write_claim(
                self.repo, actor, branch, actor_override=claim_actor_override,
                branch_override=claim_branch_override,
            )
        write_plan(
            self.repo, actor, branch, actor_override=actor_override,
            branch_override=branch_override,
        )
        return branch

    def test_collects_two_isolated_branch_plans_without_merging_branches(self):
        a01 = self._branch_with_plan("A01")
        a02 = self._branch_with_plan("A02")
        output = pathlib.Path(self.temp.name) / "collected"
        result = collector.collect_plans(
            self.repo, {"A01": a01, "A02": a02}, ISSUE, RUN_ID, output
        )
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["collected"], ["A01", "A02"])
        self.assertTrue((output / "A01.json").is_file())
        self.assertTrue((output / "A02.json").is_file())

    def test_missing_plan_on_ref_is_veto(self):
        a01 = self._branch_with_plan("A01")
        result = collector.collect_plans(
            self.repo,
            {"A01": a01, "A02": "main"},
            ISSUE,
            RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(any(item.startswith("plan_missing:A02:") for item in result["errors"]))

    def test_plan_actor_mismatch_is_veto(self):
        a01 = self._branch_with_plan("A01", actor_override="A02")
        result = collector.collect_plans(
            self.repo,
            {"A01": a01},
            ISSUE,
            RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(any(item.startswith("actor_mismatch:A01:") for item in result["errors"]))

    def test_plan_branch_mismatch_is_veto(self):
        a01 = self._branch_with_plan("A01", branch_override="agent/27/A01/wrong")
        result = collector.collect_plans(
            self.repo,
            {"A01": a01},
            ISSUE,
            RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(any(item.startswith("branch_mismatch:A01:") for item in result["errors"]))

    def test_duplicate_ref_is_veto(self):
        a01 = self._branch_with_plan("A01")
        result = collector.collect_plans(
            self.repo,
            {"A01": a01, "A02": a01},
            ISSUE,
            RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("duplicate_ref", result["errors"])

    def test_invalid_ref_is_veto(self):
        result = collector.collect_plans(
            self.repo,
            {"A01": "../../escape"},
            ISSUE,
            RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(any(item.startswith("invalid_ref:A01:") for item in result["errors"]))

    def test_snapshot_records_resolved_sha_plan_and_claim_hashes(self):
        a01 = self._branch_with_plan("A01")
        approved_head = git_out(self.repo, "rev-parse", a01)
        result = collector.collect_plans(
            self.repo, {"A01": a01}, ISSUE, RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "PASS", result)
        snap = result["snapshots"]["A01"]
        self.assertEqual(snap["branch"], a01)
        self.assertEqual(snap["plan_head_sha"], approved_head)
        self.assertEqual(len(snap["plan_sha256"]), 64)
        self.assertEqual(len(snap["claim_sha256"]), 64)
        self.assertEqual(snap["claim_id"], "claim-A01-0001")
        self.assertEqual(snap["executor_id"], "executor-A01")
        self.assertEqual(snap["execution_id"], "execution-A01")

    def test_missing_claim_on_plan_ref_is_veto(self):
        a01 = self._branch_with_plan("A01", claim=False)
        result = collector.collect_plans(
            self.repo, {"A01": a01}, ISSUE, RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(any(item.startswith("claim_missing:A01:") for item in result["errors"]))

    def test_claim_actor_mismatch_is_veto(self):
        a01 = self._branch_with_plan("A01", claim_actor_override="A02")
        result = collector.collect_plans(
            self.repo, {"A01": a01}, ISSUE, RUN_ID,
            pathlib.Path(self.temp.name) / "out",
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertTrue(any(item.startswith("claim_actor_mismatch:A01:") for item in result["errors"]))

    def test_ref_move_after_resolution_does_not_change_approved_snapshot(self):
        a01 = self._branch_with_plan("A01")
        approved_head = git_out(self.repo, "rev-parse", a01)
        original = collector._resolve_ref
        moved = {"done": False}

        def resolve_then_move(repo, ref):
            sha, error = original(repo, ref)
            if ref == a01 and not moved["done"]:
                moved["done"] = True
                (self.repo / "after-plan.txt").write_text("drift\n", encoding="utf-8")
                git(self.repo, "add", "after-plan.txt")
                git(self.repo, "commit", "-m", "advance after resolve")
            return sha, error

        collector._resolve_ref = resolve_then_move
        try:
            result = collector.collect_plans(
                self.repo, {"A01": a01}, ISSUE, RUN_ID,
                pathlib.Path(self.temp.name) / "out",
            )
        finally:
            collector._resolve_ref = original
        self.assertEqual(result["result"], "PASS", result)
        self.assertNotEqual(git_out(self.repo, "rev-parse", a01), approved_head)
        self.assertEqual(result["snapshots"]["A01"]["plan_head_sha"], approved_head)


if __name__ == "__main__":
    unittest.main()
