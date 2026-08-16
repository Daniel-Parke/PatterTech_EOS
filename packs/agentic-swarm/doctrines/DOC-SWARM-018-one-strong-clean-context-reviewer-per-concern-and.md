---
summary: One strong clean-context reviewer per concern, and reviewers report rather than fix.
type: doctrine
tags: [eos]
id: DOC-SWARM-018
statement: One strong clean-context reviewer per concern, and reviewers report rather than fix.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0484, EV-0485, EV-0486, EV-0491]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-SWARM-018

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Not a panel: measured inter-judge error
correlation puts effective jury size at about two however many judges
you add (EV-0486). Asking one reviewer to explain and fix in a single
pass collapsed its recognition of correct code from 52.4 to 11.0 per
cent, and a compare-and-report prompt restored it to 85.4 (EV-0484). A
reviewer weaker than the writer may not modify the writer's output,
because it regressed 11.2 per cent of already-passing solutions
(EV-0485). One integrator ranks and deduplicates findings; they are
never merged by vote (EV-0491).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:008`, lines 275-284, SHA-256 `177869752f105c1276f87ddc45976735e91b787121ba14d704c0ee7d5adb7b6e`.
