from __future__ import annotations

import json
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_quality_bound_workflow as module

CONTROL_PLANE_ROOT = pathlib.Path(__file__).resolve().parents[1]


def _preparation() -> dict:
    return {
        "result": "PASS",
        "assignments": [{"actor_id": "A01", "prompt": "Inspect the target."}],
    }


def _deep_pass_result() -> dict:
    return {
        "result": "PASS",
        "failures": [],
        "executions": {
            "A03": {
                "decision": {
                    "decision": "PASS",
                    "evidence": [
                        {"kind": "web_search", "reference": "query: current primary docs"},
                        {
                            "kind": "web_fetch",
                            "reference": "https://code.claude.com/docs/en/model-config",
                        },
                    ],
                    "reasoning_quality": {
                        "research_stop_reason": "decision_saturated",
                    },
                }
            }
        },
    }


class QualityBoundWorkflowTests(unittest.TestCase):
    def test_normal_run_binds_before_delegating_and_persists_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", return_value=_deep_pass_result()) as delegate:
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td
                )
            self.assertEqual(result["result"], "PASS")
            self.assertEqual(result["reasoning_runtime"]["effort"], "high")
            self.assertTrue(result["delivery_contract"]["token_drip_as_depth_signal_forbidden"])
            evidence_path = pathlib.Path(td) / "quality-bound-preparation.json"
            self.assertTrue(evidence_path.is_file())
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertTrue(evidence["quality_profile_binding"]["bound"])
            self.assertEqual(evidence["quality_profile_binding"]["reasoning_effort"], "high")
            delegated_preparation = delegate.call_args.args[0]
            self.assertIn("[QUALITY_PROFILE_BINDING]", delegated_preparation["assignments"][0]["prompt"])
            self.assertIn("reasoning_effort=high", delegated_preparation["assignments"][0]["prompt"])
            self.assertIn("token-by-token pacing", delegated_preparation["assignments"][0]["prompt"])

    def test_material_pass_without_observable_research_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            shallow = {
                "result": "PASS",
                "executions": {
                    "A03": {
                        "decision": {
                            "decision": "PASS",
                            "evidence": [{"kind": "readback", "reference": "self report"}],
                            "reasoning_quality": {"research_stop_reason": "decision_saturated"},
                        }
                    }
                },
            }
            with mock.patch.object(module, "run_workflow", return_value=shallow):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("web_search_receipt_missing:A03", result["failures"])
            self.assertIn("fetched_source_url_missing:A03", result["failures"])

    def test_simple_run_does_not_require_external_research(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", return_value={"result": "PASS"}):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="simple",
                )
            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(result["reasoning_runtime"]["effort"], "medium")

    def test_critical_run_enforces_xhigh_and_temporarily_clears_thinking_disable(self) -> None:
        observed = {}

        def fake_run(*args, **kwargs):
            observed["effort"] = os.environ.get("CLAUDE_CODE_EFFORT_LEVEL")
            observed["max_thinking"] = os.environ.get("MAX_THINKING_TOKENS")
            return _deep_pass_result()

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.dict(os.environ, {"MAX_THINKING_TOKENS": "0"}, clear=False):
                with mock.patch.object(module, "run_workflow", side_effect=fake_run):
                    result = module.run_quality_bound_workflow(
                        _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                        task_class="critical",
                    )
                self.assertEqual(os.environ.get("MAX_THINKING_TOKENS"), "0")
            self.assertEqual(observed["effort"], "xhigh")
            self.assertIsNone(observed["max_thinking"])
            self.assertTrue(result["reasoning_runtime"]["cleared_inherited_max_thinking_tokens_zero"])

    def test_resume_without_prior_binding_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow") as delegate:
                with self.assertRaisesRegex(ValueError, "resume_quality_binding_evidence_missing"):
                    module.run_quality_bound_workflow(
                        _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                        resume_existing=True,
                    )
                delegate.assert_not_called()

    def test_resume_with_mismatched_binding_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            output = pathlib.Path(td)
            (output / "quality-bound-preparation.json").write_text(
                json.dumps({
                    "quality_profile_binding": {
                        "bound": True,
                        "profile_id": "wrong-profile",
                        "profile_sha256": "0" * 64,
                        "task_class": "material",
                        "profile_path": "ai-system/configs/continuous-thinking-global.json",
                    }
                }),
                encoding="utf-8",
            )
            with mock.patch.object(module, "run_workflow") as delegate:
                with self.assertRaisesRegex(ValueError, "resume_quality_binding_mismatch"):
                    module.run_quality_bound_workflow(
                        _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                        resume_existing=True,
                    )
                delegate.assert_not_called()

    def test_resume_with_same_binding_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            output = pathlib.Path(td)
            bound = module.bind_preparation(_preparation(), CONTROL_PLANE_ROOT, task_class="critical")
            (output / "quality-bound-preparation.json").write_text(
                json.dumps(bound), encoding="utf-8"
            )
            with mock.patch.object(module, "run_workflow", return_value=_deep_pass_result()) as delegate:
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="critical", resume_existing=True,
                )
            self.assertEqual(result["result"], "PASS")
            delegate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
