---
id: WG-COD-005
summary: One repository or several, and how the trunk flows through whichever you pick
kind: wargame
type: wargame
tags: [arch, delivery, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-COD-009, DOC-COD-010]
applies_when: [edits_source]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0026, EV-0168, EV-0170, EV-0171, EV-0172, EV-0173, EV-0183]
review: 2027-08
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-COD-005: One repository or several?

## Decision question and stakes

A venture grows a second deployable thing. The fork is whether it lives
in the same repository, and it is really a question about which costs
you can pay: bespoke tooling, or cross-repo version coordination.

## Doctrines or coverage gap under pressure

- `DOC-COD-009` (default): Trunk-based flow.
- `DOC-COD-010` (default): Monorepo per venture until tooling cost forces otherwise.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Do the parts ship together, or on separate release trains?
- Is there a consumer outside the venture?
- Can you fund the build and test tooling a large single repository
  needs, which for a venture means roughly none?
- How often does a change have to touch two parts at once?

Applicability is `edits_source`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. One repository per venture

Assume `A. One repository per venture` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing until the build gets slow or ownership gets unclear (EV-0173).

### Premortem for B. A repository per deployable

Assume `B. A repository per deployable` was selected and the outcome failed. Test this option's stated failure mechanism first: every cross-part change becomes a two-repository dance with a version bump in the middle, and you now need a compatibility story (EV-0171) whether or not you wanted one.

### Premortem for C. One repository, published contract packages

Assume `C. One repository, published contract packages` was selected and the outcome failed. Test this option's stated failure mechanism first: a publishing step and a versioning discipline for the artefacts, which is real work.

### Premortem for D. Split by release train

Assume `D. Split by release train` was selected and the outcome failed. Test this option's stated failure mechanism first: you have to know your release trains, and they move.

## Decision rule

- One venture, one release train, no outside consumer: A.
- Anything outside the venture consumes an interface: C. Publish and
  version that interface, and keep the rest in one trunk.
- A part genuinely ships on its own cadence with its own consumers: D,
  and only for that part.
- B for everything is not a default. Take it only when ownership has
  actually split between people or ventures.

## Safe default

A. A small repository gets the benefits of a single trunk for free, and
the pain reported in the literature sits in the middle sizes that a
venture does not reach for years.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Do the parts ship together, or on separate release trains?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. A small repository gets the benefits of a single trunk for free, and the pain reported in the literature sits in the middle sizes that a venture does not reach for years.

**Exit condition:** Stop or roll back the selected branch when nothing until the build gets slow or ownership gets unclear (EV-0173), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Do the parts ship together, or on separate release trains?

## Counter-evidence and transfer limits

### Evidence boundary

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
### Preserved reasoning: Whatever you pick, the trunk flows the same way

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
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
