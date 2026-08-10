"""Calculation detail. Off limits to anything outside the catalogue."""


def apply_discount(list_price, fraction):
    if not 0 <= fraction < 1:
        raise ValueError("fraction must be in [0, 1)")
    return list_price * (1 - fraction)
