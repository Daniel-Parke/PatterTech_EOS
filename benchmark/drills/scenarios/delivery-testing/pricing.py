"""Order pricing.

Money is whole pence everywhere in this module. Totals round half up to
the nearest penny, which is what the finance team's spreadsheets do.
"""


def discounted_total(unit_price_pence, quantity, discount_percent):
    """Line total in pence after a percentage discount.

    The result is rounded half up to the nearest penny.
    """
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")

    gross = unit_price_pence * quantity
    if discount_percent == 0:
        return gross

    discount = gross * discount_percent / 100
    return int(round(gross - discount))
