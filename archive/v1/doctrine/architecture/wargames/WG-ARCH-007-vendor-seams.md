---
summary: Vendor integration: their SDK everywhere, an owned adapter, or the raw protocol?
type: wargame
tags: [arch, infra, security]
status: archived
review_by: 2027-07
---

# WG-ARCH-007: SDK everywhere, an owned adapter, or the raw protocol?

## The question

Every vendor arrives with an SDK that wants to be imported everywhere,
and every vendor eventually changes terms, prices or existence. The
fork is how deep a vendor is allowed into the codebase, and it is
taken per vendor, per seam.

## It depends on

- How replaceable the vendor must be (contract clauses, sovereignty
  requirements, cost trajectories).
- The security surface: does the integration receive attacker-shaped
  input (webhooks) or hold the keys to identity or money?
- How much of the SDK's value is the protocol against convenience.

## Options

### A. SDK throughout
Import the vendor everywhere it is used. Fastest week one; the exit
cost grows with every import site.

### B. Owned adapter
One interface the venture owns, the SDK confined inside it, an exit
route documented (what replaces it, what migrates). The venture's own
store remains the source of truth for anything authoritative.

### C. Raw protocol
No SDK; the integration is standard-library code against the wire
format (HMAC verification, REST calls). Smallest attack surface and
no dependency; costs maintenance of protocol knowledge.

## Decision rule

Identity, money or anything contractually handover-bound: B at
minimum, with the exit route written where the contract or ADR lives,
and the venture's database staying the authorisation truth. Webhook
verification and signature checking: C; a vendor SDK is attack surface
there. Fringe conveniences with trivial exits: A is tolerable.
Anything without a documented exit route is a deviation, not a
default.

## Default

B. Vendors are guests with documented departure plans.

## Worked rulings

- **AutoWatt (2026-07, argued)**: B across the estate of exceptions in
  its ADR-0002, forced explicit by contract (each non-AWS service
  carries reason, trade-off and migration route; Clerk sits behind an
  adapter with the venture database as authz truth).
- **WiseWattage (2026, argued)**: C for webhooks (stdlib HMAC-SHA256,
  idempotency keys, no provider SDKs, its ADR-001), B for identity.
