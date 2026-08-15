---
summary: Every material control in the EOS, classified by what actually enforces it, with the file and the test behind each classification
type: org
tags: [eos]
---

# Control enforcement

Written 2026-08-15 against commit `14d4ad7` on
`eos/audit-research-expansion`. The repository's first rule is that a
control which is not built must not be described as though it were, and
this file is the audit of that rule against itself. Every row was
checked in the code or the workflow, not in the prose that describes
them.

## The six classes

1. **Documented expectation.** Advice or policy. Nothing reads it.
2. **Procedural.** A person or agent has to follow a step. Nothing fires
   if they do not.
3. **Detective.** A command reports the breach after or during the act.
4. **Preventive.** A command refuses the act.
5. **Platform-enforced.** CI, branch protection or another system runs
   it without anyone choosing to.
6. **Runtime-audited.** Observable and reviewable while it operates.

A control can sit in more than one class. What matters is the weakest
class a reader could mistake for the strongest.

## What CI actually runs

`.github/workflows/checks.yml` has two steps, on every push and pull
request, across ubuntu and windows against CPython 3.11 and 3.14:

```
python -m tools.eos check
python -m pytest tests -q
```

That is 34 registered checks and 533 tests. Everything else in this file
that is described as enforced is enforced by somebody typing a command.

## Platform-enforced

These run in CI. A breach fails the build.

| Control | Where claimed | Mechanism |
| --- | --- | --- |
| `AGENTS.md` and `CLAUDE.md` are byte identical | `GOVERNANCE.md` | E003, `structural.py:529` compares bytes |
| Both routers are at most 40 lines | `GOVERNANCE.md` | E007, `structural.py:667`, error severity. The only line budget that fails a build |
| No em-dash in prose | `packs/writing-content/PACK.md` | E004, `structural.py:548`, error. Exclamation marks and clichés warn, and the prose says so |
| Derived files match their generator | `GOVERNANCE.md` | E001 for the five index outputs, E011 for the two task views |
| A `derived: true` file has a registered generator | `GOVERNANCE.md` | S005, `semantic.py:393`. Exactly seven files carry the flag and they are exactly the seven in the table |
| Supersession pairs resolve both ways | `GOVERNANCE.md` | S002, `semantic.py:201`. **Scoped to markdown front-matter only**, see the gap below |
| A recorded commit is an ancestor of HEAD | `GOVERNANCE.md` | S007, `semantic.py:451` |
| A derived view does not claim git was unavailable when it was not | this pass | S020, `semantic.py`, added 2026-08-15 |
| A venture pin resolves and is reachable | `GOVERNANCE.md` | S010, `semantic.py:658` |
| Frozen benchmark files match their hashes | `benchmark/FREEZE_MANIFEST.json` | B001, `freeze.py`, 130 files |
| The tag vocabulary is parsed from `GOVERNANCE.md` | `GOVERNANCE.md` | E009. Warn severity, as claimed |
| Every subcommand, flag and task op is documented | `README.md` | Three tests parse `tools/CLI_CONTRACTS.md` |
| The dependency lock serves every platform CI builds | this pass | `tests/test_gen_lock.py`, added 2026-08-15 |

## Detective at a command, procedural in practice

Real mechanisms. Nothing runs them for you.

| Control | Mechanism | What is missing |
| --- | --- | --- |
| Tier ruling and the merge gate | `router.py`, 13 factors; `route --diff` recomputes and only ever raises | No CI job, no hook, no branch protection. `TOUR.md` and `kernel/POLICY_SPEC.md` both say so plainly |
| Protected-set touch | `route` exits 3 when a diff touches a protected path with no `--adr` | It fires only if somebody runs `route --diff`, and it checks that a value was passed, never that the ADR exists |
| The seed rubric | `check --seed`, D001 to D011, 702 lines | Not in CI, and there are no seeds in this repository, so the D series never runs here outside the tests |
| Pack acceptance drills | 22 frozen specs, 199 graders | Run by hand. As of 2026-08-15 all 22 have a recorded discrimination result and none has a pack verdict, because no command supplies the cold-agent session |
| Claim discipline | `task new` and `update` refuse an unnamed session; `claims-verify` reports C001 to C005 | With an empty lanes list nothing is gated, which `OPERATORS_GUIDE.md` states correctly as "the release rather than a lock" |

