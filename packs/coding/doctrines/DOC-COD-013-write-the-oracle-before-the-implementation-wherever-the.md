---
summary: Write the oracle before the implementation wherever the condition can be stated.
type: doctrine
tags: [eos]
id: DOC-COD-013
statement: Write the oracle before the implementation wherever the condition can be stated.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0006, EV-0178]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-COD-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

For a FIX that means the failing reproduction, which is
available before any code exists. Reason: it is the cheapest way to
satisfy B1's independence clause, because at that moment there is no
implementation to read. It is a default and not a rule because ordering
is not what the evidence measures. Prompting for more tests across the
500 tasks of SWE-bench Verified changed test-writing behaviour on most
tasks and left the number resolved statistically unchanged (EV-0006),
and in the human literature the active ingredient was granularity and
uniformity rather than sequencing (EV-0178). Override by recording where
the oracle did come from, which is what B1 actually wants.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:007`, lines 245-255, SHA-256 `f0b172c45f27b8270a025fc845f29a91557fe2a9ea344d211bf6bb3428de6f41`.
