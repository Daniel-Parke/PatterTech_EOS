---
summary: The artefact that decides a lane's success is authored outside that lane, before it runs, and does not share its context.
type: doctrine
tags: [eos]
id: DOC-SWARM-007
statement: The artefact that decides a lane's success is authored outside that lane, before it runs, and does not share its context.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0053, EV-0111, EV-0480, EV-0483]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-SWARM-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Test,
property, acceptance script, differential target or clean-context
reviewer: the form is free, the independence is not. The lane may not
write to its own harness, meaning the test files, fixtures, evaluation
scripts and CI configuration for the node being judged. Lane count is
gated on oracle strength: with a decidable external oracle, wide fan-out
is permitted; without one, cap at one or two lanes and put a person at
the merge gate. Prevents confidently wrong output accepted on its own
say-so. Generating tests with the buggy implementation in context
produced 104 effective tests against 304 from the correct implementation
and 187 from the specification alone (EV-0480). Models under evaluation
have overridden equality, exited the test process with a success code
and patched the test configuration, in production training environments
(EV-0483). Self-review without external truth degrades the answer
(EV-0111). The one run that sustained sixteen lanes had its conformance
suite, reference implementation and CI in place first, and its author's
words are that the verifier must be nearly perfect or the model solves
the wrong problem (EV-0053).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:007`, lines 173-191, SHA-256 `1e791cf6eb443f73c8dfdead218659ced2e2b3f2abae0375393e7ba7f4d36da5`.
