---
summary: Which oracle each change type needs, what counts as one, and how independence and a demonstrated failure are proved
type: foundation
tags: [testing, delivery]
kind: fact
scope: estate
sources: [EV-0003, EV-0004, EV-0005, EV-0006, EV-0007, EV-0094, EV-0105, EV-0178, EV-0180, EV-0191, EV-0192]
volatility: slow
review: 2027-05
---

# Oracle reference

Level 3 material behind binding requirement B1 and Wargame
`packs/coding/wargames/WG-COD-001-oracle-strategy.md`.

## Definition

An oracle is an executable statement of intent that fails when the
behaviour is wrong and passes when it is right, and that was not derived
from the implementation it judges. The second half is the part that gets
skipped.

## Oracle by change type

| Change type | Oracle | Where it comes from |
| --- | --- | --- |
| FIX | A test reproducing the reported failure | The report, and it fails at the current commit |
| FEATURE | A test asserting the new acceptance condition | The requirement, and it fails at the current commit |
| REFACTOR | A characterisation or approval test capturing current behaviour | The running code, deliberately, and it passes at the current commit |
| CHORE, mechanical bulk | The existing suite, plus a sampled acceptance check over the class of change | The class, not the instance |
| Interface change | The declared failure and success surface asserted at the boundary | The interface declaration |

A change that is two of these is two commits, and a characterisation pin
is always its own commit, because a pin and a specification are
different claims and a reviewer has to be able to tell them apart.

## How independence is proved

Two proofs, and the second one is the one that binds.

**Authoring context.** Record which session wrote the oracle, what was
in front of it, and by which method it stayed independent. The task
record carries this as `oracle_provenance`, with `author_session` and
`independence_method`. If the record does not exist, the commit message
answers the same question in one line: which specification,
reproduction, invariant or reference the expected value came from. An
unanswerable question here is a stop, not a shrug.

**Commit order, where you have it.** Committing the oracle on its own
and the implementation after is the cheapest evidence that the oracle
was not read off the code, because at that moment the code did not
exist. This is worth doing and it is default D7, not a rule. History
showing the implementation first is not proof of contamination, only an
absence of the cheap proof, and the authoring record has to carry the
weight instead.

## How the bite is proved

A check that has never been observed failing is an instrument nobody
calibrated. Test-first gave that proof away free, once per new test.
Its replacement is stronger and costs more.

- Revert the change and run the check. It must go red.
- Where a revert will not isolate it, mutate the changed lines and
  require the check to kill the mutants (EV-0192, EV-0191).
- Where the change is a new module with nothing to revert to, seed a
  fault by hand and record what the check did.

Mutation is diff-scoped by default, because whole-repository runs cost
more than they return, and mutation-guided generation is the production
version of the same idea (EV-0105). The delivery-testing pack owns the
mechanics in `packs/delivery-testing/references/QUALITY_SIGNALS.md`.

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
the oracle has to come from somewhere other than the code it judges.
They do not support a claim about the order.

## What the human literature adds

Across 82 observations from 39 professional developers, quality and
productivity were associated with granularity and uniformity of work
increments rather than with whether the test came before or after the
code (EV-0178). Small sample, short greenfield tasks, correlational
within an experimental corpus. Read together with the agent evidence it
says the same thing twice: the order is not the ingredient. What the
order was quietly buying is a clean context and small steps, and both of
those are now stated directly, as B1 and D8 in the pack body. Never cite
one population as evidence about the other, and do not cite either as
evidence that the test must come first.

## What does not count

- A print statement, a logging line, or anything that passes whatever
  the behaviour does. Agent test-writing frequency is about the same in
  runs that resolve and runs that do not, and what gets written is
  mostly observational prints rather than assertions (EV-0006).
- A test written by the author that had the implementation in front of
  it, in any order, with no failing run recorded.
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
