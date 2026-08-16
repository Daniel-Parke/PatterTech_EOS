---
summary: Activation, outcomes and decision map for the api-integration Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [exposes_service_boundary, consumes_external_api, receives_webhooks, publishes_events]
activation_paths: [**/api/**, **/routes/**, **/handlers/**, **/webhooks/**, **/openapi*.y*ml, **/openapi*.json, **/asyncapi*.y*ml, **/*.proto, **/schemas/**, **/endpoints/**]
volatility: slow
review: none
type: pack
tags: [arch, security, money]
sources: [EV-0023, EV-0024, EV-0061, EV-0091, EV-0122, EV-0124, EV-0125, EV-0126, EV-0127, EV-0128, EV-0129, EV-0130, EV-0131, EV-0132, EV-0133, EV-0135, EV-0136, EV-0137, EV-0138, EV-0139, EV-0140, EV-0141, EV-0142, EV-0143, EV-0144, EV-0145]
display_name: APIs and Integrations
category: engineering
id_namespace: API
depends_on: [architecture, security-privacy]
---


# APIs and Integrations

This pack governs work at a service boundary: the HTTP and RPC APIs we
publish or consume, webhook receivers, event contracts, and the way any
of them change. It activates when a change touches an API contract, a
webhook handler, an event payload or a client of someone else's API. It
binds a breaking-change gate, webhook verification before parsing,
idempotency on money-touching paths, and dated deprecation before
removal.

## Activation

Path triggers, checked first:

- `api/`, `openapi.*`, `asyncapi.*`, any `.proto`, `schema/`
- webhook, integration, client or connector directories
- route and handler files that serve or receive a public request

Task-type triggers, when paths are ambiguous: publishing or changing a
service boundary; adding or changing a webhook receiver; consuming a
third-party API; changing an event payload; deprecating or removing an
endpoint or field.

Keyword triggers, fallback only when neither path nor task type fires:
openapi, asyncapi, protobuf, grpc, graphql, webhook, signature,
idempotency, pagination, rate limit, versioning, breaking change,
deprecation, sunset.

Applicability predicates:

- `exposes_service_boundary`: the venture serves an API another codebase
  calls. Everything below applies.
- `consumes_external_api`: the venture calls someone else's API. The
  binding requirements on retries, idempotency and adapters apply; the
  contract-publishing ones do not.
- `receives_webhooks`: an endpoint accepts a push from a third party.
  BR-4 and BR-5 apply in full.
- `publishes_events`: the venture writes to a topic or queue others
  read. BR-2 applies in its event form, as do defaults D9 and D10.

Policy routing (`kernel/POLICY_SPEC.md`): contact with a public API
surface activates the public-contract factor, floor R2. Billing and
payment paths activate the money factor, floor R2. Any actual movement
of funds is manual-only at the guard (`kernel/GUARD_SPEC.md`) and this
pack never softens that. A webhook receiver that refunds, charges or
transfers is a money-movement surface: the agent may write and test it,
never fire it.

## Outcomes and non-goals

Outcomes we are buying: a consumer can upgrade on its own schedule; a
change that would break a consumer fails the build rather than
production; a forged or replayed webhook cannot move anything; a retried
payment charges once; deprecation and removal are two dated, announced
events.

Non-goals: authentication and authorisation design (security-privacy
pack); gateway, transport and rate-limit enforcement operations
(devops-reliability); internal module boundaries (architecture); client
data fetching (ui-ux). This pack is also not a style guide. Naming,
casing and description rules belong in an executable ruleset, not here.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="BR-2"></a>
- `BR-2` to [DOC-API-001](doctrines/DOC-API-001-a-breaking-change-check-runs-in-ci-against-a-committed.md) (binding)
<a id="BR-4"></a>
- `BR-4` to [DOC-API-002](doctrines/DOC-API-002-webhook-receivers-authenticate-the-exact-raw-request-before.md) (binding)
<a id="BR-5"></a>
- `BR-5` to [DOC-API-003](doctrines/DOC-API-003-money-touching-mutating-endpoints-define-all-four.md) (binding)
<a id="BR-6"></a>
- `BR-6` to [DOC-API-004](doctrines/DOC-API-004-deprecation-and-removal-are-two-dated-events-and-removal-is.md) (binding)
- source `defaults:001` to [DOC-API-005](doctrines/DOC-API-005-errors-use-application-problem-json.md) (default)
- source `defaults:002` to [DOC-API-006](doctrines/DOC-API-006-cursor-pagination-with-opaque-tokens-no-offset.md) (default)
- source `defaults:003` to [DOC-API-007](doctrines/DOC-API-007-idempotency-key-as-the-header-name.md) (default)
- source `defaults:004` to [DOC-API-008](doctrines/DOC-API-008-cloudevents-envelope-for-events.md) (default)
- source `defaults:005` to [DOC-API-009](doctrines/DOC-API-009-backward-transitive-for-any-log-a-consumer-can-rewind.md) (default)
- source `defaults:006` to [DOC-API-010](doctrines/DOC-API-010-schema-derived-property-tests-against-the-contract.md) (default)
- source `defaults:007` to [DOC-API-011](doctrines/DOC-API-011-rate-limit-policy-advertised-separately-from-the-live-budget.md) (default)
- source `defaults:008` to [DOC-API-012](doctrines/DOC-API-012-webhook-signatures-over-the-triple-id-timestamp-payload-with.md) (default)
- source `defaults:009` to [DOC-API-013](doctrines/DOC-API-013-the-contract-is-machine-readable-and-lives-in-the-repo.md) (default)
- source `defaults:010` to [DOC-API-014](doctrines/DOC-API-014-the-compatibility-promise-is-declared-before-the-first.md) (default)
- source `preferences:001` to [DOC-API-015](doctrines/DOC-API-015-contract-first-with-a-definition-language-such-as-typespec.md) (preference)
- source `preferences:002` to [DOC-API-016](doctrines/DOC-API-016-an-executable-ruleset-ev-0137-rather-than-a-style-document.md) (preference)
- source `preferences:003` to [DOC-API-017](doctrines/DOC-API-017-graphql-only-where-selection-based-delivery-solves-a.md) (preference)
- source `preferences:004` to [DOC-API-018](doctrines/DOC-API-018-one-problem-type-uri-namespace-per-venture-so-error-types.md) (preference)

## Decision map

| Fork | Options | Wargame |
| --- | --- | --- |
| Who authors the contract, and when | hand-written spec, definition language, code-first generation, none | `packs/api-integration/wargames/WG-API-001-contract-authoring.md` |
| How the boundary is allowed to change | add-only, declared tier plus gate, explicit version parameter, pinned date with transformers | `packs/api-integration/wargames/WG-API-002-versioning-and-breaking-change.md` |
| How a webhook is trusted | bare-body HMAC, signed triple, RFC 9421, asymmetric or provider-native | `packs/api-integration/wargames/WG-API-003-webhook-trust.md` |
| What shape the boundary takes | REST, RPC, events, GraphQL | `packs/api-integration/wargames/WG-API-004-boundary-shape.md` |
| How a collection is traversed | offset, opaque cursor, keyset, hybrid | `packs/api-integration/wargames/WG-API-005-collection-traversal.md` |

Level-three detail the body defers to: what counts as breaking and how
the gate is wired,
`packs/api-integration/references/breaking-change-catalogue.md`;
the verification order a receiver needs,
`packs/api-integration/references/webhook-verification.md`; the four
decisions a header does not make,
`packs/api-integration/references/idempotency-parameters.md`; the error
envelope, rate limit and deprecation signals,
`packs/api-integration/references/error-and-limits.md`. Worked cases: a week
of changes to a live API in
`packs/api-integration/examples/EX-API-001-invoices-api-change.md`,
and dated versioning read properly in
`packs/api-integration/examples/EX-API-002-stripe-versioning.md`.
Evaluation criteria are in `packs/api-integration/CHECKS.md`.

## Failure modes and anti-patterns

- **Parse, then verify.** The most common webhook defect. The signature
  covered bytes the framework has already replaced (EV-0126). Its
  cousins: `==` on a digest, and signing a re-serialised body, which
  ends with someone disabling verification to ship.
- **Deprecation with no sunset date.** Not removal, only deferral. The
  schema accretes forever (EV-0140).
- **Caching a 5xx under an idempotency key with no retry-with-new-key
  policy.** The client receives the failure forever (EV-0133).
- **Cursor tokens that encode an offset or an authorisation claim.**
  Both are parseable, and one of them is a privilege escalation
  (EV-0130).
- **Treating an enum addition as free.** It is flagged as risky, not
  safe, and a consumer switching exhaustively will fall through
  (EV-0129).
- **The semantic break a diff cannot see.** Units, meaning or
  construction rules changed while the schema stayed identical; the gate
  passes (EV-0136).
- **Adopting CloudEvents and assuming payloads are now governed.** They
  are not, and payloads are where events actually break (EV-0138). Its
  neighbour: a non-transitive compatibility mode on a log a consumer can
  rewind (EV-0139).
- **A lint-clean spec describing a service that does something else.**
  Linting checks form, never behaviour (EV-0137).

## Open questions and counter-evidence

- **Version placement has no consensus.** Zalando forbids URL versioning
  and mandates media-type versioning (EV-0131); Azure mandates an
  `api-version` query parameter (EV-0132); Stripe pins an account to a
  date (EV-0061). Three mature estates, three incompatible answers, each
  defensible. This pack routes the choice through fit conditions and
  refuses to call any of them doctrine.
- **The error envelope is contested.** RFC 9457 is the standards answer
  (EV-0122) and Azure ships an incompatible one at scale (EV-0132).
- **The idempotency header name is contested and unratified.** The IETF
  draft has sat unfinished for years (EV-0127) and Azure mandates the
  OASIS Repeatable Requests headers instead (EV-0132). Cite it as de
  facto or not at all.
- **Contract-first versus code-first has no controlled evidence either
  way.** The nearest result is that automated wrapping of 959 real
  specifications succeeded 89.5 percent of the time, with failures
  traced to ambiguity in the specifications themselves (EV-0144). That
  is a finding about contract quality, not about authoring order. The
  preference above stays a preference.
- **The GraphQL client-effort result is thin and narrowly scoped.**
  Median six minutes against nine, widening for parameter-heavy REST
  endpoints, from 22 students writing eight queries once (EV-0141). It
  measures first-write time for novice client authors and nothing else,
  in particular none of the server, caching, authorisation or query-cost
  dimensions that drive most GraphQL regret. Do not promote it past that
  population.
- **The schema-derived fuzzing result is a preprint** over sixteen
  services, evaluated by the tool's own authors (EV-0143). Strong enough
  to default on, not strong enough to bind.
- **Webhook signing has not converged.** GitHub, Stripe and Slack each
  ship incompatible schemes (EV-0125), so any consumer library still
  special-cases per provider. Expect an adapter, not a standard.
- **Our timestamp tolerance is invented.** Standard Webhooks fixes no
  number (EV-0125); five minutes is an estate choice open to argument.

## Evidence pointer

The twenty-four primary rows behind this pack were frozen at
`packs/api-integration/research/sources.fragment.json` and have since
been imported into `registry/evidence.json` as EV-0122 to EV-0145. Every
`EV-` id cited above resolves to a row there carrying version or commit,
licence, access date, applicability limits and a review trigger. Four
rows come from earlier estate research rather than from this pack's
sweep: OpenAPI (EV-0023), AsyncAPI (EV-0024), Stripe's dated versioning
(EV-0061) and consumer-driven contract testing (EV-0091). The synthesis
and the disagreements behind this file are in
`packs/api-integration/research/NOTES.md`. The licence and quotation
sweep over all of them is at
`packs/api-integration/research/provenance.fragment.json`. It records
four cited rows whose licence nobody has confirmed and seven whose
source states none.
