---
id: WG-ARCH-007
summary: How deep a vendor is allowed into the codebase, whether SDK throughout, an owned adapter, the raw protocol, or a generated client
kind: wargame
type: wargame
tags: [arch, eos, money, security, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-API-002, DOC-ARCH-010]
applies_when: [has_server_code]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0161, EV-0150, EV-0061, EV-0023, EV-0025]
review: 2027-01
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-ARCH-007: SDK, owned adapter, raw protocol, or generated client?

Carried forward from the v1 wargame of the same id, re-graded. The
webhook half of the v1 rule now binds as B5 of
`packs/architecture/PACK.md`, because it stands on a documented
protocol requirement. The adapter half is a default, D7, because it
stands on local observation.

## Decision question and stakes

Every vendor arrives with an SDK that wants to be imported everywhere,
and every vendor eventually changes terms, prices or existence. The
fork is how deep a vendor is allowed to reach, and it is taken per
vendor and per seam, not once for the venture.

## Doctrines or coverage gap under pressure

- `DOC-API-002` (binding): Webhook receivers authenticate the exact raw request before parsing, reject stale deliveries, and process accepted deliveries idempotently against a pinned payload version.
- `DOC-ARCH-010` (default): Identity, money and handover-bound vendors sit behind an adapter the venture owns, with a written exit route.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How replaceable the vendor must be: contract clauses, sovereignty
  requirements, cost trajectories.
- Whether the seam receives attacker-shaped input, such as a webhook.
- Whether the vendor holds identity, money, or anything a handover
  obligation covers.
- How much of the SDK's value is protocol knowledge against
  convenience.
- Whether the vendor publishes a machine-readable schema you could
  generate from instead.

Applicability is `has_server_code`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. SDK throughout

Assume `A. SDK throughout` was selected and the outcome failed. Test this option's stated failure mechanism first: The exit cost grows with every import site. The SDK's version policy becomes yours. At a webhook it is attack surface with opinions about body parsing.

### Premortem for B. Owned adapter

Assume `B. Owned adapter` was selected and the outcome failed. Test this option's stated failure mechanism first: An interface to design and maintain, and the temptation to model it on the current vendor, which quietly defeats the point.

### Premortem for C. Raw protocol

Assume `C. Raw protocol` was selected and the outcome failed. Test this option's stated failure mechanism first: You maintain protocol knowledge, including replay tolerance and payload version pinning, and you re-learn it each time the vendor moves.

### Premortem for D. Generated client from the vendor's schema

Assume `D. Generated client from the vendor's schema` was selected and the outcome failed. Test this option's stated failure mechanism first: Only available where the vendor publishes a usable schema, and the generated surface is still theirs, so it needs B around it to be an exit rather than a coupling.

## Decision rule

Webhook verification and any signature checking: **C**, always, and B5
binds it. Identity, money, or anything contractually handover-bound:
**B** at minimum, with the exit route written where the decision
record lives and the venture's database staying the authorisation
truth. A vendor publishing a maintained schema, wrapped in B: **D** is
the cheaper way to keep B honest. Fringe conveniences with trivial
exits: **A** is tolerable. Anything with no documented exit route is a
deviation, not a default.

## Safe default

**B**, with **C** at every verification seam. Vendors are guests with
documented departure plans.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How replaceable the vendor must be: contract clauses, sovereignty requirements, cost trajectories.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** **B**, with **C** at every verification seam. Vendors are guests with documented departure plans.

**Exit condition:** Stop or roll back the selected branch when The exit cost grows with every import site. The SDK's version policy becomes yours. At a webhook it is attack surface with opinions about body parsing, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How replaceable the vendor must be: contract clauses, sovereignty requirements, cost trajectories.

## Counter-evidence and transfer limits

EV-0161 is vendor documentation, proprietary, and read as paraphrase
only. Its constants do not transfer: tolerances, header formats and
version-pinning semantics differ per vendor, so the rule that survives
is verify raw bytes, bound recency, pin the payload version. The
adapter default has no external evidence at all. Cockburn (EV-0150) is
the closest thing, and it argues for ports only where a second device
is genuinely plausible, which is a narrower claim than D7 makes.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
