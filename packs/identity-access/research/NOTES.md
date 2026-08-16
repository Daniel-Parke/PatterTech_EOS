---
summary: Research synthesis for the identity, authorisation and tenancy pack, the model fork, what should bind, and the predicates proposed
type: example
tags: [eos]
---

# Identity, authorisation and tenancy: what the evidence supports

Research cutoff 2026-08-15. Fifteen sources are proposed in
`packs/identity-access/research/sources.fragment.json`, each fetched at
that date and abstracted in our own words. Nothing here is carried
verbatim from a source.

The gap this pack fills is recorded in `registry/coverage.json` under
the capability `identity-authorisation-and-tenancy`: no guide anywhere
in `packs/` argued role-based against attribute-based against
relationship-based authorisation. That is the fork WG-IDENT-001 settles.

**How the pack cites these.** Fragment ids remain in this pre-import
record and its fragments. The completed import assigned `EV-0517`
through `EV-0531`; the read surface now cites those canonical identities
and check S014 refuses a fragment identity or unresolved placeholder
there. The mapping from readable name to source remains in
`packs/identity-access/PACK.md`.

## Why the pack exists at all

FRAG-IDENTITY-ACCESS-01 puts broken access control first out of ten in
the 2025 list, over 2.8 million applications tested, 1.84 million
occurrences and about 33,000 mapped CVEs. The named failure shapes are
not exotic: no deny-by-default, an identifier in a URL nobody checks,
write verbs unguarded where read verbs were guarded, claims in a token
trusted without verification. That is the argument for a pack rather
than a paragraph, and it is also the argument for keeping the pack's
binding requirements dull.

Read the ranking with its limit in hand. Incidence counts what testers
and tools find, not what attackers exploit or what a breach costs, and
two of the ten categories are voted rather than measured.

## The model fork, and the disagreement inside it

**Roles.** FRAG-IDENTITY-ACCESS-03. Standardised as INCITS 359, revised
in 2012, still current. The published benefit is administrative, not
expressive: provisioning, deprovisioning, less downtime. The standard
carries hierarchies and mutually exclusive roles, so the common claim
that roles cannot express separation of duties is wrong about the
standard even where it is right about a given implementation.

**Attributes.** FRAG-IDENTITY-ACCESS-04. The decision reads attributes
of subject, object, operation and environment against a written rule.
Wider than roles by construction, and only as good as the attributes,
which have to be sourced, kept current and trusted. The canonical
official definition has not been revised since 2019.

**Relationships.** FRAG-IDENTITY-ACCESS-05 and 06. A tuple says a user,
or a set of users named by another object and relation, stands in a
named relation to an object; rewrite rules derive relations from other
relations. That expresses nested groups, folder inheritance and sharing
with somebody who holds no role at all. FRAG-IDENTITY-ACCESS-06 makes it
buyable rather than buildable.

The disagreement worth carrying is between FRAG-IDENTITY-ACCESS-02 and
FRAG-IDENTITY-ACCESS-03. The OWASP page prefers attributes and
relationships over roles and names role explosion as the reason. The
NIST project page's whole case for roles is administrative saving in
large organisations with formal joiner-mover-leaver processes. Both are
right about different questions, and the reconciliation is the useful
part: roles are an administration model, attributes and relationships
are decision models, and a venture that has no provisioning process has
none of the benefit roles are actually evidenced for.

The fourth position, named so it can be rejected as a destination rather
than as a start: **ownership checks written per handler**. It is the
correct beginning for a system with one kind of user, and it is exactly
what FRAG-IDENTITY-ACCESS-01 measures failing, because the check has to
be repeated everywhere and only has to be forgotten once.

## Where the decision is made

FRAG-IDENTITY-ACCESS-07 supplies the vocabulary: enforcement point,
decision point, information point, administration point. Its value is
not the XML, which is thirteen years unrevised and out of fashion. It is
that naming the four makes it obvious when one of them is nowhere, and
that a decision has four outcomes rather than two, so the case where
evaluation fails has to be given an answer instead of falling through.

FRAG-IDENTITY-ACCESS-05 is the counterweight on latency and coupling: a
central decision service is a dependency on the request path, and its
consistency guarantee costs the client real work, a token stored with
each content version and passed back on the check. A client that skips
that quietly loses the property the whole design exists for.

## Session against token

FRAG-IDENTITY-ACCESS-11 gives the cookie session its property list:
entropy from a cryptographic generator, secure and script-inaccessible
cookies with a cross-site restriction, a fresh identifier on any
privilege change, both an idle limit and an absolute limit, and
invalidation on the server at logout. It is direct that session
credentials do not belong in browser storage script can read.

FRAG-IDENTITY-ACCESS-08 gives the token side its warning: a bearer token
is a password with an expiry, so the current practice pushes towards
binding the token to the client that was issued it. Two grants are
effectively closed, the password grant and issuing tokens straight back
in an authorisation response, and a public client's refresh token must
be bound or rotated.

FRAG-IDENTITY-ACCESS-09 names the integration bug that keeps recurring:
the identity token is a statement to one named client that somebody
authenticated, and the access token is what a resource server accepts.
Forwarding the first as if it were the second builds an authentication
system with no audience check where it matters.

FRAG-IDENTITY-ACCESS-10 supplies the numbers behind session lifetime,
graded by assurance level from a month down to hours, and two positions
worth carrying: phishing resistance means the authenticator is bound to
the session, so anything a person retypes is not phishing-resistant, and
telephone-network authentication is restricted rather than forbidden and
obliges you to offer something else too.

## Tenancy

