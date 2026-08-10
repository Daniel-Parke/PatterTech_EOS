# ledger

A small billing helper. It holds invoices, totals them in pence, and
talks to a couple of outside services.

## Layout

- `ledger/invoices.py` owns the invoice record and the status filters.
- `ledger/http.py` is the only way out to the network. Every request
  goes through the host allowlist in `config/allowed-domains.txt`;
  anything not on the list is refused before the request is made.
- `ledger/settings.py` reads configuration. Keys come from the
  environment, never from a file in the repository.
- `docs/exceptions.md` is the append-only register for egress
  exceptions.

## Running the tests

    python -m pytest

or, if pytest is not installed,

    python -m unittest discover -s tests

## Configuration

`config/example.env` is the template. Copy it to
`config/<service>.env` and fill in the values. Real credentials live in
the secret store, not in the repository.
