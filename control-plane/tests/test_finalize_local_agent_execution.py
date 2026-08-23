import hashlib
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "finalizer", ROOT / "scripts/finalize_local_agent_execution.py"
)
finalizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(finalizer)

ISSUE = 27
RUN_ID = "run-finalize"
BASE_FIELD = "a" * 40


def git(repo, *args, capture=False, check=True):
    cp = subprocess.run(
        ["git", "-C", str(repo), *args], text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE, check=check,
    )
    return cp.stdout.strip() if capture else cp.returncode


def write_json(repo, relative, payload):
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def commit_all(repo, message):
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD", capture=True)


def reasoning_quality(actor):
    return {
        "task_class": "material",
        "objective_model": f"verify outcome for {actor}",
        "causal_model": f"exact-state evidence determines whether {actor} may pass",
        "high_impact_unknowns": [],
        "evidence_delta": f"direct evidence resolved the decision for {actor}",
        "stagnation_state": "CLEAR",
        "verification_level": "readback" if actor in {"A08", "A10"} else "static",
        "adversarial_check": "relevant counterexample attempted without contradiction",
        "research_stop_reason": "decision_saturated",
        "remaining_risks": [],
    }


class FinalizeLocalExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.temp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "user.email", "test@example.com")
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")
        commit_all(self.repo, "base")

    def tearDown(self):
        self.temp.cleanup()

    def prepare_actor(self, actor, write_set):
        branch = f"agent/{ISSUE}/{actor}/{RUN_ID}"
        git(self.repo, "switch", "-c", branch)
        claim_path = f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/claims/{actor}.json"
        plan_path = f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/plans/{actor}.json"
        claim = {
            "schema_version": 1,
            "issue_number": ISSUE,
            "run_id": RUN_ID,
            "actor_id": actor,
            "branch": branch,
            "base_sha": BASE_FIELD,
            "claim_id": f"claim-{actor}",
            "executor_id": f"slot-{actor}",
            "execution_id": f"execution-{actor}",
            "status": "CLAIMED",
        }
        write_json(self.repo, claim_path, claim)
        commit_all(self.repo, "claim")
        plan = {
            "schema_version": 1,
            "issue_number": ISSUE,
            "run_id": RUN_ID,
            "actor_id": actor,
            "branch": branch,
            "base_sha": BASE_FIELD,
            "read_set": [],
            "write_set": write_set,
            "depends_on": [],
            "status": "PROPOSED",
        }
        write_json(self.repo, plan_path, plan)
        plan_head = commit_all(self.repo, "plan")
        plan_text = git(self.repo, "show", f"{plan_head}:{plan_path}", capture=True)
        claim_text = git(self.repo, "show", f"{plan_head}:{claim_path}", capture=True)
        snapshot = {
            "branch": branch,
            "plan_head_sha": plan_head,
            "plan_sha256": hashlib.sha256(plan_text.encode()).hexdigest(),
            "claim_sha256": hashlib.sha256(claim_text.encode()).hexdigest(),
            "claim_id": claim["claim_id"],
            "executor_id": claim["executor_id"],
            "execution_id": claim["execution_id"],
        }
        execution = {
            "schemaVersion": 1,
            "issue_number": ISSUE,
            "run_id": RUN_ID,
            "actor_id": actor,
            "branch": branch,
            "workspace": str(self.repo),
            "claim_id": claim["claim_id"],
            "executor_id": claim["executor_id"],
            "execution_id": claim["execution_id"],
            "plan_head_sha": plan_head,
            "pid": 4242,
            "process_instance_id": f"process-{actor}",
            "spawn_monotonic_ns": 123456789 + int(actor[1:]),
            "exit_code": 0,
            "session_id": f"session-{actor}",
            "decision": {
                "agent_id": actor,
                "decision": "PASS",
                "summary": "verified",
                "evidence": [{"kind": "readback", "reference": f"session-{actor}"}],
                "reasoning_quality": reasoning_quality(actor),
            },
            "stdout_sha256": "b" * 64,
            "stderr_sha256": "c" * 64,
            "failures": [],
        }
        return branch, plan_head, snapshot, execution

    def test_readonly_clean_pass_creates_bound_receipt_commit(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A08", ["docs/**"])
        result = finalizer.finalize_execution(self.repo, "A08", snapshot, execution)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["work_head_sha"], plan_head)
        self.assertNotEqual(result["final_head_sha"], plan_head)
        self.assertEqual(result["snapshot_verification"]["result"], "PASS")
        receipt_path = self.repo / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/receipts/A08.json"
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(receipt["schema_version"], 3)
        self.assertEqual(receipt["claim_id"], "claim-A08")
        self.assertEqual(receipt["plan_head_sha"], plan_head)
        self.assertEqual(receipt["head_sha"], plan_head)
        self.assertEqual(receipt["execution_id"], "execution-A08")
        self.assertEqual(receipt["reasoning_quality"]["high_impact_unknowns"], [])
        self.assertEqual(receipt["reasoning_quality"]["verification_level"], "readback")
        attestation = receipt["runtime_attestation"]
        self.assertEqual(attestation["provider"], "claude-code")
        self.assertEqual(attestation["process_instance_id"], "process-A08")
        self.assertEqual(attestation["process_id"], 4242)
        self.assertGreater(attestation["spawn_monotonic_ns"], 0)
        self.assertEqual(len(attestation["backend_session_sha256"]), 64)
        self.assertNotIn("session-A08", json.dumps(receipt, sort_keys=True))

    def test_pass_with_unresolved_high_impact_unknown_is_veto(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A04", ["docs/**"])
        execution["decision"]["reasoning_quality"]["high_impact_unknowns"] = ["causal ambiguity"]
        result = finalizer.finalize_execution(self.repo, "A04", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("decision_pass_has_high_impact_unknowns", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)

    def test_verifier_pass_with_inspection_only_is_veto(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A08", ["docs/**"])
        execution["decision"]["reasoning_quality"]["verification_level"] = "inspection"
        result = finalizer.finalize_execution(self.repo, "A08", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("decision_pass_weak_verification_level", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)

    def test_readonly_mutation_is_veto_without_receipt_commit(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A08", ["docs/**"])
        path = self.repo / "docs/changed.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("unexpected\n", encoding="utf-8")
        result = finalizer.finalize_execution(self.repo, "A08", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("readonly_workspace_modified", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)

    def test_a07_in_scope_change_commits_work_then_receipt(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A07", ["work/A07/**"])
        path = self.repo / "work/A07/result.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("done\n", encoding="utf-8")
        result = finalizer.finalize_execution(self.repo, "A07", snapshot, execution)
        self.assertEqual(result["result"], "PASS", result)
        work_head = result["work_head_sha"]
        final_head = result["final_head_sha"]
        self.assertNotEqual(work_head, plan_head)
        self.assertNotEqual(final_head, work_head)
        changed_work = git(self.repo, "diff", "--name-only", plan_head, work_head, capture=True).splitlines()
        self.assertEqual(changed_work, ["work/A07/result.txt"])
        changed_receipt = git(self.repo, "diff", "--name-only", work_head, final_head, capture=True).splitlines()
        self.assertEqual(changed_receipt, [f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/receipts/A07.json"])
        self.assertEqual(result["snapshot_verification"]["result"], "PASS")

    def test_a07_out_of_scope_change_is_veto(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A07", ["work/A07/**"])
        (self.repo / "outside.txt").write_text("no\n", encoding="utf-8")
        result = finalizer.finalize_execution(self.repo, "A07", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("write_scope_veto", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)

    def test_execution_identity_mismatch_is_veto(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A08", ["docs/**"])
        execution["executor_id"] = "foreign-slot"
        result = finalizer.finalize_execution(self.repo, "A08", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("executor_id_mismatch", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)

    def test_preexisting_staged_change_is_veto(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A07", ["work/A07/**"])
        path = self.repo / "work/A07/staged.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("staged\n", encoding="utf-8")
        git(self.repo, "add", str(path.relative_to(self.repo)))
        result = finalizer.finalize_execution(self.repo, "A07", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("preexisting_staged_changes", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)

    def test_nonpass_decision_with_dirty_tree_is_veto(self):
        _, plan_head, snapshot, execution = self.prepare_actor("A07", ["work/A07/**"])
        execution["decision"]["decision"] = "VETO"
        execution["decision"]["summary"] = "counterexample"
        path = self.repo / "work/A07/partial.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("partial\n", encoding="utf-8")
        result = finalizer.finalize_execution(self.repo, "A07", snapshot, execution)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("nonpass_workspace_modified", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD", capture=True), plan_head)


if __name__ == "__main__":
    unittest.main()
