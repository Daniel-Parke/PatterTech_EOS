---
summary: The problem is stated without naming the proposed solution.
type: doctrine
tags: [eos]
id: DOC-DISC-004
statement: The problem is stated without naming the proposed solution.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0403]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-DISC-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`proposes_capability`. The problem section describes what a person
cannot do today and what it costs them, and it does not contain the
name of the requested feature. Prevents a solution wearing a problem's
clothes, which the discovery exit criteria exist to catch
(`EV-0403`). Basis: standard. Failed the seriousness leg: a badly framed
problem is rewritten, and the verdict below is where the cost lands.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:002`, lines 152-158, SHA-256 `6e51b0b23001bcdaad0306f3ab6f1f6ef744fb62ed224b39ca04d5c55c9af9f4`.
