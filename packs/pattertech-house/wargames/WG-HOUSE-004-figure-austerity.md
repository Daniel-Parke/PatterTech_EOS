---
id: WG-HOUSE-004
summary: How austere is this figure, and may any figure in a piece carry a distinguishing device?
kind: wargame
type: wargame
tags: [content, eos, imagery, media, wargame, web]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-HOUSE-007, DOC-HOUSE-008]
applies_when: [adopts_pattertech_house]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: brand:pattertech
authority: preference
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0232, EV-0234, EV-0391]
review: 2028-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-HOUSE-004: How austere is this figure?

## Decision question and stakes

The house default is restraint, and the strongest evidence in the pack
argues against it for one specific job. Embellished charts cost nothing
in interpretation accuracy and are remembered better weeks later
(EV-0391). This Wargame decides how much a given figure
may carry, and it is the one place the house is allowed to be loud.

## Doctrines or coverage gap under pressure

- `DOC-HOUSE-007` (preference): Figures are positioned from data.
- `DOC-HOUSE-008` (preference): Every number has exactly one home.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **The job of the figure.** Read precisely, or remembered.
- **How many figures the piece carries.** A device repeated is a style,
  and a style is wallpaper.
- **Whether the figure is interactive.** The evidence covers static,
  print-like charts and says nothing about dashboards or repeated
  figures.
- **Whether the device would touch a datum.** Anything that moves,
  covers or crowds a value is out before the question is asked.

Applicability is `adopts_pattertech_house`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Austere always

What it is: every figure in the diagram kit's voice, mono labels,
hairline connectors, node dots, one endpoint accent at most. Buys total
consistency and an honest reading of every value. Costs memorability,
which the evidence says is a real cost and not a matter of taste.

### B. Austere, with one distinguished figure per piece

What it is: option A everywhere, plus one figure per piece allowed a
device that makes it the figure the reader carries away. The device sits
in the frame, the caption, the plate treatment or the composition, never
on the data. Buys the recall gain without paying accuracy. Costs a
judgement per piece about which figure earns it.

### C. Embellish throughout

What it is: a distinguishing device on every figure. Buys nothing the
evidence supports, since the study compared embellished against plain
rather than embellished against embellished. Costs the signal: once
every figure is decorated, none of them is the memorable one.

### D. Decorative chrome on data

What it is: glow on a line, gradient fills behind values, ornament
overlapping a datum. Named to be excluded. It is the failure that no
recall gain buys back, because the figure now misreports where a value
sits.

## Failure premises

### Premortem for A. Austere always

Assume `A. Austere always` was selected and the outcome failed. Test this option's stated failure mechanism first: memorability, which the evidence says is a real cost and not a matter of taste.

### Premortem for B. Austere, with one distinguished figure per piece

Assume `B. Austere, with one distinguished figure per piece` was selected and the outcome failed. Test this option's stated failure mechanism first: a judgement per piece about which figure earns it.

### Premortem for C. Embellish throughout

Assume `C. Embellish throughout` was selected and the outcome failed. Test this option's stated failure mechanism first: the signal: once every figure is decorated, none of them is the memorable one.

### Premortem for D. Decorative chrome on data

Assume `D. Decorative chrome on data` was selected and the outcome failed. Test this option's stated failure mechanism first: What it is: glow on a line, gradient fills behind values, ornament overlapping a datum. Named to be excluded. It is the failure that no recall gain buys back, because the figure now misreports where a value sits.

## Decision rule

Split by job. A figure whose numbers will be read, compared or quoted
takes A. A piece that needs one figure remembered promotes exactly one
to B, and the device stays off the data. Never C, because it spends the
budget everywhere and buys nothing. Never D. If a device would overlap a
line, cover a label or displace a node from its datapoint, the answer
was A regardless of the piece.

## Safe default

B: austere by default, one distinguished figure per piece, the device
outside the plot area.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****The job of the figure.** Read precisely, or remembered.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B: austere by default, one distinguished figure per piece, the device outside the plot area.

**Exit condition:** Stop or roll back the selected branch when memorability, which the evidence says is a real cost and not a matter of taste, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **The job of the figure.** Read precisely, or remembered.

## Counter-evidence and transfer limits

The supporting study is a single controlled comparison with a small
sample, one illustrator's hand-drawn style as the embellished condition,
static print-like charts, no interaction and no accessibility
measurement. Later replications report mixed results. It does not
license arbitrary decoration and says nothing about dashboards, repeated
figures or charts read under time pressure. Pulling the other way, the
flat-design critique argues that stripping signifiers costs
discoverability (EV-0234), and the expressive platform programme claims
gains from emphasis (EV-0232). Both are weak, both are scoped to their
own surfaces, and neither should be quoted as fact. The rule that
survives every one of them is that no ornament may overlap a line or
displace a datum.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
