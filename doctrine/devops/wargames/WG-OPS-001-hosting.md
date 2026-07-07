---
summary: Managed PaaS, a cloud estate under contract, or self-hosting?
type: wargame
tags: [ops, hosting, infra]
status: active
review_by: 2027-07
---

# WG-OPS-001: PaaS, a cloud estate, or self-hosting?

## The question

Where the venture runs decides its week-one velocity, its credibility
story, its residency posture and who holds the root account. The fork
returns whenever a contract, a trust audience or a cost trajectory
changes.

## It depends on

- Contractual clauses: residency, handover, "or compatible" platform
  requirements, joint infrastructure decisions.
- The trust audience: does anyone (insurers, enterprise buyers) judge
  the venture by where it runs?
- Operator bandwidth: who patches, who scales, who answers pages?
- Whose name is on the account: the venture's or the operator's?

## Options

### A. Managed PaaS
Railway, Vercel and kin. Fastest from zero, least ops, usage-priced.
Residency is take-what-you-get and the trust story is the vendor's,
not yours.

### B. A cloud estate under the venture's organisation
AWS or kin, region chosen, accounts owned by the venture's legal
entity, managed-container services (App Runner grade) to keep the ops
surface small, a documented route to heavier machinery. Costs setup
and modest ops literacy; buys residency, credibility and handover.

### C. Self-hosting
Your metal, your pager. Sovereign and cheap at scale; a standing ops
tax no solo-operator venture pays willingly.

## Decision rule

A contract or trust audience names residency, handover or a platform:
B, region ruled explicitly, accounts under the venture's entity, and
every non-estate service documented with reason, trade-off and
migration route. No such trigger: A, spend-guarded by WG-OPS-004,
with the B migration kept honest by containerising from day one
(WG-OPS-002). C only when sovereignty is the product.

## Default

A. Velocity first; the triggers announce themselves loudly when they
arrive.

## Worked rulings

- **WiseWattage (2026, argued)**: A. Railway for the API and database,
  Vercel for the fronts; solo velocity won, and the urllib3 deploy cap
  it taught lives in the stack profile.
- **AutoWatt (2026-07, argued)**: B. Its ADR-0002: AWS eu-west-2 under
  AutoWatt Ltd, App Runner containers, forced by the Heads of Terms
  (AWS-or-compatible, handover clauses) and the insurer trust story;
  every exception documented with a migration route.
