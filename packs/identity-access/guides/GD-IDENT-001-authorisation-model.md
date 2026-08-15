---
id: GD-IDENT-001
summary: Ownership checks, roles, attributes or relationships? The fork the coverage matrix recorded as missing
kind: wargame
type: wargame
tags: [arch, auth, eos, security, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-IDENT-001]
applies_when: [authenticates_people]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [pending-fragment-import]
review: 2028-10
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-IDENT-001: what decides whether this person may do this thing?

## Decision question and stakes

Every system with more than one kind of user meets this fork, usually in
the week the second kind arrives. The question is not which model is
best. It is what the decision is allowed to depend on, because that is
what separates the four options and it is what costs to change later.
`registry/coverage.json` recorded this argument as absent from the
packs. This guide is it.

## Doctrines or coverage gap under pressure

- `DOC-IDENT-001` (binding): Deny unless something permitted, and decide at one layer.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- What does the rule actually depend on? Who the person is, what the
  record is, or who the person is to that record?
- Can a user grant access to another user without an administrator? That
  single question decides more than any other here.
- Is there a joiner-mover-leaver process, or does one person add accounts
  by hand?
- Does anyone have to answer "who can see this record" or "what can this
  person see"? Some models make one of those very expensive.

Applicability is `authenticates_people`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Ownership checks in the handler
Each operation checks that the record belongs to the caller, or that the
caller is an administrator. Buys immediate correctness with no
machinery, and it is the right starting point for a system with one kind
of user. Costs repetition: the check has to be written everywhere and
only has to be forgotten once. This is the shape the largest measured
defect class mostly takes, and its named forms are exactly the forgotten
cases, unguarded write verbs and identifiers nobody checks belong to the
caller (OWASP Top 10:2025). A fine start, a poor destination.

### B. Roles
The person holds one or more roles; the role carries permissions; the
check asks whether any held role permits the operation. Standardised as
INCITS 359, revised in 2012 and still current, with hierarchies and
mutually exclusive roles in the standard for the cases people assume
roles cannot do (NIST RBAC project). Buys an administration model a
non-engineer can operate, and one place to look when someone leaves; the
published saving is in provisioning and downtime, not in fewer defects.
Costs a role per exception: the moment a permission depends on anything
other than who the person is, the only way to express it is a new role,
and the set grows past what anyone can reason about (OWASP authorization
guidance).

### C. Attributes
The decision evaluates attributes of the subject, of the record, of the
operation and sometimes of the environment against a written rule (NIST
SP 800-162). Buys expression: department, record classification, time of
day, request origin, all without inventing a role, and it puts the
policy somewhere a person can read. Costs attribute supply: the decision
is only as good as the attributes, and each has to come from somewhere,
be current and be trusted. Answering "what can this person see" now
means evaluating a rule against every record.

### D. Relationships
Access is derived from stored relations: this user is an editor of this
document, this document is in that folder, members of that group view
that folder. Rewrite rules turn one relation into another, so
inheritance and nested groups fall out of the model rather than being
special cases (Zanzibar). Buys the thing roles and attributes both
express badly: a user sharing a specific record with a specific other
user, with no administrator and no new role. Available as ordinary
open-source software rather than as something to build (OpenFGA). Costs
a second stateful service on the request path, a set of tuples that must
stay in step with the application's own data, and a consistency problem
that is real: revoke access and then add content, and the removed user
can see the new content unless the check respects the causal order,
which the design solves by making the client store a token per content
version and pass it back (Zanzibar).

## Failure premises

### Premortem for A. Ownership checks in the handler

Assume `A. Ownership checks in the handler` was selected and the outcome failed. Test this option's stated failure mechanism first: repetition: the check has to be written everywhere and only has to be forgotten once. This is the shape the largest measured defect class mostly takes, and its named forms are exactly the forgotten cases, unguarded write verbs and identifiers nobody checks belong to the caller (OWASP Top 10:2025). A fine start, a poor destination.

### Premortem for B. Roles

