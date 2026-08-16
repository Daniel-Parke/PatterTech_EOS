---
summary: The packet is closed and literal.
type: doctrine
tags: [eos]
id: DOC-SWARM-002
statement: The packet is closed and literal.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0108, EV-0466, EV-0467]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-SWARM-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Nine fields, all present:
objective; the exact write set; the exact read set or named sources; the
return contract; the tool set; the token and call budget; the stop
condition; the acceptance condition; and a named escape for the case
where the packet does not determine something. Targets are literal
paths, ids and symbol names, never "the auth module". Nothing is assumed
inherited, because nothing is: the spawn prompt is the only channel and
the lead's history does not carry over (EV-0108). Prevents wrong-target
action. Safe success falls from 67.9 per cent at full target certainty
to 8.6 per cent at maximum ambiguity, the wrong-target rate rises to
75.1 per cent, and agents act rather than ask in 36 to 84 per cent of
runs even when the instruction is plainly underdetermined (EV-0466);
pass@1 on otherwise solvable tasks collapsed from 89.02 to 8.94 per cent
under injected ambiguity (EV-0467). The escape is not a courtesy.
Whether an agent asks is a property of the harness rather than the
model, so the orchestrator treats "the packet does not determine X" as a
first-class outcome with no penalty attached. Field by field in
`packs/agentic-swarm/references/PACKET_AND_RETURN.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:002`, lines 107-124, SHA-256 `6bc9079e5827296ae8e26c477d0e33ced317056399f8d16c95651b8d1b1dc3c9`.
