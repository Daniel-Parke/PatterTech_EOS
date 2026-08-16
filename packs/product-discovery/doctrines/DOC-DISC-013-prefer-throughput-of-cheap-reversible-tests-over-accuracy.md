---
summary: Prefer throughput of cheap reversible tests over accuracy of ranking, where there is traffic to read.
type: doctrine
tags: [eos]
id: DOC-DISC-013
statement: Prefer throughput of cheap reversible tests over accuracy of ranking, where there is traffic to read.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0405]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-DISC-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: across a large corpus
of randomised online experiments roughly a third of ideas moved the
target metric positively, a third were flat and a third were negative,
and expert judgement inside the team did not predict which
(`EV-0405`). Scope note: that population is very
high-traffic consumer search and portal surfaces where a powered test
finishes in days. Below the power floor the base rate is a prior about
idea quality, not a runnable method.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:011`, lines 221-229, SHA-256 `91396337a638ce3aae53e137f95194a1faf378f957b1049e234bc2ed1e227631`.
