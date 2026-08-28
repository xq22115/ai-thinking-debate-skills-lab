import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "install_codex_global_quality.py"


class CodexGlobalQualityInstallerTests(unittest.TestCase):
    def run_cli(self, codex_home: pathlib.Path, command: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), command, "--codex-home", str(codex_home)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_install_creates_global_agents_and_check_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)

            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)

            agents = codex_home / "AGENTS.md"
            self.assertTrue(agents.is_file())
            content = agents.read_text(encoding="utf-8")
            self.assertIn("BEGIN AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY", content)
            self.assertIn("END AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY", content)

            checked = self.run_cli(codex_home, "check")
            self.assertEqual(checked.returncode, 0, checked.stderr or checked.stdout)


if __name__ == "__main__":
    unittest.main()
