---
summary: Three token layers and the mirroring contract
type: implementation
tags: [web, tooling, brand]
status: archived
---

# Tokens

Three layers, one source of truth, mirrored deliberately.

## Layers

1. **Primitive**: the raw values (hex colours, rem sizes, easing curves),
   named for what they are (`--color-cherenkov`, `--measure-wide`).
2. **Semantic**: what they mean (`surface ladder step 2`, `rule`, `text-dim`,
   `block-gap`). Components consume semantics, not primitives.
3. **Component**: the rare per-component variable (an accent passed into a
   tinted component), always fed from the semantic layer or a registered
   accent map.

## Rules

- One home for tokens (in the Next profile: `globals.css @theme`); everything
  else consumes.
- **The mirroring contract**: when a token changes, the same commit updates
  the raw-value code mirror, the styleguide swatches, and the design-system
  doc's token table. Drift between these four is a bug, and the styleguide
  makes it visible.
- Never hard-code a value that has a token; never mint a one-off colour in a
  component.
- Accent maps for brand families (venture -> hex) live in one module and are
  passed as props; components tint, they never restyle.
- Name tokens for meaning, not appearance, at the semantic layer (`ember`,
  not `dark-brown`), so a rebrand is a value change, not a rename.

## Guard values, not just imports

A module boundary that walks imports cannot see a value-level leak: a brand's
hex re-typed inside a generic component passes every import rule and quietly
makes the kit wear one venture's colour (the PatterTech Callout, 2026-07,
carried PatterPower's teal as its "info" tone for a month). Three defences,
all mechanical:

- **The twin scale.** Where tokens must exist on both sides of a language
  boundary (CSS custom properties for the cascade, code constants for SVG,
  canvas and inline styles), the twin is deliberate and a test pins each pair
  to the same value, so the two sides cannot drift.
- **The no-re-literal guard.** A test scans source for any raw value the
  scale names and fails the build on it, with a documented allowlist for the
  places a literal is the point (the token file itself, brand artwork,
  self-contained exports). Once a value has a name, writing the value again
  is how hexes go back to agreeing by luck.
- **Generic never wears brand.** A kit tone reads the house default accent;
  a coincidence between a house value and a brand's value is recorded as
  provenance in a comment, so a rebrand of either side is a decision, not an
  accident.
