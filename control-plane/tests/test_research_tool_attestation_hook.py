from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
POST_HOOK = REPO_ROOT / ".claude/hooks/record-web-research.py"
PRE_HOOK = REPO_ROOT / ".claude/hooks/allow-a03-web-research.py"


class ResearchToolAttestationHookTests(unittest.TestCase):
    def _run_post_hook(
        self,
        payload: dict,
        audit_dir: pathlib.Path,
        actor: str = "A03",
        requested_effort: str = "xhigh",
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["QUALITY_RESEARCH_AUDIT_DIR"] = str(audit_dir)
        env["CONTROL_PLANE_ACTOR_ID"] = actor
        env["CLAUDE_CODE_EFFORT_LEVEL"] = requested_effort
        return subprocess.run(
            [sys.executable, str(POST_HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def _run_pre_hook(self, tool: str, actor: str = "A03") -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["CONTROL_PLANE_ACTOR_ID"] = actor
        return subprocess.run(
            [sys.executable, str(PRE_HOOK)],
            input=json.dumps({
                "hook_event_name": "PreToolUse",
                "tool_name": tool,
                "tool_input": {"query": "x"} if tool == "WebSearch" else {"url": "https://example.com"},
            }),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_a03_websearch_is_allowed_without_project_allow_rule_trust(self) -> None:
        cp = self._run_pre_hook("WebSearch")
        self.assertEqual(cp.returncode, 0, cp.stderr)
        output = json.loads(cp.stdout)
        decision = output["hookSpecificOutput"]
        self.assertEqual(decision["hookEventName"], "PreToolUse")
        self.assertEqual(decision["permissionDecision"], "allow")

    def test_a03_webfetch_is_allowed_without_project_allow_rule_trust(self) -> None:
        cp = self._run_pre_hook("WebFetch")
        self.assertEqual(cp.returncode, 0, cp.stderr)
        output = json.loads(cp.stdout)
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "allow")

    def test_nonresearch_actor_is_not_granted_web_permission(self) -> None:
        cp = self._run_pre_hook("WebSearch", actor="A04")
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertEqual(cp.stdout.strip(), "")

    def test_successful_websearch_posttooluse_creates_effort_attested_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_post_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "WebSearch",
                "tool_use_id": "toolu_search_1",
                "session_id": "session-1",
                "duration_ms": 42,
                "effort": {"level": "xhigh"},
                "tool_input": {"query": "Claude Code effort current docs"},
                "tool_response": {"results": [{"title": "docs"}]},
            }, audit)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            receipts = list((audit / "A03").glob("*.json"))
            self.assertEqual(len(receipts), 1)
            payload = json.loads(receipts[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["tool_name"], "WebSearch")
            self.assertEqual(payload["query"], "Claude Code effort current docs")
            self.assertEqual(payload["requested_effort"], "xhigh")
            self.assertEqual(payload["effective_effort"], "xhigh")
            self.assertEqual(payload["effort_readback_source"], "hook_payload")
            self.assertTrue(payload["quality_evidence_accepted"])
            self.assertTrue(payload["post_tool_success"])
            self.assertEqual(len(payload["tool_response_sha256"]), 64)
            self.assertNotIn("tool_response", payload)

    def test_successful_webfetch_records_url_but_not_page_contents(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_post_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "WebFetch",
                "tool_use_id": "toolu_fetch_1",
                "session_id": "session-1",
                "effort": {"level": "xhigh"},
                "tool_input": {"url": "https://code.claude.com/docs/en/model-config"},
                "tool_response": {"content": "large private-ish content must not be persisted"},
            }, audit)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            receipt = next((audit / "A03").glob("*.json"))
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(payload["url"], "https://code.claude.com/docs/en/model-config")
            self.assertNotIn("large private-ish content", receipt.read_text(encoding="utf-8"))

    def test_effective_effort_downgrade_is_rejected_not_counted_as_pass_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_post_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "WebSearch",
                "tool_use_id": "toolu_search_downgraded",
                "session_id": "session-1",
                "effort": {"level": "high"},
                "tool_input": {"query": "x"},
                "tool_response": {"results": []},
            }, audit, requested_effort="xhigh")
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(list((audit / "A03").glob("*.json")), [])
            rejected = next((audit / "_rejected" / "A03").glob("*.json"))
            payload = json.loads(rejected.read_text(encoding="utf-8"))
            self.assertEqual(payload["rejection_reason"], "effective_effort_mismatch")
            self.assertEqual(payload["requested_effort"], "xhigh")
            self.assertEqual(payload["effective_effort"], "high")
            self.assertFalse(payload["quality_evidence_accepted"])

    def test_missing_effective_effort_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            env = os.environ.copy()
            env.pop("CLAUDE_EFFORT", None)
            env["QUALITY_RESEARCH_AUDIT_DIR"] = str(audit)
            env["CONTROL_PLANE_ACTOR_ID"] = "A03"
            env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"
            cp = subprocess.run(
                [sys.executable, str(POST_HOOK)],
                input=json.dumps({
                    "hook_event_name": "PostToolUse",
                    "tool_name": "WebFetch",
                    "tool_use_id": "toolu_fetch_no_effort",
                    "tool_input": {"url": "https://example.com"},
                    "tool_response": {"content": "x"},
                }),
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(list((audit / "A03").glob("*.json")), [])
            rejected = next((audit / "_rejected" / "A03").glob("*.json"))
            payload = json.loads(rejected.read_text(encoding="utf-8"))
            self.assertEqual(payload["rejection_reason"], "effective_effort_missing_or_unsupported")

    def test_non_web_tool_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            audit = pathlib.Path(td)
            cp = self._run_post_hook({
                "hook_event_name": "PostToolUse",
                "tool_name": "Read",
                "tool_use_id": "toolu_read_1",
                "effort": {"level": "xhigh"},
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
            "effort": {"level": "xhigh"},
            "tool_input": {"query": "x"},
            "tool_response": {"results": []},
        }
        env = os.environ.copy()
        env.pop("QUALITY_RESEARCH_AUDIT_DIR", None)
        env.pop("CONTROL_PLANE_ACTOR_ID", None)
        env.pop("CLAUDE_CODE_EFFORT_LEVEL", None)
        cp = subprocess.run(
            [sys.executable, str(POST_HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stderr)


if __name__ == "__main__":
    unittest.main()
