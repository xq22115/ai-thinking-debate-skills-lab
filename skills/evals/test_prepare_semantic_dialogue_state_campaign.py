#!/usr/bin/env python3
"""Contract tests for the semantic dialogue-state campaign packet generator."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from prepare_semantic_dialogue_state_campaign import prepare_campaign, validate_campaign


EXPECTED_ARMS = {
    "target": [
        "direct",
        "generic-careful",
        "microscope-core",
        "microscope-dialogue-state",
    ],
    "protection": ["microscope-core", "microscope-dialogue-state"],
    "generalization": ["microscope-core", "microscope-dialogue-state"],
}

EXPECTED_FIXTURES = {
    "target": "skills/evals/semantic-dialogue-state-fixtures.json",
    "protection": "skills/evals/semantic-dialogue-state-protection-fixtures.json",
    "generalization": "skills/evals/semantic-dialogue-state-generalization-holdout.json",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class CampaignPacketTests(unittest.TestCase):
    def prepare(self, root: Path) -> Path:
        campaign_dir = root / "campaign"
        prepare_campaign(
            campaign_dir,
            repo_ref="0123456789abcdef0123456789abcdef01234567",
            model_id="model-under-test",
            provider="provider-under-test",
            seed=73,
            campaign_id="campaign-contract-test",
        )
        return campaign_dir

    def test_prepare_campaign_binds_identity_and_suite_shapes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="semantic-campaign-contract-") as tmp:
            campaign_dir = self.prepare(Path(tmp))
            campaign = load_json(campaign_dir / "campaign_manifest.json")

            self.assertEqual(campaign["campaign_id"], "campaign-contract-test")
            self.assertEqual(campaign["repo_ref"], "0123456789abcdef0123456789abcdef01234567")
            self.assertEqual(campaign["model_id"], "model-under-test")
            self.assertEqual(campaign["provider"], "provider-under-test")
            self.assertEqual(campaign["seed"], 73)
            self.assertEqual(set(campaign["suites"]), {"target", "protection", "generalization"})

            for role in ("target", "protection", "generalization"):
                run_dir = campaign_dir / role
                manifest = load_json(run_dir / "manifest.json")
                self.assertEqual(manifest["repo_ref"], campaign["repo_ref"])
                self.assertEqual(manifest["model_id"], campaign["model_id"])
                self.assertEqual(manifest["provider"], campaign["provider"])
                self.assertEqual(manifest["seed"], campaign["seed"])
                self.assertEqual(manifest["fixture_path"], EXPECTED_FIXTURES[role])
                self.assertEqual(manifest["arms"], EXPECTED_ARMS[role])
                self.assertEqual(campaign["suites"][role]["run_id"], manifest["run_id"])

            self.assertEqual(load_json(campaign_dir / "target" / "manifest.json")["suite_role"], "target")
            self.assertEqual(load_json(campaign_dir / "protection" / "manifest.json")["suite_role"], "protection")
            self.assertEqual(load_json(campaign_dir / "generalization" / "manifest.json")["suite_role"], "protection")

            result = validate_campaign(campaign_dir)
            self.assertEqual(result["decision"], "CAMPAIGN_PACKET_VALID")

    def test_prepare_campaign_generates_frozen_receipt_templates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="semantic-campaign-template-") as tmp:
            campaign_dir = self.prepare(Path(tmp))
            for role in ("target", "protection", "generalization"):
                run_dir = campaign_dir / role
                manifest = load_json(run_dir / "manifest.json")
                requests = load_jsonl(run_dir / "requests.jsonl")
                templates = load_jsonl(run_dir / "execution_receipts.template.jsonl")
                self.assertEqual(len(templates), len(requests))
                self.assertGreater(len(templates), 0)
                for request, template in zip(requests, templates):
                    self.assertEqual(template["request_id"], request["request_id"])
                    self.assertEqual(template["run_id"], manifest["run_id"])
                    self.assertEqual(template["model_id"], manifest["model_id"])
                    self.assertEqual(template["provider"], manifest["provider"])
                    self.assertEqual(template["bundle_sha256"], request["bundle_sha256"])
                    self.assertIsNone(template["fresh_context"])
                    self.assertEqual(template["status"], "FILL_ME")

    def test_validate_campaign_rejects_identity_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="semantic-campaign-drift-") as tmp:
            campaign_dir = self.prepare(Path(tmp))
            protection_manifest_path = campaign_dir / "protection" / "manifest.json"
            protection_manifest = load_json(protection_manifest_path)
            protection_manifest["provider"] = "drifted-provider"
            protection_manifest_path.write_text(
                json.dumps(protection_manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "identity drift"):
                validate_campaign(campaign_dir)


if __name__ == "__main__":
    unittest.main()
