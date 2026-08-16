---
summary: Lexical retrieval first, embeddings earn their place.
type: doctrine
tags: [eos]
id: DOC-AIML-009
statement: Lexical retrieval first, embeddings earn their place.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0246]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-AIML-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Start with
BM25 or a hybrid, and make a dense retriever beat it on your own corpus
before adopting it. Out of domain, BM25 remains a hard baseline and
dense bi-encoders that win in-domain often lose zero-shot (EV-0246).
Reason: the cheapest baseline is also the one that generalises. Scope
note: BEIR predates modern instruction-tuned embedding models, so the
ranking is stale and the discipline of measuring against the baseline is
not.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:004`, lines 197-204, SHA-256 `320d8683c02d278e82581e8255e52ecdd03ae51cedb2041ae2e2efa21b6e152c`.
