import importlib.util
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "preparer", ROOT / "scripts/prepare_local_agent_run.py"
)
preparer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preparer)

EXEC_SPEC = importlib.util.spec_from_file_location(
    "local_executor", ROOT / "scripts/local_agent_executor.py"
)
local_executor = importlib.util.module_from_spec(EXEC_SPEC)
EXEC_SPEC.loader.exec_module(local_executor)

ISSUE = 27
RUN_ID = "run-prepared"


def git(repo, *args, capture=False, check=True):
    cp = subprocess.run(
        ["git", "-C", str(repo), *args], text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE, check=check,
    )
    return cp.stdout.strip() if capture else cp.returncode


def commit_all(repo, message):
    git(repo, "add", ".")
    git(
        repo, "-c", "user.name=Test", "-c", "user.email=test@example.com",
        "commit", "-m", message,
    )
    return git(repo, "rev-parse", "HEAD", capture=True)


def deterministic_id(kind, actor):
    return f"{kind}-{actor}-fixed"


class PrepareLocalAgentRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.repo = self.root / "repo"
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
        self.workspaces = self.root / "workspaces"

    def tearDown(self):
        self.temp.cleanup()

    def test_prepares_ten_claim_bound_worktrees_and_preflight(self):
        result = preparer.prepare_run(
            self.repo,
            ISSUE,
            RUN_ID,
            self.base_sha,
            "main",
            self.workspaces,
            plan_config={"A07": {"write_set": ["work/A07/**"]}},
            id_factory=deterministic_id,
        )
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(len(result["assignments"]), 10)
        self.assertEqual(result["preflight"]["result"], "PASS")
        self.assertEqual(result["collection"]["result"], "PASS")
        self.assertEqual(
            result["integration_branch"], f"task/{ISSUE}/{RUN_ID}/integration"
        )
        self.assertFalse(result["remote_push_performed"])
        self.assertEqual(result["source_repo"], str(self.repo.resolve()))
        self.assertEqual(local_executor._assignment_failures(result["assignments"]), [])

        for row in result["assignments"]:
            actor = row["actor_id"]
            workspace = pathlib.Path(row["workspace"])
            self.assertTrue(workspace.is_dir())
            self.assertEqual(git(workspace, "branch", "--show-current", capture=True), row["branch"])
            self.assertEqual(git(workspace, "rev-parse", "HEAD", capture=True), row["plan_head_sha"])
            claim_path = workspace / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/claims/{actor}.json"
            plan_path = workspace / f"ai-system/control-plane/runs/{ISSUE}/{RUN_ID}/plans/{actor}.json"
            claim = json.loads(claim_path.read_text())
            plan = json.loads(plan_path.read_text())
            self.assertEqual(claim["claim_id"], f"claim-{actor}-fixed")
            self.assertEqual(claim["executor_id"], f"executor-{actor}-fixed")
            self.assertEqual(claim["execution_id"], f"execution-{actor}-fixed")
            self.assertEqual(plan["write_set"], ["work/A07/**"] if actor == "A07" else [])
        self.assertEqual(
            result["dependencies"]["A08"], ["A01", "A07"]
        )
        self.assertEqual(
            result["dependencies"]["A10"],
            ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09"],
        )
        integration_sha = git(
            self.repo, "rev-parse", result["integration_branch"], capture=True
        )
        self.assertEqual(integration_sha, self.base_sha)
        self.assertEqual(git(self.repo, "rev-parse", "main", capture=True), self.base_sha)
        self.assertEqual(git(self.repo, "status", "--porcelain", capture=True), "")

    def test_stale_base_blocks_before_creating_workspaces(self):
        old_base = self.base_sha
        (self.repo / "later.txt").write_text("later\n", encoding="utf-8")
        commit_all(self.repo, "advance main")
        result = preparer.prepare_run(
            self.repo, ISSUE, RUN_ID, old_base, "main", self.workspaces,
            id_factory=deterministic_id,
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("base_ref_mismatch", result["failures"])
        self.assertFalse(self.workspaces.exists())

    def test_dirty_source_repo_blocks_before_mutation(self):
        (self.repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        result = preparer.prepare_run(
            self.repo, ISSUE, RUN_ID, self.base_sha, "main", self.workspaces,
            id_factory=deterministic_id,
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("source_worktree_dirty", result["failures"])
        self.assertFalse(self.workspaces.exists())

    def test_readonly_actor_cannot_request_task_write_scope(self):
        result = preparer.prepare_run(
            self.repo,
            ISSUE,
            RUN_ID,
            self.base_sha,
            "main",
            self.workspaces,
            plan_config={"A08": {"write_set": ["docs/**"]}},
            id_factory=deterministic_id,
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("readonly_write_set_nonempty:A08", result["failures"])
        self.assertFalse(self.workspaces.exists())

    def test_existing_actor_branch_blocks_before_worktree_creation(self):
        branch = f"agent/{ISSUE}/A01/{RUN_ID}"
        git(self.repo, "branch", branch, self.base_sha)
        result = preparer.prepare_run(
            self.repo, ISSUE, RUN_ID, self.base_sha, "main", self.workspaces,
            id_factory=deterministic_id,
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn(f"branch_already_exists:{branch}", result["failures"])
        self.assertFalse(self.workspaces.exists())

    def test_nonempty_workspace_root_is_veto(self):
        self.workspaces.mkdir()
        (self.workspaces / "existing.txt").write_text("occupied\n", encoding="utf-8")
        result = preparer.prepare_run(
            self.repo, ISSUE, RUN_ID, self.base_sha, "main", self.workspaces,
            id_factory=deterministic_id,
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("workspace_root_not_empty", result["failures"])


if __name__ == "__main__":
    unittest.main()
