import importlib.util
import os
import pathlib
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "project_memory.py"
spec = importlib.util.spec_from_file_location("project_memory", MODULE_PATH)
assert spec and spec.loader
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


class ProjectMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name) / "allowed"
        self.root.mkdir()
        self.workspace = self.root / "project"
        self.workspace.mkdir()
        self.old_env = dict(os.environ)
        os.environ["ORDINARY_CHAT_ALLOWED_ROOTS"] = str(self.root)
        os.environ["ORDINARY_CHAT_STATE_DIR"] = str(pathlib.Path(self.temp.name) / "state")
        os.environ.pop("ORDINARY_CHAT_MEMORY_ALLOW_WRITE", None)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)
        self.temp.cleanup()

    def test_write_is_disabled_by_default(self):
        result = memory.add(str(self.workspace), "fact", "test", 1.0, "project", [])
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "memory_write_disabled")

    def test_explicit_add_search_delete_roundtrip(self):
        os.environ["ORDINARY_CHAT_MEMORY_ALLOW_WRITE"] = "true"
        added = memory.add(
            str(self.workspace),
            "MCP gateway uses the existing local agent runtime",
            "test-suite",
            0.9,
            "project",
            ["mcp", "agent"],
        )
        self.assertEqual(added["result"], "PASS")
        item_id = added["id"]

        found = memory.search(str(self.workspace), "MCP gateway", 10)
        self.assertEqual(found["result"], "PASS")
        self.assertEqual(len(found["items"]), 1)
        self.assertEqual(found["items"][0]["source"], "test-suite")
        self.assertEqual(found["items"][0]["confidence"], 0.9)

        deleted = memory.delete(str(self.workspace), item_id)
        self.assertEqual(deleted["result"], "PASS")
        self.assertTrue(deleted["deleted"])
        empty = memory.search(str(self.workspace), "MCP gateway", 10)
        self.assertEqual(empty["items"], [])

    def test_workspace_outside_allowlist_is_blocked(self):
        outside = pathlib.Path(self.temp.name) / "outside"
        outside.mkdir()
        result = memory.search(str(outside), "anything", 10)
        self.assertEqual(result["result"], "BLOCKED")
        self.assertEqual(result["reason"], "workspace_not_allowlisted")


if __name__ == "__main__":
    unittest.main()
