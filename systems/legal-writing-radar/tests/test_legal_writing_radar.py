from __future__ import annotations

import copy
import json
import pathlib
import sys
import unittest

SYSTEM_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SYSTEM_ROOT))

import legal_writing_radar as radar  # noqa: E402


class LegalWritingRadarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lanes = json.loads((SYSTEM_ROOT / "config" / "research_lanes.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((SYSTEM_ROOT / "evidence" / "verified-tools-2026-06-08.json").read_text(encoding="utf-8"))

    def test_verified_catalog_has_exactly_ten_unique_valid_items(self) -> None:
        errors = radar.validate_catalog(self.catalog, self.lanes, "2026-06-01", "2026-08-31")
        self.assertEqual(errors, [])
        self.assertEqual(len(self.catalog["items"]), 10)
        self.assertEqual(len({row["tool_id"] for row in self.catalog["items"]}), 10)
        self.assertEqual(len({row["official_url"] for row in self.catalog["items"]}), 10)

    def test_catalog_rejects_duplicate_tool_id(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["items"][1]["tool_id"] = catalog["items"][0]["tool_id"]
        errors = radar.validate_catalog(catalog, self.lanes, "2026-06-01", "2026-08-31")
        self.assertTrue(any("duplicate tool_id" in error for error in errors), errors)

    def test_catalog_rejects_date_outside_requested_window(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["items"][0]["release_date"] = "2026-05-31"
        errors = radar.validate_catalog(catalog, self.lanes, "2026-06-01", "2026-08-31")
        self.assertTrue(any("outside requested window" in error for error in errors), errors)

    def test_catalog_rejects_non_official_domain(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["items"][0]["official_url"] = "https://example.com/copied-press-release"
        errors = radar.validate_catalog(catalog, self.lanes, "2026-06-01", "2026-08-31")
        self.assertTrue(any("official domain" in error for error in errors), errors)

    def test_extract_published_date_requires_explicit_page_evidence(self) -> None:
        html = '<meta property="article:published_time" content="2026-07-30T09:00:00Z"><title>Launch</title>'
        self.assertEqual(radar.extract_published_date(html), "2026-07-30")
        self.assertIsNone(radar.extract_published_date("<html><title>No date</title></html>"))

    def test_discovery_keeps_only_keyword_matching_official_links(self) -> None:
        html = """
        <a href="/blog/new-legal-ai-drafting-agent">Drafting launch</a>
        <a href="https://vendor.example/news/company-picnic">Picnic</a>
        <a href="https://evil.example/blog/legal-ai-drafting">Copied</a>
        <a href="/blog/new-legal-ai-drafting-agent#top">Duplicate</a>
        """
        links = radar.discover_official_links(
            "https://vendor.example/news",
            html,
            {"vendor.example"},
            {"legal", "draft", "agent"},
        )
        self.assertEqual(links, ["https://vendor.example/blog/new-legal-ai-drafting-agent"])

    def test_blueprint_is_conclusion_first_and_does_not_invent_authority(self) -> None:
        facts = {
            "objective": "取得對方在期限前確認變更指示",
            "known_facts": ["設計圖於 2026-08-20 收到"],
            "requested_action": "請於 2026-08-31 前確認是否正式指示變更",
        }
        blueprint = radar.build_correspondence_blueprint(facts, "executive-counsel")
        self.assertEqual(blueprint["position"], facts["objective"])
        self.assertIn("[VERIFY CONTRACT / LEGAL AUTHORITY]", blueprint["authority_anchors"])
        serialized = json.dumps(blueprint, ensure_ascii=False).lower()
        self.assertNotIn("without prejudice", serialized)
        self.assertNotIn("attorney-client privileged", serialized)

    def test_international_project_blueprint_preserves_claim_structure(self) -> None:
        facts = {
            "objective": "形成正式工程紀錄並要求書面指示",
            "project_reference": "PROJECT-X / PACKAGE-03",
            "known_facts": ["Site instruction SI-17 received 2026-08-24"],
            "contract_anchors": ["Sub-Clause 1.3 — Communications"],
            "cause": "新增施工要求",
            "effect": "可能影響工期與成本",
            "entitlement": "待依合約與適用法律確認",
            "quantum": "待同期紀錄與估價確認",
            "requested_action": "請書面確認指示及後續估價程序",
            "deadline": "2026-08-31",
        }
        blueprint = radar.build_correspondence_blueprint(facts, "international-project")
        self.assertEqual(blueprint["project_reference"], "PROJECT-X / PACKAGE-03")
        self.assertEqual(
            list(blueprint["claim_logic"].keys()),
            ["cause", "effect", "entitlement", "quantum"],
        )
        self.assertEqual(blueprint["ask"], facts["requested_action"])
        self.assertEqual(blueprint["deadline"], facts["deadline"])

    def test_context_dependent_legal_labels_are_opt_in_only(self) -> None:
        facts = {
            "objective": "提出商務和解方案",
            "requested_action": "請回覆是否願意進一步協商",
            "legal_labels_confirmed": ["for settlement purposes only"],
        }
        blueprint = radar.build_correspondence_blueprint(facts, "dispute-preservation")
        self.assertEqual(blueprint["confirmed_legal_labels"], ["for settlement purposes only"])
        self.assertIn("without prejudice", blueprint["disabled_legal_labels"])
        self.assertNotIn("for settlement purposes only", blueprint["disabled_legal_labels"])


if __name__ == "__main__":
    unittest.main()
