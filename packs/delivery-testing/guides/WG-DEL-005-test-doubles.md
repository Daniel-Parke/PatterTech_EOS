---
id: WG-DEL-005
summary: Which double stands in for this port: real, container, verified fake, or mock?
kind: wargame
type: wargame
tags: [arch, delivery, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DEL-002, DOC-DEL-006, DOC-COD-001]
applies_when: [ships_code]
engages_when: [test_fidelity_changes_outcome]
consequence: high
relations: [DREL-DEL-002]
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0184, EV-0185, EV-0186, EV-0187, EV-0093, EV-0091, EV-0193, EV-0090]
review: 2028-02
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DEL-005: Which double stands in for this port?

## Decision question and stakes

Every port to something outside the process forces a choice, and the
choice decides what the test is allowed to notice. Pick the real thing
and the suite gets slow. Pick a hand-rolled double and the suite gets
fast and starts lying the moment the real thing changes. The five
double kinds are not interchangeable: only a fake has behaviour, so
only a fake can be held to a behavioural contract (EV-0184).

## Doctrines or coverage gap under pressure

- `DOC-DEL-002` (binding): Every double standing in for a dependency outside the venture's control has a contract suite that runs the same cases against the double and the real implementation, on a stated cadence.
- `DOC-DEL-006` (default): Double preference order.
- `DOC-COD-001` (binding): The oracle that judges a change is authored independently of the implementation under test.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether we own the dependency, or merely call it.
- Whether the real thing runs locally, deterministically, in seconds.
- Whether the interesting behaviour is dialect-level (a database
  rejecting a constraint) or shape-level (a JSON field).
- Whether the call itself is the observable behaviour, as with a
  payment captured exactly once.
- Whether anyone will maintain a second implementation.
- The tier: R2 and above want the double's fidelity proven, not assumed.

Applicability is `ships_code`. Engagement is `test_fidelity_changes_outcome`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. The real implementation, in process

Assume `A. The real implementation, in process` was selected and the outcome failed. Test this option's stated failure mechanism first: only viable when the dependency is fast, deterministic and simply wired (EV-0187). Drags the suite the moment it touches IO.

### Premortem for B. The real dependency in a throwaway container

Assume `B. The real dependency in a throwaway container` was selected and the outcome failed. Test this option's stated failure mechanism first: Docker wherever tests run, seconds instead of milliseconds, and no faithful emulation of managed cloud services. Bigger tests flake more often (EV-0196).

### Premortem for C. A verified fake with one contract suite over both adapters

Assume `C. A verified fake with one contract suite over both adapters` was selected and the outcome failed. Test this option's stated failure mechanism first: a second implementation and a third artefact to maintain, plus a reachable instance or a recording to verify against. The contract checks shape and known interactions, so semantic drift inside a stable shape still gets through (EV-0186).

### Premortem for D. A narrow stub, or an expectation mock at the boundary

Assume `D. A narrow stub, or an expectation mock at the boundary` was selected and the outcome failed. Test this option's stated failure mechanism first: behaviour verification couples the test to how the unit works, so a refactor that changes nothing observable breaks tests that ought to pass (EV-0185). Nothing checks the stub still resembles reality.

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

## Safe default

C for anything external we cannot run, B for infrastructure, A wherever
it is affordable, D confined to trust boundaries. Where the fake and
the real client cannot be exercised by the same suite, the port is
drawn in the wrong place: fix the port rather than fork the suite.

## Cheapest discriminating test

Run the same contract against the proposed double and the nearest available real boundary. Seed one representative mismatch and require the independent oracle to catch it.

## Fallback, exit and revisit

**Fallback `safe-default`:** C for anything external we cannot run, B for infrastructure, A wherever it is affordable, D confined to trust boundaries. Where the fake and the real client cannot be exercised by the same suite, the port is drawn in the wrong place: fix the port rather than fork the suite.

**Exit condition:** Stop or roll back the selected branch when only viable when the dependency is fast, deterministic and simply wired (EV-0187). Drags the suite the moment it touches IO, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether we own the dependency, or merely call it.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Whether we own the dependency, or merely call it.** and **Whether the real thing runs locally, deterministically, in seconds.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
