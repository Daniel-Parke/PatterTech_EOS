---
summary: A worked change to a live invoices API and its payment webhook, applying the pack end to end from activation to merge
kind: exemplar
scope: estate
sources: [EV-0129, EV-0130, EV-0122, EV-0125, EV-0133, EV-0136, EV-0124]
type: example
tags: [arch, money, security]
---

# Worked example: changing a live invoices API

A venture runs an invoices service with two external consumers and a
payment provider pushing webhooks. Four changes land in one week: rename
`amt` to `amount_minor`, add a required `tax_code` to the create
request, make the list endpoint paginate, and make the webhook receiver
verify signatures for the first time. This is the pack applied to that
week, in order.

## 1. Activation and routing

The diff touches the OpenAPI document, a route handler and a webhook
handler. Path triggers fire, so the pack activates without needing the
keyword fallback. Two policy factors fire with it: public contract
(floor R2, the consumers are external) and money (floor R2, the webhook
settles invoices). The task routes High-assurance, so an independent
oracle is written before implementation and frozen. Nothing here
authorises firing a payment: that stays manual-only at the guard.

## 2. Classify each change before touching anything

- `amt` to `amount_minor`: a rename, which is removal plus addition,
  therefore breaking (EV-0129).
- Required `tax_code`: adding a required request field, therefore
  breaking (EV-0129).
- Pagination on the list endpoint: additive if the existing unpaginated
  behaviour survives, breaking if the response shape changes.
- Webhook verification: not a contract change at all, a correctness fix
  on an endpoint that was accepting forged deliveries.

Two of the four are breaking. Neither ships silently (BR-6).

## 3. Write the compatibility promise down

Before editing the specification, DECISIONS.md gains a parseable record:

```
versioning: dated api-version query parameter, values YYYY-MM-DD
compatibility: BACKWARD
baseline: api/baseline/openapi.yaml
```

That is default D10. The tier was never written down before, which is
why the last rename in this service went out unnoticed.

## 4. Ship the rename as an addition

`amount_minor` is added. `amt` stays in the schema, marked
`deprecated: true`, with a `Deprecation` date announced in band and a
`Sunset` date ninety days later, never earlier than the deprecation date
(EV-0124). Both fields are populated by the server for the whole window.
Consumers are told out of band as well, because the headers are
informational and change nothing on their own.

## 5. Put the required field behind a discriminator

`tax_code` cannot be required and backward compatible at the same time.
It becomes required only under the new `api-version` value; requests
carrying the previous version keep the old required list. The
discriminator is present in the document, so a gate can see which shape
belongs to which version.

## 6. Pagination

The list operation gains a `page_token` query parameter and a
`next_page_token` response field. Tokens are opaque, bound to the filter
and ordering of the issuing call, and carry no authorisation (EV-0130).
No `offset` parameter is declared. The consumer who wanted page numbers
is told what the deviation would cost and declines it.

## 7. Errors

Every error response on both operations declares
`application/problem+json` with a stable type URI under the venture's
namespace (EV-0122), including the new mismatched-page-token error the
pagination change introduces.

## 8. The webhook receiver

Rewritten in the order BR-4 requires: raw bytes, headers, timestamp
inside a five-minute window, base string rebuilt as
`id.timestamp.payload`, HMAC compared with `hmac.compare_digest`, and
only then a parse (EV-0125). The delivery id goes into the idempotency
store, and the four parameters from BR-5 are settled in the same change:
first response stored including 5xx, seven-day retention to outlive the
provider's retry schedule, mismatch on key reuse is an error, in-flight
requests are not cached (EV-0133). A test issues the same delivery twice
and asserts one settlement.

## 9. The gate

CI runs the breaking check against the committed baseline and fails on
error, plus a changelog run for the release notes (EV-0136). The first
run fails on the rename, which is the correct answer: it passes once the
old field is present and deprecated rather than gone. Schema-derived
property tests run against the updated document.

## 10. What the reviewer checks

`packs/api-integration/CHECKS.md`, in order. The mechanical items pass
in CI. The two judgement items, whether the sunset window is long enough
for the slowest consumer and whether the retention window matches the
provider's retry schedule, are answered in the pull request rather than
assumed.

## What went wrong anyway

The `amt` field was still being written by a background job that nobody
had indexed as a consumer, so the deprecation notice reached two
external consumers and missed an internal one. The lesson is not about
the pack's rules, which worked: it is that the consumer inventory was
incomplete, and a gate over the specification cannot see a consumer
nobody wrote down.
