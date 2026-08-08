---
summary: Where background work runs, whether in the request process, on a durable database claim queue, on an external broker, or on a scheduled pass over state
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0151, EV-0152, EV-0157, EV-0162, EV-0163]
review: 2027-07
type: guide
tags: [arch, state, infra]
review_by: 2027-07
---

# WG-ARCH-004: background work in-process, on a durable queue, on a broker, or on a schedule?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. Two things moved. The default is now the
durable queue outright, D6 of `packs/architecture/PACK.md`, where v1
started in-process and promoted later. And a fourth option arrived
that v1 did not have: work that needs no queue at all.

## The question

The first background job arrives innocently. Send an email, refresh a
forecast. The substrate it lands on is load-bearing within a week:
deploys orphan it, retries duplicate it, and the backlog forms where
nobody looks. The fork is the substrate, and taking it early is when
EV-0152 warns the process decomposition gets welded to the logical one.

## It depends on

- Whether the work must survive a deploy, and whether anyone finds out
  when it does not.
- Whether the work is derivable from rows that already exist, or is an
  instruction with no other trace.
- Whether a unit can run twice safely. If not, none of these is safe,
  because they all retry.
- Whether workers need to fail or scale apart from the request path,
  on a DORA signal rather than a hunch (EV-0151).
- Whether anything outside this venture consumes the work.

## Options

### A. In-process executor

**What it is.** A task or thread pool inside the service. The work
runs in the process that accepted the request.

**Buys.** No infrastructure, no serialisation, no second failure
domain. The unit stays an ordinary function call and stays debuggable.

**Costs.** Work dies with the process and nobody is told, so a routine
deploy is a silent loss. The backlog lives in memory, where no tool
can see it and no operator can drain it.

### B. Durable database claim queue

**What it is.** A jobs table claimed with `FOR UPDATE SKIP LOCKED`,
idempotency keys, stale-claim reaping, and a unit-builder registry,
because closures do not serialise: persist context, rebuild the work.

**Buys.** Exactly the database's guarantees and no more, one store to
back up, work that survives a deploy, and a backlog queryable in SQL.

**Costs.** The queue competes with the application for connections,
locks and vacuum, and long claims bloat the table. It is a shared
store in EV-0162's sense: workers and API hold the same credentials
until someone splits them.

### C. External broker

**What it is.** Redis, SQS or kin, with a worker fleet deployed and
scaled on its own.

**Buys.** Fan-out to consumers outside this venture, rate shaping, and
throughput past what one database will carry. Independent
deployability at the worker, which is what DORA measures (EV-0151).

**Costs.** A second stateful system with its own failure modes. The
message and the state change can disagree, so anything doing both
needs an outbox regardless (EV-0157). And event-driven names four
patterns with four prices, so nothing is decided until one is named
(EV-0163).

### D. Scheduled pass over state

**What it is.** No queue. A periodic pass selects the rows that need
work, does it, and marks them done. The state is the backlog.

**Buys.** Nothing to lose on a deploy, because nothing was enqueued.
Idempotent by construction: a missed run is caught by the next one,
and recovery is running it again.

**Costs.** A latency floor equal to the tick, a scan that grows with
the table, and overlapping runs when a pass outlives its interval. The
work must be a function of state, so a one-off send does not fit.

## Decision rule

Work derivable from rows that already exist, where a minute of delay
costs nothing: **D**, and no queue at all. Work that exists only as an
instruction and must not vanish, with one database already serving the
system: **B**, which is D6 of the pack. Work that may vanish with
nobody harmed and nobody misled: **A** is honest, but put it behind
B's interface so promotion is a deploy and not a rewrite. A consumer
outside the venture, rate shaping, or throughput past the database's
comfort: **C**, on a measured signal (EV-0151), and name which of
EV-0163's four patterns is meant before building. Where a state change
must also produce a message, write it in the same transaction and make
consumers idempotent (EV-0157), whichever substrate carries it.

## Default

**B**, with idempotency keys and rebuildable units from the first job,
whether or not they are needed yet.

## Worked rulings

- **WiseWattage (2026, argued)**: B behind the `WW_DURABLE_JOBS` flag
  (its ADR-006), in-process the default path, after deploys orphaned
  forecast jobs. The unit-builder registry exists because a fresh
  worker could not pick up a closure.
- **Venture A (2026-07, inherited)**: the v1 default taken at seed,
  in-process with B's seam designed in. Its pin predates the pack
  system, so it carries the v1 rule with no separate argument.

## Counter-evidence

Thinner than the rest of the pack, and worth saying plainly. Nothing
in the ledger measures job substrates. EV-0157, EV-0162 and EV-0163
are single-author pattern catalogues written for multi-team estates
with no measurement, and none is about background work in one small
service. The claim mechanics in B have no ledger row at all: they rest
on one venture and on database documentation nobody has graded. D6
makes B the default while `registry/stacks/STACK-fastapi-postgres.md`
still records the v1 rule, in-process with B behind a flag, and that
profile has not been re-graded. No venture has argued C, so its costs
here are reasoned, not lived.
