import importlib.util
import os
import pathlib
import sys
import tempfile
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

    def test_health_distinguishes_external_and_local_readiness(self):
        browser = self._exe("browser-use")
        os.environ["BROWSER_USE_BIN"] = str(browser)
        payload = health.snapshot(persist=False, ttl_seconds=30)
        self.assertEqual(payload["result"], "PASS")
        self.assertIsNone(payload["capabilities"]["github-native"]["ready"])
        self.assertTrue(payload["capabilities"]["browser-use-cli"]["ready"])
        self.assertFalse(payload["capabilities"]["playwright-cli"]["ready"])

    def test_health_cache_roundtrip(self):
        first = health.cached_or_snapshot()
        self.assertEqual(first["cache"], "MISS")
        second = health.cached_or_snapshot()
        self.assertEqual(second["cache"], "HIT")

    def test_adaptive_browser_prefers_browser_use_when_ready(self):
        browser = self._exe("browser-use")
        os.environ["BROWSER_USE_BIN"] = str(browser)
        result = router.route("browser_adaptive", require_ready=True)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["selected"]["id"], "browser-use-cli")

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

    def test_repository_action_is_conditional_until_host_preflight(self):
        result = router.route("repository_action")
        self.assertEqual(result["result"], "CONDITIONAL")
        self.assertEqual(result["selected"]["id"], "github-native")
        self.assertTrue(result["selected"]["preflight_required"])

    def test_require_ready_blocks_when_only_conditional_route_exists(self):
        result = router.route("repository_action", require_ready=True)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "no_compatible_ready_route")

    def test_invalid_intent_is_blocked(self):
        result = router.route("not-real")
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "intent_invalid")


if __name__ == "__main__":
    unittest.main()
