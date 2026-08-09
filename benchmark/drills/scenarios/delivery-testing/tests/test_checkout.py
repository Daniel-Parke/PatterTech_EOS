from checkout import take_payment
from fakes import FakeGateway

ORDER = {
    "id": "ord_5512",
    "unit_price_pence": 1250,
    "quantity": 2,
    "discount_percent": 0,
    "card_token": "tok_live_4h2",
}


def test_payment_is_authorised_for_the_discounted_total():
    gateway = FakeGateway()
    result = take_payment(gateway, ORDER)
    assert gateway.calls == [(2500, "tok_live_4h2")]
    assert result["total_pence"] == 2500
    assert result["status"] == "approved"


def test_the_receipt_carries_the_authorisation_code():
    result = take_payment(FakeGateway(), ORDER)
    assert result["receipt"] == "AC0001"
