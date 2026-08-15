---
summary: Activation, outcomes and decision map for the pattertech-house Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: brand:pattertech
applies_when: [adopts_pattertech_house]
activation_paths: [**/*.css, **/*.scss, **/tokens/**, **/theme/**, **/tailwind.config.*, **/design-system/**]
volatility: slow
review: none
sources: [EV-0027, EV-0030, EV-0065, EV-0232, EV-0234, EV-0236, EV-0239, EV-0389, EV-0390, EV-0391, EV-0392, EV-0393, EV-0394, EV-0395, EV-0396, EV-0397, EV-0398, EV-0399, EV-0400, EV-0402]
type: guide
tags: [web, brand, colour, motion, layout, typography]
depends_on: [ui-ux, writing-content]
---


# pattertech-house

This pack is the PatterTech house visual language: containers, section
furniture, the graded light system, and the numbers that hold them. It
is taste, scoped to the PatterTech brand, and it activates only when a
venture's lock-book adopts it by name. Nothing here binds the estate,
and every rule is overridable by one recorded line. The portable
interface law lives in packs/ui-ux and is not repeated here.

## Activation

**The gate is adoption.** The predicate `adopts_pattertech_house` is
true only when the venture's lock-book names this pack in its adopted
set. Until then the triggers below match nothing, and an agent that
trips one loads this paragraph and stops. A house style that arrives
because a path matched is a house style nobody chose.

**Paths, once adopted.** Component, page, route, style and token
directories; design-system documentation; the styleguide route.

**Task types, once adopted.** Build or restyle a surface. Choose a
container, a section opening or a figure treatment. Set or spend a light
budget. Review a page.

**Keywords, fallback only.** Ledger, plaque, panel, colophon, section
mark, kicker, conduit, bloom, ignite, andon, Cherenkov, reticle, plate
number. Keywords never override the adoption gate.

**Predicates.**

| Predicate | True when |
| --- | --- |
| adopts_pattertech_house | the venture's lock-book names this pack |
| has_longform | the surface carries reading matter over roughly one screen |
| has_figures | the surface carries diagrams, charts or plates |
| has_dark_register | the ground is dark under GD-HOUSE-003 |

**Authority.** Everything here is `authority: preference` under
`kernel/METADATA_SPEC.md`, because a brand scope caps it there. The
authority audit under ADR-0008 found nothing in this pack to demote,
for that reason: no line in it was ever binding. There is
no deviation machinery: no waiver, no ADR, no recorded exception. A
venture departs by writing the departure in its lock-book and moving on.
Activation gives advice and never permission, and no line here lowers a
tier floor in `kernel/POLICY_SPEC.md` or softens an action class in
`kernel/GUARD_SPEC.md`.

## Outcomes and non-goals

**Outcomes.** A PatterTech surface reads as one document rather than a
template: numbered sections, a container chosen from the content, an
annotation voice carrying the precision, and light that behaves like
evidence of a source. A reader can name a moment on the page, and a
second person can rebuild the surface from written numbers rather than
from a screenshot.

**Non-goals.** This pack does not carry the accessibility floor,
keyboard behaviour, token pipeline, component sourcing or field
performance practice. Those are portable, they apply whether or not a
venture takes the house, and they live in `packs/ui-ux/PACK.md`. Where
a house rule below touches the same ground it is a restatement with no
authority of its own, and the ui-ux requirement is the one that holds.
This pack is not a copy guide, not a brand strategy, and not a component
library.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="H1"></a>
- `H1` to [DOC-HOUSE-001](doctrines/DOC-HOUSE-001-the-container-comes-from-the-content-not-from-the-layout.md) (preference)
<a id="H2"></a>
- `H2` to [DOC-HOUSE-002](doctrines/DOC-HOUSE-002-sections-open-flush-left-with-the-mark-in-a-fixed-order.md) (preference)
<a id="H3"></a>
- `H3` to [DOC-HOUSE-003](doctrines/DOC-HOUSE-003-animation-stays-on-the-compositor-whitelist.md) (preference)
<a id="H4"></a>
- `H4` to [DOC-HOUSE-004](doctrines/DOC-HOUSE-004-motion-is-judged-by-moving-area-and-scroll-coupling.md) (preference)
<a id="H5"></a>
- `H5` to [DOC-HOUSE-005](doctrines/DOC-HOUSE-005-reading-matter-never-animates-and-never-glows.md) (preference)
<a id="H6"></a>
- `H6` to [DOC-HOUSE-006](doctrines/DOC-HOUSE-006-the-dark-register-buys-itself-back-in-the-smallest-type.md) (preference)
<a id="H7"></a>
- `H7` to [DOC-HOUSE-007](doctrines/DOC-HOUSE-007-figures-are-positioned-from-data.md) (preference)
<a id="H8"></a>
- `H8` to [DOC-HOUSE-008](doctrines/DOC-HOUSE-008-every-number-has-exactly-one-home.md) (preference)
- source `defaults:001` to [DOC-HOUSE-009](doctrines/DOC-HOUSE-009-dark-first-single-register-with-a-formal-surface-ladder.md) (default)
- source `defaults:002` to [DOC-HOUSE-010](doctrines/DOC-HOUSE-010-the-full-graded-light-system-for-a-luminous-brand-fields-only-ot.md) (default)
- source `defaults:003` to [DOC-HOUSE-011](doctrines/DOC-HOUSE-011-a-surface-ladder-of-four-to-six-steps-derived-in-a-perceptually.md) (default)
- source `defaults:004` to [DOC-HOUSE-012](doctrines/DOC-HOUSE-012-a-reading-measure-at-the-low-end-of-the-usual-advice.md) (default)
- source `defaults:005` to [DOC-HOUSE-013](doctrines/DOC-HOUSE-013-three-type-roles-three-families-as-the-ceiling.md) (default)
- source `defaults:006` to [DOC-HOUSE-014](doctrines/DOC-HOUSE-014-one-delegated-pointer-listener-for-surface-reactivity.md) (default)
- source `defaults:007` to [DOC-HOUSE-015](doctrines/DOC-HOUSE-015-spend-the-design-budget-on-the-first-screen.md) (default)
- source `defaults:008` to [DOC-HOUSE-016](doctrines/DOC-HOUSE-016-platform-hygiene.md) (default)
- source `preferences:001` to [DOC-HOUSE-017](doctrines/DOC-HOUSE-017-cyan-as-the-live-accent-with-the-cherenkov-story-behind-it-and-a.md) (preference)
- source `preferences:002` to [DOC-HOUSE-018](doctrines/DOC-HOUSE-018-the-andon-line-one-accent-hairline-across-the-top-of-the-chrome.md) (preference)
- source `preferences:003` to [DOC-HOUSE-019](doctrines/DOC-HOUSE-019-plate-numbering-as-a-mono-figure-number-joined-to-its-caption-by.md) (preference)
- source `preferences:004` to [DOC-HOUSE-020](doctrines/DOC-HOUSE-020-a-journal-index-rather-than-a-card-grid-on-hubs-so-two-entries-r.md) (preference)
- source `preferences:005` to [DOC-HOUSE-021](doctrines/DOC-HOUSE-021-a-colophon-rather-than-a-closing-call-to-action-slab-written-fre.md) (preference)

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| How much light does this surface carry | Which tiers are enabled and how loud the dimmer sits | `packs/pattertech-house/guides/GD-HOUSE-001-light-posture.md` |
| Which container does this content take | Ledger, plaque, panel, table or prose | `packs/pattertech-house/guides/GD-HOUSE-002-container-choice.md` |
| Which polarity register does the surface take | Dark, light, dual or mixed, and what each costs | `packs/pattertech-house/guides/GD-HOUSE-003-polarity-register.md` |
| How austere is this figure | Whether a figure may carry a distinguishing device | `packs/pattertech-house/guides/GD-HOUSE-004-figure-austerity.md` |

Whether a surface answers presence is not a fork with a guide behind
it. The default above settles it: one delegated pointer listener, fine
pointers only, components opting in. A venture that wants an inert
surface writes that line in its lock-book.

Level-three detail: every number in
`packs/pattertech-house/refs/BUDGETS.md`, the container and furniture
anatomy in `packs/pattertech-house/refs/KIT.md`, the light mechanics in
`packs/pattertech-house/refs/LIGHT_MECHANICS.md`, a worked section in
`packs/pattertech-house/exemplars/EX-HOUSE-001-services-section.md`.

## Failure modes and anti-patterns

- **The sticker.** A glow stuck onto a static component. The v1 failure:
  clean execution that read as a generated template anyway.
- **Restraint executed as absence.** The v2 failure, verdict "Teletext,
  robotic". The budget is a dimmer, not a switch, and the v4
  recalibration exists because v3 landed on the wrong side of it.
- **The generic tell.** Centred eyebrow above an icon-tile grid, glowing
  pill buttons, gradient text on statistics, a reveal on every paragraph,
  a closing slab identical on every page. If a section could be dropped
  into any generated site unchanged, it is not designed yet. The test is
  useful, unfalsifiable, and has no oracle a cold agent can run.
- **The system as the design**, where every page is well tokenised and
  nobody remembers one of them, and its mirror, **expressive
  convergence**, where reaching for emphasis lands on the same
  gradient-and-glow vocabulary everything else generates. The
  platform-scale statement of expressiveness licenses neither (EV-0232).
- **Structural drift, all three recorded in 2026-07.** A bleed that
  inherits its wrapper, so one block renders at three widths on one page.
  An automatic margin on a grid child, which gives up stretch and
  collapses a box whose only children are absolutely positioned. A mobile
  gutter expressed in three places until an article and a marketing page
  disagree about the left edge of a phone screen.
- **A law that lives only in module documentation.** Pattern-checkable
  laws belong in the lint command.

## Open questions and counter-evidence

- **The signature-motif claim is unevidenced.** The v1 doctrine holds
  that one motif promoted everywhere becomes identity. No primary source
  for it was located at the cutoff, so it is a working hypothesis and is
  deliberately absent from the requirements above.
- **The numbers are calibration, not measurement.** Every figure in
  `packs/pattertech-house/refs/BUDGETS.md` comes from one project's eye,
  and they are reproducible because they are written down rather than
  because they are correct.
- **Restraint against memorability is a genuine standoff.** Embellished
  charts cost nothing in interpretation accuracy and gain in long-term
  recall (EV-0391), so the house may never claim that
  restraint improves comprehension. Scope note: one study, small sample,
  one illustrator's hand-drawn style, static print-like charts, no
  interaction and no accessibility measurement. The split the pack takes
  is by job, argued in GD-HOUSE-004.
- **Contrast maths is contested and the pack refuses to pick.** A
  perceptual model argues that a ratio quoted for light text on a dark
  ground misdescribes what a reader sees (EV-0389), and
  it was removed from the successor standard's draft in 2023 with no
  replacement chosen (EV-0390). WCAG 2.2 AA stays the
  only thing that can be asserted, it binds from `packs/ui-ux/PACK.md`,
  and a perceptual pass is an internal readability review that never
  appears in a conformance claim.
- **The dark register's cost to our actual readers is untested.** Nobody
  has measured whether the polarity penalty matters for the audience this
  house serves. H6 is the hedge, not the answer.
- **Refresh triggers.** A visual contrast method selected for WCAG 3; a
  status change in CSS Color 4, CSS Text 4, the Properties and Values API
  or CSS Masking 1; changed engine guidance on compositor-only
  properties; or a house budget challenged by a measurement.
