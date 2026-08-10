---
summary: Holdout tests for the app-api fixture, scored after tasks, never shown to agents
type: example
tags: [eos, testing]
---

# app-api holdout suite

Standalone unittest files that pin post-task behaviour for the app-api
fixture. Each file adds `benchmark/fixtures/app-api` to `sys.path` on its
own, so any file runs directly with `python <file>` from anywhere.

## Purpose and expected results

These tests score task outcomes and catch regressions in timing-ablation
runs. On the shipped fixture only `test_holdout_refactor.py` passes,
because the pricing it pins is correct today. The rest fail until their
task is done, each for one intended reason:

| file | task | intended failure on the shipped fixture |
| --- | --- | --- |
| test_holdout_billing.py | T04 | refund truncation: odd amounts come back one penny short |
| test_holdout_summary.py | T03 | `GET /quotes/summary` does not exist, so requests get 404 |
| test_holdout_auth.py | T07 | a non-admin token gets 200 from `/admin/reports` instead of 403 |
| test_holdout_migration.py | T06 | no `003` migration, so `users.marketing_opt_in` is missing |
| test_holdout_refactor.py | T11 | passes now and must keep passing through the refactor |

## Visibility

This suite is excluded from materialised fixtures and is never shown to
benchmarked agents. It is visible to the build side of the benchmark, so
whoever writes tasks can read it. That asymmetry is a recorded limitation:
a leak of this directory into a fixture would let an agent code to the
scoring tests.
