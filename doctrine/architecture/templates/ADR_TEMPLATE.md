---
summary: The ADR format, copy-exact, the record that carries the why
type: template
tags: [arch, eos]
template: true
---

# ADR template

Copy exactly into `org/decisions/ADR-####-<slug>.md`. An ADR exists
for every decision that closes a door (architecture doctrine rule 2).
Accepted ADRs are immutable; reversal is a new superseding ADR with
both linked. Front-matter keys are the contract the venture's
templates file also carries.

```markdown
---
id: ADR-0000
title:
status: proposed|accepted|superseded
supersedes: null
superseded_by: null
created:
approved_by: null     # the human, required for protected-set changes
review_by:
---
## Context

The forces in play, in plain words: what is true, what is wanted, what
constrains. Link the wargame if one covers this fork; the ADR then
records the ruling and its reasoning rather than re-deriving the
options.

## Decision

What was decided, stated so a stranger could implement it. Present
tense, active voice: "we run one database per service".

## Alternatives considered

Each alternative with the reason it lost. An ADR with no losers is a
description, not a decision.

## Consequences and trade-offs accepted

What this costs and what it forecloses, honestly. The next reader
weighs these against a changed world.

## Anti-patterns this guards against

Name the failure modes this decision exists to prevent, so a future
session recognises them when they knock.
```
