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
        self.assertEqual(metadata["reasoning_effort"], "high")
        self.assertEqual(len(metadata["profile_sha256"]), 64)
        assignment = bound["assignments"][0]
        self.assertEqual(assignment["quality_profile_binding"]["profile_sha256"], metadata["profile_sha256"])
        self.assertEqual(assignment["quality_profile_binding"]["reasoning_effort"], "high")
        self.assertIn(BINDING_START, assignment["prompt"])
        self.assertIn(BINDING_END, assignment["prompt"])
        self.assertIn("first-pass correctness", assignment["prompt"])
        self.assertIn("runtime or user-path evidence", assignment["prompt"])
        self.assertIn("continue until PASS", assignment["prompt"])
        self.assertIn("reasoning_effort=high", assignment["prompt"])
        self.assertIn("WebSearch and WebFetch", assignment["prompt"])
        self.assertIn("token-by-token pacing", assignment["prompt"])

    def test_critical_route_binds_xhigh_effort(self) -> None:
        preparation = {
            "result": "PASS",
            "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
        }
        bound = bind_preparation(preparation, CONTROL_PLANE_ROOT, task_class="critical")
        self.assertEqual(bound["quality_profile_binding"]["reasoning_effort"], "xhigh")
        self.assertIn("reasoning_effort=xhigh", bound["assignments"][0]["prompt"])

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
                "reasoning_runtime": {"effort_by_task_class": {"material": "high"}},
                "release": {"pass_requires": ["verified"]},
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "quality_profile_not_default_enabled"):
                load_profile(root)

    def test_task_class_must_exist_in_profile(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "route-test",
                "default_enabled": True,
                "depth_router": {"simple": {"required_stages": ["verify"]}},
                "reasoning_runtime": {"effort_by_task_class": {"critical": "xhigh"}},
                "release": {"pass_requires": ["verified"]},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_route_missing:critical"):
                bind_preparation(preparation, root, task_class="critical")

    def test_task_class_must_have_runtime_effort(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "effort-test",
                "default_enabled": True,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "reasoning_runtime": {"effort_by_task_class": {}},
                "release": {"pass_requires": ["verified"]},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_reasoning_effort_missing:material"):
                bind_preparation(preparation, root, task_class="material")


if __name__ == "__main__":
    unittest.main()
