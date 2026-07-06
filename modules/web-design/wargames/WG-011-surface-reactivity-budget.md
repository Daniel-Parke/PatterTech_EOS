# WG-011: Should the surface react to presence?

status: active
review_by: 2027-07

## The question

Does the site respond to the user's cursor beyond classic hover states, and
if so, how far does the reactivity go?

## It depends on

- The desired register: "alive to presence" is a strong futurist signal;
  formal or archival sites may want stillness.
- Touch share: cursor-reactive effects vanish on touch, so the design must
  stand without them.
- Performance floor: a single delegated listener is cheap; per-component
  listeners and canvas-tracking effects are not.
- Whether the interactivity carries meaning (a field answering a charge) or
  is a gimmick (things wobbling for attention).

## Options

### A. Inert
No hover states beyond colour changes. Reads archival.

### B. Hover-state only
Rich but positionless hover treatments (border brighten, arrow nudge, border
beams). Safe, classic, slightly less alive.

### C. Field-reactive
One delegated pointer listener sets local coordinates on the `[data-bloom]`
element under the cursor; CSS paints a soft radial there. Rows, panels,
buttons and controls answer presence. Fine pointers only; touch and reduced
motion opt out; components opt in with one attribute so server components
stay server components.

### D. Fully simulated
Cursor-tracking canvases, magnetic elements, distortion. Expensive, showy,
and it moves what the user is trying to read: off-doctrine.

## Decision rule

If the brand's philosophy includes responsiveness or field physics, choose C
with B's treatments as its base layer (the beam and brightening still play on
hover). Choose B when the team cannot own a shared listener's upkeep or the
audience skews formal. Never D. Whatever the ruling, the site must feel
complete on touch: fields, conduits and ignition carry the life there.

## Default

C for house projects; it is one small file and one attribute per component.

## Worked rulings

- **PatterTech Website v3 (2026-07)**: C. `BloomField` (one rAF-throttled
  delegated listener in the root layout) + `[data-bloom]` on ledger rows,
  journal entries, panels, buttons, carousel arrows and zoom controls; nav
  links excluded (their underline pseudo-element is spoken for). Touch keeps
  fields, conduits and ignite.
