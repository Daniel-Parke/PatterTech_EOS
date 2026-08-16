---
summary: If a step can be code, make it code.
type: doctrine
tags: [eos]
id: DOC-SWARM-025
statement: If a step can be code, make it code.
kind: doctrine
authority: preference
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0010, EV-0053, EV-0107, EV-0108, EV-0109, EV-0111, EV-0112, EV-0244, EV-0450, EV-0451, EV-0452, EV-0453, EV-0454, EV-0455, EV-0456, EV-0457, EV-0458, EV-0459, EV-0460, EV-0461, EV-0463, EV-0464, EV-0466, EV-0467, EV-0468, EV-0469, EV-0470, EV-0472, EV-0475, EV-0476, EV-0477, EV-0478, EV-0480, EV-0481, EV-0482, EV-0483, EV-0484, EV-0485, EV-0486, EV-0487, EV-0488, EV-0489, EV-0491, EV-0493, EV-0494, EV-0495]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:preferences:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SWARM-025

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Ordering, filtering, joining, counting and branching belong in the orchestrator, not in a node.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:preferences:001`, lines 328-329, SHA-256 `6c63bcd9b9529dac47a5001f5f7dc533ece635aa9720171d8f9ab232a90e9f25`.
