---
summary: Compiled prompt optimisation against hand-written legible context.
type: doctrine
tags: [eos]
id: DOC-AIML-016
statement: Compiled prompt optimisation against hand-written legible context.
kind: doctrine
authority: preference
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0086, EV-0256, EV-0266]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:preferences:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-AIML-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

An optimiser that searches instructions and demonstrations against a
  metric answers the brittleness problem directly (EV-0266, EV-0256).
  Direct legible context optimises instead for a person reading the
  transcript and seeing why the model did what it did (EV-0086). Nobody
  has run the controlled comparison.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:preferences:001`, lines 273-278, SHA-256 `a38d61ad616b224b5d85c9b78a822720c5167eb0f75721366b773f9fb65c964c`.
