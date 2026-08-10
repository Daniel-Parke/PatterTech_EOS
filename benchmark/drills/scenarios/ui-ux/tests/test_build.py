"""The build writes the page. Run with:

    python -m unittest discover -s tests
"""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BuildTest(unittest.TestCase):

    def test_build_writes_the_public_page(self):
        proc = subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue((ROOT / "dist" / "index.html").is_file())

    def test_the_page_keeps_its_three_fields(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        for name in ("postcode", "where", "phone"):
            self.assertIn('name="%s"' % name, html)


if __name__ == "__main__":
    unittest.main()
