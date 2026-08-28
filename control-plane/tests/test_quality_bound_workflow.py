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
                    "reasoning_quality": {
                        "research_stop_reason": "decision_saturated",
                    },
                }
            }
        },
    }


def _write_receipt(
    tool: str,
    *,
    sequence: int,
    actor: str = "A03",
    requested_effort: str | None = None,
    effective_effort: str | None = None,
    accepted: bool = True,
    query: str | None = None,
    url: str | None = None,
) -> None:
    audit_root = pathlib.Path(os.environ["QUALITY_RESEARCH_AUDIT_DIR"])
    actor_dir = audit_root / actor
    actor_dir.mkdir(parents=True, exist_ok=True)
    requested = requested_effort or str(os.environ.get("CLAUDE_CODE_EFFORT_LEVEL") or "")
    effective = effective_effort or requested
    if query is None and tool == "WebSearch":
        query = f"decision evidence query {sequence}"
    if url is None and tool == "WebFetch":
        url = f"https://code.claude.com/docs/en/source-{sequence}"
    payload = {
        "schemaVersion": 2,
        "actor_id": actor,
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "tool_use_id": f"toolu-{sequence}-{tool}",
        "session_id": "session-A03",
        "post_tool_success": True,
        "quality_evidence_accepted": accepted,
        "requested_effort": requested,
        "effective_effort": effective,
        "effort_readback_source": "hook_payload",
        "recorded_at_ns": sequence * 1000,
        "query": query if tool == "WebSearch" else "",
        "url": url if tool == "WebFetch" else "",
        "tool_response_sha256": "a" * 64,
    }
    (actor_dir / f"{sequence:02d}-{tool}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def _write_full_cycle(
    *,
    requested_effort: str | None = None,
    effective_effort: str | None = None,
    accepted: bool = True,
) -> None:
    _write_receipt(
        "WebSearch", sequence=1,
        requested_effort=requested_effort, effective_effort=effective_effort,
        accepted=accepted, query="current primary documentation for the leading mechanism",
    )
    _write_receipt(
        "WebFetch", sequence=2,
        requested_effort=requested_effort, effective_effort=effective_effort,
        accepted=accepted, url="https://code.claude.com/docs/en/model-config",
    )
    _write_receipt(
        "WebSearch", sequence=3,
        requested_effort=requested_effort, effective_effort=effective_effort,
        accepted=accepted, query="counterevidence failure modes conflicting guidance for the mechanism",
    )
    _write_receipt(
        "WebFetch", sequence=4,
        requested_effort=requested_effort, effective_effort=effective_effort,
        accepted=accepted, url="https://code.claude.com/docs/en/hooks",
    )


def _passing_delegate(observed: dict | None = None):
    def delegate(*args, **kwargs):
        if observed is not None:
            observed["effort"] = os.environ.get("CLAUDE_CODE_EFFORT_LEVEL")
            observed["task_class"] = os.environ.get("QUALITY_TASK_CLASS")
            observed["disable_thinking"] = os.environ.get("CLAUDE_CODE_DISABLE_THINKING")
            observed["disable_adaptive"] = os.environ.get("CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING")
            observed["max_thinking"] = os.environ.get("MAX_THINKING_TOKENS")
            observed["audit_dir"] = os.environ.get("QUALITY_RESEARCH_AUDIT_DIR")
        _write_full_cycle()
        return _deep_pass_result()
    return delegate


