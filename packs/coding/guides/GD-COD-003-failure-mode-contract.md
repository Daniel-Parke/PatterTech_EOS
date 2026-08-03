---
summary: How do callers learn a call failed, opaque errors, one sentinel, a declared taxonomy or typed results?
type: guide
tags: [arch, delivery, wargame]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0011, EV-0023, EV-0025, EV-0061, EV-0171, EV-0174, EV-0175]
review: on-change-of:EV-0175
review_by: 2028-02
---

# GD-COD-003: How do callers learn that a call failed?

## The question

A function cannot do what it was asked. What reaches the caller, and
what may the caller rely on next release? This looks like a style
question and is actually a contract question: the moment you let a
caller distinguish two failures, that distinction is part of your public
surface, and removing it is a breaking change (EV-0175).

## It depends on

- Can the caller do anything useful with the difference between two
  failures? If every failure leads to the same recovery, distinguishing
  them buys nothing.
- Does the boundary cross a process, a repository, a venture or a
  release train?
- Is the failure expected in normal operation, such as bad user input,
  or genuinely exceptional?
- Who else already depends on this surface?

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

## Default

C. Most venture code has at least one other caller within a year, and
the cost of a caller writing recovery against a failure that quietly
disappears is higher than the cost of naming the set.

## The versioning half

Version numbers mean nothing until the public surface is declared
precisely, and the failure taxonomy is part of that surface (EV-0171).
The alternative is date-based versioning with per-consumer pinning
(EV-0061, EV-0011), which solves the same coordination problem without
compatibility judgements. Either is acceptable. Neither works if the
taxonomy is undeclared.

## Why this is binding rather than taste

Error handling is where catastrophe lives. In a study of 198 randomly
sampled production failures, 92 per cent of the catastrophic ones came
from incorrect handling of errors the software had already signalled,
and about a third of those were trivial mistakes visible to plain
inspection (EV-0174). Scope note: that corpus was Java-heavy distributed
data systems in 2014. The transferable claim is where to point attention,
not the exact proportion.

## Anti-patterns

- Catching a failure, logging it, and returning as if it succeeded.
- A bare catch-all that swallows everything including the failure you
  have not thought of yet.
- Documenting a failure as inspectable and then returning it wrapped
  differently on one code path, so the caller's check silently stops
  matching (EV-0175).
- Distinguishing failures nobody recovers from differently, which is
  contract surface bought for nothing.

## Worked rulings

- **PatterTech EOS coding pack (2026-08, argued)**: C as the default and
  the declaration itself as binding. Argued from EV-0175 for the
  contract claim and EV-0174 for the severity.
- **Webhook receiver (2026-08, argued)**: C. Signature failure and
  payload failure are separately recoverable by the caller, so both are
  named and both go in the module docstring and the README. See
  `packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md`.
- **Internal formatting helper (2026-08, inherited)**: A, inherited.
  One caller, and every failure means the same thing.
