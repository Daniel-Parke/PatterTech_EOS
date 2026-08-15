---
summary: Grade a sample by hand before writing the rubric.
type: doctrine
tags: [eos]
id: DOC-AIML-006
statement: Grade a sample by hand before writing the rubric.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0254]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-AIML-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Criteria are
discovered by grading outputs, not declared in advance: practitioners
cannot say what good looks like until they have seen concrete bad
outputs, so requirements and evaluator co-evolve (EV-0254). Reason: a
rubric fixed up front measures the wrong thing with great rigour.
Override only where an external standard already defines the criteria.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:001`, lines 173-178, SHA-256 `05adf4086350a38edd5bae412fe501cd1db970bbcb25ca2f48ab4d4fec5cd28f`.
