---
summary: What a reviewer or a checker can verify about devops and reliability work, split into executable today and judgement
type: guide
tags: [ops, delivery, ci]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
review: 2028-01
sources: [EV-0020, EV-0201, EV-0202, EV-0204, EV-0209]
---

# CHECKS: evaluating work in this domain

The pack's evaluation criteria. Each row says what is checked, against
which requirement, and whether a script can settle it today. The split
matters: calling a judgement call executable is how a gate ends up
green and wrong.

## Executable today

These are scripts over a produced tree, a database container or a change
record. No judgement.

| Check | Verifies | Method |
| --- | --- | --- |
| C1 expand and contract are separate | Requirement 1 | No single migration file contains both an additive statement and a `DROP COLUMN` or `DROP TABLE` on the same subject |
| C2 no inverse scripts | Requirement 2 | No file matches a down or undo naming pattern anywhere in the migrations tree |
| C3 forward-only asserted | Requirement 2 | The change record carries a parseable `recovery: forward-only` field |
| C4 linear history | Requirement 3 | Migration ordinals strictly increase, no duplicates, no gaps against the existing history |
| C5 the gate exists and bites | Requirement 3 | CI invokes a migration linter that exits non-zero on destructive and backwards-incompatible findings, proven against a committed bad fixture |
| C6 risk classes named | Requirement 3 | Every migration file in the change appears in the change record with a `risk_class` from the four-class taxonomy |
| C7 migrations apply and the data survives | Requirement 1 | Applying every migration in order succeeds, and the pre-change value set reads back through the new shape with identical row count and identical values |
| C8 the compatibility window is real | Requirement 1 | Applying up to the expand step and running the pre-existing test suite unchanged passes |
| C9 restore evidence parses | Requirement 5 | The evidence record parses with the fixed key set, and re-running the committed script regenerates the same key set |
| C10 restore evidence passes | Requirement 5 | `result` is `pass`, `elapsed_seconds` is at most `rto_seconds`, `rows_validated` is greater than zero |
| C11 SLO validates | Requirement 4 | The SLO file validates against the OpenSLO schema, and the change record names the SLI at risk |
| C12 flags are owned and dated | Requirement 7 | Every flag entry has a non-empty `owner` and an `expires` that parses as a date after today |
| C13 the abort path works | Rollout default | The rollout configuration declares a failure condition and automatic abort, and a dry run against an injected failing metric returns abort rather than promotion |
| C14 no secrets in the diff | Guard | No secret-shaped string in the diff |
| C15 the repo checker passes | Estate | `python -m tools.eos check --repo` gains no new errors |

C1 to C14 are the pack's own criteria and are the same set the drill in
`benchmark/drills/devops-reliability.md` scores, which is deliberate: a
pack whose checks and whose acceptance drill disagree is testing itself
against a different thing from the one it teaches.

## Judgement, not executable

These need a reviewer. Writing a script for them would produce a number
that looks like a verdict.

- **Was the right option chosen?** A script can see that expand,
  migrate and contract exist. It cannot see whether the change needed
  online schema change tooling instead, or whether a freeze window was
  genuinely unavoidable.
- **Is the SLI worth trusting?** A machine can validate the object. Only
  a person can say whether the indicator tracks anything a user feels.
- **Is the hypothesis meaningful?** The restore evidence carries a
  hypothesis field. Whether it is falsifiable, or a sentence written to
  fill a field, is a reading.
- **Is the validation query sufficient?** A count of rows proves less
  than a value-set comparison, which proves less than a check that the
  application can read what was restored. The record shows which was
  used; judging whether it was enough is not mechanical.
- **Is the flag expiry honest?** A date eleven months out satisfies C12
  and defeats its purpose.
- **Is the postmortem timeline evidence-backed?** The deadline and the
  owner are checkable. Whether the timeline came from graphs and logs or
  from memory is not.
- **Was the contract step actually scheduled?** C1 to C8 pass with the
  contract migration written but never deployed. Whether it will land is
  a question about a plan.
- **Are the delivery numbers being used on a person?** No check can see
  this. It is the reason it is written down as a non-goal rather than
  built as a gate.

## Not checked here

Test adequacy belongs to the delivery-testing pack, threat modelling and
secret handling policy to security-privacy, and the choice of database
or hosting platform to architecture and the stack profiles. This pack
checks how change reaches production and how the system survives it.

## Known gaps in the executable set

C5 verifies the linter fails on the two decidable classes. It cannot
verify the data-dependent class, because that verdict depends on
production data distribution (EV-0202). C13 verifies the abort path for
the serving tier only; nothing here checks that data written under a
canary is compatible with the old reader (EV-0204), which is the hole
the exemplar walks through by hand. C9 and C10 prove a restore worked
under drill conditions and say nothing about restore under adversarial
conditions (EV-0201).
