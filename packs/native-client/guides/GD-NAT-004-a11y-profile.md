---
id: GD-NAT-004
summary: How much accessibility assurance does a non-web surface buy, and against which instrument?
kind: wargame
type: wargame
tags: [a11y, eos, product, testing, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-NAT-006]
applies_when: [has_native_ui]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0027, EV-0104, EV-0235, EV-0236, EV-0370, EV-0371, EV-0387, EV-0388]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-NAT-004: How much non-web accessibility assurance?

## Decision question and stakes

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

## Doctrines or coverage gap under pressure

- `DOC-NAT-006` (binding): Non-web accessibility conformance is stated per screen, declared in code, and gated by an automated audit with a written verdict on every undecided item.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `has_native_ui`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Platform defaults, no audit

Assume `A. Platform defaults, no audit` was selected and the outcome failed. Test this option's stated failure mechanism first: any defensible claim, and it silently fails everything custom-drawn. Named here as the practice this pack rejects.

### Premortem for B. Semantics declared, automated audit in the test suite

Assume `B. Semantics declared, automated audit in the test suite` was selected and the outcome failed. Test this option's stated failure mechanism first: the authoring habit and a per-screen test.

### Premortem for C. B plus a manual verdict list and assistive-technology passes

Assume `C. B plus a manual verdict list and assistive-technology passes` was selected and the outcome failed. Test this option's stated failure mechanism first: standing triage and device time.

### Premortem for D. C plus a conformance statement and independent audit

Assume `D. C plus a conformance statement and independent audit` was selected and the outcome failed. Test this option's stated failure mechanism first: money, calendar time and recruiting.

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

## Safe default

C for anything a member of the public installs.

Plan against a low catch rate for the automated audit. No coverage
figure is published for it at all (EV-0388), and the equivalent
web figure is contested between roughly 57 per cent and roughly a third
(EV-0236, EV-0104). The web census puts it plainly that no detected
errors does not mean accessible (EV-0235), and that caution is stronger
here where nobody has published a number.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Statutory duty.** European Accessibility Act reach, public sector procurement, or a regulated market.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C for anything a member of the public installs. Plan against a low catch rate for the automated audit. No coverage figure is published for it at all (EV-0388), and the equivalent web figure is contested between roughly 57 per cent and roughly a third (EV-0236, EV-0104). The web census puts it plainly that no detected errors does not mean accessible (EV-0235), and that caution is stronger here where nobody has published a number.

**Exit condition:** Stop or roll back the selected branch when any defensible claim, and it silently fails everything custom-drawn. Named here as the practice this pack rejects, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Statutory duty.** European Accessibility Act reach, public sector procurement, or a regulated market.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
