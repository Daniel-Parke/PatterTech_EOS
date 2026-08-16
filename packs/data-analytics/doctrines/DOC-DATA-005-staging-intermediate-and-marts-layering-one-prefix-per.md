---
summary: Staging, intermediate and marts layering, one prefix per layer.
type: doctrine
tags: [eos]
id: DOC-DATA-005
statement: Staging, intermediate and marts layering, one prefix per layer.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0307]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-DATA-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Staging is one to one with sources and only cleans and renames, joins
and logic sit in intermediate models, marts hold business entities
(EV-0307). Reason: the prefix tells a reviewer what a model may do, so
review is mechanical. Costs model count and build time. Override for a
project small enough that the layers are ceremony.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:002`, lines 155-160, SHA-256 `0614525663222364edf060a6d13b77530ab9d3924530e538cc3fc45bc7b62268`.
