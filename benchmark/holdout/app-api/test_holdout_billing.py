"""Holdout for T04: refund_pence must round half-even, not truncate.

Expected to fail on the shipped fixture, which truncates via int().
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "fixtures" / "app-api"))

from app import billing


class TestRefundRounding(unittest.TestCase):
    def test_round_amounts_still_hold(self):
        self.assertEqual(billing.refund_pence(1000, 0.10), 900)
        self.assertEqual(billing.refund_pence(2000, 0.25), 1500)
        self.assertEqual(billing.refund_pence(800, 0.5), 400)
        self.assertEqual(billing.refund_pence(0, 0.10), 0)

    def test_odd_amount_rounds_up(self):
        # 1001 * 0.90 = 900.9, half-even gives 901. Truncation gives 900.
        self.assertEqual(billing.refund_pence(1001, 0.10), 901)

    def test_more_odd_amounts(self):
        # Chosen so truncation disagrees with half-even under either a
        # float-plus-round fix or a Decimal fix.
        self.assertEqual(billing.refund_pence(2011, 0.10), 1810)
        self.assertEqual(billing.refund_pence(1001, 0.15), 851)
        self.assertEqual(billing.refund_pence(333, 0.10), 300)

    def test_half_even_tie(self):
        # 1015 * 0.90 = 913.5 exactly; half-even resolves the tie to 914.
        self.assertEqual(billing.refund_pence(1015, 0.10), 914)


if __name__ == "__main__":
    unittest.main()
