---
id: WG-EOS-002
summary: One repo, several, or a corner of an existing one?
kind: wargame
type: wargame
tags: [eos, infra, wargame]
scenario_modes: [selection, gap]
gap_domain: inception
applies_when: [runs_agents]
engages_when: [operator_requests_wargame]
consequence: high
relations: []
always_walk: true
scope: eos-internal
authority: default
basis: empirical-evidence
evidence_grade: observational
volatility: slow
sources: [EV-0168, EV-0172, EV-0173, EV-0183]
review: 2027-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-EOS-002: One repo, several, or a corner of an existing one?

## Decision question and stakes

Before the seed compiles, the venture needs a home. The choice fixes
where the org lives, what a contractual handover looks like, and how
agent parallelism isolates. It is expensive to reverse once CI,
remotes and contracts point at it.

## Doctrines or coverage gap under pressure

This inception fork covers a gap before pack Doctrine is activated. It is always walked because venture scale and repository shape decide which later rules can be loaded safely.

## Preconditions and engagement triggers

- Contractual boundary: will the whole venture ever be handed to
  someone (a client, a buyer, a co-founder)?
- Lifespan divergence: do the surfaces live and die together?
- Deploy coupling: do the surfaces ship from one tree or several?
- Shared contracts: how much generated material (types, schemas) flows
  between surfaces?
- Weight: is this a venture at all, or a surface of an existing one?

Applicability is `runs_agents`. Engagement is `operator_requests_wargame`. This is an always-walk decision.

## Options

### A. Monorepo
The org and every surface in one repo. Handover is one remote;
contracts flow without publishing; claims and worktrees give
parallelism inside it. Costs a bigger tree and one CI to rule them all.

### B. Polyrepo
An org repo plus surface repos. Buys independent lifespans, owners and
remotes; costs cross-repo coordination, versioned contracts and the
one-writer rule enforced by convention rather than claims.

### C. Adjacent
The venture is a corner of an existing repo (a docs site, a marketing
page inside an estate repo). Buys zero setup; costs the host repo's
rules and no independent handover.

## Failure premises

### Premortem for A. Monorepo

Assume `A. Monorepo` was selected and the outcome failed. Test this option's stated failure mechanism first: a bigger tree and one CI to rule them all.

### Premortem for B. Polyrepo

Assume `B. Polyrepo` was selected and the outcome failed. Test this option's stated failure mechanism first: cross-repo coordination, versioned contracts and the one-writer rule enforced by convention rather than claims.

### Premortem for C. Adjacent

Assume `C. Adjacent` was selected and the outcome failed. Test this option's stated failure mechanism first: the host repo's rules and no independent handover.

## Decision rule

If the venture could be handed over or sold as a unit, choose A; the
repo is the deliverable. If surfaces have genuinely different owners,
lifespans or remotes (a client owns one, you own another), choose B and
version the contracts between them. If the thing is a minor surface of
an existing venture with no life of its own, choose C and record the
ruling in the host's lock-book instead of seeding a new venture.

## Safe default

A, the monorepo. The estate convention is a repo per venture with the
EOS as the shared brain; nothing in the estate has yet earned B.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Contractual boundary: will the whole venture ever be handed to someone (a client, a buyer, a co-founder)?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, the monorepo. The estate convention is a repo per venture with the EOS as the shared brain; nothing in the estate has yet earned B.

**Exit condition:** Stop or roll back the selected branch when a bigger tree and one CI to rule them all, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Contractual boundary: will the whole venture ever be handed to someone (a client, a buyer, a co-founder)?

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Contractual boundary: will the whole venture ever be handed to someone (a client, a buyer, a co-founder)?** and **Lifespan divergence: do the surfaces live and die together?** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
