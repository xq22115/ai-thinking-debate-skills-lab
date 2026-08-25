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


def _runtime(efforts=None) -> dict:
    return {
        "effort_by_task_class": efforts or {
            "simple": "medium",
            "material": "xhigh",
            "critical": "max",
        },
        "effort_must_be_runtime_bound": True,
    }


def _research_policy(*, with_attestation=True) -> dict:
    value = {"triggered_research_requires_tool_backed_evidence": True}
    if with_attestation:
        value["runtime_attestation"] = {
            "required_successful_tools_for_material_or_critical": ["WebSearch", "WebFetch"]
        }
    return value


class ContinuousThinkingRuntimeBindingTests(unittest.TestCase):
    def test_real_profile_is_bound_with_hash_attestation_and_effort(self) -> None:
        preparation = {
            "result": "PASS",
            "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
        }
        bound = bind_preparation(preparation, CONTROL_PLANE_ROOT, task_class="material")
        metadata = bound["quality_profile_binding"]
        self.assertTrue(metadata["bound"])
        self.assertEqual(metadata["assignment_count"], 1)
        self.assertEqual(metadata["reasoning_effort"], "xhigh")
        self.assertEqual(len(metadata["profile_sha256"]), 64)
        assignment = bound["assignments"][0]
        self.assertEqual(assignment["quality_profile_binding"]["profile_sha256"], metadata["profile_sha256"])
        self.assertEqual(assignment["quality_profile_binding"]["reasoning_effort"], "xhigh")
        self.assertIn(BINDING_START, assignment["prompt"])
        self.assertIn(BINDING_END, assignment["prompt"])
        self.assertIn("reasoning_effort=xhigh", assignment["prompt"])
        self.assertIn("first-pass correctness", assignment["prompt"])
        self.assertIn("runtime or user-path evidence", assignment["prompt"])
        self.assertIn("continue until PASS", assignment["prompt"])
        self.assertIn("perform actual tool-backed research before release", assignment["prompt"])
        self.assertIn("observable tool/source evidence", assignment["prompt"])
        self.assertIn("delayed output cannot satisfy a research request", assignment["prompt"])
        self.assertIn("PostToolUse runtime receipt", assignment["prompt"])
        self.assertIn("WebSearch and WebFetch", assignment["prompt"])
        self.assertIn("token-by-token throttling", assignment["prompt"])
        self.assertIn("deliberate chunk pauses", assignment["prompt"])
        self.assertIn("slow streaming is not evidence of deep reasoning", assignment["prompt"])

    def test_critical_route_binds_max_effort(self) -> None:
        preparation = {
            "result": "PASS",
            "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
        }
        bound = bind_preparation(preparation, CONTROL_PLANE_ROOT, task_class="critical")
        self.assertEqual(bound["quality_profile_binding"]["reasoning_effort"], "max")
        self.assertIn("reasoning_effort=max", bound["assignments"][0]["prompt"])

    def test_simple_route_binds_medium_effort(self) -> None:
        preparation = {
            "result": "PASS",
            "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
        }
        bound = bind_preparation(preparation, CONTROL_PLANE_ROOT, task_class="simple")
        self.assertEqual(bound["quality_profile_binding"]["reasoning_effort"], "medium")
        self.assertIn("never browse ceremonially", bound["assignments"][0]["prompt"])

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

    def test_missing_reasoning_effort_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "effort-test",
                "default_enabled": True,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "reasoning_runtime": {"effort_by_task_class": {}, "effort_must_be_runtime_bound": True},
                "release": {"pass_requires": ["verified"]},
                "research_and_experience": _research_policy(),
                "output_delivery": {"artificial_output_throttling_forbidden": True},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_reasoning_effort_missing:material"):
                bind_preparation(preparation, root, task_class="material")

    def test_missing_research_evidence_gate_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "research-gate-test",
                "default_enabled": True,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "reasoning_runtime": _runtime({"material": "xhigh"}),
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
                "reasoning_runtime": _runtime({"material": "xhigh"}),
                "release": {"pass_requires": ["verified"]},
                "research_and_experience": _research_policy(),
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_output_throttling_guard_missing"):
                bind_preparation(preparation, root, task_class="material")

    def test_missing_deep_research_tool_attestation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            profile_path = root / "ai-system/configs/continuous-thinking-global.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps({
                "profile_id": "attestation-test",
                "default_enabled": True,
                "depth_router": {"material": {"required_stages": ["verify"]}},
                "reasoning_runtime": _runtime({"material": "xhigh"}),
                "release": {"pass_requires": ["verified"]},
                "research_and_experience": _research_policy(with_attestation=False),
                "output_delivery": {"artificial_output_throttling_forbidden": True},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_deep_research_tool_attestation_missing"):
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
                "reasoning_runtime": _runtime({"critical": "max"}),
                "release": {"pass_requires": ["verified"]},
                "research_and_experience": _research_policy(),
                "output_delivery": {"artificial_output_throttling_forbidden": True},
            }), encoding="utf-8")
            preparation = {"result": "PASS", "assignments": [{"prompt": "x"}]}
            with self.assertRaisesRegex(ValueError, "quality_route_missing:critical"):
                bind_preparation(preparation, root, task_class="critical")


if __name__ == "__main__":
    unittest.main()
