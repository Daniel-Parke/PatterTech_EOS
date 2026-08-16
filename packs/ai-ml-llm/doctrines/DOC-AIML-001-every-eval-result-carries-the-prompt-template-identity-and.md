---
summary: Every eval result carries the prompt template identity and the model identifier.
type: doctrine
tags: [eos]
id: DOC-AIML-001
statement: Every eval result carries the prompt template identity and the model identifier.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0256]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-AIML-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The report records the template path and a content
hash of the template, plus the exact model id used. A comparison run
under two different templates is not a comparison. Changing only the
single character separating in-context examples moved MMLU by up to
twenty-three points, enough to reorder a ranking, and the brittleness
did not shrink with scale (EV-0256). Scope note: that was few-shot
multiple choice on open-weight families, so the magnitude is
population-bound and the discipline is not.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:requirements:001`, lines 93-101, SHA-256 `595ad35061baa8473222198616f495b6201cf961667b32a58b1dc39dc9d7ab83`.
