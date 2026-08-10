---
summary: The single canonical home for every PatterTech house number, alphas, durations, measures, counts and weights
kind: fact
scope: brand:pattertech
sources: [EV-0027]
volatility: slow
review: 2028-08
type: implementation
tags: [web, motion, colour, perf, layout]
---

# House budgets

Every number the house uses lives here and nowhere else. Requirement H8
in `packs/pattertech-house/PACK.md` exists because these figures used to
live in two places and drifted. If a guide, a component or a lock-book
wants one of them, it cites this file. A number written twice is a
number that will disagree with itself.

**What these numbers are.** Calibration from one project's eye, not
measurement. They are reproducible because they are written down. A
measurement that contradicts one of them is grounds to change it, and
the change lands here first.

## Light

| Budget | Value | Note |
| --- | --- | --- |
| Field accent alpha | at most about 6 per cent | ambient strata, washes, section seams |
| Field breathe period | 60 to 120 seconds | opacity only |
| Conduit duty cycle | at least about 12 seconds for a loop | the resolved figure, see below |
| Conduit bright core | about 90 pixels on a 1-pixel line, 80 to 90 per cent alpha | |
| Bloom alpha | at most about 10 per cent | fine pointers only |
| Bloom radius | 90 to 250 pixels | |
| Neon on controls | shadow at negative spread, never fill | outer at about 45 per cent, inset at about 25 per cent |
| Monument text shadow | layered at about 25 and 10 per cent alpha | never on body text |
| Ignite overshoot | brightness 1.3 to 1.0 over about 0.5 seconds | no fill mode |
| Heading sweep | one shot, about 1.1 seconds | the one sanctioned paint-property animation |
| Persistent slow-traveller rules | at most 2 per page, about 12 seconds each | monuments only |
| Travelling conduits | 1 per viewport | |
| Warm interlude | 1 per long-form piece | |
| Mono annotation voices | about 2 per viewport region | |
| Pseudo-elements per element | 2, budgeted up front | a third decorated layer ships as a real span |

**Travelling conduit or persistent slow traveller.** Both rows above
describe a moving rule, and the duty cycle is what separates them. A
travelling conduit moves during the first tenth of its cycle and holds
offscreen for the rest, so the light is a passing event: one per
viewport, anywhere. A rule whose core is on screen for most of its
period is a persistent slow traveller, whatever it is called in the
markup: monuments only, at most two per page. Read the keyframe
percentages rather than the animation name, because the two are the
same CSS apart from where the stops sit.

**The resolved conduit figure.** The v1 archive stated eighteen seconds
or longer in two foundation documents. The newer argued ruling in
WG-WEB-005, recorded against the v4 recalibration, relaxed it to twelve
seconds or longer after the surface read as too quiet on interior pages.
The newer argued ruling wins. Twelve is the house number and eighteen is
history.

## Motion

| Budget | Value |
| --- | --- |
| Functional and hover transitions | 0.2 to 0.4 seconds |
| Easing curves per project | 1, tokenised |
| Reading matter motion | none, at any budget |
| Animatable properties | transform, opacity, one-shot filter, shadow transitions on small elements |

## Type and measure

| Budget | Value |
| --- | --- |
| Body size | 1.0 to 1.1 rem |
| Reading measure | about 48 rem, near 55 to 70 characters |
| Wide measure | about 56 rem, figures and stat rows |
| Full measure | about 72 rem, the cap of the full bleed |
| Body leading | 1.7 to 1.75 |
| Display leading | 1.05 to 1.15 |
| Display ladder, desktop first step | 3 to 4.5 rem, stepping to about 2.25 rem on mobile |
| Kicker size | about 0.7 rem, uppercase |
| Kicker tracking | 0.2 to 0.3 em |
| Lead paragraph cap | about 65 characters |
| Font families | 3, subset, swap on load |
| Weights | 1 for display, regular plus 1 emphasis for text |

## Colour and contrast

| Budget | Value |
| --- | --- |
| Surface ladder steps | 4 to 6, derived in a perceptually uniform space |
| Accents with meaning | 1 live accent, 1 counter-accent |
| Headings, measured on ground | about 17 to 1 |
| Long-form body | about 13 to 1 |
| Secondary interface text | about 7 to 1 |
| Captions | the AA floor, which binds from `packs/ui-ux/PACK.md` (EV-0027) |

The three upper tiers are house targets sitting above the floor. Only
the floor is a conformance matter, and only the floor may be claimed.

## Layout

| Budget | Value |
| --- | --- |
| Page container steps | 3, chosen per page and never per block |
| Mobile gutter | one value, decided once, bound everywhere it is encoded |
| Horizontal scroll at 375 pixels | none, verified by script |
| Diagram label clearance | at least 6 pixels from any line |
| Endpoint accents per figure | at most 1 |

## Media and weight

| Budget | Value |
| --- | --- |
| Single image on the wire | about 150 KB |
| Page image transfer after a full scroll | about 1.5 MB |
| First viewport | about 500 KB |
| Third-party scripts | analytics only, embeds as facades until clicked |
| Image variants | committed, web-sized, with intrinsic dimensions and lazy loading |

## Change log for these numbers

- **2026-07**: conduit duty cycle relaxed from about 18 seconds to about
  12 seconds, argued in WG-WEB-005 against the v4 read.
- **2026-08**: all figures gathered here from the v1 foundations, which
  are now history under `archive/v1-final:doctrine/web-design`.
