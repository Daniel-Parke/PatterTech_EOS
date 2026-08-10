---
summary: A set of content needs a container. Ledger, plaque, panel, table or prose?
kind: guide
authority: preference
basis: local-observation
evidence_grade: anecdotal
scope: brand:pattertech
sources: [EV-0234, EV-0239]
review: 2028-05
type: guide
tags: [web, layout, density, content]
---

# GD-HOUSE-002: Which container does this content take?

## The question

A block of content has to sit in something. The house holds that there
is no universal card, so the container is derived from what the content
is rather than from what the page needs to look like. This carries
WG-WEB-003 forward. The anatomy of each container is in
`packs/pattertech-house/refs/KIT.md`.

## It depends on

- **What the content is.** Parallel facts, numbers, self-contained
  things, records, or sentences.
- **Whether items are links.** A whole-row link changes the anatomy and
  the hover affordance.
- **How many items, and whether the set grows.** A container that reads
  well at four and badly at thirty is the wrong container.
- **Whether items carry status or a per-item accent.** That pushes
  towards a ruled form with a meta column.

## Options

### A. Ledger, a ruled editorial list

What it is: hairline-ruled rows, each with a mono index, a display
title, a muted body and an optional right-hand mono meta column. Buys
scale from three rows to thirty, a document-like reading, and graceful
growth in every direction. Costs the visual separation a box gives, so
a ledger inside a busy page needs its rules to carry the work.

### B. Plaque, ruled figures

What it is: values in the display face with tabular figures, hairline
rules top and bottom, mono uppercase captions. Buys a readout that looks
measured rather than marketed. Costs impact if repeated: never more than
one row per moment, and a row of numbers is never a monument.

### C. Panel, the quiet box

What it is: a border on the first surface step, modest radius, no lift
and no sheen on hover. Buys a boundary around a genuinely self-contained
thing: a diagram, a product, a document, a contact channel. Costs the
whole point if used for parallel facts, at which stage it is the card
grid wearing a different name.

### D. Table or spec table

What it is: real records with three or more comparable fields, ruled
rows, mono headers, no zebra fill. Buys comparison. Costs readability if
a value needs a sentence, which means the content was prose.

### E. Prose

What it is: paragraphs. Buys everything a box would have taken away.
Costs nothing. This is the commonest correct answer and the one drafts
reach for last.

## Decision rule

Ask what the content is before asking how it should look. Facts take A.
Numbers take B. Things take C. Records take D. Sentences take E. If a
draft has three icon tiles each holding one sentence, the answer was A
or E and the icons were decoration. If the box's title would work as a
heading in a list, it was never a panel.

## Default

A ledger. It is the workhorse that replaced the card grid, and it
degrades well when meta, links or a second column arrive later. A small
container surface is easier to hold consistent than a large one
(EV-0239).

## Worked rulings

- **PatterTech Website (2026-07, argued)**: every icon-tile grid became a
  ledger, covering forces, tailwinds, applications, principles, services,
  ways and interests. Statistic bands became plaques. Ventures,
  whitepapers, contact channels and the contact block became panels. A
  five-term glossary stayed a ruled table with audio. Several boxed
  asides went back to prose.
- **The house drill (2026-08, argued)**: four parallel service offerings
  with a title, a line of description and a lead time in days resolve to
  one ledger with a mono meta column, not four panels and not four stat
  cards. Worked in
  `packs/pattertech-house/exemplars/EX-HOUSE-001-services-section.md`.

## Counter-evidence

There is no measurement behind this fork. The case against the card grid
is a recorded aesthetic verdict, not a comprehension result, and the
flat-design critique cuts both ways: stripping the box also strips a
signifier, and a ruled list has to pay that back with rules, indices and
hover affordance that are genuinely visible (EV-0234). A ledger whose
rules are too faint to see is the same failure as a card grid, arrived
at from the other direction.
