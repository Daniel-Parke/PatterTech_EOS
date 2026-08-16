---
id: WG-UIUX-004
summary: Where do this surface's interactive components come from?
kind: wargame
type: wargame
tags: [a11y, eos, tooling, wargame, web]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-UIUX-003, DOC-UIUX-010]
applies_when: [has_user_interface]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: local-observation
evidence_grade: observational
sources: [EV-0066, EV-0067, EV-0227, EV-0228, EV-0229, EV-0230, EV-0231, EV-0238, EV-0239]
review: 2027-11
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-UIUX-004: Where do this surface's interactive components come from?

## Decision question and stakes

Menus, dialogs, comboboxes, tabs and date pickers are where
accessibility is won or lost, and they are expensive to get right. The
fork is whether the estate writes that behaviour, rents it, copies it,
or inherits it from a platform. It decides who fixes the next
accessibility bug and how quickly it reaches your users.

## Doctrines or coverage gap under pressure

- `DOC-UIUX-003` (binding): Every interactive component maps to an APG pattern or documents its deviation with a behaviour test.
- `DOC-UIUX-010` (default): Headless behaviour layer plus own visual layer.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Team size and patch appetite.** Who will read an upstream changelog
  and apply a fix.
- **How far the visual language must travel from the source.** A heavy
  visual departure fights a styled kit.
- **How many surfaces share the components**, and whether they share a
  philosophy.
- **Lifespan.** A campaign page and a ten-year internal tool are
  different bets.
- **Licence.** Openly published does not mean freely usable
  (EV-0238).
- **Maintenance signal in the actual repo**, not the brand behind it
  (EV-0231).

Applicability is `has_user_interface`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Headless primitives plus own visual layer
Behaviour, roles, focus management and keyboard handling come from an
unstyled library; the visual layer is yours (EV-0066). Buys hard
correctness for free with zero visual opinion, which is what makes one
behaviour core under several philosophies affordable. Costs a
dependency on the primitive library's release pace, and the styling
work is entirely yours.

### B. Adopt a vendor system whole
Tokens, components, icons and grid arrive as one versioned dependency,
sometimes with several generations coexisting so migration is
incremental (EV-0227, EV-0228). Buys accessibility, documentation and
cross-product consistency without staffing them. Costs a visual
identity that reads as the vendor unless retokenised, a heavy surface,
and change at the vendor's pace.

### C. Copy the source and own it
Component source is pasted into the repo and maintained locally
(EV-0067). Buys total freedom to restyle and restructure, and no
upgrade gate. Costs the upstream accessibility fix flow, which is the
load-bearing cost: a bug fixed upstream never reaches you unless
somebody notices and ports it.

### D. Platform-native controls
On a store platform, the system control with system behaviour, with
house style applied inside it (EV-0230, EV-0229). Buys familiarity,
platform accessibility work and OS updates for free. Costs two
implementations for two platforms and limits how far a house language
can travel.

### E. Build from scratch
Behaviour written in-house against the APG patterns. Buys an exact fit
where no library models the interaction. Costs the most, repeatedly,
and every pattern needs its own keyboard test suite before it ships.

## Failure premises

### Premortem for A. Headless primitives plus own visual layer

Assume `A. Headless primitives plus own visual layer` was selected and the outcome failed. Test this option's stated failure mechanism first: a dependency on the primitive library's release pace, and the styling work is entirely yours.

### Premortem for B. Adopt a vendor system whole

Assume `B. Adopt a vendor system whole` was selected and the outcome failed. Test this option's stated failure mechanism first: a visual identity that reads as the vendor unless retokenised, a heavy surface, and change at the vendor's pace.

### Premortem for C. Copy the source and own it

Assume `C. Copy the source and own it` was selected and the outcome failed. Test this option's stated failure mechanism first: the upstream accessibility fix flow, which is the load-bearing cost: a bug fixed upstream never reaches you unless somebody notices and ports it.

### Premortem for D. Platform-native controls

Assume `D. Platform-native controls` was selected and the outcome failed. Test this option's stated failure mechanism first: two implementations for two platforms and limits how far a house language can travel.

### Premortem for E. Build from scratch

Assume `E. Build from scratch` was selected and the outcome failed. Test this option's stated failure mechanism first: the most, repeatedly, and every pattern needs its own keyboard test suite before it ships.

## Decision rule

If the surface has a distinct visual philosophy and a small team,
choose A. If the estate runs many internal apps that must feel like one
product and no one will staff a design system, choose B. If the team
will genuinely read upstream changelogs and wants to restructure
components, choose C, and record who owns the port-back duty. If the
surface ships into a store, choose D and apply A or C only for what the
platform does not provide. Choose E only when a documented pattern has
no maintained implementation, and say which APG pattern it follows.

## Safe default

A, headless primitives plus an own visual layer. It is the option that
keeps one behavioural core under several philosophies, which is what
this pack is built to allow. Departing is cheap: record the reason and
the option taken.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Team size and patch appetite.** Who will read an upstream changelog and apply a fix.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, headless primitives plus an own visual layer. It is the option that keeps one behavioural core under several philosophies, which is what this pack is built to allow. Departing is cheap: record the reason and the option taken.

**Exit condition:** Stop or roll back the selected branch when a dependency on the primitive library's release pace, and the styling work is entirely yours, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Team size and patch appetite.** Who will read an upstream changelog and apply a fix.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Team size and patch appetite.** Who will read an upstream changelog and apply a fix.** and ****How far the visual language must travel from the source.** A heavy visual departure fights a styled kit.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
