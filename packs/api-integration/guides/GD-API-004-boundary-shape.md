---
summary: What shape does a boundary take: REST over OpenAPI, typed RPC, an event stream, or GraphQL?
kind: guide
authority: advisory
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0023, EV-0024, EV-0135, EV-0138, EV-0139, EV-0140, EV-0141, EV-0142, EV-0011, EV-0012]
review: on-change-of:EV-0023
type: guide
tags: [arch, state, realtime]
review_by: 2027-06
---

# GD-API-004: what shape does the boundary take?

## The question

Before any of the contract, versioning or signature questions, there is
the shape: request and response over HTTP, a typed procedure call, a
published event, or a query language. The fork is real because each
shape moves the cost somewhere different, and because a shape is
expensive to change once consumers exist. The failure that decides it is
choosing a shape for how the team likes writing code rather than for how
the consumers actually consume.

## It depends on

- Are the consumers known and few, or unknown and many?
- Does the caller need an answer now, or does the producer need to stop
  caring who listens?
- Is the data resource-shaped, or is it a set of actions?
- Does a consumer need to replay history?

## Options

### A. REST over HTTP with an OpenAPI contract

Resources, verbs, status codes, a committed specification (EV-0023).
Buys: every client on earth can call it, caching and proxies work,
tooling is deep, and the specification doubles as a test oracle. Costs:
over-fetching and under-fetching for rich clients; N calls for N
resources; the contract says nothing about ordering across calls.

### B. Typed RPC, usually protobuf and gRPC

Generated stubs on both sides, binary on the wire, tiered compatibility
checking available out of the box (EV-0135). Buys: strong typing across
the seam, low overhead at high call volume, breaking-change detection
that understands the type system. Costs: browsers need a proxy layer,
debugging is not curl-shaped, and it presumes you control both sides
well enough to regenerate stubs together.

### C. Events over a broker

The producer publishes, consumers subscribe, with a CloudEvents envelope
for routing, deduplication and tracing (EV-0138) and a registry
compatibility mode chosen before the first change (EV-0139). Buys:
fan-out, replay, and producer and consumer lifecycles that do not have
to line up. Costs: no answer to the caller, ordering and
exactly-once are your problem, and CloudEvents governs metadata only, so
payload evolution, which is where events actually break, stays yours.

### D. GraphQL

One endpoint, client-selected fields, continuous schema evolution
instead of versioning (EV-0140). Buys: rich clients fetch exactly what
they need in one call, and additions cannot break existing queries. One
controlled experiment found client query implementation faster than
REST, median six minutes against nine (EV-0141). Costs: the experiment
had 22 students, measured first-write time only, and measured precisely
the dimension GraphQL optimises, so it scopes to novice client authors
and no further. Caching, authorisation and query cost all become
bespoke, and production queries exercised only 26.9 and 48.7 percent of
two real schemas, so most of a mature surface is untested (EV-0142).

## Decision rule

- Resource-shaped data, cacheable, unknown or many consumers, ordinary
  CRUD: A.
- Known services, high call volume, strong typing wanted, both sides
  regenerated together: B.
- Fan-out, replay, or decoupled producer and consumer lifecycles: C.
  Choose the compatibility mode first (EV-0139) and treat the payload
  schema as a contract in its own right (EV-0024).
- D only where selection-based delivery solves a demonstrated client
  problem, and then with schema surface monitored against real
  production queries.

Agent-facing boundaries are a fourth shape rather than a variant of
these: MCP carries dated specification revisions and capability
negotiation (EV-0011), and A2A carries a task state machine (EV-0012).
Take the protocol as given and version against its revision, do not
invent a house dialect.

## Default

A for anything a browser or a third party calls. C where a producer must
stop caring who listens. B and D require an argued case.

## Worked rulings

- **WiseWattage and PatterTech_Business (2026, inherited)**: A, with
  the generated contract seam from
  `archive/v1/doctrine/architecture/wargames/WG-ARCH-005-contract-seam.md`.
- **No venture runs B, C or D in production.** The fit conditions above
  are read from the sources rather than from our own operating
  experience, which is the honest status of this guide.
