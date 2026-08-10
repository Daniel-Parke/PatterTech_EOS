import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ledger.http import DestinationNotAllowed, check_destination  # noqa: E402
from ledger.invoices import Invoice, settled, total_pence  # noqa: E402

SAMPLE = [
    Invoice("INV-1001", "Ashgrove Joinery", "settled", 124500, "2026-07-02"),
    Invoice("INV-1002", "Padgett Hire", "draft", 8000),
    Invoice("INV-1003", "Rowan Glass", "settled", 31999, "2026-07-05"),
    Invoice("INV-1004", "Padgett Hire", "void", 4250),
]


class InvoiceTests(unittest.TestCase):
    def test_settled_keeps_order(self):
        self.assertEqual([i.number for i in settled(SAMPLE)],
                         ["INV-1001", "INV-1003"])

    def test_totals_add_up_in_pence(self):
        self.assertEqual(total_pence(settled(SAMPLE)), 156499)

    def test_a_float_total_is_refused(self):
        with self.assertRaises(TypeError):
            Invoice("INV-1005", "Ashgrove Joinery", "settled", 12.45)

    def test_an_unknown_status_is_refused(self):
        with self.assertRaises(ValueError):
            Invoice("INV-1006", "Rowan Glass", "posted", 100)


class DestinationTests(unittest.TestCase):
    def test_a_listed_host_is_allowed(self):
        self.assertEqual(
            check_destination("https://api.paycircle.example/v2/settlements"),
            "api.paycircle.example")

    def test_an_unlisted_host_is_refused(self):
        with self.assertRaises(DestinationNotAllowed):
            check_destination("https://somewhere.else.example/v1/thing")


if __name__ == "__main__":
    unittest.main()
