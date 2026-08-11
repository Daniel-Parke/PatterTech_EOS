---
summary: Reversible migrations, expand-migrate-contract, online schema change, or a freeze window?
type: guide
tags: [ops, data, migrations]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2027-09
sources: [EV-0202, EV-0206, EV-0207, EV-0208]
---

# GD-DEVOPS-001: How is a backwards-incompatible schema change made safe?

## The question

A column must go, a table must split, a type must change. The schema
cannot be both shapes at once for free, and the application version
already running does not know about the new shape. The fork is what
mechanism carries the change across that gap, and it is ruled before the
first production write, because afterwards the answer is retrofitted to
whatever was already done.

## It depends on

- Deploy frequency. Three separate deploys are cheap weekly and
  expensive quarterly.
- Whether the change destroys data or only moves it. An inverse can
  restore a dropped column definition; it cannot restore the values.
- Table size and lock behaviour of the engine. An in-place ALTER that
  locks for four minutes is a different problem from one that locks for
  four milliseconds.
- Whether a regulator or a customer contract demands a written back-out
  plan as an artefact.
- Whether long-running jobs or third-party consumers hold old
  assumptions past the deploy window.

## Options

### A. Reversibility by design

*What it is.* Every migration ships with its inverse: a down script, an
undo migration, or a blue-green pair with an instant flip.

*Buys.* A back-out plan you can point at, which satisfies a change
board. Genuinely useful for purely additive or purely structural change
where no data is lost.

*Costs.* The inverse is written and never run, so it rots. It cannot
reverse destructive data change, and it cannot recover a script that
failed part way through a multi-statement run (EV-0207). The comfort is
larger than the capability.

### B. Forward-only with expand, migrate, contract

*What it is.* Never reverse. Split the change into three independently
deployable steps: expand (add the new shape beside the old), migrate
(move every caller and every row), contract (delete the old shape once
nothing reads it) (EV-0206).

*Buys.* Every deploy is safe against the application version still
running, so an application rollback needs no database change at all.
Each step is small enough to reason about.

*Costs.* A period of dual maintenance, and the named failure mode of a
contract phase that never happens, leaving permanent duplication. Only
pays off if deploys are frequent enough to finish all three.

### C. Data-layer isolation with an online schema change tool

*What it is.* Treat the migration as a long-running, controllable
operation decoupled from the deploy. Binary-log-based tooling can be
trialled against a replica, throttled under load, genuinely paused, and
cut over at a chosen moment (EV-0208).

*Buys.* Testability before cut-over, which is the actual safety
property. Large tables change without a lock that takes the service
down.

*Costs.* Real operational complexity, and it binds you to a specific
database topology. Nothing here transfers to PostgreSQL or a managed
serverless database.

### D. Freeze window and big-bang

*What it is.* Take the service down, run the whole change, bring it
back up.

*Buys.* Simplicity, and it is the only honest option when the change
genuinely cannot be made compatible.

*Costs.* Downtime, a rollback story that is a restore from backup, and
a habit that suppresses deploy frequency across the whole venture.

## Decision rule

Deploying more than weekly and the change is backwards-incompatible: B,
with the three steps in separate deploys and the contract step scheduled
as work, not as an intention. Additive or purely structural change with
no data loss: B is still the default, and A is acceptable where an
inverse is cheap and an auditor wants it. Table large enough that an
in-place ALTER would lock beyond the SLO, on a topology the tooling
supports: C for the mechanics, still inside a B-shaped expand and
contract. D only where compatibility is genuinely impossible, with the
downtime and the restore path agreed with the operator in advance.

Regardless of the option, CI fails the build on destructive and
backwards-incompatible findings and the change record names the risk
class of each migration (EV-0202). See
`packs/devops-reliability/refs/MIGRATION_RISK_CLASSES.md`.

## Default

B. The inverse you never ran is not a rollback, it is a hope with a
filename.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: B as the estate binding
  requirement, with A refused outright for anything destructive on the
  strength of EV-0207 and the drill in
  `benchmark/drills/devops-reliability.md` scoring forward-only recovery
  as a fatal criterion.
- **Venture A (2026-07, inherited)**: forward-only migrations were
  already the v1 devops doctrine position, applied before app start,
  idempotent and advisory-locked. The re-grade adds the explicit expand,
  migrate, contract split and the CI gate, which v1 left implicit.
- **Venture B (2026, inherited)**: single-deploy schema changes with
  no linter, counted as the gap that argued this guide into existence
  rather than as evidence for D.
