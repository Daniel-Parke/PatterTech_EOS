---
id: WG-AGENT-004
summary: What holds the truth that checks an agent's work, and what do you do when nothing does?
kind: wargame
type: wargame
tags: [delivery, eos, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-AGENT-002]
applies_when: [builds_agent_workflow]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0053, EV-0076, EV-0087, EV-0089, EV-0108, EV-0109, EV-0111, EV-0115, EV-0119, EV-0120]
review: on-change-of:anthropic-evals-publication
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-AGENT-004: What checks the work?

## Decision question and stakes

An agent that cannot be checked cannot be trusted to iterate. The fork
is what holds the ground truth: a machine oracle, a rule set, another
model, or a person. Get this wrong and an evaluator-optimizer loop
becomes an expensive way to make the answer worse.

## Doctrines or coverage gap under pressure

- `DOC-AGENT-002` (binding): Irreversible or externally visible acts pass a human checkpoint.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Oracle quality**: is there something outside the generator that
  says right or wrong, and how complete is it?
- **Reversibility**: what does a wrong answer that gets through cost?
- **Determinism**: does the same input give the same verdict?
- **Latency and cost**: how often can the check run?
- **Coverage**: does the check see the whole output or a slice?

Applicability is `builds_agent_workflow`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Machine oracle
Tests, type checkers, compilers, schema validators, linters. Buys
deterministic external truth, cheap to run repeatedly, and it is the
condition under which self-directed iteration reliably improves work
(EV-0053, EV-0111). Costs authoring, and it only covers what it
asserts.

### B. Defined rules and mechanical checks
Explicit assertions the output must satisfy: required sections,
forbidden strings, line budgets, shape checks. Buys determinism where
no test suite is possible, and it is ranked above a model judge in
vendor guidance (EV-0115). Costs expressiveness, since taste does not
reduce to regex.

### C. Model as judge
A separate model, separate context, scoring against a rubric. Buys
coverage of things rules cannot express. Costs determinism and
calibration, and it is worth nothing at all if the judge is the same
context that generated the work, because intrinsic self-correction
without external feedback degrades answers (EV-0111, EV-0089).

### D. Human review at a checkpoint
A person looks before the act lands. Buys judgement and accountability.
Costs latency, and it does not scale to every output (EV-0108).

## Failure premises

### Premortem for A. Machine oracle

Assume `A. Machine oracle` was selected and the outcome failed. Test this option's stated failure mechanism first: authoring, and it only covers what it asserts.

### Premortem for B. Defined rules and mechanical checks

Assume `B. Defined rules and mechanical checks` was selected and the outcome failed. Test this option's stated failure mechanism first: expressiveness, since taste does not reduce to regex.

### Premortem for C. Model as judge

Assume `C. Model as judge` was selected and the outcome failed. Test this option's stated failure mechanism first: determinism and calibration, and it is worth nothing at all if the judge is the same context that generated the work, because intrinsic self-correction without external feedback degrades answers (EV-0111, EV-0089).

### Premortem for D. Human review at a checkpoint

Assume `D. Human review at a checkpoint` was selected and the outcome failed. Test this option's stated failure mechanism first: latency, and it does not scale to every output (EV-0108).

## Decision rule

If a machine oracle exists or can be written in reasonable time, A, and
put the generating step inside an evaluator-optimizer loop. If not, B
for everything that reduces to a mechanical assertion. Use C only as a
separate context with a written rubric, and never as the sole gate on
anything irreversible. Use D at every irreversible or externally
visible act regardless of what else is in place, because that is
binding requirement B3. Where none of A, B or C hold, say the output
has no external oracle and do not claim an iteration loop for it. That
statement is a legitimate answer and is more useful than a judge
nobody believes.

Guardrails are a different thing from evaluation: cheap checks that run
beside the work and trip a wire, registered at the runner rather than
inside an agent so no agent can configure them away (EV-0076, EV-0120,
EV-0119).

## Safe default

A where an oracle exists, B where it does not, D at every irreversible
act. Evaluation suites start at twenty to fifty tasks harvested from
real failures and score pass@k and pass^k, because a single green run
proves little against a non-deterministic system (EV-0087).

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Oracle quality**: is there something outside the generator that says right or wrong, and how complete is it?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A where an oracle exists, B where it does not, D at every irreversible act. Evaluation suites start at twenty to fifty tasks harvested from real failures and score pass@k and pass^k, because a single green run proves little against a non-deterministic system (EV-0087).

**Exit condition:** Stop or roll back the selected branch when authoring, and it only covers what it asserts, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Oracle quality**: is there something outside the generator that says right or wrong, and how complete is it?

## Counter-evidence and transfer limits

### Preserved reasoning: Notes

Absent verification is one of the three failure clusters that dominate
annotated multi-agent traces, alongside specification gaps and
inter-agent misalignment (EV-0109). Whoever writes the oracle should
not be holding the implementation in context; that separation is the
one this estate kept from v1.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
