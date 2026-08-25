from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from continuous_thinking_runtime_binding import (
    BINDING_END,
    BINDING_START,
    bind_preparation,
    load_profile,
)

CONTROL_PLANE_ROOT = pathlib.Path(__file__).resolve().parents[1]


class ContinuousThinkingRuntimeBindingTests(unittest.TestCase):
    def test_real_profile_is_bound_with_hash_attestation(self) -> None:
        preparation = {
            "result": "PASS",
            "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
        }
        bound = bind_preparation(preparation, CONTROL_PLANE_ROOT, task_class="material")
        metadata = bound["quality_profile_binding"]
        self.assertTrue(metadata["bound"])
        self.assertEqual(metadata["assignment_count"], 1)
        self.assertEqual(len(metadata["profile_sha256"]), 64)
        assignment = bound["assignments"][0]
        self.assertEqual(assignment["quality_profile_binding"]["profile_sha256"], metadata["profile_sha256"])
        self.assertIn(BINDING_START, assignment["prompt"])
        self.assertIn(BINDING_END, assignment["prompt"])
        self.assertIn("first-pass correctness", assignment["prompt"])
        self.assertIn("runtime or user-path evidence", assignment["prompt"])
        self.assertIn("continue until PASS", assignment["prompt"])
        self.assertIn("perform actual tool-backed research before release", assignment["prompt"])
        self.assertIn("observable tool/source evidence", assignment["prompt"])
        self.assertIn("delayed output cannot satisfy a research request", assignment["prompt"])
        self.assertIn("token-by-token throttling", assignment["prompt"])
        self.assertIn("deliberate chunk pauses", assignment["prompt"])
        self.assertIn("slow streaming is not evidence of deep reasoning", assignment["prompt"])

    def test_rebinding_same_profile_is_idempotent(self) -> None:
        preparation = {
            "result": "PASS",
            "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
        }
        once = bind_preparation(preparation, CONTROL_PLANE_ROOT, task_class="critical")
        twice = bind_preparation(once, CONTROL_PLANE_ROOT, task_class="critical")
        self.assertEqual(once, twice)
        self.assertEqual(twice["assignments"][0]["prompt"].count(BINDING_START), 1)

    def test_nonpass_preparation_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "preparation_not_pass"):
            bind_preparation({"result": "VETO", "assignments": [{}]}, CONTROL_PLANE_ROOT)

    def test_disabled_profile_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "disabled-test",
                "default_enabled": False,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "release": {"pass_requires": ["verified"]},
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "quality_profile_not_default_enabled"):
                load_profile(root)

    def test_missing_research_evidence_gate_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "research-gate-test",
                "default_enabled": True,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "release": {"pass_requires": ["verified"]},
                "output_delivery": {"artificial_output_throttling_forbidden": True},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_research_evidence_gate_missing"):
                bind_preparation(preparation, root, task_class="material")

    def test_missing_output_throttling_guard_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "delivery-guard-test",
                "default_enabled": True,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "release": {"pass_requires": ["verified"]},
                "research_and_experience": {"triggered_research_requires_tool_backed_evidence": True},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_output_throttling_guard_missing"):
                bind_preparation(preparation, root, task_class="material")

    def test_task_class_must_exist_in_profile(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "route-test",
                "default_enabled": True,
                "depth_router": {"simple": {"required_stages": ["verify"]}},
                "release": {"pass_requires": ["verified"]},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_route_missing:critical"):
                bind_preparation(preparation, root, task_class="critical")


if __name__ == "__main__":
    unittest.main()
