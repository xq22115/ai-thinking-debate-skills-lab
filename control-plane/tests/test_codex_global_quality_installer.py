import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "install_codex_global_quality.py"
BEGIN = "<!-- BEGIN AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY -->"
END = "<!-- END AI-THINKING-DEBATE-SKILLS-LAB CONTINUOUS-QUALITY -->"


class CodexGlobalQualityInstallerTests(unittest.TestCase):
    def run_cli(self, codex_home: pathlib.Path, command: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), command, "--codex-home", str(codex_home)],
            text=True,
            capture_output=True,
            check=False,
        )

    def result(self, process: subprocess.CompletedProcess[str]) -> dict[str, object]:
        return json.loads(process.stdout)

    def test_install_creates_global_agents_and_check_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)

            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)

            agents = codex_home / "AGENTS.md"
            self.assertTrue(agents.is_file())
            content = agents.read_text(encoding="utf-8")
            self.assertIn(BEGIN, content)
            self.assertIn(END, content)
            self.assertNotIn("](./", content, "global policy must not depend on workspace-relative links")

            checked = self.run_cli(codex_home, "check")
            self.assertEqual(checked.returncode, 0, checked.stderr or checked.stdout)

    def test_nonempty_override_is_the_real_install_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            override = codex_home / "AGENTS.override.md"
            agents = codex_home / "AGENTS.md"
            override.write_text("keep override rule\n", encoding="utf-8")
            agents.write_text("keep fallback rule\n", encoding="utf-8")

            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)
            self.assertEqual(pathlib.Path(str(self.result(installed)["target"])), override)
            self.assertIn("keep override rule", override.read_text(encoding="utf-8"))
            self.assertIn(BEGIN, override.read_text(encoding="utf-8"))
            self.assertEqual(agents.read_text(encoding="utf-8"), "keep fallback rule\n")

    def test_empty_override_falls_back_to_agents_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            override = codex_home / "AGENTS.override.md"
            agents = codex_home / "AGENTS.md"
            override.write_text("\n", encoding="utf-8")
            agents.write_text("keep fallback rule\n", encoding="utf-8")

            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)
            self.assertEqual(pathlib.Path(str(self.result(installed)["target"])), agents)
            self.assertEqual(override.read_text(encoding="utf-8"), "\n")
            self.assertIn("keep fallback rule", agents.read_text(encoding="utf-8"))
            self.assertIn(BEGIN, agents.read_text(encoding="utf-8"))

    def test_existing_user_text_is_backed_up_and_second_install_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            agents = codex_home / "AGENTS.md"
            original = "my durable personal rule\n"
            agents.write_text(original, encoding="utf-8")

            first = self.run_cli(codex_home, "install")
            self.assertEqual(first.returncode, 0, first.stderr or first.stdout)
            self.assertTrue(self.result(first)["changed"])
            first_content = agents.read_text(encoding="utf-8")
            self.assertIn(original.strip(), first_content)
            self.assertEqual(first_content.count(BEGIN), 1)

            backup_dir = codex_home / "quality-installer-backups"
            backups = list(backup_dir.glob("AGENTS.md.*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), original)

            second = self.run_cli(codex_home, "install")
            self.assertEqual(second.returncode, 0, second.stderr or second.stdout)
            self.assertFalse(self.result(second)["changed"])
            self.assertEqual(agents.read_text(encoding="utf-8"), first_content)
            self.assertEqual(len(list(backup_dir.glob("AGENTS.md.*.bak"))), 1)

    def test_install_preserves_windows_crlf_bytes_and_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            agents = codex_home / "AGENTS.md"
            original = b"windows rule one\r\nwindows rule two\r\n"
            agents.write_bytes(original)

            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)
            self.assertTrue(agents.read_bytes().startswith(original))

            backups = list((codex_home / "quality-installer-backups").glob("AGENTS.md.*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), original)

    def test_check_fails_when_only_inactive_fallback_contains_managed_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)
            (codex_home / "AGENTS.override.md").write_text("new active override without managed block\n", encoding="utf-8")

            checked = self.run_cli(codex_home, "check")
            self.assertNotEqual(checked.returncode, 0)
            self.assertEqual(self.result(checked)["status"], "FAIL")
            self.assertTrue(str(self.result(checked)["target"]).endswith("AGENTS.override.md"))

    def test_malformed_managed_markers_fail_closed_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            agents = codex_home / "AGENTS.md"
            original = f"keep me\n\n{BEGIN}\ntruncated policy\n"
            agents.write_text(original, encoding="utf-8")

            installed = self.run_cli(codex_home, "install")
            self.assertNotEqual(installed.returncode, 0)
            self.assertEqual(agents.read_text(encoding="utf-8"), original)

    def test_stale_managed_block_is_replaced_not_duplicated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            agents = codex_home / "AGENTS.md"
            agents.write_text(f"keep me\n\n{BEGIN}\nold policy\n{END}\n", encoding="utf-8")

            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)
            content = agents.read_text(encoding="utf-8")
            self.assertIn("keep me", content)
            self.assertNotIn("old policy", content)
            self.assertEqual(content.count(BEGIN), 1)
            self.assertEqual(content.count(END), 1)

    def test_uninstall_removes_only_managed_block_and_preserves_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            agents = codex_home / "AGENTS.md"
            agents.write_text("before rule\nafter rule\n", encoding="utf-8")
            installed = self.run_cli(codex_home, "install")
            self.assertEqual(installed.returncode, 0, installed.stderr or installed.stdout)

            removed = self.run_cli(codex_home, "uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr or removed.stdout)
            content = agents.read_text(encoding="utf-8")
            self.assertIn("before rule", content)
            self.assertIn("after rule", content)
            self.assertNotIn(BEGIN, content)
            self.assertNotIn(END, content)

    def test_uninstall_removes_managed_blocks_from_both_candidate_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = pathlib.Path(tmp)
            first = self.run_cli(codex_home, "install")
            self.assertEqual(first.returncode, 0, first.stderr or first.stdout)
            agents = codex_home / "AGENTS.md"
            fallback_with_block = agents.read_text(encoding="utf-8")
            override = codex_home / "AGENTS.override.md"
            override.write_text("override user rule\n", encoding="utf-8")
            second = self.run_cli(codex_home, "install")
            self.assertEqual(second.returncode, 0, second.stderr or second.stdout)
            self.assertIn(BEGIN, fallback_with_block)
            self.assertIn(BEGIN, override.read_text(encoding="utf-8"))

            removed = self.run_cli(codex_home, "uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr or removed.stdout)
            if agents.exists():
                self.assertNotIn(BEGIN, agents.read_text(encoding="utf-8"))
            self.assertNotIn(BEGIN, override.read_text(encoding="utf-8"))
            self.assertIn("override user rule", override.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
