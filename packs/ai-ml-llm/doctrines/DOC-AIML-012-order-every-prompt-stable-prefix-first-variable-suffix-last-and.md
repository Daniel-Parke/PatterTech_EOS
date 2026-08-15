---
summary: Order every prompt stable prefix first, variable suffix last, and assert the cache hit rate.
type: doctrine
tags: [eos]
id: DOC-AIML-012
statement: Order every prompt stable prefix first, variable suffix last, and assert the cache hit rate.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0243, EV-0261]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-AIML-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Cached prefix reads are charged at a tenth
of base input while writes cost more, minimum cacheable length varies by
model, and short prompts fail to cache with no error, so the only
reliable check is reading the cache token counts back from the response
(EV-0261). Reason: cost is decided in prompt layout before it is decided
in model choice. This default fights the evidence placement rule in
EV-0243 and the conflict is resolved per prompt in
`packs/ai-ml-llm/refs/CONTEXT_LAYOUT.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:007`, lines 223-231, SHA-256 `3b4a40edc7641421690cc32a6d8b9a6f8d8566f8da1cf7b1a09fb380580fcde0`.
