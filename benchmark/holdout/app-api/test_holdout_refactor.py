"""Holdout for T11: price_pence behaviour is pinned through the refactor.

Contains an independent reference implementation of the pricing spec and
compares it with app.billing.price_pence over the full input matrix. This
suite passes on the shipped fixture, because the shipped pricing is
correct; its job is to catch behaviour drift during the refactor.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "fixtures" / "app-api"))

from app import billing

RATES = {
    # tariff -> (domestic_unit, business_unit, standing)
    "STD": (28, 26, 60),
    "ECO7": (24, 22, 75),
    "FIX12": (30, 28, 50),
}


def reference_price_pence(kwh, tariff_code, customer_type, promo):
    """Clean restatement of the pricing spec, integer pence throughout."""
    if tariff_code not in RATES:
        raise ValueError("unknown tariff: {}".format(tariff_code))
    domestic_unit, business_unit, standing = RATES[tariff_code]
    unit = business_unit if customer_type == "business" else domestic_unit
    energy = kwh * unit
    if promo == "SAVE10":
        energy = energy * 90 // 100
    subtotal = energy + standing
    if promo == "GREEN5":
        subtotal = subtotal * 95 // 100
    vat_multiplier = 120 if customer_type == "business" else 105
    total = subtotal * vat_multiplier // 100
    if promo == "NEW":
        total = max(total - 100, 0)
    return total


class TestPricePenceStaysPinned(unittest.TestCase):
    def test_full_matrix_matches_reference(self):
        for kwh in (0, 1, 7, 100, 250):
            for tariff in ("STD", "ECO7", "FIX12"):
                for customer_type in ("domestic", "business"):
                    for promo in (None, "SAVE10", "GREEN5", "NEW"):
                        with self.subTest(
                            kwh=kwh,
                            tariff=tariff,
                            customer_type=customer_type,
                            promo=promo,
                        ):
                            self.assertEqual(
                                billing.price_pence(kwh, tariff, customer_type, promo),
                                reference_price_pence(kwh, tariff, customer_type, promo),
                            )

    def test_literal_spot_pins(self):
        self.assertEqual(billing.price_pence(100, "STD", "domestic", None), 3003)
        self.assertEqual(billing.price_pence(100, "STD", "business", None), 3192)
        self.assertEqual(billing.price_pence(100, "ECO7", "domestic", "SAVE10"), 2346)
        self.assertEqual(billing.price_pence(50, "FIX12", "business", "GREEN5"), 1652)
        self.assertEqual(billing.price_pence(10, "STD", "domestic", "NEW"), 257)
        self.assertEqual(billing.price_pence(0, "ECO7", "domestic", "NEW"), 0)
        self.assertEqual(billing.price_pence(250, "STD", "domestic", None), 7413)
        self.assertEqual(billing.price_pence(400, "FIX12", "business", "GREEN5"), 12824)

    def test_unknown_tariff_still_raises(self):
        with self.assertRaises(ValueError):
            billing.price_pence(100, "MEGA", "domestic", None)


if __name__ == "__main__":
    unittest.main()
