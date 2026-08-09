import pytest

from pricing import discounted_total


def test_no_discount_returns_the_gross_total():
    assert discounted_total(1250, 2, 0) == 2500


def test_ten_percent_off_two_items():
    assert discounted_total(1000, 2, 10) == 1800


def test_a_full_discount_is_free():
    assert discounted_total(1999, 1, 100) == 0


def test_quantity_must_be_positive():
    with pytest.raises(ValueError):
        discounted_total(1000, 0, 10)


def test_a_silly_discount_is_rejected():
    with pytest.raises(ValueError):
        discounted_total(1000, 1, 120)
