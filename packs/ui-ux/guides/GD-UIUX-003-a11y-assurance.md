---
id: GD-UIUX-003
summary: How much accessibility assurance does this surface buy?
kind: wargame
type: wargame
tags: [a11y, eos, testing, wargame, web]
scenario_modes: [selection, exception, conflict]
applicable_doctrines: [DOC-UIUX-002, DOC-UIUX-007, DOC-HOUSE-004, DOC-HOUSE-015, DOC-UIUX-011, DOC-UIUX-014]
applies_when: [has_user_interface]
engages_when: [house_style_costs_access_or_performance]
consequence: high
relations: [DREL-HOUSE-001]
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0027, EV-0028, EV-0029, EV-0104, EV-0235, EV-0236, EV-0237]
review: on-change-of:WCAG-2.2
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-UIUX-003: How much accessibility assurance does this surface buy?

## Decision question and stakes

Automated rules find a minority of accessibility defects, and the
maintainers of the tools say so (EV-0236, EV-0104). The fork is how
much assurance a surface buys on top, and therefore what a passing
build is allowed to claim. This is a budget question with a legal edge,
not a tooling preference.

## Doctrines or coverage gap under pressure

- `DOC-UIUX-002` (binding): The six cheap failure classes are gated individually.
- `DOC-UIUX-007` (default): The claim is evidenced by a real-browser run with pinned tags, plus a written verdict on every incomplete.
- `DOC-HOUSE-004` (preference): Motion is judged by moving area and scroll coupling.
- `DOC-HOUSE-015` (default): Spend the design budget on the first screen.
- `DOC-UIUX-011` (default): Field performance is a design constraint on public surfaces.
- `DOC-UIUX-014` (default): Honour reduced-motion preferences globally.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `has_user_interface`. Engagement is `house_style_costs_access_or_performance`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Unpinned automated rules only

Assume `A. Unpinned automated rules only` was selected and the outcome failed. Test this option's stated failure mechanism first: the meaning of the result, because house opinion and standard conformance are conflated, and colour contrast does not even run outside a real browser engine (EV-0236). Named here as the common practice this pack rejects.

### Premortem for B. Pinned tags in a real browser, with incomplete triaged

Assume `B. Pinned tags in a real browser, with incomplete triaged` was selected and the outcome failed. Test this option's stated failure mechanism first: a standing triage habit, since the incomplete list is where the judgement lives.

### Premortem for C. B plus behaviour and states testing

Assume `C. B plus behaviour and states testing` was selected and the outcome failed. Test this option's stated failure mechanism first: test authoring per pattern.

### Premortem for D. C plus assistive-technology and user testing, with an audit

Assume `D. C plus assistive-technology and user testing, with an audit` was selected and the outcome failed. Test this option's stated failure mechanism first: money and calendar time, and it needs recruiting.

## Decision rule

If a statutory duty applies, or the surface is one people cannot avoid,
or a public conformance statement will be published, choose D. If the
surface is a public product with custom interactive components, choose
C. If it is an internal tool with mostly native controls, choose B.
Never choose A. Overlays are not an option at any level: they cannot
repair labels, alternative text or keyboard access, and sniffing
assistive-technology use exposes disability status without consent
(EV-0237).

## Safe default

B is the floor for anything with a web UI. Its six-class half binds as
B3 in PACK.md; its pinned-run half is B2, a default since the 2026-08
audit, so a surface that skips it says why. C is the default for
anything public. Plan against roughly a third of defects being machine-findable,
not the tool vendor's higher figure, when deciding what the gap costs
(EV-0236, EV-0104).

## Cheapest discriminating test

Exercise the hardest representative journey with reduced motion and on the lowest supported device, then inspect the accessibility tree and named assistive-technology path for the claimed criteria.

## Fallback, exit and revisit

**Fallback `safe-default`:** B is the floor for anything with a web UI. Its six-class half binds as B3 in PACK.md; its pinned-run half is B2, a default since the 2026-08 audit, so a surface that skips it says why. C is the default for anything public. Plan against roughly a third of defects being machine-findable, not the tool vendor's higher figure, when deciding what the gap costs (EV-0236, EV-0104).

**Exit condition:** Stop or roll back the selected branch when the meaning of the result, because house opinion and standard conformance are conflated, and colour contrast does not even run outside a real browser engine (EV-0236). Named here as the common practice this pack rejects, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Statutory duty.** Public sector, procurement, or a regulated market.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Statutory duty.** Public sector, procurement, or a regulated market.** and ****Whether the user can go elsewhere.** Exclusion is only a real cost where there is no alternative route.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
