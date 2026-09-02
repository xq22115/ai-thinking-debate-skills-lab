from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".agents/hooks/goal-fidelity-preinvocation.py"


def run_hook(payload: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        text=True,
        capture_output=True,
        check=True,
        cwd=ROOT,
    )
    return json.loads(proc.stdout)


class GoalFidelityPreInvocationTests(unittest.TestCase):
    def _message(self, payload: str) -> str:
        data = run_hook(payload)
        self.assertEqual(len(data.get("injectSteps", [])), 1)
        return data["injectSteps"][0]["ephemeralMessage"]

    def test_first_invocation_is_reanchored(self) -> None:
        message = self._message('{"invocationNum": 0}')
        self.assertIn("ROOT_GOAL", message)
        self.assertIn("CURRENT_BLOCKER", message)

    def test_later_invocation_is_reanchored(self) -> None:
        message = self._message('{"invocationNum": 7}')
        self.assertIn("acceptance test", message.lower())

    def test_malformed_payload_fails_open_to_goal_anchor_not_empty_context(self) -> None:
        message = self._message("not-json")
        self.assertIn("GOAL-LOCK CONTINUATION", message)

    def test_three_known_escape_patterns_are_explicitly_rejected(self) -> None:
        message = self._message('{}').lower()
        for required in (
            "exploiting",
            "killing",
            "gaming",
            "generic refusal/policy/ethics debate",
        ):
            self.assertIn(required, message)

    def test_blocker_requires_goal_mapped_next_action(self) -> None:
        message = self._message('{}').lower()
        self.assertIn("which unresolved goal contract field or acceptance test this action advances", message)
        self.assertIn("reject the action as non-progress", message)
        self.assertIn("choose a materially different task-advancing route", message)

    def test_legitimate_controller_diagnosis_remains_possible(self) -> None:
        message = self._message('{}').lower()
        self.assertIn("controller analysis is allowed only when diagnosing or modifying", message)
        self.assertIn("authorized task-relevant objective", message)


if __name__ == "__main__":
    unittest.main()
