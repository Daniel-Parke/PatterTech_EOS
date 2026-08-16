---
summary: External link checking is advisory, never blocking.
type: doctrine
tags: [eos]
id: DOC-DOCS-011
statement: External link checking is advisory, never blocking.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0331]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-DOCS-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason:
external checking fails against rate limits and transient outages, so
making it blocking buys false failures and then gets turned off
(EV-0331). The blocking half of the check runs offline over internal
links and anchors only, which is also what makes it reproducible.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:defaults:005`, lines 237-241, SHA-256 `cc7416e9ca242b6f60913574657d61bc77c5b030e935d48b22aab97925b59cf7`.
