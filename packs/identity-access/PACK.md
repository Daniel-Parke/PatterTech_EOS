---
summary: Authenticating people, deciding what each may do, and keeping one tenant out of another's data
type: guide
tags: [auth, security, arch, state]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [authenticates_people, serves_multiple_tenants, has_privileged_access_path, changes_authorisation_rule]
activation_paths: [**/auth/**, **/authz/**, **/*authoriz*/**, **/*authoris*/**, **/permissions/**, **/*permission*/**, **/roles/**, **/*rbac*/**, **/policies/**, **/*.rego, **/*.cedar, **/tenants/**, **/*tenant*/**, **/*session*/**, **/*login*/**, **/*oauth*/**, **/*oidc*/**, **/*saml*/**]
volatility: slow
review: 2029-02
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
---

# Identity, authorisation and tenancy

This pack owns who a person is, what they may do, and whose data they
may touch. It activates when a venture authenticates people, serves more
than one customer from one system, holds a privileged access path, or
changes an authorisation rule. It carries five binding requirements, a
short set of defaults you may override with a recorded reason, and four
decision guides. Secrets, injection, personal data and approval before
external action stay with the security and privacy pack.

## Activation

**Path triggers.** Authentication and authorisation modules, permission
and role definitions, policy files including engine-specific ones,
tenant modules, session handling, login and sign-up surfaces, and
anything named for OAuth, OpenID Connect or SAML.

**Task-type triggers.** Adding a login. Adding a second kind of user.
Adding a customer whose data must not mix with another's. Adding an
administrator or support view that reads somebody else's records.
Changing what a role or a policy permits. Adding an endpoint that takes
a record identifier from the caller. Integrating an identity provider.
Designing the schema for anything a tenant owns.

**Keyword fallback**, used only when paths and task type miss: role,
permission, policy, tenant, multi-tenant, session, token, JWT, scope,
claim, impersonation, break-glass, least privilege, SSO.

**Applicability predicates.** The four in the front matter:

- `authenticates_people`: a person proves who they are before the
  venture acts for them, whether it checks the credential itself or
  delegates.
- `serves_multiple_tenants`: one running system holds data for more than
  one customer organisation and one must not see another's.
- `has_privileged_access_path`: an account or route can reach data or
  actions it does not own.
- `changes_authorisation_rule`: this piece of work adds or changes a
  permission, a role, a policy or a tenant scope.

None true means the pack stays at level 1 and costs one paragraph. Any
true loads this body. A binding requirement whose own predicate is false
does not apply, and each requirement names the predicate it needs. The
predicates are proposed in `packs/identity-access/research/NOTES.md` and
are the integrator's to add to `kernel/PREDICATES.md`.

**Policy routing.** These triggers do not set a tier. Authorisation work
lands on the `auth-surface` factor in `kernel/POLICY_SPEC.md`, which
floors at R2, and personal data or key material can raise it further.
Action-time verdicts come from `kernel/GUARD_SPEC.md`.

**What is not here.** This pack does not restate
`packs/security-privacy/PACK.md`. Secrets and their scanning, prompt
injection and the instruction-source boundary, lawful basis and
complaints routes, and operator approval before a consequential external
action are all that pack's. Where the subjects meet, this one cites
rather than repeats: a token is a credential, so its storage is that
pack's B4; an identity provider is an external dependency, so sending
anything to it is that pack's B6; a user record is personal data, so its
lawful basis is that pack's B5.

## Outcomes and non-goals

Outcomes this pack is accountable for:

- No request reaches data or an action without something having decided
  it may, and the decision fails closed.
- A tenant cannot read, write or infer the existence of another tenant's
  records, and the guarantee does not rest on every handler being
  written correctly.
- A credential presented to the venture is checked for what it is, who
  issued it, who it was issued to and whether it has expired.
- Every path that reaches data it does not own is named, and its use
  leaves a record somebody reads.
- The authorisation model in use is the one that was argued for, and the
  argument is written down where the next person will find it.

Non-goals. This pack does not choose an identity vendor for you and
holds no opinion on any vendor's commercial terms. It is not a
compliance programme and issues no attestation. It does not design
cryptography, does not cover machine-to-machine trust inside a cluster,
and does not cover physical or network access control. It says nothing
about consent, lawful basis or data subject rights, which are the
security and privacy pack's. It does not describe an enforcement
adapter, because this repository has none for these rules: everything
below is a rule for a venture's own pipeline and its own reviewers.

## Binding requirements

Five. Each names the failure it prevents, the predicate it needs and the
evidence behind it. Basis per rule: B1, B3 and B5 standard, on the 2025
list and the protocol specifications; B2 and B4 decision, on vendor
documentation plus this estate's own ruling.

**B1. Deny unless something permitted, and decide at one layer.** Every
request that reads or changes data resolves an authorisation decision
before it touches the data, and the decision is made on the server from
the authenticated identity, never from a value the caller supplied. The
check runs at one layer every request passes through, not per handler. A
decision that cannot be evaluated is a denial, not a gap. Predicate:
`authenticates_people`. Prevents: the largest measured defect class in
web software, whose named shapes are a missing check rather than a
clever bypass (OWASP Top 10:2025, OWASP authorization guidance). Getting
it right on most requests is the same as getting it wrong.

**B2. The tenant boundary is enforced below the code that serves the
request.** Where one system holds more than one customer's data, the
tenant predicate is applied by the storage layer, by a separate schema
or by a separate store, so that one forgotten condition in one query
cannot cross the boundary. The tenant is taken from the authenticated
credential and never from a parameter, a header or a path segment the
caller controls. Where a database row policy is the mechanism, the
bypass paths are closed in the same change: the application does not
connect as the table owner, no application role carries the bypass
attribute, and the tenant is set per transaction rather than per
connection. Predicate: `serves_multiple_tenants`. Prevents: a
cross-tenant read, which one source calls potentially unrecoverable for
the business it happens to (AWS SaaS Lens, PostgreSQL row security docs,
Azure multitenancy guidance).

**B3. A credential is validated before it is believed.** Signature,
issuer, audience and expiry are checked on every token on every request,
and the algorithm is fixed by the verifier rather than read from the
token. An identity token is never accepted as an access token, and a
session identifier is never forwarded as a bearer credential to another
service. Session identifiers come from a cryptographic generator, are
re-issued whenever the privilege level changes, and are invalidated on
the server at logout. Predicate: `authenticates_people`. Prevents: an
authentication system with no audience check where it matters, and a
session that survives its own logout (OpenID Connect Core, RFC 9700,
OWASP session guidance).

**B4. The privileged path is named, alarmed and reviewed.** Every route
that reaches data or actions it does not own is listed somewhere a
person can read: administrator views, support impersonation, and the
break-glass account. Each use raises an alert and leaves a record
carrying who, when, what for and what was reached. Each use gets a look
afterwards that says whether it was a drill, a real emergency or misuse.
The path is exercised on a schedule so that it is known to work before
it is needed. Predicate: `has_privileged_access_path`. Prevents: the
account that is outside every other control and that nobody watches
(Entra emergency access guidance). Detail in
`packs/identity-access/refs/break-glass.md`.

**B5. An authorisation change ships with the refusal that proves it.**
Adding or changing a permission, a role, a policy or a tenant scope
lands with at least one test that the wrong actor is refused: the other
tenant's identifier returns nothing, the reader cannot write, the
support view cannot reach what it was not opened for. Predicate:
`changes_authorisation_rule`. Prevents: a permission model tested only
from the inside, which is how a model passes every test it has and still
lets the wrong person in (OWASP Top 10:2025).

## Defaults

Do these unless the venture writes down why not, and its lock-book is
where that goes.

| Default | Reason | Evidence |
| --- | --- | --- |
| Start with record ownership plus a small fixed role set; move model only when a real rule cannot be expressed | Most systems never need more, and the cost of the wrong model is paid in migration rather than in bugs | OWASP authorization guidance, NIST RBAC project |
| Reach for relationships when sharing crosses the ownership tree, and for attributes when the rule depends on facts about the record or the environment | These are the two rules roles express by inventing a role per case | NIST SP 800-162, Zanzibar |
| One decision point, in process, until latency, reuse across services or an audit requirement argues otherwise | A central decision service is a dependency on the request path and buys nothing a single application needs | XACML 3.0, Zanzibar |
| Delegate authentication to a provider rather than storing passwords | The provider ships the parts that are tedious and easy to get wrong, and the specification names them | RFC 9700, NIST SP 800-63B-4 |
| Server-side sessions in cookies for a first-party browser surface; tokens for anything else | Session credentials do not belong where page script can read them | OWASP session guidance |
| Shared tables with a tenant key and a database-enforced predicate, until a customer's own keys, data location or backup policy buys them a dedicated store | Density is cheap and dedicated stores are bought per requirement, not per customer | Azure multitenancy guidance, AWS SaaS Lens |
| Both an idle limit and an absolute session limit, inside the graded ranges, with the higher-privilege surface on the shorter one | A session with only one of the two limits is a session that never really ends | NIST SP 800-63B-4, OWASP session guidance |
| A refusal answers the same way everywhere, and the choice between 403 and 404 is made once and written down | Two different refusals across one API is an existence oracle for anyone who notices | OWASP Top 10:2025 |
| At least two break-glass credentials, neither depending on the identity provider, tested at least every ninety days | The path exists for the outage that takes the normal path out | Entra emergency access guidance |

## Preferences

Taste. Record the choice and move on. None of these bind.

- Which policy engine, if any. A relationship engine is available as
  ordinary open-source software rather than as something to build
  (OpenFGA), which changes the cost but not the fork.
- Whether roles are rows in a table or values in an enum.
- Whether the permission check reads as a decorator, a middleware or a
  call at the top of a service function, so long as B1 holds and there
  is one of them.
- Which refusal code, so long as it is one code.
- Session and token lifetimes within the graded ranges.
- Whether tenant context travels as a request-scoped variable or an
  explicit argument, so long as it comes from the credential.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| Roles against attributes against relationships | GD-IDENT-001 | Ownership plus a small role set, moving to relationships or attributes on a rule that cannot be expressed |
| Server session against bearer token | GD-IDENT-002 | Cookie session for a first-party browser surface, sender-constrained token for anything else |
| Identity provider against self-hosted | GD-IDENT-003 | A provider, with the sign-in surface kept thin enough to move |
| Tenant isolation by row, schema or database | GD-IDENT-004 | Shared tables with a database-enforced tenant predicate, escalating per requirement |

Guides sit in `packs/identity-access/guides/`. Level-three detail sits
in three references:
`packs/identity-access/refs/decision-point-placement.md` for where the
decision is made and what happens when it cannot be,
`packs/identity-access/refs/tenant-isolation-mechanics.md` for what
walks past a row policy and the checklist that catches it, and
`packs/identity-access/refs/break-glass.md` for the emergency path. The
worked example is
`packs/identity-access/exemplars/EX-IDENT-001-cross-tenant-share.md`.

## Evidence

Fifteen sources, all fetched on 2026-08-15. This pack was written before
the fragment import ran, so there are no evidence ids to cite yet and
the front matter says `pending-fragment-import` rather than inventing
them. Citations in the body name the source instead, which stays true
after the import assigns ids.

| Named here as | Source |
| --- | --- |
| OWASP Top 10:2025 | OWASP Top 10:2025, A01 Broken Access Control |
| OWASP authorization guidance | OWASP Cheat Sheet Series, Authorization |
| NIST RBAC project | NIST role-based access control project, and ANSI/INCITS 359 |
| NIST SP 800-162 | Guide to Attribute Based Access Control, Update 2 |
| Zanzibar | Zanzibar: Google's Consistent, Global Authorization System, USENIX ATC 2019 |
| OpenFGA | OpenFGA, relationship-based authorisation engine |
| XACML 3.0 | OASIS eXtensible Access Control Markup Language 3.0 |
| RFC 9700 | Best Current Practice for OAuth 2.0 Security, BCP 240 |
| OpenID Connect Core | OpenID Connect Core 1.0, errata set 2 |
| NIST SP 800-63B-4 | Digital Identity Guidelines: Authentication and Authenticator Management |
| OWASP session guidance | OWASP Cheat Sheet Series, Session Management |
| PostgreSQL row security docs | PostgreSQL documentation, Row Security Policies |
| Azure multitenancy guidance | Azure Architecture Center, storage and data in multitenant solutions |
| AWS SaaS Lens | AWS Well-Architected SaaS Lens, silo, pool and bridge models |
| Entra emergency access guidance | Microsoft Entra ID, manage emergency access admin accounts |

The version, licence, access date, applicability limits, counter-evidence
and review trigger for each are in
`packs/identity-access/research/sources.fragment.json`, and the licence
sweep behind them is in
`packs/identity-access/research/provenance.fragment.json`.

## Failure modes and anti-patterns

- The check written per handler and forgotten on the fourth one. This is
  not a hypothetical: it is the shape the measured defect class mostly
  takes (OWASP Top 10:2025).
- A role invented because the rule actually needed an attribute.
  Manager-of-region-north is an attribute wearing a role's clothes
  (OWASP authorization guidance, NIST SP 800-162).
- The tenant taken from a request parameter, a subdomain or a header,
  because it was convenient in a test harness and nobody removed it.
- A row policy switched on while the application still connects as the
  table owner, so the policy is present, documented and inert
  (PostgreSQL row security docs).
- The identity token forwarded to an API as if it were a credential
  (OpenID Connect Core).
- A break-glass account that is somebody's personal administrator login,
  or one nobody has signed into for a year and which will therefore fail
  at the moment it is needed (Entra emergency access guidance).
- Buying a relationship engine to express five permissions, and then
  running a second stateful service on the request path for ever
  (Zanzibar, OpenFGA).
- Reporting a permission model as tested when only the allow paths have
  tests. The refusals are the model.
- Assuming one licence covers the sources. Of the fifteen this pack
  cites, three are United States Government work, three are Creative
  Commons in two different versions, one is Apache-2.0, one is the
  PostgreSQL licence, one is the IETF Trust's, one is the OASIS policy,
  one is the OpenID Foundation's and was not readable at the access,
  three are vendor terms with no open reuse, and one carries no licence
  statement at all. The per-source list is in
  `packs/identity-access/research/provenance.fragment.json`.

## Open questions and counter-evidence

**The model fork has no controlled evidence behind it, and the two
published opinions disagree.** The OWASP guidance prefers attributes and
relationships over roles and names role explosion as the reason (OWASP
authorization guidance). The standards position values roles for
administration, and the economic estimate it rests on is about
provisioning and deprovisioning in large organisations (NIST RBAC
project). They are reconcilable: roles are an administration model,
attributes and relationships are decision models. Notice what that costs
a small venture, though. The strongest published argument for roles is a
saving in an administrative process most ventures here do not have, so
the default in GD-IDENT-001 is argued from cost of change rather than
from evidence.

**The relationship evidence is one company's production report.** The
Zanzibar paper is a system paper with no control arm and no comparison
against roles or attributes. Its numbers are inseparable from a globally
consistent database, a specialised index, request hedging and per-client
quotas, and its own lessons section reports hot spots as a critical
availability problem. There is no independent evaluation of
relationship-based authorisation against the alternatives. If one
appears, GD-IDENT-001 is the first thing that should move.

**The best tenancy control is the one teams skip.** Pushing the tenant
predicate into the database is the mechanism most likely to hold, and
the vendor that hosts two of the databases offering it reports that
carrying identity into every query is hard enough that many multi-tenant
systems do not use it (Azure multitenancy guidance). B2 therefore names
the outcome and allows three mechanisms rather than requiring the one
that is correct and unused.

**Break-glass rests on a single vendor source, declared AI-assisted.**
The Entra emergency access guidance covers one directory product and is
not a standard, and its own trade is that the highest-privilege accounts
sit outside the controls protecting everyone else. B4 keeps the shape
and drops the product, which is a judgement rather than a finding.

**Where the evidence is thin.** No source here measures whether a
central decision point is safer than an in-process one. No source
measures the refusal-code question. The graded session limits come from
a federal risk framework and were not derived from any venture in this
estate. The tenant isolation vocabulary everyone uses comes from a
whitepaper its own publisher now marks as historical (AWS SaaS Lens).

**Refresh triggers.** A new OWASP Top 10 edition; a revision of the NIST
attribute guide, which is the stale source in this set; a published
independent evaluation of relationship-based authorisation; OpenFGA
graduating or being archived; an update to the OAuth security best
current practice; a PostgreSQL release that changes row-security bypass
rules; AWS replacing the withdrawn tenant isolation whitepaper.
