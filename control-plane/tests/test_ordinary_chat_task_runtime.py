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

    def config(self, recipes=None):
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
                "protectedPaths": ["control-plane/scripts/**", "control-plane/ordinary-chat-task-requests/**", "control-plane/ordinary-chat-task-results/**"]
            },
            "snapshotExclude": [".git/**", "state/**", "out/**"],
            "fetch": {"allowedHosts": ["example.invalid"], "maxBytes": 1024, "timeoutSeconds": 1},
            "recipes": {"defaultTimeoutSeconds": 30, "passEnv": ["PATH", "HOME"], "definitions": recipes or {}}
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

    def execute(self, root, request, config=None, state="state/state.json", output="out/result.json", resume=False):
        self.write_json(root / "config.json", config or self.config())
        self.write_json(root / "request.json", request)
        args = ["execute", "--request", "request.json", "--config", "config.json", "--state", state, "--output", output]
        if resume:
            args.append("--resume-probe")
        return self.run_runtime(root, *args)

    def test_real_mutation_resume_and_five_method_adjudication(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            (root / "docs/example.txt").write_text("alpha\n", encoding="utf-8")
            request = self.base_request()
            primary = self.execute(root, request, output="out/primary.json")
            self.assertEqual(primary.returncode, 0, primary.stderr)
            self.assertEqual((root / "docs/example.txt").read_text(encoding="utf-8"), "beta\n")
            first = json.loads((root / "out/primary.json").read_text(encoding="utf-8"))
            self.assertEqual(first["outcome"], "PASS")
            self.assertEqual(first["changed_paths"], ["docs/example.txt"])
            resume = self.execute(root, request, output="out/resume.json", resume=True)
            self.assertEqual(resume.returncode, 0, resume.stderr)
            replay = json.loads((root / "out/resume.json").read_text(encoding="utf-8"))
            self.assertEqual(replay["executed_steps"], 0)
            self.assertEqual(replay["resumed_steps"], 1)
            self.assertEqual(replay["changed_paths"], [])
            self.assertEqual(replay["acceptance_changed_paths_basis"], ["docs/example.txt"])
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
            proc = self.execute(root, request)
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
            proc = self.execute(root, request)
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
            proc = self.execute(root, request)
            self.assertNotEqual(proc.returncode, 0)

    def test_hidden_dot_path_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            target = root / ".github/example.txt"
            target.parent.mkdir(parents=True)
            target.write_text("hidden-path-ok\n", encoding="utf-8")
            request = {
                "schemaVersion": 2,
                "request_id": "task-hidden-001",
                "goal": "Read an exact dot-prefixed repository path without corrupting its name.",
                "intent": "ordinary_chat_task",
                "mode": "audit",
                "mutation": {"required": False, "commit": False, "allowed_paths": []},
                "steps": [{"id": "read", "action": "read_text", "with": {"path": ".github/example.txt"}}],
                "acceptance": [{"type": "step_passed", "step_id": "read"}]
            }
            proc = self.execute(root, request)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((root / "out/result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["steps"]["read"]["evidence"]["path"], ".github/example.txt")

    def test_audit_mode_rejects_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            request = self.base_request()
            request["mode"] = "audit"
            request["mutation"] = {"required": False, "commit": False, "allowed_paths": ["docs/**"]}
            request["steps"] = [{"id": "write", "action": "write_text", "with": {"path": "docs/x.txt", "content": "x"}}]
            request["acceptance"] = [{"type": "step_passed", "step_id": "write"}]
            proc = self.execute(root, request)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse((root / "docs/x.txt").exists())

    def test_state_rejects_changed_request_revision(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            (root / "docs/example.txt").write_text("alpha\n", encoding="utf-8")
            request = {
                "schemaVersion": 2,
                "request_id": "task-state-001",
                "goal": "Read a file once and bind the saved state to the exact request revision.",
                "intent": "ordinary_chat_task",
                "mode": "audit",
                "mutation": {"required": False, "commit": False, "allowed_paths": []},
                "steps": [{"id": "read", "action": "read_text", "with": {"path": "docs/example.txt"}}],
                "acceptance": [{"type": "step_passed", "step_id": "read"}]
            }
            first = self.execute(root, request)
            self.assertEqual(first.returncode, 0, first.stderr)
            request["goal"] += " Changed after state creation."
            second = self.execute(root, request, output="out/second.json", resume=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("different request revision", second.stderr)

    def test_dependency_execution_is_deterministic_even_when_dependency_appears_later(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            request = {
                "schemaVersion": 2,
                "request_id": "task-order-001",
                "goal": "Execute a later-declared producer before its dependent consumer deterministically.",
                "intent": "ordinary_chat_task",
                "mode": "execute",
                "mutation": {"required": True, "commit": False, "allowed_paths": ["docs/value.txt"]},
                "steps": [
                    {"id": "consumer", "action": "read_text", "depends_on": ["producer"], "with": {"path": "docs/value.txt"}},
                    {"id": "producer", "action": "write_text", "with": {"path": "docs/value.txt", "content": "ready\n"}}
                ],
                "acceptance": [
                    {"type": "step_passed", "step_id": "producer"},
                    {"type": "step_passed", "step_id": "consumer"},
                    {"type": "file_contains", "path": "docs/value.txt", "text": "ready"},
                    {"type": "no_unexpected_changes", "paths": ["docs/value.txt"]}
                ]
            }
            proc = self.execute(root, request)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((root / "out/result.json").read_text(encoding="utf-8"))
            self.assertIn("ready", result["steps"]["consumer"]["evidence"]["text"])

    def test_registry_recipe_side_effect_outside_request_scope_vetoes_completion(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "docs").mkdir()
            recipes = {
                "bad-side-effect": {
                    "commands": [{
                        "argv": [sys.executable, "-c", "from pathlib import Path; Path('docs/unexpected.txt').write_text('oops\\n')"],
                        "cwd": ".",
                        "timeoutSeconds": 30
                    }]
                }
            }
            request = {
                "schemaVersion": 2,
                "request_id": "task-sidefx-001",
                "goal": "Detect and veto an undeclared side effect even when a registered recipe exits zero.",
                "intent": "ordinary_chat_task",
                "mode": "execute",
                "mutation": {"required": False, "commit": False, "allowed_paths": ["docs/expected.txt"]},
                "steps": [{"id": "recipe", "action": "run_recipe", "with": {"recipe": "bad-side-effect"}}],
                "acceptance": [{"type": "step_passed", "step_id": "recipe"}]
            }
            proc = self.execute(root, request, config=self.config(recipes))
            self.assertNotEqual(proc.returncode, 0)
            result = json.loads((root / "out/result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["outcome"], "FAIL")
            self.assertEqual(result["unexpected_changes"], ["docs/unexpected.txt"])

    def test_unknown_recipe_fails_without_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            request = {
                "schemaVersion": 2,
                "request_id": "task-recipe-001",
                "goal": "Reject an unknown executable recipe rather than inventing or falling back to shell.",
                "intent": "ordinary_chat_task",
                "mode": "execute",
                "mutation": {"required": False, "commit": False, "allowed_paths": []},
                "steps": [{"id": "recipe", "action": "run_recipe", "with": {"recipe": "does-not-exist"}}],
                "acceptance": [{"type": "step_passed", "step_id": "recipe"}]
            }
            proc = self.execute(root, request)
            self.assertNotEqual(proc.returncode, 0)
            result = json.loads((root / "out/result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["steps"]["recipe"]["status"], "FAIL")
            self.assertIn("unknown recipe", result["steps"]["recipe"]["reason"])


if __name__ == "__main__":
    unittest.main()
