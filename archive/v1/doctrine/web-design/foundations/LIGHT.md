---
summary: The graded light system, field to radiance, with budgets
type: foundation
tags: [web, colour, motion]
status: archived
---

# Light

The light system that makes Doctrine 2 buildable. Extracted from the
PatterTech v3 pass ("the Cherenkov principle": a precise vessel around an
undeniable source; the surface never announces the power, the light escapes
anyway). This is what separates futuristic-and-alive from robotic on one side
and template-glow on the other.

## The four tiers

| Tier | Meaning | Typical carriers | Budget |
| --- | --- | --- | --- |
| **Field** | potential energy in the environment | page background washes, interlude bands, chosen section seams | accent alpha <= ~6%; breathes over 60-120s; generated gradients only |
| **Conduit** | energy moving along structure | a chrome hairline, a rule that charges when revealed, a progress bar's bright head | duty cycle >= ~18s for loops, or event-triggered one-shots |
| **Bloom** | the field disturbed by presence | interactive rows, panels, buttons, controls | alpha <= ~10%, 90-250px radius, fine pointers only |
| **Radiance** | the sources themselves | signature visuals, neon on interactive UI, monuments, live status dots | measured shadows and text-shadows; never on body text |

Named behaviours: **breathe** (field opacity oscillation), **travel** (a
streak crossing a conduit), **bloom** (radial answering the cursor),
**ignite** (a one-shot luminance overshoot as revealed furniture comes
online), **glint** (a single sweep when a counter completes), **radiate**
(standing glow on a source).

## Implementation patterns (proven)

- **Fields**: layered `radial-gradient` strata on a `::before` with
  `isolation: isolate; z-index: -1`; breathe by animating **opacity only**
  (compositor-cheap), never background-position (full repaint). Offset
  `animation-delay` between band variants so they do not sync. Warm "pillars"
  read comes from tall narrow radials anchored to the bottom edge.
- **Conduits**: a full-size `::after` carrying a ~90px bright core in a
  linear-gradient, `transform: translateX(-101% -> 101%)` inside
  `overflow: hidden`; the duty cycle lives in the keyframes (move during the
  first ~10%, hold offscreen for the rest). One-shot variants gate the
  animation on the project's reveal mechanism.
- **Bloom**: ONE delegated listener for the whole site (a client component
  mounted once): rAF-throttled `pointermove`, `closest('[data-bloom]')`, set
  `--bx`/`--by` (percent within the element) and `--bloom: 1`, clear on
  leave. CSS paints the radial on `[data-bloom]::after` inside
  `@media (hover: hover) and (pointer: fine)`. Components opt in with an
  attribute, so server components stay server components.
- **Neon (radiance on UI)**: shadow at negative spread, never fill:
  `box-shadow: 0 0 18px -8px accent45 + inset 0 0 12px -8px accent25`, hover
  deepens. Focus rings gain a soft outer ring. Monument text may carry a
  layered `text-shadow` at ~25%/10% alpha.
- **Ignite**: `reveal.is-shown { animation: brightness(1.3) -> 1 over 0.5s }`
  with NO fill mode (a persistent filter would leave a containing block on
  every revealed element).
- **Heading sweep (one-shot)**: `background-clip: text` over a 300%-wide
  gradient whose two resting windows are plain text colour, with
  `background-position` animated once (~1.1s, `both` fill) as the reveal
  fires. The element keeps clipped text afterwards but shows exactly the
  text colour, so the settled state is indistinguishable from an unswept
  heading; reduced motion lands on the same state instantly. This is the one
  sanctioned exception to the background-position ban below because it is a
  one-shot, not a loop. Never combine with a text-shadow: a shadow paints
  over clipped text.
- **Live rule**: the persistent slow traveller for monuments: a 1px rule
  with a ~35%-wide bright band on a `::before`, `translateX(-120% -> 380%)`
  over ~12s ease-in-out, infinite, inside `overflow: hidden`. Budget: at
  most two per page, monuments only (a colophon rule, a hub-page seam).
- **Pseudo-element allocation**: budget the two pseudos per element up front
  (e.g. panel top-light on `::before`, bloom on `::after`); anything third
  (a border beam) ships as a real decorated span. A border beam is a
  conic-gradient masked to the 1px ring via `mask-composite: exclude` with a
  registered `@property` angle.

## The GPU whitelist

Only `opacity`, `transform`, `filter` (one-shots), `box-shadow`/`text-shadow`
transitions on small elements, and static `background-image` layers. Nothing
that triggers layout; no continuous filter or background-position animation.

## Degradation ladder

- `(hover: none)` / coarse pointers: lose bloom only; fields, conduits,
  ignite and radiance stay.
- `prefers-reduced-motion`: everything freezes to static gradients (a global
  kill block plus `display: none` on the bloom layer).
- No JavaScript: all content visible (reveal hidden states live behind
  `@media (scripting: enabled)`); fields and conduits are pure CSS and keep
  working.

## Calibration notes

- If a screenshot of any single component looks "glowy", the tier budget is
  blown; light should be visible in the periphery and deniable up close.
- The opposite failure is real too (PatterTech v4, 2026-07): there is a fine
  line between elegant and invisible. The test that decides it: if a
  first-time visitor scrolls a page and can name no moment, the dimmer is too
  low; if anything loops busily beside reading matter, it is too high.
- Arrival does the loud work. One-shot events (heading sweeps, rule charges,
  stat glints) may be plainly visible because they happen once, on cue; the
  page stays calm between events. Spend arrival freely before spending loops.
- One warm field moment per long read; one travelling conduit per viewport;
  seams on marquee sections only. Repetition turns light back into wallpaper.
- Colour is part of the light system: mono indices and journal numerals carry
  the brand accent by default, not grey. A page can be starved of energy by
  desaturation as surely as by stillness.
- The mono annotation voice stays quiet alongside the light (tracking ~0.2em,
  roughly two mono voices per viewport region); light replaces the shouting,
  it does not join it.
