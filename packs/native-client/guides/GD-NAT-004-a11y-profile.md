---
summary: How much accessibility assurance does a non-web surface buy, and against which instrument?
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0027, EV-0104, EV-0235, EV-0236]
review: on-change-of:EN-301-549-v4-publication
type: guide
tags: [a11y, testing, product]
---

# GD-NAT-004: How much non-web accessibility assurance?

## The question

This is the profile `packs/ui-ux/PACK.md` defers to when a surface has
no web UI. Three things change when the surface is an app.

The unit of conformance becomes a screen or view rather than a page,
and the web terms have to be translated onto platform terms
(EV-0370). The reviewable artefact becomes the semantics
declaration in code, with content descriptions, descendant merging,
explicit heading and pane-title semantics, custom actions with human
labels and null descriptions for decoration (EV-0387). And the
instrument that binds in the EU is EN 301 549 clause 11, which adds
obligations WCAG never states: interoperability with platform assistive
technology, and support for user preference settings (EV-0371).

The numeric floors still come from WCAG 2.2 (EV-0027) through the
mobile mapping, because the platform guidance publishes no touch target
minimum and no contrast ratio at all (EV-0387).

## It depends on

- **Statutory duty.** European Accessibility Act reach, public sector
  procurement, or a regulated market.
- **Whether the user can go elsewhere.** Exclusion only costs where
  there is no alternative route.
- **How much custom drawing there is.** A screen of platform controls
  and a screen the framework drew itself need different evidence,
  especially under architecture C in GD-NAT-001.
- **Closed functionality.** The mapping acknowledges this as a gap, so
  a kiosk or a locked-down device needs its own argument.
- **Rate of change.** A surface rebuilt monthly needs the audit in the
  test suite, not in an annual review.

## Options

### A. Platform defaults, no audit
Ship with whatever the toolkit gives. Buys nothing but time. Costs any
defensible claim, and it silently fails everything custom-drawn. Named
here as the practice this pack rejects.

### B. Semantics declared, automated audit in the test suite
Every screen's semantics are written deliberately, and the platform's
own audit runs inside the test runner over every screen, scoped by
audit type, failing the build on any violation (EV-0388). Buys a
gate that is a normal failing test rather than a review ritual. Costs
the authoring habit and a per-screen test.

### C. B plus a manual verdict list and assistive-technology passes
Every item the audit cannot decide gets a written verdict in a named
file, with the file's entry count equal to the audit's undecided count.
Adds screen reader and magnification passes and a user preference check
under clause 11 (EV-0371). Buys coverage of the defect class no
audit sees. Costs standing triage and device time.

### D. C plus a conformance statement and independent audit
Adds testing with disabled users and an independent audit before a
public conformance claim against EN 301 549 clause 11 and its WCAG
mapping. Buys the only evidence that survives challenge. Costs money,
calendar time and recruiting.

## Decision rule

If a statutory duty applies, or a public conformance claim will be
made, take D. If the app is a public product, or any part of the
interface is custom-drawn rather than platform-supplied, take C. Take B
only for an internal tool built entirely from platform controls. Never
take A. B is the binding floor: PACK.md B6 requires the declared
semantics, the in-suite audit and the verdict file, so B is not
optional here.

State the claim per screen, never per app. Where EN 301 549 applies,
state it as clause 11 plus the WCAG mapping, and note that the in-force
version references an older WCAG level, so targeting WCAG 2.2 puts you
ahead of the binding standard rather than behind it (EV-0371).

## Default

C for anything a member of the public installs.

Plan against a low catch rate for the automated audit. No coverage
figure is published for it at all (EV-0388), and the equivalent
web figure is contested between roughly 57 per cent and roughly a third
(EV-0236, EV-0104). The web census puts it plainly that no detected
errors does not mean accessible (EV-0235), and that caution is stronger
here where nobody has published a number.

## Worked rulings

- **native-client pack exemplar (2026-08, argued)**: C. Audit in the
  test suite over all six screens, a verdict file whose entry count
  equals the undecided count, and a static check for unlabelled
  interactive elements and explicitly marked decoration. See
  `packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md`.
- **The mapping has no legal force (external, inherited)**: the mobile
  mapping is a Group Draft Note, informative, replaceable at any time,
  Level A and AA only (EV-0370). Use it to translate. Do not
  cite it as an obligation.
