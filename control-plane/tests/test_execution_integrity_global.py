from __future__ import annotations

import pathlib
import sys
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_execution_integrity_global import validate


class ExecutionIntegrityGlobalProfileTests(unittest.TestCase):
    def test_repository_wide_execution_integrity_is_fail_closed(self) -> None:
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
