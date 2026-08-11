---
summary: The non-web accessibility profile, the unit of conformance, the semantics declaration, clause 11 extras and the audit route
kind: fact
scope: estate
sources: [EV-0027, EV-0104, EV-0235, EV-0236, EV-0370, EV-0371, EV-0385, EV-0387, EV-0388]
volatility: slow
review: on-change-of:EN-301-549-v4-publication
type: ux
tags: [a11y, testing, product]
---

# The non-web accessibility profile

Reference for PACK.md B6 and for GD-NAT-004. This is the profile
`packs/ui-ux/PACK.md` defers to when a surface has no web UI. Read it
alongside `packs/ui-ux/refs/A11Y_FLOOR.md`, which owns the numeric
floors and the web route.

Sources here are readable and not reusable, so everything below is
paraphrase.

## What changes when the surface is an app

**The unit of conformance is a screen or view, not a page**
(EV-0370). A claim is made per screen and aggregated, never
asserted once for the app. Web terms map onto platform terms, and the
criteria that carry most of the weight on a device are the
mobile-shaped ones: orientation, pointer gestures, motion actuation,
dragging movements and target size.

**The reviewable artefact is the semantics declaration in code, not a
screenshot** (EV-0387). What a reviewer reads:

- Content descriptions on every interactive element, and null
  descriptions marking decoration explicitly.
- Descendant merging, so a composite reads as one thing rather than
  five.
- Explicit heading semantics and pane titles, which are how a screen
  reader user navigates structure.
- Custom actions carrying human labels, not identifiers.
- State exposed as state, not painted as colour.

**Clause 11 adds obligations WCAG never states** (EV-0371).
Chiefly two: interoperability with the platform's assistive technology,
and support for the user's own preference settings. A native app that
only passes a WCAG mapping is still short of the standard. The platform
guidance treats both as implicit platform behaviour rather than as a
developer obligation, which is exactly why it has to be checked
deliberately once you stop using platform controls.

## Where the numbers come from

The platform accessibility guidance publishes no numeric thresholds at
all, no touch target minimum and no contrast ratio (EV-0387).
The measurable floor comes from WCAG 2.2 (EV-0027) through the mobile
mapping (EV-0370). Two cautions on that route:

- The mapping is a Group Draft Note, explicitly informative, not
  endorsed, replaceable at any time, and covering Level A and AA only.
  It translates. It does not oblige.
- Closed functionality, a kiosk or a locked-down device, is
  acknowledged as a gap in the mapping and needs its own argument.

## The audit route

An automated accessibility audit exists inside the platform test runner
and can be scoped to an app, a screen or a single element with
selectable audit types, covering missing labels, clipped text, contrast
and dynamic type support (EV-0388). That is what makes the gate
a normal failing test rather than a manual ritual.

Three limits, stated because the gate is only as good as its honesty:

- The primary sources for that capability could not be fetched at
  inspection and the description rests partly on secondary write-ups.
  Re-verify against the current platform test reference before quoting
  it.
- No coverage figure is published for it. On the web the equivalent
  figure is contested between roughly 57 per cent and roughly a third
  (EV-0236, EV-0104). Here there is no number to argue about, so the
  manual verdict list carries more weight, not less.
- No detected errors does not mean accessible. The web census says so
  outright (EV-0235), and the caution applies at least as strongly
  where no coverage figure exists.

The verdict file is therefore load-bearing. Every item the audit cannot
decide gets a written verdict naming what was inspected and the
conclusion. The file's entry count equals the audit's undecided count,
and that equality is a check a script can run.

## Architecture interacts with this

Under GD-NAT-001 option C, the framework draws its own widgets, so
platform conventions, accessibility services and system controls arrive
only as far as the framework has reimplemented them (EV-0385).
That does not make the option wrong. It makes the accessibility budget
a line item you have chosen to pay in your own code rather than inherit
from the toolkit, and the semantics declaration becomes the whole story
rather than a supplement to platform behaviour.

Under options A, B and D the platform toolkit supplies the baseline,
which is why PACK.md D8 starts from the platform's own control.

## Statutory reach

EN 301 549 binds through the European Accessibility Act and public
sector procurement, not everywhere. The version in force at the cutoff
is V3.2.1 (2021-03) and it references an older WCAG level than the
mobile mapping targets, so an app built to WCAG 2.2 is ahead of the
binding standard rather than behind it. A v4.1.x revision aligning the
clauses with WCAG 2.2 was reported in approval and was not published
when checked (EV-0371). Recheck on publication before restating
any of this.
