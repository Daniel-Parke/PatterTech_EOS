---
summary: One token source, three layers, generated outputs and the guards that stop values drifting
kind: fact
scope: estate
sources: [EV-0030, EV-0064, EV-0065, EV-0227]
volatility: slow
review: on-change-of:DTCG-format-module
type: implementation
tags: [tooling, brand, colour]
---

# Token pipeline

Reference for PACK.md B6 and WG-UIUX-006.

## Shape

The community format defines a token as a named value with a type,
supports aliasing one token to another, and groups tokens into a tree
(EV-0030). The format reached a dated spec release in late 2025 and is
still moving, so pin the version you validate against and re-read on
each release.

Three layers, one source:

1. **Primitive**: raw values named for what they are.
2. **Semantic**: what a value means in context, for example surface
   step, rule, text-dim, block-gap. Components consume this layer.
3. **Component**: the rare per-component variable, always fed from the
   semantic layer or a registered accent map.

Public-sector practice adds a sharper rule: consumers reach tokens
through functions and one settings layer, so the structure stays
invariant while the palette varies (EV-0064). That is what makes a
rebrand a value change rather than a rename.

## Generation

A generator reads the source and writes each platform's output
(EV-0065): custom properties, native resources, documentation tables,
whatever consumes values. Three rules follow:

- Outputs are build artefacts. Editing one is a defect, and the next
  build reverts it.
- Regeneration from source produces no diff. That is the check, and it
  is one command.
- Outputs for at least the platforms actually in use exist and are
  committed or built in CI, so a reviewer can see what changed. Where
  only one platform consumes values today, generate a second output
  anyway, a documentation table being the cheapest, so the pipeline's
  portability is proven rather than assumed.

Enterprise systems ship tokens, components, icons and grid in one
versioned repository so consumers upgrade the whole set together
(EV-0227). Adopting that shape is a choice in WG-UIUX-004, not a
requirement here.

## Guards against value drift

An import-boundary rule cannot see a value re-typed inside a component,
so three mechanical defences carry over from v1 doctrine:

- **The twin scale.** Where the same value must exist on both sides of
  a language boundary, one test pins each pair so the two sides cannot
  drift apart.
- **The no-re-literal guard.** A test scans source for any raw value
  the scale already names and fails the build, with a written allowlist
  for the places a literal is the point: the token source itself, brand
  artwork, self-contained exports.
- **Generic never wears brand.** A shared component reads the house
  default accent. Where a house value and a brand value coincide, the
  coincidence is recorded in a comment, so a rebrand of either side
  stays a decision.

## Two surfaces, one source

Different philosophies do not need different token sources. They
consume different semantic sets over the same primitives: a denser
spacing set and a tighter type scale for an operations surface, a
generous set for a service flow. The primitives, the aliasing and the
generator are shared, so a colour correction reaches both surfaces in
one commit while the two go on looking nothing alike.
