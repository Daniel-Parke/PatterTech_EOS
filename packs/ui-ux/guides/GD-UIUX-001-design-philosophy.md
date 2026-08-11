---
summary: Which design philosophy does this surface take?
kind: guide
authority: advisory
basis: local-observation
evidence_grade: observational
scope: estate
sources: [EV-0062, EV-0063, EV-0103, EV-0227, EV-0228, EV-0229, EV-0230, EV-0231, EV-0232, EV-0234, EV-0238, EV-0239, EV-0240, EV-0241]
review: 2027-10
type: guide
tags: [web, density, layout]
---

# GD-UIUX-001: Which design philosophy does this surface take?

## The question

Every surface answers to a philosophy: how dense it is, how loud, what
its type scale and component inventory look like, and what it optimises
for. The question is which one this surface takes, and it is asked per
surface, not per estate. Two surfaces in one repo may take different
answers and usually should.

## It depends on

- **Can the user leave?** A statutory service, an internal tool and a
  paid-acquisition landing page differ mainly here.
- **What is the surface for?** Completing a task, reading, monitoring,
  browsing, or converting.
- **Session shape.** One long visit, many short visits, or a
  once-in-a-lifetime form.
- **Who reads it.** Experts on their eighth hour, or a stranger on a
  phone in a hurry.
- **What failure costs.** Exclusion, a wrong operational call, a lost
  sale, or mild annoyance.
- **Platform.** A browser, or a store with its own conventions.

## Options

### A. Content-first public service
Plain language, one thing per page, generous targets, evidence gate
before a component is admitted (EV-0062, EV-0063, EV-0103). Buys the
widest reach and the lowest exclusion risk. Costs pace: it wants a
standing team and it looks plain by design.

### B. Dense enterprise
One versioned kit of tokens, components, icons and grid across many
long-lived apps, with multi-generation migration as a feature
(EV-0227, EV-0228). Buys cross-product consistency and expert speed.
Costs a heavy surface and slow change, and it reads as bureaucracy
anywhere a first-time user lands.

### C. Consumer and lifestyle, expressive
Emphasis through size, shape, containment and colour; personality is
part of the product (EV-0232). Buys attention and faster target finding
in the vendor's own studies. Costs familiarity: the same research found
that breaking established patterns hurt, and expressive treatment on
destructive controls is dangerous.

### D. Editorial
Typography, measure and article furniture at the centre, small
component surface, page budget shared with consent and analytics code
(EV-0239). Buys reading comfort at length. Costs governance machinery,
so it does not scale to a large multi-team estate.

### E. Conversion-led landing
One primary action, field performance treated as a design constraint,
claims settled by experiment (EV-0241). Buys a surface with a money
number attached. Costs pressure toward dark patterns and toward
optimising a local metric.

### F. Data-heavy dashboard
Commit to a method such as RED, USE or the four golden signals, order
panels as a narrative answering one named question, carry written
context in the dashboard (EV-0240). Buys a fast read under stress.
Costs breadth: an opinionated dashboard serves fewer questions.

### G. Mobile-native, platform-conformant
The system control with system behaviour is the starting point and
house style is applied inside it (EV-0230, EV-0229). Buys familiarity
and free platform accessibility work. Costs two truths for two
platforms, and a shared house language that loses arguments to each
platform's conventions. Check the implementation's maintenance state,
not the brand behind it (EV-0231).

### H. Restrained minimal, applied over any of A to G
Minimal and expressive is an axis rather than a system, so it composes
with the seven above. Buys speed, calm and less to maintain. Costs
discoverability where signifiers are stripped (EV-0234), which has to
be paid back by an explicit interaction-state contract (PACK.md B7).

## Decision rule

If the user cannot avoid the surface, or a statutory duty applies,
choose A. If the reader is an operator answering a named question under
time pressure, choose F. If the job is reading at length, choose D. If
the surface is a paid entry point with a conversion target, choose E.
If it is one of many internal apps that must feel like one product,
choose B. If it ships into a platform store, choose G and apply the
rest inside it. If use is discretionary and the surface competes for
attention, choose C. Apply H as a dial over whichever of A to G won,
and be stricter about states the more you strip.

## Default

None, deliberately. This guide has no house default and adding one
would break the pluralism contract in PACK.md. Where the triggers are
genuinely silent, name the surface's dominant job, choose the
philosophy that serves it, and record what you would give up if you had
chosen the runner-up. PatterTech house style is a separate preference
pack, and it activates only when a venture adopts it by name.

## Worked rulings

Rulings are marked argued (engaged the triggers afresh) or inherited
(took a prior answer without new argument).

- **ui-ux pack exemplar (2026-08, argued)**: a service task flow took
  A and an operations dashboard took F in one repo, sharing one token
  source and one behaviour layer, with measurably different type scale,
  density and component inventory. Written up in
  `packs/ui-ux/exemplars/EX-UIUX-001-two-surfaces-one-spine.md`.
- **PatterTech Website (2026-07, argued, inherited into this pack)**:
  long reads took a skim layer over a read-first structure, which is
  option D with the density fork of WG-WEB-006 answered read-first.
  Recorded in `archive/v1-final:doctrine/web-design/wargames/WG-WEB-006-density-and-audience.md`.
