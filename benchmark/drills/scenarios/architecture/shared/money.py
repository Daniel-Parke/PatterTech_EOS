"""Money handling shared by both domains. Depends on neither."""

from decimal import Decimal


def pence(amount):
    """Return the amount in whole pence, rounding half up."""
    return int((Decimal(str(amount)) * 100).quantize(Decimal("1")))


def format_gbp(amount):
    return "GBP %.2f" % (pence(amount) / 100.0)