Assume `B. Roles` was selected and the outcome failed. Test this option's stated failure mechanism first: a role per exception: the moment a permission depends on anything other than who the person is, the only way to express it is a new role, and the set grows past what anyone can reason about (OWASP authorization guidance).

### Premortem for C. Attributes

Assume `C. Attributes` was selected and the outcome failed. Test this option's stated failure mechanism first: attribute supply: the decision is only as good as the attributes, and each has to come from somewhere, be current and be trusted. Answering "what can this person see" now means evaluating a rule against every record.

### Premortem for D. Relationships

Assume `D. Relationships` was selected and the outcome failed. Test this option's stated failure mechanism first: a second stateful service on the request path, a set of tuples that must stay in step with the application's own data, and a consistency problem that is real: revoke access and then add content, and the removed user can see the new content unless the check respects the causal order, which the design solves by making the client store a token per content version and pass it back (Zanzibar).

## Decision rule

- One kind of user, records with one owner, no sharing: A. Do not
  install a model to express "it is mine".
- Two to about six kinds of user, permissions that depend only on which
  kind: B, with the roles held as data rather than compiled in, so the
  set can be read and audited.
- A rule that depends on a property of the record or of the request
  rather than of the person: C for that rule. Do not answer it with a
  role, because the role you invent will encode the property in its name
  and nothing will be able to query it.
- Users share individual records with individual users, or permission is
  inherited down a container tree: D. This is the case A, B and C all
  handle by growing something unbounded, and it is the strongest reason
  in this guide to change model.
- Regulated separation of duties, or a permission set the customer
  configures and audits: B plus C, with the mutually exclusive role
  machinery the standard already carries.
- Mixed is normal. Roles for the coarse question of what kind of user
  this is, relationships or attributes for the fine one. What is not
  normal is two mechanisms both able to grant the same permission.

## Safe default

A plus a small fixed role set, and move only when a real rule cannot be
expressed. The cost of the wrong model is paid in migration, not in
bugs, so the cheap move is to keep the check in one place from the
start, which B1 requires anyway, and change what that one place
consults. A venture that has done that can change model in a week; one
that has spread checks through its handlers cannot.

Do not read the default as a preference for roles on the merits. It is a
preference for not buying a model before the rule that needs it exists.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **What does the rule actually depend on? Who the person is, what the record is, or who the person is to that record?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A plus a small fixed role set, and move only when a real rule cannot be expressed. The cost of the wrong model is paid in migration, not in bugs, so the cheap move is to keep the check in one place from the start, which B1 requires anyway, and change what that one place consults. A venture that has done that can change model in a week; one that has spread checks through its handlers cannot. Do not read the default as a preference for roles on the merits. It is a preference for not buying a model before the rule that needs it exists.

**Exit condition:** Stop or roll back the selected branch when repetition: the check has to be written everywhere and only has to be forgotten once. This is the shape the largest measured defect class mostly takes, and its named forms are exactly the forgotten cases, unguarded write verbs and identifiers nobody checks belong to the caller (OWASP Top 10:2025). A fine start, a poor destination, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: What does the rule actually depend on? Who the person is, what the record is, or who the person is to that record?

## Counter-evidence and transfer limits

There is no controlled comparison of these models, and the two published
opinions point opposite ways. OWASP prefers attributes and relationships
and gives no measurement for the preference (OWASP authorization
guidance); the standards position values roles for an administrative
saving in large organisations with formal provisioning (NIST RBAC
project), which is the dimension a small venture has least of.

The relationship evidence is one company's production report with no
control arm, at a scale nothing here shares, and its own lessons section
reports hot spots as a critical availability problem needing caching,
prefetch and deduplication to contain (Zanzibar). The attribute
definition of record has not been revised since 2019 and predates the
relationship systems now in production (NIST SP 800-162).

So the rule above is argued from what each model can express and what it
costs to change, not from evidence that one produces fewer defects. If
an independent evaluation is published, this guide moves first.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