class QualityBoundWorkflowTests(unittest.TestCase):
    def test_normal_deep_run_binds_effort_requires_falsification_cycle_and_persists_evidence(self) -> None:
        observed = {}
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=_passing_delegate(observed)) as delegate:
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td
                )
            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(observed["effort"], "xhigh")
            self.assertEqual(observed["task_class"], "material")
            self.assertIsNotNone(observed["audit_dir"])
            self.assertEqual(result["reasoning_runtime"]["requested_effort"], "xhigh")
            self.assertTrue(result["reasoning_runtime"]["effective_effort_verified_by_research_hook"])
            self.assertTrue(result["reasoning_runtime"]["adaptive_research_saturation_verified"])
            self.assertEqual(result["research_runtime_attestation"]["result"], "PASS")
            self.assertEqual(result["research_runtime_attestation"]["expected_effort"], "xhigh")
            self.assertEqual(result["research_runtime_attestation"]["observed_effective_efforts"], ["xhigh"])
            self.assertTrue(result["research_runtime_attestation"]["falsification_cycle"]["complete"])
            self.assertEqual(
                set(result["research_runtime_attestation"]["observed_tools"]),
                {"WebSearch", "WebFetch"},
            )
            self.assertTrue(result["delivery_contract"]["normal_continuous_delivery_after_release_gate"])
            evidence_path = pathlib.Path(td) / "quality-bound-preparation.json"
            self.assertTrue(evidence_path.is_file())
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertTrue(evidence["quality_profile_binding"]["bound"])
            self.assertEqual(evidence["quality_profile_binding"]["reasoning_effort"], "xhigh")
            delegated_preparation = delegate.call_args.args[0]
            self.assertIn("[QUALITY_PROFILE_BINDING]", delegated_preparation["assignments"][0]["prompt"])
            self.assertIn("reasoning_effort=xhigh", delegated_preparation["assignments"][0]["prompt"])

    def test_deep_pass_without_successful_tool_receipts_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", return_value=_deep_pass_result()):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("successful_tool_receipt_missing:A03:WebSearch", result["failures"])
            self.assertIn("successful_tool_receipt_missing:A03:WebFetch", result["failures"])
            self.assertIn("research_cycle_discover_search_missing:A03", result["failures"])
            self.assertEqual(result["research_runtime_attestation"]["result"], "FAIL")

    def test_one_search_and_fetch_is_not_research_saturation(self) -> None:
        def first_pass_delegate(*args, **kwargs):
            _write_receipt("WebSearch", sequence=1, query="leading mechanism primary docs")
            _write_receipt("WebFetch", sequence=2, url="https://code.claude.com/docs/en/model-config")
            return _deep_pass_result()

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=first_pass_delegate):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("research_cycle_distinct_challenge_search_missing:A03", result["failures"])
            self.assertFalse(result["research_runtime_attestation"]["falsification_cycle"]["complete"])

    def test_repeating_same_query_after_inspection_does_not_count_as_challenge(self) -> None:
        def repeated_query_delegate(*args, **kwargs):
            query = "leading mechanism primary docs"
            _write_receipt("WebSearch", sequence=1, query=query)
            _write_receipt("WebFetch", sequence=2, url="https://code.claude.com/docs/en/model-config")
            _write_receipt("WebSearch", sequence=3, query=query)
            _write_receipt("WebFetch", sequence=4, url="https://code.claude.com/docs/en/hooks")
            return _deep_pass_result()

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=repeated_query_delegate):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("research_cycle_distinct_challenge_search_missing:A03", result["failures"])

    def test_challenge_search_requires_distinct_followup_source(self) -> None:
        def same_source_delegate(*args, **kwargs):
            same_url = "https://code.claude.com/docs/en/model-config"
            _write_receipt("WebSearch", sequence=1, query="leading mechanism primary docs")
            _write_receipt("WebFetch", sequence=2, url=same_url)
            _write_receipt("WebSearch", sequence=3, query="counterevidence and failure modes")
            _write_receipt("WebFetch", sequence=4, url=same_url)
            return _deep_pass_result()

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=same_source_delegate):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("research_cycle_distinct_followup_inspection_missing:A03", result["failures"])

    def test_deep_pass_with_downgraded_effort_receipts_fails_closed(self) -> None:
        def downgraded_delegate(*args, **kwargs):
            _write_full_cycle(requested_effort="xhigh", effective_effort="high")
            return _deep_pass_result()

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=downgraded_delegate):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertIn("research_receipt_not_effort_attested:A03:WebSearch", result["failures"])
            self.assertIn("research_receipt_not_effort_attested:A03:WebFetch", result["failures"])
            self.assertEqual(result["research_runtime_attestation"]["accepted_receipt_count"], 0)
            self.assertFalse(result["reasoning_runtime"]["effective_effort_verified_by_research_hook"])

    def test_deep_pass_with_self_marked_unaccepted_receipts_fails_closed(self) -> None:
        def unaccepted_delegate(*args, **kwargs):
            _write_full_cycle(accepted=False)
            return _deep_pass_result()

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=unaccepted_delegate):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="material",
                )
            self.assertEqual(result["result"], "FAIL", result)
            self.assertEqual(result["research_runtime_attestation"]["accepted_receipt_count"], 0)

    def test_simple_run_does_not_force_external_research(self) -> None:
        observed = {}

        def simple_delegate(*args, **kwargs):
            observed["effort"] = os.environ.get("CLAUDE_CODE_EFFORT_LEVEL")
            observed["task_class"] = os.environ.get("QUALITY_TASK_CLASS")
            return {"result": "PASS"}

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", side_effect=simple_delegate):
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="simple",
                )
            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(observed["effort"], "medium")
            self.assertEqual(observed["task_class"], "simple")
            self.assertEqual(result["reasoning_runtime"]["requested_effort"], "medium")
            self.assertFalse(result["reasoning_runtime"]["effective_effort_verified_by_research_hook"])
            self.assertFalse(result["reasoning_runtime"]["adaptive_research_saturation_verified"])
            self.assertEqual(result["research_runtime_attestation"]["result"], "NOT_REQUIRED")

    def test_critical_run_uses_max_effort_and_clears_then_restores_thinking_disablers(self) -> None:
        observed = {}
        initial = {
            "CLAUDE_CODE_EFFORT_LEVEL": "low",
            "QUALITY_TASK_CLASS": "simple",
            "CLAUDE_CODE_DISABLE_THINKING": "1",
            "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1",
            "MAX_THINKING_TOKENS": "0",
        }
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.dict(os.environ, initial, clear=False):
                with mock.patch.object(module, "run_workflow", side_effect=_passing_delegate(observed)):
                    result = module.run_quality_bound_workflow(
                        _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                        task_class="critical",
                    )
                self.assertEqual(os.environ.get("CLAUDE_CODE_EFFORT_LEVEL"), "low")
                self.assertEqual(os.environ.get("QUALITY_TASK_CLASS"), "simple")
                self.assertEqual(os.environ.get("CLAUDE_CODE_DISABLE_THINKING"), "1")
                self.assertEqual(os.environ.get("CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING"), "1")
                self.assertEqual(os.environ.get("MAX_THINKING_TOKENS"), "0")
            self.assertEqual(observed["effort"], "max")
            self.assertEqual(observed["task_class"], "critical")
            self.assertIsNone(observed["disable_thinking"])
            self.assertIsNone(observed["disable_adaptive"])
            self.assertIsNone(observed["max_thinking"])
            self.assertEqual(result["research_runtime_attestation"]["expected_effort"], "max")
            self.assertEqual(result["research_runtime_attestation"]["observed_effective_efforts"], ["max"])
            self.assertTrue(result["research_runtime_attestation"]["falsification_cycle"]["complete"])
            self.assertEqual(
                set(result["reasoning_runtime"]["thinking_disable_overrides_cleared_for_run"]),
                {
                    "CLAUDE_CODE_DISABLE_THINKING",
                    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING",
                    "MAX_THINKING_TOKENS",
                },
            )
            self.assertTrue(result["reasoning_runtime"]["effective_effort_verified_by_research_hook"])
            self.assertTrue(result["reasoning_runtime"]["adaptive_research_saturation_verified"])
            self.assertTrue(result["reasoning_runtime"]["environment_restored_after_run"])

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
                        "reasoning_effort": "low",
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

    def test_resume_with_same_binding_is_allowed_and_still_requires_fresh_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            output = pathlib.Path(td)
            bound = module.bind_preparation(_preparation(), CONTROL_PLANE_ROOT, task_class="critical")
            (output / "quality-bound-preparation.json").write_text(
                json.dumps(bound), encoding="utf-8"
            )
            with mock.patch.object(module, "run_workflow", side_effect=_passing_delegate()) as delegate:
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="critical", resume_existing=True,
                )
            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(result["research_runtime_attestation"]["result"], "PASS")
            self.assertTrue(result["research_runtime_attestation"]["falsification_cycle"]["complete"])
            delegate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
