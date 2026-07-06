# Colour

How to derive a project's palette. Doctrine 2 (semantic ornament) governs how
colour may behave; WG-001 governs the register (dark, light or dual).

## Principles

- **A surface ladder, not one background.** Define 4-6 surface steps from the
  page ground upward (PatterTech: void -> surface -> surface-2 -> surface-3 ->
  ember) and give each a job. Long pages need a tonal journey; interlude bands
  step up one surface so a 20,000px read does not flatline.
- **One live accent, one counter-accent.** The primary accent belongs to
  live/interactive things and brand moments; the counter-accent (usually warm
  against a cool primary) carries a distinct meaning (PatterTech: amber is the
  quote voice and the authority thread). Two accents with meanings beat five
  accents with none.
- **Text in tiers with measured contrast.** Four tiers: headings (~17:1 on
  ground), long-form body (~13:1), secondary UI (~7:1), captions (AA minimum).
  Record the measured ratios in the lock-in.
- **Accent families for multi-brand sites.** If ventures/products carry their
  own accents, map them in one place and pass them as a prop; components tint,
  they do not restyle.
- **Hairlines are colour too.** Define line/rule tokens; most separation on
  the page should come from them, not from filled boxes.

## Deriving for a new brand

1. Rule on WG-001 (register) first; everything else keys off the ground.
2. Pick the primary accent from the brand story (PatterTech's cyan is
   Cherenkov radiation: light from something genuinely energetic). An accent
   with a story survives; an accent from a palette generator drifts.
3. Build the ladder by mixing the accent's temperature into the ground in
   small steps; verify each step is distinguishable on cheap displays.
4. Derive text tiers against the ground and measure the ratios.
5. Name every token semantically in one file; mirror raw values wherever code
   needs them (see implementation/TOKENS.md).

## Pitfalls

- Gradient text and glow as brand identity (they read as template; if light
  matters to the brand, earn it through one animated signature piece).
- Grey-on-grey ladders with steps nobody can see.
- Accent used for both decoration and meaning until it means nothing.
- Forgetting selection, scrollbar and focus colours; they are part of the
  palette.
