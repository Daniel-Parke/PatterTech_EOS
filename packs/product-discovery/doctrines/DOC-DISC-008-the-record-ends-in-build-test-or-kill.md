---
summary: The record ends in BUILD, TEST or KILL.
type: doctrine
tags: [eos]
id: DOC-DISC-008
statement: The record ends in BUILD, TEST or KILL.
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
migration_sources: [packs/product-discovery/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B8]
---

# DOC-DISC-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`proposes_capability`. One of the three words, alone, with the reason
under it. Prevents the verdict that is really a deferral. Stopping at
the end of discovery counts as a successful discovery, which is what
makes kill part of the definition rather than an embarrassment
(`EV-0403`). Basis: standard. Failed the seriousness leg: a deferral is
the cheapest thing in this pack to reverse.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:006`, lines 188-194, SHA-256 `a097c6460efa1800c77b1f6370a3c2cd66bef2cf950c204c17accee4c91dfabd`.
