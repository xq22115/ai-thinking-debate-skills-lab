import importlib.util
import os
import pathlib
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "ordinary_chat_bridge.py"
spec = importlib.util.spec_from_file_location("ordinary_chat_bridge", MODULE_PATH)
assert spec and spec.loader
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class OrdinaryChatBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name) / "allowed"
        self.root.mkdir()
        self.workspace = self.root / "project"
        self.workspace.mkdir()
        self.old_env = dict(os.environ)
        os.environ["ORDINARY_CHAT_STATE_DIR"] = str(pathlib.Path(self.temp.name) / "state")
        os.environ.pop("CHAT_WORK_AGENT_PATH", None)
        os.environ.pop("CLAUDE_PATH", None)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)
        self.temp.cleanup()

    def test_preflight_blocks_without_allowlist(self):
        os.environ.pop("ORDINARY_CHAT_ALLOWED_ROOTS", None)
        result = bridge.preflight(str(self.workspace), str(self.workspace))
        self.assertEqual(result["result"], "BLOCKED")
        self.assertFalse(result["allowed_roots_configured"])

    def test_preflight_accepts_allowlisted_workspace(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.preflight(str(self.workspace), str(self.workspace))
        self.assertEqual(result["result"], "PASS")
        self.assertTrue(result["workspace_allowed"])
        self.assertTrue(result["repo_allowed"])

    def test_submit_chat_fails_closed_without_agent_binary(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.submit_chat(str(self.workspace), "inspect this project")
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("chat_work_agent_unavailable", result["failures"])

    def test_a01_rejects_parent_traversal_write_set(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.submit_a01(
            str(self.workspace), 1, "main", "goal", ["../outside"], 3, 180, 0.05, None
        )
        self.assertEqual(result["result"], "BLOCKED")
        self.assertTrue(any(item.startswith("invalid_write_set:") for item in result["failures"]))

    def test_invalid_run_id_is_not_found(self):
        result = bridge.status("not-a-run-id")
        self.assertEqual(result["result"], "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
