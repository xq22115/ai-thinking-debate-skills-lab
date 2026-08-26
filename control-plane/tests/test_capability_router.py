import importlib.util
import json
import os
import pathlib
import stat
import sys
import tempfile
import time
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

health_spec = importlib.util.spec_from_file_location("capability_health", SCRIPTS / "capability_health.py")
assert health_spec and health_spec.loader
health = importlib.util.module_from_spec(health_spec)
sys.modules["capability_health"] = health
health_spec.loader.exec_module(health)

router_spec = importlib.util.spec_from_file_location("capability_router", SCRIPTS / "capability_router.py")
assert router_spec and router_spec.loader
router = importlib.util.module_from_spec(router_spec)
router_spec.loader.exec_module(router)


class CapabilityRouterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = pathlib.Path(self.temp.name)
        self.bin_dir = self.base / "bin"
        self.bin_dir.mkdir()
        self.old_env = dict(os.environ)
        os.environ["ORDINARY_CHAT_STATE_DIR"] = str(self.base / "state")
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

    def _cache_path(self) -> pathlib.Path:
        return health._state_dir() / "health" / "capability-health.json"

    def test_health_distinguishes_external_and_local_readiness(self):
        browser = self._exe("browser-use")
        os.environ["BROWSER_USE_BIN"] = str(browser)
        payload = health.snapshot(persist=False, ttl_seconds=30)
        self.assertEqual(payload["result"], "PASS")
        self.assertIsNone(payload["capabilities"]["github-native"]["ready"])
        self.assertTrue(payload["capabilities"]["browser-use-cli"]["ready"])
        self.assertFalse(payload["capabilities"]["playwright-cli"]["ready"])

    def test_persisted_health_cache_is_private_on_posix(self):
        health.snapshot(persist=True, ttl_seconds=30)
        path = self._cache_path()
        self.assertTrue(path.is_file())
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

    def test_health_cache_roundtrip(self):
        first = health.cached_or_snapshot()
        self.assertEqual(first["cache"], "MISS")
        second = health.cached_or_snapshot()
        self.assertEqual(second["cache"], "HIT")

    def test_corrupt_health_cache_fails_closed_and_reprobes(self):
        path = self._cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not-json", encoding="utf-8")
        result = health.cached_or_snapshot()
        self.assertEqual(result["cache"], "MISS")
        self.assertEqual(result["result"], "PASS")

    def test_forged_far_future_cache_is_rejected(self):
        path = self._cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        now = int(time.time())
        path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "generated_at_unix": now,
                    "expires_at_unix": now + 86400,
                    "ttl_seconds": 86400,
                    "capabilities": {
                        "browser-use-cli": {"state": "ready", "ready": True},
                    },
                    "result": "PASS",
                }
            ),
            encoding="utf-8",
        )
        result = health.cached_or_snapshot()
        self.assertEqual(result["cache"], "MISS")
        self.assertFalse(result["capabilities"]["browser-use-cli"]["ready"])

    def test_expired_cache_is_reprobed(self):
        path = self._cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        now = int(time.time())
        path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "generated_at_unix": now - 30,
                    "expires_at_unix": now - 1,
                    "ttl_seconds": 29,
                    "capabilities": {
                        "browser-use-cli": {"state": "ready", "ready": True},
                    },
                    "result": "PASS",
                }
            ),
            encoding="utf-8",
        )
        result = health.cached_or_snapshot()
        self.assertEqual(result["cache"], "MISS")
        self.assertFalse(result["capabilities"]["browser-use-cli"]["ready"])

    def test_adaptive_browser_prefers_browser_use_when_ready(self):
        browser = self._exe("browser-use")
        os.environ["BROWSER_USE_BIN"] = str(browser)
        result = router.route("browser_adaptive", require_ready=True)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["selected"]["id"], "browser-use-cli")

    def test_adaptive_browser_falls_back_to_playwright_cli_when_only_ready_backend(self):
        playwright = self._exe("playwright-cli")
        os.environ["PLAYWRIGHT_CLI_BIN"] = str(playwright)
        result = router.route("browser_adaptive", require_ready=True)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["selected"]["id"], "playwright-cli")

    def test_deterministic_browser_prefers_playwright_when_ready(self):
        playwright = self._exe("playwright-cli")
        os.environ["PLAYWRIGHT_CLI_BIN"] = str(playwright)
        result = router.route("browser_deterministic", require_ready=True)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["selected"]["id"], "playwright-cli")

    def test_long_local_prefers_configured_chat_agent(self):
        agent = self._exe("chat-work-agent")
        os.environ["CHAT_WORK_AGENT_PATH"] = str(agent)
        result = router.route("local_long", require_ready=True)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["selected"]["id"], "chat-work-agent")

    def test_long_local_falls_back_to_a01_when_chat_agent_unavailable(self):
        claude = self._exe("claude")
        os.environ["CLAUDE_PATH"] = str(claude)
        result = router.route("local_long", require_ready=True)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["selected"]["id"], "a01-a10-runtime")

    def test_repository_action_is_conditional_until_host_preflight(self):
        result = router.route("repository_action")
        self.assertEqual(result["result"], "CONDITIONAL")
        self.assertEqual(result["selected"]["id"], "github-native")
        self.assertTrue(result["selected"]["preflight_required"])

    def test_require_ready_blocks_when_only_conditional_route_exists(self):
        result = router.route("repository_action", require_ready=True)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "no_compatible_ready_route")

    def test_write_request_does_not_route_to_read_only_project_memory(self):
        result = router.route("project_recall", needs_write=True)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "no_compatible_route")
        self.assertEqual(result["candidates"][0]["state"], "INCOMPATIBLE")

    def test_invalid_intent_is_blocked(self):
        result = router.route("not-real")
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "intent_invalid")


if __name__ == "__main__":
    unittest.main()
