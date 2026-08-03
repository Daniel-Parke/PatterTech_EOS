---
summary: Visual regression: nothing, component states, or full pages?
type: wargame
tags: [delivery, testing, web]
status: archived
review_by: 2027-07
---

# WG-DEL-003: What does visual regression testing cover?

## The question

Pixel comparison is the only gate that catches what every other gate
misses: the page that still passes its tests and looks wrong. It is
also the flakiest gate ever invented when run naively. The fork is its
scope, because scope decides whether zero-threshold comparison is
achievable.

## It depends on

- Whether a component kit exists with enumerable states (a styleguide
  or storybook surface).
- Whether rendering can be containerised and pinned (fonts, browser,
  rasteriser identical everywhere).
- How data-dependent the pages are; live data makes full pages diff by
  nature.

## Options

### A. None yet
No visual gate until the brand system stabilises. Honest at the very
start; every week it persists, drift compounds quietly.

### B. Component states, pixel-exact, pinned
Every kit component's states rendered in a pinned container, compared
at zero threshold against committed baselines; re-baselining is a
reviewed event. Deterministic by construction; blind to page-level
composition.

### C. Full pages
Screenshot the routes. Sees composition; inherits every data and
timing flake, so thresholds creep and the gate goes soft.

## Decision rule

A component kit exists: B, from the kit's first week, in the pinned
container the stack profile specifies. Add C only for genuinely static
pages (marketing routes with fixed content) where zero threshold still
holds. Data-driven pages are covered by end-to-end assertions, not
pixels. A is tolerable only before any kit exists, and building the
styleguide surface ends it.

## Default

B. Pixel-exact or it is not a gate; pinned or it is not pixel-exact.

## Worked rulings

- **WiseWattage (2026, argued)**: B. Lost Pixel at threshold zero over
  Storybook states, rendered in the pinned Docker image after host
  fonts made identical code diff across machines; baselines committed,
  updates deliberate.
- **PatterTech_Website (2026-07, argued)**: capture tooling over the
  real routes (its regression smokes) with a stable kit; a C-shaped
  ruling that works because the site is fully static, recorded in the
  v0.1 lock-in.
