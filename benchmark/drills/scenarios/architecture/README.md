# Billing and catalogue

A small Python service with three packages.

- `billing` raises invoices.
- `catalogue` owns product data and exposes it through `catalogue.api`.
  Everything under `catalogue/internal/` is a storage or calculation
  detail and is not meant for callers outside the package.
- `shared` carries money handling.

Run the tests with `python -m pytest`. There are none yet.
