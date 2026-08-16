---
summary: The pack applied end to end, a service task flow and an operations dashboard sharing one token source and one behaviour layer
kind: example
scope: estate
type: example
tags: [web, a11y, layout]
---

# EX-UIUX-001: two surfaces, one spine

The situation. One repository must ship two surfaces for the same
venture: a public task flow where a citizen completes a three-field
form, and an internal operations dashboard where a duty engineer
answers one question during an incident. Same team, same tokens, same
components, two audiences with nothing in common.

This is the pack applied in order, with the decisions written down as
they were taken.

## 1. Activation

Both surfaces have a web UI, so the predicates `has_web_ui`,
`has_user_interface`, `has_forms` (service only), `has_shared_components`
and `has_design_tokens` are true. There is no statutory duty on the
dashboard and there is one on the service flow, which changes the
assurance level and nothing else.

## 2. Philosophy, one per surface

Ruled with WG-UIUX-003 before any pixel work, and recorded in a
decisions file at the repository root.

- **Service flow: content-first public service (option A).** Triggers:
  the user cannot avoid the surface, the task is a form, and the cost
  of failure is exclusion. Evidence cited: EV-0062, EV-0063.
  Consequences accepted: it will look plain, and admitting a new
  component will be slow.
- **Dashboard: data-heavy dashboard (option F).** Triggers: an
  operator under time pressure, one named question, a long session.
  Evidence cited: EV-0240. Consequences accepted: it answers fewer
  questions than a general explorer would, and it needs written panel
  context maintained.

The runner-up for the dashboard was dense enterprise (option B), turned
down because there is one operations surface, not twenty, so a versioned
cross-product kit would cost more than it returns.

## 3. Components

WG-UIUX-004 default taken: headless primitives with an own visual
layer. One shared module holds every interactive component, and both
surfaces import from it. A check greps both surface directories for
component implementations and fails on any duplicate, so the temptation
to fork a button for the dashboard is caught in review.

Each component carries its pattern map and its states manifest, per the
component contract reference. The error summary on the form is a real
pattern with focus management on submit, not a styled div.

## 4. Tokens

WG-UIUX-006 default taken: one source file in the community format,
two generated platform outputs, generation asserted to produce no diff
against a fresh build. The two surfaces consume different semantic sets
over the same primitives: the service flow takes a generous spacing set
and a larger base size; the dashboard takes a compressed set and a
smaller base with more steps. One colour correction reaches both in one
commit.

## 5. Assurance

WG-UIUX-005 option C for both, since both carry custom interactive
components. The service flow also has a statutory duty, so an audit is
scheduled before any public conformance statement, which is option D
arriving later rather than a different build.

What runs on every change:

- the scanner in a real browser over every route, tags pinned to the
  claimed version and levels, zero violations,
- a manual verdict file whose entry count equals the scanner's
  incomplete count,
- six individual assertions for contrast, image alternatives, form
  labels, empty links, empty buttons and page language,
- a keyboard contract test per component asserting the keys and the
  state change each produces, not that the component rendered,
- a states manifest test walking all six states per component,
- no overlay script in either build output.

## 6. Proving the two surfaces really differ

The philosophy record is only worth something if the surfaces diverge.
Three measured differences, each with a stated threshold in the
repository:

| Measure | Service flow | Dashboard |
| --- | --- | --- |
| base type size and scale steps | larger base, fewer steps | smaller base, more steps |
| spacing density | generous, one task per screen | compressed, four panels per screen |
| component inventory | small, form and content parts | panels, legends, time controls |

A single house style cannot satisfy both, which is the point of the
pluralism contract.

## 7. What went in the record

The decisions file names, per surface: the philosophy, the evidence
ids, the triggers that decided it, the runner-up, and what was given up
by not taking it. It is validated against a schema so a missing
evidence id fails the build rather than passing review unnoticed.

## What this example does not show

It does not show a native platform surface, where the platform profile
activates and the system control is the starting point. It does not
show a rebrand, which is where the token layering earns its keep. It
does not show an expressive consumer surface, which would take option C
in WG-UIUX-003 and would be the harder case for the states contract.
