---
summary: One repo, several, or a corner of an existing one?
kind: guide
scope: eos-internal
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
volatility: slow
sources: [EV-0168, EV-0172, EV-0173, EV-0183]
review: 2027-07
type: wargame
tags: [eos, wargame, infra]
status: active
---

# WG-EOS-002: One repo, several, or a corner of an existing one?

## The question

Before the seed compiles, the venture needs a home. The choice fixes
where the org lives, what a contractual handover looks like, and how
agent parallelism isolates. It is expensive to reverse once CI,
remotes and contracts point at it.

## It depends on

- Contractual boundary: will the whole venture ever be handed to
  someone (a client, a buyer, a co-founder)?
- Lifespan divergence: do the surfaces live and die together?
- Deploy coupling: do the surfaces ship from one tree or several?
- Shared contracts: how much generated material (types, schemas) flows
  between surfaces?
- Weight: is this a venture at all, or a surface of an existing one?

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

## Decision rule

If the venture could be handed over or sold as a unit, choose A; the
repo is the deliverable. If surfaces have genuinely different owners,
lifespans or remotes (a client owns one, you own another), choose B and
version the contracts between them. If the thing is a minor surface of
an existing venture with no life of its own, choose C and record the
ruling in the host's lock-book instead of seeding a new venture.

## Default

A, the monorepo. The estate convention is a repo per venture with the
EOS as the shared brain; nothing in the estate has yet earned B.

## Worked rulings

- **AutoWatt (2026-07, argued)**: A. Three surfaces (api, app, website)
  ship as containers from one tree per its own ADR-0002, and the Heads
  of Terms contemplate handover of the whole; one repo is the clean
  unit. Ruled ahead of this wargame at the reseed and recorded in its
  lock-book.
- **PatterTech_Business (2026-06, argued, pre-EOS)**: A. Its ADR-0011
  fixed one platform monorepo with every layer extraction-ready, after
  living with the alternative; the extraction-ready clause is the
  polyrepo escape hatch done cheaply.
- **WiseWattage (2026, inherited, pre-EOS)**: A in practice (api, app,
  website, packages in one tree); never argued, counted here as the
  default holding, not as promotion evidence.
