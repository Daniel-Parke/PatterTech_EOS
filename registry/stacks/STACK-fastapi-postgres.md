---
summary: Profile 02, FastAPI on Postgres, shape, caps and hard-won constraints
type: stack
tags: [infra, hosting, data, testing]
status: active
review: 2027-01
---

# Stack profile 02: FastAPI on Postgres

The default stack for APIs and services with a database. Reference
implementation: WiseWattage (its `pyproject.toml`, `docker/` and
`docs/ADR-001/002/003/006/007` are the receipts).

## Shape

- Python 3.11 or 3.12, uv for installs (no pip in production images),
  FastAPI 0.115+, Pydantic v2 for every contract.
- Postgres 16 (TimescaleDB where time-series demands it). Driver:
  psycopg 3 with psycopg-pool. Repositories speak raw SQL behind a
  repository layer; no ORM by default.
- Migrations: forward-only, idempotent, advisory-locked, applied by a
  runner before app start; a failed migration fails the deploy closed.
- Auth: the identity provider behind an adapter; the venture's own
  database stays the authorisation source of truth.
- Background work: in-process executor by default; a durable Postgres
  claim queue (`FOR UPDATE SKIP LOCKED`, stale-claim reaping, a
  unit-builder registry because closures do not serialise) behind a
  flag when jobs must survive deploys.
- Observability: Sentry, inert without its DSN. Rate limits fail open
  for anonymous traffic and fail closed on billing-tier reads.
- Testing: pytest with xdist, integration suites against a real
  Postgres service container, coverage floors ratcheted upwards.
- Container: slim Python base, multi-stage, healthcheck endpoint;
  the dependency layer keyed on `pyproject.toml` alone.

## Constraints to design around

- Cap `urllib3>=2.2,<2.5`: 2.5+ moved ProxyConfig and broke Railway
  startup at import time in WiseWattage, 2026-07; lift the cap only
  after a real deploy proves it. This profile is where the rule lives.
  The lessons ledger carries the harvest row it came from and names
  this profile as its owner, which is provenance rather than a second
  home for the rule.
- The Docker dependency layer must never be keyed on source: a stale
  layer with fresh code shipped a broken prod once. Key on the
  manifest, nothing else.
- Feature flags default off, documented per flag; rollback is a flag
  flip, not a deploy.
- Every persisted table needs a named consumer and a retention plan
  before it lands; an audit hypertable with neither once filled a
  storage tier alone. Never time-based retention on representative-year
  timestamps.
- Keyset pagination on `(updated_at, id)` with an opaque cursor for
  every list endpoint; offset pagination does not scale past toy data.
- Webhooks: standard-library HMAC-SHA256 verification, idempotency via
  a processed-events primary key, no provider SDKs.
- Batch inserts (`executemany`) for anything high-volume; row-by-row
  into hypertables is a performance cliff.

## When not to use this profile

No server state: profile 01.

Where heavy telemetry goes is not this profile's question to answer.
`packs/architecture/guides/WG-ARCH-008-database-topology.md` owns it and
D8 of `packs/architecture/PACK.md` carries the live default, which is
one database with private tables and distinct credentials, and two
stores only once a second real owner or a genuinely volume-asymmetric
feed appears. This profile used to answer it with a blanket separate
stores, which was v1's answer and predates that guide.
