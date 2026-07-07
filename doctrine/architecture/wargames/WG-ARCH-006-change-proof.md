---
summary: What proves a change changed nothing: green tests, pinned behaviour, or byte-stable output?
type: wargame
tags: [arch, testing, ci]
status: active
review_by: 2027-07
---

# WG-ARCH-006: What proves a refactor changed nothing?

## The question

Restructures, moves and upgrades all claim behaviour is unchanged. The
fork is the strength of proof demanded before that claim is believed,
because "the tests pass" measures only what the tests measure.

## It depends on

- Is the output a deterministic artefact (documents, exports, builds)
  or live behaviour?
- How thin is the existing suite over the touched paths?
- Will agents do the restructuring? They need proofs, not confidence.

## Options

### A. The suite is the proof
Green tests before and after. Exactly as strong as the suite is
complete, and silent about everything it does not cover.

### B. Behaviour pinned first
Characterisation or golden tests written over the touched surface
before the change, discarded or kept after. Costs a pre-step; buys a
fence around the actual blast radius.

### C. Byte-stable output canary
A hash of the composed output (content, not paths), pinned before and
compared after; re-baselining is a deliberate reviewed event with the
old and new hashes recorded. The strongest claim available, and only
possible where output is deterministic.

## Decision rule

Deterministic artefact output: C, hashing composed content so the
canary survives file moves. Live behaviour with a thin suite: B before
touching anything. A alone only where the suite demonstrably covers
the touched paths. For agent-driven restructures, A is never
sufficient by itself.

## Default

B, with C wherever determinism makes it possible; pixels count as
artefacts (pinned-container visual regression at zero threshold is C
for UI).

## Worked rulings

- **PatterTech_Business (2026-06, argued)**: C; the output-hash canary
  (its ADR-0004) hashed composed kit output, survived the physical
  ring move of ADR-0007 unchanged, and re-baselining is governed as a
  reviewed event (ADR-0011).
- **WiseWattage (2026, argued)**: C for pixels (Lost Pixel at zero
  threshold in a pinned container) and B by policy for refactors (its
  PB-012 pins behaviour with characterisation tests where thin).
