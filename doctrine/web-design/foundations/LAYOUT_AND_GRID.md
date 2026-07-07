---
summary: The reading grid, measures and bleeds that kill drift
type: foundation
tags: [web, layout]
---

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
- **A bleed means the same width in every wrapper.** Cap the full column at
  the full measure with outer `1fr` tracks outside `[full-start]`; without
  the cap, `full` inherits whatever container the grid happens to sit in,
  and the same component renders at different widths on one page (the
  PatterTech chapter-six carousel, 2026-07). True edge-to-edge bands are
  composed outside the grid as their own monuments, never through a bleed.
- Vertical rhythm is the grid `row-gap`; blocks never set their own vertical
  margins.
- Shared components are width-agnostic: they never carry `max-w-*`, so they
  are correct wherever they are dropped.
- Never put auto margins on a direct grid child. Auto margins defeat the
  default stretch, the child shrinks to fit its content, and a box whose
  only children are absolutely positioned shrinks to a border shell (the
  PatterTech 2px video player, 2026-07). Components own their inner
  centring; the grid owns the child's width.

This single structure removes the commonest layout bugs (a component wider
than the prose, margin-collapsing rhythm drift, wrapper-dependent bleeds) by
construction. PatterTech's `.prose-grid` is the reference implementation.

## Measures

Three measures cover everything: reading (~48rem), wide (~56rem, for figures
and stat rows), full (~72rem, the cap of the full bleed). Body text, videos
and carousels never leave the reading measure: media is a citation
(patterns/MEDIA.md, WG-WEB-014).

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
