---
summary: Decision-relevant synthesis for the API and integration pack, covering contract style, versioning philosophy, webhook security, idempotency and pagination, with the disagreements between mature estates left visible.
type: example
tags: [eos]
---

# API and integration: what the evidence actually supports

Research cutoff 2026-08-03. New sources are in `sources.fragment.json`
as `FRAG-API-INTEGRATION-01` to `-24`. Existing ledger records cited
here: EV-0011, EV-0012, EV-0023, EV-0024, EV-0025, EV-0034, EV-0039,
EV-0057, EV-0061, EV-0091.

## Current versions, as at the cutoff

OpenAPI 3.2.0, published 19 September 2025, Apache-2.0, using the JSON
Schema 2020-12 dialect, and adding streaming content, the QUERY method
and a first-class `webhooks` object (EV-0023). AsyncAPI 3.1.0 (EV-0024).
JSON Schema 2020-12 still the current dialect (EV-0025). GraphQL
September 2025 edition, with a prerelease working draft dated 2 April
2026 (FRAG-19). CloudEvents 1.0.2 (FRAG-17). JSON:API 1.1 (FRAG-13).
Note one live gap: Spectral lists OpenAPI up to 3.1 only (FRAG-16), so
standardising on 3.2 means the lint gate lags the spec.

## Three materially different philosophies

**One: freeze the contract, absorb breakage in the server.** Stripe
pins each consumer to a dated version and encapsulates every
incompatible change as a self-contained transformation module, which
kept roughly a hundred breaking changes invisible to callers since 2011
(EV-0061). Azure's variant is a mandatory `api-version` query parameter
rejected with a named error when absent (FRAG-11). Fits when consumers
are external, numerous and cannot be made to upgrade. The trade is real
engineering cost in the version machinery, and Stripe's own account
concedes it pays off only at high consumer count.

**Two: never break, only add.** JSON:API commits publicly to
never-remove-only-add and consequently keeps its version field optional
(FRAG-13). GraphQL is the same bet with a stronger mechanism: clients
receive only what they selected, so additions cannot break them
(FRAG-19). dbt model contracts (EV-0057) refine it usefully by scoping
the promise, contracts on public models, no ceremony on private ones.
Fits when the surface is small, or when selection-based delivery makes
additions genuinely free. The anti-pattern is schema accretion:
deprecation without a sunset date is not removal, and the AutoGraphQL
study found production queries exercised only 26.9 and 48.7 percent of
two real schemas, so most of a mature GraphQL surface is untested and
unmonitored (FRAG-21).

**Three: declare a compatibility tier and machine-check it.** Buf makes
strictness an explicit setting (FILE, PACKAGE, WIRE_JSON, WIRE) with a
strict default you relax deliberately (FRAG-14). Confluent does the same
for events, where the mode encodes an upgrade order: BACKWARD means
consumers first, FORWARD means producers first, FULL means either, and
only the transitive variants are safe for a log a consumer can rewind
(FRAG-18). oasdiff brings it to HTTP with configurable rules and a
separate changelog for consumer-visible-but-not-breaking changes
(FRAG-15). Fits any estate with more than one team. This is the pattern
with the best cost-to-value ratio for us and should be the pack's spine.

## Disagreements worth recording

Versioning placement is genuinely unsettled. Zalando says MUST NOT
version in the URL and MUST use media-type versioning (FRAG-10). Azure
says no version segment in the path either, but mandates a query
parameter (FRAG-11). Stripe uses an account-pinned date (EV-0061).
Three mature estates, three incompatible answers, all defensible. The
pack must not pretend consensus exists. Media-type versioning in
particular is poorly served by browsers, caches and casual clients.

Error format is contested the same way. RFC 9457 (obsoleting RFC 7807)
is the standards answer (FRAG-01); Azure mandates an incompatible
`error.code` envelope plus an `x-ms-error-code` header and treats codes
as contract requiring a version bump to extend (FRAG-11).

Idempotency header naming is unsettled. The IETF `Idempotency-Key` draft
is still a draft after years, with no RFC number (FRAG-06), while Azure
mandates OASIS Repeatable Requests headers instead (FRAG-11). Cite the
draft as de facto, never as ratified.

GraphQL's evidence is thin and one-sided. The one controlled experiment
found a real client-authoring gain, median 6 minutes versus 9, widening
for parameter-heavy REST endpoints, but with 22 students and only
first-write time measured (FRAG-20). It measures exactly the dimension
GraphQL optimises and none of the server, caching, authorisation or
query-cost dimensions that drive most GraphQL regret. Treat as
suggestive, not decisive.

