---
summary: Trained cascade routing against model self-assessment routing.
type: doctrine
tags: [eos]
id: DOC-AIML-017
statement: Trained cascade routing against model self-assessment routing.
kind: doctrine
authority: preference
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0245, EV-0262]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:preferences:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-AIML-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A
  trained confidence scorer and a cheap first model is one shape
  (EV-0262); asking the model whether the retrieved context suffices is
  another (EV-0245). Both work in their own papers, on retired models.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:preferences:002`, lines 279-282, SHA-256 `470bf2efe37d517ffa83035cc4d68c65bf29bff0278ecee5b763eac37602204a`.
