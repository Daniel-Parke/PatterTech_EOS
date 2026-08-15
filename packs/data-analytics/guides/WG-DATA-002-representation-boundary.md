---
id: WG-DATA-002
summary: When should tabular data cross into an array, optimiser, solver or model representation, and what must the boundary preserve?
kind: wargame
type: wargame
tags: [data, eos, perf, testing, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-DATA-020, DOC-DATA-021, DOC-COD-012]
gap_domain: data-representation-boundary
applies_when: [reads_for_decision, calls_a_model, edits_source]
engages_when: [crosses_dataframe_array_boundary]
consequence: high
relations: []
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0563, EV-0564, EV-0568, EV-0569]
review: 2027-08
lifecycle: active
---

# WG-DATA-002: Where does the representation boundary sit?

## Decision question and stakes

Decide whether data stays in a labelled tabular representation, crosses once
into a dense array or domain object, or moves through a protocol into a solver,
model or device-native representation. The boundary can remove labels, change
dtype or layout, create a copy, transfer ownership, move devices and alter
numerical behaviour. Those are interface properties, not incidental tuning.

## Doctrines or coverage gap under pressure

- `DOC-DATA-020` requires the boundary to be measured on representative data.
- `DOC-DATA-021` keeps the highest-level sufficient representation until a
  lower-level form earns its cost.
- `DOC-COD-012` prefers a simple, visible pipeline before a clever one.
- The uncovered domain is `data-representation-boundary`: existing rules do
  not decide dtype, layout, copy, ownership or device transfer.

## Preconditions and engagement triggers

Name which semantics the source representation carries: labels, index
alignment, missing values, categories, time zones, units or nullable types.
Name the consumer's required dtype, shape, order, device, mutability and
tolerance. Establish who owns the memory after transfer and whether the source
may change while the consumer reads it.

Applicability is any of `reads_for_decision`, `calls_a_model` or
`edits_source`. Engage when `crosses_dataframe_array_boundary` is true.

## Options

### A. Keep the labelled tabular boundary

Perform the operation in the dataframe or table abstraction and expose a
labelled result. This preserves semantics and reviewability, and avoids a
conversion contract. It may prevent use of a solver or kernel that only
accepts arrays, and may leave a proven hotspot untouched.

### B. Convert once to a host array at an explicit adapter

Make one named conversion, assert dtype, shape, order and missing-value policy,
then keep numerical work behind that adapter. This gives array libraries and
solvers a stable interface. Conversion can copy, coerce mixed types, discard
labels and double peak memory (EV-0568).

### C. Exchange through an interoperability protocol

Use an array or dataframe protocol, including a device-aware route where
supported, and assert whether exchange is zero-copy or copied. This can avoid
serialisation and redundant memory, but protocol support does not guarantee
matching layout, ownership, device or numerical meaning (EV-0569).

### D. Materialise a domain-specific transfer artefact

Write a versioned, validated file or message at the boundary and let the
consumer own its representation. This costs serialisation and storage but
creates a reproducible hand-off, isolates runtimes and makes replay possible.

## Failure premises

### Premortem for A. Keep the labelled tabular boundary

Assume A failed. A required solver was wrapped in slow row-wise calls, or a
large numeric kernel stayed opaque because preserving labels was treated as an
absolute goal rather than a tested benefit.

### Premortem for B. Convert once to a host array at an explicit adapter

Assume B failed. The conversion silently widened a dtype, encoded missing
values differently, changed order, or created a second full-size allocation.
The numerical result looked plausible because the oracle checked only shape.

### Premortem for C. Exchange through an interoperability protocol

Assume C failed. A supposedly zero-copy view outlived its owner, a consumer
mutated shared memory, or a device transfer occurred despite the protocol.
The protocol passed while tolerance and ownership were unspecified.

### Premortem for D. Materialise a domain-specific transfer artefact

Assume D failed. The versioned artefact became a second source of truth,
serialisation dominated elapsed time, or producer and consumer evolved the
schema independently without a compatibility test.

## Decision rule

Use A when labels and dataframe semantics are part of correctness and the
measured operation meets its objective. Use B when a host-array consumer is
required and one explicit conversion meets memory and tolerance limits. Use C
only when the protocol is supported at both ends and tests settle device,
layout, ownership, mutation and copy behaviour. Use D when runtime isolation,
replay or independent lifecycle matters more than transfer cost.

Any option loses if it cannot round-trip the representative semantic cases or
if peak memory exceeds the recorded ceiling. A zero-copy claim is rejected
unless the probe demonstrates it for the tested versions and path.

## Safe default

Keep the labelled representation through cleaning and business rules. Cross
once, at a named adapter next to the consumer that requires the lower-level
form, with explicit dtype, shape, missing-value, ownership and tolerance
assertions.

## Cheapest discriminating test

Round-trip a representative slice containing nulls, edge numeric values,
categories and ordering-sensitive rows. Record source and destination dtype,
shape, strides or layout, device, copies, peak memory, boundary time and result
tolerance. Mutate or release the source deliberately to expose unsafe shared
ownership.

## Fallback, exit and revisit

**Fallback `labelled-adapter-boundary`:** materialise a copied host array at
one adapter and retain the labelled source until the consumer returns a
validated result.

**Exit condition:** leave the chosen boundary when semantic round-trip,
ownership, memory or numerical tolerance fails, or when an undocumented copy
appears on the supported path.

**Revisit trigger:** repeat after a dtype, device, protocol, solver, model,
data-volume or ownership change.

## Counter-evidence and transfer limits

Interoperability documentation describes mechanisms, not guaranteed zero-copy
behaviour across every implementation. Instructional dataframe examples do
not set a break-even size. A copy can be the safer choice where lifetime and
mutation are hard to prove. The ruling applies to the tested versions, device
and data shape; it does not authorise removing labels or changing numerical
rules elsewhere in the pipeline.
