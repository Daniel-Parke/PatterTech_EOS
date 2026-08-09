# Postbox

The marketing site and the small service behind it. One deployable,
running on our own boxes behind the load balancer. Nothing here is
shipped to anybody: people reach it over the web and that is the only
way it is ever used.

## Layout

- `app/` the service. `server.py` holds the WSGI callable.
- `tests/` what we have. `make test` runs them.
- `third_party/` source we copied in rather than depended on.
- `vendor/` the unpacked snapshot of the internal package index. The
  build boxes have no network, so the wheels live in the tree. It goes
  on `PYTHONPATH`; the Makefile does that for you.
- `sbom/inventory.json` the component list `scripts/licence_scan.py`
  writes. CI runs the scan and fails if the file is stale.
- `docs/` deployment notes and whatever compliance we have written down.

## Running it

    make test
    make run

Python 3.11 or newer. Nothing else to install.

## Deploys

Tagged, then `ops deploy postbox`. See `docs/deploy.md`.
