---
summary: The pack applied end to end to one feature, sharing a report outside the ownership tree, on a system with two tenants
type: example
tags: [auth, arch, data]
kind: example
scope: estate
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
---

# EX-IDENT-001: the share that crosses the ownership tree

One feature, one agent, this pack loaded and nothing else. The system is
a hosted web application with two paying customers. It has users,
reports owned by users, an owner role and a member role, and one
PostgreSQL database with a tenant column on every table. Nothing has
gone wrong yet.

The task: let a user share a report with a named colleague, and give
support a way to look at a customer's report when they raise a ticket.

## Step 0: activation

Path triggers fire on the permissions module and the tenant module. The
task type is "adding a second kind of access to a record" and "adding a
support view that reads somebody else's records".
`authenticates_people`, `serves_multiple_tenants`,
`has_privileged_access_path` and `changes_authorisation_rule` are all
true, so every binding requirement in the pack applies to this one task,
which is unusual and worth noticing.

Routing: the change lands on the `auth-surface` factor in
`kernel/POLICY_SPEC.md`, which floors it at R2. The report contains
customer names, so the personal data factor is live too and the security
and privacy pack activates alongside this one.

## Step 1: the model question, and resisting the easy answer

The obvious implementation is a new role, `report_viewer`. WG-IDENT-001
says no, and the reason is worth stating rather than asserting: the
permission does not depend on who the person is, it depends on who the
person is to that report. A role expressing that would have to be one
role per report, which is the role explosion named in the OWASP
authorization guidance.

The second obvious implementation is an attribute: put a list of user
identifiers on the report and check membership. That is a relationship
in a trench coat, and it works, which matters. The Wargame's decision rule
sends sharing to option D, relationships, but it also says the cost of
the wrong model is paid in migration rather than in bugs.

The ruling for this feature: a `report_share` table, holding report,
user and relation. That is a relation tuple in the shape Zanzibar
describes, stored in the venture's own database, with no second service
on the request path. If sharing later grows folders, groups and
inheritance, the tuples are already the right shape and the migration is
to an engine rather than to a new model. Buying the engine now, for one
relation, would be the anti-pattern the pack names.

Recorded in the lock-book as a ruling on WG-IDENT-001, with that
sentence about migration as the reason.

## Step 2: one decision point

The existing code checks ownership inline in three handlers. B1 says one
layer, and this change would make it four. So the first commit moves the
three existing checks into a single `can(user, action, report)` function
and leaves behaviour identical, and the second commit adds sharing to
that one function.

This is the cheap move
`packs/identity-access/references/decision-point-placement.md` argues for: in
process, no network hop, and reversible. It also means the negative
tests in step 5 have one thing to aim at.

The function returns a denial when no rule matches and a denial when
evaluation fails, and the second case logs loudly. A silent deny on
error is indistinguishable from a correct refusal and will be diagnosed
as a permissions bug for as long as it lasts.

## Step 3: the tenant boundary, which nearly broke

The share is between two users, and nothing in the first draft stopped
those users being in different tenants. The draft would have let a user
share a report with anyone whose user identifier they could guess,
across the boundary, through a feature designed to grant access.

B2 catches it, and the fix is at two layers rather than one:

- The application refuses a share where the target user's tenant does
  not match the report's tenant, and returns the same refusal it returns
  for a report that does not exist.
- The row policy on `report_share` carries the tenant predicate as a
  restrictive policy, so the row cannot be written even if the
  application check is removed later.

Then the checklist in
`packs/identity-access/references/tenant-isolation-mechanics.md` runs, and two
items fail. The application connects as the role that created the
tables, so every policy in the database is inert; the fix is one
statement per table forcing the owner under its own policies. And the
nightly export job sets the tenant on the connection rather than per
transaction, so under the pooler it can inherit the previous request's
tenant. Neither defect was introduced by this feature. Both were found
because this feature made somebody read the list (PostgreSQL row
security docs).

One residual risk is recorded rather than fixed: the unique constraint
on `report_share` bypasses row policies, so a share attempt can confirm
that a report identifier exists in another tenant. Mitigation is to
check tenancy before the insert, which the application now does, and the
residual is written into the lock-book rather than left implicit.

## Step 4: the support view, which is a cross-tenant read

Support needs to see a customer's report. That is B2's boundary being
crossed on purpose, so it is B4's problem rather than B2's.

What ships: a named support role, a view that requires an open ticket
identifier and records it, an entry per use carrying who, when, which
ticket and which report, an alert to the operator on every use, and a
weekly read of that list. Impersonation is refused for this feature,
because a record saying the customer opened their own report when
support did is worse than no record.

The break-glass account is a separate matter and predates this task, but
the review notices it is federated through the identity provider, which
property 2 in `packs/identity-access/references/break-glass.md` rules out:
provider outage is one of the reasons the path exists (Entra emergency
access guidance). That is filed as its own task rather than folded into
this change, because it is not this feature's fault and hiding it inside
an unrelated diff is how it stops getting fixed.

## Step 5: the tests that prove the refusals

B5 wants the refusals, and this feature ships five:

1. A member of tenant B requests a report of tenant A by identifier and
   gets the same answer as for a report that does not exist.
2. A user shares with a target in another tenant and is refused.
3. The row policy refuses the same insert with the application check
   removed, which is the test that proves the second layer exists.
4. A user with a read share attempts to write and is refused.
5. The support view without a ticket identifier is refused.

The allow paths get tests too, but they were never the risk. A
permission model with only allow tests passes everything it has and
still lets the wrong person in, which is what the measured defect class
mostly is (OWASP Top 10:2025).

## Step 6: the token, briefly

The front end holds a session cookie and the sharing call is
first-party, so WG-IDENT-002 option A already applies and nothing
changes. One thing is checked anyway, because it is the recurring bug:
the service does not accept the identity token from the provider as a
credential, and the audience check happens where the session is
established rather than per call (OpenID Connect Core). It was already
correct. The check took two minutes and would have been expensive to
discover later.

## What made this work

Nothing here depended on anyone being clever about security. The role
was avoided by asking what the rule depends on. The cross-tenant share
was caught by a rule that says the boundary lives below the handler. The
inert policies were found by reading a checklist. The support view was
designed rather than improvised because a requirement said every
privileged path is named.

The one judgement call was step 1, and it went against the Wargame's first
preference on purpose: relationships in the venture's own database
rather than a relationship engine, because the shape is what matters and
the service is what costs. That is written down as a ruling with a
reason, which is the difference between a decision and a habit.
