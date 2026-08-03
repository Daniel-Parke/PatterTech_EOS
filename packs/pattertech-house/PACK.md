---
summary: The PatterTech house visual language, adopted by name and never by default, with every house number in one place
kind: rule
authority: preference
lifecycle: active
basis: decision
evidence_grade: observational
scope: brand:pattertech
applies_when: [adopts_pattertech_house]
volatility: slow
review: on-change-of:WCAG-2.2
sources: [EV-0027, EV-0030, EV-0065, EV-0232, EV-0234, EV-0236, EV-0239]
type: guide
tags: [web, brand, colour, motion, layout, typography]
review_by: 2028-03
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
`kernel/METADATA_SPEC.md`, because a brand scope caps it there. There is
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

## House requirements

These hold inside an adopting venture, they are preferences at estate
level, and a lock-book line overrides any of them. Each names the failure
it prevents and the basis it rests on. Most rest on a recorded ruling
rather than on measurement, the correct shape for a domain built of
taste.

**Evidence pointer.** EV ids resolve in `registry/evidence.json`. The
fourteen house sources are frozen with version, licence, access date and
review trigger in `packs/pattertech-house/research/sources.fragment.json`
and are cited by fragment id, because the integrator import that assigns
final EV ids has not yet run for this pack.

**H1. The container comes from the content, not from the layout.**
`adopts_pattertech_house`. Parallel facts take a ledger, numbers take a
plaque, prose stays prose, and a panel is reserved for a genuinely
self-contained thing. Prevents the icon-tile card grid, the strongest
generic-template tell and the reason the 2026-07 rebuild happened.
Basis: local-observation, from the worked ruling in WG-WEB-003. See
`packs/pattertech-house/guides/GD-HOUSE-002-container-choice.md`.

**H2. Sections open flush left, with the mark in a fixed order.**
`adopts_pattertech_house`. Index, hairline, kicker, title, as real
heading structure rather than styled text. Prevents the centred
eyebrow-and-cards rhythm, and keeps the outline honest for anyone
reading through headings (EV-0027). Basis: decision, with the heading
part supported by a standard.

**H3. Animation stays on the compositor whitelist.**
`adopts_pattertech_house`. Transform, opacity, one-shot filters, and
shadow transitions on small elements. The one sanctioned exception is
the heading sweep, which is a one-shot and is named as such. Prevents a
page that looks calm and repaints every frame
(FRAG-PATTERTECH-HOUSE-07), and prevents layer promotion being sprinkled
rather than budgeted (FRAG-PATTERTECH-HOUSE-08). Basis: standard, from
engine guidance. Scope note: compositing rules are engine-specific and
change, so the whitelist is conservative rather than exact, and a
measurement on target hardware beats it.

**H4. Motion is judged by moving area and scroll coupling.**
`adopts_pattertech_house`. No large-area or scroll-coupled movement and
no parallax on a reading surface, whatever the reduced-motion setting
says, because most readers never set it (FRAG-PATTERTECH-HOUSE-09).
Prevents vestibular harm on a page that passes the query check. Basis:
decision, on a practitioner synthesis rather than a trial, so the
discrimination rule transfers and no numeric threshold does.

**H5. Reading matter never animates and never glows.** `has_longform`.
Paragraphs, lists, tables and notes arrive already visible, and
body-tier text carries no text shadow. Prevents the
fade-up-on-every-paragraph tell, and prevents a glow being spent where
the dark-register penalty is already largest
(FRAG-PATTERTECH-HOUSE-05). Basis: decision.

**H6. The dark register buys itself back in the smallest type.**
`has_dark_register`. Mono kickers, indices and captions get size, weight
and measured contrast above the floor rather than at it, and are
reviewed on a cheap display. Prevents the house leaning its annotation
voice on the exact condition where positive polarity wins by the most
(FRAG-PATTERTECH-HOUSE-05, FRAG-PATTERTECH-HOUSE-06). Basis:
empirical-evidence. Scope note: acuity and proofreading tasks for adults
with normal or corrected vision under office lighting, not sustained
reading, and some readers with impairments do better dark.

**H7. Figures are positioned from data.** `has_figures`. Scales place
every node, no label or box overlaps a line, connectors join labels to
their nodes, no glow sits on a line, and at most one endpoint accent
marks the datum that matters. Prevents a figure that lies about where a
value sits, which no recall gain buys back
(FRAG-PATTERTECH-HOUSE-03). Basis: local-observation. See
`packs/pattertech-house/guides/GD-HOUSE-004-figure-austerity.md`.

**H8. Every number has exactly one home.**
`adopts_pattertech_house`. All house alphas, durations, duty cycles,
measures, layer counts and weight budgets live in
`packs/pattertech-house/refs/BUDGETS.md` and are cited, never restated.
Prevents the failure that produced this pack: two documents carrying the
same budget, drifting, and an agent picking whichever it read last.
Basis: decision.

