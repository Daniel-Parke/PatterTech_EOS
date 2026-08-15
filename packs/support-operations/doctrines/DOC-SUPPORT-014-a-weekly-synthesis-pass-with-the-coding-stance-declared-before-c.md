---
summary: A weekly synthesis pass with the coding stance declared before coding.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-014
statement: A weekly synthesis pass with the coding stance declared before coding.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0431]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:012]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

What the data set is, whether coding is inductive or driven
  by an existing frame, whether it reads the surface or the meaning
  underneath, and what counts as a theme, all written down first.
  Prevalence is reported against a stated denominator, because a count
  of tickets mentioning a thing means nothing without the population it
  came from (EV-0431). Themes are constructed by the
  analyst, so "a theme emerged" is not an available sentence.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:012`, lines 258-265, SHA-256 `139056f2bbd053aad25e887fee78f4ba9f4de9ffde60286a838d9014724c0f71`.
