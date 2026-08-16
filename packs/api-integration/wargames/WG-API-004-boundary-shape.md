---
id: WG-API-004
summary: What shape does a boundary take: REST over OpenAPI, typed RPC, an event stream, or GraphQL?
kind: wargame
type: wargame
tags: [arch, eos, realtime, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-API-013]
applies_when: [exposes_service_boundary]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0023, EV-0024, EV-0135, EV-0138, EV-0139, EV-0140, EV-0141, EV-0142, EV-0011, EV-0012]
review: on-change-of:EV-0023
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-API-004: what shape does the boundary take?

## Decision question and stakes

Before any of the contract, versioning or signature questions, there is
the shape: request and response over HTTP, a typed procedure call, a
published event, or a query language. The fork is real because each
shape moves the cost somewhere different, and because a shape is
expensive to change once consumers exist. The failure that decides it is
choosing a shape for how the team likes writing code rather than for how
the consumers actually consume.

## Doctrines or coverage gap under pressure

- `DOC-API-013` (default): The contract is machine-readable and lives in the repo.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Are the consumers known and few, or unknown and many?
- Does the caller need an answer now, or does the producer need to stop
  caring who listens?
- Is the data resource-shaped, or is it a set of actions?
- Does a consumer need to replay history?

Applicability is `exposes_service_boundary`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. REST over HTTP with an OpenAPI contract

Assume `A. REST over HTTP with an OpenAPI contract` was selected and the outcome failed. Test this option's stated failure mechanism first: over-fetching and under-fetching for rich clients; N calls for N resources; the contract says nothing about ordering across calls.

### Premortem for B. Typed RPC, usually protobuf and gRPC

Assume `B. Typed RPC, usually protobuf and gRPC` was selected and the outcome failed. Test this option's stated failure mechanism first: browsers need a proxy layer, debugging is not curl-shaped, and it presumes you control both sides well enough to regenerate stubs together.

### Premortem for C. Events over a broker

Assume `C. Events over a broker` was selected and the outcome failed. Test this option's stated failure mechanism first: no answer to the caller, ordering and exactly-once are your problem, and CloudEvents governs metadata only, so payload evolution, which is where events actually break, stays yours.

### Premortem for D. GraphQL

Assume `D. GraphQL` was selected and the outcome failed. Test this option's stated failure mechanism first: the experiment had 22 students, measured first-write time only, and measured precisely the dimension GraphQL optimises, so it scopes to novice client authors and no further. Caching, authorisation and query cost all become bespoke, and production queries exercised only 26.9 and 48.7 percent of two real schemas, so most of a mature surface is untested (EV-0142).

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

## Safe default

A for anything a browser or a third party calls. C where a producer must
stop caring who listens. B and D require an argued case.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Are the consumers known and few, or unknown and many?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A for anything a browser or a third party calls. C where a producer must stop caring who listens. B and D require an argued case.

**Exit condition:** Stop or roll back the selected branch when over-fetching and under-fetching for rich clients; N calls for N resources; the contract says nothing about ordering across calls, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Are the consumers known and few, or unknown and many?

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Are the consumers known and few, or unknown and many?** and **Does the caller need an answer now, or does the producer need to stop caring who listens?** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
