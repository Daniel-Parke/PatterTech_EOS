---
summary: Retrieval before fine-tuning for anything that is a fact.
type: doctrine
tags: [eos]
id: DOC-AIML-008
statement: Retrieval before fine-tuning for anything that is a fact.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0248, EV-0249]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-AIML-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Retrieval beat unsupervised fine-tuning in almost every
knowledge-injection condition tested, including for facts the base model
had never seen (EV-0248). Fine-tuning is for form, task shape and format
adherence. Reason: facts move faster than training runs. Scope note:
seven-billion-parameter open models and multiple-choice evaluation, and
parameter-efficient tuning is a real trade rather than a free lunch
(EV-0249). See `packs/ai-ml-llm/guides/GD-AIML-002-knowledge-source.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:003`, lines 188-195, SHA-256 `d62d43e2b3a4824a8495fa6bbb4e6f083bf2381617cb2de9523cff6587912493`.
