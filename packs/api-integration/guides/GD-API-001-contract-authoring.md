---
summary: Who writes the contract and when: by hand, in a definition language, generated from the handlers, or not at all?
kind: guide
authority: advisory
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0023, EV-0137, EV-0144, EV-0145, EV-0057]
review: on-change-of:EV-0023
type: guide
tags: [arch, tooling, ci]
review_by: 2027-11
---

# GD-API-001: who authors the contract, and when?

## The question

Every boundary ends up with a machine-readable contract, because BR-1
requires one. The fork is where it comes from: written before the code,
compiled from a definition language, emitted from the handlers, or
assembled after the fact when someone asks for docs. The failure that
decides it is drift: a document that says one thing while the service
does another is worse than no document, because generation, testing and
review all trust it.

## It depends on

- Who reads the contract before the code exists: another team, an
  external consumer, or nobody?
- Is the bigger risk a badly designed boundary, or a document that
  quietly stops matching the service?
- Do you own both sides of the seam, or only one?
- Is there more than one boundary sharing house patterns?

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
Costs: fails BR-1, defeats the breaking-change gate (there is no
baseline to diff), defeats schema-derived testing, and defeats client
generation.

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
(BR-1, BR-2), and house style is enforced by a ruleset rather than by
review comments (EV-0137).

## Default

C for internal boundaries in this estate, generated, committed and
drift-checked. A or B when the boundary is public. The choice is
recorded next to the code, not assumed.

## Worked rulings

- **WiseWattage (2026, argued, inherited here)**: C. OpenAPI generated
  from the API app, compiled into a types package and a typed client,
  committed with a CI drift check. See
  `packs/architecture/guides/WG-ARCH-005-contract-seam.md` and the
  2026-07 lesson in `registry/LESSONS.md`, which records that generated
  artefacts rot silently without the drift check.
- **PatterTech_Business (2026-06, argued, inherited here)**: C, from
  the same wargame, after failed mutations masqueraded as success in a
  plain-JS client.
- No venture has yet argued B. The definition-language option stays a
  preference until one does.
