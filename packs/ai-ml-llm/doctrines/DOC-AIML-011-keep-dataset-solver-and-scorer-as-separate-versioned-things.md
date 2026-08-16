---
summary: Keep dataset, solver and scorer as separate versioned things.
type: doctrine
tags: [eos]
id: DOC-AIML-011
statement: Keep dataset, solver and scorer as separate versioned things.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0264, EV-0265, EV-0266]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-AIML-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The decomposition a national safety institute settled on lets you swap
the model without rewriting the eval and swap the scorer without
rewriting the dataset (EV-0264). Reason: model churn is the one
certainty in this domain. Scope note: that framework is built for model
evaluation rather than end-to-end product evaluation, and the
alternatives encode different decompositions (EV-0265, EV-0266), so the
split is one defensible shape rather than a standard.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:006`, lines 214-221, SHA-256 `9f57f95baf1f94667fddf0094890fbef2f54c5a8faaa8fa1467fe5e425161956`.
