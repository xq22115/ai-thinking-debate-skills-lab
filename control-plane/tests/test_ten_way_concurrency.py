import importlib.util
import json
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
RUN_ID = "run-ten-way-overlap"
PLAN_SHA = "b" * 40


def make_fake_claude(path: pathlib.Path):
    script = '''#!/usr/bin/env python3
import json, os, sys, time
args = sys.argv[1:]
if args == ["--version"]:
    print("9.9.9 (Fake Claude Code)")
    raise SystemExit(0)
if args == ["auth", "status"]:
    print(json.dumps({"loggedIn": True, "authMethod": "fake", "apiProvider": "fake"}))
    raise SystemExit(0)
actor = os.environ.get("CONTROL_PLANE_ACTOR_ID", "UNKNOWN")
time.sleep(0.15)
verification = "readback" if actor in {"A08", "A10"} else "static"
print(json.dumps({
  "type": "result",
  "session_id": f"session-{actor}",
  "structured_output": {
    "agent_id": actor,
    "decision": "PASS",
    "summary": f"validated {actor}",
    "evidence": [{"kind": "readback", "reference": f"fake-{actor}"}],
    "reasoning_quality": {
      "task_class": "material",
      "objective_model": f"validate outcome for {actor}",
      "causal_model": f"direct evidence determines {actor} verdict",
      "high_impact_unknowns": [],
      "evidence_delta": f"new direct evidence for {actor}",
      "stagnation_state": "CLEAR",
      "verification_level": verification,
      "adversarial_check": "counterexample attempted without contradiction",
      "research_stop_reason": "decision_saturated",
      "remaining_risks": []
    }
  }
}))
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


class TenWayConcurrentExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.fake = self.root / "claude"
        self.output = self.root / "out"
        make_fake_claude(self.fake)

    def tearDown(self):
        self.temp.cleanup()

    def test_strict_mode_proves_all_ten_shared_a_live_interval(self):
        result = executor.execute_agents(
            assignments(self.root / "ws"),
            self.fake,
            self.output,
            max_parallel=10,
            require_all_concurrent=True,
        )
        self.assertEqual(result["result"], "PASS", result)
        concurrency = result["concurrency"]
        self.assertTrue(concurrency["require_all_concurrent"])
        self.assertEqual(concurrency["required_count"], 10)
        self.assertEqual(concurrency["observed_count"], 10)
        self.assertTrue(concurrency["common_overlap_proven"])
        self.assertGreater(concurrency["common_overlap_ns"], 0)
        for row in result["executions"].values():
            self.assertGreater(row["finish_monotonic_ns"], row["spawn_monotonic_ns"])

    def test_strict_mode_rejects_serial_ten_passes(self):
        result = executor.execute_agents(
            assignments(self.root / "ws"),
            self.fake,
            self.output,
            max_parallel=1,
            require_all_concurrent=True,
        )
        self.assertEqual(result["result"], "FAIL", result)
        self.assertIn("ten_way_common_overlap_missing", result["failures"])
        self.assertFalse(result["concurrency"]["common_overlap_proven"])

    def test_default_mode_remains_backward_compatible(self):
        result = executor.execute_agents(
            assignments(self.root / "ws"),
            self.fake,
            self.output,
            max_parallel=1,
        )
        self.assertEqual(result["result"], "PASS", result)
        self.assertFalse(result["concurrency"]["require_all_concurrent"])


if __name__ == "__main__":
    unittest.main()
