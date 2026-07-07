---
summary: How do frontend and backend share types: by hand, generated with a drift gate, or one language?
type: wargame
tags: [arch, ci, tooling]
status: active
review_by: 2027-07
---

# WG-ARCH-005: How do the frontend and backend share types?

## The question

Two codebases describe the same requests and responses. The fork is
what keeps them agreeing: discipline, generation, or unification. The
failure mode that decides it is the silent one, where a renamed field
makes a mutation fail quietly and the UI reports success.

## It depends on

- One language across the seam, or two?
- Does anything human-maintained sit between the API's truth and the
  client's belief?
- Can generation run offline and deterministically (no live server
  needed to know the contract)?

## Options

### A. Hand-maintained types
Someone updates the client types when the API changes. Works until
the week it does not; the failure is silent.

### B. Generated from the API schema, committed, drift-gated
OpenAPI written deterministically from the API app, compiled into a
types package and a typed client that always checks `response.ok` and
throws typed errors; a CI test fails when the committed schema lags
the app. A backend change the frontend has not absorbed becomes a
build failure.

### C. One language, shared source
tRPC-style or shared TypeScript models. Erases the seam where the
whole stack is one language; unavailable across Python and TypeScript.

## Decision rule

Two languages: B, always, with the generator offline and the schema
committed. One-language monorepo: C is legitimate; take it with the
same commit-and-gate discipline for anything that leaves the repo. A
is not an option on any venture with users.

## Default

B. The estate runs Python services under TypeScript fronts; the seam
is generated, committed and gated or it lies.

## Worked rulings

- **PatterTech_Business (2026-06, argued)**: B, its ADR-0006, after
  failed mutations masqueraded as success in a plain-JS app; the typed
  client's always-check-ok rule is written into the seam.
- **WiseWattage (2026, argued)**: B; OpenAPI to a generated types
  package and client, committed, with the drift check in CI.
