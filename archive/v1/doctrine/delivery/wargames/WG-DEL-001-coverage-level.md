---
summary: What coverage floor, per surface, and how does it move?
type: wargame
tags: [delivery, testing, ci]
status: archived
review_by: 2027-07
---

# WG-DEL-001: What coverage floor, and how does it move?

## The question

Coverage numbers are cheap to demand and expensive to mean. The fork
is whether a venture sets floors at all, where they sit per surface,
and the mechanism by which they move, because a floor that can move
down is decoration.

## It depends on

- Whether CI exists yet (no CI, no floor to enforce).
- The surface's blast radius: an engine that computes money deserves a
  higher bar than a marketing page.
- Whether the codebase predates the floor (legacy joins by allowlist,
  not by big bang).

## Options

### A. No floor, review judgement
Coverage observed, not gated. Honest about how little a number proves;
provides nothing when review is tired.

### B. Floors per surface, ratchet-only-up
A measured floor per surface (engine higher than API, API higher than
UI), enforced in CI, moved only upwards, raised when real coverage
rises naturally. New or legacy modules join via an allowlist that only
grows.

### C. High bar everywhere from day one
Ninety-plus across the board. Produces assertion theatre in exactly
the code that least rewards it.

## Decision rule

CI exists: B, floors set from the first honest measurement (not an
aspiration), engine-grade surfaces above service surfaces above UI.
Raise a floor in the same change that raised coverage; never lower one
without a ruled deviation. A only where there is no CI (S ventures);
C never.

## Default

B. The estate's proven starting bands: high sixties to low seventies
for services at birth, engine surfaces a notch above, both ratcheted.

## Worked rulings

- **WiseWattage (2026, argued)**: B. API floor 70, engine floor 73,
  enforced in CI, with the mypy allowlist running the same
  ratchet-only-up mechanism for types; adopted after big-bang
  strictness proved unpayable on the existing tree.
