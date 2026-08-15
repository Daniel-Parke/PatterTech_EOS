---
summary: What a reviewer or a script can verify about identity, authorisation and tenancy work, executable today versus judgement
type: guide
tags: [auth, testing, data]
review: 2028-09
kind: record
scope: estate
---

# CHECKS: evaluating work under this pack

Every criterion states what it checks and how. Executable means a script
or an existing tool can rule on it today with no human reading.
Judgement means a reviewer has to read and decide, and the criterion
exists to tell them what to look for.

Where these run matters. This repository is documentation and has no
runtime, no users and no tenants, so none of the C series below is wired
into `python -m tools.eos check`. They are criteria for a venture's own
pipeline and its own reviewers, and a venture that adopts this pack is
adopting the job of implementing them.

## Executable today

| # | Criterion | How it is checked | Binds to |
| --- | --- | --- | --- |
| C1 | Every route that reads or changes data resolves an authorisation decision | Route table enumerated from the framework and compared against the set the decision function covers; a route in neither the covered set nor an explicit public list fails | B1 |
| C2 | The decision fails closed | The decision function is called with a policy source that errors and with an action no rule matches; both must return a denial | B1 |
| C3 | No authorisation input is taken from the caller | Static scan of the decision call sites for arguments sourced from request parameters, headers or path segments rather than from the authenticated principal | B1, B2 |
| C4 | Every table holding tenant data is covered | Catalogue query lists tables carrying the tenant column; each must have a row policy, or sit in a per-tenant schema or store. A table in none of the three fails | B2 |
| C5 | The row policy is not inert | Connect as the application role and read a row belonging to another tenant. Success fails the check, which is what catches the owner exemption and the bypass attribute | B2 |
| C6 | Tenant context is set per transaction | Grep the connection setup and the job runner for the tenant being set on the connection or the pool rather than inside the transaction | B2 |
| C7 | Tokens are validated on signature, issuer, audience and expiry, with a fixed algorithm | Verifier configuration parsed; a configuration that reads the algorithm from the token fails, as does one with no audience value | B3 |
| C8 | Session identifiers are re-issued on privilege change and invalidated server-side at logout | Integration test captures the identifier before and after sign-in and after logout; an unchanged identifier, or one that still resolves after logout, fails | B3 |
| C9 | Every privileged route is on the named list | The list is compared against routes annotated as privileged; a route in one and not the other fails | B4 |
| C10 | Every use of a privileged route left a record and raised an alert | Count of privileged-route invocations in the request log equals count of records, and each record carries actor, time, reason and target | B4 |
| C11 | The break-glass credential still works and its alert still fires | Scheduled drill: sign in, confirm the alert arrived, record the date. A drill older than ninety days fails | B4, Defaults |
| C12 | A change touching a permission, role, policy or tenant scope carries at least one refusal test | Diff scanned for the permission surfaces; the same diff must add or change a test whose assertion is a denial | B5 |
| C13 | The cross-tenant refusal is the standard refusal | Request another tenant's identifier and a non-existent identifier; the two responses must be identical in status and body | B2, Defaults |
| C14 | Every source cited in this pack's front matter resolves to a row in the evidence ledger | Each id in front matter looked up in `registry/evidence.json` | Pack hygiene |

C14 is live. The fragment import assigned `EV-0517` through `EV-0531`,
and the pack's front matter cites those canonical rows. S014 refuses an
unresolved placeholder or an evidence identity absent from the ledger;
S016 keeps the ledger's derived `cited_by` view aligned with the read
surface.

## Judgement

| # | Criterion | What the reviewer looks for | Binds to |
| --- | --- | --- | --- |
| J1 | The model was argued, not inherited | A ruling on GD-IDENT-001 exists, names what the rules actually depend on, and says why the chosen model expresses them. "We used roles" with no reason fails | Decision map |
| J2 | No role is an attribute in disguise | Read the role names. One that encodes a region, a department, a record type or a customer is an attribute that was made into a role because the model could not carry it | GD-IDENT-001 |
| J3 | There is one mechanism that can grant a permission, not two | Two independent paths to the same grant means every audit has to check both, and one will drift | B1 |
| J4 | The tenant boundary claim matches the mechanism | The lock-book says which layer holds the guarantee. "The application filters by tenant" and "the database refuses" are different promises | B2 |
| J5 | Propagation reaches the places that are usually forgotten | Background jobs, scheduled tasks, migrations, exports, admin tooling. A boundary that holds only on the request path is a boundary with office hours | B2 |
| J6 | Break-glass is designed, not improvised | Two credentials, not federated through the provider, not tied to one person's device, a different authentication method, tested within ninety days | B4 |
| J7 | The privileged-use review actually happened | Somebody read the records and reached a verdict per use: drill, emergency or misuse. A list nobody reads is a log, not a control | B4 |
| J8 | Impersonation records who really acted | An audit trail that says the customer did it, when staff did it, is worse than no trail | B4 |
| J9 | The refusal tests are the interesting ones | Wrong tenant, wrong role, wrong relation, missing context. A suite of allow paths with one token denial fails | B5 |
| J10 | Session and token lifetimes were chosen against the surface | An administrative surface on the same lifetime as a public one is a lifetime nobody picked | Defaults |
| J11 | Preferences are recorded as preferences | A taste choice presented as binding is a finding, and the reverse too | Pack hygiene |
| J12 | Thin evidence is admitted | Where the pack says there is no controlled evidence, work relying on it says so rather than borrowing confidence | Open questions |

## Not checkable, and why

Whether the permission model expresses what the business meant. There is
no oracle for that outside the business, and a checker that claimed one
would be asserting the requirements rather than testing them.

Whether a permission set is least privilege in fact. Least privilege is
defined against what each person actually needs to do, which nothing in
a repository knows. What can be checked is narrower and is C1 and C12:
that a decision is made, and that the refusal was tested.

Whether a cross-tenant path exists through a route nobody enumerated. C1
and C4 check the routes and tables that are known; a path through an
unlisted surface is exactly the case they cannot see, which is why B2
puts the boundary below the code rather than relying on the list being
complete.

Whether a decision point that is up today will be up under load. The one
well-documented central authorisation system reports hot spots as a
critical availability problem needing dedicated mitigation, and that is
a property of a running system under real traffic, not of a review.

No criterion here is phrased as a percentage of unauthorised requests
blocked. Without the count of legitimate requests served on the same
run, that number is unfalsifiable in the direction that matters, and the
same argument is made at greater length in
`packs/security-privacy/CHECKS.md`.

## Failure severity

C1 through C10, C12 and C13 are pass or fail. C11 is pass or fail and
its failure mode is a stale date rather than a broken control, so it
reports the age rather than only the verdict. C14 is pack hygiene and
fails until the fragment import runs.

The J series produces findings with severity set by the reviewer, and a
J-series finding never downgrades a C-series failure. J4 is the one to
read first when a C-series check passes and something still feels wrong:
a passing boundary check on the request path says nothing about the
export job.
