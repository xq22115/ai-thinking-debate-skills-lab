import importlib.util
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

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
        result = bridge.preflight(str(self.workspace), None)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertFalse(result["allowed_roots_configured"])

    def test_preflight_accepts_allowlisted_workspace(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.preflight(str(self.workspace), None)
        self.assertEqual(result["result"], "PASS")
        self.assertTrue(result["workspace_allowed"])
        self.assertFalse(result["chat_submit_ready"])

    def test_preflight_blocks_workspace_outside_allowlist(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        outside = pathlib.Path(self.temp.name) / "outside"
        outside.mkdir()
        result = bridge.preflight(str(outside), None)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("workspace_not_allowlisted", result["failures"])

    def test_preflight_blocks_non_git_repo(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.preflight(None, str(self.workspace))
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("repo_not_git", result["failures"])

    def test_submit_chat_fails_closed_without_agent_binary(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.submit_chat(str(self.workspace), "inspect this project")
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("chat_work_agent_unavailable", result["failures"])

    def test_queue_parent_does_not_rewrite_record_after_spawn(self):
        fake_process = mock.Mock(pid=4321)
        with mock.patch.object(bridge.subprocess, "Popen", return_value=fake_process):
            response = bridge._queue("chat-work-agent", {"workspace": str(self.workspace), "goal": "goal"})
        persisted = bridge.status(response["run_id"])
        self.assertEqual(response["status"], "QUEUED")
        self.assertEqual(response["worker_pid"], 4321)
        self.assertEqual(persisted["status"], "QUEUED")
        self.assertNotIn("worker_pid", persisted)
        self.assertNotIn("spawned_at_unix", persisted)

    def test_a01_rejects_parent_traversal_write_set(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.submit_a01(
            str(self.workspace), 1, "main", "goal", ["../outside"], 3, 180, 0.05, None
        )
        self.assertEqual(result["result"], "BLOCKED")
        self.assertTrue(any(item.startswith("invalid_write_set:") for item in result["failures"]))

    def test_a01_rejects_windows_traversal_and_git_internal_write_set(self):
        failures = bridge._validate_write_set([r"..\outside", r"C:\temp\x", ".git/config"])
        self.assertEqual(len(failures), 3)

    def test_a01_rejects_option_like_base_ref(self):
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        result = bridge.submit_a01(
            str(self.workspace), 1, "--help", "goal", [], 3, 180, 0.05, None
        )
        self.assertEqual(result["result"], "BLOCKED")
        self.assertIn("base_ref_invalid", result["failures"])

    def test_invalid_run_id_is_not_found(self):
        result = bridge.status("not-a-run-id")
        self.assertEqual(result["result"], "NOT_FOUND")

    def test_record_identity_mismatch_is_rejected(self):
        run_id = "9" * 32
        bridge._json_write(
            bridge._record_path(run_id),
            {"schemaVersion": 1, "run_id": "8" * 32, "kind": "chat-work-agent", "status": "PASS"},
        )
        result = bridge.status(run_id)
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("record_integrity_invalid", result["failures"])

    def test_receipt_identity_mismatch_is_rejected(self):
        run_id = "a" * 32
        run_dir = bridge._record_path(run_id).parent
        receipt_dir = run_dir / "workflow" / "receipts"
        receipt_dir.mkdir(parents=True)
        bridge._json_write(
            bridge._record_path(run_id),
            {"schemaVersion": 1, "run_id": run_id, "kind": "a01-a10", "status": "PASS", "receipt_dir": str(receipt_dir)},
        )
        (receipt_dir / "A01.json").write_text(
            json.dumps({"run_id": "b" * 32, "actor_id": "A01", "result": "PASS"}),
            encoding="utf-8",
        )
        result = bridge.receipt_summary(run_id, "A01")
        self.assertEqual(result["result"], "FAIL")
        self.assertEqual(result["reason"], "receipt_identity_mismatch")

    def test_receipt_dir_outside_run_is_rejected(self):
        run_id = "c" * 32
        outside = pathlib.Path(self.temp.name) / "receipts"
        outside.mkdir()
        bridge._json_write(
            bridge._record_path(run_id),
            {"schemaVersion": 1, "run_id": run_id, "kind": "a01-a10", "status": "PASS", "receipt_dir": str(outside)},
        )
        result = bridge.receipt_summary(run_id, "A01")
        self.assertEqual(result["result"], "FAIL")
        self.assertEqual(result["reason"], "receipt_dir_outside_run")


if __name__ == "__main__":
    unittest.main()
