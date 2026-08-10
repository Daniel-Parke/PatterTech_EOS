from app import billing


def test_first_payment_carries_the_joining_fee():
    assert billing.first_payment_pence() == 898


def test_recurring_payment_drops_the_joining_fee():
    assert billing.recurring_payment_pence() == 648


def test_storage_is_added_only_when_asked_for():
    assert billing.recurring_payment_pence(extra_storage=True) == 848


def test_format_gbp():
    assert billing.format_gbp(898) == "£8.98"
