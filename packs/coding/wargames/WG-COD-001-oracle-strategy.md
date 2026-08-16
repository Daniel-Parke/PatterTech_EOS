---
id: WG-COD-001
summary: Where does the oracle for this change come from, specification, characterisation, contract or downstream gate?
kind: wargame
type: wargame
tags: [delivery, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-COD-013, DOC-COD-001, DOC-COD-002]
applies_when: [edits_source]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0003, EV-0004, EV-0005, EV-0006, EV-0007, EV-0008, EV-0070, EV-0177, EV-0178, EV-0180, EV-0181, EV-0191, EV-0192]
review: 2027-05
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-COD-001: Where does the oracle come from?

## Decision question and stakes

Something has to say whether the code is right, and it has to come from
somewhere other than the code. When the author is a model, that is the
whole game: the implementation and any check written in the same context
will agree with each other, including where both are wrong. The fork is
which independent statement of intent you build. When you write it is a
separate and much smaller question, settled by D7 in the pack body and
by `packs/delivery-testing/wargames/WG-DEL-007-test-timing.md`.

## Doctrines or coverage gap under pressure

- `DOC-COD-013` (default): Write the oracle before the implementation wherever the condition can be stated.
- `DOC-COD-001` (binding): The oracle that judges a change is authored independently of the implementation under test.
- `DOC-COD-002` (binding): A gate oracle is observed failing before its green result counts as acceptance evidence.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can you state an acceptance condition before you start? A FIX almost
  always can. An exploratory spike usually cannot.
- Does a specification exist for the code you are about to change, or is
  the current behaviour the only specification there is?
- Is the change crossing a boundary that another agent, venture or
  release train depends on?
- Is the change mechanical and high-volume, where per-change oracles
  cost more than they return?

Applicability is `edits_source`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Specification-sourced, from a context that never held the code

Write the executable acceptance condition from the requirement, in a
context that does not contain the candidate implementation. For a FIX
that means a failing reproduction. Writing it before the implementation
exists is the cheapest way to get that context, which is why D7 keeps it
as the default, but a separate session handed the specification and not
the diff satisfies it equally. Buys: an oracle the implementation cannot
have contaminated. Tests generated after faulty code detect roughly half
the faults of independently generated ones (EV-0007), and supplying the
right test context cut regressions from 6.08 to 1.82 per cent while
generic instructions made them worse (EV-0003). Costs: you have to state
the condition, which rules out genuine exploration, and a frozen oracle
that turns out wrong needs a ruled amendment rather than an edit.

### B. Characterisation first

Capture what the code does now as the oracle, then change. Approval
testing inverts the assertion: record current output as an approved
artefact and diff every later run against it (EV-0180). Buys: a
behaviour net around code nobody can specify, in minutes. Costs: it
locks in current bugs, so it is a safety net and never a specification,
and approvals rot into reflexive stamps unless approving is deliberate.

### C. Contract first

Declare the interface, then let implementations satisfy it. The
distinguishable failure modes are part of it. Buys: coordination across
a boundary two parties depend on, and a machine check for drift. Costs:
rigidity with no coordination benefit when the module has one caller.

### D. Generate and gate

Let the model write broadly and put the bar downstream in machine
checks: diff-aware policy and security rules, blocking findings split
from monitoring findings (EV-0070). Buys: throughput on high-volume
mechanical change. Costs: it catches classes of defect, not intent.
Roughly 40 per cent of generated programs in security-relevant scenarios
carried a vulnerability, and the rate moved with prompt and domain
(EV-0181, a 2021 model on loaded prompts), so the gate is necessary
under every option rather than an alternative to them.

## Failure premises

### Premortem for A. Specification-sourced, from a context that never held the code

Assume `A. Specification-sourced, from a context that never held the code` was selected and the outcome failed. Test this option's stated failure mechanism first: you have to state the condition, which rules out genuine exploration, and a frozen oracle that turns out wrong needs a ruled amendment rather than an edit.

### Premortem for B. Characterisation first

Assume `B. Characterisation first` was selected and the outcome failed. Test this option's stated failure mechanism first: it locks in current bugs, so it is a safety net and never a specification, and approvals rot into reflexive stamps unless approving is deliberate.

### Premortem for C. Contract first

Assume `C. Contract first` was selected and the outcome failed. Test this option's stated failure mechanism first: rigidity with no coordination benefit when the module has one caller.

### Premortem for D. Generate and gate

Assume `D. Generate and gate` was selected and the outcome failed. Test this option's stated failure mechanism first: it catches classes of defect, not intent. Roughly 40 per cent of generated programs in security-relevant scenarios carried a vulnerability, and the rate moved with prompt and domain (EV-0181, a 2021 model on loaded prompts), so the gate is necessary under every option rather than an alternative to them.

## Decision rule

- The change has a stateable acceptance condition, or is a FIX, or
  touches a boundary: A, written from the requirement and by default
  written first, because that is the cheapest clean context there is.
- The code has no trustworthy specification and you are about to move
  its structure: B first, then A for the new behaviour. See
  `packs/coding/wargames/WG-COD-004-pin-then-change.md`.
- Two agents, two ventures or two release trains meet here: C on top of
  A, declaring the failure modes as part of it. See
  `packs/coding/wargames/WG-COD-003-failure-mode-contract.md`.
- Mechanical bulk change with no per-change intent to state: D, with a
  sampled A oracle over the class rather than each instance.
- Under every option the gate from D still runs. It is a floor.

## Safe default

A. Almost every change in a venture repo has a stateable acceptance
condition, and the cost of finding out later that the checks agreed with
the bug is higher than the cost of stating it. What binds is the source
of the condition, not the moment it is written: B1 in the pack body is
the floor, not authored by the agent holding the implementation and seen
to fail once before it counts.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can you state an acceptance condition before you start? A FIX almost always can. An exploratory spike usually cannot.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. Almost every change in a venture repo has a stateable acceptance condition, and the cost of finding out later that the checks agreed with the bug is higher than the cost of stating it. What binds is the source of the condition, not the moment it is written: B1 in the pack body is the floor, not authored by the agent holding the implementation and seen to fail once before it counts.

**Exit condition:** Stop or roll back the selected branch when you have to state the condition, which rules out genuine exploration, and a frozen oracle that turns out wrong needs a ruled amendment rather than an edit, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can you state an acceptance condition before you start? A FIX almost always can. An exploratory spike usually cannot.

## Counter-evidence and transfer limits

### Evidence boundary

The agent results above (EV-0003, EV-0004, EV-0005, EV-0007) are runs on
curated benchmarks, mostly SWE-bench Verified. Across 82 observations
from 39 human professionals, quality and productivity tracked
granularity and uniformity of work increments, not sequencing (EV-0178).
The two populations agree more than this Wargame used to claim, and
neither measures ordering as the active ingredient: EV-0007 isolates the
authoring context, EV-0178 isolates increment size. Do not cite either
as evidence for the other, or as evidence that the test must come first.

The strongest measurement of contamination is EV-0480. Prompted with the
buggy implementation, eleven frontier models produced 104.15
bug-revealing tests on average, against 304.08 prompted with the correct
implementation and 186.77 when the code was replaced by a specification.
Its licence was recorded from a research packet rather than read at
source, so the row carries no observation date.
### Preserved reasoning: What does not count as an oracle

An observational print is not a test. Agent test-writing frequency is
about the same in runs that resolve and runs that do not, and what gets
written is mostly prints rather than assertions (EV-0006). If it does
not fail when the behaviour is wrong, it is not an oracle.
### Historical ruling boundary

The baseline file carried 4 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
