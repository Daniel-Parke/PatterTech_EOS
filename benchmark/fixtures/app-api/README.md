---
summary: Energy quote JSON API fixture with planted defects for benchmark tasks
type: example
tags: [eos, testing]
---

# app-api fixture

A small energy quote API built on `http.server` and `sqlite3`, stdlib only.
It is a benchmark fixture: some defects are planted on purpose and some
features are missing on purpose. The task table below is the ground truth.

## Running

```
python run.py
```

This creates `data/app.db`, applies `migrations/*.sql` in filename order,
seeds three users and four quotes when the users table is empty, and serves
on `http://127.0.0.1:8765`. Seed passwords are `admin-pass`, `alice-pass`
and `bob-pass`.

`requirements.txt` names `jsonlogx` for structured logging. When it is not
installed the app falls back to the vendored `app/loglite.py`, which is what
actually runs.

## Endpoints

| method and path | auth | behaviour |
| --- | --- | --- |
| POST /login | none | body `{email, password}`, returns `{token}`, 401 on bad credentials, 400 on a bad body |
| GET /quotes | Bearer token | the authenticated user's quotes, 401 without a valid token |
| POST /quotes | Bearer token | body `{kwh, tariff_code, customer_type, promo?}`, validates inputs, prices via `app/billing.py`, returns 201 with the quote |
| GET /admin/reports | Bearer token | aggregate report: count, total_pence, by_tariff |
| anything else | | 404 |

## Schema

- `users`: id, email unique, password_hash (sha256 hex), role (`user` or
  `admin`), created_at.
- `quotes`: id, user_id, kwh, tariff_code, customer_type, promo,
  price_pence, created_at.
- `schema_migrations`: filename, applied_at. Written by
  `app.db.apply_migrations`, which applies each migration file exactly once.

## Pricing rules

Integer pence throughout. Unit rate per kWh and standing charge by tariff:
STD 28 domestic, 26 business, 60 standing; ECO7 24, 22, 75; FIX12 30, 28,
50. Promo codes: SAVE10 takes ten percent off the energy charge, GREEN5
takes five percent off the pre-VAT subtotal, NEW takes 100 pence off the
final total and never goes below zero. VAT is five percent domestic and
twenty percent business. Unknown tariffs raise ValueError.

## Tests

Run the visible diagnostic suite from this directory:

```
python -m unittest discover -s tests
```

It passes on the shipped fixture. It deliberately does not cover the
planted defects below; the holdout suite in `benchmark/holdout/app-api/`
does, and is never shown to benchmarked agents.

## Task table

| id | kind | where | detail |
| --- | --- | --- | --- |
| T03 | missing feature | app/server.py | no `GET /quotes/summary` endpoint; spec wants `{count, total_pence, mean_pence}` for the authenticated user, mean rounded half-even |
| T04 | planted defect | app/billing.py | `refund_pence` truncates with `int()`; `refund_pence(1001, 0.10)` gives 900 where half-even rounding gives 901 |
| T06 | missing migration | migrations/ | no `003` migration adding `users.marketing_opt_in` defaulting to 0 for legacy and new rows |
| T07 | planted defect | app/server.py | `/admin/reports` checks only that the token is valid, not that the role is `admin`; a plain user gets 200 where the spec wants 403 |
| T11 | refactor target | app/billing.py | `price_pence` is three near identical tariff branches; behaviour is correct and must stay pinned through any refactor |
