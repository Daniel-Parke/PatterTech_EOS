---
summary: How deep a vendor is allowed into the codebase, whether SDK throughout, an owned adapter, the raw protocol, or a generated client
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0161, EV-0150, EV-0061, EV-0023, EV-0025]
review: 2027-01
type: guide
tags: [arch, security, money]
review_by: 2027-01
---

# WG-ARCH-007: SDK, owned adapter, raw protocol, or generated client?

Carried forward from the v1 wargame of the same id, re-graded. The
webhook half of the v1 rule now binds as B5 of
`packs/architecture/PACK.md`, because it stands on a documented
protocol requirement. The adapter half is a default, D7, because it
stands on local observation.

## The question

Every vendor arrives with an SDK that wants to be imported everywhere,
and every vendor eventually changes terms, prices or existence. The
fork is how deep a vendor is allowed to reach, and it is taken per
vendor and per seam, not once for the venture.

## It depends on

- How replaceable the vendor must be: contract clauses, sovereignty
  requirements, cost trajectories.
- Whether the seam receives attacker-shaped input, such as a webhook.
- Whether the vendor holds identity, money, or anything a handover
  obligation covers.
- How much of the SDK's value is protocol knowledge against
  convenience.
- Whether the vendor publishes a machine-readable schema you could
  generate from instead.

## Options

### A. SDK throughout

**What it is.** Import the vendor wherever it is used.

**Buys.** The fastest first week, and the vendor's own retry, pagination
and error handling for free.

**Costs.** The exit cost grows with every import site. The SDK's
version policy becomes yours. At a webhook it is attack surface with
opinions about body parsing.

### B. Owned adapter

**What it is.** One interface the venture owns, the SDK confined
inside it, and an exit route written down naming what replaces it and
what migrates. The venture's own store stays the authorisation truth.

**Buys.** A single place to change, a seam tests can stub, and an exit
that is a task rather than a project.

**Costs.** An interface to design and maintain, and the temptation to
model it on the current vendor, which quietly defeats the point.

### C. Raw protocol

**What it is.** No SDK. Standard-library code against the wire format:
HMAC verification over raw bytes, plain HTTP calls.

**Buys.** The smallest attack surface, no dependency, and full control
of the bytes. Stripe's own documentation (EV-0161) makes the case
without meaning to: verification is over the exact raw request bytes,
so any middleware that parses or re-serialises the body destroys the
signature.

**Costs.** You maintain protocol knowledge, including replay tolerance
and payload version pinning, and you re-learn it each time the vendor
moves.

### D. Generated client from the vendor's schema

**What it is.** The vendor publishes OpenAPI or JSON Schema
(EV-0023, EV-0025); you generate a client offline, commit it, and gate
it for drift.

**Buys.** Types that track the vendor without a hand-maintained layer,
and a build failure when the vendor's contract moves.

**Costs.** Only available where the vendor publishes a usable schema,
and the generated surface is still theirs, so it needs B around it to
be an exit rather than a coupling.

## Decision rule

Webhook verification and any signature checking: **C**, always, and B5
binds it. Identity, money, or anything contractually handover-bound:
**B** at minimum, with the exit route written where the decision
record lives and the venture's database staying the authorisation
truth. A vendor publishing a maintained schema, wrapped in B: **D** is
the cheaper way to keep B honest. Fringe conveniences with trivial
exits: **A** is tolerable. Anything with no documented exit route is a
deviation, not a default.

## Default

**B**, with **C** at every verification seam. Vendors are guests with
documented departure plans.

## Worked rulings

- **AutoWatt (2026-07, argued)**: B across an explicit estate of
  exceptions, forced explicit by contract. Each non-AWS service
  carries a reason, a trade-off and a migration route, and Clerk sits
  behind an adapter with the venture database as the authorisation
  truth.
- **WiseWattage (2026, argued)**: C for webhooks, using stdlib
  HMAC-SHA256 with idempotency keys and no provider SDKs, and B for
  identity.
- **PatterTech_Business (2026-07, inherited)**: B taken from the
  estate default, with payment vendor version pinning recorded when
  Stripe's version policy (EV-0061) forced the question.

## Counter-evidence

EV-0161 is vendor documentation, proprietary, and read as paraphrase
only. Its constants do not transfer: tolerances, header formats and
version-pinning semantics differ per vendor, so the rule that survives
is verify raw bytes, bound recency, pin the payload version. The
adapter default has no external evidence at all. Cockburn (EV-0150) is
the closest thing, and it argues for ports only where a second device
is genuinely plausible, which is a narrower claim than D7 makes.
