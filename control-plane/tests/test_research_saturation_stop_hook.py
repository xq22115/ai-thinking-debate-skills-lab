from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / ".claude/hooks/enforce-a03-research-cycle.py"


def _write_receipt(
    audit: pathlib.Path,
    *,
    sequence: int,
    tool: str,
    query: str = "",
    url: str = "",
    effort: str = "xhigh",
) -> None:
    actor_dir = audit / "A03"
    actor_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schemaVersion": 2,
        "actor_id": "A03",
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "tool_use_id": f"toolu-{sequence}-{tool}",
        "session_id": "session-A03",
        "recorded_at_ns": sequence * 1000,
        "query": query,
        "url": url,
        "requested_effort": effort,
        "effective_effort": effort,
        "effort_readback_source": "hook_payload",
        "post_tool_success": True,
        "quality_evidence_accepted": True,
    }
    (actor_dir / f"{sequence:02d}-{tool}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def _full_cycle(audit: pathlib.Path, *, effort: str = "xhigh") -> None:
    _write_receipt(
        audit, sequence=1, tool="WebSearch", effort=effort,
        query="current primary documentation for leading mechanism",
    )
    _write_receipt(
        audit, sequence=2, tool="WebFetch", effort=effort,
        url="https://code.claude.com/docs/en/model-config",
    )
    _write_receipt(
        audit, sequence=3, tool="WebSearch", effort=effort,
        query="counterevidence failure modes conflicting guidance",
    )
    _write_receipt(
        audit, sequence=4, tool="WebFetch", effort=effort,
        url="https://code.claude.com/docs/en/hooks",
    )


class ResearchSaturationStopHookTests(unittest.TestCase):
    def _run(
        self,
        audit: pathlib.Path,
        *,
        actor: str = "A03",
        task_class: str = "material",
        effort: str = "xhigh",
        stop_hook_active: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["QUALITY_RESEARCH_AUDIT_DIR"] = str(audit)
        env["CONTROL_PLANE_ACTOR_ID"] = actor
        env["QUALITY_TASK_CLASS"] = task_class
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps({
                "hook_event_name": "Stop",
                "stop_hook_active": stop_hook_active,
                "last_assistant_message": "done",
            }),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def _decision(self, cp: subprocess.CompletedProcess[str]) -> dict:
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertTrue(cp.stdout.strip(), "expected Stop hook to block")
        return json.loads(cp.stdout)

    def test_nonresearch_actor_is_not_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cp = self._run(pathlib.Path(td), actor="A04")
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(cp.stdout.strip(), "")

    def test_simple_research_actor_is_not_forced_into_deep_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cp = self._run(pathlib.Path(td), task_class="simple", effort="medium")
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(cp.stdout.strip(), "")

    def test_no_search_blocks_stop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            decision = self._decision(self._run(pathlib.Path(td)))
            self.assertEqual(decision["decision"], "block")
            self.assertIn("no accepted WebSearch", decision["reason"])

    def test_discovery_search_without_inspection_blocks_stop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            _write_receipt(audit, sequence=1, tool="WebSearch", query="primary docs")
            decision = self._decision(self._run(audit))
            self.assertIn("not followed by inspection", decision["reason"])

    def test_one_search_fetch_pass_still_blocks_for_challenge_search(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            _write_receipt(audit, sequence=1, tool="WebSearch", query="primary docs")
            _write_receipt(
                audit, sequence=2, tool="WebFetch",
                url="https://code.claude.com/docs/en/model-config",
            )
            decision = self._decision(self._run(audit))
            self.assertIn("materially different WebSearch", decision["reason"])

    def test_repeated_query_after_fetch_does_not_count_as_challenge(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            query = "primary docs"
            _write_receipt(audit, sequence=1, tool="WebSearch", query=query)
            _write_receipt(
                audit, sequence=2, tool="WebFetch",
                url="https://code.claude.com/docs/en/model-config",
            )
            _write_receipt(audit, sequence=3, tool="WebSearch", query="  PRIMARY   docs ")
            decision = self._decision(self._run(audit, stop_hook_active=True))
            self.assertIn("repeating the same query does not count", decision["reason"])

    def test_challenge_without_distinct_followup_source_blocks_stop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            same_url = "https://code.claude.com/docs/en/model-config"
            _write_receipt(audit, sequence=1, tool="WebSearch", query="primary docs")
            _write_receipt(audit, sequence=2, tool="WebFetch", url=same_url)
            _write_receipt(audit, sequence=3, tool="WebSearch", query="counterevidence failure modes")
            _write_receipt(audit, sequence=4, tool="WebFetch", url=same_url + "#section")
            decision = self._decision(self._run(audit))
            self.assertIn("distinct follow-up source", decision["reason"])

    def test_complete_falsification_cycle_allows_stop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            _full_cycle(audit)
            cp = self._run(audit)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(cp.stdout.strip(), "")

    def test_wrong_effort_receipts_do_not_satisfy_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            _full_cycle(audit, effort="high")
            decision = self._decision(self._run(audit, effort="xhigh"))
            self.assertIn("no accepted WebSearch", decision["reason"])


if __name__ == "__main__":
    unittest.main()
