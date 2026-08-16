---
summary: The error envelope, rate limit advertisement and deprecation signalling a boundary carries, with the contested parts marked
kind: fact
scope: estate
sources: [EV-0122, EV-0128, EV-0124, EV-0132]
volatility: slow
review: on-change-of:EV-0122
type: example
tags: [arch, content]
---

# Reference: errors, limits and deprecation signals

Level 3 detail behind the defaults in the pack body.

## Errors as contract

RFC 9457 defines a container, not a taxonomy (EV-0122). It gives one
negotiated media type, `application/problem+json`, carrying a stable
machine-readable `type` URI plus human `title` and `detail`, so a
consumer branches on the type rather than on prose or on a bare status
code.

The design work the RFC does not do for you:

- Choosing the type URIs and keeping them stable. They are contract:
  changing one is a breaking change to any consumer branching on it.
- Deciding which failures deserve a distinct type at all. Too many types
  and nobody branches; too few and everyone parses `detail`.
- Namespacing. One URI prefix per venture keeps them greppable.

Extension members are allowed and are the right place for structured
detail, for example the offending field on a validation failure.

Contested: Azure mandates an incompatible envelope with `error.code` and
`error.message` plus an `x-ms-error-code` header, and treats codes as
contract requiring a version bump to extend (EV-0132). A venture on that
platform follows the platform. The RFC is our default, not a universal.

## Rate limits

Split the static policy from the live budget so a client can plan its
call pattern instead of discovering the ceiling by refusal (EV-0128).
That is a `RateLimit-Policy` field describing the quota and a
`RateLimit` field describing what remains.

Two cautions. The specification is an Internet-Draft, not an RFC, and
its field syntax has churned across eleven revisions, so interoperating
means pinning to a specific draft; ours is draft-11. And it is advisory:
it defines advertisement, not enforcement, and says nothing about 429
behaviour or backoff, which remain yours to specify.

## Deprecation and sunset

Two headers, two dates, and the second is never earlier than the first
(EV-0124):

- `Deprecation` carries when the resource became or becomes deprecated.
- `Sunset` carries when it stops responding.

Both are informational, so they change nothing unless consumers
instrument for them. Neither says how long the gap should be, which is a
per-boundary judgement: long enough for the slowest consumer you know
about, and announced out of band as well as in band.

## What goes in the specification

For each operation, the contract carries the error responses with their
media type and their type URIs, the pagination parameters and response
fields, and any deprecation marker with its sunset date. A gate can then
see a removed error type or a changed parameter as the breaking change
it is. Anything left out of the specification is invisible to the gate
and to schema-derived tests alike.
