---
summary: Write classification, the four conflict policies, the reservation pattern and what the outbox must guarantee
kind: fact
scope: estate
sources: [EV-0206]
volatility: slow
review: 2028-08
type: pattern
tags: [state, data, delivery]
---

# Write classes and conflict policies

Reference for PACK.md B1, B2 and B3, and for GD-NAT-002. Nothing here
is a library recommendation.

## Classify first

| Class | Test | Typical examples |
| --- | --- | --- |
| commutative | two offline edits applied in either order give a result both users would accept | notes, tags, sets, add-only counters, reactions |
| last-writer-acceptable | losing one of two concurrent edits is annoying and not harmful | preferences, drafts, display settings, sort order |
| invariant-bearing | some property must hold across all replicas, and a merged value can break it | bookings, stock, balances, permissions, approvals, anything unique |

The test for the third class is the useful one: name the invariant out
loud. "Exactly one holder per slot." "Balance never negative." "Only an
approver may approve." If you can name it, the class is
invariant-bearing and B2 applies.

## The four policies

Exactly one per write class. The vocabulary is fixed so a schema can
validate it.

| Policy | What the client does offline | What happens on reconnection |
| --- | --- | --- |
| `converge` | accepts the write locally | replicas merge, no round trip, converged value is final |
| `last-writer-wins` | accepts the write locally | the later timestamp survives, the other is discarded and the user is told |
| `reserve-then-commit` | accepts only against a reservation held before going offline | the reservation is redeemed, or it has expired and a compensation event fires |
| `reject-offline` | refuses the write with a message naming why | nothing to reconcile |

`converge` and `last-writer-wins` are forbidden on an invariant-bearing
class. Convergence is a claim about replicas agreeing, not about the
agreed value satisfying a constraint (EV-0379).

## The reservation pattern

For `reserve-then-commit`:

1. While online, the client asks the server to hold the resource and
   receives a reservation with an identity and an expiry.
2. Offline, the client accepts the write only if it holds an unexpired
   reservation for that resource. Otherwise it degrades to
   `reject-offline` and says so.
3. On reconnection the client redeems the reservation. The server is
   the only authority on whether it is still valid.
4. If redemption fails, a named compensation event fires: the user is
   told, the local state is reverted, and the event is recorded so
   support can see it happened.

The loser of a contested resource must produce a compensation event,
not a silent revert. A booking that disappears without explanation is a
support ticket and a refund.

## What the outbox must guarantee

B3 in three properties.

- **Durable.** A write acknowledged in the interface survives process
  death. Acknowledge after the local commit, never before.
- **Ordered.** Mutations leave in the order they were made, so causal
  dependencies hold.
- **Idempotent.** Every mutation carries a client-generated identity
  that the server deduplicates on. Replay after a crash, a retry or a
  duplicate delivery produces one effect.

The blocked state is the fourth property, and it is the one teams
forget. A server-authoritative queue holds the client at its last
confirmed checkpoint until every pending mutation is acknowledged
(EV-0383), so one stuck mutation stalls the whole client. The
requirement is that this state is named in the interface within a
stated timeout, that reads keep working while it holds, and that there
is a documented way out of it.

## Storage growth

Where `converge` is used, the store grows. The maintainers say
text-suitable CRDTs only grow and answer with conditional tombstone
collection (EV-0381), and the conditions were not enumerated at
inspection, so no growth bound can be stated from that source. Budget
device storage, measure document size on realistic data, and decide the
compaction trigger before shipping, not after.

## Contract change across versions

Old binaries live for years, so client and server contracts change by
expand, migrate, contract (EV-0206): ship the new shape alongside the
old, wait out the installed base, then remove the old. The wait is
measured from telemetry on live versions, not from the release date.
