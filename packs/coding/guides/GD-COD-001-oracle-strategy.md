---
summary: Where does the oracle for this change come from, test-first, characterisation, contract or downstream gate?
type: guide
tags: [testing, delivery, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0003, EV-0004, EV-0005, EV-0006, EV-0007, EV-0008, EV-0070, EV-0177, EV-0178, EV-0180, EV-0181]
review: 2027-05
review_by: 2027-05
---

# GD-COD-001: Where does the oracle come from?

## The question

Something has to say whether the code is right, and it has to exist
independently of the code. When the author is a model, that is the whole
game: the model will make the implementation and any test written
alongside it agree with each other, including where both are wrong. The
fork is which independent statement of intent you build, and when.

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

### A. Test-first, oracle-first

Write the executable acceptance condition before the implementation, and
commit it first. For a FIX that means a failing reproduction. Buys: an
oracle the implementation cannot have contaminated, which is the whole
point. Generating tests after faulty code roughly halves fault detection
compared with generating them independently (EV-0007), and supplying the
right test context cut regressions from 6.08 to 1.82 per cent while
generic instructions made them worse (EV-0003). Costs: you have to be
able to state the condition, which rules out genuine exploration.

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
  touches a boundary: A. Commit the oracle before the implementation.
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
condition, and the cost of finding out later that the tests agreed with
the bug is higher than the cost of writing the condition first.

## What does not count as an oracle

An observational print is not a test. Agent test-writing frequency is
about the same in runs that resolve and runs that do not, and what gets
written is mostly prints rather than assertions (EV-0006). If it does
not fail when the behaviour is wrong, it is not an oracle.

## Evidence boundary

The agent results above (EV-0003, EV-0004, EV-0005, EV-0007) are runs on
curated benchmarks, mostly SWE-bench Verified. The human result runs the
other way: across 82 observations from 39 professionals, quality and
productivity tracked granularity and uniformity of work increments, not
sequencing (EV-0178). These are not in conflict, because the mechanism
differs: for a human the test is a design aid, for a model it is the
only reliable oracle. Do not cite either side as evidence for the other.

## Worked rulings

- **PatterTech EOS coding pack (2026-08, argued)**: A as the binding
  default, with D as an unconditional floor. Argued from EV-0007 and
  EV-0003 for the sequencing, and from EV-0181 for the floor. The human
  TDD literature was excluded from the argument on purpose.
- **Inherited parser with no tests (2026-08, argued)**: B then A. The
  behaviour pin lands in its own commit, the new failing test for the
  intended change lands next, the implementation lands third. Worked in
  full at `packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md`.
- **High-volume dependency bumps (2026-08, inherited)**: D with a
  sampled A oracle, inherited from the EV-0008 finding that a fixed
  pipeline matched autonomous agents at far lower cost.
