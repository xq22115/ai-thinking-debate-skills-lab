import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO = pathlib.Path(__file__).resolve().parents[2]
RUNTIME = REPO / "control-plane/scripts/ordinary_chat_task_runtime.py"


class OrdinaryChatTaskRuntimeTests(unittest.TestCase):
    def write_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def config(self):
        return {
            "requestSchemaVersion": 2,
            "intent": "ordinary_chat_task",
            "allowedModes": ["execute", "audit"],
            "maxSteps": 16,
            "maxReadChars": 10000,
            "maxSearchFileBytes": 100000,
            "maxSearchMatches": 50,
            "enabledActions": ["read_text", "search_text", "write_text", "replace_text", "json_set", "fetch_url", "run_recipe"],
            "mutation": {
                "globalAllowedPaths": ["docs/**", "control-plane/**"],
                "protectedPaths": ["control-plane/scripts/**", "control-plane/ordinary-chat-task-requests/**"]
            },
            "snapshotExclude": [".git/**", "state/**", "out/**"],
            "fetch": {"allowedHosts": ["example.invalid"], "maxBytes": 1024, "timeoutSeconds": 1},
            "recipes": {"defaultTimeoutSeconds": 30, "passEnv": ["PATH", "HOME"], "definitions": {}}
        }

    def base_request(self):
        return {
            "schemaVersion": 2,
            "request_id": "task-test-001",
            "goal": "Replace a real repository file and prove the resulting outcome.",
            "intent": "ordinary_chat_task",
            "mode": "execute",
            "mutation": {"required": True, "commit": False, "allowed_paths": ["docs/**"]},
            "steps": [
                {"id": "edit", "action": "replace_text", "with": {"path": "docs/example.txt", "find": "alpha", "replace": "beta", "expected_count": 1}}
            ],
            "acceptance": [
                {"type": "step_passed", "step_id": "edit"},
                {"type": "file_contains", "path": "docs/example.txt", "text": "beta"},
                {"type": "changed_path", "path": "docs/example.txt"},
                {"type": "no_unexpected_changes", "paths": ["docs/example.txt"]}
            ]
        }

    def run_runtime(self, cwd, *args):
        return subprocess.run([sys.executable, str(RUNTIME), *args], cwd=cwd, text=True, capture_output=True)

    def test_real_mutation_resume_and_five_method_adjudication(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            (root / "docs/example.txt").write_text("alpha\n", encoding="utf-8")
            self.write_json(root / "config.json", self.config())
            self.write_json(root / "request.json", self.base_request())
            primary = self.run_runtime(root, "execute", "--request", "request.json", "--config", "config.json", "--state", "state/state.json", "--output", "out/primary.json")
            self.assertEqual(primary.returncode, 0, primary.stderr)
            self.assertEqual((root / "docs/example.txt").read_text(encoding="utf-8"), "beta\n")
            first = json.loads((root / "out/primary.json").read_text(encoding="utf-8"))
            self.assertEqual(first["outcome"], "PASS")
            self.assertEqual(first["changed_paths"], ["docs/example.txt"])
            resume = self.run_runtime(root, "execute", "--request", "request.json", "--config", "config.json", "--state", "state/state.json", "--output", "out/resume.json", "--resume-probe")
            self.assertEqual(resume.returncode, 0, resume.stderr)
            replay = json.loads((root / "out/resume.json").read_text(encoding="utf-8"))
            self.assertEqual(replay["executed_steps"], 0)
            self.assertEqual(replay["resumed_steps"], 1)
            self.assertEqual(replay["changed_paths"], [])
            judged = self.run_runtime(root, "adjudicate", "--request", "request.json", "--primary", "out/primary.json", "--resume", "out/resume.json", "--output", "out/completion.json")
            self.assertEqual(judged.returncode, 0, judged.stderr)
            report = json.loads((root / "out/completion.json").read_text(encoding="utf-8"))
            self.assertEqual(report["result"], "PASS")
            self.assertEqual(report["completion_methods_passed"], 5)

    def test_rejects_command_field_in_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            (root / "docs/example.txt").write_text("alpha\n", encoding="utf-8")
            request = self.base_request()
            request["command"] = "echo forbidden"
            self.write_json(root / "config.json", self.config())
            self.write_json(root / "request.json", request)
            proc = self.run_runtime(root, "execute", "--request", "request.json", "--config", "config.json", "--state", "state/state.json", "--output", "out/result.json")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("unsupported top-level fields", proc.stderr)

    def test_protected_runtime_path_is_not_mutable(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            target = root / "control-plane/scripts/runtime.py"
            target.parent.mkdir(parents=True)
            target.write_text("old\n", encoding="utf-8")
            request = self.base_request()
            request["mutation"]["allowed_paths"] = ["control-plane/**"]
            request["steps"] = [{"id": "edit", "action": "write_text", "with": {"path": "control-plane/scripts/runtime.py", "content": "new\n"}}]
            request["acceptance"] = [{"type": "step_passed", "step_id": "edit"}]
            self.write_json(root / "config.json", self.config())
            self.write_json(root / "request.json", request)
            proc = self.run_runtime(root, "execute", "--request", "request.json", "--config", "config.json", "--state", "state/state.json", "--output", "out/result.json")
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(target.read_text(encoding="utf-8"), "old\n")

    def test_dependency_cycle_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            (root / "docs/example.txt").write_text("alpha\n", encoding="utf-8")
            request = self.base_request()
            request["mutation"]["required"] = False
            request["steps"] = [
                {"id": "a", "action": "read_text", "depends_on": ["b"], "with": {"path": "docs/example.txt"}},
                {"id": "b", "action": "read_text", "depends_on": ["a"], "with": {"path": "docs/example.txt"}}
            ]
            request["acceptance"] = [{"type": "step_passed", "step_id": "a"}]
            self.write_json(root / "config.json", self.config())
            self.write_json(root / "request.json", request)
            proc = self.run_runtime(root, "execute", "--request", "request.json", "--config", "config.json", "--state", "state/state.json", "--output", "out/result.json")
            self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
