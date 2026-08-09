"""The money type, as the rest of the code expects to find it."""

from booking.api import Money


def test_money_is_a_currency_and_a_whole_number_of_minor_units():
    price = Money(1099, "GBP")
    assert price.currency == "GBP"
    assert price.amount == 1099
    assert isinstance(price.amount, int)
    assert not isinstance(price.amount, bool)


def test_money_renders_as_a_plain_amount():
    assert str(Money(250, "GBP")) == "2.50"


def test_money_adds_within_a_currency():
    total = Money(1099, "GBP") + Money(401, "GBP")
    assert (total.amount, total.currency) == (1500, "GBP")


def test_money_multiplies_by_a_count():
    nightly = Money(11000, "GBP")
    assert (nightly * 3).amount == 33000
