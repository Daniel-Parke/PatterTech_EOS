---
id: WG-UIUX-002
summary: When native HTML cannot express a required interaction, what custom representation is justified and what equivalent behaviour must it earn?
kind: wargame
type: wargame
tags: [eos, testing, web, wargame]
scenario_modes: [conflict, exception, gap]
applicable_doctrines: [DOC-UIUX-001, DOC-UIUX-002, DOC-UIUX-003, DOC-UIUX-007, DOC-UIUX-015, DOC-UIUX-023]
gap_domain: semantic-custom-interaction
applies_when: [has_user_interface]
engages_when: [requires_non_semantic_custom_control]
consequence: high
relations: [DREL-UIUX-002]
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0027, EV-0575, EV-0576, EV-0577]
review: on-change-of:WCAG-2.2
lifecycle: active
---

# WG-UIUX-002: Native semantics or custom interaction?

## Decision question and stakes

A required editing, visualisation or spatial task cannot be expressed by one
meaningful native HTML control. Decide how much custom rendering and behaviour
to introduce while preserving an operable, understandable and testable route
for keyboard and assistive-technology users. A visually successful control can
silently exclude users if role, name, state, focus or keyboard behaviour is
missing.

## Doctrines or coverage gap under pressure

- `DOC-UIUX-001`, `DOC-UIUX-002`, `DOC-UIUX-003` and `DOC-UIUX-007` keep
  conformance explicit, gate cheap failures, require mapped interaction
  behaviour and demand real-browser evidence.
- `DOC-UIUX-015` keeps content visible without client execution where content
  is the product.
- `DOC-UIUX-023` starts from native semantics and gives a custom exception its
  own keyboard, focus and assistive-technology obligation.
- `DREL-UIUX-002` records the tension between a required custom interaction
  and the native-semantics floor.
- The uncovered domain is `semantic-custom-interaction`.

Binding accessibility Doctrines are not waivable options. If the product
cannot meet them, the result is a blocked design or Doctrine review, not a
Wargame victory.

## Preconditions and engagement triggers

Write the exact user task and the missing native capability. List every state,
operation, input method, focus transition and announcement the interaction
requires. Identify the target browser, operating system, screen reader and
input combinations, plus any non-visual or simplified representation that
could meet the same outcome.

Applicability is `has_user_interface`. Engage when
`requires_non_semantic_custom_control` is true. Mere preference for canvas,
animation or a component library does not settle that predicate.

## Options

### A. Reframe the task with native controls

Split the interaction into links, buttons, inputs, tables, details or other
native elements, even if this changes the visual composition. This inherits
browser semantics and much behaviour. It may make a genuinely spatial or
high-frequency task slow or impossible.

### B. Compose a DOM-backed custom widget

Use native elements where possible, add the permitted roles and properties
for missing semantics, and implement the mapped keyboard and focus pattern.
This preserves an inspectable accessibility tree. Assigning a role does not
create its behaviour, so the team owns the full interaction contract
(EV-0576, EV-0577).

### C. Custom-render the primary surface with an equivalent operable route

Use canvas, WebGL or another custom renderer for the task it uniquely serves,
and provide a synchronised DOM-backed control or alternative representation
for navigation, values, editing and status. This supports dense spatial work
but creates two representations whose state and errors must remain aligned.

### D. Change the product requirement

Remove or narrow the interaction when no implementation can meet the required
outcome and accessibility floor at proportionate risk. This loses feature
scope but avoids shipping an exclusion disguised as an exception.

## Failure premises

### Premortem for A. Reframe the task with native controls

Assume A failed. The accessible route technically worked but turned a frequent
expert task into dozens of operations, causing abandonment or unsafe shortcuts.

### Premortem for B. Compose a DOM-backed custom widget

Assume B failed. Role and name were present, but arrow keys, escape, focus
return, disabled state or live updates differed from the promised pattern. A
unit test passed while browser and assistive-technology behaviour did not.

### Premortem for C. Custom-render the primary surface with an equivalent operable route

Assume C failed. The alternative lagged behind visual state, exposed an
unmanageable stream of nodes, or allowed viewing but not the consequential
edit. Two surfaces doubled defects without providing equivalent outcomes.

### Premortem for D. Change the product requirement

Assume D failed. The requirement was cut without representative users, and a
workable custom route was rejected because the team treated accessibility as a
ban on innovation rather than an engineering obligation.

## Decision rule

Choose A if representative users can complete the task within the recorded
time and error tolerance. Choose B when native elements can carry most of the
structure and the remaining behaviour maps to a tested pattern. Choose C only
when the custom renderer is necessary for the named task and the equivalent
route completes the same material outcome, not merely reads a summary. Choose
D when B and C cannot satisfy the binding floor or the maintenance owner and
test matrix do not exist.

No option ships until keyboard-only completion, visible focus, accessibility
tree and named browser-assistive-technology checks pass for the hardest state.

## Safe default

Native elements and behaviour are the safe product default. Once the pressure
fact is proven true, B is the safest experimental starting point. There is no
safe deployment default for a required non-semantic control without the full
behaviour and representative evidence named above.

## Cheapest discriminating test

Build only the hardest representative interaction state. Inspect its
accessibility tree, then complete the task keyboard-only, including entry,
operation, cancellation, error and focus return. If custom behaviour remains,
run the named screen-reader and browser pair and compare task outcome with the
visual route. A copied APG example is a starting hypothesis, not a passing
result (EV-0577).

## Fallback, exit and revisit

**Fallback `native-or-readonly-route`:** disable the custom edit and retain a
native, truthful read or submission route while the interaction is repaired.
Do not represent reduced capability as full service.

**Exit condition:** withdraw the custom route when state synchronisation,
keyboard completion, focus, accessible naming or the named assistive test
fails, or when no owner maintains the interaction contract.

**Revisit trigger:** repeat for a new interaction pattern, consequential state,
target browser or assistive-technology combination, or when a native platform
capability becomes sufficient.

## Counter-evidence and transfer limits

ARIA in HTML defines permitted semantics but does not implement keyboard,
focus, styling or usability (EV-0576). APG provides patterns and examples, not
product certification (EV-0577). WCAG cannot cover every disability need
(EV-0027), so conformance alone does not settle representative task success.
Conversely, one user's success does not replace the named criteria. The ruling
applies only to the recorded task, states and target technology combinations.
