# kestrel-orders

The small service behind order totals, card authorisation and payment
reminders. It is imported by the storefront and by the back office job
runner; there is no web layer here.

## Layout

- `pricing.py` works out what a line costs after a discount. Money is
  whole pence throughout and totals round half up to the nearest penny,
  matching the finance team's spreadsheets.
- `gateway.py` is the client for the Kestrel payments API. It takes a
  `transport` callable so the tests can drive it without a network.
- `fakes.py` holds the in-memory stand-ins the tests use.
- `checkout.py` puts pricing and authorisation together.
- `scheduling.py` works out when unpaid invoice reminders go out.

## Running the tests

    python -m pip install -e ".[dev]"
    python -m pytest

## Known issues

- Finance have flagged that some half price orders come out a penny
  short on the invoice. Nobody has pinned down which ones yet.
- `tests/test_schedule.py` goes red now and then on CI and passes when
  you run it again. It has been rerun by hand three times this month.
