---
id: GD-HOUSE-001
summary: How much light does this surface carry, and which tiers of the graded system are enabled?
kind: wargame
type: wargame
tags: [brand, colour, eos, motion, wargame, web]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-HOUSE-010]
applies_when: [adopts_pattertech_house]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: brand:pattertech
authority: preference
basis: local-observation
evidence_grade: anecdotal
sources: [EV-0232, EV-0234, EV-0395, EV-0396]
review: 2028-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-HOUSE-001: How much light does this surface carry?

## Decision question and stakes

The house treats light as evidence of a source rather than decoration,
graded into four tiers: field, conduit, bloom and radiance. This guide
decides which tiers a surface enables and where the dimmer sits. It
carries the retired historical web ornament-budget scenario forward with its numbers moved out to
`packs/pattertech-house/refs/BUDGETS.md`.

## Doctrines or coverage gap under pressure

- `DOC-HOUSE-010` (default): The full graded light system for a luminous brand, fields only otherwise.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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
  Every promoted layer costs memory (EV-0396).

Applicability is `adopts_pattertech_house`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Structure only

Assume `A. Structure only` was selected and the outcome failed. Test this option's stated failure mechanism first: the brand's own story: executed on a luminous brand this reads inert, and the recorded verdict on it was blunt.

### Premortem for B. Fields only

Assume `B. Fields only` was selected and the outcome failed. Test this option's stated failure mechanism first: , and it degrades to nothing under reduced motion without leaving a hole. Costs the sense that the structure itself carries anything.

### Premortem for C. The full graded system

Assume `C. The full graded system` was selected and the outcome failed. Test this option's stated failure mechanism first: discipline: the budgets in `packs/pattertech-house/refs/BUDGETS.md` have to be held, or it collapses into option D by accident.

### Premortem for D. Loud

Assume `D. Loud` was selected and the outcome failed. Test this option's stated failure mechanism first: What it is: standing glow on static components, gradient text on content, cards that lift. Named here to be excluded. It is the generated template look regardless of intent, and the flat-design correction argues the same failure from the other side: affordance removed and then paid for in noise (EV-0234). Never choose it.

## Decision rule

Match the brand's physics. A luminous or energetic brand takes C with
the budgets enforced. A print-native or deliberately austere brand takes
A or B. Never D. Inside C, scale by surface: reading-heavy pages leave
light in the environment, marketing pages may spend conduit and bloom
more freely. Two tests settle a dispute. If a screenshot of a single
component looks glowing, the budget is blown. If a first-time visitor
scrolls the page and can name no moment, the dimmer is too low.

## Safe default

C, with the budgets held, for any brand whose story involves energy. B
otherwise. Spend arrival before spending loops: one-shot events may be
plainly visible because they happen once, on cue, and the page stays
calm between them.

## Cheapest discriminating test

Test one representative task with the intended audience under reduced motion and on the lowest supported device. Measure loading and frame behaviour before spending the optional house treatment.

## Fallback, exit and revisit

**Fallback `safe-default`:** C, with the budgets held, for any brand whose story involves energy. B otherwise. Spend arrival before spending loops: one-shot events may be plainly visible because they happen once, on cue, and the page stays calm between them.

**Exit condition:** Stop or roll back the selected branch when the brand's own story: executed on a luminous brand this reads inert, and the recorded verdict on it was blunt, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **The brand's physics.** Does the story involve light, energy or emission? A luminous brand starved of light reads dead. A paper brand drowned in glow reads cheap.

## Counter-evidence and transfer limits

The one-shot heading sweep animates a paint property, which the
compositor guidance warns against (EV-0395). It is
sanctioned because it runs once rather than in a loop, and because its
settled state is indistinguishable from an unswept heading, so reduced
motion lands on the same pixels instantly. If a measurement shows the
sweep costing a frame budget on target hardware, the measurement wins.
### Historical ruling boundary

The baseline file carried 4 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
