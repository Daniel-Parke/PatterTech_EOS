---
summary: Which oracle each change type needs, what counts as one, and the commit order that proves it came first
type: foundation
tags: [testing, delivery]
kind: fact
scope: estate
sources: [EV-0003, EV-0004, EV-0005, EV-0006, EV-0007, EV-0094, EV-0178, EV-0180]
volatility: slow
review: 2027-05
---

# Oracle reference

Level 3 material behind binding requirement B1 and guide
`packs/coding/guides/GD-COD-001-oracle-strategy.md`.

## Definition

An oracle is an executable statement of intent that fails when the
behaviour is wrong and passes when it is right, and that was not derived
from the implementation it judges. The second half is the part that gets
skipped.

## Oracle by change type

| Change type | Oracle | Lands before |
| --- | --- | --- |
| FIX | A test reproducing the reported failure, failing at the current commit | The fix |
| FEATURE | A test asserting the new acceptance condition, failing at the current commit | The implementation |
| REFACTOR | A characterisation or approval test capturing current behaviour, passing at the current commit | The structural change |
| CHORE, mechanical bulk | The existing suite, plus a sampled acceptance check over the class of change | The bulk edit |
| Interface change | The declared failure and success surface asserted at the boundary | The implementation |

A change that is two of these is two commits, in that order.

## Commit order is the proof

The claim that the oracle came first is only checkable in history.
Commit the oracle on its own, then the implementation. Where a
characterisation pin and a new behaviour test are both needed, that is
three commits: pin, new failing test, implementation. History that shows
the implementation first cannot be distinguished from tests written to
match the code, which is exactly the failure mode being avoided.

## Why independence matters more for agents

Generating tests after faulty code roughly halves fault detection
compared with generating them independently, because the implementation
and the tests become mutually consistent and conceal the defect
(EV-0007). Surfacing targeted test-impact context cut regressions on a
benchmark from 6.08 to 1.82 per cent, while generic test-driven
instructions with no contextual data made regressions worse at 9.94 per
cent (EV-0003), so the instruction alone is not the active ingredient.
Converting requirements into structured acceptance tests before coding
improved generated web-app quality substantially, but only where the
enforcement protocol matched the work (EV-0005). With human-written
tests supplied, a narrow test-driven workflow reached 94.3 per cent on
SWE-bench Verified (EV-0004).

Scope, stated plainly: these are agent runs on curated benchmarks,
mostly SWE-bench Verified and generated web applications. EV-0004 in
particular measures resolving tests somebody else wrote, which is a
different problem from deciding what the tests should say. None of these
numbers is a claim about human developers, about arbitrary production
diffs, or about this estate's code. What they support is the direction:
the oracle has to exist independently, and it has to exist first.

## The human literature runs the other way, and that is fine

Across 82 observations from 39 professional developers, quality and
productivity were associated with granularity and uniformity of work
increments rather than with whether the test came before or after the
code (EV-0178). Small sample, short greenfield tasks, correlational
within an experimental corpus. It does not license abandoning test-first
where regression protection rather than developer productivity is the
goal. The mechanism differs between the two populations: for a human the
test is a design aid, for a model it is the only reliable oracle. Never
cite one side as evidence about the other.

## What does not count

- A print statement, a logging line, or anything that passes whatever
  the behaviour does. Agent test-writing frequency is about the same in
  runs that resolve and runs that do not, and what gets written is
  mostly observational prints rather than assertions (EV-0006).
- A test written in the same turn as the implementation by the same
  author with no failing run recorded.
- A snapshot approved without anyone reading the diff. Approval is a
  deliberate act or the file is decoration (EV-0180).
- A test whose result depends on a network call it does not control. An
  oracle that can fail for reasons unrelated to the code is not an
  oracle, it is a coin toss with a stack trace.
- Coverage as a proxy. Optimise for confidence per test; coverage past
  roughly 70 per cent has diminishing returns for applications
  (EV-0094). The delivery-testing pack owns this properly.

## Characterisation pins in particular

An approval test records current output as an approved artefact and
diffs every later run against it (EV-0180). Three rules keep it honest:

1. It is a safety net, never a specification. It captures current bugs
   with equal fidelity.
2. Any change to an approved file is reviewed as a behaviour change,
   because that is what it is.
3. Non-deterministic output needs scrubbing before it can be pinned, or
   the pin becomes a flake generator.

A pin over a single input is a weak pin. Cover the representative shapes
the caller actually sends, and give each declared failure mode its own
assertion, so that a change to one shape cannot hide behind another.
