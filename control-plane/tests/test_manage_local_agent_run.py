import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "manager", ROOT / "scripts/manage_local_agent_run.py"
)
manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manager)

WF_SPEC = importlib.util.spec_from_file_location(
    "workflow_fixture", ROOT / "tests/test_run_local_agent_workflow.py"
)
wf_fixture = importlib.util.module_from_spec(WF_SPEC)
WF_SPEC.loader.exec_module(wf_fixture)

PREP_SPEC = importlib.util.spec_from_file_location(
    "preparer", ROOT / "scripts/prepare_local_agent_run.py"
)
preparer = importlib.util.module_from_spec(PREP_SPEC)
PREP_SPEC.loader.exec_module(preparer)
ISSUE = 27
RUN_ID = "run-lifecycle"


def git(repo, *args, capture=False, check=True):
    cp = subprocess.run(
        ["git", "-C", str(repo), *args], text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE, check=check,
    )
    return cp.stdout.strip() if capture else cp.returncode


def commit_all(repo, message):
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD", capture=True)


def deterministic_id(kind, actor):
    return f"{kind}-{actor}-lifecycle"


class LifecycleCliSurfaceTests(unittest.TestCase):
    def test_resume_is_exposed_as_first_class_lifecycle_command(self):
        cp = subprocess.run(
            [sys.executable, str(ROOT / "scripts/manage_local_agent_run.py"), "--help"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertIn("resume", cp.stdout)
        resume = subprocess.run(
            [sys.executable, str(ROOT / "scripts/manage_local_agent_run.py"), "resume", "--help"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(resume.returncode, 0, resume.stderr)
        for marker in ["--preparation-json", "--claude-path", "--output-dir", "--max-parallel", "--timeout-seconds", "--max-budget-usd"]:
            self.assertIn(marker, resume.stdout)


class ManageLocalAgentRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "user.email", "test@example.com")
        (self.repo / "AGENTS.md").write_text("# test\n", encoding="utf-8")
        cp = self.repo / "ai-system/control-plane"
        cp.mkdir(parents=True)
        shutil.copy2(ROOT / "ai-system/control-plane/registry.json", cp / "registry.json")
        shutil.copytree(ROOT / "ai-system/control-plane/agents", cp / "agents")
        self.base_sha = commit_all(self.repo, "base")
        git(self.remote.parent, "init", "--bare", str(self.remote))
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "-u", "origin", "main")
        self.workspaces = self.root / "workspaces"
        self.preparation = preparer.prepare_run(
            self.repo, ISSUE, RUN_ID, self.base_sha, "main", self.workspaces,
            plan_config={"A07": {"write_set": ["work/A07/**"]}},
            id_factory=deterministic_id,
        )
        self.assertEqual(self.preparation["result"], "PASS", self.preparation)
        self.fake = self.root / "claude"
        wf_fixture.make_fake_claude(self.fake)
        self.workflow_output = self.root / "workflow-output"
        self.workflow = wf_fixture.workflow.run_workflow(
            self.preparation, self.fake, self.workflow_output,
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
        )
        self.assertEqual(self.workflow["result"], "PASS", self.workflow)

    def tearDown(self):
        self.temp.cleanup()
    def test_resume_cli_needs_no_claude_when_all_receipts_revalidate(self):
        prep_json = self.root / "resume-preparation.json"
        prep_json.write_text(json.dumps(self.preparation), encoding="utf-8")
        output_dir = self.root / "resume-cli-output"
        cp = subprocess.run(
            [
                sys.executable, str(ROOT / "scripts/manage_local_agent_run.py"), "resume",
                "--preparation-json", str(prep_json),
                "--output-dir", str(output_dir),
            ],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        result = json.loads(cp.stdout)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["model_process_count"], 0)
        self.assertEqual(result["resumed_actors"], [f"A{i:02d}" for i in range(1, 11)])
        self.assertEqual(result["backend_probe"]["result"], "NOT_RUN")

    def test_status_reports_finalized_unpublished_run(self):
        status = manager.inspect_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(status["result"], "PASS", status)
        self.assertEqual(status["stage"], "FINALIZED_PASS_UNPUBLISHED")
        self.assertEqual(len(status["actors"]), 10)
        self.assertTrue(all(row["receipt_exists"] for row in status["actors"].values()))
        self.assertTrue(all(row["remote_head"] is None for row in status["actors"].values()))
        self.assertEqual(status["base_freshness"]["result"], "PASS")

    def test_status_invalid_receipt_never_reuses_previous_actor_payload(self):
        actor = "A02"
        assignment = next(row for row in self.preparation["assignments"] if row["actor_id"] == actor)
        workspace = pathlib.Path(assignment["workspace"])
        receipt_path = workspace / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/receipts/{actor}.json"
        receipt_path.write_text("{not-json", encoding="utf-8")
        commit_all(workspace, "corrupt receipt for status negative test")
        status = manager.inspect_run(self.preparation, None, remote="origin")
        self.assertEqual(status["result"], "VETO", status)
        self.assertEqual(status["actors"][actor]["receipt_result"], "INVALID")
        self.assertNotEqual(status["derived_adjudication"].get("result"), "PASS")
        self.assertTrue(any("A02" in failure for failure in status["failures"]), status)

    def test_status_derives_verified_pass_from_git_without_workflow_json(self):
        status = manager.inspect_run(self.preparation, None, remote="origin")
        self.assertEqual(status["result"], "PASS", status)
        self.assertEqual(status["stage"], "FINALIZED_PASS_UNPUBLISHED")
        self.assertEqual(status["derived_adjudication"]["result"], "PASS")
        self.assertEqual(status["base_freshness"]["result"], "PASS")
        self.assertTrue(all(row["snapshot_verification"] == "PASS" for row in status["actors"].values()))
        self.assertTrue(all(row["receipt_result"] == "PASS" for row in status["actors"].values()))

    def test_status_keeps_durable_receipts_after_worktree_cleanup(self):
        published = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(published["result"], "PASS", published)
        cleaned = manager.cleanup_run(self.preparation)
        self.assertEqual(cleaned["result"], "PASS", cleaned)
        status = manager.inspect_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(status["result"], "PASS", status)
        self.assertEqual(status["stage"], "FINALIZED_PASS_PUBLISHED")
        self.assertEqual(status["remote_actor_count"], 10)
        self.assertTrue(all(row["receipt_exists"] for row in status["actors"].values()))
        self.assertTrue(all(row["receipt_source"] == "git-head" for row in status["actors"].values()))
        self.assertTrue(all(not row["workspace_exists"] for row in status["actors"].values()))

    def test_publish_pushes_finalized_actor_branches_and_is_idempotent(self):
        first = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(first["result"], "PASS", first)
        self.assertEqual(len(first["pushed"]), 10)
        self.assertTrue(first["atomic_push_attempted"])
        second = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(second["result"], "PASS", second)
        for actor, finalization in self.workflow["finalizations"].items():
            branch = next(row["branch"] for row in self.preparation["assignments"] if row["actor_id"] == actor)
            remote_head = git(self.remote, "rev-parse", f"refs/heads/{branch}", capture=True)
            self.assertEqual(remote_head, finalization["final_head_sha"])

    def test_actor_publish_divergence_vetoes_before_any_partial_push(self):
        a02_branch = next(row["branch"] for row in self.preparation["assignments"] if row["actor_id"] == "A02")
        diverge = self.root / "diverge-a02"
        git(self.repo, "worktree", "add", "-q", "-b", "tmp-diverge-a02", str(diverge), self.base_sha)
        (diverge / "remote-only.txt").write_text("diverged\n", encoding="utf-8")
        commit_all(diverge, "diverged remote a02")
        git(diverge, "push", "origin", f"HEAD:refs/heads/{a02_branch}")
        result = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(result["result"], "VETO", result)
        self.assertFalse(result["atomic_push_attempted"])
        self.assertIn("remote_not_fast_forward:A02", result["failures"])
        a01_branch = next(row["branch"] for row in self.preparation["assignments"] if row["actor_id"] == "A01")
        self.assertIsNone(manager._remote_head(self.repo, "origin", a01_branch))

    def test_integrate_requires_complete_workflow_pass(self):
        bad = json.loads(json.dumps(self.workflow))
        bad["result"] = "VETO"
        result = manager.integrate_run(self.preparation, bad)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("workflow_not_pass", result["failures"])
        self.assertEqual(git(self.repo, "rev-parse", self.preparation["integration_branch"], capture=True), self.base_sha)
    def test_integrate_merges_all_actor_evidence_and_re_adjudicates(self):
        result = manager.integrate_run(self.preparation, self.workflow)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["adjudication"]["result"], "PASS")
        self.assertEqual(result["base_freshness"]["result"], "PASS")
        self.assertEqual(len(result["merged_actor_heads"]), 10)
        integration = pathlib.Path(result["integration_workspace"])
        for actor in [f"A{i:02d}" for i in range(1, 11)]:
            receipt = integration / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/receipts/{actor}.json"
            self.assertTrue(receipt.is_file(), actor)
        self.assertTrue((integration / "work/A07/result.txt").is_file())
        integration_receipt = integration / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/integration.json"
        self.assertTrue(integration_receipt.is_file())
        self.assertEqual(git(integration, "status", "--porcelain", capture=True), "")

    def test_publish_integration_is_fast_forward_only_and_idempotent(self):
        integration = manager.integrate_run(self.preparation, self.workflow)
        self.assertEqual(integration["result"], "PASS", integration)
        first = manager.publish_integration(self.preparation, integration, remote="origin")
        self.assertEqual(first["result"], "PASS", first)
        self.assertTrue(first["pushed"])
        second = manager.publish_integration(self.preparation, integration, remote="origin")
        self.assertEqual(second["result"], "PASS", second)
        self.assertTrue(second["unchanged"])
        remote_head = git(self.remote, "rev-parse", f"refs/heads/{self.preparation['integration_branch']}", capture=True)
        self.assertEqual(remote_head, integration["integration_head_sha"])

    def test_publish_integration_rejects_diverged_remote(self):
        integration = manager.integrate_run(self.preparation, self.workflow)
        self.assertEqual(integration["result"], "PASS", integration)
        other = self.root / "other"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(other)], check=True)
        git(other, "config", "user.name", "Other")
        git(other, "config", "user.email", "other@example.com")
        git(other, "switch", "-c", self.preparation["integration_branch"], self.base_sha)
        (other / "diverge.txt").write_text("diverged\n", encoding="utf-8")
        commit_all(other, "diverged remote")
        git(other, "push", "origin", f"HEAD:refs/heads/{self.preparation['integration_branch']}")
        result = manager.publish_integration(self.preparation, integration, remote="origin")
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("integration_remote_not_fast_forward", result["failures"])

    def test_cleanup_removes_clean_worktrees_but_keeps_local_branches(self):
        manager.integrate_run(self.preparation, self.workflow)
        result = manager.cleanup_run(self.preparation)
        self.assertEqual(result["result"], "PASS", result)
        self.assertGreaterEqual(len(result["removed_worktrees"]), 10)
        for assignment in self.preparation["assignments"]:
            self.assertFalse(pathlib.Path(assignment["workspace"]).exists())
            self.assertEqual(git(self.repo, "show-ref", "--verify", "--quiet", f"refs/heads/{assignment['branch']}", check=False), 0)
        self.assertTrue((self.workspaces / "_coordination").is_dir())

    def test_rehydrate_restores_cleaned_actor_worktrees_and_allows_receipt_only_resume(self):
        cleaned = manager.cleanup_run(self.preparation)
        self.assertEqual(cleaned["result"], "PASS", cleaned)
        restored = manager.rehydrate_run(self.preparation)
        self.assertEqual(restored["result"], "PASS", restored)
        self.assertEqual(len(restored["restored_actors"]), 10)
        for assignment in self.preparation["assignments"]:
            self.assertTrue(pathlib.Path(assignment["workspace"]).is_dir())
        resumed = wf_fixture.workflow.run_workflow(
            self.preparation, self.root / "missing-claude", self.root / "rehydrated-resume",
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
            resume_existing=True,
        )
        self.assertEqual(resumed["result"], "PASS", resumed)
        self.assertEqual(set(resumed["resumed_actors"]), {f"A{i:02d}" for i in range(1, 11)})
        self.assertEqual(resumed["executions"], {})
        self.assertEqual(resumed["backend_probe"]["result"], "NOT_RUN")

    def test_recovery_rejects_plan_history_tamper_after_receipt(self):
        published = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(published["result"], "PASS", published)
        actor = "A03"
        assignment = next(row for row in self.preparation["assignments"] if row["actor_id"] == actor)
        workspace = pathlib.Path(assignment["workspace"])
        plan_path = workspace / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/plans/{actor}.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["read_set"] = ["README.md"]
        plan_path.write_text(json.dumps(plan, sort_keys=True), encoding="utf-8")
        commit_all(workspace, "tamper plan after receipt")
        branch = assignment["branch"]
        git(workspace, "push", "origin", f"HEAD:refs/heads/{branch}")
        cleaned = manager.cleanup_run(self.preparation)
        self.assertEqual(cleaned["result"], "PASS", cleaned)
        fresh = self.root / "fresh-tamper"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(fresh)], check=True)
        subprocess.run(["git", "-C", str(fresh), "checkout", "-q", "main"], check=True)
        recovered = manager.recover_run(
            fresh, ISSUE, RUN_ID, "main", self.root / "recovered-tamper", remote="origin"
        )
        self.assertEqual(recovered["result"], "VETO", recovered)
        self.assertIn("plan_history_not_immutable:A03", recovered["failures"])

    def test_recovery_rejects_claim_history_tamper_after_receipt(self):
        published = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(published["result"], "PASS", published)
        actor = "A04"
        assignment = next(row for row in self.preparation["assignments"] if row["actor_id"] == actor)
        workspace = pathlib.Path(assignment["workspace"])
        claim_path = workspace / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/claims/{actor}.json"
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        claim["executor_id"] = claim["executor_id"] + "-tampered"
        claim_path.write_text(json.dumps(claim, sort_keys=True), encoding="utf-8")
        commit_all(workspace, "tamper claim after receipt")
        branch = assignment["branch"]
        git(workspace, "push", "origin", f"HEAD:refs/heads/{branch}")
        cleaned = manager.cleanup_run(self.preparation)
        self.assertEqual(cleaned["result"], "PASS", cleaned)
        fresh = self.root / "fresh-claim-tamper"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(fresh)], check=True)
        subprocess.run(["git", "-C", str(fresh), "checkout", "-q", "main"], check=True)
        recovered = manager.recover_run(
            fresh, ISSUE, RUN_ID, "main", self.root / "recovered-claim-tamper", remote="origin"
        )
        self.assertEqual(recovered["result"], "VETO", recovered)
        self.assertIn("claim_history_not_immutable:A04", recovered["failures"])

    def test_recover_from_remote_actor_branches_without_coordination_files(self):
        published = manager.publish_run(self.preparation, self.workflow, remote="origin")
        self.assertEqual(published["result"], "PASS", published)
        cleaned = manager.cleanup_run(self.preparation)
        self.assertEqual(cleaned["result"], "PASS", cleaned)
        shutil.rmtree(self.workspaces / "_coordination")

        fresh = self.root / "fresh-clone"
        subprocess.run([
            "git", "clone", "-q", "--branch", "main", str(self.remote), str(fresh)
        ], check=True)
        recovered_root = self.root / "recovered-workspaces"
        recovered = manager.recover_run(
            fresh, ISSUE, RUN_ID, "main", recovered_root, remote="origin"
        )
        self.assertEqual(recovered["result"], "PASS", recovered)
        self.assertEqual(len(recovered["assignments"]), 10)
        self.assertEqual(set(recovered["snapshots"]), {f"A{i:02d}" for i in range(1, 11)})
        self.assertTrue((recovered_root / "_coordination/run-preparation.json").is_file())

        resumed = wf_fixture.workflow.run_workflow(
            recovered, self.root / "missing-claude", self.root / "remote-recovery-resume",
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
            resume_existing=True,
        )
        self.assertEqual(resumed["result"], "PASS", resumed)
        self.assertEqual(set(resumed["resumed_actors"]), {f"A{i:02d}" for i in range(1, 11)})
        self.assertEqual(resumed["executions"], {})
        self.assertEqual(resumed["backend_probe"]["result"], "NOT_RUN")

    def test_cleanup_vetoes_dirty_workspace_without_force(self):
        a08 = pathlib.Path(next(row["workspace"] for row in self.preparation["assignments"] if row["actor_id"] == "A08"))
        (a08 / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        result = manager.cleanup_run(self.preparation)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("A08", result["dirty_actors"])
        self.assertTrue(a08.exists())


if __name__ == "__main__":
    unittest.main()
