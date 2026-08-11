---
summary: Structural layout rules that hold under any visual philosophy, measures, bleeds, rhythm and density
kind: fact
scope: estate
sources: [EV-0062, EV-0239, EV-0240]
volatility: slow
review: 2027-11
type: foundation
tags: [layout, density, typography]
---

# Layout and measure

Reference for the layout preference in PACK.md. Everything here is
structure, so it survives a change of philosophy. The specific numbers
are examples from v1 practice, not house law.

## The reading grid

Long-form and task content lays out on a grid with named columns: a
reading column inside a wider column inside a full column, with outer
tracks capping the full width.

- Every direct child sits in the reading measure by default.
- A block goes wider only by opting in.
- A bleed means the same width in every wrapper. Cap the full column
  with outer tracks, or the same component renders at different widths
  on one page depending on where it was dropped.
- True edge-to-edge bands are composed outside the grid, never through
  a bleed.
- Vertical rhythm is the grid row gap. Blocks never set their own
  vertical margins.
- No auto margins on a direct grid child. They defeat the default
  stretch, the child shrinks to its content, and a box whose only
  children are absolutely positioned collapses to a border shell.
- Shared components are width-agnostic and carry no maximum width.

This structure removes the commonest layout defects by construction: a
component wider than the prose it sits in, rhythm drift from collapsing
margins, and wrapper-dependent bleeds.

## Measures

Three measures cover almost everything: a reading measure for prose, a
wider one for figures and stat rows, and a full measure as the cap.
Body text and inline media stay in the reading measure, because media
inside an argument is a citation. In v1 practice these were about 48,
56 and 72 rem; a dense operations surface will want narrower columns
and more of them, and that is the philosophy talking, not a defect.

## Density

Density is chosen with the audience, not inherited. Three answers,
carried forward from v1 practice: skim-first for readers arriving for
the gist, read-first for readers going end to end, reference-first for
people looking one thing up.

Signals worth reading:

- Public-service work pushes toward one thing per page and generous
  targets (EV-0062).
- Editorial work centres measure and typography and keeps the component
  surface small (EV-0239).
- Operations work orders panels as a narrative answering one named
  question, and carries written context in the surface itself
  (EV-0240).

Two surfaces in one estate should differ measurably in type scale,
spacing density and component inventory when their philosophies differ.
If they do not, the philosophy record is decorative.

## Responsive behaviour

- No horizontal page scroll at the narrowest supported width, asserted
  by script on every changed route.
- Text reflows at high zoom without loss of content or function.
- Touch targets are sized for the input the surface actually receives.
- Tables, diagrams and code scroll inside their own container, never by
  scrolling the page.
