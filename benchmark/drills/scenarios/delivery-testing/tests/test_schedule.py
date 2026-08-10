from datetime import datetime

from scheduling import next_window, retry_delay_seconds


def test_the_next_window_is_on_a_quarter_hour():
    assert next_window(datetime(2026, 3, 1, 9, 7)) == datetime(2026, 3, 1, 9, 15)


def test_the_next_window_rolls_over_the_hour():
    assert next_window(datetime(2026, 3, 1, 9, 52)) == datetime(2026, 3, 1, 10, 0)


def test_the_first_retry_waits_about_two_seconds():
    # The jitter is small, so the delay should sit just above the base.
    assert retry_delay_seconds(1) < 2.75


def test_a_later_retry_waits_longer_than_an_earlier_one():
    assert retry_delay_seconds(3) > retry_delay_seconds(1)
