---
summary: Activation, outcomes and decision map for the identity-access Doctrine and Wargames
type: guide
tags: [auth, security, arch, state]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [authenticates_people, serves_multiple_tenants, has_privileged_access_path, changes_authorisation_rule]
activation_paths: [**/auth/**, **/authz/**, **/*authoriz*/**, **/*authoris*/**, **/permissions/**, **/*permission*/**, **/roles/**, **/*rbac*/**, **/policies/**, **/*.rego, **/*.cedar, **/tenants/**, **/*tenant*/**, **/*session*/**, **/*login*/**, **/*oauth*/**, **/*oidc*/**, **/*saml*/**]
volatility: slow
review: none
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
depends_on: [architecture, security-privacy]
---


# Identity, authorisation and tenancy

This pack owns who a person is, what they may do, and whose data they
may touch. It activates when a venture authenticates people, serves more
than one customer from one system, holds a privileged access path, or
changes an authorisation rule. It carries five binding requirements, a
short set of defaults you may override with a recorded reason, and four
Wargames. Secrets, injection, personal data and approval before
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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-IDENT-001](doctrines/DOC-IDENT-001-deny-unless-something-permitted-and-decide-at-one-layer.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-IDENT-002](doctrines/DOC-IDENT-002-the-tenant-boundary-is-enforced-below-the-code-that-serves-the-r.md) (default)
<a id="B3"></a>
- `B3` to [DOC-IDENT-003](doctrines/DOC-IDENT-003-validate-a-tokens-signature-issuer-audience-and-expiry-on-every.md) (binding), [DOC-IDENT-004](doctrines/DOC-IDENT-004-an-identity-token-is-never-accepted-as-an-access-token.md) (binding), [DOC-IDENT-005](doctrines/DOC-IDENT-005-a-session-identifier-is-never-forwarded-as-a-bearer-credential.md) (binding), [DOC-IDENT-006](doctrines/DOC-IDENT-006-session-identifiers-come-from-a-cryptographic-generator.md) (binding), [DOC-IDENT-007](doctrines/DOC-IDENT-007-reissue-the-session-identifier-whenever-privilege-changes.md) (binding), [DOC-IDENT-008](doctrines/DOC-IDENT-008-invalidate-the-server-side-session-at-logout.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-IDENT-009](doctrines/DOC-IDENT-009-the-privileged-path-is-named-alarmed-and-reviewed.md) (default)
<a id="B5"></a>
- `B5` to [DOC-IDENT-010](doctrines/DOC-IDENT-010-an-authorisation-change-ships-with-the-refusal-that-proves-it.md) (binding)
- source `defaults:001` to [DOC-IDENT-011](doctrines/DOC-IDENT-011-start-with-record-ownership-plus-a-small-fixed-role-set-move-mod.md) (default)
- source `defaults:002` to [DOC-IDENT-012](doctrines/DOC-IDENT-012-reach-for-relationships-when-sharing-crosses-the-ownership-tree.md) (default)
- source `defaults:003` to [DOC-IDENT-013](doctrines/DOC-IDENT-013-one-decision-point-in-process-until-latency-reuse-across-service.md) (default)
- source `defaults:004` to [DOC-IDENT-014](doctrines/DOC-IDENT-014-delegate-authentication-to-a-provider-rather-than-storing-passwo.md) (default)
- source `defaults:005` to [DOC-IDENT-015](doctrines/DOC-IDENT-015-server-side-sessions-in-cookies-for-a-first-party-browser-surfac.md) (default)
- source `defaults:006` to [DOC-IDENT-016](doctrines/DOC-IDENT-016-shared-tables-with-a-tenant-key-and-a-database-enforced-predicat.md) (default)
- source `defaults:007` to [DOC-IDENT-017](doctrines/DOC-IDENT-017-both-an-idle-limit-and-an-absolute-session-limit-inside-the-grad.md) (default)
- source `defaults:008` to [DOC-IDENT-018](doctrines/DOC-IDENT-018-a-refusal-answers-the-same-way-everywhere-and-the-choice-between.md) (default)
- source `defaults:009` to [DOC-IDENT-019](doctrines/DOC-IDENT-019-at-least-two-break-glass-credentials-neither-depending-on-the-id.md) (default)
- source `preferences:001` to [DOC-IDENT-020](doctrines/DOC-IDENT-020-which-policy-engine-if-any.md) (preference)
- source `preferences:002` to [DOC-IDENT-021](doctrines/DOC-IDENT-021-whether-roles-are-rows-in-a-table-or-values-in-an-enum.md) (preference)
- source `preferences:003` to [DOC-IDENT-022](doctrines/DOC-IDENT-022-whether-the-permission-check-reads-as-a-decorator-a-middleware-o.md) (preference)
- source `preferences:004` to [DOC-IDENT-023](doctrines/DOC-IDENT-023-which-refusal-code-so-long-as-it-is-one-code.md) (preference)
- source `preferences:005` to [DOC-IDENT-024](doctrines/DOC-IDENT-024-session-and-token-lifetimes-within-the-graded-ranges.md) (preference)
- source `preferences:006` to [DOC-IDENT-025](doctrines/DOC-IDENT-025-whether-tenant-context-travels-as-a-request-scoped-variable-or-a.md) (preference)

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
