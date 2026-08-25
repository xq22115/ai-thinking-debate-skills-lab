from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / ".claude/hooks/record-web-research.py"


class ResearchToolAttestationHookTests(unittest.TestCase):
    def _run_hook(self, payload: dict, audit_dir: pathlib.Path, actor: str = "A03") -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["QUALITY_RESEARCH_AUDIT_DIR"] = str(audit_dir)
        env["CONTROL_PLANE_ACTOR_ID"] = actor
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_successful_websearch_posttooluse_creates_minimal_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "WebSearch",
                "tool_use_id": "toolu_search_1",
                "session_id": "session-1",
                "duration_ms": 42,
                "tool_input": {"query": "Claude Code effort current docs"},
                "tool_response": {"results": [{"title": "docs"}]},
            }, audit)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            receipts = list((audit / "A03").glob("*.json"))
            self.assertEqual(len(receipts), 1)
            payload = json.loads(receipts[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["tool_name"], "WebSearch")
            self.assertEqual(payload["query"], "Claude Code effort current docs")
            self.assertTrue(payload["post_tool_success"])
            self.assertEqual(len(payload["tool_response_sha256"]), 64)
            self.assertNotIn("tool_response", payload)

    def test_successful_webfetch_records_url_but_not_page_contents(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "WebFetch",
                "tool_use_id": "toolu_fetch_1",
                "session_id": "session-1",
                "tool_input": {"url": "https://code.claude.com/docs/en/model-config"},
                "tool_response": {"content": "large private-ish content must not be persisted"},
            }, audit)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            receipt = next((audit / "A03").glob("*.json"))
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(payload["url"], "https://code.claude.com/docs/en/model-config")
            self.assertNotIn("large private-ish content", receipt.read_text(encoding="utf-8"))

    def test_non_web_tool_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "Read",
                "tool_use_id": "toolu_read_1",
                "tool_input": {"file_path": "README.md"},
                "tool_response": {"content": "x"},
            }, audit)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(list(audit.rglob("*.json")), [])

    def test_missing_runtime_env_is_noop_not_false_evidence(self) -> None:
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "WebSearch",
            "tool_use_id": "toolu_search_2",
            "tool_input": {"query": "x"},
            "tool_response": {"results": []},
        }
        env = os.environ.copy()
        env.pop("QUALITY_RESEARCH_AUDIT_DIR", None)
        env.pop("CONTROL_PLANE_ACTOR_ID", None)
        cp = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stderr)


if __name__ == "__main__":
    unittest.main()
