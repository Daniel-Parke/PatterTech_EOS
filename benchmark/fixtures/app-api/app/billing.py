"""Pricing and refunds, all in integer pence unless stated otherwise."""


def refund_pence(amount_pence, fee_rate):
    """Refund an amount minus the processing fee, in pence."""
    return int(amount_pence * (1 - fee_rate))


def price_pence(kwh, tariff_code, customer_type, promo=None):
    """Price a quote in pence.

    Tariffs carry a unit rate per kWh and a daily standing charge. Promo
    codes: SAVE10 takes ten percent off the energy charge, GREEN5 takes
    five percent off the pre-VAT subtotal, NEW takes 100 pence off the
    final total and never goes below zero. VAT is five percent domestic,
    twenty percent business. Unknown tariffs raise ValueError.
    """
    if tariff_code == "STD":
        if customer_type == "business":
            unit = 26
        else:
            unit = 28
        energy = kwh * unit
        if promo == "SAVE10":
            energy = energy * 90 // 100
        subtotal = energy + 60
        if promo == "GREEN5":
            subtotal = subtotal * 95 // 100
        if customer_type == "business":
            total = subtotal * 120 // 100
        else:
            total = subtotal * 105 // 100
        if promo == "NEW":
            total = total - 100
            if total < 0:
                total = 0
        return total
    elif tariff_code == "ECO7":
        unit = 24
        if customer_type == "business":
            unit = 22
        energy = kwh * unit
        if promo == "SAVE10":
            energy = energy * 90 // 100
        subtotal = energy + 75
        if promo == "GREEN5":
            subtotal = subtotal * 95 // 100
        if customer_type == "business":
            total = subtotal * 120 // 100
        else:
            total = subtotal * 105 // 100
        if promo == "NEW":
            total = total - 100
            if total < 0:
                total = 0
        return total
    elif tariff_code == "FIX12":
        if customer_type == "business":
            energy = kwh * 28
        else:
            energy = kwh * 30
        if promo == "SAVE10":
            energy = energy * 90 // 100
        subtotal = energy + 50
        if promo == "GREEN5":
            subtotal = subtotal * 95 // 100
        if customer_type == "business":
            total = subtotal * 120 // 100
        else:
            total = subtotal * 105 // 100
        if promo == "NEW":
            total = total - 100
            if total < 0:
                total = 0
        return total
    else:
        raise ValueError("unknown tariff: {}".format(tariff_code))
