# orders-service

The order capture service behind the storefront. It exposes a small HTTP
API described by `api/openapi.yaml`, and it receives payment events from
the payment provider on `/webhooks/payments`.

## Layout

- `api/openapi.yaml` is the source of truth for the public API. The
  handlers are written to it, not the other way round.
- `api/baseline/openapi.yaml` is the copy of the spec as it stood at the
  last release. It is updated by hand when a release ships, and it is
  what we compare against when we want to know what changed.
- `app/` holds the Flask application. `app/main.py` has the order
  endpoints, `app/webhooks.py` has the payment receiver, `app/store.py`
  is the in-memory store we still have not replaced.
- `tests/` runs under pytest.

## Running it

    pip install -r requirements.txt
    flask --app app.main run

## Tests

    python -m pytest

## Consumers

The storefront web client and the warehouse picking tool both read
`GET /orders`. The warehouse tool is on a six week release train, so
anything that changes the shape of an order needs to keep working for a
client that has not been rebuilt yet.
