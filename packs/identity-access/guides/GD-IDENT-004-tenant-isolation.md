---
id: GD-IDENT-004
summary: Tenant isolation by application filter, by database row policy, by schema, or by a store per tenant?
kind: wargame
type: wargame
tags: [arch, auth, data, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-IDENT-002]
applies_when: [serves_multiple_tenants]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [pending-fragment-import]
review: 2029-01
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-IDENT-004: where does the tenant boundary live?

## Decision question and stakes

One system, several customers, and a guarantee that one cannot see
another. The fork is which layer holds that guarantee, because the layer
decides what a single mistake costs. A boundary held in the application
fails one query at a time. A boundary held by the database fails only if
somebody removes it.

Getting this wrong is described by one source as potentially
unrecoverable for the business it happens to (AWS SaaS Lens), which is a
fair description of telling a customer that another customer read their
data.

## Doctrines or coverage gap under pressure

- `DOC-IDENT-002` (default): The tenant boundary is enforced below the code that serves the request.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How many tenants now, and how many in two years? Three and fifty are
  different problems (Azure multitenancy guidance).
- Does any tenant need its own encryption keys, its own backup policy,
  its own data location, or its own restore? Each of those buys a
  dedicated store on its own.
- Does the venture need to report across all tenants, or attribute
  consumption per tenant for billing? Both get harder with every step
  towards separation.
- What is the hard scale ceiling of the single shared resource, and how
  far away is it?
- Can the application carry the tenant identity from the request into
  every query, including background jobs and migrations?

Applicability is `serves_multiple_tenants`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Shared tables, tenant column, filter in the application
Every row carries a tenant key and every query adds the condition. Buys
the highest density and the lowest cost, one schema to migrate and one
store to back up. Costs the guarantee: it now rests on every query ever
written, including the one added at half past five in a background job,
and the failure mode is exactly the one the 2025 list measures most of
(OWASP Top 10:2025). This option is the default state of any system that
has not decided, which is why it is listed first and not recommended
alone.

### B. Shared tables, tenant column, database row policy
Same schema, but the database applies the predicate before the query's
own conditions, so a forgotten condition changes nothing (PostgreSQL row
security docs). Buys a boundary a handler cannot forget. Costs
propagation and care. The tenant has to be set per transaction rather
than per connection wherever pooling reuses one database role, and the
bypass paths have to be closed deliberately: a superuser, any role
holding the bypass attribute, and by default the table's own owner,
which is the role most applications connect as. Constraint checks bypass
policies by design, so a unique or foreign key violation can still
confirm that a row exists in another tenant. The vendor that hosts two
of the databases offering this is candid that carrying identity into
every query is hard enough that many multi-tenant systems skip the
feature (Azure multitenancy guidance).

### C. Schema per tenant
One database, one schema each, the connection scoped to a schema. Buys a
boundary that is easy to reason about and per-tenant restore that is
merely awkward rather than impossible. Costs migration work that scales
with tenant count and a catalogue that grows with it, and cross-tenant
reporting becomes a union nobody enjoys writing.

### D. Database or full stack per tenant
Dedicated resources, up to and including a separate deployment (AWS SaaS
Lens). Buys the strongest boundary, per-tenant keys, locality and backup
policy, and a blast radius of one. Costs the economics: the most
expensive shape per tenant and the most work to operate. What stops it
being a managed service is that onboarding, identity and operations stay
shared; the moment each customer gets its own version and its own
operational life, the model's advantages are gone.

### E. Mixed, per component
Some components dedicated, some shared, chosen per component by its
regulatory profile and its noisy-neighbour behaviour (AWS SaaS Lens).
Buys proportion. Costs a decision per component and the discipline to
record which is which.

## Failure premises

### Premortem for A. Shared tables, tenant column, filter in the application

Assume `A. Shared tables, tenant column, filter in the application` was selected and the outcome failed. Test this option's stated failure mechanism first: , one schema to migrate and one store to back up. Costs the guarantee: it now rests on every query ever written, including the one added at half past five in a background job, and the failure mode is exactly the one the 2025 list measures most of (OWASP Top 10:2025). This option is the default state of any system that has not decided, which is why it is listed first and not recommended alone.

