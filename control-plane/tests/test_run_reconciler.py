import importlib.util
import json
import os
import pathlib
import tempfile
import time
import unittest
from unittest import mock

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "run_reconciler.py"
spec = importlib.util.spec_from_file_location("run_reconciler", MODULE_PATH)
assert spec and spec.loader
reconciler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reconciler)


class RunReconcilerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_env = dict(os.environ)
        os.environ["ORDINARY_CHAT_STATE_DIR"] = str(pathlib.Path(self.temp.name) / "state")
        os.environ["ORDINARY_CHAT_STARTUP_GRACE_SECONDS"] = "5"

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)
        self.temp.cleanup()

    def _record(self, run_id: str, payload: dict) -> None:
        path = reconciler._record_path(run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_terminal_status_remains_terminal(self):
        run_id = "a" * 32
        self._record(run_id, {"status": "PASS", "worker_pid": 999999, "updated_at_unix": int(time.time())})
        result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "TERMINAL")
        self.assertEqual(result["effective_status"], "PASS")

    def test_missing_pid_within_grace_is_starting(self):
        run_id = "b" * 32
        self._record(run_id, {"status": "QUEUED", "updated_at_unix": int(time.time())})
        result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "STARTING")
        self.assertEqual(result["effective_status"], "QUEUED")

    def test_missing_pid_past_grace_is_stale(self):
        run_id = "c" * 32
        self._record(run_id, {"status": "RUNNING", "updated_at_unix": int(time.time()) - 30})
        result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "STALE")
        self.assertEqual(result["effective_status"], "STALE")

    def test_live_pid_is_live(self):
        run_id = "d" * 32
        self._record(run_id, {"status": "RUNNING", "worker_pid": 123, "updated_at_unix": int(time.time())})
        with mock.patch.object(reconciler, "_pid_alive", return_value=True):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "LIVE")
        self.assertEqual(result["effective_status"], "RUNNING")

    def test_dead_pid_is_stale(self):
        run_id = "e" * 32
        self._record(run_id, {"status": "RUNNING", "worker_pid": 123, "updated_at_unix": int(time.time())})
        with mock.patch.object(reconciler, "_pid_alive", return_value=False):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "STALE")
        self.assertEqual(result["reason"], "worker_pid_not_alive")

    def test_invalid_run_id_is_not_found(self):
        result = reconciler.inspect("bad")
        self.assertEqual(result["result"], "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
