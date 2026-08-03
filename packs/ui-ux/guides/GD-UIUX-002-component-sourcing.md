---
summary: Where do this surface's interactive components come from?
kind: guide
authority: default
basis: local-observation
evidence_grade: observational
scope: estate
sources: [EV-0066, EV-0067, EV-0227, EV-0228, EV-0229, EV-0230, EV-0231, EV-0238, EV-0239]
review: 2027-11
type: guide
tags: [web, tooling, a11y]
review_by: 2027-11
---

# GD-UIUX-002: Where do this surface's interactive components come from?

## The question

Menus, dialogs, comboboxes, tabs and date pickers are where
accessibility is won or lost, and they are expensive to get right. The
fork is whether the estate writes that behaviour, rents it, copies it,
or inherits it from a platform. It decides who fixes the next
accessibility bug and how quickly it reaches your users.

## It depends on

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

## Decision rule

If the surface has a distinct visual philosophy and a small team,
choose A. If the estate runs many internal apps that must feel like one
product and no one will staff a design system, choose B. If the team
will genuinely read upstream changelogs and wants to restructure
components, choose C, and record who owns the port-back duty. If the
surface ships into a store, choose D and apply A or C only for what the
platform does not provide. Choose E only when a documented pattern has
no maintained implementation, and say which APG pattern it follows.

## Default

A, headless primitives plus an own visual layer. It is the option that
keeps one behavioural core under several philosophies, which is what
this pack is built to allow. Departing is cheap: record the reason and
the option taken.

## Worked rulings

- **ui-ux pack exemplar (2026-08, argued)**: both surfaces imported
  from one shared module built on headless primitives, so a service
  form and an operations dashboard share zero duplicate component
  implementations while looking nothing alike. See
  `packs/ui-ux/exemplars/two-surfaces-one-spine.md`.
- **Counter-ruling worth reading (external, inherited)**: one large
  estate archived its React implementation and moved to framework
  agnostic web components (EV-0238) while another kept three
  generations alive at once (EV-0228). Both were defensible at that
  size, which is why this guide has no rule about clean breaks.
