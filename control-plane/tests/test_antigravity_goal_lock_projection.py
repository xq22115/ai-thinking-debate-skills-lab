from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
RULE = REPO_ROOT / ".agents/rules/goal-fidelity-anti-evasion.md"
HOOKS = REPO_ROOT / ".agents/hooks.json"
PREINVOCATION = REPO_ROOT / ".agents/hooks/goal-fidelity-preinvocation.py"
AGENT_DIR = REPO_ROOT / ".agents/agents"
EXPECTED_AGENTS = {
    "goal-contract-auditor": "Goal Contract Auditor",
    "route-recovery-engineer": "Route Recovery Engineer",
    "anti-evasion-red-team": "Anti-Evasion Red Team",
    "contribution-evidence-auditor": "Contribution / Evidence Auditor",
    "owning-runtime-verifier": "Owning Runtime Verifier",
}


class AntigravityGoalLockProjectionTests(unittest.TestCase):
    def test_workspace_rule_is_always_on_and_goal_bound(self) -> None:
        text = RULE.read_text(encoding="utf-8")
        self.assertIn("trigger: always_on", text)
        self.assertIn("CURRENT_BLOCKER", text)
        self.assertIn("ROOT_GOAL", text)
        self.assertIn("Five-lane recovery council", text)
        self.assertIn("five observed subagent executions", text)
        self.assertIn("Do not reduce requested reasoning effort", text)
        self.assertIn("owning-runtime-verifier", text)
        self.assertIn("invoke_subagent", text)
        for name in EXPECTED_AGENTS:
            self.assertIn(f"`{name}`", text)

    def test_five_registered_subagents_are_distinct_pro_runtime_roles(self) -> None:
        names: set[str] = set()
        contents: list[str] = []
        for name, role_marker in EXPECTED_AGENTS.items():
            path = AGENT_DIR / f"{name}.md"
            self.assertTrue(path.is_file(), f"missing custom subagent: {path}")
            text = path.read_text(encoding="utf-8")
            contents.append(text)
            self.assertIn(f"name: {name}", text)
            self.assertIn("subagent: true", text)
            self.assertIn("mainAgent: false", text)
            self.assertIn("model: pro", text)
            self.assertIn("commandExecutionPolicy: sandbox", text)
            self.assertIn(role_marker, text)
            names.add(name)
        self.assertEqual(len(names), 5)
        self.assertEqual(len(set(contents)), 5, "five agents must not be duplicate definitions")

    def test_each_subagent_has_unique_goal_advancing_or_verification_duty(self) -> None:
        expected_markers = {
            "goal-contract-auditor": ["Goal Contract", "detect drift", "Route Recovery Engineer"],
            "route-recovery-engineer": ["materially different route", "Goal Contract Auditor", "observable test/read-back"],
            "anti-evasion-red-team": ["controller/hook", "headcount theater", "Contribution/Evidence Auditor"],
            "contribution-evidence-auditor": ["numeric agent count", "runtime independence", "Anti-Evasion Red Team"],
            "owning-runtime-verifier": ["highest practical layer", "PASS / FAIL / BLOCKED / NOT_RUN", "Goal Contract Auditor"],
        }
        for name, markers in expected_markers.items():
            text = (AGENT_DIR / f"{name}.md").read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, text, f"{name} missing duty marker: {marker}")

    def test_preinvocation_hook_is_registered(self) -> None:
        data = json.loads(HOOKS.read_text(encoding="utf-8"))
        definition = data["goal-fidelity-anti-evasion"]
        handlers = definition["PreInvocation"]
        self.assertEqual(len(handlers), 1)
        self.assertEqual(handlers[0]["type"], "command")
        self.assertEqual(
            handlers[0]["command"],
            "python .agents/hooks/goal-fidelity-preinvocation.py",
        )
        self.assertEqual(handlers[0]["timeout"], 5)

    def _run(self, invocation_num: int) -> dict:
        cp = subprocess.run(
            [sys.executable, str(PREINVOCATION)],
            input=json.dumps({
                "invocationNum": invocation_num,
                "initialNumSteps": 7,
                "conversationId": "test-conversation",
                "workspacePaths": [str(REPO_ROOT)],
                "transcriptPath": "/tmp/transcript.jsonl",
                "artifactDirectoryPath": "/tmp/artifacts",
            }),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stderr)
        return json.loads(cp.stdout)

    def test_first_invocation_does_not_duplicate_always_on_rule(self) -> None:
        result = self._run(0)
        self.assertEqual(result, {"injectSteps": []})

    def test_continuation_reanchors_goal_and_rejects_evasion(self) -> None:
        result = self._run(1)
        self.assertEqual(len(result["injectSteps"]), 1)
        message = result["injectSteps"][0]["ephemeralMessage"]
        self.assertIn("ROOT_GOAL", message)
        self.assertIn("CURRENT_BLOCKER", message)
        self.assertIn("killing", message)
        self.assertIn("gaming", message)
        self.assertIn("agent headcount", message)
        self.assertIn("reasoning effort", message)
        self.assertIn("unique contribution", message)
        self.assertIn("owning-runtime evidence", message)


if __name__ == "__main__":
    unittest.main()
