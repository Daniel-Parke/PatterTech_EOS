---
id: GD-API-001
summary: Who writes the contract and when: by hand, in a definition language, generated from the handlers, or not at all?
kind: wargame
type: wargame
tags: [arch, ci, eos, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-API-001]
applies_when: [exposes_service_boundary]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0023, EV-0137, EV-0144, EV-0145, EV-0057]
review: on-change-of:EV-0023
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-API-001: who authors the contract, and when?

## Decision question and stakes

Almost every boundary ends up with a machine-readable contract, because
default D9 asks for one and BR-2 cannot run without one. The fork is
where it comes from: written before the code,
compiled from a definition language, emitted from the handlers, or
assembled after the fact when someone asks for docs. The failure that
decides it is drift: a document that says one thing while the service
does another is worse than no document, because generation, testing and
review all trust it.

## Doctrines or coverage gap under pressure

- `DOC-API-001` (binding): A breaking-change check runs in CI against a committed baseline, and fails the build.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Who reads the contract before the code exists: another team, an
  external consumer, or nobody?
- Is the bigger risk a badly designed boundary, or a document that
  quietly stops matching the service?
- Do you own both sides of the seam, or only one?
- Is there more than one boundary sharing house patterns?

Applicability is `exposes_service_boundary`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Hand-written specification, committed, code follows

A person authors OpenAPI or AsyncAPI, reviews it, then implements
against it. Buys: a design conversation before anything is built, and a
document consumers can work from on day one. Costs: hand-written
specifications are where ambiguity comes from, and ambiguity caps every
downstream generator (EV-0144). Nothing stops the implementation
diverging later unless a gate is added.

### B. Definition language compiled to a specification

Author in a language with reuse and linting, such as TypeSpec, and emit
OpenAPI, clients and docs from one definition (EV-0145). Buys: house
patterns packaged as libraries, so the conforming choice is the cheap
one, and consistency across many boundaries. Costs: a compile step and a
second language between intent and the emitted artefact; the emitted
specification becomes a build output, which breaks any workflow that
expected to hand-edit it. Vendor-led roadmap despite the MIT licence.

### C. Code-first, specification generated from the handlers, committed
and drift-gated

The framework emits the specification deterministically; it is committed
and a CI check fails when the committed copy lags the app. Buys: the
document cannot drift from the service, by construction. Costs: the
boundary gets designed by whoever writes the handler, so the design
conversation happens late or not at all, and the emitted shapes carry
implementation habits.

### D. No committed contract

Prose docs, a shared collection, or nothing. Buys: nothing durable.
Costs: departs from D9, defeats the breaking-change gate in BR-2
(there is no baseline to diff), defeats schema-derived testing, and
defeats client generation. Legitimate only with a recorded reason
saying how a break gets caught instead.

## Failure premises

### Premortem for A. Hand-written specification, committed, code follows

Assume `A. Hand-written specification, committed, code follows` was selected and the outcome failed. Test this option's stated failure mechanism first: hand-written specifications are where ambiguity comes from, and ambiguity caps every downstream generator (EV-0144). Nothing stops the implementation diverging later unless a gate is added.

### Premortem for B. Definition language compiled to a specification

Assume `B. Definition language compiled to a specification` was selected and the outcome failed. Test this option's stated failure mechanism first: a compile step and a second language between intent and the emitted artefact; the emitted specification becomes a build output, which breaks any workflow that expected to hand-edit it. Vendor-led roadmap despite the MIT licence.

### Premortem for C. Code-first, specification generated from the handlers, committed

Assume `C. Code-first, specification generated from the handlers, committed` was selected and the outcome failed. Test this option's stated failure mechanism first: the boundary gets designed by whoever writes the handler, so the design conversation happens late or not at all, and the emitted shapes carry implementation habits.

### Premortem for D. No committed contract

Assume `D. No committed contract` was selected and the outcome failed. Test this option's stated failure mechanism first: departs from D9, defeats the breaking-change gate in BR-2 (there is no baseline to diff), defeats schema-derived testing, and defeats client generation. Legitimate only with a recorded reason saying how a break gets caught instead.

## Decision rule

- Public boundary, or several consumers you cannot upgrade in one go:
  A or B, and add C's drift gate anyway.
- More than about three boundaries sharing conventions: B, because that
  is what pays for the compile step.
- Internal boundary, one or two consumers, both inside the estate: C.
  Drift is the live risk there, not design quality.
- D is not an option once anything outside the repo calls the boundary.

Scope the ceremony to the surface that earns it, the way dbt scopes
contracts to public models and leaves private ones alone (EV-0057).
Whichever option is taken, the specification is committed and gated
(D9, BR-2), and house style is enforced by a ruleset rather than by
review comments (EV-0137).

## Safe default

C for internal boundaries in this estate, generated, committed and
drift-checked. A or B when the boundary is public. The choice is
recorded next to the code, not assumed.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Who reads the contract before the code exists: another team, an external consumer, or nobody?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C for internal boundaries in this estate, generated, committed and drift-checked. A or B when the boundary is public. The choice is recorded next to the code, not assumed.

**Exit condition:** Stop or roll back the selected branch when hand-written specifications are where ambiguity comes from, and ambiguity caps every downstream generator (EV-0144). Nothing stops the implementation diverging later unless a gate is added, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Who reads the contract before the code exists: another team, an external consumer, or nobody?

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
