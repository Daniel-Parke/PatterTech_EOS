---
summary: Whoever writes carries the burden.
type: doctrine
tags: [eos]
id: DOC-RESEARCH-006
statement: Whoever writes carries the burden.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [keeps_a_knowledge_base]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0546]
review: 2029-08
lifecycle: active
verification_refs: [packs/research-knowledge/CHECKS.md]
migration_sources: [packs/research-knowledge/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-RESEARCH-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Anyone may read the knowledge
base. The person adding or restoring a claim owes the citation, and a
claim that needs one and lacks one is marked unsourced rather than
silently kept (EV-0546). Marked, not deleted: on a wiki removal is cheap
because history holds the text, and in most venture knowledge bases
removal loses the only copy. Predicate: `keeps_a_knowledge_base`.
Prevents: unsourced assertions accumulating faster than anyone can audit
them, which is how a knowledge base becomes a folklore store with
citations in it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/research-knowledge/PACK.md:requirements:006`, lines 179-187, SHA-256 `7ca10cf879a05535ad41eabe7344d51b7249932c40553e04be5aca03ead1c065`.
