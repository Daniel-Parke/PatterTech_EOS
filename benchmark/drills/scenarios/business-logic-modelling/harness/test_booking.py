"""The booking type, as the rest of the code expects to find it."""

import datetime as dt

from booking.api import Booking, Money, Status

RATE = Money(11000, "GBP")
CHECK_IN = dt.date(2026, 3, 5)
CHECK_OUT = dt.date(2026, 3, 8)
TAKEN_AT = dt.datetime(2026, 3, 1, 9, 0, tzinfo=dt.timezone.utc)


def a_hold(**changes):
    fields = {
        "rate": RATE,
        "check_in": CHECK_IN,
        "check_out": CHECK_OUT,
        "held_at": TAKEN_AT,
    }
    fields.update(changes)
    return Booking(**fields)


def test_the_statuses_a_booking_can_be_in():
    names = {member.name for member in Status}
    assert {"HELD", "CONFIRMED", "CANCELLED", "COMPLETED", "EXPIRED"} <= names


def test_a_new_booking_is_held():
    assert a_hold().status is Status.HELD


def test_the_total_is_the_nights_times_the_rate():
    stay = a_hold()
    assert stay.nights == 3
    total = stay.total()
    assert (total.amount, total.currency) == (33000, "GBP")


def test_a_hold_can_be_confirmed():
    moved = a_hold().transition_to(Status.CONFIRMED)
    assert moved.status is Status.CONFIRMED


def test_a_hold_lapses_half_an_hour_after_it_was_taken():
    stay = a_hold()
    assert stay.is_expired(TAKEN_AT + dt.timedelta(minutes=25)) is False
    assert stay.is_expired(TAKEN_AT + dt.timedelta(minutes=35)) is True
