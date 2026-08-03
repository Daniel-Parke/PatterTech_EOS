---
summary: Once the problem is settled, in what form do the acceptance criteria go, a user story, EARS clause order, an executable test, or a full specification chain?
type: guide
tags: [product, delivery, wargame]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0074, EV-0075]
review: 2028-07
review_by: 2028-07
---

# GD-DISC-004: In what form do the acceptance criteria go?

## The question

The problem is settled and the verdict is BUILD or TEST. Something now
has to say what done means, in a form the builder and the checker read
the same way. The fork is the notation, and the trap is that a notation
which reads as certainty can hide an open question rather than close it.

## It depends on

- Is the trigger set closed, or are the triggers user intentions?
- Who reads this, a person, an agent, or a test runner?
- How contested is the acceptance condition?
- Does an automated check exist that could hold the criterion?

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
(`FRAG-PRODUCT-DISCOVERY-07`). Buys: most of the ambiguity goes without
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
(`FRAG-PRODUCT-DISCOVERY-12`), the reference implementation calls itself
experimental, and the ceremony is fixed regardless of the size of the
change.

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

## Default

B, once the problem is settled, with C wherever a harness can hold the
criterion. Write the criteria after the verdict, not before it, because
a criterion written during framing tends to be the requester's solution
in a template.

## What EARS does and does not carry

The clause order came out of analysing airworthiness regulations for a
jet engine control system (`FRAG-PRODUCT-DISCOVERY-07`), where the
system boundary and the trigger set are both closed and knowable.
Product discovery deals in triggers that are user intentions, so the
notation transfers and its guarantees do not. What survives the transfer
is the filter: attempt the template, and when the sentence will not
form, you have found either a wish, a design decision smuggled in as a
requirement, or two requirements that need separating. That filter is
worth the whole notation on its own.

## Evidence boundary

EV-0074 and EV-0075 present the specification chain as an established
improvement, and neither carries controlled evidence for that claim. The
registered report that tests it had its protocol peer-reviewed and
accepted with no results collected at 2026-08-03, on
competitive-programming problems with closed checkable specifications,
which is the easiest possible case and the least like product discovery
(`FRAG-PRODUCT-DISCOVERY-12`). This guide teaches B on its own merits
and borrows no authority from the spec-driven claim. If the results land
and are positive, D moves up and this guide is re-argued.

## Worked rulings

- **PatterTech EOS product-discovery pack (2026-08, argued)**: B adopted
  as default D9, D refused as an estate default pending
  `FRAG-PRODUCT-DISCOVERY-12`.
- **Approvals inbox request (2026-08, argued)**: A, provisional, because
  the verdict was TEST and the acceptance condition was the stopping
  rule rather than a system behaviour. See
  `packs/product-discovery/exemplars/EX-DISC-001-approvals-inbox-request.md`.
- **Export retention window (2026-08, inherited)**: B, and the attempt
  split one requested criterion into three separate requirements, which
  is the filter doing its job.
