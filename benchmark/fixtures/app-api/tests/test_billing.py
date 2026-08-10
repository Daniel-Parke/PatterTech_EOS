"""Unit tests for pricing and refunds."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import billing


class TestRefundPence(unittest.TestCase):
    def test_ten_percent_fee(self):
        self.assertEqual(billing.refund_pence(1000, 0.10), 900)

    def test_quarter_fee(self):
        self.assertEqual(billing.refund_pence(2000, 0.25), 1500)

    def test_half_fee(self):
        self.assertEqual(billing.refund_pence(800, 0.5), 400)

    def test_zero_amount(self):
        self.assertEqual(billing.refund_pence(0, 0.10), 0)


class TestPricePence(unittest.TestCase):
    def test_std_domestic_no_promo(self):
        # 100 kWh at 28p plus 60p standing, then 5 percent VAT.
        self.assertEqual(billing.price_pence(100, "STD", "domestic", None), 3003)

    def test_std_business_no_promo(self):
        # 100 kWh at 26p plus 60p standing, then 20 percent VAT.
        self.assertEqual(billing.price_pence(100, "STD", "business", None), 3192)

    def test_eco7_domestic_save10(self):
        # SAVE10 discounts the energy charge only.
        self.assertEqual(billing.price_pence(100, "ECO7", "domestic", "SAVE10"), 2346)

    def test_fix12_business_green5(self):
        # GREEN5 discounts the pre-VAT subtotal.
        self.assertEqual(billing.price_pence(50, "FIX12", "business", "GREEN5"), 1652)

    def test_std_domestic_new(self):
        # NEW takes 100 pence off after VAT.
        self.assertEqual(billing.price_pence(10, "STD", "domestic", "NEW"), 257)

    def test_new_floors_at_zero(self):
        self.assertEqual(billing.price_pence(0, "ECO7", "domestic", "NEW"), 0)

    def test_zero_kwh_still_pays_standing(self):
        self.assertEqual(billing.price_pence(0, "STD", "domestic", None), 63)

    def test_fix12_domestic_save10_small(self):
        self.assertEqual(billing.price_pence(7, "FIX12", "domestic", "SAVE10"), 250)

    def test_eco7_business_green5(self):
        self.assertEqual(billing.price_pence(250, "ECO7", "business", "GREEN5"), 6355)

    def test_unknown_tariff_raises(self):
        with self.assertRaises(ValueError):
            billing.price_pence(100, "MEGA", "domestic", None)


if __name__ == "__main__":
    unittest.main()
