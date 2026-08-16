---
summary: A gate oracle is observed failing before its green result counts as acceptance evidence.
type: doctrine
tags: [eos]
id: DOC-COD-002
statement: A gate oracle is observed failing before its green result counts as acceptance evidence.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [decides_merge]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0003, EV-0006, EV-0007, EV-0105, EV-0191, EV-0192]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-COD-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

*Independent.* The artefact that decides whether a change is correct is not authored by the agent holding that implementation in its context. *Seen to fail.* Before an oracle counts at the gate, it has been observed red: against the parent commit, against the change reverted, or against a seeded fault. And the vacuous check, a green suite nobody has ever seen go red: agent test-writing frequency is about the same in runs that resolve and runs that do not, because what gets written is mostly observational prints (EV-0006).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:requirements:001`, lines 84-113, SHA-256 `97b67e4ca83f78c270813ea4b0ca2805f8f5a96911f4be3c53b2bbb8c0afd513`.
