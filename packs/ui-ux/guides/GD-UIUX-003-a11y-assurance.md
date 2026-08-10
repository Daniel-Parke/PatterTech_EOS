---
summary: How much accessibility assurance does this surface buy?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0027, EV-0028, EV-0029, EV-0104, EV-0235, EV-0236, EV-0237]
review: on-change-of:WCAG-2.2
type: guide
tags: [a11y, testing, web]
---

# GD-UIUX-003: How much accessibility assurance does this surface buy?

## The question

Automated rules find a minority of accessibility defects, and the
maintainers of the tools say so (EV-0236, EV-0104). The fork is how
much assurance a surface buys on top, and therefore what a passing
build is allowed to claim. This is a budget question with a legal edge,
not a tooling preference.

## It depends on

- **Statutory duty.** Public sector, procurement, or a regulated
  market.
- **Whether the user can go elsewhere.** Exclusion is only a real cost
  where there is no alternative route.
- **Interaction complexity.** A static page and a combobox-heavy
  workflow need different evidence.
- **Rate of change.** A surface rebuilt monthly needs the checks in CI,
  not in an annual audit.
- **What the venture will claim in public.** A conformance statement is
  a claim you must be able to defend.

## Options

### A. Unpinned automated rules only
The default in most repos: run the checker with its whole rule set,
including non-normative best-practice rules, and read a pass as done.
Buys a cheap signal. Costs the meaning of the result, because house
opinion and standard conformance are conflated, and colour contrast
does not even run outside a real browser engine (EV-0236). Named here
as the common practice this pack rejects.

### B. Pinned tags in a real browser, with incomplete triaged
Rule tags pinned to WCAG 2.2 A and AA, run in a real browser engine
over every route, zero violations, and every `incomplete` result given
a written human verdict in a named file (EV-0236). Buys a result that
means one specific thing. Costs a standing triage habit, since the
incomplete list is where the judgement lives.

### C. B plus behaviour and states testing
Adds a keyboard contract test per interactive component against its APG
pattern, tab order, visible focus in computed styles, and an asserted
states manifest (EV-0028, EV-0029). Buys coverage of the class of
defect no scanner sees: a component that renders correctly and cannot
be driven. Costs test authoring per pattern.

### D. C plus assistive-technology and user testing, with an audit
Adds screen reader and magnification passes, testing with disabled
users, and an independent audit before a public conformance claim.
Buys the only evidence that survives challenge. Costs money and
calendar time, and it needs recruiting.

## Decision rule

If a statutory duty applies, or the surface is one people cannot avoid,
or a public conformance statement will be published, choose D. If the
surface is a public product with custom interactive components, choose
C. If it is an internal tool with mostly native controls, choose B.
Never choose A. Overlays are not an option at any level: they cannot
repair labels, alternative text or keyboard access, and sniffing
assistive-technology use exposes disability status without consent
(EV-0237).

## Default

B is the floor for anything with a web UI, and it is binding as B2 and
B3 in PACK.md rather than optional here. C is the default for anything
public. Plan against roughly a third of defects being machine-findable,
not the tool vendor's higher figure, when deciding what the gap costs
(EV-0236, EV-0104).

## Worked rulings

- **ui-ux pack exemplar (2026-08, argued)**: both surfaces took C. The
  service flow carried a manual verdict file whose entry count equals
  the scanner's incomplete count, and each interactive component
  carried a keyboard contract test asserting key behaviour rather than
  rendering. See `packs/ui-ux/exemplars/two-surfaces-one-spine.md`.
- **The census that sets the floor (external, inherited)**: the six
  commonest failures are cheap to detect and were present on the
  majority of the top million home pages in February 2026 (EV-0235),
  which is why B3 in PACK.md gates them individually rather than
  trusting one aggregate pass.
