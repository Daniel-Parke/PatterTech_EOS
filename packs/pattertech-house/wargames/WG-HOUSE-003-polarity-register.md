---
id: WG-HOUSE-003
summary: Does this surface render dark, light, dual or mixed, and what does each cost the reader?
kind: wargame
type: wargame
tags: [a11y, brand, colour, eos, wargame, web]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-HOUSE-006]
applies_when: [adopts_pattertech_house]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: brand:pattertech
authority: preference
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0027, EV-0393, EV-0394]
review: 2028-06
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-HOUSE-003: Which polarity register does the surface take?

## Decision question and stakes

Does the surface render on a dark ground, a light ground, both, or a
mixed register where the chrome is dark and reading surfaces go light?
This is the sharpest fork in the pack, because the house default sits on
the side the evidence is least kind to. It carries the retired historical web surface-register scenario forward
with the polarity literature attached.

## Doctrines or coverage gap under pressure

- `DOC-HOUSE-006` (preference): The dark register buys itself back in the smallest type.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **The brand's physics.** Emission and glow favour dark. Paper, print
  and daylight favour light.
- **The signature visuals.** Luminous diagrams and canvases need a dark
  ground to exist at all.
- **Print siblings.** If the venture ships light documents, a light
  reading register rhymes with them.
- **The content mix.** Dense instrument surfaces read well dark. Very
  long text is easier to sustain light unless the dark body contrast is
  engineered deliberately.
- **The maintenance budget.** Every register roughly doubles the token
  and review surface. Dual is a cost, not a toggle.

Applicability is `adopts_pattertech_house`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Dark-first, single register

What it is: one token set on a dark ground with a formal surface ladder.
Buys glow-native signature pieces, one register to hold consistent, and
the house identity as designed. Costs the measured polarity advantage:
positive polarity gave better acuity and better proofreading for both
younger and older adults, concentrated at small character sizes
(EV-0393). The house leans its annotation voice on
exactly that size band, so the cost lands where it hurts most.

### B. Light-first, single register

What it is: an editorial print feel by default. Buys the polarity
advantage and a natural rhyme with printed siblings. Costs the
signature visuals, which need reworking or framing as dark islands, and
costs the brand story where the story is emitted light.

### C. Dual register with a theme switch

What it is: both, chosen by the reader. Buys the honest answer to a
literature that says register is a preference rather than a truth
(EV-0394), and it serves the readers with impairments
who genuinely do better dark. Costs twice the surface to design, test
and review, and it doubles the chance the two drift.

### D. Mixed register, dark chrome and light reading surfaces

What it is: the chrome stays dark, the article kit goes light. Buys the
strongest "this is a document" cue for a research-led surface, and puts
the polarity advantage exactly where the small text lives. Costs a
second register for the article kit and the review that goes with it.

## Failure premises

### Premortem for A. Dark-first, single register

Assume `A. Dark-first, single register` was selected and the outcome failed. Test this option's stated failure mechanism first: the measured polarity advantage: positive polarity gave better acuity and better proofreading for both younger and older adults, concentrated at small character sizes (EV-0393). The house leans its annotation voice on exactly that size band, so the cost lands where it hurts most.

### Premortem for B. Light-first, single register

Assume `B. Light-first, single register` was selected and the outcome failed. Test this option's stated failure mechanism first: the signature visuals, which need reworking or framing as dark islands, and costs the brand story where the story is emitted light.

### Premortem for C. Dual register with a theme switch

Assume `C. Dual register with a theme switch` was selected and the outcome failed. Test this option's stated failure mechanism first: twice the surface to design, test and review, and it doubles the chance the two drift.

### Premortem for D. Mixed register, dark chrome and light reading surfaces

Assume `D. Mixed register, dark chrome and light reading surfaces` was selected and the outcome failed. Test this option's stated failure mechanism first: a second register for the article kit and the review that goes with it.

## Decision rule

If the identity is luminous and the signature visuals emit light, take
A and engineer the small type back up under H6 in
`packs/pattertech-house/PACK.md`. If the brand is print-native and its
visuals are ink-like, take B. Take C only for a demonstrated
dual-context audience, and only if the review budget covers two
registers honestly. Consider D when long reads dominate and the printed
siblings are light. Whatever the ruling, the contrast floor is the
WCAG 2.2 AA requirement binding from `packs/ui-ux/PACK.md` (EV-0027),
and a perceptual pass is an internal readability review that never
appears in a conformance claim.

## Safe default

A, with a formal surface ladder and one warm interlude surface, and with
a light register treated as a supported variant rather than a promise
made in passing.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****The brand's physics.** Emission and glow favour dark. Paper, print and daylight favour light.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with a formal surface ladder and one warm interlude surface, and with a light register treated as a supported variant rather than a promise made in passing.

**Exit condition:** Stop or roll back the selected branch when the measured polarity advantage: positive polarity gave better acuity and better proofreading for both younger and older adults, concentrated at small character sizes (EV-0393). The house leans its annotation voice on exactly that size band, so the cost lands where it hurts most, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **The brand's physics.** Emission and glow favour dark. Paper, print and daylight favour light.

## Counter-evidence and transfer limits

Two things pull against A and both are real. Platform design languages
ship dark registers as first-class and readers report preferring them,
so preference and measured performance disagree here. And the polarity
advantage shrinks as type grows, so a dark surface with a generous type
ladder pays much less than a dark surface leaning on small tracked mono.
Scope note on the finding itself: acuity and proofreading tasks under
controlled office lighting on displays of their period, adults with
normal or corrected vision, not sustained reading and not low-light use.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