## Preventive, with a named limit

| Control | Mechanism | Limit |
| --- | --- | --- |
| The guard fails closed | `guard.py`, 10 classes, 4 verdicts. A missing, malformed or failing mapping clamps to manual-only | Verified offline at mapping level only. `kernel/adapters/claude-code.json` records `host_run: false`, so no live session has ever been guarded |
| Six classes never execute on an agent's authority | `org/policy.json` `approvals.always_human`, read at `guard.py:422` | Depends on the host adapter actually calling the guard |
| Three of ten guarded classes are covered | The adapter's own record | The other seven stay manual-only. No class rules `allow` |

## Documented expectation only

Nothing reads these. Each is disclosed somewhere, and the third column
says whether the disclosure is where a reader would look.

| Control | Disclosed | Adequately |
| --- | --- | --- |
| `parallelism.max_lanes` | `OPERATORS_GUIDE.md`, `org/migration/MIGRATION_MAP.md` | Yes. The v2.1 build ran twelve lanes against a value of four |
| `parallelism.claim_expiry_hours`, `renewal_window_hours` | `OPERATORS_GUIDE.md`, added 2026-08-15 | Now. Before this pass the block had one value disclosed as inert and two silent, which reads as though the silent two work |
| `org/capability-profile.json` | `OPERATORS_GUIDE.md` | Yes. Read by no code at all |
| Standing-exception expiry | `kernel/POLICY_SPEC.md` | Yes. "No check reads expiry dates" |
| Spike branches that never merge | `kernel/POLICY_SPEC.md` | Yes. Held by the exploration playbook. No `spike` match exists in `tools/`, `tests/` or `.github/` |
| Task record at 40 lines, review verdict at 10 | `GOVERNANCE.md` | Yes. "Nothing measures either" |
| The 500-line pack body budget | `GOVERNANCE.md` | Yes. Kept by review alone |
| The 11-point pack definition of done | `packs/PACK_SHAPE.md` | **No.** See the gap below |
| `risk.factors`, `path_patterns.reversible`, `protected_pointers` in policy | `kernel/POLICY_SPEC.md`, `tools/CLI_CONTRACTS.md` | Yes. Validated at seed time, consulted by no ruling |

## The gaps worth naming

**The routing layer was inert for the whole v2.1 build.** Routing at
record creation reads declarations and passes an empty dict for the
derived half (`taskops.py:157`). Of the first 25 task records, 21 ruled
R0 with an empty reasons list, 23 declared no side effect, and on 22 the
ruled tier came out below the tier the author proposed. T-0013 proposed
R3 and was ruled R0. The mechanism is sound and the gate that would have
caught it is a command nobody is recorded as having run. `task new` now
says which of the two cases produced a ruling, but that is honesty about
the gap and not a closing of it.

**S002 does not cover the ledgers.** `GOVERNANCE.md` says supersession
is explicit, bidirectional and that the checker enforces the pair. S002
iterates markdown front-matter. `registry/evidence.json` has no
supersession fields at all, and no lesson row uses them. The written
rule and the enforced rule have parted company, and closing it is
research-programme work rather than a repair.

**The pack definition of done is review-held.** Eleven points in
`packs/PACK_SHAPE.md`; S006 checks that three organs exist and S015
that two front-matter keys are present. Points 4, 6, 7, 9, 10 and 11,
which are the ones about three materially different patterns, worked
examples, three maintained primary sources and counter-evidence, are
kept by whoever reviews. Nothing overtly claims otherwise, but eleven
numbered points sitting next to a repository full of check ids invite
the inference.

**Release gate 8 is now satisfiable in principle and unmet in fact.**
`benchmark/PROTOCOL.md` asks that pack drills pass. Until 2026-08-15
every drill carried a null verdict, so the gate could not be evaluated
at all. It now can be, and it is not met: the recorded verdicts are the
discrimination check against untouched fixtures, which is not evidence
about any pack.

## The shape of it

CI enforces document consistency, and it does that thoroughly across
four platform and version pairs. The four controls that gate actual risk
are the router, the guard, the seed rubric and the drills, and every one
of them runs only when a person types the command. The repository states
this in `TOUR.md` and `kernel/POLICY_SPEC.md` rather than hiding it,
which is why the asymmetry is a finding about practice and not about
honesty. The 1.0 gate is where it has to be closed.
