---
summary: Binding requirements, defaults and decision guides for API contracts, webhooks, event payloads and integration change
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary, consumes_external_api, receives_webhooks, publishes_events]
activation_paths: [**/api/**, **/routes/**, **/handlers/**, **/webhooks/**, **/openapi*.y*ml, **/openapi*.json, **/asyncapi*.y*ml, **/*.proto, **/schemas/**, **/endpoints/**]
volatility: slow
review: 2027-12
type: guide
tags: [arch, security, money]
sources: [EV-0023, EV-0024, EV-0061, EV-0091, EV-0122, EV-0124, EV-0125, EV-0126, EV-0127, EV-0128, EV-0129, EV-0130, EV-0131, EV-0132, EV-0133, EV-0135, EV-0136, EV-0137, EV-0138, EV-0139, EV-0140, EV-0141, EV-0142, EV-0143, EV-0144, EV-0145]
---

# API and integration

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

## Binding requirements

Four, each with a named failure and cited evidence. Every one names a
failure that lands outside this repository: a consumer's production
breaks, or money moves twice, and neither is something we can take back.

The authority audit under ADR-0008 moved two of the original six to
defaults, because each named a missing artefact rather than a failure:
the machine-readable contract is now D9 and the declared compatibility
promise is now D10. The four that stayed keep their numbers, so the
citations in the guides, refs and exemplars still resolve, which is why
the list below starts at BR-2.

**BR-2. A breaking-change check runs in CI against a committed baseline,
and fails the build.** For HTTP that is `oasdiff breaking` against the
frozen previous revision (EV-0136); for protobuf it is the buf breaking
check (EV-0135); for a registry-backed event topic it is the registry's
own compatibility check (EV-0139). Prevents: shipping a break silently
and learning about it from a consumer. A published boundary carrying no
machine-readable contract cannot satisfy this, which is what D9 costs
when you depart from it, and why departing from D9 is done in writing
rather than in silence.

**BR-4. Webhook receivers verify before they parse.** The signature is
computed over the exact bytes received, compared in constant time
(`hmac.compare_digest`, `crypto.timingSafeEqual` or `secure_compare`),
and rejected outside a numeric timestamp tolerance. A framework that
hands the handler a parsed object has already destroyed the bytes the
signature covers (EV-0126, EV-0125). Prevents: forged deliveries and
replayed deliveries, both of which are free to an attacker otherwise.
The ADR-0008 audit left this one alone even though EV-0126 is vendor
documentation: verifying the authenticity of an inbound message is a
security floor, and a floor stays binding whatever its basis field says.

**BR-5. Money-touching mutating endpoints define all four idempotency
parameters, not just a header.** What is stored (status code and body of
the first attempt), for how long, what happens when the same key arrives
with different parameters, and what happens under concurrency (EV-0133).
Prevents: the double charge, and the retry loop that receives a cached
500 forever. EV-0133 is vendor documentation, so this one binds on the
failure rather than on the evidence grade: charging a customer twice is
money already moved, and money already moved is the definition of hard
to reverse.

**BR-6. Deprecation and removal are two dated events, and removal is
never the earlier one.** Announce deprecation in band with a date, carry
a separate sunset date, and do not remove before it (EV-0124). A rename
is a removal plus an addition and is therefore breaking: add the new
name, mark the old one deprecated, and let both resolve until sunset
(EV-0129). Adding a required field to a request is equally breaking, so
it ships behind a version discriminator, never in place. Prevents: the
silent removal that only the consumer discovers.

## Defaults

Overridable, but the override is recorded next to the code with its
reason.

- **D1. Errors use `application/problem+json`** (EV-0122). One
  negotiated container with a stable type URI a consumer can branch on.
  Override where a platform mandates a different envelope (EV-0132).
- **D2. Cursor pagination with opaque tokens, no offset** (EV-0130).
  Tokens bind to the filter and ordering of the issuing call and carry
  no authorisation. Override for a table UI that needs page numbers, see
  `packs/api-integration/guides/GD-API-005-collection-traversal.md`.
- **D3. `Idempotency-Key` as the header name**, cited as de facto. The
  IETF draft has never reached RFC (EV-0127) and Azure mandates a
  different family (EV-0132), so this is a house choice, not a standard.
- **D4. CloudEvents envelope for events** (EV-0138), which standardises
  routing and deduplication metadata only; payload evolution stays
  yours.
- **D5. `BACKWARD_TRANSITIVE` for any log a consumer can rewind**
  (EV-0139). Non-transitive modes check only the last version and give
  false comfort on replay.
- **D6. Schema-derived property tests against the contract** (EV-0143,
  1.4 to 4.5 times more unique defects than the next-best fuzzer across
  sixteen services; preprint, authors evaluating their own tool), plus
  consumer-driven contract tests where two teams share a boundary
  (EV-0091).
- **D7. Rate limit policy advertised separately from the live budget**,
  pinned to draft-11 (EV-0128).
- **D8. Webhook signatures over the triple `id.timestamp.payload` with a
  versioned prefix**, for anything we emit (EV-0125). Timestamp
  tolerance five minutes: that number is an estate choice, since no
  source fixes one.
- **D9. The contract is machine-readable and lives in the repo.** A
  boundary we publish carries a committed OpenAPI 3.x document
  (EV-0023), AsyncAPI document (EV-0024) or protobuf definition,
  versioned with the code. Reason: prose cannot be diffed, generated
  from or tested against, and under-specified contracts cap every
  downstream automation (EV-0144). This is a default rather than binding
  because what it names is a missing artefact, not a failure; the
  failure is a break reaching a consumer, and BR-2 is what stops that.
  Departing costs you BR-2, so the recorded reason has to say how the
  break gets caught instead.
- **D10. The compatibility promise is declared before the first
  change.** A parseable line in DECISIONS.md or an ADR records the
  versioning approach and the tier or mode, for example a
  `compatibility` line naming BACKWARD. Tiers come from the toolchain in
  use: FILE, PACKAGE, WIRE_JSON or WIRE for protobuf (EV-0135);
  BACKWARD, FORWARD, FULL, NONE and their transitive variants for events
  (EV-0139). Reason:
  otherwise you discover your own promise by breaking someone. This is a
  default rather than binding because the gate in BR-2 still runs
  without it, at whatever strictness the tool defaults to, so the cost
  of departing is that you have accepted that default sight unseen.

## Preferences

Taste. Argue them if you like, override them without ceremony.

- Contract-first with a definition language such as TypeSpec (EV-0145)
  when the boundary is public or has several consumers; code-first
  generation when it is internal, because a spec emitted from the
  handlers cannot drift from them. OpenAPI itself declines to prescribe
  either (EV-0023) and there is no controlled evidence on the question.
- An executable ruleset (EV-0137) rather than a style document, noting
  that Spectral listed no OpenAPI 3.2 support at the access date.
- GraphQL only where selection-based delivery solves a demonstrated
  client problem, and then with the schema surface monitored against
  real production queries (EV-0142).
- One problem-type URI namespace per venture, so error types are
  greppable across services.

## Decision map

| Fork | Options | Guide |
| --- | --- | --- |
| Who authors the contract, and when | hand-written spec, definition language, code-first generation, none | `packs/api-integration/guides/GD-API-001-contract-authoring.md` |
| How the boundary is allowed to change | add-only, declared tier plus gate, explicit version parameter, pinned date with transformers | `packs/api-integration/guides/GD-API-002-versioning-and-breaking-change.md` |
| How a webhook is trusted | bare-body HMAC, signed triple, RFC 9421, asymmetric or provider-native | `packs/api-integration/guides/GD-API-003-webhook-trust.md` |
| What shape the boundary takes | REST, RPC, events, GraphQL | `packs/api-integration/guides/GD-API-004-boundary-shape.md` |
| How a collection is traversed | offset, opaque cursor, keyset, hybrid | `packs/api-integration/guides/GD-API-005-collection-traversal.md` |

Reference material the body defers to sits in
`packs/api-integration/refs/`, worked cases in
`packs/api-integration/exemplars/`, and the evaluation criteria in
`packs/api-integration/CHECKS.md`.

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
(EV-0061) and consumer-driven contract testing (EV-0091). The licence
and quotation sweep over all of them is at
`packs/api-integration/research/provenance.fragment.json`. It records
four cited rows whose licence nobody has confirmed and seven whose
source states none.
