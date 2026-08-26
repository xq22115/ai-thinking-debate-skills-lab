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
        os.environ["ORDINARY_CHAT_LIVENESS_MAX_SILENCE_SECONDS"] = "30"
        os.environ["ORDINARY_CHAT_PROCESS_START_TOLERANCE_SECONDS"] = "15"

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

    def test_live_pid_with_matching_process_birth_is_live(self):
        run_id = "d" * 32
        started = int(time.time()) - 2
        self._record(
            run_id,
            {
                "status": "RUNNING",
                "worker_pid": 123,
                "worker_started_at_unix": started,
                "updated_at_unix": int(time.time()),
            },
        )
        with (
            mock.patch.object(reconciler, "_pid_alive", return_value=True),
            mock.patch.object(reconciler, "_process_start_unix", return_value=started - 1),
        ):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "LIVE")
        self.assertEqual(result["effective_status"], "RUNNING")
        self.assertEqual(result["process_identity"], "MATCH")

    def test_reused_live_pid_is_not_reported_live(self):
        run_id = "e" * 32
        started = int(time.time()) - 120
        self._record(
            run_id,
            {
                "status": "RUNNING",
                "worker_pid": 123,
                "worker_started_at_unix": started,
                "updated_at_unix": int(time.time()),
            },
        )
        with (
            mock.patch.object(reconciler, "_pid_alive", return_value=True),
            mock.patch.object(reconciler, "_process_start_unix", return_value=started + 90),
        ):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "STALE")
        self.assertEqual(result["effective_status"], "STALE")
        self.assertEqual(result["reason"], "worker_pid_reused_or_identity_mismatch")

    def test_live_pid_without_process_identity_is_conditional(self):
        run_id = "f" * 32
        started = int(time.time()) - 2
        self._record(
            run_id,
            {
                "status": "RUNNING",
                "worker_pid": 123,
                "worker_started_at_unix": started,
                "updated_at_unix": int(time.time()),
            },
        )
        with (
            mock.patch.object(reconciler, "_pid_alive", return_value=True),
            mock.patch.object(reconciler, "_process_start_unix", return_value=None),
        ):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "LIVE_UNCONFIRMED")
        self.assertEqual(result["result"], "CONDITIONAL")

    def test_alive_but_silent_worker_is_suspect_not_pass_live(self):
        run_id = "1" * 32
        started = int(time.time()) - 100
        self._record(
            run_id,
            {
                "status": "RUNNING",
                "worker_pid": 123,
                "worker_started_at_unix": started,
                "updated_at_unix": int(time.time()) - 90,
            },
        )
        with (
            mock.patch.object(reconciler, "_pid_alive", return_value=True),
            mock.patch.object(reconciler, "_process_start_unix", return_value=started),
        ):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "SUSPECT")
        self.assertEqual(result["result"], "CONDITIONAL")
        self.assertEqual(result["reason"], "worker_alive_but_record_silent_past_threshold")

    def test_dead_pid_is_stale(self):
        run_id = "2" * 32
        self._record(run_id, {"status": "RUNNING", "worker_pid": 123, "updated_at_unix": int(time.time())})
        with mock.patch.object(reconciler, "_pid_alive", return_value=False):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "STALE")
        self.assertEqual(result["reason"], "worker_pid_not_alive")

    def test_unknown_pid_probe_is_conditional(self):
        run_id = "3" * 32
        self._record(run_id, {"status": "RUNNING", "worker_pid": 123, "updated_at_unix": int(time.time())})
        with mock.patch.object(reconciler, "_pid_alive", return_value=None):
            result = reconciler.inspect(run_id)
        self.assertEqual(result["liveness"], "UNKNOWN")
        self.assertEqual(result["result"], "CONDITIONAL")

    def test_invalid_run_id_is_not_found(self):
        result = reconciler.inspect("bad")
        self.assertEqual(result["result"], "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
