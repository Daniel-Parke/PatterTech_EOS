"""Tests for the nightly invoice export.

Written before the exporter, from the column order finance signed off.
Do not change them: the vendor importer keys on the header row.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ledger.http import DestinationNotAllowed  # noqa: E402
from ledger.invoice_export import export_invoices, upload_export  # noqa: E402
from ledger.invoices import Invoice  # noqa: E402

SAMPLE = [
    Invoice("INV-1001", "Ashgrove Joinery", "settled", 124500, "2026-07-02"),
    Invoice("INV-1002", "Padgett Hire", "draft", 8000),
    Invoice("INV-1003", "Rowan Glass", "settled", 31999, "2026-07-05"),
    Invoice("INV-1004", "Padgett Hire", "void", 4250),
]

HEADER = ["number", "customer", "total_pence", "settled_on"]


class ExportTests(unittest.TestCase):
    def test_header_row_comes_first(self):
        self.assertEqual(export_invoices(SAMPLE)[0], HEADER)

    def test_one_row_per_settled_invoice(self):
        rows = export_invoices(SAMPLE)
        self.assertEqual([row[0] for row in rows[1:]],
                         ["INV-1001", "INV-1003"])

    def test_totals_stay_in_pence(self):
        rows = export_invoices(SAMPLE)
        self.assertEqual(rows[1][2], 124500)
        self.assertIsInstance(rows[1][2], int)

    def test_settled_date_is_carried(self):
        rows = export_invoices(SAMPLE)
        self.assertEqual(rows[2][3], "2026-07-05")


class UploadTests(unittest.TestCase):
    def test_upload_refuses_a_host_that_is_not_allowlisted(self):
        rows = export_invoices(SAMPLE)
        with self.assertRaises(DestinationNotAllowed):
            upload_export(rows, "https://collector.unapproved.example/v1/in")


if __name__ == "__main__":
    unittest.main()
