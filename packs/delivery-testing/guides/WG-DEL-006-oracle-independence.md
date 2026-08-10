---
summary: How independent must the oracle be from the code it judges, and who authors it?
kind: guide
scope: estate
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
applies_when: [ships_code, has_test_suite]
sources: [EV-0006, EV-0007, EV-0009, EV-0017, EV-0189, EV-0191, EV-0092]
review: 2028-03
type: wargame
status: active
tags: [delivery, testing, ci]
---

# WG-DEL-006: How independent is the oracle?

## The question

A suite is worth exactly what its oracle is worth. Everything else,
coverage, mutation score, test count, is a measure of how much
machinery surrounds that judgement. The fork is not whether to write
tests. It is how far the thing making the judgement sits from the thing
being judged, because an oracle read back off the implementation agrees
with the implementation by construction, bugs included.

This guide covers independence for the suite. The sibling fork, which
kind of oracle a given change should build and when to commit it, is
the coding pack's oracle-strategy guide, GD-COD-001. Read that one for
the change; read this one for the suite that has to keep holding.

## It depends on

- Whether a specification exists that is not the code.
- Whether the behaviour has a checkable invariant, a published schema,
  or a second implementation to compare against.
- The tier. R2 and above already demand an oracle authored before
  implementation and frozen (`kernel/POLICY_SPEC.md`).
- Who is writing. A model will make an implementation and a test
  written beside it agree with each other, including where both are
  wrong.
- Whether the code is legacy behaviour we intend to preserve, or new
  behaviour we intend to specify.

## Options

### A. The implementation is the oracle
What it is: characterisation. Record what the code does now and assert
it keeps doing that.
Buys: a net around code nobody can specify, in minutes, which is what a
REFACTOR needs before structure moves.
Costs: it certifies current bugs. Tests generated after faulty code
detected roughly half the faults of tests generated independently, 14%
against 25% (EV-0007). Coverage and mutation numbers computed over such
a suite are informative only while the code is assumed correct
(EV-0009).

### B. Same author, oracle written first from the spec
What it is: the acceptance condition is written from the requirement
before the implementation exists, by whoever is doing the work.
Buys: most of the independence at almost no coordination cost. The
requirement, not the code, is what the assertion is read from.
Costs: the author's misreading of the requirement propagates into both
artefacts, and nothing catches it.

### C. Independent author, oracle frozen before implementation
What it is: a different session, agent or person writes the acceptance
condition from the agreement, and it is committed and frozen before
implementation starts.
Buys: the strongest independence available without an external
reference, and the failure mode in B stops being invisible.
Costs: coordination, and a frozen oracle that turns out to be wrong
needs a ruled change rather than an edit.

### D. An external reference is the oracle
What it is: a property or invariant (EV-0017), a published schema
driving generated conformance and negative cases (EV-0189), a reference
implementation, or a differential run against the previous version.
Buys: an oracle nobody on the team can quietly bend, and cases nobody
would have written by hand.
Costs: it pays only where an invariant or a schema exists, a
well-described but wrong API still passes a schema check, and
generation adds triage effort.

## Decision rule

- R2, or anything crossing a boundary another party depends on: **B**
  is sufficient and **C** is preferred where a second session is cheap.
  What the evidence protects is the author not having the implementation
  in context while writing the oracle, and writing the oracle first in
  the same session satisfies that: the implementation does not exist yet
  (EV-0007). Ambiguity here is not academic. In benchmarking, a third of
  R2 runs read this line as demanding a separate session, blocked waiting
  for one, and delivered nothing, while the rest wrote the oracle first
  and delivered correctly. A rule that half the readers obey by stopping
  is a badly written rule.
- R3, or anything irreversible: **C**. A separate author is required
  here, and the session must stop and request one rather than proceed.
  Defence in depth is worth a hand-off when the change cannot be undone.
- R0 or R1 with a stateable acceptance condition: **B** as the floor.
- A checkable invariant or a published schema exists: add **D** on top
  of whatever else is in force, because it is the cheapest independence
  the domain will ever offer.
- Legacy behaviour about to be restructured: **A** first, in its own
  commit, labelled as a pin rather than a specification, then B or C
  for the new behaviour.
- Any change where the only available oracle is the code just written:
  stop. That is not an oracle. Say so on the task record and get a
  specification, a reproduction or an invariant.

## Default

B everywhere, C from R2 upwards, D wherever the domain offers an
invariant or a schema, A confined to pinning. Binding requirement 1 in
the pack body is the floor beneath all of this: the check that decides
correctness is never derived from the implementation under test.

## What does not count as an oracle

A print. A log line. An assertion that the function returned something.
A test that passes against both the fixed and the broken version.
Agent-written test volume is uncorrelated with task success, largely
because what gets written is observational rather than assertive
(EV-0006, scoped to SWE-bench Verified runs). The mechanical test is
simple: revert the fix, and the test must go red.

## Worked rulings

- **Venture A (2026, argued)**: C. The acceptance walk-through in the
  signed agreement, its §A5, was written as a failing suite at Genesis,
  before any implementation, and the acceptance skips were lifted only
  when the journeys went green end to end. The agreement, not the code,
  was the oracle.
- **PatterTech EOS delivery pack (2026-08, argued)**: independence
  binds, ordering does not. Argued from EV-0007, which isolates
  independence rather than test-first as the load-bearing property, and
  from EV-0009 on why quality numbers stop meaning anything once the
  oracle is contaminated. The timing question was deliberately left to
  WG-DEL-007 and the P7 ablation.
