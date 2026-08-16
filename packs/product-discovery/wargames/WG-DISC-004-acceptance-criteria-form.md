---
id: WG-DISC-004
summary: Once the problem is settled, in what form do the acceptance criteria go, a user story, EARS clause order, an executable test, or a full specification chain?
kind: wargame
type: wargame
tags: [delivery, eos, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DISC-003, DOC-DISC-005, DOC-DISC-017]
applies_when: [proposes_capability]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0074, EV-0075]
review: 2028-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DISC-004: In what form do the acceptance criteria go?

## Decision question and stakes

The problem is settled and the verdict is BUILD or TEST. Something now
has to say what done means, in a form the builder and the checker read
the same way. The fork is the notation, and the trap is that a notation
which reads as certainty can hide an open question rather than close it.

## Doctrines or coverage gap under pressure

- `DOC-DISC-003` (default): A discovery record exists and names the decision it unblocks.
- `DOC-DISC-005` (default): Every signal names a threshold and a source that exists.
- `DOC-DISC-017` (default): Write acceptance criteria in EARS clause order once the problem is settled.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is the trigger set closed, or are the triggers user intentions?
- Who reads this, a person, an agent, or a test runner?
- How contested is the acceptance condition?
- Does an automated check exist that could hold the criterion?

Applicability is `proposes_capability`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. User story with bullet criteria

As a role, I want a thing, so that an outcome, plus a list of bullets.
Buys: everybody already reads it, it carries the reason, and it is
cheap. Costs: the bullets have no grammar, so ambiguity survives
contact. Two readers agreeing they understood a bullet is not evidence
they understood the same thing.

### B. EARS clause order

While optional preconditions, when an optional trigger, the named system
shall produce one or more responses, with at most one trigger and
exactly one named system per requirement
(`EV-0409`). Buys: most of the ambiguity goes without
leaving natural language, and the template acts as a filter, because a
requirement that will not fit is usually a wish, a design decision, or
two requirements stuck together. Costs: it constrains form only and can
say nothing about whether the requirement should exist. Forcing an open
question into a shall-statement converts uncertainty into false
certainty, which is the exact failure this pack spends B1 to B3
preventing.

### C. Executable acceptance test first

Write the failing test, let it be the criterion. Buys: the only form
that cannot drift from the code, and the coding pack already binds an
oracle before acceptance. Costs: it only expresses what the harness can
observe, and it says nothing to a stakeholder who cannot read it.

### D. A full specification chain

Constitution, specification, plan and tasks, each layer generated from
the one above and checked by a command rather than by re-reading
(EV-0074), with specifications treated as living artefacts and gates at
phase boundaries (EV-0075). Buys: consistency between layers is
machine-checkable, and the chain suits greenfield work where nothing
exists to contradict it. Costs: the claim that this improves outcomes
had an accepted protocol and no collected results at the cutoff
(`EV-0414`), the reference implementation calls itself
experimental, and the ceremony is fixed regardless of the size of the
change.

## Failure premises

### Premortem for A. User story with bullet criteria

Assume `A. User story with bullet criteria` was selected and the outcome failed. Test this option's stated failure mechanism first: the bullets have no grammar, so ambiguity survives contact. Two readers agreeing they understood a bullet is not evidence they understood the same thing.

### Premortem for B. EARS clause order

Assume `B. EARS clause order` was selected and the outcome failed. Test this option's stated failure mechanism first: it constrains form only and can say nothing about whether the requirement should exist. Forcing an open question into a shall-statement converts uncertainty into false certainty, which is the exact failure this pack spends B1 to B3 preventing.

### Premortem for C. Executable acceptance test first

Assume `C. Executable acceptance test first` was selected and the outcome failed. Test this option's stated failure mechanism first: it only expresses what the harness can observe, and it says nothing to a stakeholder who cannot read it.

### Premortem for D. A full specification chain

Assume `D. A full specification chain` was selected and the outcome failed. Test this option's stated failure mechanism first: the claim that this improves outcomes had an accepted protocol and no collected results at the cutoff (`EV-0414`), the reference implementation calls itself experimental, and the ceremony is fixed regardless of the size of the change.

## Decision rule

- The trigger is a system event, a state or a time, and the response is
  observable: B, then C for the ones a harness can hold.
- The trigger is a user intention and the acceptance condition is still
  contested: stay in A, and say in the record that the criterion is
  provisional. Do not dress an open question in shall.
- The criterion is the whole point of the change and a harness can
  observe it: C, with B as the human-readable statement beside it.
- Greenfield, several layers of artefact, and somebody will actually
  run the consistency command: D is defensible, and it is a bet rather
  than a practice with evidence behind it.
- Any form, one rule: a criterion that names a solution rather than an
  observable condition goes back to the problem section.

## Safe default

B, once the problem is settled, with C wherever a harness can hold the
criterion. Write the criteria after the verdict, not before it, because
a criterion written during framing tends to be the requester's solution
in a template.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is the trigger set closed, or are the triggers user intentions?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B, once the problem is settled, with C wherever a harness can hold the criterion. Write the criteria after the verdict, not before it, because a criterion written during framing tends to be the requester's solution in a template.

**Exit condition:** Stop or roll back the selected branch when the bullets have no grammar, so ambiguity survives contact. Two readers agreeing they understood a bullet is not evidence they understood the same thing, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is the trigger set closed, or are the triggers user intentions?

## Counter-evidence and transfer limits

### Evidence boundary

EV-0074 and EV-0075 present the specification chain as an established
improvement, and neither carries controlled evidence for that claim. The
registered report that tests it had its protocol peer-reviewed and
accepted with no results collected at 2026-08-03, on
competitive-programming problems with closed checkable specifications,
which is the easiest possible case and the least like product discovery
(`EV-0414`). This Wargame teaches B on its own merits
and borrows no authority from the spec-driven claim. If the results land
and are positive, D moves up and this Wargame is re-argued.
### Preserved reasoning: What EARS does and does not carry

The clause order came out of analysing airworthiness regulations for a
jet engine control system (`EV-0409`), where the
system boundary and the trigger set are both closed and knowable.
Product discovery deals in triggers that are user intentions, so the
notation transfers and its guarantees do not. What survives the transfer
is the filter: attempt the template, and when the sentence will not
form, you have found either a wish, a design decision smuggled in as a
requirement, or two requirements that need separating. That filter is
worth the whole notation on its own.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
