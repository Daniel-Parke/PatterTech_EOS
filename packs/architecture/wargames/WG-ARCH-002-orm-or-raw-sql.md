---
id: WG-ARCH-002
summary: How the service reaches its data, whether an ORM, raw SQL behind a repository, a query builder, or SQL files compiled to typed access, and where the seam sits
kind: wargame
type: wargame
tags: [arch, data, eos, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-ARCH-002, DOC-ARCH-003]
applies_when: [has_cross_language_contract]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0150, EV-0202, EV-0010]
review: 2027-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-ARCH-002: how does a service reach its data, and where is the seam?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. The ruling survives and the grading falls:
nothing in the sweep measures the dialect, so the dialect is a
preference in `packs/architecture/PACK.md`. The seam is what this Wargame
rules on, and one option arrived that v1 lacked.

## Decision question and stakes

How a service talks to its database decides where performance work
happens, what a migration looks like, and whether a query can be read
at all. It is taken once, early, and reversed at great cost. The v1
framing missed half of it: the dialect and the seam are separate
decisions, and only one of the two has an argument behind it.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-002` (binding): Generated contract artefacts are produced deterministically from a committed source and CI fails when they drift.
- `DOC-ARCH-003` (binding): A typed client verifies that a response succeeded before treating the response body as data.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether the service owns its schema or borrows one.
- Whether any of the data is hot: time-series, bulk writes, large
  scans, anything where the query plan is what matters.
- How much of the surface is administrative CRUD over a modest schema.
- Whether filters are composed at request time, or every query is known
  when the code is written.
- Which language you are in, since builder and generator support is
  spread unevenly across stacks.

Applicability is `has_cross_language_contract`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. ORM as the model layer

**What it is.** Mapped classes are the domain objects. The session,
the identity map and lazy loading travel wherever those objects travel.

**Buys.** CRUD written quickly, change tracking for free, and a
migration generated from a diff of the models.

**Costs.** The query is produced where nobody reads it, so the N+1
arrives at load, not at review, and the escape to raw SQL opens
mid-incident. Mapped objects leak past the seam. The migration buy is
undercut, since risk is checkable whoever wrote the file (EV-0202).

### B. Raw SQL behind a repository layer

**What it is.** Statements written by hand, all in one module, typed
rows outward. Nothing above the repository knows SQL exists.

**Buys.** Every query can be read, explained and batched, and the seam
is the one EV-0150 argues for, bought for testability not portability.

**Costs.** Mapping written by hand, nothing checks a statement against
the schema until it runs, and the repository can drift into a
pass-through that hides nothing.

### C. Query builder as the only path

**What it is.** Statements composed in the host language against
generated schema types. jOOQ on the JVM, Kysely in TypeScript,
SQLAlchemy Core in Python. No object graph, no lazy load.

**Buys.** Composition where filters are unknown until the request
arrives, and a rename that fails to compile rather than in production.

**Costs.** A statement assembled across six call sites has no single
form you can read or paste into a query plan, and what you review is
builder code rather than the SQL that runs.

### D. SQL files compiled to typed access

**What it is.** The query lives in a `.sql` file and a generator
compiles it against the real schema into typed functions. sqlc for Go,
PgTyped for TypeScript. jOOQ belongs to C, not here: it is a
query-builder DSL with schema code generation, and the artefact a
reviewer reads is builder code rather than SQL.

**Buys.** The reviewed artefact is the SQL that runs, checked against
the real schema before anything ships. A column renamed under a query
is a build failure rather than a runtime one, which is the class of
drift no option above catches at all.

**Costs.** A database has to be reachable at generate time, so
generation is not offline and does not satisfy B4 of
`packs/architecture/PACK.md` as it stands; a venture taking D owes
either a schema-only generation path or a recorded exception. Dynamic
filters fall back to strings. The generator has to support the
language, and for Python that support is thin, so D loses here on
tooling rather than on merit.

## Failure premises

### Premortem for A. ORM as the model layer

Assume `A. ORM as the model layer` was selected and the outcome failed. Test this option's stated failure mechanism first: The query is produced where nobody reads it, so the N+1 arrives at load, not at review, and the escape to raw SQL opens mid-incident. Mapped objects leak past the seam. The migration buy is undercut, since risk is checkable whoever wrote the file (EV-0202).

### Premortem for B. Raw SQL behind a repository layer

Assume `B. Raw SQL behind a repository layer` was selected and the outcome failed. Test this option's stated failure mechanism first: Mapping written by hand, nothing checks a statement against the schema until it runs, and the repository can drift into a pass-through that hides nothing.

### Premortem for C. Query builder as the only path

Assume `C. Query builder as the only path` was selected and the outcome failed. Test this option's stated failure mechanism first: A statement assembled across six call sites has no single form you can read or paste into a query plan, and what you review is builder code rather than the SQL that runs.

### Premortem for D. SQL files compiled to typed access

Assume `D. SQL files compiled to typed access` was selected and the outcome failed. Test this option's stated failure mechanism first: A database has to be reachable at generate time, so generation is not offline and does not satisfy B4 of `packs/architecture/PACK.md` as it stands; a venture taking D owes either a schema-only generation path or a recorded exception. Dynamic filters fall back to strings. The generator has to support the language, and for Python that support is thin, so D loses here on tooling rather than on merit.

## Decision rule

Any hot data, meaning time-series, bulk writes or large scans: **B**,
because the query you tune has to be the query that runs. A surface of
administrative CRUD with no plan-sensitive path: **A** is defensible,
with raw SQL sanctioned for hot paths from the first week and the
boundary written down. Never mix A and B on the same tables without it.
Filters composed at request time, an admin grid or a faceted search:
**C**, since the honest alternative is string concatenation. A
supported generator, with schema drift as the recurring pain: **D**.

The seam does not move with the dialect. Put data access behind a
repository whichever option wins, and buy it for the reason EV-0150
gives, that the application should be drivable by a test as easily as
by a request. Do not buy it to swap the database; that second device is
not plausible here, and a port bought for one is ceremony.

## Safe default

**B**, with the repository seam regardless of which dialect wins.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether the service owns its schema or borrows one.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** **B**, with the repository seam regardless of which dialect wins.

**Exit condition:** Stop or roll back the selected branch when The query is produced where nobody reads it, so the N+1 arrives at load, not at review, and the escape to raw SQL opens mid-incident. Mapped objects leak past the seam. The migration buy is undercut, since risk is checkable whoever wrote the file (EV-0202), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether the service owns its schema or borrows one.

## Counter-evidence and transfer limits

This fork has no evidence, and pretending otherwise would be worse.
Nothing in the 2026 sweep compares data-access dialects, and none of
the three sources here is about the choice. EV-0150 argues for a seam,
not for what sits behind it, and it is a 2005 pattern statement with no
empirical evaluation. EV-0202 only removes a point from A's ledger. The
v1 claim that agents write better SQL than ORM incantations is
untested, and EV-0010 is the reminder that such intuitions have been
measured wrong once, with the sign inverted. The ruling rests on one
venture's argument and a stack profile that generalised it.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
