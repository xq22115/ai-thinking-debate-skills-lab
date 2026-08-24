from __future__ import annotations

import json
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


class QualityBoundWorkflowTests(unittest.TestCase):
    def test_normal_run_binds_before_delegating_and_persists_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(module, "run_workflow", return_value={"result": "PASS"}) as delegate:
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td
                )
            self.assertEqual(result["result"], "PASS")
            evidence_path = pathlib.Path(td) / "quality-bound-preparation.json"
            self.assertTrue(evidence_path.is_file())
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertTrue(evidence["quality_profile_binding"]["bound"])
            delegated_preparation = delegate.call_args.args[0]
            self.assertIn("[QUALITY_PROFILE_BINDING]", delegated_preparation["assignments"][0]["prompt"])

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
            with mock.patch.object(module, "run_workflow", return_value={"result": "PASS"}) as delegate:
                result = module.run_quality_bound_workflow(
                    _preparation(), CONTROL_PLANE_ROOT, "/unused/claude", td,
                    task_class="critical", resume_existing=True,
                )
            self.assertEqual(result["result"], "PASS")
            delegate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
