---
id: GD-DATAENG-002
summary: Overwrite the partition, merge on a key, append-only with a view that picks the winner, or an idempotent write token?
kind: wargame
type: wargame
tags: [data, eos, ops, state, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DATAENG-002]
applies_when: [reprocesses_data]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [pending-import]
review: 2028-01
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DATAENG-002: how is a reprocess made idempotent?

## Decision question and stakes

The same window is going to be processed more than once. A retry after a
half-finished run, a correction after a bug, a backfill after a new
column, or a replay after the source resent everything it had already
sent. The fork is what the second run does to what the first run wrote.

Getting this wrong produces the one data defect with no clean recovery:
duplicate rows that nothing distinguishes, in a table other things have
already read.

## Doctrines or coverage gap under pressure

- `DOC-DATAENG-002` (binding): Reprocessing a window replaces a bounded unit or merges on a declared key. Bare append is not a reprocessing strategy.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether the rows carry a key the source keeps unique. The
  incremental-strategy documentation is blunt that every strategy but
  append is only worth the reliability of its key.
- Whether the thing being corrected lines up with the way the table is
  partitioned.
- Whether a correction can move a row from one partition to another.
- Whether readers can carry logic, or need the table to be already
  right.
- Whether the store offers an atomic commit at all. The table format
  specification's pointer swap is what makes a replacement one commit
  rather than a delete with a gap in the middle.

Applicability is `reprocesses_data`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Replace a bounded unit

*What it is.* Delete the window and write it again, or overwrite the
partition in one commit.

*Buys.* The cheapest correct answer, and the easiest to reason about:
after the run, the window holds exactly what this run produced. Needs no
key. The microbatch documentation builds its whole model on this, one
independent batch replaced atomically, so a batch can be rerun over a
period that already holds rows and the table it leaves behind does not
change.

*Costs.* Needs the table partitioned on the thing being corrected, and
needs the store to make the swap atomic. Breaks when a correction moves
a row out of the window being replaced, because the old copy sits in a
partition this run never touches.

### B. Merge on a declared key

*What it is.* Match on a key, update what matches, insert what does not.

*Buys.* Corrects rows wherever they sit, including the case that beats
option A. Handles a source that resends an old row inside a new window.

*Costs.* The most expensive, because deciding what matches means reading
the destination. Rests entirely on the key: a merge with no key degrades
into an append, and a key the source quietly reuses overwrites a
different row rather than failing.

### C. Append only, with a view that picks the winner

*What it is.* Never modify anything. Write every version with an
ingestion timestamp or a sequence number, and resolve at read time to
the latest per key.

*Buys.* The write path cannot corrupt anything, which makes retries free
and makes the raw record permanent and auditable. Late corrections need
no special handling at all.

*Costs.* Every reader inherits the resolution logic, and the moment one
reader forgets it, the numbers are wrong in a way the table looks fine
about. Storage grows with rewrites rather than with data. Still needs a
key to resolve on, so it does not escape option B's dependency, it only
moves it downstream.

### D. An idempotent write token

*What it is.* The write carries an application identifier and a version
that only increases; the target records the highest version seen for
that identifier and ignores a repeat.

*Buys.* Makes a retry safe with no key in the rows at all, and without
reading the destination to compare. The right answer when the payload
genuinely has no natural key.

*Costs.* Available in one table format's streaming integration, not
generally. It guards a repeat of the same logical write, not two
different attempts at the same period, so it does not replace A or B for
corrections. And the identifier is the whole mechanism: reuse it after
resetting the counter and the target silently ignores good writes,
which is a failure in the dangerous direction.

## Failure premises

### Premortem for A. Replace a bounded unit

Assume `A. Replace a bounded unit` was selected and the outcome failed. Test this option's stated failure mechanism first: * Needs the table partitioned on the thing being corrected, and needs the store to make the swap atomic. Breaks when a correction moves a row out of the window being replaced, because the old copy sits in a partition this run never touches.

### Premortem for B. Merge on a declared key

Assume `B. Merge on a declared key` was selected and the outcome failed. Test this option's stated failure mechanism first: * The most expensive, because deciding what matches means reading the destination. Rests entirely on the key: a merge with no key degrades into an append, and a key the source quietly reuses overwrites a different row rather than failing.

### Premortem for C. Append only, with a view that picks the winner

Assume `C. Append only, with a view that picks the winner` was selected and the outcome failed. Test this option's stated failure mechanism first: * Every reader inherits the resolution logic, and the moment one reader forgets it, the numbers are wrong in a way the table looks fine about. Storage grows with rewrites rather than with data. Still needs a key to resolve on, so it does not escape option B's dependency, it only moves it downstream.

### Premortem for D. An idempotent write token

Assume `D. An idempotent write token` was selected and the outcome failed. Test this option's stated failure mechanism first: * Available in one table format's streaming integration, not generally. It guards a repeat of the same logical write, not two different attempts at the same period, so it does not replace A or B for corrections. And the identifier is the whole mechanism: reuse it after resetting the counter and the target silently ignores good writes, which is a failure in the dangerous direction.

## Decision rule

Table is partitioned on the window being corrected and corrections stay
inside their window: A. Corrections can move a row between windows, or
the table is not partitioned on the correction axis: B, on a key the
source owner will confirm is stable, and if nobody will confirm it, that
is the finding. Raw landing zone that must stay exactly as received: C,
with the resolving view built and named at the same time, never later.
Payload with no usable key and a retry-prone writer: D, on top of A or
B rather than instead of them.

Mixing is normal and is usually right: C in the landing zone, A in the
scheduled transform, B for the one table where corrections move.

## Safe default

A. It is the only option that leaves the window in a state you can
describe in one sentence without mentioning the reader.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether the rows carry a key the source keeps unique. The incremental-strategy documentation is blunt that every strategy but append is only worth the reliability of its key.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. It is the only option that leaves the window in a state you can describe in one sentence without mentioning the reader.

**Exit condition:** Stop or roll back the selected branch when * Needs the table partitioned on the thing being corrected, and needs the store to make the swap atomic. Breaks when a correction moves a row out of the window being replaced, because the old copy sits in a partition this run never touches, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether the rows carry a key the source keeps unique. The incremental-strategy documentation is blunt that every strategy but append is only worth the reliability of its key.

## Counter-evidence and transfer limits

### Preserved reasoning: The honest weakness

No source found compares these for correctness or cost at any scale, and
the maintainer documentation puts no numbers behind its cost claims. The
case where A and B genuinely disagree, a correction that moves a row
across a partition boundary, is addressed by nothing in the evidence
set. This guide argues it from mechanism, which is weaker than evidence,
and `packs/data-engineering/PACK.md` records it as an open question.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
