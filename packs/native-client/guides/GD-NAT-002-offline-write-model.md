---
summary: What happens to a write made with no network?
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0206]
review: 2027-08
type: guide
tags: [state, data, delivery]
review_by: 2027-08
---

# GD-NAT-002: What happens to a write made with no network?

## The question

The fork is not which sync library to use. It is what the product
promises about a write the user made in a tunnel, and that promise has
to be made per write class before any library is chosen. PACK.md binds
this as B1, B2 and B3; this guide is the argument behind it.

The load-bearing contradiction: convergence proofs prove replicas agree
and no update is lost (FRAG-NATIVE-10), and say nothing about whether
the agreed value satisfies a uniqueness constraint, a balance, an
approval state or the user's intent. Meanwhile the shipped
server-authoritative product states plainly that there is no single
correct choice for handling a write failure (FRAG-NATIVE-14). Both are
right. Together they mean the library never answers the question that
matters.

## It depends on

- **The write class.** Classify first: commutative (notes, sets,
  counters), last-writer-acceptable (preferences, drafts) or
  invariant-bearing (money, bookings, permissions). Detail in
  `packs/native-client/refs/WRITE_CLASSES.md`.
- **Whether offline writing is a named requirement** or an assumption
  nobody wrote down.
- **How long a device is realistically offline.** Minutes on a train is
  a different product from a week in the field.
- **What a wrong merge costs.** A duplicated note is an annoyance, a
  double-booked slot is a refund and an apology.
- **Storage budget on the device**, which decides whether a growing
  document is viable at all.

## Options

### A. Online-required with a read cache
No local writes. Reads come from a cache, writes fail fast with a clear
message. Buys correctness for nothing: conflicts cannot occur, there is
no policy to maintain and no storage growth. Costs the offline
experience entirely.

### B. Server-authoritative sync
A durable local store, fast local reads, and a blocking FIFO upload
queue that holds the client at its last confirmed checkpoint until the
backend acknowledges every pending mutation (FRAG-NATIVE-14). Buys
local speed with no local conflict resolution: the server decides.
Costs head-of-line blocking, where one unacknowledged mutation stalls
the whole client, and costs you writing and testing the write-failure
policy yourself, because the vendor says there is no single correct
one.

### C. Convergent replication
A CRDT store that merges without a round trip (FRAG-NATIVE-11,
FRAG-NATIVE-12). Buys no blocking, no coordination and genuine
multi-device editing. Costs documents that only grow, so compaction and
a storage budget are first-class from day one, and costs the acceptance
of a converged value nobody chose. Convergence is not correctness
(FRAG-NATIVE-10).

### D. Split by write class
Read-path sync plus conventional writes for most classes, with
`reserve-then-commit` for the invariant-bearing ones and `converge`
only where the class is genuinely commutative. Buys most of the offline
benefit for a fraction of the risk, which is the shape a serious
project narrowed itself to when it scoped down to reads and left writes
to the application (FRAG-NATIVE-13). Costs a heterogeneous client with
more than one path to reason about, and a reservation service on the
server.

## Decision rule

Classify every write class first, then pick exactly one policy per
class from `converge`, `last-writer-wins`, `reserve-then-commit` and
`reject-offline`, and record it in a decisions file before any library
is chosen. An invariant-bearing class may never take `converge` or
`last-writer-wins`.

If no offline write is a named requirement, take A. If offline writes
are required and every class is commutative or
last-writer-acceptable, take B or C on the blocking question: choose C
if a stalled client is unacceptable and you can pay for compaction,
choose B if a converged value nobody chose is unacceptable and you can
pay for a named degraded state. If any class is invariant-bearing, take
D. Server contracts change by expand, migrate, contract regardless
(EV-0206), because the old binary is still out there.

## Default

A, online-first with a read cache, until an offline write is a named
requirement. It is the cheapest correct answer and it is reversible,
which none of the others is.

## Worked rulings

- **native-client pack exemplar (2026-08, argued)**: D, with `converge`
  on notes, `last-writer-wins` on preferences and `reserve-then-commit`
  on bookings, plus a compensation event for the loser. See
  `packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md`.
- **Read-only as a deliberate scope (external, inherited)**: narrowing
  to a read-path engine with partial replication (FRAG-NATIVE-13) is
  the strongest available signal that the write path is the expensive
  half. The reason behind that scope change is not documented by the
  maintainers, so the inference is ours and is held loosely.
