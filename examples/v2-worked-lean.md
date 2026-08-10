---
summary: Worked example, an Express run end to end in an S venture, from request to commit
type: example
tags: [eos]
---

# Worked example: the lean run

One task, start to finish, in the smallest shape v2 offers. The venture
is Herbfield Lane, the S seed at benchmark/fixtures/seed-v2-S, which is
a real compiled seed in this repository and passes the seed check with
zero errors. Read this beside examples/v2-worked-high-assurance.md; the
same kernel produces both, and the difference is entirely the ruling.

Paths below that start with docs/ are the venture's own; in this
repository they sit under benchmark/fixtures/seed-v2-S, so
benchmark/fixtures/seed-v2-S/docs/LOCKBOOK.md is the lock-book this
example reads and benchmark/fixtures/seed-v2-S/docs/policy.json is the
policy it routes against.

The scene is two weeks after Session 0. The first-build lock-in, the
top row of benchmark/fixtures/seed-v2-S/docs/TASKS.md, has landed, so
the QC gate section of the lock-book now names real commands instead of
deferrals.

## The request

The operator sends one line: the workshop phone number has changed, the
new one is on the invoice. Nothing else.

## Boot

The agent opens benchmark/fixtures/seed-v2-S/AGENTS.md, thirty-two
lines including its front-matter and the whole of the always-loaded
surface. It says what to read, in order: the lock-book, then route,
then record.

From the lock-book the agent reads two sections and skips the rest: the
structural contracts, six lines, and the QC gates, thirteen lines. The
identity, narrative and token sections are not touched by a phone
number and are not read.

That is forty-four lines of context beyond the task itself, against the
Express budget of sixty in docs/policy.json. Nothing else loads. No
pack activates, because a copy change satisfies no pack's predicates:
the UI and UX pack wants a design or component decision and this is
neither.

## Route

The agent declares its facts and routes before working:

```json
{"capabilities": [], "side_effects": []}
```

The router rules:

```json
{"tier": "R0", "reasons": [], "discrepancies": []}
```

An empty reasons list is the honest output when no factor is active.
The phone number is not auth, not money, not personal data under the
firm's own name, not a schema, not a public contract, and the diff is
two lines in two files. R0 routes to Express per kernel/POLICY_SPEC.md.

## Mode

Express, as docs/policy.json defines it: context pack sixty lines,
artefacts a commit message and nothing else, verification targeted
checks, test timing alongside. Three stop conditions sit on the mode,
and the agent holds them the whole way: a durable-band decision, a
derived risk fact changing mid-run, or a diagnosis that needs a
hypothesis ledger. Any of them converts the run to Standard before it
continues.

## Decide

Everything here is in the free band: copy per the applicable voice
scope, and file placement in an existing scheme. The agent decides and
records the decision in the commit message. There is nothing to
escalate and nothing durable to write down.

## Do and verify

Two edits: the contact page copy and the same number in the brief,
because the brief is the venture's business truth and a stale number
there would outlive the page. Then the targeted checks the lock-book's
QC gates name for a copy-only change: the build, and the overflow check
at 375 pixels because the number's length changed. The full screenshot
and regression sets do not run; they are not affected and Express does
not run unaffected suites.

## Close

The commit message is the whole record:

```
contact: the workshop number changes to the new line

The operator's workshop number changed. Updated the contact page and
docs/VENTURE_BRIEF.md, which holds the same fact as business truth.

Routed R0, no factor active. Express. Build green, overflow at 375
green. Copy follows the WG-VOX-001 register ruling in the lock-book.
```

That is the end. No row was added to docs/TASKS.md, because Express
work needs none and the template says so. No task record exists,
because R0 does not create one. No session log was written, because git
is the log in v2. No derived view moved, because no record changed.

## What it cost

Forty-four lines of boot reading, one commit, two checks. Under v1 the
same change would have opened a work order, claimed the session in
STATE, written a session log with a Resume Packet at close, and run the
full gate ladder from G1. That gap is the whole argument for the
router, and it is why the benchmark measures ceremony lines rather than
counting features.

## What would have changed the answer

- The number belonging to a named private individual rather than the
  workshop: personal data, floor R2, High-assurance.
- The same edit inside a payment or auth surface the policy lists as
  sensitive: floor R2.
- A publish step to a new external destination: the guard rules that
  action manual-only under kernel/GUARD_SPEC.md whatever the tier says,
  and the operator performs it outside the agent.
- Realising mid-run that the contact page needs restructuring: a
  durable-band decision, so the run converts to Standard, opens a task
  record, and the commit stops being the whole record.
