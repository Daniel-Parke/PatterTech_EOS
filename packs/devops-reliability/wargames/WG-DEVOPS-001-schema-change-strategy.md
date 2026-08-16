---
id: WG-DEVOPS-001
summary: Reversible migrations, expand-migrate-contract, online schema change, or a freeze window?
kind: wargame
type: wargame
tags: [data, eos, migrations, ops, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DEVOPS-001]
applies_when: [deploys_to_environment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0202, EV-0206, EV-0207, EV-0208]
review: 2027-09
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DEVOPS-001: How is a backwards-incompatible schema change made safe?

## Decision question and stakes

A column must go, a table must split, a type must change. The schema
cannot be both shapes at once for free, and the application version
already running does not know about the new shape. The fork is what
mechanism carries the change across that gap, and it is ruled before the
first production write, because afterwards the answer is retrofitted to
whatever was already done.

## Doctrines or coverage gap under pressure

- `DOC-DEVOPS-001` (binding): Backwards-incompatible schema change ships as expand, migrate, contract, in separate deploys.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `deploys_to_environment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Reversibility by design

Assume `A. Reversibility by design` was selected and the outcome failed. Test this option's stated failure mechanism first: * The inverse is written and never run, so it rots. It cannot reverse destructive data change, and it cannot recover a script that failed part way through a multi-statement run (EV-0207). The comfort is larger than the capability.

### Premortem for B. Forward-only with expand, migrate, contract

Assume `B. Forward-only with expand, migrate, contract` was selected and the outcome failed. Test this option's stated failure mechanism first: * A period of dual maintenance, and the named failure mode of a contract phase that never happens, leaving permanent duplication. Only pays off if deploys are frequent enough to finish all three.

### Premortem for C. Data-layer isolation with an online schema change tool

Assume `C. Data-layer isolation with an online schema change tool` was selected and the outcome failed. Test this option's stated failure mechanism first: * Real operational complexity, and it binds you to a specific database topology. Nothing here transfers to PostgreSQL or a managed serverless database.

### Premortem for D. Freeze window and big-bang

Assume `D. Freeze window and big-bang` was selected and the outcome failed. Test this option's stated failure mechanism first: * Downtime, a rollback story that is a restore from backup, and a habit that suppresses deploy frequency across the whole venture.

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
`packs/devops-reliability/references/MIGRATION_RISK_CLASSES.md`.

## Safe default

B. The inverse you never ran is not a rollback, it is a hope with a
filename.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Deploy frequency. Three separate deploys are cheap weekly and expensive quarterly.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B. The inverse you never ran is not a rollback, it is a hope with a filename.

**Exit condition:** Stop or roll back the selected branch when * The inverse is written and never run, so it rots. It cannot reverse destructive data change, and it cannot recover a script that failed part way through a multi-statement run (EV-0207). The comfort is larger than the capability, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Deploy frequency. Three separate deploys are cheap weekly and expensive quarterly.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Deploy frequency. Three separate deploys are cheap weekly and expensive quarterly.** and **Whether the change destroys data or only moves it. An inverse can restore a dropped column definition; it cannot restore the values.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
