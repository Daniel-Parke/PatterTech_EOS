---
id: WG-DATA-006
summary: How is an experiment allowed to end, a locked fixed horizon, an always-valid sequential test, an asymmetric gate, or no experiment at all?
kind: wargame
type: wargame
tags: [data, eos, product, testing, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DATA-002, DOC-DATA-003]
applies_when: [runs_experiment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0059, EV-0312, EV-0313, EV-0315, EV-0316, EV-0317]
review: 2028-01
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DATA-006: How is an experiment allowed to end?

## Decision question and stakes

Traffic is split. At some point somebody says "B won". What earns that
sentence, who is allowed to say it, and when? This is the fork where a
wrong choice does not produce a wrong number, it produces a confident
wrong decision that nobody can later distinguish from a right one.

## Doctrines or coverage gap under pressure

- `DOC-DATA-002` (binding): The randomisation unit, the primary metric and the stopping rule are written down before traffic starts.
- `DOC-DATA-003` (binding): Sample ratio mismatch is checked and reported before any experiment result is read, and a failed check voids the result.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How many units per week can you actually assign, and how long can the
  test run before the answer stops mattering?
- Will anyone look at the dashboard before the end? Answer honestly.
- Is the metric a rate on every unit, or a rare conversion?
- Do you have pre-experiment behaviour for these units?
- What happens if you are wrong, and can you roll it back?

Applicability is `runs_experiment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Fixed horizon, locked in advance

Power the test, compute the sample size, declare the primary metric and
the stopping point, do not look until it lands. Buys: the most power per
unit of traffic, and a decision rule nobody can argue with afterwards.
Costs: it is only valid if nobody looks. Monitoring a fixed-horizon test
continuously can push the false positive rate far above its nominal five
per cent (EV-0313), so the method depends on operator discipline that
most teams do not have.

### B. Always valid, monitor freely

Treat peeking as a property of the stopping rule rather than of the
operator, and use a statistic whose p-values and intervals stay valid at
every moment (EV-0312). Group sequential tests and multiple-comparison
correction ship in a maintained Apache-2.0 library (EV-0317). Buys:
continuous monitoring becomes a supported operation instead of a
violation, and early stopping for harm is legitimate. Costs: validity at
all times is bought with power, so for a fixed effect size it needs more
samples than a fixed-horizon test that is genuinely left alone. Nobody
has measured that penalty at venture sample sizes.

### C. Asymmetric gating

Goal metrics decide the ship; guardrail metrics only block on
statistically significant harm (EV-0059). Buys: it stops a guardrail's
noise from vetoing every launch, and it makes the ship decision one
metric wide. Costs: vendor convention rather than a validated optimum,
and it presumes you named the guardrails correctly in advance.

### D. Do not experiment

Below the traffic where a properly powered test is reachable, decide by
argument, ship behind a flag, and instrument a guardrail. Buys: honesty,
and a faster decision. Costs: you carry the risk of being wrong without
a number to hide behind. This is the common case for a small venture and
none of the sources says it plainly, because none of them was written
for one.

## Failure premises

### Premortem for A. Fixed horizon, locked in advance

Assume `A. Fixed horizon, locked in advance` was selected and the outcome failed. Test this option's stated failure mechanism first: it is only valid if nobody looks. Monitoring a fixed-horizon test continuously can push the false positive rate far above its nominal five per cent (EV-0313), so the method depends on operator discipline that most teams do not have.

### Premortem for B. Always valid, monitor freely

Assume `B. Always valid, monitor freely` was selected and the outcome failed. Test this option's stated failure mechanism first: validity at all times is bought with power, so for a fixed effect size it needs more samples than a fixed-horizon test that is genuinely left alone. Nobody has measured that penalty at venture sample sizes.

### Premortem for C. Asymmetric gating

Assume `C. Asymmetric gating` was selected and the outcome failed. Test this option's stated failure mechanism first: vendor convention rather than a validated optimum, and it presumes you named the guardrails correctly in advance.

### Premortem for D. Do not experiment

Assume `D. Do not experiment` was selected and the outcome failed. Test this option's stated failure mechanism first: you carry the risk of being wrong without a number to hide behind. This is the common case for a small venture and none of the sources says it plainly, because none of them was written for one.

## Decision rule

- Compute the required sample size before anything else. If the test
  cannot reach it inside the window where the answer still matters: D.
- Reachable, and the team can genuinely leave it alone: A.
- Reachable, and somebody will look: B, chosen deliberately and written
  into the stopping rule before traffic starts.
- Any of A, B or D that ships something: C on top, so guardrails block
  only on significant harm.
- Stable units observed before the test, and a metric their pre-period
  behaviour predicts: add variance reduction and re-power. It bought
  roughly half the variance at Bing, which is the same power at half the
  users (EV-0315). It does nothing for first-session funnels or
  anonymous traffic.

## Safe default

A, or D when the arithmetic says A is out of reach. B is the deliberate
alternative when the discipline A needs is not available, and choosing
it is a written decision, not a mid-test rescue.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How many units per week can you actually assign, and how long can the test run before the answer stops mattering?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, or D when the arithmetic says A is out of reach. B is the deliberate alternative when the discipline A needs is not available, and choosing it is a written decision, not a mid-test rescue.

**Exit condition:** Stop or roll back the selected branch when it is only valid if nobody looks. Monitoring a fixed-horizon test continuously can push the false positive rate far above its nominal five per cent (EV-0313), so the method depends on operator discipline that most teams do not have, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How many units per week can you actually assign, and how long can the test run before the answer stops mattering?

## Counter-evidence and transfer limits

### Preserved reasoning: What binds regardless of which you pick

- The randomisation unit, the primary metric and the stopping rule are
  written down before traffic starts (B4).
- Sample ratio mismatch is checked and reported before the result is
  read, and a failed check voids the result outright (B5). The causes
  sort into assignment, execution, log processing, telemetry and
  interference, which is a search order rather than just a red light
  (EV-0316).
- A surprisingly large effect is evidence of a bug before it is evidence
  of a win (EV-0313).
### Preserved reasoning: The standoff, stated plainly

One peer-reviewed position treats peeking as a misunderstanding to be
corrected. Another treats it as a stopping-rule property and fixes the
statistic instead. Both are right inside their own frame and they
disagree about whether the operator or the mathematics should change.
This Wargame sides with the first and names the second as the deliberate
alternative, which is a judgement about which failure is more likely in
a small team, not a finding.

Scope note on the numbers. The base rate of roughly eighty-five to
ninety per cent of ideas failing to move the metric is measured on
mature products at scale where the obvious wins are gone. A young
product may face a better prior. Use it to argue for humility, never as
a computed input.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
