---
summary: Does this surface render dark, light, dual or mixed, and what does each cost the reader?
kind: guide
authority: preference
basis: empirical-evidence
evidence_grade: controlled
scope: brand:pattertech
sources: [EV-0027]
review: 2028-06
type: guide
tags: [web, colour, a11y, brand]
---

# GD-HOUSE-003: Which polarity register does the surface take?

## The question

Does the surface render on a dark ground, a light ground, both, or a
mixed register where the chrome is dark and reading surfaces go light?
This is the sharpest fork in the pack, because the house default sits on
the side the evidence is least kind to. It carries WG-WEB-001 forward
with the polarity literature attached.

## It depends on

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

## Default

A, with a formal surface ladder and one warm interlude surface, and with
a light register treated as a supported variant rather than a promise
made in passing.

## Worked rulings

- **PatterTech Website (2026-07, argued)**: A. Emitted light is the
  identity, the hero and diagrams are glow-native, and the maintenance
  budget is one person. The monotone risk was answered with the surface
  ladder and interlude bands rather than a second register. D was
  considered and declined on review cost, with a note to revisit if the
  journal grows past roughly twenty long reads.
- **Venture A (2026-07, argued)**: B, against the house default. An
  insurer-facing registry brand whose one physical object is an etched
  plate is print-native, and the ink-like clause carried it. Recorded in
  that venture's lock-book, not here.

## Counter-evidence

Two things pull against A and both are real. Platform design languages
ship dark registers as first-class and readers report preferring them,
so preference and measured performance disagree here. And the polarity
advantage shrinks as type grows, so a dark surface with a generous type
ladder pays much less than a dark surface leaning on small tracked mono.
Scope note on the finding itself: acuity and proofreading tasks under
controlled office lighting on displays of their period, adults with
normal or corrected vision, not sustained reading and not low-light use.
