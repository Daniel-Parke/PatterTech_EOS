"""Taking payment for an order."""

from pricing import discounted_total


def take_payment(gateway, order):
    """Price the order, authorise it and return a receipt line."""
    total = discounted_total(
        order["unit_price_pence"],
        order["quantity"],
        order["discount_percent"],
    )
    result = gateway.authorise(total, order["card_token"])
    return {
        "order_id": order["id"],
        "total_pence": total,
        "receipt": result["auth_code"],
        "status": result["status"],
    }
