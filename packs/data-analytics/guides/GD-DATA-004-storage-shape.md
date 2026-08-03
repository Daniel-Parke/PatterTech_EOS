---
summary: Where does the analytics data sit, a single managed warehouse, a warehouse over an open table format, a lakehouse, or files and a single-node engine?
type: guide
tags: [data, infra, arch]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0057]
review: 2027-08
review_by: 2027-08
---

# GD-DATA-004: Where does the analytics data sit?

## The question

The events have to land somewhere and be queried from somewhere. This
decision is usually made by copying whatever the last project did, and
it is the one with the largest gap between the loudest advice and the
common case.

## It depends on

- The working set, meaning how much data a typical query actually
  scans. Not the storage total. These are different quantities and only
  the second is usually quoted (`FRAG-DATA-ANALYTICS-07`).
- Is anything other than SQL going to read these tables, now or within
  the horizon you are planning for?
- Is unstructured data or model training in scope at all?
- How much operations time exists? Catalogue, compaction and snapshot
  expiry are ongoing work (`FRAG-DATA-ANALYTICS-06`).
- How expensive would leaving be, and does that cost actually bind on
  anything you plan to do?

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
without an export (`FRAG-DATA-ANALYTICS-06`). Buys: buying a query
engine and owning your tables become separable decisions. Costs:
catalogue operation, compaction and snapshot expiry become your job, and
implementation parity across languages is a claim to verify per feature
rather than a given.

### C. Lakehouse

One copy of the data in an open direct-access format with a metadata
layer over it giving transactions and schema enforcement, replacing the
two-tier lake-plus-warehouse shape (`FRAG-DATA-ANALYTICS-05`). Buys: the
same facts stop existing twice with an ETL hop between them, which is
where staleness and duplicated cost come from. Costs: it solves a
problem you only have if you already have a lake, and the argument
presumes machine learning and unstructured data are in scope.

### D. Files and a single-node engine

Columnar files on object storage, queried by a single-node engine. Buys:
almost no operational surface and very low cost at small working sets.
Costs: concurrency, governance and anything resembling a service level
are yours to invent.

## Decision rule

- Measure or estimate the working set of a typical query before
  anything else. If it is in megabytes, A or D, and the rest of this
  guide is not your problem yet.
- One team, SQL only, no unstructured data: A.
- More than one engine already reads the same tables, or you can name a
  concrete migration you expect to make: B.
- A lake already exists and the same facts are being copied into a
  warehouse: C, which is the situation the lakehouse argument was
  actually written about.
- Analysis is one person on one machine and nothing serves users: D.

## Default

A. Below a few terabytes the maintenance an open format asks for usually
exceeds the coupling it avoids, and the working set for a young product
is almost always small. Override with a measured working set or a named
second engine, not with an expectation of growth.

## Both sides here are vendor sources

The lakehouse argument is made by the vendor whose product is the
lakehouse, with a synthetic decision-support benchmark answering the
performance objection. The small-working-set account is made by a
single-node warehouse company, from figures the author states are
recalled rather than published. Neither is disqualified and both are
discounted. They are also not really arguing with each other: one
describes an estate that already has a lake, the other describes
everyone else. Decide which population you are in and say so.

## The reversibility question

The open table format is the seam that keeps this decision reversible,
and a seam has a running cost. Buying it before you can name what it
would let you do is paying for optionality you have not priced. Buying
it after you need it is a migration. There is no clever answer: pick a
review trigger, such as the first time a second engine needs the same
table, and revisit then.

Migration mechanics, when this decision does change, sit outside this
pack in
`packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md`.

## Worked rulings

- **PatterTech EOS data-analytics pack (2026-08, argued)**: A as the
  default with the working set as the trigger. Argued from
  `FRAG-DATA-ANALYTICS-07` for the population and
  `FRAG-DATA-ANALYTICS-06` for the cost of the seam.
- **Signup and checkout event model (2026-08, inherited)**: A,
  inherited. Two hundred thousand events, one consumer, SQL only. See
  `packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md`.
