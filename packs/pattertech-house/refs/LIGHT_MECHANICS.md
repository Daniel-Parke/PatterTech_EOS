---
summary: How the four light tiers are built, the compositor whitelist, the degradation ladder and the token registration they depend on
kind: fact
scope: brand:pattertech
volatility: slow
sources: [EV-0030, EV-0065]
review: on-change-of:CSS-Masking-Module-Level-1
type: implementation
tags: [web, motion, colour, perf]
review_by: 2028-10
---

# Light mechanics

How the graded light system is built. The posture fork is
`packs/pattertech-house/guides/GD-HOUSE-001-light-posture.md` and every
number is in `packs/pattertech-house/refs/BUDGETS.md`.

## The four tiers

**Field** is potential energy in the environment: page washes, interlude
bands, chosen section seams. **Conduit** is energy moving along
structure: a chrome hairline, a rule that charges as it reveals, the
bright head of a progress bar. **Bloom** is the field disturbed by
presence: rows, panels, buttons and controls answering a cursor.
**Radiance** is the sources themselves: signature visuals, measured neon
on interactive controls, monuments and live status.

The named behaviours are breathe, travel, bloom, ignite, glint and
radiate. Each belongs to exactly one tier, and a component that wants a
behaviour from a tier the posture did not enable does not get it.

## Build patterns

**Fields.** Layered radial strata on a pseudo-element, isolated and
behind the content, breathing by animating opacity alone. Offset the
delay between band variants so they do not synchronise. The warm
pillars read comes from tall narrow radials anchored to the bottom edge.

**Conduits.** A full-size pseudo-element carrying a bright core in a
linear gradient, translated across inside a hidden overflow. The duty
cycle lives in the keyframes: move during the first tenth, hold offscreen
for the rest. One-shot variants gate on the reveal mechanism instead.

**Bloom.** One delegated listener for the whole site, throttled to the
frame, resolving the nearest opted-in ancestor, writing the pointer
position and a flag as custom properties, and clearing on leave. The
paint is pure CSS inside a fine-pointer query. Components opt in with a
single attribute, so server-rendered components stay server-rendered.

**Neon.** Shadow at negative spread, never fill, with an inset
companion, deepening on hover. Focus rings gain a soft outer ring.

**Ignite.** A brightness overshoot settling to normal as revealed
furniture arrives, with no fill mode, because a persistent filter leaves
a containing block on every revealed element.

**Heading sweep.** A clipped-text gradient three times the element's
width, whose two resting windows are the plain text colour, with the
position animated once as the reveal fires. The settled state is
indistinguishable from an unswept heading, so reduced motion lands on the
same pixels instantly. Never combine it with a text shadow, because a
shadow paints over clipped text.

**Border beam.** A conic gradient masked down to the one-pixel ring by
compositing with exclusion, driven by a registered angle. Masking is a
paint-time operation on the whole box, so the animation drives the angle
or a transform underneath a static mask rather than animating the mask
itself (FRAG-PATTERTECH-HOUSE-13). Support is uneven and prefixed in
places, so a masked ring carries a documented fallback, and a masked
decorative element is hidden from assistive technology explicitly.

## The compositor whitelist

Only transform, opacity, one-shot filters, shadow transitions on small
elements, and static background image layers. Nothing that triggers
layout. No continuous filter and no looping background-position
animation. This is mechanical rather than aesthetic: those are the
properties that stay on the compositing stage, and everything else forces
layout or paint on every frame (FRAG-PATTERTECH-HOUSE-07). The whitelist
is conservative rather than exact, because modern engines composite more
than the guidance assumes, and a measurement on target hardware beats the
rule where the two disagree.

Layer promotion is what makes the cheap properties cheap, and each layer
costs memory, so promotion is budgeted rather than sprinkled
(FRAG-PATTERTECH-HOUSE-08). A page putting fields, conduits and blooms on
many elements at once is spending layers, and low-memory phones are the
binding constraint. No published numeric ceiling exists, so the count in
`packs/pattertech-house/refs/BUDGETS.md` is local calibration.

## Token registration

Any effect built on an animated angle, length or colour depends on that
custom property being registered with a declared syntax, initial value
and inheritance behaviour. Without registration the value is untyped and
the animation silently does nothing
(FRAG-PATTERTECH-HOUSE-10). The house declares every animated custom
property in one place, as part of the token layer, alongside the
generated token outputs (EV-0030, EV-0065). The specification is still a
working draft, and registration makes an animation possible rather than
cheap: a registered colour can still drive a repaint every frame.

## Degradation ladder

- **Coarse pointers.** Bloom is lost. Fields, conduits, ignite and
  radiance stay, so a touch surface is complete rather than stripped.
- **Reduced motion.** Everything freezes to static gradients through one
  global block, with the bloom layer removed outright.
- **No scripting.** All content is visible. Reveal hidden states live
  behind a scripting query, and fields and conduits are pure CSS and keep
  working.

Honouring the reduced-motion preference is the floor rather than the
answer, because most readers never set it. The character of the motion is
what makes a surface safe by default: small, local and opacity-led rather
than large-area, parallax or scroll-coupled
(FRAG-PATTERTECH-HOUSE-09).

## Calibration notes

If a screenshot of a single component looks glowing, the tier budget is
blown: light should be visible in the periphery and deniable up close.
The opposite failure is equally real, and the test that settles it is
whether a first-time reader can name a moment on the page. Arrival does
the loud work, so spend one-shot events freely before spending loops.
Repetition turns light back into wallpaper: one warm field moment per
long read, one travelling conduit per viewport, seams on marquee sections
only. Colour is part of the light system, and a page can be starved of
energy by desaturation as surely as by stillness.
