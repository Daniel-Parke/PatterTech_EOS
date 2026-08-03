---
summary: Single-run cold-agent acceptance drill for the API and integration pack, with deterministic machine-checkable criteria.
type: example
tags: [eos]
---

# Drill: evolve a webhook-bearing API without breaking a consumer

## Scenario

A cold agent is given only the pack and a seeded repo containing
`api/openapi.yaml` (an OpenAPI 3.1 orders service with `POST /orders`,
`GET /orders` and one webhook receiver), `api/baseline/openapi.yaml`
(the frozen previous revision), and a `TASK.md` change request: rename
`orders[].ref` to `orders[].reference`, add a required `currency` field
to the create request, add cursor pagination to `GET /orders`, and make
the webhook receiver verify signatures.

The rename and the new required field are breaking (FRAG-08) and must
not be shipped silently. One run, no human turns.

## Deterministic pass criteria

Every check must return true. Each is a file existence, exit code or
parse assertion, no judgement.

1. `api/openapi.yaml` parses as valid OpenAPI 3.x.
2. A CI config invokes a breaking-change check against
   `api/baseline/openapi.yaml` (harness greps for `oasdiff breaking` or
   equivalent, then runs it).
3. The old name `ref` is still resolvable: it remains in the schema with
   `deprecated: true`, or a second version identifier is present that
   serves the old shape.
4. `currency` appearing in a `required` list implies a version
   discriminator exists in the document.
5. `GET /orders` declares a `page_token` or `cursor` query parameter and
   a next-token response field, and declares no `offset` (FRAG-09).
6. Error responses on both operations use media type
   `application/problem+json` (FRAG-01).
7. No JSON parse call precedes the signature check in the webhook
   handler source (FRAG-05).
8. The handler calls `hmac.compare_digest`, `crypto.timingSafeEqual` or
   `secure_compare`, and does not compare the digest with `==`
   (FRAG-04, FRAG-05).
9. A numeric timestamp tolerance bound is present in the handler source
   (FRAG-04).
10. A `DECISIONS.md` or ADR file carries a parseable line recording the
    versioning approach and compatibility tier, for example
    `compatibility: BACKWARD` (FRAG-14, FRAG-18).
11. `python tools/eos_check.py --repo` exits zero.

## Scoring

Eleven binary checks, pass threshold 11 of 11. Partial credit is
recorded for diagnosis only and is not a pass.