Contract-first versus code-first has no controlled evidence either way.
OpenAPI deliberately declines to prescribe (EV-0023). The strongest
indirect result is Wittern's: automated GraphQL wrapping succeeded for
89.5 percent of 959 real OpenAPI documents, failures traced to missing
or ambiguous information in the specifications themselves (FRAG-23).
The lesson is about contract quality, not authoring order. Code-first
has a genuine advantage the contract-first camp under-argues: a spec
generated from the handlers cannot drift from them.

## Fit conditions: REST, RPC, events

Resource-shaped, cacheable, many unknown consumers, ordinary CRUD:
REST with OpenAPI. Tight coupling between known services, strong typing,
high call volume, generated stubs: RPC, where buf's tiered compatibility
is available (FRAG-14). Fan-out, replay, decoupled producer and
consumer lifecycles: events, with a CloudEvents envelope for routing and
deduplication (FRAG-17) and a registry compatibility mode chosen before
the first change (FRAG-18). CloudEvents governs metadata only; payload
evolution, which is where events actually break, is still yours.
Agent-facing boundaries add a fourth shape: MCP's dated spec revisions
and capability negotiation (EV-0011) and A2A's task state machine
(EV-0012).

## Webhook security: what is actually settled

Sign an explicit, ordered base string, never the bare body. Standard
Webhooks 1.0.0 signs `id.timestamp.payload`, which gives the consumer an
idempotency key and a replay window in one, and its versioned prefixes
(`v1` HMAC-SHA256, `v1a` ed25519) plus multiple signature headers give
zero-downtime key rotation (FRAG-04). RFC 9421 is the rigorous
generalisation: canonicalise covered components so both sides build
byte-identical input, and bind `created`, `expires` and `nonce`
(FRAG-02). Verification must use the raw body before parsing and a
constant-time comparison (FRAG-05, FRAG-04). Counter-evidence to note
honestly: there is no convergence in the field. GitHub, Stripe and Slack
each ship incompatible schemes, so a consumer library still special-cases
per provider. ASVS (EV-0034) and the OWASP cheat sheets (EV-0039) carry
the surrounding SSRF and secret-handling requirements.

## Idempotency and pagination: settle the parameters, not just the header

Stripe's documentation is the clearest specification of the four
decisions a header alone does not make (FRAG-12): store the status code
and body of the first attempt including 5xx; retain at least 24 hours,
after which the same key starts fresh; error on key reuse with different
parameters rather than silently overwriting; and do not cache a request
that conflicted with a concurrent one, since it is safe to retry.
The sharp edge: caching a 500 means naive client retry loops receive the
failure forever, so retry-with-a-new-key policy is part of the contract.

Pagination: prefer cursors (FRAG-10). AIP-158 supplies the rules worth
copying, tokens opaque and non-parseable, bound to the filter and
ordering of the issuing call with a mismatch being an error, never
carrying authorisation, and total counts optional and possibly estimated
(FRAG-09). Opacity forbids jump-to-page-N, so a table UI is a legitimate
reason to deviate; JSON:API stays strategy-agnostic (FRAG-13).

Rate limits: advertise the policy separately from the live budget so
clients plan rather than discover by refusal, per the RateLimit draft,
pinned to draft-11 (FRAG-07).

## Proposed binding requirements, defaults and preferences

**Binding.** Every service boundary has a machine-readable contract in
the repo (OpenAPI 3.x, AsyncAPI, or protobuf) (EV-0023, EV-0024). A
breaking-change gate runs in CI against a committed baseline and fails
the build (FRAG-15, FRAG-14). The declared compatibility tier or mode is
written down before the first change, not inferred (FRAG-14, FRAG-18).
Webhook receivers verify over the raw body with constant-time comparison
and a bounded timestamp window (FRAG-04, FRAG-05). Non-idempotent
mutating endpoints define all four idempotency parameters, not just the
header (FRAG-12). Deprecation and removal are two dated events, with
removal never earlier than deprecation (FRAG-03).

**Defaults.** RFC 9457 problem details for errors (FRAG-01). Cursor
pagination with opaque tokens (FRAG-09). `Idempotency-Key` as the header
name, marked de facto (FRAG-06). CloudEvents envelope for events
(FRAG-17). BACKWARD_TRANSITIVE for replayable event logs (FRAG-18).
Schema-derived property-based tests against the contract, given the 1.4
to 4.5 times defect-finding advantage (FRAG-22), and consumer-driven
contract tests where two teams share a boundary (EV-0091).

**Preferences.** Contract-first with a definition language such as
TypeSpec when the boundary is public or has several consumers (FRAG-24);
code-first generation is acceptable and sometimes better for internal
boundaries because the spec cannot drift. Spectral rulesets to make house
style executable (FRAG-16). GraphQL only where selection-based delivery
demonstrably solves a client problem, with schema surface monitored
against actual production queries (FRAG-21).
