import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "resources" / "authority-ledger.json"


class AuthorityLedgerTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.items = self.data["authorities"]

    def test_authority_ids_and_urls_are_unique(self):
        ids = [item["id"] for item in self.items]
        urls = [item["url"] for item in self.items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(url.startswith("https://") for url in urls))

    def test_retrieval_date_is_not_misrepresented_as_source_date(self):
        self.assertIn("verified_at", self.data)
        self.assertIn("date_semantics", self.data)
        for item in self.items:
            self.assertNotIn("date", item)
            self.assertIn("source_date", item)
            self.assertTrue(item["source_date_kind"])

    def test_every_authority_records_mechanism_use_and_limitation(self):
        for item in self.items:
            self.assertTrue(item["mechanism"])
            self.assertTrue(item["engine_use"])
            self.assertTrue(item["limitation"])


if __name__ == "__main__":
    unittest.main()
