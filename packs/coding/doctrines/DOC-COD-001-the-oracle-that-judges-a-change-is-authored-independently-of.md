---
summary: The oracle that judges a change is authored independently of the implementation under test.
type: doctrine
tags: [eos]
id: DOC-COD-001
statement: The oracle that judges a change is authored independently of the implementation under test.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0003, EV-0006, EV-0007, EV-0009, EV-0105, EV-0191, EV-0192]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:requirements:001, packs/delivery-testing/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-COD-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

### `packs/coding/PACK.md:requirements:001`

*Independent.* The artefact that decides whether a change is correct is not authored by the agent holding that implementation in its context. *Seen to fail.* Before an oracle counts at the gate, it has been observed red: against the parent commit, against the change reverted, or against a seeded fault. Mutual consistency, where a check written from the code agrees with the fault it should catch: tests generated after faulty code detected roughly half the faults of independently generated tests, 14 per cent against 25 per cent (EV-0007), and surfacing the right test context cut regressions from 6.08 to 1.82 per cent (EV-0003).

### `packs/delivery-testing/PACK.md:requirements:001`

The
   check that decides whether the change is correct is derived from the
   specification, the reproduction, an invariant or a reference, never
   read back off the code just written. Basis empirical-evidence,
   grade controlled: tests generated after faulty code detected roughly
   half the faults of tests generated independently, 14% against 25%
   (EV-0007), and coverage and mutation numbers stop being informative
   exactly when the code may already be wrong (EV-0009). Both results
   come from task-level programming problems and LLM suites, so the
   number is theirs and the principle is what carries. Prevents: the
   test learning the bug and then certifying it. This says nothing about
   when the check is written; ordering is a default and lives in
   WG-DEL-007. See WG-DEL-006.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:requirements:001`, lines 84-113, SHA-256 `97b67e4ca83f78c270813ea4b0ca2805f8f5a96911f4be3c53b2bbb8c0afd513`.
- `packs/delivery-testing/PACK.md:requirements:001`, lines 88-100, SHA-256 `4b6bb28d40378bb0c366bf63484e458c0e33a33ec165a962bfa2ef8c13f60543`.
