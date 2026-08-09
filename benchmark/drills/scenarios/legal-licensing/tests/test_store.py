import json
import tempfile
import unittest
from pathlib import Path

from app.store import JsonList


class JsonListTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "records.json"

    def test_missing_file_reads_as_empty(self):
        self.assertEqual(JsonList(self.path).read(), [])

    def test_appends_survive_a_reopen(self):
        JsonList(self.path).append({"email": "first@example.com"})
        JsonList(self.path).append({"email": "second@example.com"})
        rows = JsonList(self.path).read()
        self.assertEqual([r["email"] for r in rows],
                         ["first@example.com", "second@example.com"])

    def test_rubbish_in_the_file_reads_as_empty(self):
        self.path.write_text("{not json", encoding="utf-8")
        self.assertEqual(JsonList(self.path).read(), [])

    def test_writes_are_json(self):
        JsonList(self.path).write([{"email": "sam@example.com"}])
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")),
                         [{"email": "sam@example.com"}])


if __name__ == "__main__":
    unittest.main()
