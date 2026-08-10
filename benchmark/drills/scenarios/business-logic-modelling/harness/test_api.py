"""What the package exposes to the rest of the world."""

import booking.api


def test_the_api_module_carries_the_model():
    for name in ("Money", "Booking", "Status"):
        assert hasattr(booking.api, name), "booking.api is missing %s" % name
