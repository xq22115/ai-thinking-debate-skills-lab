import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "deep-reasoning-quality-gate.yml"


class CodexGlobalQualityRegistrationTests(unittest.TestCase):
    def test_deep_reasoning_gate_compiles_and_runs_installer_tests(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("control-plane/scripts/install_codex_global_quality.py", text)
        self.assertIn("tests/test_codex_global_quality_installer.py", text)


if __name__ == "__main__":
    unittest.main()
