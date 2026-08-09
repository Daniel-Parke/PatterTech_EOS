# events-warehouse

Nightly exports from the storefront, and the small pipeline that turns
them into the tables the analysts query.

## Layout

- `raw/events.csv` — the app's event stream, exported nightly from the
  production database.
- `raw/experiment.csv` — assignments and conversions for the variant
  test that is running at the moment. See `docs/experiment-log.md`.
- `pipeline/build.py` — reads `raw/` and writes `warehouse/`.

## Running it

    python pipeline/build.py

That is the whole build. `warehouse/` is generated and is not committed.

## Known rough edges

- Event names come straight from whatever the app happened to emit at
  the time, so there are `_v2` and `_v3` suffixes in there.
- `order_total` is only filled in on the events that carry money.
- Nothing checks the exports before they land in `warehouse/`. If a
  nightly export comes through malformed we find out from a dashboard.
