# Worked example: the PatterTech website redesign (2026-07)

The project that produced this module. Repo: `PatterTech_Website` (its
`docs/DESIGN_SYSTEM.md` is the lock-in). The design language is called "the
instrument and the journal".

## The diagnosis

The site was well-built and consistent, and still read as AI-generated past
the hero. The craft was fine; the vocabulary was generic. Every page answered
every layout question the same way: centred mono eyebrow with a pulsing dot,
big heading, muted lead, a grid of rounded icon-tile cards, a glowing CTA
slab, repeated five to seven times per page on one flat near-black void, with
decorative glow (glow-text stats, gradient text, button glow, hover sheens,
per-paragraph scroll reveals) as the only ornament. That exact formula is the
house style of AI site generators, so clean execution could not rescue it.

Meanwhile the genuinely distinctive assets never left their frames: a canvas
hero, an animated energy schematic, a diagram kit with mono labels, hairline
connectors and node dots, a kanji glossary with audio, branded social cards,
and writing with an actual voice.

## The move

Promote the diagram annotation language to the whole page, and let
typography and editorial asymmetry replace the card grid:

- Section marks with hanging mono indices replaced the centred eyebrow
  formula; chapters hang their numbers in the reading gutter with a tick.
- The universal card was retired for a container vocabulary: ledgers for
  facts, plaques for numbers, quiet panels for self-contained things, prose
  for reading matter, interlude bands for pacing.
- Glow became semantic: only the animated Logomark, the hero shimmer and a
  live status dot may glow. Buttons, cards and stats went quiet.
- A formal surface ladder (void -> surface -> surface-2 -> surface-3 ->
  ember) gave 20,000px reads a tonal journey; each piece gets one warm
  interlude, spent on its thesis moment.
- Figures gained plate numbers ("Fig. 01") with annotated captions; the
  research hub became a numbered journal index; every page now closes with a
  quiet colophon written fresh, threading to the next piece.
- The chrome gained one motif: a single cherenkov hairline across the top of
  every page (the andon line), and the header CTA went quiet to pay for it.

## The numbers

- Article image transfer after a full scroll: ~34MB potential -> 0.33MB
  measured (WG-008 ruling; 58 committed variants totalling 2.6MB).
- The og:image went from a 1.08MB PNG to a 34KB JPG.
- Reveal went from a motion-library wrapper (with an SSR hydration mismatch
  warning on every page) to CSS + IntersectionObserver with a
  `@media (scripting: enabled)` guard: no mismatch, no bundle cost, readable
  without JavaScript.
- Every route passes the 375px overflow gate; lint, tests, build and the
  capture-toolkit smoke all green through five migration phases, each of
  which left the build shippable.

## What to steal for the next project

The method more than the pixels: find what the project is already excellent
at (here, the diagrams), name it as the signature motif, and promote its
vocabulary everywhere; then delete every treatment that pattern-matches to
template output and let structure do the talking. The wargames record how
each fork was ruled (WG-001 A, WG-003 throughout, WG-004 B, WG-005, WG-007 A,
WG-008 A, WG-009 B, WG-010).

## v3: the Cherenkov principle (2026-07)

The owner's verdict on v2: much closer and genuinely unique, but "Teletext"
and robotic. The de-glow had over-corrected; a brand whose story is emitted
light had been starved of light. He supplied the narrative brief that now
anchors the lock-in: total ambition behind a calm mask; energy gathered until
the momentum cannot be stopped; a fury that burns magnificently and
illuminates everything around it; power that cannot be denied yet cannot
exactly be placed. Themes: physics, nuclear (Cherenkov), electricity and
circuits, cosmology and nebulae, neural networks.

The reframe: the v2 structure was never the aesthetic, it was the containment
vessel; v3 let the glow through as a graded system (foundations/LIGHT.md).
Fields (nebular strata breathing on interludes, one warm pillars moment per
piece, two seams on home), conduits (the header line is live, every
Colophon's rule charges on reveal, the reading-progress bar carries a bright
head), bloom (one delegated listener; rows, panels, buttons and controls
answer the cursor), radiance (refined neon on buttons, nav and focus;
monuments radiate; diagram dots glow; the structure diagram lights its
circuit paths on hover), plus ignite on every reveal and a glint when
counters complete. The Teletext edge was also typographic: mono tracking
came down from 0.28em to 0.2em, the footer meta returned to the text face,
and panels regained a quiet gradient surface with a standing top light.

Rulings recorded this round: WG-005 -> C (the budget is a dimmer, not a
switch); WG-011 -> C (field-reactive, fine pointers only); WG-012 -> A
(generated light only; the brand's light must be computed, like Cherenkov
radiation itself). The lesson that earned its own doctrine edit: restraint
executed as absence reads robotic; execute restraint as containment.
