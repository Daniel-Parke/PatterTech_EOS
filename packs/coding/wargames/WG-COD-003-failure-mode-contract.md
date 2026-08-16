---
id: WG-COD-003
summary: How do callers learn a call failed, opaque errors, one sentinel, a declared taxonomy or typed results?
kind: wargame
type: wargame
tags: [arch, delivery, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-COD-005, DOC-COD-015, DOC-COD-004]
applies_when: [edits_source]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0011, EV-0023, EV-0025, EV-0061, EV-0171, EV-0174, EV-0175]
review: on-change-of:EV-0175
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-COD-003: How do callers learn that a call failed?

## Decision question and stakes

A function cannot do what it was asked. What reaches the caller, and
what may the caller rely on next release? This looks like a style
question and is actually a contract question: the moment you let a
caller distinguish two failures, that distinction is part of your public
surface, and removing it is a breaking change (EV-0175).

## Doctrines or coverage gap under pressure

- `DOC-COD-005` (binding): On a published interface, distinguishable failures are declared and versioned.
- `DOC-COD-015` (default): Declare distinguishable failures on internal interfaces too, where more than one caller exists.
- `DOC-COD-004` (binding): The error path is handled, never discarded.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can the caller do anything useful with the difference between two
  failures? If every failure leads to the same recovery, distinguishing
  them buys nothing.
- Does the boundary cross a process, a repository, a venture or a
  release train?
- Is the failure expected in normal operation, such as bad user input,
  or genuinely exceptional?
- Who else already depends on this surface?

Applicability is `edits_source`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Opaque failure

One error type, message as a string, no structure. Buys: loose coupling
and nothing to version. Costs: callers cannot recover selectively, so
they either give up or parse messages, which is a contract nobody
declared. Legitimate in leaf and throwaway code.

### B. One sentinel per module

A single module-level error type that everything is translated into,
with the cause attached. Buys: callers can tell your failures from
everyone else's, at almost no design cost. Costs: still no selective
recovery within your module.

### C. Declared, versioned failure taxonomy

A named, documented set of distinguishable failures, each carrying its
cause, with the set treated as versioned interface surface: adding one
is a minor change, removing or renaming one is a major change
(EV-0171, EV-0175). Buys: callers can write recovery that keeps working.
Costs: you own the set, and you cannot quietly change your mind.

### D. Typed results at the boundary

Failure is a value in the return type, enumerated in a schema, and the
transport carries it explicitly (EV-0023 for HTTP surfaces, EV-0025 for
the payload shape). Buys: the compiler or the schema check makes
unhandled failure visible, and remote callers see the same taxonomy as
local ones. Costs: heavier, and it fits badly in codebases whose idiom
is exceptions.

## Failure premises

### Premortem for A. Opaque failure

Assume `A. Opaque failure` was selected and the outcome failed. Test this option's stated failure mechanism first: callers cannot recover selectively, so they either give up or parse messages, which is a contract nobody declared. Legitimate in leaf and throwaway code.

### Premortem for B. One sentinel per module

Assume `B. One sentinel per module` was selected and the outcome failed. Test this option's stated failure mechanism first: Costs: still no selective recovery within your module.

### Premortem for C. Declared, versioned failure taxonomy

Assume `C. Declared, versioned failure taxonomy` was selected and the outcome failed. Test this option's stated failure mechanism first: you own the set, and you cannot quietly change your mind.

### Premortem for D. Typed results at the boundary

Assume `D. Typed results at the boundary` was selected and the outcome failed. Test this option's stated failure mechanism first: heavier, and it fits badly in codebases whose idiom is exceptions.

## Decision rule

- Leaf code, one caller, failure means give up: A.
- Internal module, callers only need to know it was you: B.
- Any surface another agent, venture or release train calls, or any
  failure a caller is expected to recover from selectively: C, and
  declare it in the interface documentation.
- The surface crosses a process boundary or is consumed by generated
  clients: D on top of C, with the taxonomy in the schema.
- Whatever you choose, never widen it by accident. Wrapping an error so
  the cause is inspectable is a decision to publish that cause
  (EV-0175). Wrap deliberately, or translate without exposing the cause.

## Safe default

C. Most venture code has at least one other caller within a year, and
the cost of a caller writing recovery against a failure that quietly
disappears is higher than the cost of naming the set.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can the caller do anything useful with the difference between two failures? If every failure leads to the same recovery, distinguishing them buys nothing.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. Most venture code has at least one other caller within a year, and the cost of a caller writing recovery against a failure that quietly disappears is higher than the cost of naming the set.

**Exit condition:** Stop or roll back the selected branch when callers cannot recover selectively, so they either give up or parse messages, which is a contract nobody declared. Legitimate in leaf and throwaway code, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can the caller do anything useful with the difference between two failures? If every failure leads to the same recovery, distinguishing them buys nothing.

## Counter-evidence and transfer limits

### Preserved reasoning: The versioning half

Version numbers mean nothing until the public surface is declared
precisely, and the failure taxonomy is part of that surface (EV-0171).
The alternative is date-based versioning with per-consumer pinning
(EV-0061, EV-0011), which solves the same coordination problem without
compatibility judgements. Either is acceptable. Neither works if the
taxonomy is undeclared.
### Preserved reasoning: Which half of this binds

Since 2026-08-10 the split is by consumer. On a published interface, one
with a consumer the venture does not control, declaring and versioning
the distinguishable failures is binding requirement B4: the caller
cannot see the change coming and cannot undo the recovery code it
already shipped. Inside the venture it is default D9, because the same
declaration on a module with one caller buys rigidity and no
coordination, which the pack lists as an anti-pattern. The reason for
the split is the reach of the mistake, not a change in the evidence.

Handling the error at all is a different matter and binds everywhere,
which is B3 and the paragraph below.
### Preserved reasoning: Why the error path binds rather than being taste

Error handling is where catastrophe lives. In a study of 198 randomly
sampled production failures, 92 per cent of the catastrophic ones came
from incorrect handling of errors the software had already signalled,
and about a third of those were trivial mistakes visible to plain
inspection (EV-0174). Scope note: that corpus was Java-heavy distributed
data systems in 2014. The transferable claim is where to point attention,
not the exact proportion.
### Preserved reasoning: Anti-patterns

- Catching a failure, logging it, and returning as if it succeeded.
- A bare catch-all that swallows everything including the failure you
  have not thought of yet.
- Documenting a failure as inspectable and then returning it wrapped
  differently on one code path, so the caller's check silently stops
  matching (EV-0175).
- Distinguishing failures nobody recovers from differently, which is
  contract surface bought for nothing.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
