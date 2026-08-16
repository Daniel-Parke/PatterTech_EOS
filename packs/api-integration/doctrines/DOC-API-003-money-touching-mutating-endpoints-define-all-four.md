---
summary: Money-touching mutating endpoints define all four idempotency parameters, not just a header.
type: doctrine
tags: [eos]
id: DOC-API-003
statement: Money-touching mutating endpoints define all four idempotency parameters, not just a header.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0133]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [BR-5]
---

# DOC-API-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

What is stored (status code and body of
the first attempt), for how long, what happens when the same key arrives
with different parameters, and what happens under concurrency (EV-0133).
Prevents: the double charge, and the retry loop that receives a cached
500 forever. EV-0133 is vendor documentation, so this one binds on the
failure rather than on the evidence grade: charging a customer twice is
money already moved, and money already moved is the definition of hard
to reverse.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:requirements:003`, lines 114-122, SHA-256 `5eb725bbbc2cc0ea998a7a844b38e8947864b6a62558dad7184b887a4d3dcc51`.
