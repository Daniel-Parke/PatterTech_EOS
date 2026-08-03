---
summary: Single-run cold-agent acceptance drill for the devops-reliability pack, with deterministic machine-checkable criteria.
type: example
tags: [eos]
---

# Drill: ship a destructive schema change safely

## Scenario

A cold agent, given only this pack and a seeded fixture repository, is
told: the `users.email_address` column must be replaced by a normalised
`contacts` table, the service must stay releasable throughout, and the
data must be provably recoverable. One run, no human hints.

The fixture supplies a service with a migrations directory, a CI
workflow file, a running database container with seeded rows, an SLO
file, a flag configuration file, and an empty `evidence/` directory.
The agent produces migration files, CI configuration, a rollout
configuration, a restore-drill script with its recorded output, and a
change record naming the risk class of each migration.

## Machine-checkable criteria

A run passes only if all of the following hold. Every check is a script
over the produced tree and container state, no judgement calls.

1. Three or more migration files exist, and no single file contains both
   an additive statement and a `DROP COLUMN` or `DROP TABLE` on the same
   subject. Expand and contract are separate deploys.
2. No file matches a down or undo naming pattern, and the change record
   asserts forward-only recovery in a parseable field.
3. Migration ordinals are strictly increasing, no duplicates, no gaps
   against the pre-existing history.
4. CI invokes a migration linter that exits non-zero on destructive and
   backwards-incompatible findings, verified against a seeded bad fixture.
5. Applying every migration in order succeeds, and the seeded email
   values read back through `contacts` with identical row count and
   identical value set to the pre-run capture.
6. Applying up to the expand step and running the pre-existing test
   suite unchanged passes, proving the compatibility window.
7. `evidence/restore-drill.json` parses with keys `started_at`,
   `completed_at`, `elapsed_seconds`, `rto_seconds`, `rpo_seconds`,
   `rows_validated`, `validation_query`, `result`, and re-running the
   committed script regenerates the same key set.
8. In that file `result` equals `pass`, `elapsed_seconds` is at most
   `rto_seconds`, and `rows_validated` is greater than zero.
9. The SLO file still validates against the OpenSLO schema and the
   change record names the SLI at risk.
10. Every added flag entry has non-empty `owner` and `expires`, and
    `expires` parses as a date after the run date.
11. The rollout configuration declares a failure condition and automatic
    abort, and a dry-run against an injected failing metric returns
    abort, not promotion.
12. No secret-shaped string in the diff, and
    `python tools/eos_check.py --repo` exits zero.

## Scoring

Pass requires 12 of 12. Criteria 1, 2, 5 and 8 are fatal.
