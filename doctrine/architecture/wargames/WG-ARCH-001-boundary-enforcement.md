---
summary: Where do module boundaries live: convention, machine contract, or the directory tree?
type: wargame
tags: [arch, tooling]
status: active
review_by: 2027-07
---

# WG-ARCH-001: Where do module boundaries live?

## The question

Every codebase claims a layering. The fork is what stops it eroding:
a convention people remember, a machine-checked import contract, or a
directory tree that makes violations physically awkward. Erosion is
quiet and one-way; by the time a boundary hurts, it has been crossed
for months.

## It depends on

- Who writes the code: agents cross conventions without noticing;
  they respect failing checks absolutely.
- Whether a proof of harmless movement exists (tests or an output
  canary) that makes re-shaping the tree safe.
- How many consumers a shared layer has.

## Options

### A. Convention
Documented layering, enforced by review. Free, and it erodes at the
speed of the busiest week.

### B. Machine contract over any layout
An import-linter style contract in CI: the layering fails the build
when crossed, wherever files sit. Cheap, layout-agnostic, and the
contract file documents the architecture.

### C. The tree is the architecture
Boundaries as physical directories (shared, platform, products), plus
the machine contract. The location of a file answers "may I import
this"; the move is only safe with a behaviour canary proving it
changed nothing.

## Decision rule

Agents in the workforce or a second consumer of any shared layer: at
least B, from the first week. Move to C when a canary exists that
proves moves are output-neutral, and do the move in one reviewed
change. A is acceptable only for a single-surface S venture.

## Default

B, rising to C once a canary exists.

## Worked rulings

- **PatterTech_Business (2026-06, argued)**: B at its ADR-0001 (rings
  enforced by import-linter over a flat tree), then C at ADR-0007 once
  the output-hash canary proved the physical move neutral; both hashes
  unchanged after the re-shape.
- **WiseWattage (2026, argued)**: B in substance; one-way dependencies
  (app to api to engine) documented and review-enforced with CI
  boundary checks arriving piecemeal. The erosion it suffered first is
  why the rule exists.
