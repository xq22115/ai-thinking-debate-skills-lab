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
CONFIG = REPO_ROOT / "control-plane/ai-system/configs/goal-fidelity-global.json"
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
        self.assertIn("Blocker recovery state machine", text)
        self.assertIn("NEXT_ACTION_CLASS", text)
        self.assertIn("EXPECTED_PROGRESS_DELTA", text)
        self.assertIn("CONTROL_PLANE_TARGETING", text)
        self.assertIn("two materially similar failures", text)
        self.assertIn("positive and task-directed", text)
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
            "goal-contract-auditor": ["Goal Contract", "drift between that contract", "Route Recovery Engineer"],
            "route-recovery-engineer": ["materially different route", "Goal Contract Auditor", "observable test/read-back"],
            "anti-evasion-red-team": ["hook/controller", "headcount theater", "Contribution/Evidence Auditor"],
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

    def test_machine_contract_encodes_typed_blocker_recovery(self) -> None:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        recovery = data["anti_evasion_control"]["blocker_recovery_state_machine"]
        self.assertEqual(
            set(recovery["action_classes"]),
            {"ADVANCE", "VERIFY", "RECOVER_ROUTE", "CONTROL_PLANE_TARGETING"},
        )
        self.assertEqual(
            set(recovery["default_progress_classes"]),
            {"ADVANCE", "VERIFY", "RECOVER_ROUTE"},
        )
        self.assertEqual(recovery["same_route_failure_limit_before_causal_pivot"], 2)
        self.assertTrue(recovery["control_plane_targeting_requires_explicit_goal_contract_target"])
        self.assertTrue(recovery["control_plane_targeting_never_counts_as_progress_by_default"])
        self.assertTrue(recovery["mixed_task_still_executable_scope_must_continue"])
        self.assertTrue(recovery["blocker_messages_should_be_positive_task_directed_not_evasion_priming"])

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

    def test_continuation_reanchors_goal_and_uses_typed_recovery(self) -> None:
        result = self._run(1)
        self.assertEqual(len(result["injectSteps"]), 1)
        message = result["injectSteps"][0]["ephemeralMessage"]
        self.assertIn("ROOT_GOAL", message)
        self.assertIn("CURRENT_BLOCKER", message)
        self.assertIn("NEXT_ACTION_CLASS", message)
        self.assertIn("ADVANCE", message)
        self.assertIn("VERIFY", message)
        self.assertIn("RECOVER_ROUTE", message)
        self.assertIn("CONTROL_PLANE_TARGETING", message)
        self.assertIn("EXPECTED_PROGRESS_DELTA", message)
        self.assertIn("EVIDENCE_TARGET", message)
        self.assertIn("two materially similar failures", message)
        self.assertIn("unique contribution", message)
        self.assertIn("owning-runtime evidence", message)


if __name__ == "__main__":
    unittest.main()
