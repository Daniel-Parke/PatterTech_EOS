---
summary: How much light does this project carry?
type: wargame
tags: [web, colour, motion, brand]
status: active (rewritten 2026-07 after the PatterTech v2 over-correction)
review_by: 2027-07
---

# WG-WEB-005: How much light does this project carry?

## The question

Where does the project sit on the light spectrum, and which tiers of the
light system (foundations/LIGHT.md) does it enable?

## It depends on

- The brand's physics: does its story involve light, energy or emission? A
  luminous brand starved of light reads dead; a paper brand drowned in glow
  reads cheap.
- The audience's tolerance for atmosphere: research readers accept more
  ambience than compliance auditors.
- The performance floor and touch share (fields and conduits are CSS-cheap;
  bloom needs fine pointers; see WG-WEB-011).
- How much of the site is long-form reading (reading matter never animates,
  whatever the budget).

## Options

### A. Structure only
No light beyond signature pieces. Correct for document-heavy, regulatory or
deliberately austere brands. Warning from the worked ruling below: executed
on a luminous brand, this reads Teletext.

### B. Fields only
Ambient strata and washes, nothing travels and nothing reacts. A calm,
atmospheric floor.

### C. The full graded system (fields + conduits + bloom + refined neon)
The Cherenkov posture: environment breathes, structure conducts, surfaces
answer presence, interactive UI carries measured neon. Needs the budgets held
(alphas, duty cycles) or it collapses into v1-style decoration.

### D. Loud
Standing glow on static components, gradient text on content, lifted cards.
Off-doctrine; this is the AI-template look regardless of intent.

## Decision rule

Match the brand's physics: luminous/energetic brand -> C with the budgets
enforced; print-native or austere brand -> A or B. Never D. Within C, scale
by surface: reading-heavy pages leave light in the environment; marketing
pages may spend conduit and bloom more freely. If a single component looks
"glowy" in a screenshot, the budget is blown.

## Default

C, with LIGHT.md's budgets, for any brand whose story involves energy;
B otherwise.

## Worked rulings

- **PatterTech v1 (pre-2026-07)**: unintentional D. Glow-text stats,
  glowing buttons, hover sheens, pulsing dots everywhere; read as an
  AI-generated template despite clean execution.
- **PatterTech v2 (2026-07)**: over-corrected to A ("nothing glows unless
  live"). Structurally excellent and unique, but the owner's verdict was
  "Teletext, robotic". Lesson recorded: **the budget is a dimmer, not a
  switch**; restraint executed as absence reads dead on a brand whose story
  is literally emitted light.
- **PatterTech v3 (2026-07)**: C, "the Cherenkov principle". Fields on
  interludes and two home seams; the header line and Colophon rules as
  conduits; bloom via one delegated listener; refined neon on buttons, nav,
  focus; monuments radiate; body text still never glows; reading matter
  still never animates. This is the house default going forward.
- **PatterTech v4 (2026-07)**: C with the dimmer one step higher. v3 passed
  the laws but failed the owner's read: "there is a fine line between elegant
  and invisible", and v3 sat on the wrong side of it on interior pages, where
  the home hero carried most of the energy. The recalibration: conduit duty
  cycles relaxed from >= ~18s to >= ~12s; a one-shot heading sweep
  (white-to-cherenkov, settling to solid type) on section and page titles;
  mono indices moved from grey to the brand blue by default; one persistent
  slow-traveller rule allowed on monuments (two per page at most). The test
  recorded with it: if a first-time visitor scrolls a page and can name no
  moment, the dimmer is too low; if anything loops busily beside reading
  matter, it is too high.
