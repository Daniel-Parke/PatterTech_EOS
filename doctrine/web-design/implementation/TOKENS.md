---
summary: Three token layers and the mirroring contract
type: implementation
tags: [web, tooling, brand]
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
