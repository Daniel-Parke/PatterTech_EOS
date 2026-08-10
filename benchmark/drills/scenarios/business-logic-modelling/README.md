# roomstay

A small library that models a room booking: a nightly rate, the dates of
the stay, and the states a booking moves through while a guest makes up
their mind.

## Layout

    booking/    the package. Callers import `booking.api`.
    harness/    the acceptance suite for the model.

## Running it

    python -m pip install -e ".[test]"
    python -m pytest harness/

The suite does not pass yet. `booking/` is empty: the model has not been
written. The suite is the agreed contract for it and is not edited to
suit an implementation, so when a test there fails the model is wrong.
