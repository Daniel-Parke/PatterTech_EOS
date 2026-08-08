---
summary: How the service reaches its data, whether an ORM, raw SQL behind a repository, a query builder, or SQL files compiled to typed access, and where the seam sits
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0150, EV-0202, EV-0010]
review: 2027-07
type: guide
tags: [arch, data]
review_by: 2027-07
---

# WG-ARCH-002: how does a service reach its data, and where is the seam?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. The ruling survives and the grading falls:
nothing in the sweep measures the dialect, so the dialect is a
preference in `packs/architecture/PACK.md`. The seam is what this guide
rules on, and one option arrived that v1 lacked.

## The question

How a service talks to its database decides where performance work
happens, what a migration looks like, and whether a query can be read
at all. The fork is taken once, early, and reversed at great cost,
because the choice spreads to every call site. The v1 framing missed
half of it: the dialect and the seam are separate decisions, and only
one of the two has an argument behind it.

## It depends on

- Whether the service owns its schema or borrows one.
- Whether any of the data is hot: time-series, bulk writes, large
  scans, anything where the query plan is what matters.
- How much of the surface is administrative CRUD over a modest schema.
- Whether filters are composed at request time, or every query is known
  when the code is written.
- Which language you are in, since builders and generators are spread
  unevenly.

## Options

### A. ORM as the model layer

**What it is.** Mapped classes are the domain objects. The session,
the identity map and lazy loading travel wherever those objects travel.

**Buys.** CRUD written quickly, change tracking for free, and a
migration generated from a diff of the models.

**Costs.** The query is produced where nobody reads it, so the N+1
arrives at load rather than at review, the escape to raw SQL opens
mid-incident, and mapped objects leak past the seam. The migration
argument is weaker than it looks: migration risk is statically
checkable whoever wrote the file (EV-0202).

### B. Raw SQL behind a repository layer

**What it is.** Statements written by hand, all in one module, typed
rows outward. Nothing above the repository knows SQL exists.

**Buys.** Every query can be read, explained and batched, and the seam
is the one EV-0150 argues for, bought for testability rather than for a
swap nobody performs.

**Costs.** Mapping written by hand, and nothing checks a statement
against the schema until it runs. The repository grows a method per
query and drifts towards a pass-through that hides nothing.

### C. Query builder as the only path

**What it is.** Statements composed in the host language against
generated schema types. jOOQ on the JVM, Kysely in TypeScript,
SQLAlchemy Core in Python. No object graph, no lazy load.

**Buys.** Composition where the filters are not known until the request
arrives, and a renamed column that fails to compile rather than in
production.

**Costs.** A statement assembled across six call sites has no single
form you can read or paste into a query plan, and what you review is
builder code rather than the SQL that runs.

### D. SQL files compiled to typed access

**What it is.** The query lives in a `.sql` file and a generator
compiles it against the real schema into typed functions. sqlc for Go,
PgTyped for TypeScript, jOOQ's generator on the JVM. The output is
committed and drift-gated as B4 asks of generated artefacts.

**Buys.** The reviewed artefact is SQL, and the schema drift B cannot
see until runtime fails the build instead.

**Costs.** A database has to be reachable at generate time, dynamic
filters fall back to strings, and the generator has to support your
language. For Python that support is thin, so here D loses on tooling
rather than on merit.

## Decision rule

Any hot data, meaning time-series, bulk writes or large scans: **B**,
because the query you tune has to be the query that runs. A surface of
administrative CRUD over a modest schema with no plan-sensitive path:
**A** is defensible, with raw SQL sanctioned for the hot paths from the
first week and the boundary written down. Never mix A and B on the same
tables without it. Filters composed at request time, an admin grid or a
faceted search: **C**, since the honest alternative is string
concatenation. A supported generator, with schema drift as the
recurring pain: **D**.

The seam does not move with the dialect. Put data access behind a
repository whichever option wins, and buy it for the reason EV-0150
gives, that the application should be drivable by a test as easily as
by a request. Do not buy it to swap the database. That second device is
not plausible here, and a port bought for one is ceremony.

## Default

**B**, with the repository seam regardless of which dialect wins.

## Worked rulings

- **WiseWattage (2026, argued)**: B. Its ADR-003 moved persistence to
  batched `executemany` against hypertables once row-by-row inserts
  proved a cliff, and the repository layer kept the change local. An
  ORM could not have hidden that cost better, only longer.
- **AutoWatt (2026-07, inherited)**: B by taking stack profile 02,
  which rules psycopg 3 behind repositories and no ORM by default
  (`registry/stacks/STACK-fastapi-postgres.md`). No separate argument.
- **Guth (2026, argued)**: not applicable. The venture holds no
  relational store anywhere, so the fork never fires and the row says
  so rather than picking a dialect it will not use.

## Counter-evidence

This fork has no evidence, and pretending otherwise would be worse than
saying so. Nothing in the 2026 sweep compares data-access dialects, and
none of the three sources here is about the choice. EV-0150 argues for
a seam, not for what sits behind it, and it is a 2005 pattern statement
with no empirical evaluation. EV-0202 only removes a point from A's
ledger. The v1 claim that agents write better SQL than ORM incantations
is untested, and EV-0010 is the reminder that intuitions about agent
productivity have been measured wrong once already, with the sign
inverted. The ruling rests on one venture's argument and a stack
profile that generalised it. One decent comparison would move it.
