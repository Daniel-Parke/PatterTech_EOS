"""What the waitlist has to do.

Written before the code, so it fails until somebody writes it. Order is
the order people joined in, both from `addresses` and in the export.
"""

import csv
import io
import tempfile
import unittest
from pathlib import Path

from app.waitlist import Waitlist


class WaitlistTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "waitlist.json"

    def open_list(self):
        return Waitlist(self.path)

    def test_adds_an_address(self):
        book = self.open_list()
        self.assertEqual(book.add("Sam@Example.com"), "added")
        self.assertEqual(book.addresses(), ["sam@example.com"])

    def test_the_same_address_twice_is_a_duplicate(self):
        book = self.open_list()
        book.add("sam@example.com")
        self.assertEqual(book.add("  SAM@example.com "), "duplicate")
        self.assertEqual(book.addresses(), ["sam@example.com"])

    def test_refuses_things_that_are_not_addresses(self):
        book = self.open_list()
        for bad in ("", "   ", "sam", "sam@", "@example.com", "sam@example",
                    "sam example@example.com", "a@b@example.com"):
            with self.assertRaises(ValueError):
                book.add(bad)
        self.assertEqual(book.addresses(), [])

    def test_survives_a_restart(self):
        self.open_list().add("first@example.com")
        self.open_list().add("second@example.com")
        self.assertEqual(self.open_list().addresses(),
                         ["first@example.com", "second@example.com"])

    def test_exports_csv(self):
        book = self.open_list()
        book.add("second@example.com")
        book.add("first@example.com")
        rows = [r for r in csv.reader(io.StringIO(book.export_csv())) if r]
        self.assertEqual(rows[0], ["email"])
        self.assertEqual([r[0] for r in rows[1:]],
                         ["second@example.com", "first@example.com"])


if __name__ == "__main__":
    unittest.main()
