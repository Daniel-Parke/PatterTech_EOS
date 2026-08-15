---
id: GD-HOUSE-002
summary: A set of content needs a container. Ledger, plaque, panel, table or prose?
kind: wargame
type: wargame
tags: [content, density, eos, layout, wargame, web]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-HOUSE-001]
applies_when: [adopts_pattertech_house]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: brand:pattertech
authority: preference
basis: local-observation
evidence_grade: anecdotal
sources: [EV-0234, EV-0239]
review: 2028-05
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-HOUSE-002: Which container does this content take?

## Decision question and stakes

A block of content has to sit in something. The house holds that there
is no universal card, so the container is derived from what the content
is rather than from what the page needs to look like. This carries
the retired historical web container-choice scenario forward. The anatomy of each container is in
`packs/pattertech-house/refs/KIT.md`.

## Doctrines or coverage gap under pressure

- `DOC-HOUSE-001` (preference): The container comes from the content, not from the layout.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **What the content is.** Parallel facts, numbers, self-contained
  things, records, or sentences.
- **Whether items are links.** A whole-row link changes the anatomy and
  the hover affordance.
- **How many items, and whether the set grows.** A container that reads
  well at four and badly at thirty is the wrong container.
- **Whether items carry status or a per-item accent.** That pushes
  towards a ruled form with a meta column.

Applicability is `adopts_pattertech_house`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Ledger, a ruled editorial list

Assume `A. Ledger, a ruled editorial list` was selected and the outcome failed. Test this option's stated failure mechanism first: the visual separation a box gives, so a ledger inside a busy page needs its rules to carry the work.

### Premortem for B. Plaque, ruled figures

Assume `B. Plaque, ruled figures` was selected and the outcome failed. Test this option's stated failure mechanism first: impact if repeated: never more than one row per moment, and a row of numbers is never a monument.

### Premortem for C. Panel, the quiet box

Assume `C. Panel, the quiet box` was selected and the outcome failed. Test this option's stated failure mechanism first: the whole point if used for parallel facts, at which stage it is the card grid wearing a different name.

### Premortem for D. Table or spec table

Assume `D. Table or spec table` was selected and the outcome failed. Test this option's stated failure mechanism first: readability if a value needs a sentence, which means the content was prose.

### Premortem for E. Prose

Assume `E. Prose` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing. This is the commonest correct answer and the one drafts reach for last.

## Decision rule

Ask what the content is before asking how it should look. Facts take A.
Numbers take B. Things take C. Records take D. Sentences take E. If a
draft has three icon tiles each holding one sentence, the answer was A
or E and the icons were decoration. If the box's title would work as a
heading in a list, it was never a panel.

## Safe default

A ledger. It is the workhorse that replaced the card grid, and it
degrades well when meta, links or a second column arrive later. A small
container surface is easier to hold consistent than a large one
(EV-0239).

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****What the content is.** Parallel facts, numbers, self-contained things, records, or sentences.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A ledger. It is the workhorse that replaced the card grid, and it degrades well when meta, links or a second column arrive later. A small container surface is easier to hold consistent than a large one (EV-0239).

**Exit condition:** Stop or roll back the selected branch when the visual separation a box gives, so a ledger inside a busy page needs its rules to carry the work, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **What the content is.** Parallel facts, numbers, self-contained things, records, or sentences.

## Counter-evidence and transfer limits

There is no measurement behind this fork. The case against the card grid
is a recorded aesthetic verdict, not a comprehension result, and the
flat-design critique cuts both ways: stripping the box also strips a
signifier, and a ruled list has to pay that back with rules, indices and
hover affordance that are genuinely visible (EV-0234). A ledger whose
rules are too faint to see is the same failure as a card grid, arrived
at from the other direction.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
