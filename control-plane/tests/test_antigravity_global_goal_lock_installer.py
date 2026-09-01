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


class AntigravityGlobalGoalLockInstallerTests(unittest.TestCase):
    def _run(self, home: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), "--home", str(home)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_install_preserves_existing_content_backs_up_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            target = home / ".gemini/GEMINI.md"
            target.parent.mkdir(parents=True)
            original = "# Existing global rules\n\nKEEP_THIS_SETTING=yes\n"
            target.write_text(original, encoding="utf-8")

            first = self._run(home)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_result = json.loads(first.stdout)
            self.assertEqual(first_result["status"], "UPDATED")
            self.assertTrue(first_result["changed"])
            self.assertEqual(first_result["begin_marker_count"], 1)
            self.assertEqual(first_result["end_marker_count"], 1)

            installed = target.read_text(encoding="utf-8")
            self.assertIn("KEEP_THIS_SETTING=yes", installed)
            self.assertEqual(installed.count(BEGIN), 1)
            self.assertEqual(installed.count(END), 1)
            self.assertIn("ROOT_GOAL", installed)
            self.assertIn("CURRENT_BLOCKER", installed)
            self.assertIn("Five-lane recovery council", installed)
            self.assertIn("Do not reduce requested reasoning effort", installed)

            backups = list(target.parent.glob("GEMINI.md.goal-lock.bak.*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), original)

            second = self._run(home)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_result = json.loads(second.stdout)
            self.assertEqual(second_result["status"], "UNCHANGED")
            self.assertFalse(second_result["changed"])
            self.assertIsNone(second_result["backup"])
            self.assertEqual(len(list(target.parent.glob("GEMINI.md.goal-lock.bak.*"))), 1)
            self.assertEqual(target.read_text(encoding="utf-8"), installed)

    def test_new_home_creates_global_rule_without_backup(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            cp = self._run(home)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            result = json.loads(cp.stdout)
            self.assertEqual(result["status"], "UPDATED")
            self.assertIsNone(result["backup"])
            target = home / ".gemini/GEMINI.md"
            self.assertTrue(target.exists())
            self.assertEqual(target.read_text(encoding="utf-8").count(BEGIN), 1)

    def test_malformed_managed_block_fails_without_rewriting_file(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
