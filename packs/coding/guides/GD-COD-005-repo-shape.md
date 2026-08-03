---
summary: One repository or several, and how the trunk flows through whichever you pick
type: guide
tags: [arch, delivery, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0026, EV-0168, EV-0170, EV-0171, EV-0172, EV-0173, EV-0183]
review: 2027-08
review_by: 2027-08
---

# GD-COD-005: One repository or several?

## The question

A venture grows a second deployable thing. The fork is whether it lives
in the same repository, and it is really a question about which costs
you can pay: bespoke tooling, or cross-repo version coordination.

## It depends on

- Do the parts ship together, or on separate release trains?
- Is there a consumer outside the venture?
- Can you fund the build and test tooling a large single repository
  needs, which for a venture means roughly none?
- How often does a change have to touch two parts at once?

## Options

### A. One repository per venture

Everything ships from one trunk. Buys: one version of everything, atomic
cross-part change, cheap large-scale refactoring, and no coordination
protocol at all. At venture scale these come free precisely because the
repository is small (EV-0172). Costs: nothing until the build gets slow
or ownership gets unclear (EV-0173).

### B. A repository per deployable

Each part has its own trunk and its own release. Buys: clean ownership
and independent release cadence. Costs: every cross-part change becomes
a two-repository dance with a version bump in the middle, and you now
need a compatibility story (EV-0171) whether or not you wanted one.

### C. One repository, published contract packages

Single trunk, with the shared interfaces published as versioned
artefacts that outside consumers pin. Buys: atomic internal change plus
a stable external surface. Costs: a publishing step and a versioning
discipline for the artefacts, which is real work.

### D. Split by release train

One repository per group of things that ship together, however many
deployables that is. Buys: the split follows the actual coupling rather
than the org chart. Costs: you have to know your release trains, and
they move.

## Decision rule

- One venture, one release train, no outside consumer: A.
- Anything outside the venture consumes an interface: C. Publish and
  version that interface, and keep the rest in one trunk.
- A part genuinely ships on its own cadence with its own consumers: D,
  and only for that part.
- B for everything is not a default. Take it only when ownership has
  actually split between people or ventures.

## Default

A. A small repository gets the benefits of a single trunk for free, and
the pain reported in the literature sits in the middle sizes that a
venture does not reach for years.

## Whatever you pick, the trunk flows the same way

Trunk-based development is defined operationally, not ideologically:
three or fewer active branches, branch lifetime in hours rather than
days, at least one merge to trunk per developer per day, and no code
freezes (EV-0168). For a solo operator directing agents the residue that
matters is merge cadence and the ban on freezes; branch counts take care
of themselves. Big changes ride behind feature flags or branch by
abstraction rather than a long branch (EV-0183), and the flag machinery
is itself a system with a lifecycle that has to be managed (EV-0026), so
it is not free either.

Commit message grammar is a preference, not part of this fork. Adopt
Conventional Commits only where release automation consumes it, and
normalise at merge rather than expecting every agent commit to comply
(EV-0170).

## Evidence boundary

EV-0172 is an experience report with operational statistics and no
comparison group, and it is candid that the benefits at two billion
lines are bought with tooling investment most organisations cannot fund.
Quoting the benefits without the investment is the standard misreading.
EV-0173 is a grey-literature review from 2018, so it reports advocacy
rather than measurement and predates both current build tooling and
machine authorship. EV-0168 is survey association, not causal evidence,
and EV-0183 is a practitioner site that is stale by its own copyright
notice. There is no controlled comparison of repository shapes. Anyone
claiming a winner here is asserting.

## Worked rulings

- **PatterTech EOS coding pack (2026-08, argued)**: A as the default,
  C once anything outside the venture consumes an interface. Argued from
  EV-0172 and EV-0173, both read for their costs rather than their
  headlines.
- **PatterTech EOS itself (2026-08, inherited)**: A. One repository,
  documentation and tooling together, inherited from the estate map.
