import hashlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


health = _load("capability_health", SCRIPTS / "capability_health.py")
router = _load("capability_router", SCRIPTS / "capability_router.py")
bridge = _load("ordinary_chat_bridge_chaos", SCRIPTS / "ordinary_chat_bridge.py")
reconciler = _load("run_reconciler_chaos", SCRIPTS / "run_reconciler.py")


class OrdinaryChatChaosTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = pathlib.Path(self.temp.name)
        self.state = self.base / "state"
        self.allowed = self.base / "allowed"
        self.allowed.mkdir()
        self.workspace = self.allowed / "workspace"
        self.workspace.mkdir()
        self.bin_dir = self.base / "bin"
        self.bin_dir.mkdir()
        self.old_env = dict(os.environ)
        os.environ["ORDINARY_CHAT_STATE_DIR"] = str(self.state)
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.allowed)
        os.environ["PATH"] = str(self.bin_dir)
        for name in ["CHAT_WORK_AGENT_PATH", "CLAUDE_PATH", "PLAYWRIGHT_CLI_BIN", "BROWSER_USE_BIN"]:
            os.environ.pop(name, None)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)
        self.temp.cleanup()

    def _exe(self, name: str) -> pathlib.Path:
        path = self.bin_dir / name
        path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        path.chmod(0o755)
        return path

    def _record(self, run_id: str, **updates) -> pathlib.Path:
        payload = {
            "schemaVersion": 1,
            "run_id": run_id,
            "kind": "chat-work-agent",
            "status": "QUEUED",
            "goal_sha256": hashlib.sha256(b"goal").hexdigest(),
            "created_at_unix": int(time.time()),
            "updated_at_unix": int(time.time()),
        }
        payload.update(updates)
        path = bridge._record_path(run_id)
        bridge._json_write(path, payload)
        return path

    def test_require_ready_does_not_trust_backend_that_disappears_after_cache(self):
        browser = self._exe("browser-use")
        os.environ["BROWSER_USE_BIN"] = str(browser)
        warm = health.cached_or_snapshot()
        self.assertTrue(warm["capabilities"]["browser-use-cli"]["ready"])
        self.assertEqual(health.cached_or_snapshot()["cache"], "HIT")
        browser.unlink()

        decision = router.route("browser_adaptive", require_ready=True)
        self.assertEqual(decision["health_probe"], "FRESH")
        self.assertEqual(decision["result"], "BLOCKED")
        candidate = next(item for item in decision["candidates"] if item["id"] == "browser-use-cli")
        self.assertFalse(candidate["ready"])

    def test_corrupted_spec_becomes_terminal_failure_instead_of_silent_worker_exit(self):
        run_id = "a" * 32
        self._record(run_id)
        spec_path = bridge._record_path(run_id).parent / "spec.json"
        spec_path.write_text("{truncated", encoding="utf-8")

        bridge.worker(str(spec_path))

        record = bridge.status(run_id)
        self.assertEqual(record["status"], "FAIL")
        self.assertIn("worker_spec_unreadable", record["failures"])
        self.assertFalse(spec_path.exists())

    def test_spec_run_id_confusion_cannot_mutate_another_run(self):
        run_a = "b" * 32
        run_b = "c" * 32
        self._record(run_a)
        self._record(run_b, status="PASS")
        spec_path = bridge._record_path(run_a).parent / "spec.json"
        bridge._json_write(
            spec_path,
            {
                "run_id": run_b,
                "kind": "chat-work-agent",
                "workspace": str(self.workspace),
                "goal": "goal",
            },
        )

        bridge.worker(str(spec_path))

        a = bridge.status(run_a)
        b = bridge.status(run_b)
        self.assertEqual(a["status"], "FAIL")
        self.assertIn("worker_spec_run_id_mismatch", a["failures"])
        self.assertEqual(b["status"], "PASS")
        self.assertNotIn("worker_spec_run_id_mismatch", b.get("failures", []))

    def test_bridge_rejects_parseable_record_copied_from_another_run(self):
        run_a = "d" * 32
        run_b = "e" * 32
        path = bridge._record_path(run_a)
        bridge._json_write(path, {"schemaVersion": 1, "run_id": run_b, "status": "PASS"})
        result = bridge.status(run_a)
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("record_integrity_invalid", result["failures"])

    def test_liveness_rejects_record_copied_from_another_run(self):
        run_a = "f" * 32
        run_b = "0" * 32
        path = reconciler._record_path(run_a)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"schemaVersion": 1, "run_id": run_b, "status": "PASS"}),
            encoding="utf-8",
        )
        result = reconciler.inspect(run_a)
        self.assertEqual(result["result"], "FAIL")
        self.assertEqual(result["reason"], "record_integrity_invalid")

    def test_truncated_record_fails_closed_in_bridge_and_liveness(self):
        run_id = "1" * 32
        path = bridge._record_path(run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{", encoding="utf-8")
        bridge_result = bridge.status(run_id)
        liveness_result = reconciler.inspect(run_id)
        self.assertEqual(bridge_result["result"], "FAIL")
        self.assertIn("record_unreadable", bridge_result["failures"])
        self.assertEqual(liveness_result["result"], "FAIL")
        self.assertEqual(liveness_result["reason"], "record_unreadable")

    def test_real_process_kill_transitions_liveness_from_live_to_stale(self):
        run_id = "2" * 32
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            observed = None
            deadline = time.time() + 5
            while time.time() < deadline and observed is None:
                observed = reconciler._process_start_unix(proc.pid)
                if observed is None:
                    time.sleep(0.05)
            self.assertIsNotNone(observed)
            now = int(time.time())
            self._record(
                run_id,
                status="RUNNING",
                worker_pid=proc.pid,
                worker_started_at_unix=observed,
                updated_at_unix=now,
            )
            live = reconciler.inspect(run_id)
            self.assertEqual(live["liveness"], "LIVE")
            self.assertEqual(live["process_identity"], "MATCH")

            proc.kill()
            proc.wait(timeout=5)
            stale = reconciler.inspect(run_id)
            self.assertEqual(stale["liveness"], "STALE")
            self.assertEqual(stale["effective_status"], "STALE")
            self.assertEqual(stale["reason"], "worker_pid_not_alive")
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
