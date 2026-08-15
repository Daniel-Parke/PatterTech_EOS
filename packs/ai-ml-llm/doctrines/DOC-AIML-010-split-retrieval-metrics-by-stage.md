---
summary: Split retrieval metrics by stage.
type: doctrine
tags: [eos]
id: DOC-AIML-010
statement: Split retrieval metrics by stage.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0247, EV-0265]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-AIML-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Measure context precision and
recall for the retriever separately from faithfulness and answer
relevance for the generator (EV-0265), and measure groundedness against
the retrieved context separately from answer correctness, because a
system can be right and ungrounded or grounded and wrong (EV-0247).
Reason: a single end-to-end score cannot tell you whether to fix the
retriever or the prompt.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:005`, lines 206-212, SHA-256 `508a7b555cd2a91d67fdce5adf3a267fe97217586439ae843bc16ec43bf0fa56`.
