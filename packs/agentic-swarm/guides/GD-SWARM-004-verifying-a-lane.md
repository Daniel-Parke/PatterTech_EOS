---
summary: What decides that a lane's work is good, and who is allowed to have written it?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
scope: estate
sources: [EV-0006, EV-0053, EV-0105, EV-0111, EV-0178, EV-0251]
review: on-change-of:agent-harness-major-release
type: guide
tags: [eos, delivery, testing]
---

# GD-SWARM-004: what decides a lane is done?

## The question

A lane returns and says it is finished. Something other than the lane
has to agree. The fork is what that something is, and the rule that
matters more than the form is who wrote it: the artefact that decides a
lane's success is authored outside the lane, before it runs, without
the lane's context. `packs/agentic-development/PACK.md` B4 already says
evaluation is separate from generation and holds external truth. This
guide is about which oracle to reach for in a graph, and how lane count
follows from the answer.

## It depends on

- **Decidability.** Does the check give a verdict a script can read, or
  does it give an opinion?
- **Who can author it without seeing the implementation.** The
  authoring context may hold the specification, the interface and prior
  art. It may not hold the candidate code.
- **Whether it has been shown to bite.** A suite that has never been
  seen to fail has not been shown to be capable of failing.
- **Where the behaviour lives.** Cross-lane behaviour is the
  integrator's oracle, never a lane's, because every lane can pass
  while the composition is wrong.
- **Blast radius of a wrong pass.** Money, auth, deletion, migration
  and public contracts do not take a machine-only path.

## Options

### A. Decidable external oracle
A conformance suite, a reference implementation to diff against, a
property or a metamorphic relation. Buys per-unit verdicts, which is
what makes wide fan-out safe: it is the condition under which sixteen
lanes worked, and the author's stated constraint was that the verifier
must be nearly perfect (EV-0053). Costs authoring, and most business
software has nothing like it.

### B. Executable acceptance authored ahead of the lane
Tests, contract checks or an acceptance script written from the
specification by somebody other than the implementing lane. Buys
external truth without a reference implementation. Costs the authoring
pass, and it is only as good as the specification clause it came from.

### C. Repository-level always-on gates
Strictest type checking, static analysis tuned to a low effective
false-positive rate, sanitisers, secret scanning, dependency
resolution. Buys the classes agents emit systematically and never write
tests for, at near-zero marginal cost per lane. Costs tuning, and it
catches shape rather than intent.

### D. Clean-context reviewer
A model that did not write the work, seeing the diff and the criteria
but not the reasoning that produced them, asked to describe behaviour
and compare it against the requirement. Buys coverage of things rules
cannot express. Costs determinism, and it must not be weaker than the
writer, must not be asked to fix in the same pass, and must never be
the sole gate. A model judge reaches roughly human-level agreement on
preference and carries documented position and self-preference biases
(EV-0251).

### E. A person at the gate
Buys judgement and accountability. Costs the scarcest thing in the run.
Spend it confirming that the acceptance criteria say what was meant,
not reading the diff, because contract incompleteness rather than
implementation error is the documented escape route.

## Decision rule

C always, for every lane, because it is cheap and it catches what
nobody writes tests for. Then A where an oracle exists or can be built,
and let lane count be as wide as the oracle is strong. B where it does
not, at one or two lanes. D beside A or B, never instead. E at the
merge gate whenever A is absent, and always for the excluded classes:
authentication and authorisation, secrets, money, data deletion and
migration, public API contracts, and any file previously implicated in
an incident.

Two constraints ride on top whatever is chosen. The lane may not write
to its own harness: test files, fixtures, evaluation scripts and CI
configuration for the node being judged are outside its write set.
And agreement between lanes is not a verdict, however many lanes agree.

## Default

C plus B, with D beside it and E at the gate. No fan-out beyond two
lanes without A. Report the mutation score on the changed lines rather
than a coverage percentage, because coverage is not the meter
(EV-0105).

## Worked rulings

- **PatterTech_EOS, 2026-08-10, argued.** C plus E. The repository
  checker predates every lane and is mechanical, so it is C; prose
  quality has no machine oracle, so acceptance is a person at the gate.
  No lane may weaken or delete a check to pass, which is the floor the
  estate already carries.

## Notes

Ordering is ceremony and independence is not. Forcing a frontier model
to write tests across about 500 benchmark tasks changed the number
resolved by zero (EV-0006), and the ingredient the older evidence
actually supports is small uniform work increments rather than the
sequence (EV-0178). Meanwhile, prompting an oracle author with the
buggy implementation instead of the specification cut bug-revealing
tests by about two thirds, and self-review without external feedback
degrades the answer (EV-0111). Drop the ritual; keep the separation.
