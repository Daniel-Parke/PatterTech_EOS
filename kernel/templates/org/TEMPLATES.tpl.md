---
summary: Canonical artefact formats template, front-matter contracts for orders, decisions, logs and registries
type: template
tags: [eos]
template: true
extracted_from: Venture A@d2e3250
---

# Templates · Canonical artefact formats

Copy exactly; front-matter keys are contracts other sessions and future
automation rely on. Dates ISO (`YYYY-MM-DD`). IDs are allocated by
taking the next number in the relevant directory or file; check before
writing.

<!-- scale: M -->
## Queue item (a row of `org/QUEUE.md`)

```markdown
### WO-#### · <title>
- type: FEAT|FIX|REFACTOR|PERF|MAINT|HARDEN|COMPLY|RESEARCH|DOCS|OPS|SPIKE
  · tier: T1|T2|T3 · priority: P0|P1|P2|P3 · status: ready|in_progress|
  in_verification|blocked
- acceptance: [ ] checkable criteria, one box each
- done when: <the observable finish line, including the gates>
```

Queue sections: Ready (ordered), Blocked, Done (id, session, date).
Done rows may be pruned a quarter after completion; git keeps history.
<!-- scale: end -->

<!-- scale: L -->
## Work order · `org/work/items/WO-####-<slug>.md`

```markdown
---
id: WO-0000
title:
type: FEAT|FIX|REFACTOR|PERF|MAINT|HARDEN|COMPLY|RESEARCH|DOCS|OPS|SPIKE
practice: product|engineering|quality|security|compliance|operations|data|experience|knowledge
priority: P0|P1|P2|P3
risk_tier: T1|T2|T3|T4
status: draft|ready|in_progress|in_verification|done|blocked|cancelled
claims: []            # path globs this WO may touch
depends_on: []        # WO ids
links: []             # specs, ADRs, registry rows
created:
updated:
session: null         # owning session id when in_progress
---
## Context
Why this exists; link, don't restate.

## Scope
**In:** ...
**Out:** ... (be explicit; this fence is what VERIFY enforces)

## Acceptance criteria
- [ ] ...

## Test specification
Given / When / Then at the levels the type requires.

## Verification requirements
What review must specifically confirm; anything unusual for the tier.

## Notes log
- YYYY-MM-DD S-#### ...

## Verification record
- gate / verdict / session / date / evidence
```

## Suggestion · `org/work/suggestions/SUGG-####-<slug>.md`

```markdown
---
id: SUGG-0000
from_session: S-0000
practice:
created:
status: open|promoted|merged|declined
resolution: null      # WO id, or one-line reason
---
**Observation:** what you saw, with evidence (file, line, commit).
**Proposal:** what you think should happen.
**Why it matters:** the cost of ignoring it.
```
<!-- scale: end -->

## Decision · `org/decisions/ADR-####-<slug>.md`

```markdown
---
id: ADR-0000
title:
status: proposed|accepted|superseded
supersedes: null
superseded_by: null
created:
approved_by: null     # the human, for protected-set changes
review_by:
---
## Context
## Decision
## Alternatives considered
Each with the reason it lost.
## Consequences and trade-offs accepted
## Anti-patterns this guards against
```

<!-- scale: L -->
## Research note · `org/knowledge/research/RN-YYYYMMDD-<slug>.md`

```markdown
---
id: RN-YYYYMMDD-slug
question:
practice:
maturity: L0
confidence: high|medium|low
sources: []           # url plus date_accessed for each
created:
review_by:
supersedes: null
---
## Findings
## Recommendation
## What this changes (orders or suggestions filed, or "nothing, because...")
```

Guidance (`org/knowledge/guidance/`) and standards (`org/standards/`)
use the same front-matter with `maturity: L1` or `L2`, plus
`owner_practice:` and, for standards, `enforced_by:` (the L3 checks, or
`manual` until automated).

## Registry row (inside any `REG-*` file)

```markdown
### OBL-### · <short name>
- **Obligation/target:** what must be true
- **Source:** law, standard or decision, with link
- **Applies to:** surfaces, data, processes
- **Status:** met | partial | gap | deferred(trigger: ...) | n/a(reason)
- **Control:** what we do or build so it is true
- **Verification:** how we prove it (test, audit step, document, monitor)
- **Owner:** practice · **Review by:** date · **Evidence:** links
```
<!-- scale: end -->

## Session log · `org/logs/YYYY-MM/S-####-<role>.md`

```markdown
---
id: S-0000
role: PLAN|WORK|VERIFY|HUMAN
date:
model:
launcher:
items_touched: []
commits: []           # short hashes
spend_estimate:
---
## What happened
5 to 15 lines, past tense, facts.
## Decisions taken (within my authority)
## Filed
Questions, suggestions and orders created.
## Handoff
Exact next action if anything is unfinished.
```

<!-- scale: L -->
## Audit report · `org/metrics/audits/AUD-YYYYMMDD-<practice>.md`

```markdown
---
id: AUD-YYYYMMDD-<practice>
practice:
session:
scope_sampled:
---
## Findings
### F1 · <severity: critical|major|minor|observation> · <title>
Evidence, impact, recommendation, filed as: WO or SUGG id.
## Registry deltas applied
## Scoreboard deltas applied
```
<!-- scale: end -->
