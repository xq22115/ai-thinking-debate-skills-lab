from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
INSTALLER = REPO_ROOT / "control-plane/scripts/install_antigravity_global_goal_lock.py"
BEGIN = "<!-- AI-THINKING-DEBATE:ANTIGRAVITY-GOAL-LOCK:BEGIN -->"
END = "<!-- AI-THINKING-DEBATE:ANTIGRAVITY-GOAL-LOCK:END -->"
AGENT_NAMES = (
    "goal-contract-auditor",
    "route-recovery-engineer",
    "anti-evasion-red-team",
    "contribution-evidence-auditor",
    "owning-runtime-verifier",
)


class AntigravityGlobalGoalLockInstallerTests(unittest.TestCase):
    def _run(self, home: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), "--home", str(home)],
            text=True,
            capture_output=True,
            check=False,
        )

    def _agent_result_map(self, result: dict) -> dict[str, dict]:
        return {row["name"]: row for row in result["agents"]}

    def test_install_preserves_existing_content_backs_up_all_replacements_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            target = home / ".gemini/GEMINI.md"
            target.parent.mkdir(parents=True)
            original = "# Existing global rules\n\nKEEP_THIS_SETTING=yes\n"
            target.write_text(original, encoding="utf-8")

            agents_dir = home / ".gemini/config/agents"
            agents_dir.mkdir(parents=True)
            existing_agent = agents_dir / "route-recovery-engineer.md"
            old_agent_content = "# user's previous same-name agent\nKEEP_AGENT_BACKUP=yes\n"
            existing_agent.write_text(old_agent_content, encoding="utf-8")

            first = self._run(home)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_result = json.loads(first.stdout)
            self.assertEqual(first_result["status"], "UPDATED")
            self.assertTrue(first_result["changed"])
            self.assertEqual(first_result["agent_count"], 5)
            self.assertTrue(first_result["all_agent_targets_global"])
            self.assertEqual(first_result["rule"]["begin_marker_count"], 1)
            self.assertEqual(first_result["rule"]["end_marker_count"], 1)

            installed = target.read_text(encoding="utf-8")
            self.assertIn("KEEP_THIS_SETTING=yes", installed)
            self.assertEqual(installed.count(BEGIN), 1)
            self.assertEqual(installed.count(END), 1)
            self.assertIn("ROOT_GOAL", installed)
            self.assertIn("CURRENT_BLOCKER", installed)
            self.assertIn("Five-lane recovery council", installed)
            self.assertIn("Do not reduce requested reasoning effort", installed)
            for name in AGENT_NAMES:
                self.assertIn(f"`{name}`", installed)

            rule_backups = list(target.parent.glob("GEMINI.md.goal-lock.bak.*"))
            self.assertEqual(len(rule_backups), 1)
            self.assertEqual(rule_backups[0].read_text(encoding="utf-8"), original)

            agent_results = self._agent_result_map(first_result)
            self.assertEqual(set(agent_results), set(AGENT_NAMES))
            for name in AGENT_NAMES:
                global_agent = agents_dir / f"{name}.md"
                canonical = REPO_ROOT / ".agents/agents" / f"{name}.md"
                self.assertTrue(global_agent.is_file())
                self.assertEqual(
                    global_agent.read_text(encoding="utf-8"),
                    canonical.read_text(encoding="utf-8"),
                )
                self.assertIn("model: pro", global_agent.read_text(encoding="utf-8"))

            replaced_result = agent_results["route-recovery-engineer"]
            self.assertTrue(replaced_result["changed"])
            self.assertIsNotNone(replaced_result["backup"])
            agent_backup = pathlib.Path(replaced_result["backup"])
            self.assertTrue(agent_backup.is_file())
            self.assertEqual(agent_backup.read_text(encoding="utf-8"), old_agent_content)

            second = self._run(home)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_result = json.loads(second.stdout)
            self.assertEqual(second_result["status"], "UNCHANGED")
            self.assertFalse(second_result["changed"])
            self.assertFalse(second_result["rule"]["changed"])
            self.assertIsNone(second_result["rule"]["backup"])
            self.assertEqual(len(list(target.parent.glob("GEMINI.md.goal-lock.bak.*"))), 1)
            for row in second_result["agents"]:
                self.assertFalse(row["changed"])
                self.assertIsNone(row["backup"])
            self.assertEqual(
                len(list(agents_dir.glob("route-recovery-engineer.md.goal-lock.bak.*"))),
                1,
            )
            self.assertEqual(target.read_text(encoding="utf-8"), installed)

    def test_new_home_creates_global_rule_and_all_five_agents_without_backup(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            cp = self._run(home)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            result = json.loads(cp.stdout)
            self.assertEqual(result["status"], "UPDATED")
            self.assertEqual(result["agent_count"], 5)
            self.assertIsNone(result["rule"]["backup"])
            target = home / ".gemini/GEMINI.md"
            self.assertTrue(target.exists())
            self.assertEqual(target.read_text(encoding="utf-8").count(BEGIN), 1)
            for row in result["agents"]:
                self.assertTrue(row["changed"])
                self.assertIsNone(row["backup"])
                self.assertTrue(pathlib.Path(row["target"]).exists())

    def test_malformed_managed_block_fails_before_rule_or_agent_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            target = home / ".gemini/GEMINI.md"
            target.parent.mkdir(parents=True)
            malformed = f"before\n{BEGIN}\nbroken without end\n"
            target.write_text(malformed, encoding="utf-8")

            cp = self._run(home)
            self.assertNotEqual(cp.returncode, 0)
            result = json.loads(cp.stdout)
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("malformed", result["error"])
            self.assertEqual(target.read_text(encoding="utf-8"), malformed)
            self.assertEqual(list(target.parent.glob("GEMINI.md.goal-lock.bak.*")), [])
            self.assertFalse((home / ".gemini/config/agents").exists())


if __name__ == "__main__":
    unittest.main()
