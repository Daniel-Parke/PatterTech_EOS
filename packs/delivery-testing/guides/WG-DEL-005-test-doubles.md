---
summary: Which double stands in for this port: real, container, verified fake, or mock?
kind: guide
scope: estate
authority: default
lifecycle: active
basis: standard
evidence_grade: observational
sources: [EV-0184, EV-0185, EV-0186, EV-0187, EV-0093, EV-0091, EV-0193, EV-0090]
review: 2028-02
type: wargame
status: active
tags: [delivery, testing, arch]
---

# WG-DEL-005: Which double stands in for this port?

## The question

Every port to something outside the process forces a choice, and the
choice decides what the test is allowed to notice. Pick the real thing
and the suite gets slow. Pick a hand-rolled double and the suite gets
fast and starts lying the moment the real thing changes. The five
double kinds are not interchangeable: only a fake has behaviour, so
only a fake can be held to a behavioural contract (EV-0184).

## It depends on

- Whether we own the dependency, or merely call it.
- Whether the real thing runs locally, deterministically, in seconds.
- Whether the interesting behaviour is dialect-level (a database
  rejecting a constraint) or shape-level (a JSON field).
- Whether the call itself is the observable behaviour, as with a
  payment captured exactly once.
- Whether anyone will maintain a second implementation.
- The tier: R2 and above want the double's fidelity proven, not assumed.

## Options

### A. The real implementation, in process
What it is: no double at all. The collaborator is constructed and used.
Buys: the highest fidelity available, and nothing to keep in step.
Costs: only viable when the dependency is fast, deterministic and
simply wired (EV-0187). Drags the suite the moment it touches IO.

### B. The real dependency in a throwaway container
What it is: the actual database, broker or storage engine, started per
run and discarded (EV-0093).
Buys: dialect-level truth. Constraint violations, isolation levels and
driver quirks show up in the test rather than in production.
Costs: Docker wherever tests run, seconds instead of milliseconds, and
no faithful emulation of managed cloud services. Bigger tests flake
more often (EV-0196).

### C. A verified fake with one contract suite over both adapters
What it is: a working in-memory implementation of the port, plus a
single suite of cases parameterised over the fake and the real client,
run on a stated cadence (EV-0187, EV-0186).
Buys: unit-suite speed with drift detection. When the real service
changes shape, the shared suite goes red against the fake and the fake
gets fixed.
Costs: a second implementation and a third artefact to maintain, plus a
reachable instance or a recording to verify against. The contract
checks shape and known interactions, so semantic drift inside a stable
shape still gets through (EV-0186).

### D. A narrow stub, or an expectation mock at the boundary
What it is: a canned answer to force a state, or a mock asserting the
call was made (EV-0185).
Buys: precise control of hard-to-reach branches, and sharp failure
localisation. At a trust boundary the call is the behaviour worth
asserting.
Costs: behaviour verification couples the test to how the unit works,
so a refactor that changes nothing observable breaks tests that ought
to pass (EV-0185). Nothing checks the stub still resembles reality.

## Decision rule

- The dependency is pure, in-process and fast: **A**.
- It is a datastore, a broker, or anything with dialect-level
  behaviour we depend on: **B**, with a container per run.
- It is a third-party service we cannot run, or a managed service a
  container cannot emulate: **C**. The contract suite is not optional
  here; a fake without one is forbidden by binding requirement 3.
- The observable behaviour genuinely is the call, for example that a
  payment is captured exactly once, or that an alert was sent: **D**,
  at that boundary only.
- The collaborator is our own internal code: never **D**. Use the real
  object.
- We own both sides and both are deployable: **C** with a
  consumer-driven contract, and the verification result answering the
  deploy question by exit code (EV-0193, EV-0091).
- We call a third party we cannot fix: **C**, with the contract run as
  a monitor rather than a merge gate, because a red gate you cannot act
  on trains people to ignore gates (EV-0186 against EV-0193).

## Default

C for anything external we cannot run, B for infrastructure, A wherever
it is affordable, D confined to trust boundaries. Where the fake and
the real client cannot be exercised by the same suite, the port is
drawn in the wrong place: fix the port rather than fork the suite.

## Worked rulings

- **Venture A (2026, argued)**: sorted every external dependency into
  config-only boundaries and code ports. Config-only boundaries run the
  same real adapter in both worlds against a protocol-faithful local
  server, which is B in local clothes: a local issuer for tokens, MinIO
  for blobs, Postgres for the database, never a hand-rolled fake. Code
  ports, the few places where local and production genuinely differ,
  which are email, error reporting, the clock and id generation, get a
  small interface and swappable implementations, which is C. Recorded
  in that venture's ADR-0003.
- **WiseWattage (2026, inherited)**: the external weather API runs in a
  synthetic mode built as infrastructure rather than as a per-test
  mock, so CI is offline and deterministic. The determinism fix landed
  once, in the adapter, and every test inherited it. Recorded in
  WG-DEL-004.
