---
summary: One brand or a family of accents?
type: wargame
tags: [web, brand, colour]
status: archived
review_by: 2027-07
---

# WG-WEB-009: One brand or a family of accents?

## The question

The site hosts sub-brands (ventures, products, imprints). Do they get their
own accents, and how far may an accent reach?

## It depends on

- Whether sub-brands live their own lives off-site (own domains, logos) or
  exist only as site sections.
- How many there are: three accents can stay coherent; eight cannot.
- Whether content is published "under" a sub-brand (an imprint model).

## Options

### A. Single accent
Everything in the parent accent. Simplest; sub-brands read as topics.

### B. Accent map (the imprint model)
One registered map (name -> hex) in a single module. Components accept an
accent prop and tint indices, straps, ticks and kickers; structure, type and
surfaces never change. Content pages take the accent of their publishing
venture.

### C. Full sub-brand theming
Per-brand type or surface changes. Off-doctrine on a shared site; if a
sub-brand needs this, it needs its own site speaking the family language.

## Decision rule

No family at all (one trade, one brand) -> A with a single accent; the map
is overhead without imprints. Sub-brands with independent identity and
published work -> B, with the map capped around five accents and every
accent passing contrast checks on the site's grounds. Purely topical
sections -> A. Anything pushing on type or surfaces -> C's answer: a
separate site.

## Default

B with a small map, because it keeps the system coherent while letting
imprints own their work.

## Worked rulings

- **PatterTech Website (2026-07)**: B. `accentFor()` maps PatterPower teal,
  WiseWattage green, PatterOS cyan, default deep-sky. The whitepaper page
  runs teal through kickers, ledger indices, plaque ticks and the panel tick;
  the journal index tints each entry's number by its venture. Structure and
  type identical throughout.
