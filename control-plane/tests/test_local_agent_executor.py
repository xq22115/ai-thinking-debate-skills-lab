import importlib.util
import json
import os
import pathlib
import stat
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "local_executor", ROOT / "scripts/local_agent_executor.py"
)
executor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(executor)

ACTORS = [f"A{i:02d}" for i in range(1, 11)]
ISSUE = 27
RUN_ID = "run-local"
PLAN_SHA = "a" * 40


def make_fake_claude(path: pathlib.Path, *, logged_in=True, fail_actor=None,
                     missing_session_actor=None, duplicate_session=False):
    script = f'''#!/usr/bin/env python3
import json, os, sys, time
args = sys.argv[1:]
if args == ["--version"]:
    print("9.9.9 (Fake Claude Code)")
    raise SystemExit(0)
if args == ["auth", "status"]:
    print(json.dumps({{"loggedIn": {str(logged_in)}, "authMethod": "fake", "apiProvider": "fake"}}))
    raise SystemExit(0)
actor = os.environ.get("CONTROL_PLANE_ACTOR_ID", "UNKNOWN")
if actor == {fail_actor!r}:
    print("forced failure", file=sys.stderr)
    raise SystemExit(7)
time.sleep(0.15)
session = "shared-session" if {duplicate_session!r} else f"session-{{actor}}"
payload = {{
  "type": "result",
  "session_id": None if actor == {missing_session_actor!r} else session,
  "structured_output": {{
    "agent_id": actor,
    "decision": "PASS",
    "summary": f"validated {{actor}}",
    "evidence": [{{"kind": "readback", "reference": f"fake-{{actor}}"}}]
  }}
}}
print(json.dumps(payload))
'''
    path.write_text(script, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def assignments(root: pathlib.Path):
    rows = []
    for actor in ACTORS:
        workspace = root / actor
        workspace.mkdir(parents=True, exist_ok=True)
        rows.append({
            "issue_number": ISSUE,
            "run_id": RUN_ID,
            "actor_id": actor,
            "branch": f"agent/{ISSUE}/{actor}/{RUN_ID}",
            "workspace": str(workspace),
            "role_file": f"ai-system/control-plane/agents/{actor}.md",
            "claim_id": f"claim-{actor}",
            "executor_id": f"local-slot-{actor}",
            "execution_id": f"execution-{actor}",
            "plan_head_sha": PLAN_SHA,
        })
    return rows


class LocalAgentExecutorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.fake = self.root / "claude"
        self.output = self.root / "out"

    def tearDown(self):
        self.temp.cleanup()

    def test_probe_blocks_when_not_authenticated(self):
        make_fake_claude(self.fake, logged_in=False)
        result = executor.probe_claude(self.fake)
        self.assertEqual(result["result"], "BLOCKED", result)
        self.assertFalse(result["logged_in"])

    def test_probe_passes_when_authenticated(self):
        make_fake_claude(self.fake, logged_in=True)
        result = executor.probe_claude(self.fake)
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["version"], "9.9.9 (Fake Claude Code)")

    def test_unauthenticated_backend_launches_zero_model_processes(self):
        make_fake_claude(self.fake, logged_in=False)
        result = executor.execute_agents(
            assignments(self.root / "ws"), self.fake, self.output
        )
        self.assertEqual(result["result"], "BLOCKED", result)
        self.assertEqual(result["executions"], [])

    def test_duplicate_workspace_is_veto(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        rows[1]["workspace"] = rows[0]["workspace"]
        result = executor.execute_agents(rows, self.fake, self.output)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("duplicate_workspace", result["failures"])

    def test_duplicate_branch_is_veto(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        rows[1]["branch"] = rows[0]["branch"]
        result = executor.execute_agents(rows, self.fake, self.output)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("duplicate_branch", result["failures"])

    def test_assignment_requires_claim_bound_identity(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        rows[0].pop("claim_id")
        rows[1].pop("plan_head_sha")
        result = executor.execute_agents(rows, self.fake, self.output)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("missing_claim_id:A01", result["failures"])
        self.assertIn("missing_plan_head_sha:A02", result["failures"])

    def test_invalid_issue_or_branch_run_identity_is_veto(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        rows[0]["issue_number"] = 0
        rows[1]["run_id"] = "other-run"
        result = executor.execute_agents(rows, self.fake, self.output)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("invalid_issue_number:A01", result["failures"])
        self.assertIn("branch_run_id_mismatch:A02", result["failures"])

    def test_duplicate_claim_bound_executor_id_is_veto(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        rows[1]["executor_id"] = rows[0]["executor_id"]
        result = executor.execute_agents(rows, self.fake, self.output)
        self.assertEqual(result["result"], "VETO", result)
        self.assertIn("duplicate_executor_id", result["failures"])

    def test_execution_uses_predeclared_claim_identity(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        result = executor.execute_agents(rows, self.fake, self.output)
        self.assertEqual(result["result"], "PASS", result)
        for assignment in rows:
            actor = assignment["actor_id"]
            row = result["executions"][actor]
            self.assertEqual(row["execution_id"], assignment["execution_id"])
            self.assertEqual(row["executor_id"], assignment["executor_id"])
            self.assertEqual(row["claim_id"], assignment["claim_id"])
            self.assertEqual(row["plan_head_sha"], assignment["plan_head_sha"])

    def test_nonzero_child_exit_fails_closed(self):
        make_fake_claude(self.fake, fail_actor="A05")
        result = executor.execute_agents(
            assignments(self.root / "ws"), self.fake, self.output
        )
        self.assertEqual(result["result"], "FAIL", result)
        self.assertEqual(result["executions"]["A05"]["exit_code"], 7)

    def test_missing_session_id_fails_closed(self):
        make_fake_claude(self.fake, missing_session_actor="A08")
        result = executor.execute_agents(
            assignments(self.root / "ws"), self.fake, self.output
        )
        self.assertEqual(result["result"], "FAIL", result)
        self.assertIn("missing_session_id:A08", result["failures"])

    def test_duplicate_session_ids_fail_closed(self):
        make_fake_claude(self.fake, duplicate_session=True)
        result = executor.execute_agents(
            assignments(self.root / "ws"), self.fake, self.output
        )
        self.assertEqual(result["result"], "FAIL", result)
        self.assertIn("duplicate_session_id", result["failures"])

    def test_ten_successful_runs_are_process_and_session_distinct(self):
        make_fake_claude(self.fake)
        result = executor.execute_agents(
            assignments(self.root / "ws"), self.fake, self.output, max_parallel=10
        )
        self.assertEqual(result["result"], "PASS", result)
        runs = result["executions"]
        self.assertEqual(set(runs), set(ACTORS))
        self.assertTrue(all(row["pid"] > 0 for row in runs.values()))
        self.assertEqual(len({row["process_instance_id"] for row in runs.values()}), 10)
        self.assertTrue(all(row["spawn_monotonic_ns"] > 0 for row in runs.values()))
        self.assertEqual(len({row["execution_id"] for row in runs.values()}), 10)
        self.assertEqual(len({row["session_id"] for row in runs.values()}), 10)
        self.assertEqual(len({row["workspace"] for row in runs.values()}), 10)
        for actor, row in runs.items():
            self.assertEqual(row["decision"]["agent_id"], actor)
            self.assertTrue((self.output / f"{actor}.json").is_file())

    def test_readonly_role_can_mount_existing_dependency_dirs(self):
        dep1 = self.root / "dep-A07"
        dep2 = self.root / "dep-A08"
        dep1.mkdir()
        dep2.mkdir()
        cmd = executor.build_claude_command(
            self.fake, "A09", "prompt", max_budget_usd=0.01,
            read_dirs=[str(dep1), str(dep2)],
        )
        index = cmd.index("--add-dir")
        self.assertEqual(cmd[index + 1:index + 3], [str(dep1), str(dep2)])
        self.assertIn("--allowedTools", cmd[index + 3:])

    def test_a07_cannot_mount_external_dependency_workspace(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        external = self.root / "dependency"
        external.mkdir()
        rows[6]["read_dirs"] = [str(external)]
        failures = executor._assignment_failures(rows)
        self.assertIn("write_role_external_read_dir_forbidden:A07", failures)

    def test_readonly_dependency_dir_must_exist_and_be_unique(self):
        make_fake_claude(self.fake)
        rows = assignments(self.root / "ws")
        dep = self.root / "dep"
        dep.mkdir()
        rows[7]["read_dirs"] = [str(dep), str(dep), str(self.root / "missing")]
        failures = executor._assignment_failures(rows)
        self.assertIn("duplicate_dependency_read_dir:A08", failures)
        self.assertIn("dependency_read_dir_missing:A08", failures)

    def test_tool_policy_is_positive_allowlist_and_never_grants_bash(self):
        read_cmd = executor.build_claude_command(
            self.fake, "A08", "prompt", max_budget_usd=0.01
        )
        write_cmd = executor.build_claude_command(
            self.fake, "A07", "prompt", max_budget_usd=0.01
        )
        read_tools = read_cmd[read_cmd.index("--allowedTools") + 1]
        write_tools = write_cmd[write_cmd.index("--allowedTools") + 1]
        self.assertEqual(read_tools, "Read,Glob,Grep")
        self.assertEqual(write_tools, "Read,Glob,Grep,Edit,Write")
        self.assertNotIn("Bash", read_tools)
        self.assertNotIn("Bash", write_tools)
        self.assertNotIn("--disallowedTools", read_cmd)
        self.assertNotIn("--disallowedTools", write_cmd)
        self.assertIn("--max-budget-usd", write_cmd)


if __name__ == "__main__":
    unittest.main()