### Premortem for B. Shared tables, tenant column, database row policy

Assume `B. Shared tables, tenant column, database row policy` was selected and the outcome failed. Test this option's stated failure mechanism first: propagation and care. The tenant has to be set per transaction rather than per connection wherever pooling reuses one database role, and the bypass paths have to be closed deliberately: a superuser, any role holding the bypass attribute, and by default the table's own owner, which is the role most applications connect as. Constraint checks bypass policies by design, so a unique or foreign key violation can still confirm that a row exists in another tenant. The vendor that hosts two of the databases offering this.

### Premortem for C. Schema per tenant

Assume `C. Schema per tenant` was selected and the outcome failed. Test this option's stated failure mechanism first: migration work that scales with tenant count and a catalogue that grows with it, and cross-tenant reporting becomes a union nobody enjoys writing.

### Premortem for D. Database or full stack per tenant

Assume `D. Database or full stack per tenant` was selected and the outcome failed. Test this option's stated failure mechanism first: the economics: the most expensive shape per tenant and the most work to operate. What stops it being a managed service is that onboarding, identity and operations stay shared; the moment each customer gets its own version and its own operational life, the model's advantages are gone.

### Premortem for E. Mixed, per component

Assume `E. Mixed, per component` was selected and the outcome failed. Test this option's stated failure mechanism first: a decision per component and the discipline to record which is which.

## Decision rule

- Any system with more than one tenant, always: B as the floor, not A. A
  is what B degrades to when somebody forgets, which is the argument for
  having B underneath.
- Where the store offers no row policy: C, because the only remaining
  alternative is A and A has no floor.
- A tenant needing its own keys, its own data location, its own backup
  or restore policy: D for that tenant, bought per requirement rather
  than per customer.
- Regulatory separation, or a tenant whose load would harm the others: D
  for that tenant, or E if the requirement is limited to one component.
- Cross-tenant reporting is needed and there is no warehouse: weigh it
  before C or D, because it is the cost that arrives last and is hardest
  to reverse.
- Never a table per tenant inside one database, and never a column added
  to satisfy one customer. Both are named as shapes to avoid and both
  stop the system scaling (Azure multitenancy guidance).
- The tenant always comes from the authenticated credential. A tenant
  read from a parameter, a header or a subdomain is not a boundary, it
  is a suggestion.

## Safe default

B, escalating to C, D or E per requirement. Density is cheap and
separation is bought one requirement at a time. Whichever is chosen, the
venture writes down which layer holds the guarantee: "the application
filters by tenant" and "the database refuses" are different promises and
only one survives a forgotten query.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How many tenants now, and how many in two years? Three and fifty are different problems (Azure multitenancy guidance).** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B, escalating to C, D or E per requirement. Density is cheap and separation is bought one requirement at a time. Whichever is chosen, the venture writes down which layer holds the guarantee: "the application filters by tenant" and "the database refuses" are different promises and only one survives a forgotten query.

**Exit condition:** Stop or roll back the selected branch when , one schema to migrate and one store to back up. Costs the guarantee: it now rests on every query ever written, including the one added at half past five in a background job, and the failure mode is exactly the one the 2025 list measures most of (OWASP Top 10:2025). This option is the default state of any system that has not decided, which is why it is listed first and not recommended alone, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How many tenants now, and how many in two years? Three and fifty are different problems (Azure multitenancy guidance).

## Counter-evidence and transfer limits

The vocabulary everyone uses for this fork comes from a 2020 whitepaper
its own publisher now marks as historical (AWS SaaS Lens). The naming
survives; the engineering behind it is not maintained, which is a reason
to treat the three words as a way to talk rather than as current advice.

The default is also in tension with its own best source. Pushing the
predicate into the database is the mechanism most likely to hold, and
the vendor that hosts two of the databases offering it reports that the
propagation cost drives teams away (Azure multitenancy guidance). A
control that is correct and unused is worth less than a weaker one that
ships, which is why B2 names the outcome and allows three mechanisms
while this guide argues for one.

Nothing in the source set measures cross-tenant leak rates by isolation
model. There is no evidence that B produces fewer incidents than A. The
argument for it is structural, that A has no floor, and structural
arguments have been wrong before.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
