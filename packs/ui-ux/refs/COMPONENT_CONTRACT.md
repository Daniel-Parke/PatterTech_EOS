---
summary: What a shared component owes its consumers, states manifest, pattern map and the admission gate
kind: fact
scope: estate
sources: [EV-0028, EV-0029, EV-0066, EV-0103, EV-0232, EV-0234, EV-0239]
volatility: slow
review: 2027-10
type: implementation
tags: [web, a11y, tooling]
---

# Component contract

Reference for PACK.md B4 and B7. A component is a behaviour promise
with a look attached, and only the behaviour half is portable.

## The states manifest

Every component names and renders six states: focus, hover, active,
disabled, loading and error. The manifest is exported alongside the
component so a test can walk it.

| State | What it must communicate |
| --- | --- |
| focus | which control the keyboard is on, visibly, always |
| hover | that the thing is operable, for pointer users |
| active | that the press registered |
| disabled | that it is unavailable, and ideally why, without relying on colour |
| loading | that work is in progress, announced not just spun |
| error | what went wrong and what to do, in text |

The reason is a standoff of weak evidence rather than a proven law.
One argument says stripping visual signifiers costs discoverability
(EV-0234, anecdotal, 2015). The other says emphasis through size,
shape, containment and colour speeds target finding (EV-0232,
vendor-run, unpublished). They point the same way from opposite
directions, so the estate takes the cheap precaution: whatever a visual
style removes, the state contract pays back.

## Pattern map

Each interactive component records:

- the authoring-practices pattern it implements, or the deviation and
  why (EV-0028, EV-0029),
- the keys it answers and the state change each produces,
- the roles, states and properties it sets, and when,
- the focus management rule on open, close and completion.

A headless primitive library supplies most of this and holds no visual
opinion (EV-0066), which is why the default in GD-UIUX-002 is to take
behaviour from one and own the look.

## Admission gate

A shared kit stays small on purpose (EV-0239). Before a component is
admitted:

- name at least two surfaces that need it, with the use in each,
- show it cannot be composed from what already exists,
- state the pattern it implements and the tests that pin it,
- state who maintains it.

Public-service systems run a heavier version of this gate with
published criteria and a community backlog (EV-0103). That pace suits a
standing team; an editorial or product team may want a lighter gate and
should say so rather than skip it silently.

## Composition rules that survive a restyle

- Shared components are width-agnostic: they carry no maximum width and
  are correct wherever they are dropped.
- Components consume semantic token names, never primitives and never
  raw values.
- A component tints; it does not restyle itself per brand. Accent maps
  are passed in from one registered module.
- Behaviour lives in one module path, shared. Two surfaces with
  different philosophies import the same behaviour and different
  presentation.
- A component that renders differently under reduced motion still
  renders the same content.