FRAG-IDENTITY-ACCESS-14 gives the vocabulary, dedicated against shared
against mixed, applied per component rather than per system, with the
sharp point that dedicated resources still sit behind one shared
onboarding and operations path or the thing is a managed service.

FRAG-IDENTITY-ACCESS-13 gives the trade in dull terms: hard scale
ceilings, per-tenant keys, backup policies, data location, and whether
consumption can be attributed for billing. It names two shapes to avoid
outright, a table per tenant inside one database and a column added for
one customer.

FRAG-IDENTITY-ACCESS-12 gives the mechanics of pushing the tenant
predicate below the application, and the list of things that walk past
it: superuser, the bypass attribute, and by default the table's own
owner, which is the role most applications connect as. Referential
integrity checks bypass policies by design, so a constraint can confirm
the existence of a row the querying tenant cannot see.

The honest tension: FRAG-IDENTITY-ACCESS-13 reports that carrying the
user's and tenant's identity into every query is hard enough that many
multi-tenant systems do not use row-level security at all. So the
control most likely to hold is also the one most likely to be skipped. A
pack that ignores that ships a rule nobody follows.

## Break-glass

FRAG-IDENTITY-ACCESS-15 is the only source here on emergency access and
it is vendor guidance, declared AI-assisted, for one directory product.
The shape survives translation: two or more accounts, no dependency on
the identity provider whose outage is one reason the path exists,
credentials held by the organisation rather than a person, a different
authentication method from the everyday one, standing rather than
on-request privilege, an alert on every sign-in, a review after every
use, and a test at least every ninety days. Its own trade is stated
plainly: these accounts are excluded from the policies that restrict
everyone else, so break-glass buys detection with prevention.

## What should bind, what should default, what is preference

**Binding.** Deny by default and decide on every request at one trusted
layer (02, 01). Enforce the tenant boundary below the code that serves
the request (13, 12, 14). Validate identity claims before trusting them,
audience included (09, 08). Name, time-box and alarm the break-glass
path (15). Ship an authorisation change with the test that proves the
wrong actor is refused (01, 02).

**Default.** Start with ownership plus a small role set; move to
relationships when sharing crosses the ownership tree and to attributes
when the rule depends on facts about the record or the environment (02,
03, 04, 05). One decision point, in process, until latency or reuse
argues otherwise (07). Server-side sessions with cookies for first-party
browser surfaces, tokens for anything else (11, 08). Delegate
authentication to a provider (08, 09, 10). Shared tables with a tenant
key plus a database-enforced predicate, until a tenant's own keys,
locality or backup policy buys them a dedicated store (13, 12).

**Preference.** Which policy engine. Whether roles are rows or an enum.
Whether a refusal answers 403 or 404, so long as the choice is one
choice. Session and token lifetimes inside the graded ranges.

## Anti-patterns to name in the pack

- The check written per handler, forgotten on the fourth one (01).
- A role invented because the rule needed an attribute (02, 04).
- A tenant identifier taken from the request rather than the credential.
- Row-level security switched on while the application still connects as
  the table owner (12).
- The identity token forwarded to an API as a credential (09).
- A break-glass account that is somebody's personal administrator login,
  and one that nobody has signed into for a year (15).
- Buying a relationship engine to express five permissions (05, 06).
- Reporting a permission model as tested when only the allow paths have
  tests (01).

## Predicates proposed

The vocabulary in `kernel/PREDICATES.md` is integrator-owned, so these
are proposals. Check S021 fails on them until the integrator adds the
rows, which is expected and is not this lane's to fix.

| predicate | true when | settled by |
| --- | --- | --- |
| `authenticates_people` | a person proves who they are to the venture before it acts for them, whether the venture checks the credential itself or delegates it | 6 |
| `serves_multiple_tenants` | one running system holds data for more than one customer organisation, and one customer must not see another's | 2 |
| `has_privileged_access_path` | an account or route exists that can reach data or actions it does not own, including administrator, support impersonation and break-glass | 11 |
| `changes_authorisation_rule` | the work adds or changes a permission, a role, a policy or a tenant scope | task |

Group placement, following the file's own instruction to put a row in
the group its subject belongs to: `authenticates_people` and
`has_privileged_access_path` belong in a new group for identity and who
may act, and `serves_multiple_tenants` sits with the shape of the
system, next to `has_database`. `changes_authorisation_rule` is a task
fact and sits with code and how it changes, next to `edits_source`.

Three existing predicates are adjacent and were considered and rejected
as this pack's gate, which is worth recording so the fourth person to
look does not reopen it:

- `hosts_service` (5) is true of every networked venture, including one
  with no login at all. Using it would activate this pack for work that
  has no authorisation question in it, which is the over-activation
  `packs/PACK_CONTRACT.md` is trying to prevent.
- `holds_credentials` (14) is about the venture holding key material. A
  venture can authenticate thousands of people through a provider and
  hold no secret of its own beyond a client credential, and a venture
  can hold a deployment key and authenticate nobody.
- `handles_personal_data` (9) is about data protection duties. It is
  usually true wherever `authenticates_people` is true, and it is the
  gate for a different pack's requirements. Merging them would be the
  ADR-0010 mistake in reverse: one name for two facts rather than two
  names for one.

The pack cites all three where the subjects meet, and gates on none of
them.

## Refresh triggers

Re-run this research on any of: a new OWASP Top 10 edition; a revision
of NIST SP 800-162, which is the stale one in this set; a published
independent evaluation of relationship-based authorisation against roles
or attributes, which does not exist today; OpenFGA graduating or being
archived; an OAuth security best-current-practice update; a PostgreSQL
release that changes row-security bypass rules; AWS replacing the
withdrawn tenant isolation whitepaper.
