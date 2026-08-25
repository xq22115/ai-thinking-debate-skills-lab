import importlib.util
import os
import pathlib
import stat
import tempfile
import time
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
        os.environ.pop("ORDINARY_CHAT_MEMORY_EPHEMERAL_TTL_SECONDS", None)

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

    def test_memory_files_are_private(self):
        os.environ["ORDINARY_CHAT_MEMORY_ALLOW_WRITE"] = "true"
        result = memory.add(str(self.workspace), "private fact", "test", 1.0, "project", [])
        self.assertEqual(result["result"], "PASS")
        state_mode = stat.S_IMODE(memory._state_dir().stat().st_mode)
        memory_mode = stat.S_IMODE(memory._memory_dir().stat().st_mode)
        db_mode = stat.S_IMODE(memory._db_path(self.workspace.resolve()).stat().st_mode)
        self.assertEqual(state_mode, 0o700)
        self.assertEqual(memory_mode, 0o700)
        self.assertEqual(db_mode, 0o600)

    def test_like_wildcards_are_searched_literally(self):
        os.environ["ORDINARY_CHAT_MEMORY_ALLOW_WRITE"] = "true"
        memory.add(str(self.workspace), "literal % marker", "test", 1.0, "project", [])
        memory.add(str(self.workspace), "literal X marker", "test", 1.0, "project", [])
        found = memory.search(str(self.workspace), "%", 10)
        self.assertEqual([item["content"] for item in found["items"]], ["literal % marker"])

    def test_ephemeral_items_expire(self):
        os.environ["ORDINARY_CHAT_MEMORY_ALLOW_WRITE"] = "true"
        os.environ["ORDINARY_CHAT_MEMORY_EPHEMERAL_TTL_SECONDS"] = "60"
        added = memory.add(str(self.workspace), "short-lived", "test", 1.0, "ephemeral", [])
        self.assertEqual(added["result"], "PASS")
        with memory._database(self.workspace.resolve()) as db:
            db.execute(
                "UPDATE memory_items SET created_at = ? WHERE id = ?",
                (int(time.time()) - 120, added["id"]),
            )
        found = memory.search(str(self.workspace), "short-lived", 10)
        self.assertEqual(found["items"], [])
        self.assertGreaterEqual(found["purged_expired"], 1)

    def test_invalid_source_tags_and_delete_id_are_blocked(self):
        os.environ["ORDINARY_CHAT_MEMORY_ALLOW_WRITE"] = "true"
        empty_source = memory.add(str(self.workspace), "fact", "   ", 1.0, "project", [])
        self.assertEqual(empty_source["reason"], "source_empty")
        bad_tag = memory.add(str(self.workspace), "fact", "test", 1.0, "project", [""])
        self.assertEqual(bad_tag["reason"], "tag_invalid")
        bad_delete = memory.delete(str(self.workspace), "not-an-id")
        self.assertEqual(bad_delete["reason"], "id_invalid")


if __name__ == "__main__":
    unittest.main()
