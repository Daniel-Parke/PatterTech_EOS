---
summary: How much light does this surface carry, and which tiers of the graded system are enabled?
kind: guide
authority: preference
basis: local-observation
evidence_grade: anecdotal
scope: brand:pattertech
sources: [EV-0232, EV-0234]
review: 2028-04
type: guide
tags: [web, motion, colour, brand]
review_by: 2028-04
---

# GD-HOUSE-001: How much light does this surface carry?

## The question

The house treats light as evidence of a source rather than decoration,
graded into four tiers: field, conduit, bloom and radiance. This guide
decides which tiers a surface enables and where the dimmer sits. It
carries WG-WEB-005 forward with its numbers moved out to
`packs/pattertech-house/refs/BUDGETS.md`.

## It depends on

- **The brand's physics.** Does the story involve light, energy or
  emission? A luminous brand starved of light reads dead. A paper brand
  drowned in glow reads cheap.
- **The audience's tolerance for atmosphere.** Research readers accept
  more ambience than compliance auditors.
- **The share of long-form reading.** Reading matter never animates,
  whatever the posture, so a reading-heavy surface has fewer places to
  spend.
- **Touch share and the performance floor.** Fields and conduits are
  cheap in CSS. Bloom needs a fine pointer and a delegated listener.
  Every promoted layer costs memory (FRAG-PATTERTECH-HOUSE-08).

## Options

### A. Structure only

What it is: no light beyond the signature pieces. Buys total calm, the
lowest maintenance surface, and no exposure to the layer budget. Costs
the brand's own story: executed on a luminous brand this reads inert,
and the recorded verdict on it was blunt.

### B. Fields only

What it is: ambient strata and washes. Nothing travels, nothing answers
presence. Buys atmosphere at almost no cost, and it degrades to nothing
under reduced motion without leaving a hole. Costs the sense that the
structure itself carries anything.

### C. The full graded system

What it is: fields breathe, conduits travel, surfaces answer presence,
interactive controls carry measured neon, monuments radiate. Buys the
posture the house was built for, and it is the only option in which a
first-time reader can name a moment on the page. Costs discipline: the
budgets in `packs/pattertech-house/refs/BUDGETS.md` have to be held, or
it collapses into option D by accident.

### D. Loud

What it is: standing glow on static components, gradient text on
content, cards that lift. Named here to be excluded. It is the generated
template look regardless of intent, and the flat-design correction
argues the same failure from the other side: affordance removed and then
paid for in noise (EV-0234). Never choose it.

## Decision rule

Match the brand's physics. A luminous or energetic brand takes C with
the budgets enforced. A print-native or deliberately austere brand takes
A or B. Never D. Inside C, scale by surface: reading-heavy pages leave
light in the environment, marketing pages may spend conduit and bloom
more freely. Two tests settle a dispute. If a screenshot of a single
component looks glowing, the budget is blown. If a first-time visitor
scrolls the page and can name no moment, the dimmer is too low.

## Default

C, with the budgets held, for any brand whose story involves energy. B
otherwise. Spend arrival before spending loops: one-shot events may be
plainly visible because they happen once, on cue, and the page stays
calm between them.

## Worked rulings

- **PatterTech v1 (before 2026-07, inherited)**: unintentional D. Glowing
  statistics, glowing buttons, hover sheens, pulsing dots. Clean
  execution that read as a generated template.
- **PatterTech v2 (2026-07, argued)**: over-corrected to A. Structurally
  strong, and the owner's verdict was "Teletext, robotic". The lesson
  recorded with it is that the budget is a dimmer, not a switch.
- **PatterTech v3 (2026-07, argued)**: C. Fields on interludes and two
  home seams, the header line and colophon rules as conduits, bloom
  through one delegated listener, measured neon on controls and focus,
  monuments radiating, body text still not glowing.
- **PatterTech v4 (2026-07, argued)**: C with the dimmer one step higher.
  v3 passed the laws and failed the read on interior pages, where the
  home hero carried most of the energy. The recalibration relaxed the
  conduit duty cycle, added a one-shot heading sweep on section and page
  titles, moved mono indices from grey to the brand accent, and allowed a
  small number of persistent slow-traveller rules on monuments. This is
  the newer argued ruling, and it is the one the house follows. The
  relaxed figure lives in `packs/pattertech-house/refs/BUDGETS.md` and
  nowhere else.

## Counter-evidence

The one-shot heading sweep animates a paint property, which the
compositor guidance warns against (FRAG-PATTERTECH-HOUSE-07). It is
sanctioned because it runs once rather than in a loop, and because its
settled state is indistinguishable from an unswept heading, so reduced
motion lands on the same pixels instantly. If a measurement shows the
sweep costing a frame budget on target hardware, the measurement wins.
