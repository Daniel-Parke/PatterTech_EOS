---
summary: What a data contract has to carry to satisfy B1 and B2, the rule kinds available, and how a contract fails silently
type: foundation
tags: [data, delivery, testing]
kind: fact
scope: estate
sources: [EV-0056, EV-0057]
volatility: slow
review: 2028-08
---

# Data contract reference

Level-three material behind binding requirements B1 and B2 and guide
`packs/data-analytics/guides/GD-DATA-001-quality-gate-placement.md`.
The pack binds what a contract must carry and what happens when it
fails. It does not bind the format.

## The five things one document has to carry

A contract that omits any of these leaves an unowned gap
(`EV-0305`).

| Element | What it states | Why it cannot live elsewhere |
| --- | --- | --- |
| Schema | column names, types, nullability, keys | the shape consumers write against |
| Quality rules | what must be true of the values | a schema alone says nothing about correctness |
| Freshness | how stale the data may be | a correct and eight-hour-stale table is an outage |
| Owner | one named person or team | a rule with no owner fires into an empty room |
| Support path | where a consumer reports a problem | otherwise the problem arrives as a complaint about the product |

The format war is unsettled: a dedicated contract standard, a
transformation tool's own schema file and an expectation suite all
satisfy this. Pick one, put all five in it, and treat the choice as
taste. Sections aimed at inter-company data sharing, such as pricing and
infrastructure metadata, are dead weight inside a single venture.

## Rule kinds, and what each catches

| Kind | Example | Catches | Misses |
| --- | --- | --- | --- |
| Presence | column not null | dropped fields, failed joins | wrong values that are present |
| Type and shape | numeric, matches pattern | upstream schema change | unit changes inside the same type |
| Range | value between bounds | corrupted or defaulted values | plausible wrong values |
| Set membership | status in an accepted list | new enum values arriving unannounced | old values that stop appearing |
| Uniqueness | one row per declared grain | fan-out from a bad join | duplicate business events upstream |
| Referential | every key resolves | orphaned rows | keys that resolve to the wrong thing |
| Volume | row count within expected band | pipeline partial failure | slow drift |
| Freshness | maximum age of the newest row | stalled pipeline | data that arrives on time and wrong |
| Distribution | metric within its historic band | drift nobody wrote a rule for | a bug that arrived before the history did |

The first eight are declared. The ninth is computed, needs history, and
is the only one that catches what you failed to anticipate
(`EV-0306`).

## Blocking against monitoring

B2 says a quality gate failure blocks publication. Concretely:

- The check runs inside the build, as a step the pipeline depends on,
  not as a job scheduled afterwards.
- Failure exits non-zero and the downstream publish step does not run.
- The previous good version of the table stays visible to consumers.
- The failure names the rule, the column and the offending row count.

A check that runs after publication and opens a ticket is monitoring. It
is worth having. It is not a gate, and calling it one is how a pipeline
ends up with documentation where its gate should be.

## Contract scope

Contracts freeze the interface of models other people read, while
internals refactor freely, and private models carry no contract ceremony
(EV-0057). The test for whether a model is public: can you name a
consumer outside the session that wrote it? If not, no contract.

## How a contract fails silently

- **Semantic drift.** A column that changes from pence to pounds passes
  every shape check. No source found offers a gate. Put the unit in the
  column name and treat unexplained metric step changes as bugs.
- **Suggested constraints.** Rules derived from the current data encode
  whatever the data currently does, including the defect
  (`EV-0306`). Read every suggestion before accepting it.
- **Expectation rot.** A suite checks what you declared, not what you
  forgot to declare, and the gap grows as the product changes (EV-0056).
- **The contract nobody runs.** The most common failure. Criteria 1 and
  2 of the pack drill pass while criterion 3 fails, and that combination
  is worth logging separately because it looks like compliance.
