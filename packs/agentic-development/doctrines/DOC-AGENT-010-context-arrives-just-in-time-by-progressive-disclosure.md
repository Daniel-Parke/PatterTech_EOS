---
summary: Context arrives just in time, by progressive disclosure.
type: doctrine
tags: [eos]
id: DOC-AGENT-010
statement: Context arrives just in time, by progressive disclosure.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0083, EV-0086, EV-0114]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-AGENT-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Load
identifiers and summaries, fetch bodies on demand, rather than
pre-loading everything (EV-0086, EV-0114, EV-0083). Reason: tool and
document surface is a context cost, and one worked vendor example fell
from about 150,000 tokens to about 2,000 on this change alone.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:006`, lines 194-198, SHA-256 `78e4be384c55574fbfd9ee9912c783051319ce197670a308c8fc5d2693610dd3`.
