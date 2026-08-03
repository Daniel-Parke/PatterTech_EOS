---
summary: Worked example, replacing users.email_address with a normalised contacts table without a change window
type: example
tags: [ops, data, migrations]
kind: exemplar
scope: estate
sources: [EV-0201, EV-0202, EV-0204, EV-0206, EV-0209]
---

# EX-DEVOPS-001: from users.email_address to a contacts table

The situation the pack was built for. A live service stores one email
address per user in `users.email_address`. Product now needs several
contacts per user, so the column must be replaced by a normalised
`contacts` table. The service stays releasable throughout and the data
must be provably recoverable. This walks the whole thing.

## 1. Route the task

The diff will contain DDL and a column drop, so the router in
`kernel/POLICY_SPEC.md` activates the schema-change factor (floor R2)
and the destructive-migration factor (floor R3). Ruling: R3, high
assurance plus a recorded operator approval for the contract step. The
drop of a column holding live data is a deletion under
`kernel/GUARD_SPEC.md`, which is manual-only, so the agent prepares it
and does not run it.

The pack activates on `runs_schema_migrations` and
`stores_persistent_data`, both true.

## 2. Prove recovery before changing anything

Requirement 5 comes first, because the change is destructive and the
restore path is the only thing standing behind it. Following
`packs/devops-reliability/refs/RESTORE_DRILL_EVIDENCE.md`:

- RTO 3600 seconds, RPO 86400 seconds, both the operator's numbers.
- Hypothesis, written down first: after restoring the latest snapshot
  into a scratch instance, every email address present at capture reads
  back with the same row count and the same value set.
- Capture the pre-drill value set from the live source.
- Restore into a scratch instance, run the validation query, compare.
- Record elapsed 702 seconds against the 3600 RTO, 4128 rows validated,
  result pass, and tear the scratch instance down.

The evidence record lands in the venture's evidence directory as JSON
with the fixed key set. Re-running the committed script regenerates the
same keys, which is what makes it evidence rather than a claim.

## 3. Split the change into three deploys

Expand, migrate, contract (EV-0206), one deploy each, per
`packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md`.

| Ordinal | File | Risk class | Deploy |
| --- | --- | --- | --- |
| 0007 | add contacts table, unique on (user_id, email) | additive | expand |
| 0008 | backfill contacts from users.email_address, dual-write trigger | data-dependent | expand |
| 0009 | drop users.email_address | destructive | contract |

No file contains both an additive statement and a drop on the same
subject. Ordinals continue the existing history with no gaps and no
duplicates. There are no down files, and the change record asserts
`recovery: forward-only`.

Migration 0008 is data-dependent: the unique constraint on 0007 fails
only if duplicates exist, so a pre-flight count runs first and the
result goes in the change record. That is a warning class, not a build
failure, precisely because the linter cannot know.

## 4. Hold the compatibility window open

After 0007 and 0008 the old application version still reads
`users.email_address` and the new one reads `contacts`, and both are
correct. The pre-existing test suite runs unchanged against the
post-expand schema, which is the proof that the window is real rather
than asserted. Nothing in the test suite is edited to make this pass; an
edited test proves nothing about the running application.

Reads move behind a flag, registered per
`packs/devops-reliability/refs/FLAG_AND_ROLLOUT_LIFECYCLE.md`: key
`contacts_read_path`, owner named, expires in eight weeks,
`terminal_value: true`, kind release.

## 5. Roll out with a machine deciding

The read-path change is user-facing, so a rollout object declares the
metric provider, a success condition, a failure condition and a failure
limit, aborting back to the last stable version automatically
(EV-0204). A dry run against an injected failing metric returns abort,
which is the only way to know the abort path works before it is needed.

The abort protects the serving tier only. Rows written by the canary
through the new path are still there afterwards, which is exactly why
0008 keeps the old column populated by dual write until contract.

## 6. Name the SLI at risk

The service's OpenSLO object is unchanged and still validates. The
change record names `api-availability` as the SLI at risk, because the
backfill in 0008 touches every row and the contract in 0009 takes a
brief lock. If the error budget is already spent, the error budget
policy in `packs/devops-reliability/refs/SLO_AND_ERROR_BUDGET.md` says
this waits: it is neither a P0 fix nor security work.

## 7. Contract, and only then

0009 ships as a separate deploy once telemetry shows no reads of
`users.email_address` for a full window. It is a deletion of live data,
so it goes to the operator with a recorded approval, not an assertion in
prose. Once it lands, the flag reaches its terminal value, the dead
branch is deleted, and the registry entry goes with it.

## What the change record ends up carrying

Migration files with risk classes and subjects, `recovery: forward-only`,
the compatibility-window statement, the SLI at risk, the pre-flight
duplicate count, a pointer to the restore evidence record, and the flag
entry with owner and expiry. Every one of those is a field a script can
read, which is the point.

## Where this could still go wrong

The contract deploy is the step that gets deferred forever, leaving
permanent duplication. It is scheduled as work with the flag expiry as
its deadline, because an intention is not a schedule.
