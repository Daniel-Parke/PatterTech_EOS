---
id: WG-DATA-007
summary: Where does the analytics data sit, a single managed warehouse, a warehouse over an open table format, a lakehouse, or files and a single-node engine?
kind: wargame
type: wargame
tags: [arch, data, eos, infra, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DATA-008]
applies_when: [publishes_analytics_table]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0057, EV-0309, EV-0310, EV-0311]
review: 2028-01
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DATA-007: Where does the analytics data sit?

## Decision question and stakes

The events have to land somewhere and be queried from somewhere. This
decision is usually made by copying whatever the last project did, and
it is the one with the largest gap between the loudest advice and the
common case.

## Doctrines or coverage gap under pressure

- `DOC-DATA-008` (default): One managed warehouse until the working set argues otherwise.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- The working set, meaning how much data a typical query actually scans.
  Not the storage total. These are different quantities and only the
  second is usually quoted (EV-0311).
- Is anything other than SQL going to read these tables, now or within
  the horizon you are planning for?
- Is unstructured data or model training in scope at all?
- How much operations time exists? Catalogue, compaction and snapshot
  expiry are ongoing work (EV-0310).
- How expensive would leaving be, and does that cost actually bind on
  anything you plan to do?

Applicability is `publishes_analytics_table`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. One managed warehouse

Everything lands in a single managed columnar warehouse and everything
queries it. Buys: no storage layer to operate, and the vendor absorbs
compaction, metadata and tuning. Costs: your tables live in the vendor's
format, so leaving means an export.

### B. Managed engine over an open table format

Query engine and table format are separated: the table metadata,
snapshots, schema evolution and partition evolution live with the files
in an open format, so more than one engine can read the same table
without an export (EV-0310). Buys: buying a query engine and owning your
tables become separable decisions. Costs: catalogue operation,
compaction and snapshot expiry become your job, and implementation
parity across languages is a claim to verify per feature rather than a
given.

### C. Lakehouse

One copy of the data in an open direct-access format with a metadata
layer over it giving transactions and schema enforcement, replacing the
two-tier lake-plus-warehouse shape (EV-0309). Buys: the same facts stop
existing twice with an ETL hop between them, which is where staleness
and duplicated cost come from. Costs: it solves a problem you only have
if you already have a lake, and the argument presumes machine learning
and unstructured data are in scope.

### D. Files and a single-node engine

Columnar files on object storage, queried by a single-node engine. Buys:
almost no operational surface and very low cost at small working sets.
Costs: concurrency, governance and anything resembling a service level
are yours to invent.

## Failure premises

### Premortem for A. One managed warehouse

Assume `A. One managed warehouse` was selected and the outcome failed. Test this option's stated failure mechanism first: your tables live in the vendor's format, so leaving means an export.

### Premortem for B. Managed engine over an open table format

Assume `B. Managed engine over an open table format` was selected and the outcome failed. Test this option's stated failure mechanism first: catalogue operation, compaction and snapshot expiry become your job, and implementation parity across languages is a claim to verify per feature rather than a given.

### Premortem for C. Lakehouse

Assume `C. Lakehouse` was selected and the outcome failed. Test this option's stated failure mechanism first: come from. Costs: it solves a problem you only have if you already have a lake, and the argument presumes machine learning and unstructured data are in scope.

### Premortem for D. Files and a single-node engine

Assume `D. Files and a single-node engine` was selected and the outcome failed. Test this option's stated failure mechanism first: concurrency, governance and anything resembling a service level are yours to invent.

## Decision rule

- Measure or estimate the working set of a typical query before anything
  else. If it is in megabytes, A or D, and the rest of this Wargame is not
  your problem yet.
- One team, SQL only, no unstructured data: A.
- More than one engine already reads the same tables, or you can name a
  concrete migration you expect to make: B.
- A lake already exists and the same facts are being copied into a
  warehouse: C, which is the situation the lakehouse argument was
  actually written about.
- Analysis is one person on one machine and nothing serves users: D.

## Safe default

A. Below a few terabytes the maintenance an open format asks for usually
exceeds the coupling it avoids, and the working set for a young product
is almost always small. Override with a measured working set or a named
second engine, not with an expectation of growth.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **The working set, meaning how much data a typical query actually scans. Not the storage total. These are different quantities and only the second is usually quoted (EV-0311).** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. Below a few terabytes the maintenance an open format asks for usually exceeds the coupling it avoids, and the working set for a young product is almost always small. Override with a measured working set or a named second engine, not with an expectation of growth.

**Exit condition:** Stop or roll back the selected branch when your tables live in the vendor's format, so leaving means an export, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: The working set, meaning how much data a typical query actually scans. Not the storage total. These are different quantities and only the second is usually quoted (EV-0311).

## Counter-evidence and transfer limits

### Preserved reasoning: Both sides here are vendor sources

The lakehouse argument is made by the vendor whose product is the
lakehouse, with a synthetic decision-support benchmark answering the
performance objection. The small-working-set account is made by a
single-node warehouse company, from figures the author states are
recalled rather than published. Neither is disqualified and both are
discounted. They are also not really arguing with each other: one
describes an estate that already has a lake, the other describes
everyone else. Decide which population you are in and say so.
### Preserved reasoning: The reversibility question

The open table format is the seam that keeps this decision reversible,
and a seam has a running cost. Buying it before you can name what it
would let you do is paying for optionality you have not priced. Buying
it after you need it is a migration. There is no clever answer: pick a
review trigger, such as the first time a second engine needs the same
table, and revisit then.

Migration mechanics, when this decision does change, sit outside this
pack in
`packs/devops-reliability/wargames/WG-DEVOPS-001-schema-change-strategy.md`.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
