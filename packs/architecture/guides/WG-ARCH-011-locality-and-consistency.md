---
id: WG-ARCH-011
summary: Where should data and decisions live when local, cloud, hybrid or offline operation introduces conflicting consistency needs?
kind: wargame
type: wargame
tags: [arch, data, eos, state, wargame]
scenario_modes: [selection, exception, gap]
applicable_doctrines: [DOC-NAT-001, DOC-NAT-002, DOC-NAT-003, DOC-NAT-009]
gap_domain: locality-consistency
applies_when: [has_local_write_store, stores_persistent_data]
engages_when: [requires_offline_or_hybrid_consistency]
consequence: high
relations: [DREL-NAT-001]
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0206, EV-0379, EV-0380, EV-0381, EV-0382, EV-0383, EV-0564]
review: 2027-08
review_cohort: T-0026-pressure-wargames
lifecycle: active
---

# WG-ARCH-011: Where do authority and consistency live?

## Decision question and stakes

Choose where authoritative state lives and what a user may read or write while
local and hosted parts cannot communicate. The answer determines conflict,
data loss, latency, privacy, recovery and whether the interface tells the
truth. Convergence is not the same as preserving a business invariant.

## Doctrines or coverage gap under pressure

- `DOC-NAT-009` starts online-first with a read cache until offline writes are
  named.
- `DOC-NAT-001` requires a conflict policy for each write class before a sync
  library is chosen.
- `DOC-NAT-002` does not accept an invariant-bearing offline write without a
  reservation or compensation path.
- `DOC-NAT-003` requires a durable, ordered, idempotent outbox with a named
  blocked state.
- `DREL-NAT-001` records that the online-first and invariant-protection
  Doctrines reinforce the safe default. This Wargame tests the named offline
  exception rather than inventing a clash between them.
- The uncovered domain is `locality-consistency`.

## Preconditions and engagement triggers

Classify every journey as read, commutative write, overwriting write or
invariant-bearing write. Name authority, conflict owner, permitted staleness,
partition duration, device loss model, encryption and deletion duties,
reconnection behaviour and visible pending or rejected states. Define the
validation oracle for concurrent change.

Applicability is `has_local_write_store` or `stores_persistent_data`. Engage
when `requires_offline_or_hybrid_consistency` is true.

## Options

### A. Hosted authority with local read cache

Cache reads for speed and limited offline use, but require connectivity for
writes. This avoids write conflicts and keeps one authority. It blocks useful
work during outage and may not satisfy field or remote users.

### B. Hosted authority with durable local outbox

Accept selected writes locally, show them as pending, upload in order and let
the server accept, reject or compensate. This provides bounded offline work
without pretending local state is final. A blocked mutation can stall the
queue, so failure and bypass policy are product behaviour (EV-0383).

### C. Mergeable local-first state

Replicate a data type whose operations converge and synchronise peers or a
server later. This can support collaborative or prolonged offline editing.
Convergence does not preserve uniqueness, balances, approvals or other domain
invariants by itself (EV-0379), and storage growth and compaction are material
(EV-0380, EV-0381).

### D. Local authority with explicit export or optional sync

Keep state on the device and treat hosted services as backup or transfer
destinations. This maximises autonomy and can minimise central data holding. It
makes device loss, multi-device divergence, support and migration the owner's
problem.

## Failure premises

### Premortem for A. Hosted authority with local read cache

Assume A failed. The interface looked available but a critical write was
impossible in the field, cached permissions or records became dangerously
stale, or the product had promised offline behaviour it never provided.

### Premortem for B. Hosted authority with durable local outbox

Assume B failed. One rejected item blocked later work, retries duplicated an
effect, or users mistook pending state for accepted state. An invariant-bearing
write was accepted without reservation or compensation.

### Premortem for C. Mergeable local-first state

Assume C failed. Replicas converged on a state the domain forbade, tombstones
and history exhausted storage, or a library's merge semantics did not match the
product's conflict policy.

### Premortem for D. Local authority with explicit export or optional sync

Assume D failed. A lost device meant lost state, exports were untested, or two
devices both appeared authoritative and no human could reconcile them.

## Decision rule

Choose A for offline reads or short partitions when writes can honestly wait.
Choose B for named write classes with durable idempotent upload and explicit
server acceptance, rejection or compensation. Choose C only for data whose
operations are genuinely mergeable and whose business invariants are proved
separately. Choose D when local ownership is a product requirement and backup,
export, migration and device-loss recovery pass.

Invariant-bearing writes do not select C merely because its replicas
converge. If no reservation, compensation or human conflict route exists,
offline acceptance is blocked.

## Safe default

Hosted authority with a local read cache. For a proven offline write need, add
one durable outbox and conflict policy per write class before considering
general mergeable state.

## Cheapest discriminating test

Disconnect during a representative write, make a conflicting change at the
authority, reconnect and process a duplicate acknowledgement. Record visible
pending and rejected states, ordering, data loss, invariant outcome, recovery
effort and behaviour after device restart. For mergeable state, include a
domain-invalid but convergent case.

## Fallback, exit and revisit

**Fallback `read-cache-write-closed`:** retain cached reads, stop new offline
writes, preserve the durable outbox and require connectivity for further
mutation until reconciliation is proved.

**Exit condition:** leave the selected model when it loses an accepted write,
hides pending or rejected state, violates an invariant, cannot recover after
restart, or exceeds its device storage budget.

**Revisit trigger:** repeat for a new write class, longer partition, second
device, changed authority, stronger invariant, changed deletion duty or sync
library lifecycle.

## Counter-evidence and transfer limits

The retained CRDT evidence proves convergence for particular data types, not
application correctness (EV-0379). Library claims about compression and
consistency require local verification (EV-0380, EV-0383). A sync project
deliberately limiting itself to reads is evidence that offline writes are the
hard boundary, not proof that they are never justified (EV-0382). The ruling
does not transfer between write classes with different invariants.
