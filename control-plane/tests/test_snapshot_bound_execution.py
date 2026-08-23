import hashlib
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "snapshot_verifier", ROOT / "scripts/verify_snapshot_bound_execution.py"
)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)

ISSUE = 27
RUN_ID = "20260817T190000Z-snapshot"
ACTOR = "A07"
BRANCH = f"agent/{ISSUE}/{ACTOR}/{RUN_ID}"
BASE_SHA_FIELD = "a" * 40


def git(repo, *args, capture=False):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], check=True, text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip() if capture else None


def write_json(repo, relative, payload):
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def commit_all(repo, message):
    git(repo, "add", ".")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD", capture=True)


def reasoning_quality():
    return {
        "task_class": "material",
        "objective_model": "Verify A07 work remains bound to the approved snapshot and declared scope",
        "causal_model": "Plan/claim identity plus work-head ancestry, receipt-only final commit, and scope evidence determine whether the execution is authentic",
        "high_impact_unknowns": [],
        "evidence_delta": "Snapshot, ancestry, identity, and changed-path evidence resolve the execution verdict",
        "stagnation_state": "CLEAR",
        "verification_level": "readback",
        "adversarial_check": "Receipt rewriting, foreign paths, stale snapshots, and smuggled post-work changes are exercised by negative tests",
        "research_stop_reason": "decision_saturated",
        "remaining_risks": [],
    }


class SnapshotBoundExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.temp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test")
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")
        self.base_commit = commit_all(self.repo, "base")
        git(self.repo, "switch", "-c", BRANCH)
        self.claim_path = (
            f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/claims/{ACTOR}.json"
        )
        self.plan_path = (
            f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/plans/{ACTOR}.json"
        )
        self.receipt_path = (
            f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/receipts/{ACTOR}.json"
        )
        self.claim = {
            "schema_version": 1, "issue_number": ISSUE, "run_id": RUN_ID,
            "actor_id": ACTOR, "branch": BRANCH, "base_sha": BASE_SHA_FIELD,
            "claim_id": "claim-A07-0001", "executor_id": "executor-A07",
            "execution_id": "execution-A07", "status": "CLAIMED",
        }
        write_json(self.repo, self.claim_path, self.claim)
        commit_all(self.repo, "claim")
        self.plan = {
            "schema_version": 1, "issue_number": ISSUE, "run_id": RUN_ID,
            "actor_id": ACTOR, "branch": BRANCH, "base_sha": BASE_SHA_FIELD,
            "read_set": [], "write_set": ["work/A07/**"],
            "depends_on": [], "status": "PROPOSED",
        }
        write_json(self.repo, self.plan_path, self.plan)
        self.plan_head = commit_all(self.repo, "plan")
        self.snapshot = self._snapshot()

    def tearDown(self):
        self.temp.cleanup()

    def _show(self, revision, path):
        return git(self.repo, "show", f"{revision}:{path}", capture=True)

    def _snapshot(self):
        plan_text = self._show(self.plan_head, self.plan_path)
        claim_text = self._show(self.plan_head, self.claim_path)
        return {
            "branch": BRANCH,
            "plan_head_sha": self.plan_head,
            "plan_sha256": hashlib.sha256(plan_text.encode()).hexdigest(),
            "claim_sha256": hashlib.sha256(claim_text.encode()).hexdigest(),
            "claim_id": self.claim["claim_id"],
            "executor_id": self.claim["executor_id"],
            "execution_id": self.claim["execution_id"],
        }

    def _work_commit(self, relative="work/A07/file.txt", content="ok\n"):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return commit_all(self.repo, f"change {relative}")

    def _verify(self, final_head):
        return verifier.verify_execution(
            self.repo, ISSUE, RUN_ID, ACTOR, self.snapshot, final_head
        )

    def _receipt(self, work_head, **overrides):
        payload = {
            "schema_version": 3,
            "issue_number": ISSUE,
            "run_id": RUN_ID,
            "agent_id": ACTOR,
            "role": "實作代理",
            "branch": BRANCH,
            "claim_id": self.claim["claim_id"],
            "plan_head_sha": self.plan_head,
            "head_sha": work_head,
            "result": "PASS",
            "independent_agent_execution": True,
            "executor_id": self.claim["executor_id"],
            "execution_id": self.claim["execution_id"],
            "evidence_partition": "partition-A07",
            "reasoning_quality": reasoning_quality(),
            "runtime_attestation": {
                "provider": "claude-code",
                "observer": "scripts/local_agent_executor.py",
                "process_instance_id": "process-instance-A07",
                "process_id": 7007,
                "spawn_monotonic_ns": 123456789,
                "backend_session_sha256": "a" * 64,
                "stdout_sha256": "b" * 64,
                "stderr_sha256": "c" * 64,
            },
            "evidence": [{
                "kind": "test", "reference": "snapshot-bound-test",
                "result": "PASS", "sha": work_head,
            }],
        }
        payload.update(overrides)
        return payload

    def _commit_receipt(self, work_head, **overrides):
        write_json(self.repo, self.receipt_path, self._receipt(work_head, **overrides))
        return commit_all(self.repo, "receipt")

    def test_valid_descendant_with_bound_receipt_passes(self):
        work_head = self._work_commit()
        final_head = self._commit_receipt(work_head)
        result = self._verify(final_head)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["undeclared_paths"], [])
        self.assertEqual(result["work_head_sha"], work_head)
        self.assertTrue(result["receipt_identity_bound"])

    def test_receipt_executor_mismatch_is_veto(self):
        work_head = self._work_commit()
        final_head = self._commit_receipt(work_head, executor_id="executor-A08")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("receipt_executor_id_mismatch", result["failures"])

    def test_receipt_claim_mismatch_is_veto(self):
        work_head = self._work_commit()
        final_head = self._commit_receipt(work_head, claim_id="claim-other")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("receipt_claim_id_mismatch", result["failures"])

    def test_receipt_plan_head_mismatch_is_veto(self):
        work_head = self._work_commit()
        final_head = self._commit_receipt(work_head, plan_head_sha=self.base_commit)
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("receipt_plan_head_sha_mismatch", result["failures"])

    def test_receipt_evidence_cannot_be_rewritten_by_second_receipt_only_commit(self):
        work_head = self._work_commit()
        first_receipt_head = self._commit_receipt(work_head)
        changed = self._receipt(work_head)
        changed["evidence"][0]["reference"] = "rewritten-evidence"
        write_json(self.repo, self.receipt_path, changed)
        second_receipt_head = commit_all(self.repo, "rewrite receipt evidence")
        result = self._verify(second_receipt_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("receipt_commit_not_immediate_child_of_work_head", result["failures"])
        self.assertNotEqual(first_receipt_head, second_receipt_head)

    def test_receipt_commit_cannot_smuggle_additional_task_change(self):
        work_head = self._work_commit()
        write_json(self.repo, self.receipt_path, self._receipt(work_head))
        extra = self.repo / "work/A07/after-work.txt"
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("smuggled\n", encoding="utf-8")
        final_head = commit_all(self.repo, "receipt plus extra change")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("post_work_diff_not_receipt_only", result["failures"])

    def test_branch_advanced_after_evidence_is_veto(self):
        final_head = self._work_commit()
        self._work_commit("work/A07/later.txt", "later\n")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("final_head_not_current_branch_head", result["failures"])

    def test_non_descendant_final_head_is_veto(self):
        git(self.repo, "switch", "main")
        unrelated = self._work_commit("unrelated.txt", "other\n")
        git(self.repo, "branch", "-f", BRANCH, unrelated)
        result = self._verify(unrelated)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("plan_snapshot_not_ancestor", result["failures"])

    def test_plan_rewrite_after_preflight_is_veto(self):
        changed = dict(self.plan)
        changed["write_set"] = ["**"]
        write_json(self.repo, self.plan_path, changed)
        final_head = commit_all(self.repo, "rewrite plan")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("plan_snapshot_changed", result["failures"])

    def test_claim_rewrite_after_preflight_is_veto(self):
        changed = dict(self.claim)
        changed["executor_id"] = "other-executor"
        write_json(self.repo, self.claim_path, changed)
        final_head = commit_all(self.repo, "rewrite claim")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("claim_snapshot_changed", result["failures"])

    def test_undeclared_task_path_is_veto(self):
        final_head = self._work_commit("outside.txt", "no\n")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("outside.txt", result["undeclared_paths"])

    def test_foreign_receipt_path_is_not_an_exception(self):
        foreign = (
            f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/receipts/A08.json"
        )
        final_head = self._work_commit(foreign, "{}\n")
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn(foreign, result["undeclared_paths"])

    def test_old_snapshot_cannot_be_replayed_after_new_plan(self):
        changed = dict(self.plan)
        changed["read_set"] = ["README.md"]
        write_json(self.repo, self.plan_path, changed)
        commit_all(self.repo, "new approved-looking plan")
        final_head = self._work_commit()
        result = self._verify(final_head)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("plan_snapshot_changed", result["failures"])


if __name__ == "__main__":
    unittest.main()
