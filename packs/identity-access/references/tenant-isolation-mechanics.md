---
summary: How a database row policy actually behaves, what walks past it, and the checklist for making a tenant boundary real
type: guide
tags: [auth, data, migrations]
kind: fact
scope: estate
volatility: slow
review: 2029-05
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
---

# Reference: tenant isolation mechanics

Level 3 detail behind binding requirement B2 and behind WG-IDENT-004.
Read this before switching on a row policy, because the feature is easy
to enable and easy to make inert.

## What a row policy does

The database evaluates a boolean expression for each row before the
query's own conditions are applied (PostgreSQL row security docs).
Policies can be written per command, so read and write can differ, and
they combine two ways: permissive policies are combined with or,
restrictive ones with and. A restrictive policy is the one to reach for
when the tenant predicate must hold in addition to everything else,
rather than as one more way to be allowed.

The point of the mechanism is that the predicate stops depending on any
author remembering it. That is the whole argument for B2.

## What walks straight past it

Four paths, all documented, all easy to leave open (PostgreSQL row
security docs):

1. **A superuser.** Nothing applies.
2. **Any role carrying the bypass attribute.** Granted for maintenance
   and rarely taken away.
3. **The table's owner, by default.** This is the important one, because
   the role an application connects as is very often the role that
   created the tables. Subjecting the owner to its own policies is a
   separate statement, issued per table, and a system that skipped it
   has policies that are present, documented and doing nothing.
4. **Referential integrity checks.** Unique constraints and foreign keys
   bypass policies by design, so a constraint violation can confirm that
   a row exists in a tenant the caller cannot read. That is a narrow
   channel and a real one: it turns an insert into an existence oracle.

There is a fifth, which is not a bypass but has the same effect:
**connection pooling that reuses one database role for every tenant**.
If the tenant is set on the connection rather than per transaction, the
next request served by that pooled connection inherits it. Set it per
transaction.

## What it costs, honestly

The vendor that hosts two of the databases offering this records
that the user's and the tenant's identity have to be propagated
from the request all the way into every query, that this is hard to
design, implement, test and maintain, and that many multi-tenant systems
therefore do not use the feature at all (Azure multitenancy guidance).
Take that as the real cost estimate rather than the vendor's most
optimistic one.

The places propagation is usually forgotten, in order of how often:
background jobs, scheduled tasks, data migrations, admin tooling, export
and reporting queries, and anything a person runs by hand against
production.

## Isolation is not authorisation

A tenant boundary answers "whose data is this". It does not answer "may
this person do this". A system can have a perfect boundary and still let
every member of a tenant delete every other member's records. The two
are separate controls and B1 and B2 are separate requirements for that
reason. Dedicated resources also still sit behind one shared onboarding
and operations path; if each customer gets its own version and its own
operational life, the thing has stopped being one system (AWS SaaS
Lens).

## Checklist before calling a boundary real

- The tenant comes from the authenticated credential, never from a
  parameter, header, subdomain or path segment.
- The application does not connect as the table owner, or the owner's
  exemption is switched off per table.
- No application role carries the bypass attribute.
- The tenant is set per transaction, not per connection.
- Every table holding tenant data is either covered by a policy, or in a
  per-tenant schema or store. There is a list, and it is generated from
  the catalogue rather than written by hand.
- Background jobs, migrations and exports set the tenant the same way
  the request path does.
- A test exists that reads with tenant A's credential and asks for
  tenant B's identifier, and expects nothing back. Under B5 that test
  ships with the change.
- The refusal is the same refusal used everywhere else, so the boundary
  is not also an existence oracle.

## Shapes to avoid

Two are named outright in the Azure multitenancy guidance: a table per
tenant inside one database, and a column added to the shared schema to
satisfy one customer. Both feel like small
accommodations and both stop the system scaling in the ordinary way, the
first by making every query and migration a loop over tenants, the
second by making the schema a record of past sales.

A third, from the same source: taking a dependency on exactly one schema
version, which removes the ability to migrate tenants at different times
and therefore the ability to roll one back.
