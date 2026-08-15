---
id: GD-NAT-002
summary: What happens to a write made with no network?
kind: wargame
type: wargame
tags: [data, delivery, eos, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-NAT-001, DOC-NAT-002, DOC-NAT-003]
applies_when: [has_local_write_store]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0206, EV-0379, EV-0380, EV-0381, EV-0382, EV-0383]
review: 2028-05
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-NAT-002: What happens to a write made with no network?

## Decision question and stakes

The fork is not which sync library to use. It is what the product
promises about a write the user made in a tunnel, and that promise has
to be made per write class before any library is chosen. PACK.md
carries this as B1, B2 and B3, defaults since the ADR-0008 audit
because the remedies are rulings of ours rather than published rules.
This guide is the argument behind them.

The load-bearing contradiction: convergence proofs prove replicas agree
and no update is lost (EV-0379), and say nothing about whether
the agreed value satisfies a uniqueness constraint, a balance, an
approval state or the user's intent. Meanwhile the shipped
server-authoritative product states plainly that there is no single
correct choice for handling a write failure (EV-0383). Both are
right. Together they mean the library never answers the question that
matters.

## Doctrines or coverage gap under pressure

- `DOC-NAT-001` (default): A conflict policy per write class, named before a sync library is chosen.
- `DOC-NAT-002` (default): No offline acceptance of an invariant-bearing write without a reservation or compensation path.
- `DOC-NAT-003` (default): The outbox is durable, ordered and idempotent, and its blocked state is named.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `has_local_write_store`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Online-required with a read cache
No local writes. Reads come from a cache, writes fail fast with a clear
message. Buys correctness for nothing: conflicts cannot occur, there is
no policy to maintain and no storage growth. Costs the offline
experience entirely.

### B. Server-authoritative sync
A durable local store, fast local reads, and a blocking FIFO upload
queue that holds the client at its last confirmed checkpoint until the
backend acknowledges every pending mutation (EV-0383). Buys
local speed with no local conflict resolution: the server decides.
Costs head-of-line blocking, where one unacknowledged mutation stalls
the whole client, and costs you writing and testing the write-failure
policy yourself, because the vendor says there is no single correct
one.

### C. Convergent replication
A CRDT store that merges without a round trip (EV-0380,
EV-0381). Buys no blocking, no coordination and genuine
multi-device editing. Costs documents that only grow, so compaction and
a storage budget are first-class from day one, and costs the acceptance
of a converged value nobody chose. Convergence is not correctness
(EV-0379).

### D. Split by write class
Read-path sync plus conventional writes for most classes, with
`reserve-then-commit` for the invariant-bearing ones and `converge`
only where the class is genuinely commutative. Buys most of the offline
benefit for a fraction of the risk, which is the shape a serious
project narrowed itself to when it scoped down to reads and left writes
to the application (EV-0382). Costs a heterogeneous client with
more than one path to reason about, and a reservation service on the
server.

## Failure premises

### Premortem for A. Online-required with a read cache

Assume `A. Online-required with a read cache` was selected and the outcome failed. Test this option's stated failure mechanism first: the offline experience entirely.

### Premortem for B. Server-authoritative sync

Assume `B. Server-authoritative sync` was selected and the outcome failed. Test this option's stated failure mechanism first: head-of-line blocking, where one unacknowledged mutation stalls the whole client, and costs you writing and testing the write-failure policy yourself, because the vendor says there is no single correct one.

### Premortem for C. Convergent replication

Assume `C. Convergent replication` was selected and the outcome failed. Test this option's stated failure mechanism first: documents that only grow, so compaction and a storage budget are first-class from day one, and costs the acceptance of a converged value nobody chose. Convergence is not correctness (EV-0379).

### Premortem for D. Split by write class

Assume `D. Split by write class` was selected and the outcome failed. Test this option's stated failure mechanism first: a heterogeneous client with more than one path to reason about, and a reservation service on the server.

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

## Safe default

A, online-first with a read cache, until an offline write is a named
requirement. It is the cheapest correct answer and it is reversible,
which none of the others is.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****The write class.** Classify first: commutative (notes, sets, counters), last-writer-acceptable (preferences, drafts) or invariant-bearing (money, bookings, permissions). Detail in `packs/native-client/refs/WRITE_CLASSES.md`.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, online-first with a read cache, until an offline write is a named requirement. It is the cheapest correct answer and it is reversible, which none of the others is.

**Exit condition:** Stop or roll back the selected branch when the offline experience entirely, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **The write class.** Classify first: commutative (notes, sets, counters), last-writer-acceptable (preferences, drafts) or invariant-bearing (money, bookings, permissions). Detail in `packs/native-client/refs/WRITE_CLASSES.md`.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****The write class.** Classify first: commutative (notes, sets, counters), last-writer-acceptable (preferences, drafts) or invariant-bearing (money, bookings, permissions). Detail in `packs/native-client/refs/WRITE_CLASSES.md`.** and ****Whether offline writing is a named requirement** or an assumption nobody wrote down.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
