---
summary: What a reviewer or a script can verify about a pipeline in this domain, split into executable today, judgement, and what no check reaches
type: guide
tags: [data, ops, ci]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
review: 2027-11
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
---

# CHECKS: evaluating work in this domain

The pack's evaluation criteria. Each row says what is checked, against
which requirement or default, and whether a script can settle it today.
The split is the point: calling a judgement executable is how a green
gate ends up wrong, and in this domain a wrong answer looks exactly like
a right one.

## Executable today

Scripts over a pipeline's code, its configuration, its run ledger and a
test fixture. No judgement.

| Check | Verifies | Method |
| --- | --- | --- |
| C1 rerun equality | B2 | Run a window, snapshot the target, rerun the same window, compare. Row count and value set identical, and the run ledger's `rows_out` unchanged |
| C2 no bare append on a reprocessable target | B2 | No write path into a target the pipeline may rerun uses append with no key and no replacement; `strategy` in the ledger is never absent |
| C3 every hop is declared and its sink is honest | B1 | Each hop has the six fields in `packs/data-engineering/refs/DELIVERY_GUARANTEES.md`, and no hop pairs `guarantee: at-least-once` with `sink_idempotence: none` |
| C4 no exactly-once claim without a cooperating sink | B1 | A hop claiming `exactly-once` names a sink from the two rows that can supply it: a transaction covering position and output, or the position stored with the output |
| C5 the lateness horizon exists | B3 | The pipeline declares a lookback, an allowed lateness or a full recompute, as a value in configuration rather than in prose |
| C6 late records have a destination | B3 | A quarantine target exists, the pipeline writes to it on the late path, and a fixture record past the horizon lands in it |
| C7 no clock in the window | D1 | No call to a current-time function appears in the code that derives the window or the partition value. The run ledger's `window_source` is `scheduler`, `event-time` or `high-water-mark` |
| C8 the window is half-open | D1 | `window_start` inclusive and `window_end` exclusive, proven by a fixture row exactly on the boundary appearing in one window and not both |
| C9 backfill is the same code | D2 | The backfill entry point resolves to the same callable as the scheduled entry point, differing only in parameters. No file matching a backfill script pattern outside the pipeline package |
| C10 the partition value is derived once | D4 | Exactly one function returns the partition value, every write path calls it, and it has a test crossing a daylight-saving boundary and a midnight in a non-UTC zone |
| C11 the run ledger is complete | D7 | Every run writes a row with all thirteen fields, and a run that failed still writes one with `result: fail` |
| C12 reconciliation holds | D7 | For every ledger row, `rows_in` equals `rows_out` plus `rows_quarantined` plus a declared filtered count |
| C13 the schedule can absorb a rerun | D5 | Measured runtime of one window is less than the schedule interval, from the ledger's own timestamps |
| C14 no secrets in the diff | Guard | No secret-shaped string in the diff, including in connector configuration |

C1 is the one to build first. It is the only check that tests the claim
the whole pack rests on, and a pipeline that fails it fails B2 whatever
its configuration says.

C7 is the cheapest and catches the most expensive defect. It is a
lint rule over one module.

## Judgement, not executable

These need a reviewer. A script over them would produce a number that
reads like a verdict.

- **Is the lookback the right length?** C5 proves a number exists. Only
  the quarantine's own arrival distribution says whether it is the right
  number, and only a person can tell a genuinely late record from a
  vendor replay.
- **Is the dedupe key actually unique in the source?** A merge on a key
  the source reuses overwrites a different row and reconciles perfectly.
  Uniqueness in the sample is not uniqueness in the source, and the only
  real check is asking whoever owns the source.
- **Is the partition column the correction axis?** C10 proves the value
  is derived safely. Whether it is derived from the right column, so
  that a correction can be expressed as a replacement at all, is a
  reading of how corrections actually arrive.
- **Does the ingestion shape see everything it needs to?** A polling
  extract that cannot see a delete reconciles for ever while quietly
  keeping rows the source dropped. No count anywhere moves.
- **Is the quarantine being read?** C6 proves records land in it. An
  unread quarantine is a drop with extra storage, and nothing mechanical
  can tell the difference.
- **Was the guarantee claim inherited or established?** C4 checks a
  declared sink type against a list. Whether the sink really behaves
  that way under a partial failure is an argument about a system nobody
  in the venture wrote.
- **Is a restatement acceptable to consumers?** Holding a window open
  and revising a number is a contract with whoever already acted on the
  first answer. That is a conversation, not a setting.

## Not checked here

Whether the number is the right number, whether the model's grain is
declared, whether an event is well named and whether a quality rule
blocks publication all belong to `packs/data-analytics/CHECKS.md`.
Migration mechanics, restore proof and rollout belong to
`packs/devops-reliability/CHECKS.md`. Threat modelling and access to the
source's credentials belong to `packs/security-privacy/PACK.md`. This
pack checks that the bytes arrived correctly and can be made correct
again.

## Known gaps in the executable set

C1 proves idempotence over the input it was given. It cannot prove it
over an input that changed between the two runs, which is the case a
real rerun faces, so the fixture has to be frozen and the check is
therefore weaker than the property it is named for.

C3 and C4 check declarations against a list of sink types. Nothing here
verifies that a store actually behaves as its row claims under a partial
failure, and the change-capture project's own exactly-once page is the
reason to doubt the strongest claims in that list rather than to trust
them.

C12 reconciles counts and says nothing about values. A transform that
corrupts every row while preserving the count passes it. That gap is
covered by quality rules, which are `packs/data-analytics/PACK.md`, and
naming the boundary is more useful than building a weak version of
somebody else's gate here.

Nothing in this set measures how much data actually arrives late,
because no run of the pipeline can distinguish a record that is late
from one that will never come. Only the quarantine, read by a person
over weeks, converts that into a number.
