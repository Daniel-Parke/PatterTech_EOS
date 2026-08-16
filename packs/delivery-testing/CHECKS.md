---
summary: What a reviewer or a checker can verify about delivery and testing work, and which checks run today
kind: record
scope: estate
authority: default
lifecycle: active
basis: decision
evidence_grade: not-applicable
sources: [EV-0007, EV-0015, EV-0016, EV-0186, EV-0187, EV-0190, EV-0195]
review: 2027-08
type: checks
tags: [delivery, testing, ci]
---

# CHECKS: delivery, testing and quality

Evaluation criteria for work in this domain. Each check names the
requirement it serves and whether a machine can decide it today.
"Executable" means a script can rule on it with no human reading;
"partly" means a script narrows it and a person rules; "judgement"
means a person rules.

## Mechanical checks

| Id | Check | Serves | Executable today |
| --- | --- | --- | --- |
| C1 | The new or changed test goes red when the implementation is reverted | Requirement 1 | Executable: revert the file, run the suite, expect non-zero |
| C2 | The new test reaches the code through its public interface only, with no private attribute access and no patching inside the module under test | Requirement 1 | Executable: AST scan of the added test |
| C3 | No retry, rerun or flaky marker added to a blocking gate in the diff, in test code or in CI configuration | Requirement 4 | Executable: diff and config grep |
| C4 | Every quarantine record carries a test, a reason, a named owner and an entry date. No quarantine at all is a pass; a bare quarantine is a fail | Requirement 4 | Executable: schema check over the quarantine file |
| C4b | No quarantine has passed its expiry, default thirty days | Defaults | Executable: date arithmetic over the same file |
| C5 | Every double standing in for a dependency outside the venture's control has a contract file that reaches both the double and the real client from the same parameterisation | Requirement 3 | Executable: AST scan for both symbols under one parameterisation, once the venture lists which dependencies are outside its control |
| C6 | The contract suite detects a seeded drift: run against recorded real responses, it goes red for a stale double | Requirement 3 | Executable, where a recording exists |
| C7 | Every threshold used as a gate states a number, a scope and the command that produces it | Requirement 5 | Partly: config parse finds the number, a person judges the scope wording |
| C7b | Every check named as a gate can fail: it has a command, that command runs in CI, and its non-zero exit blocks | Requirement 5 | Executable: CI config parse, plus one run against a deliberately failing input |
| C8 | No threshold, floor or allowlist moved in the loosening direction in this change | Requirement 2 | Executable: compare gate values against the base commit |
| C9 | The repository declares a full unselected run and its cadence, and the last one is inside that cadence | Requirement 6 | Executable, where CI declares the cadence |
| C10 | Property-based tests in blocking gates pin their seed | Defaults | Executable: config parse |
| C11 | No new commercial or hosted-service dependency was added to satisfy a testing rule | Non-goals, and vendor independence | Executable: manifest and CI diff |
| C12 | Suite exits zero on a clean checkout | All | Executable |

## Judgement checks

- **Was the oracle genuinely independent?** C1 and C2 are proxies. A
  test can pass both and still have been written by reading the
  implementation. The reviewer asks where the expected value came from,
  and the answer should name a specification, a reproduction, an
  invariant or a reference (EV-0007).
- **Is the contract case set worth anything?** A contract suite with
  three shape assertions and no behaviour is a compliance artefact.
  Ask which real incident each case would have caught (EV-0186).
- **Is the double at the right level?** A fake where a container would
  do, or a mock where the real object would do, passes every mechanical
  check and still buys the wrong thing (EV-0187).
- **Was a flake diagnosed or contained?** Containment with a record is
  allowed; the reviewer checks that the product-defect question was
  asked first, because a newly flaky test is a real regression about
  one time in six (EV-0195).
- **Did a verifier exist before the work fanned out?** For parallel
  work the reviewer asks who wrote the acceptance conditions, when, and
  whether any lane could have seen them being written. Lanes agreeing
  with each other is not an answer (WG-DEL-007).
- **Is the timing cell the right one?** The matrix is a default. A
  departure needs a recorded reason, and the reason should be about the
  change class rather than the deadline.
- **Has the harness been staged honestly, or just skipped?** The stage
  layer is a default and defers breadth, not floors. The reviewer checks
  that the risk classes were never deferred, that the cheap tier is a
  command rather than a list, and that the deferral was named at review
  rather than left silent.
- **Does the suite tell the truth about what it covers?** Selection
  hides tests that never run. The reviewer checks that requirement 6 is
  actually satisfied rather than declared (EV-0016).

## What is not checked

- Coverage percentage as a pass or fail. Floors are per surface and
  ratchet upwards; the number is never a universal gate.
- Test count, test-to-code ratio, or layer proportions.
- Mutation score, unless the venture has recorded its own threshold and
  scope (EV-0190).
- How complete the product is. Nothing here fires at a percentage of
  features done, because no standard or study we found gates rigour
  that way.
