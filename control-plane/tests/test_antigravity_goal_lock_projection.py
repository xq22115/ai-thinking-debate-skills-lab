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


class AntigravityGoalLockProjectionTests(unittest.TestCase):
    def test_workspace_rule_is_always_on_and_goal_bound(self) -> None:
        text = RULE.read_text(encoding="utf-8")
        self.assertIn("trigger: always_on", text)
        self.assertIn("CURRENT_BLOCKER", text)
        self.assertIn("ROOT_GOAL", text)
        self.assertIn("Five-lane recovery council", text)
        self.assertIn("five observed executions", text)
        self.assertIn("Do not reduce requested reasoning effort", text)
        self.assertIn("Owning-runtime verifier", text)

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
