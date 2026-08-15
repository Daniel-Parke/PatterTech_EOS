---
id: GD-UIUX-001
summary: Which design philosophy does this surface take?
kind: wargame
type: wargame
tags: [density, eos, layout, wargame, web]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-UIUX-008, DOC-UIUX-009, DOC-DISC-016, DOC-HOUSE-004, DOC-HOUSE-015, DOC-UIUX-011, DOC-UIUX-014]
applies_when: [has_user_interface]
engages_when: [serves_novice_and_expert_users, house_style_costs_access_or_performance]
consequence: high
relations: []
scope: estate
authority: advisory
basis: local-observation
evidence_grade: observational
sources: [EV-0062, EV-0063, EV-0103, EV-0227, EV-0228, EV-0229, EV-0230, EV-0231, EV-0232, EV-0234, EV-0238, EV-0239, EV-0240, EV-0241]
review: 2027-10
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-UIUX-001: Which design philosophy does this surface take?

## Decision question and stakes

Every surface answers to a philosophy: how dense it is, how loud, what
its type scale and component inventory look like, and what it optimises
for. The question is which one this surface takes, and it is asked per
surface, not per estate. Two surfaces in one repo may take different
answers and usually should.

## Doctrines or coverage gap under pressure

- `DOC-UIUX-008` (default): Every component declares its interaction states.
- `DOC-UIUX-009` (default): One named philosophy per surface, recorded before pixel work.
- `DOC-DISC-016` (default): Recruit by frame, then by count.
- `DOC-HOUSE-004` (preference): Motion is judged by moving area and scroll coupling.
- `DOC-HOUSE-015` (default): Spend the design budget on the first screen.
- `DOC-UIUX-011` (default): Field performance is a design constraint on public surfaces.
- `DOC-UIUX-014` (default): Honour reduced-motion preferences globally.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `has_user_interface`. Engagement is `serves_novice_and_expert_users`, `house_style_costs_access_or_performance`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Content-first public service

Assume `A. Content-first public service` was selected and the outcome failed. Test this option's stated failure mechanism first: pace: it wants a standing team and it looks plain by design.

### Premortem for B. Dense enterprise

Assume `B. Dense enterprise` was selected and the outcome failed. Test this option's stated failure mechanism first: a heavy surface and slow change, and it reads as bureaucracy anywhere a first-time user lands.

### Premortem for C. Consumer and lifestyle, expressive

Assume `C. Consumer and lifestyle, expressive` was selected and the outcome failed. Test this option's stated failure mechanism first: familiarity: the same research found that breaking established patterns hurt, and expressive treatment on destructive controls is dangerous.

### Premortem for D. Editorial

Assume `D. Editorial` was selected and the outcome failed. Test this option's stated failure mechanism first: governance machinery, so it does not scale to a large multi-team estate.

### Premortem for E. Conversion-led landing

Assume `E. Conversion-led landing` was selected and the outcome failed. Test this option's stated failure mechanism first: pressure toward dark patterns and toward optimising a local metric.

### Premortem for F. Data-heavy dashboard

Assume `F. Data-heavy dashboard` was selected and the outcome failed. Test this option's stated failure mechanism first: breadth: an opinionated dashboard serves fewer questions.

### Premortem for G. Mobile-native, platform-conformant

Assume `G. Mobile-native, platform-conformant` was selected and the outcome failed. Test this option's stated failure mechanism first: two truths for two platforms, and a shared house language that loses arguments to each platform's conventions. Check the implementation's maintenance state, not the brand behind it (EV-0231).

### Premortem for H. Restrained minimal, applied over any of A to G

Assume `H. Restrained minimal, applied over any of A to G` was selected and the outcome failed. Test this option's stated failure mechanism first: discoverability where signifiers are stripped (EV-0234), which has to be paid back by an explicit interaction-state contract (PACK.md B7).

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

## Safe default

None, deliberately. This guide has no house default and adding one
would break the pluralism contract in PACK.md. Where the triggers are
genuinely silent, name the surface's dominant job, choose the
philosophy that serves it, and record what you would give up if you had
chosen the runner-up. PatterTech house style is a separate preference
pack, and it activates only when a venture adopts it by name.

## Cheapest discriminating test

Run the same representative task with novice and frequent users. Record completion, error and search time, then repeat on the lowest supported device if house treatment or density changes performance.

## Fallback, exit and revisit

**Fallback `safe-default`:** None, deliberately. This guide has no house default and adding one would break the pluralism contract in PACK.md. Where the triggers are genuinely silent, name the surface's dominant job, choose the philosophy that serves it, and record what you would give up if you had chosen the runner-up. PatterTech house style is a separate preference pack, and it activates only when a venture adopts it by name.

**Exit condition:** Stop or roll back the selected branch when pace: it wants a standing team and it looks plain by design, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Can the user leave?** A statutory service, an internal tool and a paid-acquisition landing page differ mainly here.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
