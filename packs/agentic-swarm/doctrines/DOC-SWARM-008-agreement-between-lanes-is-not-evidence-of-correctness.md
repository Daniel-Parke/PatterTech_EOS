---
summary: Agreement between lanes is not evidence of correctness.
type: doctrine
tags: [eos]
id: DOC-SWARM-008
statement: Agreement between lanes is not evidence of correctness.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0481, EV-0482]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B8]
---

# DOC-SWARM-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Concurrence across models, vendors, languages or runs may not be used
as a merge criterion or as a substitute for an oracle. Prevents the
swarm's most attractive fallacy, that fan-out buys independence.
Independently generated implementations co-failed 429 times against
115.36 predicted under independence, z equals 29.20, with perfect
failure correlation in 87 of 158 cross-agent pairs, and the failures
concentrated on the specification's ambiguous clauses (EV-0481). Human
programmers were measured failing the same way in 1986 (EV-0482). The
same study measures a 66 per cent mean reduction in failures from
majority voting across three implementations, so voting is a real
reducer and still not a verdict: it may order what a person looks at
first, never decide a merge. When lanes disagree, or agree on something
wrong, suspect the specification clause first.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:008`, lines 193-206, SHA-256 `c892599a7f70dc4862e57e276a611daf297239c36e042ab572813cab5a5a382d`.
