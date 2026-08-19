import importlib.util
import json
import pathlib
import shutil
import stat
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "workflow", ROOT / "scripts/run_local_agent_workflow.py"
)
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)

PREP_SPEC = importlib.util.spec_from_file_location(
    "preparer", ROOT / "scripts/prepare_local_agent_run.py"
)
preparer = importlib.util.module_from_spec(PREP_SPEC)
PREP_SPEC.loader.exec_module(preparer)

ISSUE = 27
RUN_ID = "run-workflow"


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
    return f"{kind}-{actor}-workflow"


def make_fake_claude(path: pathlib.Path, *, logged_in=True, veto_actor=None, fail_actor=None):
    script = f'''#!/usr/bin/env python3
import json, os, pathlib, sys
args = sys.argv[1:]
if args == ["--version"]:
    print("9.9.9 (Fake Claude Code)")
    raise SystemExit(0)
if args == ["auth", "status"]:
    print(json.dumps({{"loggedIn": {str(logged_in)}, "authMethod": "fake", "apiProvider": "fake"}}))
    raise SystemExit(0)
actor = os.environ.get("CONTROL_PLANE_ACTOR_ID", "UNKNOWN")
read_dirs = []
if "--add-dir" in args:
    i = args.index("--add-dir") + 1
    while i < len(args) and not args[i].startswith("--"):
        read_dirs.append(args[i])
        i += 1
if actor == {fail_actor!r}:
    print("intentional fake child failure", file=sys.stderr)
    raise SystemExit(23)
if actor == "A07":
    if read_dirs:
        print("A07 received external dirs", file=sys.stderr)
        raise SystemExit(19)
    target = pathlib.Path.cwd() / "work/A07/result.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("implemented by fake A07\\n", encoding="utf-8")
if actor == "A08":
    if not any(pathlib.Path(d).name == "A07" for d in read_dirs):
        print("A08 missing A07 dependency workspace", file=sys.stderr)
        raise SystemExit(20)
if actor == "A10":
    names = {{pathlib.Path(d).name for d in read_dirs}}
    expected = {{f"A{{i:02d}}" for i in range(1, 10)}}
    if not expected.issubset(names):
        print("A10 missing dependency workspaces", file=sys.stderr)
        raise SystemExit(21)
decision = "VETO" if actor == {veto_actor!r} else "PASS"
summary = "counterexample" if decision == "VETO" else f"validated {{actor}}"
payload = {{
  "type": "result",
  "session_id": f"session-{{actor}}",
  "structured_output": {{
    "agent_id": actor,
    "decision": decision,
    "summary": summary,
    "evidence": [{{"kind": "readback", "reference": f"fake-{{actor}}"}}]
  }}
}}
print(json.dumps(payload))
'''
    path.write_text(script, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


class RunLocalAgentWorkflowTests(unittest.TestCase):
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
        self.preparation = preparer.prepare_run(
            self.repo,
            ISSUE,
            RUN_ID,
            self.base_sha,
            "main",
            self.workspaces,
            plan_config={"A07": {"write_set": ["work/A07/**"]}},
            id_factory=deterministic_id,
        )
        self.assertEqual(self.preparation["result"], "PASS", self.preparation)
        self.fake = self.root / "claude"
        self.output = self.root / "workflow-output"

    def tearDown(self):
        self.temp.cleanup()

    def test_successful_dependency_aware_run_reaches_adjudication_pass(self):
        make_fake_claude(self.fake)
        result = workflow.run_workflow(
            self.preparation,
            self.fake,
            self.output,
            max_parallel=3,
            timeout_seconds=20,
            max_budget_usd=0.01,
        )
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(
            result["waves"],
            [
                ["A01"],
                ["A02", "A03", "A04"],
                ["A05"],
                ["A06"],
                ["A07"],
                ["A08"],
                ["A09"],
                ["A10"],
            ],
        )
        self.assertEqual(set(result["executions"]), {f"A{i:02d}" for i in range(1, 11)})
        self.assertEqual(len({row["process_instance_id"] for row in result["executions"].values()}), 10)
        self.assertEqual(len({row["session_id"] for row in result["executions"].values()}), 10)
        self.assertEqual(result["adjudication"]["result"], "PASS")
        self.assertEqual(result["base_freshness"]["result"], "PASS")
        self.assertTrue(all(value == "PASS" for value in result["statuses"].values()))
        a07 = pathlib.Path(next(row["workspace"] for row in self.preparation["assignments"] if row["actor_id"] == "A07"))
        self.assertTrue((a07 / "work/A07/result.txt").is_file())

    def test_veto_blocks_downstream_agents_from_launch(self):
        make_fake_claude(self.fake, veto_actor="A05")
        result = workflow.run_workflow(
            self.preparation,
            self.fake,
            self.output,
            max_parallel=3,
            timeout_seconds=20,
            max_budget_usd=0.01,
        )
        self.assertEqual(result["result"], "VETO", result)
        self.assertEqual(set(result["executions"]), {"A01", "A02", "A03", "A04", "A05"})
        self.assertEqual(result["statuses"]["A05"], "VETO")
        for actor in ["A06", "A07", "A08", "A09", "A10"]:
            self.assertEqual(result["statuses"][actor], "BLOCKED")
            self.assertIn(actor, result["blocked_dependencies"])
        self.assertEqual(result["adjudication"]["result"], "NOT_RUN")

    def test_unauthenticated_backend_launches_zero_agents(self):
        make_fake_claude(self.fake, logged_in=False)
        result = workflow.run_workflow(
            self.preparation,
            self.fake,
            self.output,
            max_parallel=3,
            timeout_seconds=20,
            max_budget_usd=0.01,
        )
        self.assertEqual(result["result"], "BLOCKED", result)
        self.assertEqual(result["executions"], {})
        self.assertEqual(result["waves"], [])

    def test_resume_reuses_verified_pass_receipts_and_runs_only_missing_downstream(self):
        make_fake_claude(self.fake, fail_actor="A05")
        first = workflow.run_workflow(
            self.preparation, self.fake, self.output,
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
        )
        self.assertEqual(first["result"], "FAIL", first)
        self.assertEqual(set(first["executions"]), {"A01", "A02", "A03", "A04", "A05"})
        make_fake_claude(self.fake)
        resumed_output = self.root / "workflow-resume"
        resumed = workflow.run_workflow(
            self.preparation, self.fake, resumed_output,
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
            resume_existing=True,
        )
        self.assertEqual(resumed["result"], "PASS", resumed)
        self.assertEqual(set(resumed["resumed_actors"]), {"A01", "A02", "A03", "A04"})
        self.assertEqual(set(resumed["executions"]), {"A05", "A06", "A07", "A08", "A09", "A10"})
        self.assertEqual(resumed["adjudication"]["result"], "PASS")

    def test_resume_does_not_overwrite_existing_veto_receipt(self):
        make_fake_claude(self.fake, veto_actor="A05")
        first = workflow.run_workflow(
            self.preparation, self.fake, self.output,
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
        )
        self.assertEqual(first["result"], "VETO", first)
        make_fake_claude(self.fake)
        resumed = workflow.run_workflow(
            self.preparation, self.fake, self.root / "resume-veto",
            max_parallel=3, timeout_seconds=20, max_budget_usd=0.01,
            resume_existing=True,
        )
        self.assertEqual(resumed["result"], "VETO", resumed)
        self.assertIn("existing_veto_receipt:A05", resumed["failures"])
        self.assertEqual(resumed["executions"], {})

    def test_base_drift_after_preparation_vetoes_final_pass(self):
        make_fake_claude(self.fake)
        (self.repo / "advance.txt").write_text("advance\n", encoding="utf-8")
        commit_all(self.repo, "advance base")
        result = workflow.run_workflow(
            self.preparation,
            self.fake,
            self.output,
            max_parallel=3,
            timeout_seconds=20,
            max_budget_usd=0.01,
        )
        self.assertEqual(result["adjudication"]["result"], "PASS", result)
        self.assertEqual(result["base_freshness"]["result"], "VETO", result)
        self.assertEqual(result["result"], "VETO", result)


if __name__ == "__main__":
    unittest.main()
