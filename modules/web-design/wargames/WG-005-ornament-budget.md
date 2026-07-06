# WG-005: What may glow, gradient or texture?

status: active
review_by: 2027-07

## The question

Which decorative treatments does the project sanction, and where?

## It depends on

- The signature motif: ornament that extends the motif is identity; ornament
  beside it is noise.
- The register (WG-001): glow only exists on dark grounds.
- How much the brand's story involves light or material texture.

## Options

Treatments, ruled individually rather than as a bundle:

- **Glow / shadow-bloom**: only on live things (semantic ornament, Doctrine
  2). Never on text, buttons or static stats.
- **Gradient text**: at most one animated instance on the hero if the brand
  is luminous; never static gradient text on content.
- **Hover sheens and lifts**: never; the hover affordance is border/rule
  brightening and arrow nudges.
- **Background gradients**: one or two fixed radial washes anchored to the
  page top can set depth; they never move.
- **Noise/texture**: off unless the brand is print-native; then wargame it.
- **Hairlines, ticks, rules**: unlimited; they are structure, not ornament.

## Decision rule

For each treatment ask: is it live, is it the motif, or is it structure? If
none of the three, it does not ship. Record the sanctioned exceptions by name
in the lock-in (there should be one or two, not a list).

## Default

Structure only, plus the project's named signature exceptions.

## Worked rulings

- **PatterTech Website (2026-07)**: sanctioned exceptions are the animated
  Logomark and the hero's `gradient-text-anim`, both animated. Deleted:
  glow-text on stats and wordmark, static gradient text, button glow and
  sheen, card hover lift and sheen, the pulsing eyebrow dot (replaced by a
  status-only dot), the animated divider. The fixed radial Cherenkov washes
  behind the page stayed.
