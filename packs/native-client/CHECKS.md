---
summary: What a reviewer or checker can verify about client work, split into executable today and judgement
kind: record
scope: estate
sources: [EV-0026, EV-0027, EV-0206, EV-0235, EV-0236]
volatility: slow
review: on-change-of:EN-301-549-v4-publication
type: checks
tags: [testing, a11y, delivery]
---

# CHECKS

Evaluation criteria for work in this domain. Each row says what is
verified, against which requirement, and whether a machine can settle
it today. "Executable" means a script decides it without a human
reading the output. "Judgement" means a person rules and the record is
the evidence.

B4, B5 and B6 bind. B1, B2, B3 and B7 are defaults since the ADR-0008
audit, so the rows behind them still run and a venture that departs
records why. J9 already covers the reason being written down.

## Executable today

| # | Check | Verifies | How |
| --- | --- | --- | --- |
| C1 | A decisions file exists and names the architecture and one policy per write class | B1 | schema validation of the decisions file |
| C2 | The policy vocabulary is closed | B1 | every policy value is one of `converge`, `last-writer-wins`, `reserve-then-commit`, `reject-offline` |
| C3 | No invariant-bearing class takes a merging policy | B2 | assert the class is neither `converge` nor `last-writer-wins` |
| C4 | Evidence ids in the decisions file resolve | B1 | lookup against `registry/evidence.json`, at least three ids |
| C5 | Partition test asserts the documented outcome per class | B1, B2 | two clients from one snapshot, scripted divergent offline edits, reconnect, assert per class |
| C6 | Partition outcome is order-independent | B1, B2 | run C5 twice with reconnection order swapped, assert byte-identical final state |
| C7 | Exactly one holder after convergence on a contested resource | B2 | assertion inside C5, plus a recorded compensation event for the loser |
| C8 | No acknowledged write is lost to process death | B3 | kill mid-write, restart, assert the write is present |
| C9 | The outbox is idempotent under replay | B3 | deliver the same mutation repeatedly, assert one effect |
| C10 | A blocked queue does not deadlock the app | B3 | stall an acknowledgement, assert reads and rendering continue and the named degraded state appears within a fixed timeout |
| C11 | Flag evaluation works while the queue is blocked | B4 | drive C10's state, then flip the kill switch, assert it takes effect |
| C12 | A named kill-switch flag exists and the old path still passes | B4 | with the flag off, the new behaviour is unreachable and the previous path's tests pass |
| C13 | The release document contains no rollback wording | B4 | grep for rollback phrasing, fail on any hit |
| C14 | The release document has one section per store | B4 | assert both store sections and a named halt metric per store |
| C15 | The over-the-air manifest cannot change capability | B5 | diff against the binary manifest, fail on any permission or native module delta |
| C16 | Automated accessibility audit runs over every screen and fails on violation | B6 | platform audit in the test suite, one run per screen, zero violations |
| C17 | Manual verdict file entry count equals the audit's undecided count | B6 | compare counts, fail on mismatch |
| C18 | No unlabelled interactive element, decoration explicitly marked | B6 | static check over the semantics declarations |
| C19 | Conformance is claimed per screen | B6 | the claim file has one row per screen, not one row per app |
| C20 | Removed server fields are absent from no live client version | B7 | contract diff against the supported version matrix before a contract step |
| C21 | Target SDK level meets the current store floor | D5 | read the build configuration, compare against the recorded deadline |

C6 is the discriminating check. A partition test that passes in one
reconnection order and not the other proves the outcome is a property
of the timing rather than of the policy, which means B1 was never
really decided.

C16 does not prove accessibility. No coverage figure is published for
these audits at all, and on the web the equivalent figure is contested
(EV-0236). No detected errors does not mean accessible (EV-0235), which
is why C17 exists and why the judgement rows below carry real weight.

## Judgement, recorded not automated

| # | Check | Verifies | What good looks like |
| --- | --- | --- | --- |
| J1 | The write classification is right | B1 | the invariant is named out loud for every invariant-bearing class, in one sentence a non-engineer understands |
| J2 | Each undecided audit item has a real verdict | B6 | a sentence naming what was inspected and the conclusion, not "looks fine" |
| J3 | Clause 11 obligations were checked deliberately | B6 | the app driven end to end with the platform screen reader, and user preference settings honoured, both recorded |
| J4 | Compensation is visible to the user who lost | B2 | the person is told what happened and what to do, in the interface, not only in a log |
| J5 | The degraded state message is usable | B3 | it names what is stuck and what the user can still do |
| J6 | The architecture ruling names its runner-up | WG-NAT-001 | the runner-up and the cost of not taking it are both written down |
| J7 | The halt trigger is decidable during the ramp | B4, D3 | the metric exists in telemetry, the threshold is a number, and someone is named to watch it |
| J8 | The over-the-air envelope is presentation only | B5 | a reviewer can say what changed and it is copy, styling, assets or layout |
| J9 | Defaults departed from carry a recorded reason | defaults section | the reason is in the task record, not in a commit message alone |
| J10 | Copy reads as though a person wrote it | voice law | read aloud before shipping |

## Not verifiable here

- **Whether one architecture outperforms another.** No retrievable,
  methodologically serious comparison exists on performance, energy or
  defect rate, so no check claims it.
- **Whether the app is accessible.** C16 to C19 gate what a machine can
  see. The rest is J2, J3 and, above a certain risk, testing with
  disabled users under WG-NAT-004 option D.
- **Whether a release was safe.** Neither store can take a version
  back, so the only evidence is the kill switch working and the metric
  holding.
- **The rejection risk of a specific submission.** The published
  category counts are a self-reported vendor census and do not
  decompose into engineering actions.

## Cadence

C1 to C4 run whenever the decisions file changes. C5 to C12 and C16 to
C19 run on every change set. C13, C14 and C15 run on every release
preparation. C20 runs before any contract-removal step (EV-0206). C21
runs weekly and on every store deadline change. The judgement rows run
at review, and J1 and J6 run once at the point the decision is taken,
then again if a new write class appears or the team shape changes.