**The conduit contradiction, resolved.** The v1 archive held one number
twice: `archive/v1/doctrine/web-design/foundations/LIGHT.md` and
`archive/v1/doctrine/web-design/foundations/MOTION.md` both stated a
conduit duty cycle of eighteen seconds or longer. The newer argued
ruling in WG-WEB-005, recorded against the v4 recalibration, relaxed it
after the verdict that v3 sat on the wrong side of the line between
elegant and invisible. The newer ruling wins, the relaxed figure is
written once in `packs/pattertech-house/refs/BUDGETS.md`, and the older
number is history.

## Defaults

Followed unless the lock-book records a different choice.

- **Dark-first, single register, with a formal surface ladder.** A light
  register is a supported variant when one is wanted, never a promise
  made in passing (FRAG-PATTERTECH-HOUSE-06). Reason: the identity is
  emitted light and the maintenance budget is one person.
- **The full graded light system for a luminous brand, fields only
  otherwise.** Reason: the recorded rulings show both failure directions,
  decoration and absence, and posture is the dial between them. See
  `packs/pattertech-house/guides/GD-HOUSE-001-light-posture.md`.
- **A surface ladder of four to six steps, derived in a perceptually
  uniform space.** Hold chroma and hue, step lightness evenly
  (FRAG-PATTERTECH-HOUSE-12). Reason: hexadecimal ladders go invisible at
  one end and jump at the other, the usual cause of a grey-on-grey ladder
  nobody can see.
- **A reading measure at the low end of the usual advice.** Reason: near
  fifty-five characters gave the best comprehension against narrower and
  much longer measures (FRAG-PATTERTECH-HOUSE-04). That is a choice about
  which variable is optimised, not a fact about reading: later work
  reports faster reading and stronger preference at longer measures.
  Scope note: cathode-ray displays, 2001 typography, scrolled text.
- **Three type roles, three families as the ceiling**, with scale
  contrast spent before any decoration. Reason: the mono annotation voice
  separates an editorial-technical surface from a template.
- **One delegated pointer listener for surface reactivity**, fine
  pointers only, components opting in with one attribute. Reason: it is
  one small file, and the page must stand complete on touch anyway.
- **Spend the design budget on the first screen.** Appeal judgements form
  in about fifty milliseconds and are stable on re-exposure
  (FRAG-PATTERTECH-HOUSE-14). Scope note: mid-2000s homepages, appeal
  ratings only, a student population, and no measure of whether the
  judgement is correct or survives use, so it never justifies ornament
  that costs comprehension.
- **Platform hygiene.** Line-break quality is a hint rather than a
  dependency, and balance belongs on short display lines rather than
  paragraphs (FRAG-PATTERTECH-HOUSE-11). Animated custom properties are
  registered once in the token layer, because an unregistered angle or
  colour is untyped and the animation silently does nothing
  (FRAG-PATTERTECH-HOUSE-10).

## Preferences

Taste, ours, and not portable. Depart without asking.

- Cyan as the live accent, with the Cherenkov story behind it, and amber
  as the authority and quote voice. Two accents with meanings beat five
  without, and mono indices carry the accent rather than grey.
- The andon line: one accent hairline across the top of the chrome, and
  a quiet header call to action to pay for it.
- Plate numbering as a mono figure number joined to its caption by a
  short hairline, and the reticle as four corner ticks around a single
  calibrated artefact.
- A journal index rather than a card grid on hubs, so two entries read as
  a curated record rather than a thin feed.
- A colophon rather than a closing call-to-action slab, written fresh per
  page, and one warm interlude per long read, spent on the thesis moment.

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| How much light does this surface carry | Which tiers are enabled and how loud the dimmer sits | `packs/pattertech-house/guides/GD-HOUSE-001-light-posture.md` |
| Which container does this content take | Ledger, plaque, panel, table or prose | `packs/pattertech-house/guides/GD-HOUSE-002-container-choice.md` |
| Which polarity register does the surface take | Dark, light, dual or mixed, and what each costs | `packs/pattertech-house/guides/GD-HOUSE-003-polarity-register.md` |
| How austere is this figure | Whether a figure may carry a distinguishing device | `packs/pattertech-house/guides/GD-HOUSE-004-figure-austerity.md` |
| Should the surface answer presence | Inert, hover-only or field-reactive | WG-WEB-011, carried unchanged |

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
  recall (FRAG-PATTERTECH-HOUSE-03), so the house may never claim that
  restraint improves comprehension. Scope note: one study, small sample,
  one illustrator's hand-drawn style, static print-like charts, no
  interaction and no accessibility measurement. The split the pack takes
  is by job, argued in GD-HOUSE-004.
- **Contrast maths is contested and the pack refuses to pick.** A
  perceptual model argues that a ratio quoted for light text on a dark
  ground misdescribes what a reader sees (FRAG-PATTERTECH-HOUSE-01), and
  it was removed from the successor standard's draft in 2023 with no
  replacement chosen (FRAG-PATTERTECH-HOUSE-02). WCAG 2.2 AA stays the
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
