# Layout and grid

How pages hold together. Doctrine 3 (structure over memory) and 6 (editorial
asymmetry) apply.

## The reading grid (the anti-drift core)

Long-form content lays out on a CSS grid with named columns:

```
[full ── [wide ── [ reading ] ── wide] ── full]
```

- Every direct child sits in the reading measure **by default**.
- A block goes wider only by opting in (`bleed-wide`, `bleed-full`).
- Vertical rhythm is the grid `row-gap`; blocks never set their own vertical
  margins.
- Shared components are width-agnostic: they never carry `max-w-*`, so they
  are correct wherever they are dropped.

This single structure removes the two commonest layout bugs (a component
wider than the prose, and margin-collapsing rhythm drift) by construction.
PatterTech's `.prose-grid` is the reference implementation.

## Measures

Three measures cover everything: reading (~48rem), wide (~56rem, for figures,
stat rows, grids, carousels), full (~72rem, section width). Body text and
videos never leave the reading measure.

## Marked sections and the hanging index

General pages are a sequence of sections, each opened with annotation
furniture (index + hairline + kicker + title, flush left). On large screens
the mono index hangs into a reserved left rail (implemented as extra left
padding on the section container plus absolute positioning of the index off
the content edge), the way a clause number juts into the margin of a
technical document. Below the breakpoint the index joins the annotation row.

## Containers ladder

Page container widths come in three steps (narrow/default/wide); pick per
page, never per block. Horizontal padding is constant; the rail padding is
additive on marked sections.

## Mobile law

- No element may cause horizontal page scroll at 375px; this is a merge gate,
  verified by script, not by eye.
- Diagrams reflow (stack vertically) rather than shrink or scroll.
- Display type steps down with breakpoints; body size holds.
- Never disable zoom.
