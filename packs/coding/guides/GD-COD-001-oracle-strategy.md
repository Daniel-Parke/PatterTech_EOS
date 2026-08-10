---
summary: Where does the oracle for this change come from, specification, characterisation, contract or downstream gate?
type: guide
tags: [testing, delivery, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0003, EV-0004, EV-0005, EV-0006, EV-0007, EV-0008, EV-0070, EV-0177, EV-0178, EV-0180, EV-0181, EV-0191, EV-0192]
review: 2027-05
---

# GD-COD-001: Where does the oracle come from?

## The question

Something has to say whether the code is right, and it has to come from
somewhere other than the code. When the author is a model, that is the
whole game: the model will make the implementation and any check written
in the same context agree with each other, including where both are
wrong. The fork is which independent statement of intent you build.
When you write it is a separate and much smaller question, settled by
D7 in the pack body and by
`packs/delivery-testing/guides/WG-DEL-007-test-timing.md`.

## It depends on

- Can you state an acceptance condition before you start? A FIX almost
  always can. An exploratory spike usually cannot.
- Does a specification exist for the code you are about to change, or is
  the current behaviour the only specification there is?
- Is the change crossing a boundary that another agent, venture or
  release train depends on?
- Is the change mechanical and high-volume, where per-change oracles
  cost more than they return?

## Options

### A. Specification-sourced, from a context that never held the code

Write the executable acceptance condition from the requirement, in a
context that does not contain the candidate implementation. For a FIX
that means a failing reproduction. The cheapest way to get that context
is to write it before the implementation exists, which is why D7 keeps
that as the default, but a separate session handed the specification and
not the diff satisfies it equally. Buys: an oracle the implementation
cannot have contaminated, which is the whole point. Generating tests
after faulty code roughly halves fault detection compared with
generating them independently (EV-0007), and supplying the right test
context cut regressions from 6.08 to 1.82 per cent while generic
instructions made them worse (EV-0003). Costs: you have to be able to
state the condition, which rules out genuine exploration, and where the
condition is written first a frozen oracle that turns out to be wrong
needs a ruled amendment rather than an edit.

### B. Characterisation first

Capture what the code does now as the oracle, then change. Approval
testing inverts the assertion: record current output as an approved
artefact and diff every later run against it (EV-0180). Buys: a
behaviour net around code nobody can specify, in minutes. Costs: it
locks in current bugs, so it is a safety net and never a specification,
and approvals rot into reflexive stamps unless approving is a deliberate
act.

### C. Contract first

Declare the interface, then let implementations satisfy it. The
distinguishable failure modes are part of that interface. Buys:
coordination across a boundary two parties depend on, and a machine
check for drift. Costs: rigidity with no coordination benefit when the
module has one caller.

### D. Generate and gate

Let the model write broadly and put the bar downstream in machine
checks: diff-aware policy and security rules, blocking findings split
from monitoring findings (EV-0070). Buys: throughput on high-volume
mechanical change. Costs: it catches classes of defect, not intent.
Roughly 40 per cent of generated programs in security-relevant scenarios
carried a vulnerability, and the rate moved with prompt and domain
(EV-0181, a 2021 model on loaded prompts), so the gate is necessary
under every option, not an alternative to them.

## Decision rule

- The change has a stateable acceptance condition, or is a FIX, or
  touches a boundary: A. Write it from the requirement, and by default
  write it first, because that is the cheapest clean context there is.
- The code has no trustworthy specification and you are about to move
  its structure: B first, then A for the new behaviour. See
  `packs/coding/guides/GD-COD-004-pin-then-change.md`.
- Two agents, two ventures or two release trains meet here: C on top of
  A, and declare the failure modes as part of it. See
  `packs/coding/guides/GD-COD-003-failure-mode-contract.md`.
- Mechanical bulk change with no per-change intent to state: D, with a
  sampled A oracle over the class of change rather than each instance.
- Under every option the gate from D still runs. It is a floor.

## Default

A. Almost every change in a venture repo has a stateable acceptance
condition, and the cost of finding out later that the checks agreed with
the bug is higher than the cost of stating it. What binds is the source
of the condition, not the moment it is written. B1 in the pack body is
the floor: not authored by the agent holding the implementation, and
seen to fail once before it counts.

## What does not count as an oracle

An observational print is not a test. Agent test-writing frequency is
about the same in runs that resolve and runs that do not, and what gets
written is mostly prints rather than assertions (EV-0006). If it does
not fail when the behaviour is wrong, it is not an oracle.

## Evidence boundary

The agent results above (EV-0003, EV-0004, EV-0005, EV-0007) are runs on
curated benchmarks, mostly SWE-bench Verified. Across 82 observations
from 39 human professionals, quality and productivity tracked
granularity and uniformity of work increments, not sequencing (EV-0178).
The two populations agree more than this guide used to claim. Neither
one measures ordering as the active ingredient. What EV-0007 isolates is
the authoring context, and what EV-0178 isolates is increment size. Do
not cite either side as evidence for the other, and do not cite either
as evidence that the test must come first.

The strongest measurement of contamination is EV-0480. Prompted with the
buggy implementation, eleven frontier models produced 104.15
bug-revealing tests on average, against 304.08 prompted with the correct
implementation and 186.77 when the code was replaced by a specification.
Its licence was recorded from a research packet rather than read at the
source, so the row carries no observation date.

## Worked rulings

- **PatterTech EOS coding pack (2026-08-03, argued, superseded)**: A as
  the binding default, with D as an unconditional floor. Argued from
  EV-0007 and EV-0003 for the sequencing, and from EV-0181 for the
  floor. The human TDD literature was excluded on purpose, which is how
  the ruling came out reading sequencing as the finding.
- **PatterTech EOS coding pack (2026-08-10, argued, ADR-0006)**: A on
  its source, not on its clock. The binding half is the authoring
  context plus a demonstrated failure; the ordering became D7. Argued
  from EV-0007 for the context, EV-0006 for ordering carrying no
  measured outcome, EV-0178 for what increment size was doing, and
  EV-0191 with EV-0192 for the replacement proof that a check bites.
- **Inherited parser with no tests (2026-08, argued)**: B then A. The
  behaviour pin lands in its own commit, the new failing test for the
  intended change lands next, the implementation lands third. Worked in
  full at `packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md`.
- **High-volume dependency bumps (2026-08, inherited)**: D with a
  sampled A oracle, inherited from the EV-0008 finding that a fixed
  pipeline matched autonomous agents at far lower cost.
