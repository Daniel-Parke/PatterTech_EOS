---
summary: ORM, query builder, or raw SQL behind repositories?
type: wargame
tags: [arch, data]
status: active
review_by: 2027-07
---

# WG-ARCH-002: ORM, query builder, or raw SQL behind repositories?

## The question

How the service talks to its database decides where performance work
happens, what migrations look like, and how visible the queries are.
The fork is taken once, early, and reversed only at great cost.

## It depends on

- Whether the service owns its schema or borrows one.
- Performance cliffs in the data shape (hypertables, bulk ingestion,
  large scans) that need hand-shaped SQL anyway.
- How much of the surface is administrative CRUD.

## Options

### A. ORM
Models as classes, queries generated. Fast CRUD, portable-ish,
migrations tooled. Costs opacity exactly where the data is hottest,
and the escape hatch to raw SQL arrives mid-crisis.

### B. Raw SQL behind a repository layer
Hand-written SQL in one place, typed adapters outward, no query
magic. Costs boilerplate; buys queries you can read, explain and
batch, and a repository seam tests can stub.

### C. Query builder
Composable SQL in code. Splits the difference and inherits both sets
of sharp edges; choose it deliberately or not at all.

## Decision rule

The service owns its schema and has any performance-shaped data
(time-series, bulk writes, large reads): B. The surface is dominated
by admin CRUD over a modest schema: A, with raw SQL sanctioned for
the hot paths from day one. Never mix A and B on the same tables
without a written boundary.

## Default

B for estate services; the repository layer is the architecture, the
SQL is honest, and agents write better SQL than ORM incantations.

## Worked rulings

- **WiseWattage (2026, argued)**: B. Its ADR-003 moved persistence to
  batched `executemany` against hypertables after row-by-row inserts
  proved a cliff; the repository layer made the change local. The ORM
  it never had could not have hidden that cost better, only longer.
