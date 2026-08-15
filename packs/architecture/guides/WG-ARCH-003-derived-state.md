---
id: WG-ARCH-003
summary: Where a derived value is allowed to rest, whether computed on read, cached with a named owner, frozen as an immutable snapshot, or maintained by the write path
kind: wargame
type: wargame
tags: [arch, data, eos, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-ARCH-008]
applies_when: [has_server_code]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0157, EV-0163, EV-0276]
review: 2027-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-ARCH-003: computed on read, owned cache, immutable snapshot, or maintained by the writer?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. The v1 rule bound as one writer per fact and
is now D5 of `packs/architecture/PACK.md`, a default, because nothing
outside this estate measures it. It also gained a fourth option, the
value a write path maintains and readers take on trust.

## Decision question and stakes

Scores, grades, statuses, rollups, current-anything. A derived value
wants to be stored the moment it gets expensive, and a stored
derivation parts company with its source without saying so. The fork
is where it rests, and who is answerable for it being right.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-008` (default): Derived values are computed, not stored.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether the number was quoted to a customer, signed or attested. A
  point-in-time fact is not a cache.
- Recompute cost against read rate, and whether recompute is bounded.
- Whether an invalidation owner can be named.
- Whether every write path touching an input is enumerable.
- Whether the derivation can be reproduced later: versions, rounding,
  and any external answer that fed it.
- Whether staleness is visible to the reader or silent.

Applicability is `has_server_code`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Computed on read

**What it is.** Derive from the source of record every time.

**Buys.** Never stale, never audited wrongly, nothing to invalidate,
and one place where the rule lives.

**Costs.** Compute and latency on the user's path at every read, and a
long derivation reads its inputs over a moving window, so two panels
can disagree unless the read is taken at one transaction.

### B. Cache-aside with a named owner

**What it is.** Computed as in A, then memoised in a store the readers
share, with an invalidation owner written down and a TTL as backstop.
Dropping the cache loses nothing but time.

**Buys.** The hot path, at a staleness the owner chose and bounded.

**Costs.** An invalidation discipline that has to stay true as inputs
multiply. The failure is silent: a missed invalidation serves a wrong
number that looks right, and nothing goes red.

### C. Immutable snapshot

**What it is.** The derivation captured once as a historical fact,
carrying its input digest, code and profile versions, and any external
answer that fed it. Never updated; corrections are new snapshots.

**Buys.** A number that can be defended, re-derived and audited later.
EV-0276 is why the external answers go in the row: a replay that
re-reads them at today's values reconstructs a different past.

**Costs.** Snapshots accumulate, and a reader wanting the current
value takes the latest and treats it as live. Erasure duties sit badly
against an immutable row, so one holding personal data needs its
retention plan before it lands.

### D. Maintained by the write path

**What it is.** The stored value is written eagerly, in the same
transaction as the change that moves it, or projected into a read
model by a relay. Freshness is the writer's job. Where the value lands
in another store, the change and its message go into one transaction
as an outbox and the projection is idempotent (EV-0157).

**Buys.** Cheap reads with no recompute and no miss, and the only
shape that works when the derivation is too heavy for any read path.

**Costs.** Every writer must remember, and a new write path that skips
the update makes the value wrong with no read that would notice. It is
only honest with a reconciliation job comparing stored against freshly
derived on a schedule. Relayed projection is at-least-once, so the
arithmetic has to survive being applied twice. Name the pattern in use
(EV-0163); the four hiding behind event-driven carry different costs.

## Failure premises

### Premortem for A. Computed on read

Assume `A. Computed on read` was selected and the outcome failed. Test this option's stated failure mechanism first: Compute and latency on the user's path at every read, and a long derivation reads its inputs over a moving window, so two panels can disagree unless the read is taken at one transaction.

### Premortem for B. Cache-aside with a named owner

Assume `B. Cache-aside with a named owner` was selected and the outcome failed. Test this option's stated failure mechanism first: An invalidation discipline that has to stay true as inputs multiply. The failure is silent: a missed invalidation serves a wrong number that looks right, and nothing goes red.

### Premortem for C. Immutable snapshot

Assume `C. Immutable snapshot` was selected and the outcome failed. Test this option's stated failure mechanism first: Snapshots accumulate, and a reader wanting the current value takes the latest and treats it as live. Erasure duties sit badly against an immutable row, so one holding personal data needs its retention plan before it lands.

### Premortem for D. Maintained by the write path

Assume `D. Maintained by the write path` was selected and the outcome failed. Test this option's stated failure mechanism first: Every writer must remember, and a new write path that skips the update makes the value wrong with no read that would notice. It is only honest with a reconciliation job comparing stored against freshly derived on a schedule. Relayed projection is at-least-once, so the arithmetic has to survive being applied twice. Name the pattern in use (EV-0163); the four hiding behind event-driven carry different costs.

## Decision rule

A number quoted to a customer, signed or attested: **C**, with digest
and versions recorded so it can be re-derived, and corrections issued
as new snapshots. Hot path, a nameable invalidation owner, staleness
the owner can bound: **B**. A derivation too heavy for any read path,
writers enumerable, reconciliation in place: **D**, and reconciliation
is the price of entry, not a later improvement. Otherwise **A**;
latency is cheaper than drift. Never store a derived value that is
none of the three: it has no owner, no expiry and no check.

## Safe default

**A**, computed, with **C** wherever a number left the building.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether the number was quoted to a customer, signed or attested. A point-in-time fact is not a cache.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** **A**, computed, with **C** wherever a number left the building.

**Exit condition:** Stop or roll back the selected branch when Compute and latency on the user's path at every read, and a long derivation reads its inputs over a moving window, so two panels can disagree unless the read is taken at one transaction, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether the number was quoted to a customer, signed or attested. A point-in-time fact is not a cache.

## Counter-evidence and transfer limits

This fork is thin on evidence and the grading says so. Nothing in the
ledger measures drift, and none of it observed a venture this size.
EV-0157 is a pattern page with no measurement, and its stated weakness
is exactly D's: it depends on developers remembering to write to the
outbox, and offers no way to enforce that. EV-0163 is a caution about
vocabulary rather than support for D. EV-0276 is a 2005 description
with no operational data and no guidance on snapshot cadence, and it
predates erasure obligations against an immutable log. D5 rests on
local observation across two ventures and on the argument that a
stored derivation has no failing check, not on anything measured.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
