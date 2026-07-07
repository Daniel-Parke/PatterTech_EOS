---
summary: How much may this project move?
type: wargame
tags: [web, motion]
status: active
review_by: 2027-07
---

# WG-WEB-004: How much may this project move?

## The question

Where does this project sit on the motion spectrum, and which elements get
which class of motion?

## It depends on

- Whether the brand owns signature animated pieces worth spending the whole
  budget on.
- Audience context: an investor skimming a whitepaper tolerates less theatre
  than a visitor to a creative studio.
- Performance floor: every continuous animation costs battery and frames.
- The reading share of the site: the more long-form, the stiller the pages.

## Options

### A. Still (no continuous motion)
Functional feedback only. Right for document-heavy or compliance contexts.

### B. Concentrated (the house default)
All continuous motion concentrated in named signature visuals; furniture
reveals once; reading matter still. The site feels alive exactly where it is
alive.

### C. Ambient
Background particle fields or drifting gradients on top of B. Costs frames
and can tip into template feel; needs a named justification.

### D. Theatrical
Scroll-linked scenes, parallax, page transitions. Outside doctrine for our
work; a project wanting this must wargame it as an exception with named
costs.

## Decision rule

If the project has signature visuals, choose B (or C only if an ambient
layer genuinely extends the signature system rather than decorating). If it
has none, choose A and invest in typography until a signature piece exists.
Reading matter is still in every option; that part is doctrine, not budget.

## Default

B. Concentrated.

## Worked rulings

- **PatterTech Website (2026-07)**: B with a pre-existing ambient layer (C)
  retained: the particle field is part of the Cherenkov system, not
  decoration. Per-paragraph reveals were removed from the article kit;
  reveals kept for section marks, figures and quotes; the pulsing dot became
  a semantic status-only mark; buttons and panels stopped lifting. Reveal
  was reimplemented as CSS + IntersectionObserver with a
  `@media (scripting: enabled)` guard.
- **PatterTech Website v4 (2026-07)**: B held, with the arrival class made
  louder after the owner's verdict on v3 was "too sparse, or too hard to
  notice". The principle recorded: **motion is event-driven**. Arrival does
  the loud work (headings sweep white-to-cherenkov once as they reveal, rules
  charge once, stat values glint once) and the page stays calm between
  events. One persistent slow traveller class was allowed (12s cycle, at
  most two per page, monuments only). Reading matter stayed still and quiet
  rooms (legal pages) stayed quiet.
